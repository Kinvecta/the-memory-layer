---
type: source
summary: Summary of the Oct 2026 research brief on building an LLM-readable second brain - the LLM Wiki pattern, memory layers, recall tiers, cross-harness portability and pitfalls.
sources: ["[[raw/research/second-brain-research-brief]]"]
related: ["[[llm-wiki-pattern]]", "[[agent-memory-layers]]", "[[the-memory-layer]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Second Brain Research Brief (Oct 2026)

**TL;DR:** This brief is the research behind [[the-memory-layer]]. It shows how a folder of markdown, usually opened in Obsidian, can serve as long-term memory for any AI harness. Its structure comes from the [[llm-wiki-pattern]], its memory layers from [[agent-memory-layers]], and it recommends hybrid search only once the vault outgrows its index.

**Source file:** [[raw/research/second-brain-research-brief]]  ·  **Kind:** research brief  ·  **Date:** 2026-10-21

## Key points
1. Context windows reset every session, so memory has to live outside the model. Plain markdown is the format every model and tool can read (§1). See [[context-window]].
2. Karpathy's LLM Wiki (April 2026) splits a vault into raw/, wiki/, a schema file, index.md and log.md. It runs three operations: ingest, query and lint (§2).
3. Write-ups of the pattern say index-first navigation is enough for roughly 100 to 10,000 high-signal documents. Past that, add hybrid search (§2, §4). See [[how-ai-finds-your-data]] and [[embeddings-and-vector-search]].
4. The memory layers are core, working, episodic and semantic. A scheduled heartbeat promotes episodic memory to semantic memory (§3).
5. The recall ladder runs from cheapest to most capable: file access, the index, BM25, embeddings, hybrid (RRF), MCP, and the Obsidian CLI (§4). See [[model-context-protocol]].
6. For portability, AGENTS.md is the shared manual, CLAUDE.md and GEMINI.md import it, and skills use the SKILL.md format (§5). See [[agent-skills]] and [[agnostic-ai-platform]].
7. The pitfalls are over-capturing, unbounded context, drift, mixed authorship, having no undo, [[prompt-injection]], data handling, and skill atrophy (§6).

## Worth quoting
> "Explicit links and summaries in an index replace nearest-neighbor search, and every claim traces back to a readable file."

## Pages this source updated
- [[llm-wiki-pattern]], [[agent-memory-layers]], [[the-memory-layer]]
