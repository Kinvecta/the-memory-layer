"""Lab 5 check: talk to the brain MCP server the way any host does (stdio), and prove the guardrails.

Usage:  python3 mcp_check.py <vault>
Needs brain-tools installed with the mcp extra (pip install -e "brain-tools[mcp]").
It lists the tools, runs one search and one read, saves a page to inbox/, and then tries
three things a careless or hijacked agent might do: write into raw/, escape the vault, and
overwrite a page. Each one should be refused.
"""
import asyncio, json, os, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

VAULT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")


def text(res):
    t = " ".join(getattr(c, "text", "") for c in res.content).strip()
    return " ".join((t or json.dumps(res.structured_content or {})).split())[:400]


async def main():
    params = StdioServerParameters(command=sys.executable, args=["-m", "brain.mcp_server", "--vault", VAULT],
                                   env={**os.environ, "BRAIN_VAULT": VAULT})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = (await s.list_tools()).tools
            print(f"1. {len(tools)} tools:")
            for t in tools:
                a = t.annotations
                kind = "read-only" if a and a.read_only_hint else ("writes, can replace" if a and a.destructive_hint else "writes")
                print(f"   - {t.name:16s} {kind}")
            res = await s.call_tool("brain_search", {"query": "prompt injection", "k": 3})
            hits = res.structured_content["hits"] if res.structured_content else []
            print("2. search 'prompt injection' ->", [h["path"] for h in hits])
            if hits:
                body = text(await s.call_tool("brain_read", {"path": hits[0]["path"]}))
                print("3. read top hit ->", body[:96])
            res = await s.call_tool("brain_remember", {"note": "Lab 5: the brain answered through MCP", "kind": "observation"})
            print("4. remember a fact ->", text(res))
            res = await s.call_tool("brain_save_page", {"path": "inbox/lab5-hello.md",
                    "content": "---\ntype: note\n---\n# Lab 5\nSaved through MCP. [[prompt-injection]]\n", "overwrite": True})
            print("5. save inbox/lab5-hello.md ->", "OK" if not res.is_error else "REFUSED", "|", text(res))
            for label, args in [("write into raw/", {"path": "raw/evil.md", "content": "---\n---\nhello there friend"}),
                                ("escape the vault", {"path": "wiki/../../outside.md", "content": "---\n---\nhello there friend"}),
                                ("overwrite without asking", {"path": "inbox/lab5-hello.md", "content": "---\n---\nreplaced text here"})]:
                res = await s.call_tool("brain_save_page", args)
                print(f"6. {label:24s} ->", "REFUSED" if res.is_error else "ALLOWED (check this!)", "|", text(res)[:120])

asyncio.run(main())
