"""Health checks for a brain vault (the "lint" operation, deterministic part).

The model does the judgment calls (contradictions, missing concepts). This
script finds the mechanical problems so the model knows where to look.
"""
from __future__ import annotations

import datetime as dt
import os
import re
from pathlib import Path

from .vault import LinkResolver, load_vault

REQUIRED = {"type", "created", "updated"}
WIKI_TYPES = {"concept", "entity", "source", "decision", "comparison", "question"}
STALE_DAYS = int(os.environ.get("BRAIN_STALE_DAYS", "90"))
# Invisible characters used to hide instructions in rules files ("Rules File Backdoor", 2025):
# zero-width spaces/joiners, bidi embeddings, overrides and isolates, word joiner, BOM mid-file, tag characters.
HIDDEN = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]")
# Lines in raw/ or inbox/ that read like orders to an AI. Flagged for a human, never followed.
INJECTION = re.compile(
    r"(ignore|disregard|forget)\s+(all\s+|any\s+|your\s+|the\s+)?(previous\s+|prior\s+|above\s+)?(rules|instructions|prompts?)"
    r"|\byou are now\b|\bnew instructions\b"
    r"|\b(send|copy|post|upload|email|forward)\b[^\n]{0,60}\b(to|at)\b[^\n]{0,40}(https?://|www\.|@)",
    re.IGNORECASE)
# A person lists files they have checked here; lint stops flagging them (hidden characters, injection).
REVIEWED_FLAGS = "memory/reviewed-flags.md"
MANUAL_MAX_LINES = 200
MANUAL_MAX_BYTES = 32 * 1024
SYSTEM_FILES = {"index.md", "log.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md"}


def lint(root: Path, today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    notes = load_vault(root)
    resolver = LinkResolver(notes)
    resolver.add_files(
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and not p.name.endswith(".md") and not any(part.startswith(".") for part in p.relative_to(root).parts)
    )
    issues: dict[str, list] = {k: [] for k in (
        "broken_links", "orphans", "missing_frontmatter", "stale", "not_in_index",
        "raw_without_source_page", "low_confidence", "oversized_core",
        "hidden_characters", "oversized_manual", "injection_suspects", "review_due", "disputed")}

    inbound: dict[str, int] = {p: 0 for p in notes}
    for n in notes.values():
        for t in n.links:
            hit = resolver.resolve(t)
            if hit is None:
                issues["broken_links"].append({"from": n.path, "link": t})
            elif hit in inbound and hit != n.path:
                inbound[hit] += 1

    index_text = notes["index.md"].body if "index.md" in notes else ""
    index_targets = {resolver.resolve(t) for t in re.findall(r"\[\[([^\]|#]+)", index_text)}

    for p, n in notes.items():
        if not p.startswith("wiki/"):
            continue
        missing = REQUIRED - set(n.meta)
        if missing:
            issues["missing_frontmatter"].append({"path": p, "missing": sorted(missing)})
        elif n.meta.get("type") not in WIKI_TYPES:
            issues["missing_frontmatter"].append({"path": p, "bad_type": n.meta.get("type")})
        if inbound[p] == 0:
            issues["orphans"].append(p)
        if p not in index_targets:
            issues["not_in_index"].append(p)
        reviewed = n.meta.get("last_reviewed") or n.meta.get("updated")
        try:
            d = dt.date.fromisoformat(str(reviewed)[:10])
            if (today - d).days > STALE_DAYS:
                issues["stale"].append({"path": p, "last_reviewed": str(d), "days": (today - d).days})
        except ValueError:
            pass
        due = n.meta.get("review_after")
        if due:
            try:
                d = dt.date.fromisoformat(str(due)[:10])
                if d < today:
                    issues["review_due"].append({"path": p, "review_after": str(d)})
            except ValueError:
                pass
        if str(n.meta.get("status", "")).lower() == "disputed":
            issues["disputed"].append(p)
        if str(n.meta.get("confidence", "")).lower() == "low":
            issues["low_confidence"].append(p)

    # Every raw source should have a wiki/sources page that points back at it.
    source_links = set()
    for n in notes.values():
        if n.meta.get("type") == "source":
            for t in n.links:
                hit = resolver.resolve(t)
                if hit and hit.startswith("raw/"):
                    source_links.add(hit)
    for p in sorted(resolver.all_files | set(notes)):
        if p.startswith("raw/") and not Path(p).name.startswith(("README", "_")) and p not in source_links:
            issues["raw_without_source_page"].append(p)

    core = root / "memory" / "core.md"
    if core.exists():
        words = len(core.read_text(encoding="utf-8").split())
        if words > 400:
            issues["oversized_core"].append({"path": "memory/core.md", "words": words, "limit": 400})

    reviewed: set[str] = set()
    rf = root / REVIEWED_FLAGS
    if rf.exists():
        reviewed = {m.strip() for m in re.findall(r"`([^`]+\.md)`", rf.read_text(encoding="utf-8"))}

    # Hidden characters anywhere in markdown, including the manual, skills, raw/ and inbox/.
    for f in sorted(root.rglob("*.md")):
        rel = f.relative_to(root)
        if any(part.startswith(".") for part in rel.parts) or rel.as_posix() in reviewed:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            m = HIDDEN.search(line.lstrip("\ufeff") if i == 1 else line)
            if m:
                issues["hidden_characters"].append({"path": rel.as_posix(), "line": i, "char": f"U+{ord(m.group()):04X}"})
                break

    # Untrusted inputs (raw/ and inbox/) that read like instructions: flag them for a human.
    for f in sorted(list(root.glob("raw/**/*.md")) + list(root.glob("inbox/**/*.md"))):
        if f.relative_to(root).as_posix() in reviewed:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            m = INJECTION.search(HIDDEN.sub("", line))
            if m:
                issues["injection_suspects"].append({"path": f.relative_to(root).as_posix(), "line": i,
                                                     "text": m.group()[:60]})
                break

    # The operating manual must stay short (Claude Code: <200 lines; Codex reads 32 KiB by default).
    manual = root / "AGENTS.md"
    if manual.exists():
        raw = manual.read_bytes()
        n_lines = raw.decode("utf-8", errors="replace").count("\n")
        if n_lines > MANUAL_MAX_LINES or len(raw) > MANUAL_MAX_BYTES:
            issues["oversized_manual"].append({"path": "AGENTS.md", "lines": n_lines, "bytes": len(raw),
                                               "limit": f"{MANUAL_MAX_LINES} lines / {MANUAL_MAX_BYTES} bytes"})

    total = sum(len(v) for v in issues.values())
    return {"notes": len(notes), "wiki_pages": sum(p.startswith("wiki/") for p in notes),
            "issue_count": total, "issues": issues}


def format_report(result: dict) -> str:
    lines = [f"# Brain lint — {dt.date.today().isoformat()}", "",
             f"{result['notes']} notes, {result['wiki_pages']} wiki pages, {result['issue_count']} issues.", ""]
    for kind, items in result["issues"].items():
        if not items:
            continue
        lines.append(f"## {kind.replace('_', ' ')} ({len(items)})")
        for it in items[:50]:
            lines.append(f"- {it}" if not isinstance(it, str) else f"- [[{it[:-3] if it.endswith('.md') else it}]]")
        if len(items) > 50:
            lines.append(f"- … {len(items) - 50} more")
        lines.append("")
    return "\n".join(lines)
