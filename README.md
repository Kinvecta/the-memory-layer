<p align="center">
  <a href="https://www.youtube.com/playlist?list=PLaleqILsm2uQ"><img src="docs/assets/banner.svg" alt="The Memory Layer: build an AI second brain any LLM can recall from" width="100%"></a>
</p>

<p align="center">
  <a href="#video-tutorials">videos</a> | <a href="#course">labs</a> | <a href="brain-tools/">brain-tools</a> | <a href="brain-vault/">reference vault</a> | <a href="course/">research</a>
</p>

<br>

<p align="center">
  <a href="https://github.com/Kinvecta/the-memory-layer/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Kinvecta/the-memory-layer/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/Kinvecta/the-memory-layer/actions/workflows/security.yml"><img alt="Security" src="https://github.com/Kinvecta/the-memory-layer/actions/workflows/security.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="license MIT" src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="LICENSE-CONTENT.md"><img alt="content CC BY 4.0" src="https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey"></a>
  <img alt="python 3.10 | 3.11 | 3.12 | 3.13" src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue">
</p>

<p align="center">
  <a href="https://www.youtube.com/playlist?list=PLaleqILsm2uQ"><img alt="YouTube playlist" src="https://img.shields.io/badge/YouTube-playlist-red?logo=youtube&logoColor=white"></a>
  <a href="#plug-the-brain-into-any-ai-app"><img alt="MCP server" src="https://img.shields.io/badge/MCP-server-yellow"></a>
  <a href="https://ollama.com"><img alt="Ollama optional" src="https://img.shields.io/badge/Ollama-optional-white?logo=ollama&logoColor=black"></a>
  <a href="https://github.com/Kinvecta/the-memory-layer/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Kinvecta/the-memory-layer?style=social"></a>
  <a href="https://obsidian.md"><img alt="Obsidian ready" src="https://img.shields.io/badge/Obsidian-ready-7C3AED?logo=obsidian&logoColor=white"></a>
</p>

> [!WARNING]
> **Not actively maintained.** This repository is published as course material for a training series recorded in 2026. It is provided as is, without warranty, and is not monitored for issues or updates. AI tools, protocols and best practices change quickly, so some content may be outdated. Code dependencies (for example the `mcp` and `pydantic` packages) will age and may come to include known vulnerabilities. Review, update and scan anything you reuse before running it, especially in production or on sensitive data. See [maintenance and security](#maintenance-and-security).

<details>
<summary><b>Table of Contents</b></summary>

- [hello](#hello)
- [start here](#start-here)
- [install](#install)
- [quickstart](#quickstart)
  - [search your brain](#search-your-brain)
  - [plug the brain into any AI app](#plug-the-brain-into-any-ai-app)
  - [keep it healthy](#keep-it-healthy)
- [course](#course)
- [video tutorials](#video-tutorials)
- [how it works](#how-it-works)
  - [keep it alive and safe](#keep-it-alive-and-safe)
- [cheat sheet](#cheat-sheet)
- [FAQ](#faq)
- [built with the memory layer](#built-with-the-memory-layer)
- [star history](#star-history)
- [what's inside](#whats-inside)
- [maintenance and security](#maintenance-and-security)

</details>

## hello

<table>
<tr>
<td width="52%" valign="top">

**The model is rented, and it forgets. The brain is yours.**

The Memory Layer is a free course and a working codebase for building an AI "second brain": a folder of plain, linked markdown files that you browse in Obsidian or any editor, and that any AI tool (Claude Code, Codex, Gemini CLI, Copilot, Cursor or a local model) can read, search, cite and keep up to date.

- **A reference brain:** 14 sources compiled into 55 linked wiki pages
- **`brain` tools:** hybrid search, an MCP server, lint and a heartbeat
- **Six narrated videos**, each with a lab and answer key
- **Slides (PDF), transcripts and research briefs** for every lesson

Switch models or apps, and the brain comes with you.

</td>
<td width="48%" valign="top">
<img src="docs/assets/one-brain-every-app.gif" width="100%" alt="Animation: four AI apps plug into one brain through a single MCP server">
<br><sub><i>One brain, one plug, every app (from Part 5).</i></sub>
</td>
</tr>
</table>

## start here

<table>
<tr>
<td width="33%" valign="top">

**Watch** (about 70 minutes)

Six short videos, 10 to 15 minutes each, from "why your AI forgets" to "keep it alive and keep it safe".

[Open the playlist](https://www.youtube.com/playlist?list=PLaleqILsm2uQ) · [video list](#video-tutorials)

</td>
<td width="33%" valign="top">

**Build** (about 15 minutes)

Install the tools, index the reference vault, search it, and connect it to your AI app over MCP.

[Install](#install) · [quickstart](#quickstart)

</td>
<td width="33%" valign="top">

**Teach or self-study**

Every part has slides (PDF), a lab with an answer key, a research brief with sources, and a transcript.

[Course materials](#course) · [how it works](#how-it-works) · [cheat sheet (PDF)](docs/the-memory-layer-cheat-sheet.pdf)

</td>
</tr>
</table>

## install

Requires Python 3.10+. The core uses only the standard library.

```bash
git clone https://github.com/Kinvecta/the-memory-layer.git
cd the-memory-layer/brain-tools
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[mcp]"
```

Optional, for meaning search that runs fully on your machine: install [Ollama](https://ollama.com) and run `ollama pull nomic-embed-text`. Without it, search falls back to keyword (BM25).

## quickstart

<p align="center">
  <img src="docs/assets/terminal-demo.gif" width="100%" alt="Terminal demo: index the vault, search it with citations, plant a note with hidden Unicode, lint flags it, and the heartbeat skips its AI step">
  <br><sub>Real commands and output against the reference vault: search with citations, then a planted note with invisible text gets caught and quarantined.</sub>
</p>

### search your brain

Index the reference vault, then ask it something. Results come back as `[[wikilinks]]` with the heading where the answer lives.

```bash
brain --vault ../brain-vault index
# Indexed 72 files: 72 changed, 0 removed, 704 chunks, vectors 0/704 (Ollama: unreachable).

brain --vault ../brain-vault search "how does the recall ladder save tokens?" -k 3
# 1. [[wiki/concepts/recall-ladder]] — Recall ladder  (keyword, 0.02839)
# § Recall ladder > The rungs > See also
# 2. [[wiki/concepts/tokens]] — Tokens  (keyword, 0.02271)
# 3. [[wiki/concepts/safe-prompting]] — Safe prompting  (keyword, 0.0217)
```

Tip: run `export BRAIN_VAULT="$(cd ../brain-vault && pwd)"` once and you can drop `--vault` from every command.

Then start any AI tool **inside `brain-vault/`** and ask a question. It reads [`AGENTS.md`](brain-vault/AGENTS.md), climbs the recall ladder and answers with citations.

**more search:**

- `--mode keyword | semantic | hybrid` to compare the three ([Part 4 lab](Part%204%20-%20Recall%20at%20Scale/lab/))
- `brain wake` prints core memory, working memory and the index: the start-of-session load
- `./install-skills.sh ../brain-vault` installs the ingest, query and lint skills for Claude Code and other agents

### plug the brain into any AI app

Find the server with `which brain-mcp`, then add one entry to your app's MCP config and fully restart the app:

```json
{
  "mcpServers": {
    "brain": {
      "command": "/ABSOLUTE/PATH/TO/brain-mcp",
      "env": { "BRAIN_VAULT": "/ABSOLUTE/PATH/brain-vault" }
    }
  }
}
```

The app now sees eight tools: `brain_wake_up`, `brain_search`, `brain_read`, `brain_remember`, `brain_save_page`, `brain_log`, `brain_lint` and `brain_reindex`.

**more MCP:**

- configs for VS Code (`servers`) and Codex (TOML): [Lab 5 host configs](Part%205%20-%20Plug%20It%20In%20Anywhere/lab/host-configs.md)
- test it end to end: `python3 "Part 5 - Plug It In Anywhere/lab/mcp_check.py" <a copy of your vault>` (it writes a test page, so use a copy)
- sharing one brain over HTTP: `brain serve --http` binds to localhost only; put auth in front before exposing it

### keep it healthy

```bash
brain --vault ../brain-vault lint
# Brain lint — 2026-10-22
# 83 notes, 55 wiki pages, 0 issues.

brain --vault ../brain-vault heartbeat   # archive working memory, re-index and lint in one job
```

The heartbeat writes to the vault (it archives working memory and appends to `log.md`), so point it at your own brain, or a copy, rather than the reference vault.

**more upkeep:** schedule the heartbeat with launchd or cron ([example plist](brain-tools/examples/)), and see every command in [`brain-tools/README.md`](brain-tools/README.md).

## course

All six parts are out. Each one has a video, slides as a PDF, a hands-on lab with an answer key, a research brief with sources, and a transcript.

| **part** | **what you learn** | **watch / lab** | **materials** | **key research** |
|:--:|---|---|---|---|
| **1** | **[Why your AI needs a brain](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/)**<br><sub>Why AI forgets, three ways to give it memory, the LLM Wiki pattern</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/EsighdlROyc) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/transcript/) | [![llm-wiki gist](https://img.shields.io/badge/gist-llm--wiki-grey?logo=github)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
| **2** | **[The operating manual](Part%202%20-%20The%20Operating%20Manual/)**<br><sub>One <code>AGENTS.md</code> for every AI tool; templates and memory layers</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/rMirmmTu3VM) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%202%20-%20The%20Operating%20Manual/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%202%20-%20The%20Operating%20Manual/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%202%20-%20The%20Operating%20Manual/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%202%20-%20The%20Operating%20Manual/transcript/) | [![arXiv 2602.11988](https://img.shields.io/badge/arXiv-2602.11988-B31B1B)](https://arxiv.org/abs/2602.11988) [![arXiv 2507.11538](https://img.shields.io/badge/arXiv-2507.11538-B31B1B)](https://arxiv.org/abs/2507.11538) |
| **3** | **[Ingest, query, lint](Part%203%20-%20Ingest,%20Query,%20Lint/)**<br><sub>Make knowledge compound; cite every answer; revert a poisoned page</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/TVV9VYqgSfI) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%203%20-%20Ingest,%20Query,%20Lint/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%203%20-%20Ingest,%20Query,%20Lint/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%203%20-%20Ingest,%20Query,%20Lint/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%203%20-%20Ingest,%20Query,%20Lint/transcript/) | [![arXiv 2304.09848](https://img.shields.io/badge/arXiv-2304.09848-B31B1B)](https://arxiv.org/abs/2304.09848) [![arXiv 2302.12173](https://img.shields.io/badge/arXiv-2302.12173-B31B1B)](https://arxiv.org/abs/2302.12173) |
| **4** | **[Recall at scale](Part%204%20-%20Recall%20at%20Scale/)**<br><sub>BM25 + local embeddings fused with RRF; measure recall@5 and MRR</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/1o8JCztX7Z0) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%204%20-%20Recall%20at%20Scale/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%204%20-%20Recall%20at%20Scale/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%204%20-%20Recall%20at%20Scale/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%204%20-%20Recall%20at%20Scale/transcript/) | [![arXiv 2307.03172](https://img.shields.io/badge/arXiv-2307.03172-B31B1B)](https://arxiv.org/abs/2307.03172) [![arXiv 2508.21038](https://img.shields.io/badge/arXiv-2508.21038-B31B1B)](https://arxiv.org/abs/2508.21038) |
| **5** | **[Plug it in anywhere](Part%205%20-%20Plug%20It%20In%20Anywhere/)**<br><sub>One MCP server for every AI app; transports, configs, write guardrails</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/609myTkXdn8) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%205%20-%20Plug%20It%20In%20Anywhere/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%205%20-%20Plug%20It%20In%20Anywhere/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%205%20-%20Plug%20It%20In%20Anywhere/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%205%20-%20Plug%20It%20In%20Anywhere/transcript/) | [![MCP spec](https://img.shields.io/badge/MCP-spec-yellow)](https://modelcontextprotocol.io/specification/2026-07-28) |
| **6** | **[Keep it alive, keep it safe](Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/)**<br><sub>A propose-only heartbeat, best-before dates, quarantine for injected notes</sub> | [![YouTube](https://img.shields.io/badge/watch-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/Ob16rIDo8Bc) [![Lab](https://img.shields.io/badge/open-lab-orange)](Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/lab/) | [![Slides](https://img.shields.io/badge/view-slides%20(PDF)-8A2BE2)](Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/slides.pdf) [![Research brief](https://img.shields.io/badge/read-brief-blue)](Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/research-brief.md) [![Transcript](https://img.shields.io/badge/read-transcript-lightgrey)](Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/transcript/) | [![arXiv 2407.12784](https://img.shields.io/badge/arXiv-2407.12784-B31B1B)](https://arxiv.org/abs/2407.12784) [![arXiv 2302.12173](https://img.shields.io/badge/arXiv-2302.12173-B31B1B)](https://arxiv.org/abs/2302.12173) |

## video tutorials

New here? Watch the [2-minute trailer](https://youtu.be/XpyePfCoe-g) first. Then watch the parts in order in the [YouTube playlist](https://www.youtube.com/playlist?list=PLaleqILsm2uQ), or jump to any part.

<table>
<tr>
<td width="40%"><a href="https://youtu.be/EsighdlROyc"><img src="Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/thumbnail.png" width="100%" alt="Watch Part 1: Why your AI needs a brain"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/EsighdlROyc">Part 1 · Why your AI needs a brain</a></b><br>
<sub><b>Published:</b> 21 Oct 2026 · <b>Length:</b> 15:16 · <a href="Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/lab/">Lab&nbsp;→</a></sub>
<p>Your AI forgets between sessions. See why memory has to live outside the model, compare vendor memory, RAG and a markdown brain, and tour a working vault in Obsidian and in a terminal.</p>
</td>
</tr>
<tr>
<td width="40%"><a href="https://youtu.be/rMirmmTu3VM"><img src="Part%202%20-%20The%20Operating%20Manual/thumbnail.png" width="100%" alt="Watch Part 2: The operating manual: one brain, every harness"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/rMirmmTu3VM">Part 2 · The operating manual: one brain, every harness</a></b><br>
<sub><b>Published:</b> 22 Oct 2026 · <b>Length:</b> 13:10 · <a href="Part%202%20-%20The%20Operating%20Manual/lab/">Lab&nbsp;→</a></sub>
<p>Write one <code>AGENTS.md</code> that Claude Code, Codex, Gemini CLI and others all follow. Templates, properties, memory layers and a six-prompt conformance test.</p>
</td>
</tr>
<tr>
<td width="40%"><a href="https://youtu.be/TVV9VYqgSfI"><img src="Part%203%20-%20Ingest,%20Query,%20Lint/thumbnail.png" width="100%" alt="Watch Part 3: Ingest, query, lint: making knowledge compound"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/TVV9VYqgSfI">Part 3 · Ingest, query, lint: making knowledge compound</a></b><br>
<sub><b>Published:</b> 22 Oct 2026 · <b>Length:</b> 11:45 · <a href="Part%203%20-%20Ingest,%20Query,%20Lint/lab/">Lab&nbsp;→</a></sub>
<p>Turn one source into many linked pages, answer with citations, lint the vault, and use git as the undo button when a page gets poisoned.</p>
</td>
</tr>
<tr>
<td width="40%"><a href="https://youtu.be/1o8JCztX7Z0"><img src="Part%204%20-%20Recall%20at%20Scale/thumbnail.png" width="100%" alt="Watch Part 4: Recall at scale: keyword, semantic, hybrid"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/1o8JCztX7Z0">Part 4 · Recall at scale: keyword, semantic, hybrid</a></b><br>
<sub><b>Published:</b> 22 Oct 2026 · <b>Length:</b> 10:20 · <a href="Part%204%20-%20Recall%20at%20Scale/lab/">Lab&nbsp;→</a></sub>
<p>When an index file stops being enough: BM25, local embeddings with Ollama, Reciprocal Rank Fusion, chunking with summaries and aliases, and a real recall eval.</p>
</td>
</tr>
<tr>
<td width="40%"><a href="https://youtu.be/609myTkXdn8"><img src="Part%205%20-%20Plug%20It%20In%20Anywhere/thumbnail.png" width="100%" alt="Watch Part 5: Plug it in anywhere: MCP and the Obsidian CLI"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/609myTkXdn8">Part 5 · Plug it in anywhere: MCP and the Obsidian CLI</a></b><br>
<sub><b>Published:</b> 22 Oct 2026 · <b>Length:</b> 9:44 · <a href="Part%205%20-%20Plug%20It%20In%20Anywhere/lab/">Lab&nbsp;→</a></sub>
<p>Connect one brain to every AI app through an MCP server. stdio vs HTTP, config files per app, three locks on every write, and when the Obsidian CLI helps.</p>
</td>
</tr>
<tr>
<td width="40%"><a href="https://youtu.be/Ob16rIDo8Bc"><img src="Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/thumbnail.png" width="100%" alt="Watch Part 6: Keep it alive, keep it safe"></a></td>
<td width="60%" valign="top">
<b><a href="https://youtu.be/Ob16rIDo8Bc">Part 6 · Keep it alive, keep it safe</a></b><br>
<sub><b>Published:</b> 22 Oct 2026 · <b>Length:</b> 9:48 · <a href="Part%206%20-%20Keep%20It%20Alive%20and%20Keep%20It%20Safe/lab/">Lab&nbsp;→</a></sub>
<p>A nightly heartbeat that proposes changes for you to approve, best-before dates for pages, and quarantine for clippings that carry hidden instructions. Plus memory poisoning, secrets, team brains and keeping a human in the loop.</p>
</td>
</tr>
</table>

## cheat sheet

All six parts on one page: the eighteen rules of thumb, the commands you'll use every week, and a link to each video. Print it, pin it, hand it out.

<p align="center">
  <a href="docs/the-memory-layer-cheat-sheet.pdf"><img src="docs/assets/cheat-sheet.png" width="100%" alt="The Memory Layer cheat sheet: six parts, eighteen rules, one brain"></a>
  <br><a href="docs/the-memory-layer-cheat-sheet.pdf"><b>Download the cheat sheet (PDF, one page)</b></a>
</p>

## how it works

```mermaid
flowchart TD
    A["raw/<br/>talks · docs · transcripts<br/><i>read-only</i>"] -->|ingest| B["wiki/<br/>sources · concepts · entities<br/>decisions · questions"]
    B --> C["index.md + log.md"]
    D["AGENTS.md<br/>one manual for every AI tool"] -.rules.-> B
    C --> E["brain search<br/>keyword + meaning, fused"]
    E --> F["brain MCP server"]
    F --> G["Editor agent"]
    F --> H["Terminal agent"]
    F --> I["Desktop chat"]
    F --> J["IDE"]
    K["heartbeat (nightly)<br/>archive · re-index · lint · scan<br/><i>proposes; you approve</i>"] -.proposes.-> B
    style F fill:#2A2A1E,stroke:#FFC400,color:#FFC400
    style D fill:#0F2440,stroke:#8FB4E8,color:#FFFFFF
    style A fill:#0F2440,stroke:#34507A,color:#C3CAD6
```

<table>
<tr>
<td width="33%" valign="top" align="center">
<img src="docs/assets/ingest.gif" width="100%" alt="Animation: one source is ingested into six linked wiki pages">
<br><b>1 · Ingest</b><br><sub>Read a source once, then file it into every page it touches, with links and a log entry.</sub>
</td>
<td width="33%" valign="top" align="center">
<img src="docs/assets/recall-ladder.svg" width="100%" alt="The recall ladder: core.md, index.md, search, links, raw; the AI stops at the first rung that answers">
<br><b>2 · Recall</b><br><sub>The AI climbs the ladder cheapest first and stops as soon as it has the answer, which saves tokens.</sub>
</td>
<td width="33%" valign="top" align="center">
<img src="docs/assets/guardrails.gif" width="100%" alt="Animation: every save passes three locks before it is written">
<br><b>3 · Guard</b><br><sub>Every save passes three locks. <code>raw/</code> is read-only, and notes are data, never commands.</sub>
</td>
</tr>
</table>

<p align="center">
<img src="docs/assets/hybrid-search.gif" width="100%" alt="Animation: keyword and meaning rankings merge with Reciprocal Rank Fusion">
<br><sub><b>Inside rung 3:</b> keyword search (BM25) and meaning search (local embeddings) each rank the pages, and Reciprocal Rank Fusion rewards the pages both agree on. Embeddings run locally with Ollama, so your notes never leave your machine.</sub>
</p>

### keep it alive and safe

The brain tends itself on a schedule, but it only proposes changes, and it stops when a note looks like an attack.

<table>
<tr>
<td width="33%" valign="top" align="center">
<img src="docs/assets/schedule.gif" width="100%" alt="Animation: cron skips runs missed while asleep; launchd runs once on wake; both skip when powered off">
<br><b>Run it nightly</b><br><sub>launchd catches up after sleep (three missed nights = one run); cron doesn't. Off is off.</sub>
</td>
<td width="33%" valign="top" align="center">
<img src="docs/assets/heartbeat.gif" width="100%" alt="Animation: the heartbeat runs fixed steps, a headless agent proposes changes, core memory and raw sources stay locked, a person reviews, one git commit">
<br><b>It proposes. You decide.</b><br><sub>Never edits <code>raw/</code> or <code>memory/core.md</code>. One commit per night, easy to revert.</sub>
</td>
<td width="33%" valign="top" align="center">
<img src="docs/assets/invisible-ink.gif" width="100%" alt="Animation: a scan reveals an instruction hidden in invisible Unicode in a clipped page; the heartbeat skips its reflect step">
<br><b>Quarantine invisible ink</b><br><sub>Hidden Unicode or injection-like lines? Lint flags them and the AI step is skipped.</sub>
</td>
</tr>
</table>

## FAQ

<details>
<summary><b>Do I need Obsidian?</b></summary>

No. The brain is a plain folder of markdown files. Obsidian gives you graph view, backlinks and properties for free, but VS Code, any editor or a terminal works too.
</details>

<details>
<summary><b>Do I need Ollama or a GPU?</b></summary>

No. Without Ollama, search runs as keyword search (BM25) using only the Python standard library. Ollama adds meaning search with a small local embedding model (`nomic-embed-text`) that runs fine on a laptop.
</details>

<details>
<summary><b>Which AI tools does it work with?</b></summary>

Any tool that reads a project folder (Claude Code, Codex, Gemini CLI, Copilot, Cursor and others follow `AGENTS.md`), plus any app that supports MCP servers. Tool support changes quickly, so check each tool's current docs.
</details>

<details>
<summary><b>Does my data leave my machine?</b></summary>

The brain tools don't send anything anywhere: the index is a local SQLite file, and embeddings run locally through Ollama. Whatever AI app you connect will see the notes it reads, under that app's own data policy.
</details>

<details>
<summary><b>How is this different from RAG or a vector database?</b></summary>

The AI compiles sources into curated, linked wiki pages once, instead of retrieving raw chunks on every question. Search is still there (keyword plus local embeddings), but it runs over pages you can read, edit and review. [Part 1](Part%201%20-%20Why%20Your%20AI%20Needs%20a%20Brain/) compares the approaches.
</details>

<details>
<summary><b>Can I use this at work?</b></summary>

The code is MIT and the course content is CC BY 4.0. The repository isn't actively maintained, so review and update it, and follow your organization's rules on which data may go into an AI tool.
</details>

## what's inside

| Folder | What it is |
|---|---|
| [`brain-vault/`](brain-vault/) | **The reference brain**: 14 sources compiled into 55 linked wiki pages, following the LLM Wiki pattern. Read [`AGENTS.md`](brain-vault/AGENTS.md) first. |
| [`brain-tools/`](brain-tools/) | **Python tools**: the `brain` CLI, hybrid BM25 + local-embedding search, an MCP server, `lint` and the `heartbeat` job. Tests included. |
| `Part 1` – `Part 6` | Each part's slides (PDF), lab and answer key, research brief and transcript |
| [`course/`](course/) | Syllabus and research briefs, with sources |

## built with the memory layer

Built your own brain with this course? Show it in [Discussions → Show and tell](https://github.com/Kinvecta/the-memory-layer/discussions/categories/show-and-tell): what's in your brain, which AI tools read it, and one thing that surprised you. Screenshots of your graph view are welcome.

Please don't post secrets, private notes or anyone's personal data. The repository isn't actively maintained, so posts are read on a best-effort basis.

## star history

<a href="https://star-history.com/#Kinvecta/the-memory-layer&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Kinvecta/the-memory-layer&type=Date&theme=dark">
    <img alt="Star history chart for Kinvecta/the-memory-layer" src="https://api.star-history.com/svg?repos=Kinvecta/the-memory-layer&type=Date" width="100%">
  </picture>
</a>

## maintenance and security

This repository is a snapshot that accompanies the videos. It is **not actively maintained**:

- **Content can go stale.** Product features, config file formats, protocol versions (MCP included) and research findings described here reflect the time of recording. Check each tool's current documentation.
- **Dependencies can go stale.** Package versions are not kept current, and dependencies may come to include published vulnerabilities after release. Before you reuse the code, update its dependencies and run your own scans (for example `pip-audit`).
- **Pull requests and issues may not get a response.** Fork the repository if you need changes.
- **Treat the brain as data.** The MCP server reads files that could contain prompt injection. Keep it on `stdio` for one user, keep writes limited to `wiki/` and `inbox/`, and never put secrets in the vault.

Automated checks run on GitHub Actions: unit tests, a secret scan of the full history (Gitleaks), a dependency audit (`pip-audit`), CodeQL code scanning, and Dependabot alerts. Passing checks lower the risk but do not prove the code is secure. To report a vulnerability, see [SECURITY.md](SECURITY.md).

## notes

- Product names are examples, not endorsements. Tool support for `AGENTS.md` and skills changes quickly, so check each tool's current docs.
- No secrets, personal data or audio/video files are stored in this repository.

## license

- **Code** (`brain-tools/`, lab check scripts): [MIT](LICENSE)
- **Course content** (vault pages, slides, labs, briefs, transcripts): [CC BY 4.0](LICENSE-CONTENT.md)

© 2026 Mark D. Espinoza / Kinvecta.

<br>

<p align="center">
  <a href="https://www.youtube.com/playlist?list=PLaleqILsm2uQ">&nbsp;<img src="docs/assets/icons/youtube.svg" width="32" height="32" alt="YouTube playlist" title="YouTube playlist"></a>
  <a href="https://kinvecta.ai">&nbsp;<img src="docs/assets/icons/website.svg" width="32" height="32" alt="Kinvecta" title="Kinvecta"></a>
  <a href="brain-tools/README.md">&nbsp;<img src="docs/assets/icons/docs.svg" width="32" height="32" alt="brain-tools docs" title="brain-tools docs"></a>
  <a href="Part%205%20-%20Plug%20It%20In%20Anywhere/lab/">&nbsp;<img src="docs/assets/icons/lab.svg" width="32" height="32" alt="Labs" title="Labs"></a>
  <a href="course/">&nbsp;<img src="docs/assets/icons/research.svg" width="32" height="32" alt="Research briefs" title="Research briefs"></a>
</p>
<p align="center"><sub>If this helped, a star helps others find it.</sub></p>
<p align="center"><sub>Built by <a href="https://kinvecta.ai">Kinvecta</a> · videos, code and labs for teams adopting AI</sub></p>
