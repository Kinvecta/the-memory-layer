"""Safe write helpers for the brain: remember, log, archive, save a page.

Every write goes through `safe_path`, which keeps agents inside the folders
they are allowed to change. `raw/` is never writable: sources are immutable.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

WRITABLE = ("memory/", "wiki/", "inbox/")
APPEND_ONLY = {"log.md"}


class WriteDenied(PermissionError):
    pass


def safe_path(root: Path, rel: str, allow=WRITABLE) -> Path:
    rel = rel.replace("\\", "/").lstrip("/")
    if not rel.endswith(".md"):
        rel += ".md"
    target = (root / rel).resolve()
    if root.resolve() not in target.parents:
        raise WriteDenied(f"{rel} is outside the vault")
    relp = target.relative_to(root.resolve()).as_posix()
    if relp not in APPEND_ONLY and not relp.startswith(tuple(allow)):
        raise WriteDenied(f"{relp} is not writable. Agents may write under {', '.join(allow)}")
    return target


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def append_log(root: Path, op: str, detail: str, actor: str = "agent") -> str:
    """log.md is append-only: one line per operation, newest at the bottom."""
    line = f"- {now()} · {op} · {actor} · {detail.strip()}"
    p = safe_path(root, "log.md")
    with p.open("a", encoding="utf-8") as f:
        f.write(("" if p.read_text(encoding="utf-8").endswith("\n") else "\n") + line + "\n")
    return line


def remember(root: Path, note: str, kind: str = "note") -> str:
    """Append a timestamped bullet to working memory (the session scratchpad)."""
    kind = re.sub(r"[^a-z-]", "", kind.lower()) or "note"
    p = safe_path(root, "memory/working.md")
    if not p.exists():
        p.write_text("---\ntype: working\n---\n# Working memory\n\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} [{kind}] {note.strip()}\n")
    return f"Remembered in memory/working.md: [{kind}] {note.strip()[:80]}"


def archive_working(root: Path, title: str = "session") -> str | None:
    """Move working memory into a dated episode file, then reset it.

    Returns the episode path, or None if working memory had no entries.
    """
    p = safe_path(root, "memory/working.md")
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    entries = [l for l in text.splitlines() if l.startswith("- ")]
    if not entries:
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "session"
    day = dt.date.today().isoformat()
    ep = safe_path(root, f"memory/episodes/{day}-{slug}.md")
    n = 2
    while ep.exists():
        ep = safe_path(root, f"memory/episodes/{day}-{slug}-{n}.md")
        n += 1
    ep.parent.mkdir(parents=True, exist_ok=True)
    ep.write_text(
        f"---\ntype: episode\ncreated: {day}\nagent_written: true\n---\n# {day} — {title}\n\n"
        + "\n".join(entries) + "\n",
        encoding="utf-8",
    )
    p.write_text("---\ntype: working\n---\n# Working memory\n\n", encoding="utf-8")
    rel = ep.relative_to(root.resolve()).as_posix()
    append_log(root, "archive", f"working memory → [[{rel[:-3]}]] ({len(entries)} entries)", "system")
    return rel


def write_page(root: Path, rel: str, content: str, overwrite: bool = False) -> str:
    """Create (or replace) a wiki/inbox page. Marks it agent_written."""
    p = safe_path(root, rel)
    if p.exists() and not overwrite:
        raise WriteDenied(f"{rel} exists. Read it and pass overwrite=true to replace it.")
    if not content.lstrip().startswith("---"):
        day = dt.date.today().isoformat()
        content = f"---\ntype: question\ncreated: {day}\nupdated: {day}\nagent_written: true\n---\n" + content
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    relp = p.relative_to(root.resolve()).as_posix()
    append_log(root, "write", f"[[{relp[:-3]}]]{' (replaced)' if overwrite else ''}")
    return relp
