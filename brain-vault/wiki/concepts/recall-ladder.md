---
type: concept
summary: The recall ladder - the cheapest-first order an AI uses to find knowledge in the brain (core.md, index.md, search, links, raw/) and why stopping early saves tokens.
aliases: [recall ladder, retrieval ladder]
sources: ["[[raw/research/second-brain-research-brief]]", "[[raw/transcripts/s4-tokens-context-and-data]]"]
related: ["[[tokens]]", "[[context-window]]", "[[how-ai-finds-your-data]]", "[[embeddings-and-vector-search]]", "[[llm-wiki-pattern]]", "[[agent-memory-layers]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Recall ladder

**TL;DR:** When the AI needs knowledge from the brain, it climbs from the cheapest source to the most expensive one and stops once it has enough. Every rung costs more [[tokens]] than the one above it, so stopping early keeps answers cheap and focused ([[source-second-brain-research-brief]] §4).

## The rungs
| Rung | Where | Typical cost | Use it for |
|---|---|---|---|
| 1 | memory/core.md | already loaded | standing facts and rules |
| 2 | index.md | about 2k tokens | scanning one-line summaries, then opening 1–3 pages |
| 3 | search (keyword + semantic) | a few thousand tokens | when the index summaries don't point to an obvious page |
| 4 | links and backlinks | grows with each page opened | following connections from the pages already read |
| 5 | raw/ | 20k+ tokens for a long source | exact wording, quotes and numbers only |

The token figures are illustrative orders of magnitude, used in The Memory Layer Part 1 figure. Actual cost depends on the vault and the tokenizer.

## Why it matters
- **Cost.** Everything loaded into the [[context-window]] is paid for on every turn. Input tokens are the bulk of volume, because the full transcript is re-sent each turn ([[tokens]]).
- **Focus.** A few relevant pages give a better answer than a pile of loosely related text.
- **It maps to the six finders.** The ladder uses whole-context loading (rung 1), agentic navigation (rungs 2 and 4), and keyword plus semantic search (rung 3), in order of cost ([[how-ai-finds-your-data]]).

## In practice
- Written into AGENTS.md §5 and the brain-query skill, so every harness climbs the same way.
- Rule of thumb: "Read the index first. Raw last."
- At very large scale (thousands of pages), rung 3 becomes the main entry point. Consider [[embeddings-and-vector-search]].

## See also
[[llm-wiki-pattern]] · [[agent-memory-layers]]
