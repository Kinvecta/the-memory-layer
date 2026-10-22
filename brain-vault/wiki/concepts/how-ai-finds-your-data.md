---
type: concept
summary: The six ways AI fetches data (whole context, semantic, keyword, agentic, structured, multimodal), which finder fits each data type, how major products retrieve as of Oct 2026, and why an index is a copy of your data.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s4-tokens-context-and-data]]", "[[raw/transcripts/s1-what-an-llm-is]]"]
related: ["[[embeddings-and-vector-search]]", "[[context-window]]", "[[tokens]]", "[[ai-harness]]", "[[model-context-protocol]]", "[[tool-calling]]", "[[ai-evals]]", "[[agnostic-ai-platform]]"]
aliases: [retrieval, RAG, finders, retrieval-augmented generation]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# How AI finds your data

**TL;DR:** A chat, workflow or agent does not know your data; it fetches what it needs at question time, and the fetching method ("finder") decides what the model can see. No single finder covers text, tables, images and code, so modern harnesses run several, merge the results and hand them to the model with citations. The model never searches on its own.

## The six finders
| Method | How it works | Best for | Weak at |
|---|---|---|---|
| Put it all in context | Whole set placed in the [[context-window]] | Small, stable sets | Anything larger than the window; cost per question |
| Semantic search (classic RAG) | Chunks turned into embeddings; closest chunks to the embedded question returned | "Find anything about X" across large prose | Exact strings, names, numbers; split tables; freshness |
| Keyword search (grep, lexical) | Exact or pattern match on live text, no index | Names, IDs, error codes, file paths, code | Synonyms, paraphrase; re-searching huge corpora |
| Agentic search | Model plans a series: list, grep, open, refine | Code, organized folders, fast-changing files | Token cost on huge repos; concepts with no keyword |
| Structured queries | Tool or MCP server runs SQL or an API query | Contracts, personnel, inventory, dates, totals | Free text; needs schema and approved connection |
| Multimodal retrieval | Pages, images, diagrams embedded with text | Scans, slides, maps, drawings, tables kept intact | Newest; fewer tools; higher indexing cost |

Source: [[source-ai-training-guide]] §2.3; [[source-s4-tokens-context-and-data]] [4:22]. Semantic search details: [[embeddings-and-vector-search]].

## Why one finder is not enough
First-generation RAG assumed everything was prose. "Chunking flattens tables, embeddings miss exact IDs, grep cannot find a concept, and a scanned image has no text to search at all" ([[source-ai-training-guide]] §2.3). "It couldn't find the table" usually means the wrong finder flattened it into prose ([[source-s4-tokens-context-and-data]] [0:49]).

## Match the finder to the data
| Data type | Finders | Watch |
|---|---|---|
| Text documents, memos | Semantic + keyword (hybrid); whole doc for small sets | Chunk boundaries; cite the page |
| Tables, spreadsheets | Structured queries; multimodal that keeps tables intact | Totals come from a query, not the model reading rows |
| Images, scans, slides, maps | Multimodal; vision model | Confirm it saw the image, not an OCR guess |
| Code, config | Agentic search; semantic as supplement | Index staleness; token cost |
| Live records | Structured queries only, via approved connection | Access control on the query; log every lookup |

Source: [[source-ai-training-guide]] §2.3.

## How it works
One question ("which vendors scored lowest on site safety last quarter?") goes to four finders at once: semantic search finds a memo passage, keyword search an exact vendor ID, a structured query the scores table, multimodal retrieval a chart on a scanned page. The [[ai-harness]] merges and cites ([[source-s4-tokens-context-and-data]] [3:45]). Classifiers, vision/OCR, embedding models and rerankers often run before the language model writes ([[source-s1-what-an-llm-is]] [3:29]).

## Major products (as of October 2026)
- **Claude Projects:** knowledge in context while it fits; near the limit, switches to a knowledge search tool (RAG) expanding capacity up to 10x.
- **Claude Code:** agentic search (Glob, Grep, file reads), which Anthropic found beat an early local vector index.
- **Claude Cowork:** works directly on files in connected folders, plus connectors.
- **OpenAI File Search:** managed vector store with hybrid semantic plus keyword search.
- **Gemini File Search:** managed RAG; since May 2026 embeds images and text together with page-level citations.

Source: [[source-ai-training-guide]] §2.3.

> [!warning] An index is a copy of your data
> It holds chunks of the source, often on different infrastructure, and needs the same access rules and approvals as the source; agentic or structured retrieval of the live, controlled source is often safer ([[source-ai-training-guide]] §2.3).

## In practice
Each finder is an approved MCP server or built-in tool, runs in the container, and the workflow's eval set includes retrieval cases (an answer in a table or an image) ([[source-ai-training-guide]] §2.3; [[agnostic-ai-platform]]). Session 4 exercise: pick finders for six real questions; "if you picked semantic search for total spend, think again" ([[source-s4-tokens-context-and-data]] [5:36]).

## See also
[[embeddings-and-vector-search]] · [[context-window]] · [[model-context-protocol]]
