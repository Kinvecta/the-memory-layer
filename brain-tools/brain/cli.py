"""`brain` command line. Works from any harness that can run a shell command.

  brain index                    refresh the search index (embeddings if Ollama is up)
  brain search "question" [-k 6] [--mode hybrid|keyword|semantic] [--folder wiki/]
  brain wake                     print core memory + working memory + index (session start)
  brain remember "fact" [--kind decision]
  brain archive [--title "what this session was"]
  brain lint [--write]           health check; --write saves a report under memory/reports/
  brain heartbeat [--llm "claude -p"] [--commit]
  brain stats
  brain serve [--http]           start the MCP server

Vault = --vault, else $BRAIN_VAULT, else the current folder.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .heartbeat import heartbeat
from .lint import format_report, lint
from .memory import archive_working, remember
from .search import BrainIndex
from .vault import vault_root


def main(argv=None):
    ap = argparse.ArgumentParser(prog="brain", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("index"); s.add_argument("--no-embed", action="store_true")
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("-k", type=int, default=6)
    s.add_argument("--mode", default="hybrid", choices=["hybrid", "keyword", "semantic"]); s.add_argument("--folder")
    sub.add_parser("wake")
    s = sub.add_parser("remember"); s.add_argument("note"); s.add_argument("--kind", default="note")
    s = sub.add_parser("archive"); s.add_argument("--title", default="session")
    s = sub.add_parser("lint"); s.add_argument("--write", action="store_true")
    s = sub.add_parser("heartbeat"); s.add_argument("--llm"); s.add_argument("--no-embed", action="store_true")
    s.add_argument("--commit", action="store_true", help="one git commit per run (vault must be a git repo)")
    s.add_argument("--working-max-hours", type=float, default=12)
    sub.add_parser("stats")
    s = sub.add_parser("serve"); s.add_argument("--http", action="store_true"); s.add_argument("--port", type=int, default=8765)
    a = ap.parse_args(argv)
    root = vault_root(a.vault)

    def emit(obj, text=None):
        print(json.dumps(obj, indent=2, default=str) if a.json or text is None else text)

    if a.cmd == "index":
        idx = BrainIndex(root); r = idx.update(use_embeddings=not a.no_embed); idx.close()
        emit(r, f"Indexed {r['files']} files: {r['changed']} changed, {r['removed']} removed, "
                f"{r['chunks']} chunks, vectors {r['chunks_with_vectors']}/{r['chunks']} (Ollama: {r['ollama']}).")
    elif a.cmd == "search":
        idx = BrainIndex(root)
        if idx.stats()["files"] == 0:
            idx.update(use_embeddings=a.mode != "keyword")
        hits = idx.search(a.query, k=a.k, mode=a.mode, path_prefix=a.folder); idx.close()
        lines = [f"{i}. [[{h['path'][:-3]}]] — {h['title']}  ({h['via']}, {h['score']})\n   § {h['heading']}\n   {h['snippet']}"
                 for i, h in enumerate(hits, 1)]
        emit(hits, "\n".join(lines) or "No matches. Try other words, or --mode keyword.")
    elif a.cmd == "wake":
        parts = []
        for rel in ("memory/core.md", "memory/working.md", "index.md"):
            p = root / rel
            if p.exists():
                parts.append(f"===== {rel} =====\n{p.read_text(encoding='utf-8')}")
        emit({"text": "\n\n".join(parts)}, "\n\n".join(parts))
    elif a.cmd == "remember":
        emit({"ok": True}, remember(root, a.note, a.kind))
    elif a.cmd == "archive":
        ep = archive_working(root, a.title)
        emit({"episode": ep}, f"Archived to {ep}" if ep else "Working memory was empty; nothing archived.")
    elif a.cmd == "lint":
        r = lint(root)
        if a.write:
            out = root / "memory" / "reports" / "lint-latest.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("---\ntype: report\nagent_written: true\n---\n" + format_report(r), encoding="utf-8")
        emit(r, format_report(r))
        return 0
    elif a.cmd == "heartbeat":
        emit(heartbeat(root, a.working_max_hours, a.llm, use_embeddings=not a.no_embed, commit=a.commit))
    elif a.cmd == "stats":
        idx = BrainIndex(root); emit(idx.stats()); idx.close()
    elif a.cmd == "serve":
        sys.argv = ["brain-mcp", "--vault", str(root)] + (["--http", "--port", str(a.port)] if a.http else [])
        from .mcp_server import main as serve
        serve()
    return 0


def entry():
    try:
        return main()
    except BrokenPipeError:  # e.g. `brain lint | head`
        sys.stderr.close()
        return 0


if __name__ == "__main__":
    sys.exit(entry())
