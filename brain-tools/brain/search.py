"""Hybrid recall for a brain vault: BM25 keywords + optional local embeddings.

Tier 1 (always on): BM25 over heading-aware chunks. Standard library only.
Tier 2 (optional):  vector similarity using a local Ollama embedding model.
Results from both are merged with Reciprocal Rank Fusion (RRF).

The index lives in <vault>/.brain/index.sqlite and is rebuilt incrementally:
only files whose content hash changed are re-chunked and re-embedded.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sqlite3
import struct
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from .vault import chunk_note, iter_markdown, load_note

STOP = set("""a an and are as at be but by can do does for from has have how i if in into is it its
of on or our so that the their them then there these they this to was we were what when where which
who why will with you your not no yes than too very just also about over under more most""".split())
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9\-_.]*[a-z0-9]|[a-z0-9]")

# Files agents read directly, never via search.
NOT_SEARCHED_ROOT = {"index.md", "log.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md"}
NOT_SEARCHED_DIRS = ("skills/", "memory/reports/")
# Small rank-fusion bonus so compiled pages beat the raw text they came from (raw is still searchable).
FOLDER_PRIOR = {"wiki/": 0.004, "memory/": 0.002}

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
EMBED_MODEL = os.environ.get("BRAIN_EMBED_MODEL", "nomic-embed-text")
# Bump when chunking changes, so an upgrade re-chunks every file instead of only edited ones.
CHUNKER_VERSION = "2"  # 2: every chunk carries its note's summary and aliases


def tokenize(text: str) -> list[str]:
    toks = TOKEN_RE.findall(text.lower())
    return [t for t in toks if t not in STOP and len(t) > 1]


# ---------------------------------------------------------------- embeddings
def embed(texts: list[str], kind: str = "document") -> list[list[float]] | None:
    """Embed texts with Ollama. Returns None if Ollama is not reachable.

    nomic-embed-text expects task prefixes; other models ignore them harmlessly.
    """
    if not texts:
        return []
    prefix = "search_query: " if kind == "query" else "search_document: "
    payload = json.dumps({"model": EMBED_MODEL, "input": [prefix + t for t in texts]}).encode()
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/embed", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["embeddings"]
    except (urllib.error.URLError, OSError, KeyError, ValueError):
        return None


def _pack(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)


def _unpack(b: bytes) -> list[float]:
    return list(struct.unpack(f"{len(b) // 4}f", b))


def _cos(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


# ---------------------------------------------------------------- index
class BrainIndex:
    def __init__(self, root: Path):
        self.root = Path(root)
        (self.root / ".brain").mkdir(exist_ok=True)
        self.db = sqlite3.connect(self.root / ".brain" / "index.sqlite")
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, hash TEXT, title TEXT, type TEXT, summary TEXT);
            CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY, path TEXT, heading TEXT, text TEXT, vec BLOB);
            CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);
            CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
            """
        )

    def close(self):
        self.db.close()

    # -- build
    def update(self, use_embeddings: bool = True) -> dict:
        """Re-index changed files. Returns counts for reporting."""
        seen, changed, embedded = set(), 0, 0
        ver = self.db.execute("SELECT v FROM meta WHERE k='chunker'").fetchone()
        if not ver or ver[0] != CHUNKER_VERSION:
            self.db.execute("DELETE FROM files")
            self.db.execute("DELETE FROM chunks")
            self.db.execute("INSERT OR REPLACE INTO meta VALUES('chunker', ?)", (CHUNKER_VERSION,))
        known = dict(self.db.execute("SELECT path, hash FROM files"))
        model = self.db.execute("SELECT v FROM meta WHERE k='embed_model'").fetchone()
        if use_embeddings and model and model[0] != EMBED_MODEL:
            self.db.execute("UPDATE chunks SET vec=NULL")  # model changed: vectors are incomparable
        for p in iter_markdown(self.root):
            rel = p.relative_to(self.root).as_posix()
            if rel in NOT_SEARCHED_ROOT or rel.startswith(NOT_SEARCHED_DIRS):
                continue
            note = load_note(self.root, p)
            seen.add(note.path)
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if known.get(note.path) == h:
                continue
            changed += 1
            self.db.execute("DELETE FROM chunks WHERE path=?", (note.path,))
            self.db.execute(
                "INSERT OR REPLACE INTO files VALUES(?,?,?,?,?)",
                (note.path, h, note.title, str(note.meta.get("type", "")), note.summary),
            )
            for c in chunk_note(note):
                self.db.execute("INSERT INTO chunks(path, heading, text) VALUES(?,?,?)",
                                (c["path"], c["heading"], c["text"]))
        for gone in set(known) - seen:
            self.db.execute("DELETE FROM files WHERE path=?", (gone,))
            self.db.execute("DELETE FROM chunks WHERE path=?", (gone,))
        ollama = None
        if use_embeddings:
            todo = self.db.execute("SELECT id, heading, text FROM chunks WHERE vec IS NULL").fetchall()
            for i in range(0, len(todo), 32):
                batch = todo[i:i + 32]
                vecs = embed([f"{h}\n{t}" for _, h, t in batch])
                if vecs is None:
                    ollama = False
                    break
                ollama = True
                for (cid, _, _), v in zip(batch, vecs):
                    self.db.execute("UPDATE chunks SET vec=? WHERE id=?", (_pack(v), cid))
                    embedded += 1
            if ollama:
                self.db.execute("INSERT OR REPLACE INTO meta VALUES('embed_model', ?)", (EMBED_MODEL,))
        self.db.commit()
        total = self.db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        with_vec = self.db.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
        return {"files": len(seen), "changed": changed, "removed": len(set(known) - seen),
                "chunks": total, "embedded_now": embedded, "chunks_with_vectors": with_vec,
                "ollama": {None: "skipped", True: "ok", False: "unreachable"}[ollama]}

    # -- query
    def search(self, query: str, k: int = 8, mode: str = "hybrid", path_prefix: str | None = None) -> list[dict]:
        """Return the best-matching notes (one hit per note, best chunk shown).

        mode: "keyword", "semantic", or "hybrid" (falls back to keyword if no vectors).
        """
        rows = self.db.execute("SELECT id, path, heading, text, vec FROM chunks").fetchall()
        if path_prefix:
            rows = [r for r in rows if r[1].startswith(path_prefix)]
        if not rows:
            return []
        rankings: list[list[int]] = []
        scores: dict[str, dict[int, float]] = {}

        if mode in ("keyword", "hybrid"):
            bm = self._bm25(query, rows)
            scores["keyword"] = bm
            rankings.append(sorted(bm, key=bm.get, reverse=True)[:50])

        used_vectors = False
        if mode in ("semantic", "hybrid") and any(r[4] for r in rows):
            qv = embed([query], kind="query")
            if qv:
                used_vectors = True
                sem = {r[0]: _cos(qv[0], _unpack(r[4])) for r in rows if r[4]}
                scores["semantic"] = sem
                rankings.append(sorted(sem, key=sem.get, reverse=True)[:50])
        if mode == "semantic" and not used_vectors:
            bm = self._bm25(query, rows)
            scores["keyword"] = bm
            rankings.append(sorted(bm, key=bm.get, reverse=True)[:50])

        fused: Counter = Counter()
        for ranking in rankings:
            for rank, cid in enumerate(ranking, start=1):
                fused[cid] += 1.0 / (60 + rank)  # RRF, k=60
        by_id = {r[0]: r for r in rows}
        best_per_note: dict[str, tuple[float, int]] = {}
        qtoks = set(tokenize(query))
        for cid, s in fused.items():
            path = by_id[cid][1]
            # small boost when query words appear in the note's file name / heading trail
            name_hits = len(qtoks & set(tokenize(Path(path).stem.replace("-", " ") + " " + by_id[cid][2])))
            s += 0.004 * name_hits
            s += next((v for k, v in FOLDER_PRIOR.items() if path.startswith(k)), 0.0)
            if path not in best_per_note or s > best_per_note[path][0]:
                best_per_note[path] = (s, cid)
        ranked = sorted(best_per_note.items(), key=lambda kv: kv[1][0], reverse=True)[:k]
        files = {p: (t, ty, su) for p, _, t, ty, su in self.db.execute("SELECT * FROM files")}
        out = []
        for path, (s, cid) in ranked:
            _, _, heading, text, _ = by_id[cid]
            title, typ, summary = files.get(path, (Path(path).stem, "", ""))
            out.append({
                "path": path, "title": title, "type": typ, "score": round(s, 5),
                "heading": heading, "snippet": _snippet(text, qtoks),
                "summary": summary, "via": "hybrid" if used_vectors and mode != "keyword" else "keyword",
            })
        return out

    def _bm25(self, query: str, rows, k1: float = 1.4, b: float = 0.75) -> dict[int, float]:
        q = tokenize(query)
        if not q:
            return {}
        docs = {r[0]: tokenize(f"{r[2]} {r[3]}") for r in rows}
        n = len(docs)
        avgdl = sum(len(d) for d in docs.values()) / max(n, 1)
        df: Counter = Counter()
        for toks in docs.values():
            df.update(set(toks))
        out = {}
        for cid, toks in docs.items():
            tf = Counter(toks)
            s = 0.0
            for t in q:
                if t not in tf:
                    continue
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(toks) / avgdl))
            if s > 0:
                out[cid] = s
        return out

    def stats(self) -> dict:
        f = self.db.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        c = self.db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        v = self.db.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
        m = self.db.execute("SELECT v FROM meta WHERE k='embed_model'").fetchone()
        return {"files": f, "chunks": c, "chunks_with_vectors": v, "embed_model": m[0] if m else None}


def _snippet(text: str, qtoks: set[str], width: int = 260) -> str:
    low = text.lower()
    pos = min((low.find(t) for t in qtoks if low.find(t) >= 0), default=0)
    start = max(0, pos - width // 3)
    s = text[start:start + width].strip()
    return ("…" if start > 0 else "") + s + ("…" if start + width < len(text) else "")
