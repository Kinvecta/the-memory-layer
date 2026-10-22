"""Read a brain vault: notes, frontmatter, wikilinks, chunks.

Standard library only. A "vault" is any folder of markdown files; Obsidian is
optional. Paths returned by this module are POSIX-style and relative to the
vault root (e.g. "wiki/concepts/tokens.md").
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

# Folders never indexed or linted (tool state, app config, templates).
SKIP_DIRS = {".git", ".obsidian", ".brain", ".trash", ".claude", ".agents", "templates", "node_modules"}

WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
CODE_RE = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)


def vault_root(explicit: str | os.PathLike | None = None) -> Path:
    """Resolve the vault: explicit arg, then $BRAIN_VAULT, then the current dir."""
    root = explicit or os.environ.get("BRAIN_VAULT") or os.getcwd()
    p = Path(root).expanduser().resolve()
    if not p.is_dir():
        raise FileNotFoundError(f"Vault folder not found: {p}")
    return p


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse a small YAML subset: `key: value`, `key: [a, b]`, and `- item` lists.

    Good enough for note properties; avoids a PyYAML dependency.
    """
    m = FM_RE.match(text)
    if not m:
        return {}, text
    data: dict = {}
    key = None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key is not None:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(_scalar(line.lstrip()[2:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                data[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                data[key] = [_scalar(v) for v in _split_list(inner)] if inner else []
            else:
                data[key] = _scalar(val)
    return data, text[m.end():]


def _split_list(s: str) -> list[str]:
    out, buf, depth, quote = [], "", 0, None
    for ch in s:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(buf.strip())
            buf = ""
            continue
        buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


def _scalar(v: str):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


@dataclass
class Note:
    path: str                      # relative POSIX path
    title: str
    meta: dict
    body: str
    links: list[str] = field(default_factory=list)   # raw link targets
    mtime: float = 0.0

    @property
    def stem(self) -> str:
        return Path(self.path).stem

    @property
    def summary(self) -> str:
        s = self.meta.get("summary")
        if s:
            return str(s)
        for para in self.body.split("\n\n"):
            p = para.strip()
            if p and not p.startswith("#") and not p.startswith(">") and not p.startswith("|"):
                return re.sub(r"\s+", " ", p)[:200]
        return ""


def iter_markdown(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield Path(dirpath) / fn


def load_note(root: Path, path: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    rel = path.relative_to(root).as_posix()
    m = re.search(r"^#\s+(.+)$", body, re.M)
    title = str(meta.get("title") or (m.group(1).strip() if m else path.stem))
    # Like Obsidian, links inside code blocks and inline code are not links.
    linkable = CODE_RE.sub(" ", body)
    links = [t.strip() for bang, t in WIKILINK_RE.findall(linkable) if not bang]
    # Frontmatter can link too, e.g. sources: ["[[raw/x]]"]
    for v in meta.values():
        for item in v if isinstance(v, list) else [v]:
            if isinstance(item, str):
                links += [t.strip() for bang, t in WIKILINK_RE.findall(item) if not bang]
    return Note(rel, title, meta, body, links, path.stat().st_mtime)


def load_vault(root: Path) -> dict[str, Note]:
    return {n.path: n for n in (load_note(root, p) for p in iter_markdown(root))}


class LinkResolver:
    """Resolve [[target]] the way Obsidian does: full path, then unique file name."""

    def __init__(self, paths):
        self.paths = set(paths)
        self.by_stem: dict[str, list[str]] = {}
        self.all_files: set[str] = set()
        for p in self.paths:
            self.by_stem.setdefault(Path(p).stem.lower(), []).append(p)

    def add_files(self, files):
        """Non-markdown files (PDFs, images) that links may point at."""
        self.all_files |= set(files)

    def resolve(self, target: str) -> str | None:
        t = target.strip().lstrip("/")
        cands = [t, t + ".md"]
        for c in cands:
            if c in self.paths or c in self.all_files:
                return c
        hits = self.by_stem.get(Path(t).stem.lower() if "/" in t else t.lower())
        if hits:
            if "/" in t:
                hits = [h for h in hits if h.endswith(t + ".md") or h.endswith(t)] or hits
            return sorted(hits, key=len)[0]
        for f in self.all_files:
            if f.endswith("/" + t) or f == t:
                return f
        return None


def chunk_note(note: Note, max_words: int = 220) -> list[dict]:
    """Split a note into heading-aware chunks for search.

    Each chunk keeps its heading trail so a hit says *where* in the note it is.
    """
    chunks: list[dict] = []
    trail: list[str] = [note.title]
    buf: list[str] = []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            words = text.split()
            for i in range(0, len(words), max_words):
                piece = " ".join(words[i:i + max_words])
                chunks.append({"path": note.path, "heading": " > ".join(trail), "text": piece})
        buf.clear()

    for line in note.body.splitlines():
        h = HEADING_RE.match(line)
        if h:
            flush()
            level = len(h.group(1))
            trail[:] = trail[: max(1, level)] if level > 1 else [h.group(2).strip()]
            if level > 1:
                trail.append(h.group(2).strip())
            continue
        buf.append(line)
    flush()
    # Summary and aliases make the note findable by its synonyms (e.g. "MCP", "RAG").
    extra = " ".join(filter(None, [str(note.meta.get("summary") or ""),
                                   " ".join(map(str, note.meta.get("aliases") or []))
                                   if isinstance(note.meta.get("aliases"), list) else str(note.meta.get("aliases") or "")]))
    if extra:
        for c in chunks:  # stamp every chunk, so each one carries its note's context
            c["text"] = extra + "\n" + c["text"]
    if not chunks:
        chunks.append({"path": note.path, "heading": note.title, "text": note.title})
    return chunks
