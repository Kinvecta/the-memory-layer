---
name: brain-query
description: Answer a question from the brain with wikilink citations, climbing the recall ladder from cheapest to most expensive. Use when the user asks what the brain knows, asks "what did we decide", "where did I note", or any question the vault might cover.
---

# Query the brain

## Recall ladder (stop as soon as you have enough)

1. **Core memory** (`memory/core.md`). This is often already loaded.
2. **Index.** Read `index.md`, pick the 1–3 pages whose summaries fit, and read them.
3. **Search.** Run `brain search "<question in natural words>" -k 6`, or call `brain_search` over MCP.
   - Use `--mode keyword` for exact terms, acronyms and names.
   - Use the default hybrid mode for "how", "why" and "anything about…" questions.
   - Use `--folder wiki/decisions/` to narrow the search.
4. **Graph.** Follow `[[links]]` and backlinks from the pages you read. `brain_read` lists both.
5. **Raw.** Open the cited `raw/` file only when you need exact wording or numbers.

## Answer format

- Lead with the answer, then the supporting points. Cite each point with `[[page]]`.
- Say what the brain **does not** cover, rather than filling gaps from general knowledge. If you add
  general knowledge, label it.
- If pages disagree, show both sides and their sources.

## Make knowledge compound

If the answer took real synthesis, such as comparing pages or connecting ideas, offer to save it as
`wiki/questions/<kebab-question>.md` using `templates/question.md`. Then add it to `index.md` and log it.
The next time someone asks, recall is a single read.
