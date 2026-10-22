---
type: concept
summary: How embedding models turn text and images into vectors for semantic search (classic RAG), what they are good and bad at, the role of rerankers, embedding token costs, and why the embedding model is baked into every index.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s4-tokens-context-and-data]]"]
related: ["[[how-ai-finds-your-data]]", "[[tokens]]", "[[context-window]]", "[[agnostic-ai-platform]]", "[[ai-evals]]", "[[large-language-model]]"]
aliases: [embeddings, vector search, semantic search, vector store, RAG, reranker]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Embeddings and vector search

**TL;DR:** Semantic search (classic RAG) splits documents into chunks, runs each through an embedding model to get a vector, embeds the question the same way, and returns the closest chunks by meaning. It is strong for "find anything about X" in large prose and weak for exact IDs, numbers and tables. The embedding model is baked into the index, so changing it means re-indexing everything.

## What it is
- **Embedding model:** "Turns text, images and pages into vectors so semantic search can compare meaning" ([[source-ai-training-guide]] §2.3). It is one of several non-LLM models inside a harness ([[large-language-model]]).
- **Semantic search (classic RAG):** documents are chunked and embedded; the question is embedded too; the closest chunks are returned ([[source-ai-training-guide]] §2.3).
- **Reranker:** re-scores the top hits so the best few reach the language model. It "quietly shapes what the model sees," so include it in retrieval evals ([[source-ai-training-guide]] §2.3).
- **RAG** is feeding a model relevant documents at question time; it does not change the model and is not training ([[source-ai-training-guide]] Glossary).

## Why it matters
Semantic search is the right finder when the exact words are unknown, across large, mixed prose ([[source-s4-tokens-context-and-data]] [4:22]). But it is weak at exact strings, names and numbers, tables split across chunks, and freshness, since the index is a snapshot. "Embeddings miss exact IDs" and "chunking flattens tables" ([[source-ai-training-guide]] §2.3). For text documents the recommended pattern is hybrid: semantic plus keyword ([[how-ai-finds-your-data]]).

## How it works
1. **Index time:** parse, chunk, embed each chunk, store vectors. Embedding tokens are charged here; Gemini File Search charges $0.15 per million tokens to index and nothing to store or query (as of Oct 2026) ([[source-ai-training-guide]] §2.2; [[tokens]]).
2. **Query time:** embed the question, find nearest vectors, optionally rerank, place top chunks in the [[context-window]] with citations.
3. **Multimodal variant:** pages, images and diagrams are embedded alongside text so a text question can find a picture or a table in its original layout. Gemini File Search has embedded images and text together since May 2026 ([[source-ai-training-guide]] §2.3).

Examples of embedding models in use (as of Oct 2026): Gemini File Search uses gemini-embedding-001 for text and gemini-embedding-2 for images; OpenAI File Search uses OpenAI embeddings; a semantic plugin for Claude Code uses Voyage embeddings ([[source-ai-training-guide]] §2.3).

## Vector search vs. agentic search
Claude Code relies on agentic search (Glob, Grep, file reads) because Anthropic found it worked better than an early local vector index; semantic search can be added via MCP plugins. For code, semantic search is only a supplement ([[source-ai-training-guide]] §2.3).

> [!warning] An index is a copy of your data
> A vector store holds chunks of the source documents, often on different infrastructure with different access controls. Give it the same access rules and approvals as the source ([[source-ai-training-guide]] §2.3; [[source-s4-tokens-context-and-data]] [4:22]).

## In practice
- **Record which embedding model built each index** and keep an approved alternative. Swapping it is "the one model change that cannot be done in configuration alone," so the eval store tracks it ([[source-ai-training-guide]] §2.3; [[agnostic-ai-platform]]).
- The vendor-neutral API layer covers embedding calls as well as chat calls.
- Cite the page, not just the file; watch chunk boundaries that cut a paragraph.
- Never use semantic search for totals; use a structured query ([[source-s4-tokens-context-and-data]] [5:36]).

## See also
[[how-ai-finds-your-data]] · [[tokens]] · [[ai-evals]] · [[agnostic-ai-platform]]
