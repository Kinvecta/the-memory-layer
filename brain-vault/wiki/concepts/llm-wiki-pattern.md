---
type: concept
summary: The LLM Wiki pattern - an LLM maintains a linked markdown wiki compiled from immutable raw sources, navigated through an index instead of a vector database.
aliases: [LLM Wiki, Karpathy wiki, second brain]
sources: ["[[raw/research/second-brain-research-brief]]"]
related: ["[[agent-memory-layers]]", "[[how-ai-finds-your-data]]", "[[embeddings-and-vector-search]]", "[[agent-skills]]", "[[the-memory-layer]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# LLM Wiki pattern

**TL;DR:** Drop sources into raw/. The model compiles them into linked wiki pages and keeps an index and a log. Any harness can then answer questions by reading the index, opening a few pages, and citing them. This vault is built this way ([[source-second-brain-research-brief]]).

## What it is
Andrej Karpathy popularized the pattern in April 2026 ([[source-second-brain-research-brief]] §2). It has five parts:

| Part | Role |
|---|---|
| raw/ | Immutable sources. The model reads them and never edits them. |
| wiki/ | Pages the model writes: sources, concepts, entities, decisions, comparisons, questions. |
| Schema (AGENTS.md / CLAUDE.md) | The rules that make output consistent. Write-ups call it the most important file. |
| index.md | The catalog. It is read first. |
| log.md | An append-only audit trail. |

## Why it matters
- **It works with any model.** Plain markdown and a written schema mean Claude, Codex, Gemini or a local model can all run it. This is [[ai-resilience]] applied to knowledge.
- **It is auditable.** Every claim cites a file. Compare a vector index, which is an opaque copy of your data ([[how-ai-finds-your-data]]).
- **Knowledge compounds.** Answers to queries become pages, so the next recall is a single read.

## How it works
1. **Ingest.** Summarize a source, update 3–10 related pages, update the index, and log the change.
2. **Query.** Read the index, open 1–3 pages, and answer with wikilinks as citations.
3. **Lint.** Check for broken links, orphans, stale claims and contradictions.

Each operation is written as a skill, so any harness runs it the same way ([[agent-skills]]).

## In practice
- At this scale, index-first navigation beats RAG: about 50–200 sources per person, or up to roughly 10,000 high-signal documents.
- Above that, add hybrid keyword and semantic search ([[embeddings-and-vector-search]]).
- Use git, so you can review and undo bad ingests.
- Keep a human reading the sources. The pattern supports thinking; it does not replace it.

## See also
[[agent-memory-layers]] · [[context-window]] · [[prompt-injection]] (clipped sources can carry instructions)
