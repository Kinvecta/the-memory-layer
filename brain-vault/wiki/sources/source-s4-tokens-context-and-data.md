---
type: source
summary: Transcript summary of Session 4, covering what a token is, token types and costs, how the context window fills, why long chats get expensive, and the six finders AI uses to fetch data.
sources: ["[[raw/transcripts/s4-tokens-context-and-data]]"]
related: ["[[source-ai-training-guide]]", "[[train-the-trainer-series]]", "[[tokens]]", "[[context-window]]", "[[how-ai-finds-your-data]]", "[[embeddings-and-vector-search]]", "[[source-s3-safe-prompting-and-verification]]", "[[source-s5-apis-endpoints-and-containers]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 4 - Tokens, Context and How AI Finds Your Data

**TL;DR:** Session 4 of the [[train-the-trainer-series]] (about 7 minutes) answers "what can the model actually see when it answers?" with two ideas: tokens, the unit the model reads, writes and bills, and finders, the ways tools fetch your data. Its rule: send less, cache what is stable, fetch with the finder that fits.

**Source file:** [[raw/transcripts/s4-tokens-context-and-data]]  ·  **Kind:** transcript  ·  **Date:** October 2026

## Key points
1. **Three complaints, one root cause** [0:49]: "the bill surprised us" (context re-sent in loops and long chats), "it forgot what I said" (early turns dropped from a full window), "it couldn't find the table" (wrong finder; table flattened into prose).
2. **Tokens** [1:16]: "The quarterly report is due Friday." is six words but eight tokens; a purchase-order line with a dollar amount splits into fourteen small tokens. Numbers and codes cost more, and every vendor's tokenizer counts differently, so any count is an estimate. See [[tokens]].
3. **Token types** [1:47]: input (instructions, tools, documents, history, question), output (priced higher, drives wait time), thinking (billed as output), cached (discount for a stable prefix), image and audio, tool descriptions, embedding (charged at indexing). "What you send costs more than what you get back."
4. **Context window budget** [2:18]: one fixed budget shared by input and output, filled in order by system prompt, tool definitions, chat history, retrieved documents (usually the biggest block), the new question, with room reserved for the answer. See [[context-window]].
5. **Long chats** [2:51]: every turn re-sends the whole conversation, so input grows while output stays small; caching makes repeated history cheap. Habit: when the topic changes, start a new chat.
6. **Six reasons tokens matter** [3:19]: cost (tokens per run times runs per month), capacity, speed, rate limits, quality (lean beats stuffed), swapping models.
7. **Finders** [3:45]: one question ("which vendors scored lowest on site safety last quarter?") goes to four finders at once: semantic search, keyword search (exact vendor ID), structured query (scores table), multimodal retrieval (chart on a scanned page). The harness merges results with citations. "The model never searches on its own." See [[how-ai-finds-your-data]].
8. **Six ways** [4:22]: everything in context, semantic search, keyword search, agentic search, structured queries, multimodal retrieval. An index is a copy of your data and needs the same access rules as the source ([[embeddings-and-vector-search]]).
9. **Match finder to data** [4:58]: memos use semantic plus keyword; tables use structured queries; scans use multimodal or vision; code uses agentic search; live records use structured queries only through an approved connection.
10. **Exercise** [5:36]: count tokens on your own prompt and multiply by monthly runs; pick finders for six questions (policy, ticket number, total spend by vendor, org chart slide, retry logic, three-page brief). "If you picked semantic search for total spend, think again."

## Worth quoting
> Send less. Cache what's stable. Fetch with the finder that fits.

> When the topic changes, start a new chat.

> The model never searches on its own. It reads what the finders return.

## Pages this source updated
- [[tokens]], [[context-window]], [[how-ai-finds-your-data]], [[embeddings-and-vector-search]]
