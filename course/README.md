# Syllabus

The Memory Layer is a six-part course on building an AI "second brain": plain, linked markdown files that any AI tool can read, search, cite and keep current. Each part is a short video with slides, a hands-on lab with an answer key, a research brief with sources and a transcript.

Take the parts in order. Each lab builds on the vault from the one before. You need Python 3.10+, git and any AI coding tool or chat app; the reference vault in [`brain-vault/`](../brain-vault/) and the tools in [`brain-tools/`](../brain-tools/) are the finished result to compare against.

| Part | Title | What you learn | Materials |
|:--:|---|---|---|
| 1 | [Why your AI needs a brain](../Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/) | Why AI forgets, three ways to give it memory, and the LLM Wiki pattern: a folder of linked markdown pages the AI maintains for you. | [video](https://youtu.be/EsighdlROyc) · [slides](../Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/slides.pdf) · [lab](../Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/lab/) · [brief](../Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/research-brief.md) |
| 2 | [The operating manual](../Part%202%20-%20The%20Operating%20Manual/) | One AGENTS.md that every AI tool reads; templates, memory layers and a conformance test. | [video](https://youtu.be/rMirmmTu3VM) · [slides](../Part%202%20-%20The%20Operating%20Manual/slides.pdf) · [lab](../Part%202%20-%20The%20Operating%20Manual/lab/) · [brief](../Part%202%20-%20The%20Operating%20Manual/research-brief.md) |
| 3 | [Ingest, query, lint](../Part%203%20-%20Ingest,%20Query,%20Lint/) | Make knowledge compound: ingest sources into the wiki, answer with citations, lint for problems and revert a poisoned page. | [video](https://youtu.be/TVV9VYqgSfI) · [slides](../Part%203%20-%20Ingest,%20Query,%20Lint/slides.pdf) · [lab](../Part%203%20-%20Ingest,%20Query,%20Lint/lab/) · [brief](../Part%203%20-%20Ingest,%20Query,%20Lint/research-brief.md) |
| 4 | [Recall at scale](../Part%204%20-%20Recall%20at%20Scale/) | Hybrid search: BM25 plus local embeddings fused with RRF, measured with recall@5 and MRR on a golden set. | [video](https://youtu.be/1o8JCztX7Z0) · [slides](../Part%204%20-%20Recall%20at%20Scale/slides.pdf) · [lab](../Part%204%20-%20Recall%20at%20Scale/lab/) · [brief](../Part%204%20-%20Recall%20at%20Scale/research-brief.md) |
| 5 | [Plug it in anywhere](../Part%205%20-%20Plug%20It%20In%20Anywhere/) | One MCP server for every AI app: transports, host configs and write guardrails. | [video](https://youtu.be/609myTkXdn8) · [slides](../Part%205%20-%20Plug%20It%20In%20Anywhere/slides.pdf) · [lab](../Part%205%20-%20Plug%20It%20In%20Anywhere/lab/) · [brief](../Part%205%20-%20Plug%20It%20In%20Anywhere/research-brief.md) |
| 6 | [Keep it alive, keep it safe](../Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/) | A propose-only heartbeat on a schedule, best-before dates for pages, and quarantine for injected or invisible-ink notes. | [video](https://youtu.be/Ob16rIDo8Bc) · [slides](../Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/slides.pdf) · [lab](../Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/lab/) · [brief](../Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/research-brief.md) |

## By the end you can

- Explain why chat memory and plain retrieval aren't enough, and keep a brain as linked markdown you own.
- Write one `AGENTS.md` operating manual that every AI tool follows.
- Ingest sources, answer with citations and lint the vault for broken, stale or poisoned pages.
- Search the brain with hybrid BM25 + embedding retrieval and measure recall.
- Serve the brain to any AI app over MCP with safe write limits.
- Keep it current with a scheduled, propose-only heartbeat, and keep it safe from injection and leaked secrets.

The playlist is [The Memory Layer: Build an AI Second Brain](https://www.youtube.com/playlist?list=PLaleqILsm2uQ).
