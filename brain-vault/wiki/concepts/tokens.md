---
type: concept
summary: What a token is (about four characters or three-quarters of a word), the eight token types and how each is priced as of Oct 2026, and why tokens drive cost, capacity, speed, rate limits, quality and model portability.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s4-tokens-context-and-data]]"]
related: ["[[context-window]]", "[[large-language-model]]", "[[how-ai-finds-your-data]]", "[[embeddings-and-vector-search]]", "[[agent-skills]]", "[[ai-evals]]", "[[workflows]]"]
aliases: [token, tokenizer, token cost]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Tokens

**TL;DR:** A token is the piece of text a model actually reads and writes, about four characters or three-quarters of an English word. Tokens are the unit of cost, capacity and speed, and what you send costs more than what you get back. Control them by caching what is stable, retrieving only what is needed, and keeping loops short.

## What it is
A token is a word, part of a word, a number or a punctuation mark. Code, tables, JSON, numbers and non-English text break into more tokens per word ([[source-ai-training-guide]] §2.2). Example: "The quarterly report is due Friday." is six words but eight tokens; a purchase-order line with a dollar amount splits into fourteen small tokens ([[source-s4-tokens-context-and-data]] [1:16]).

Every model has its own tokenizer, so any count is an estimate across vendors; one guide notes OpenAI's tokenizer undercounts Claude by roughly 15-20% on ordinary text, more on code ([[source-ai-training-guide]] §2.2).

## Token types (as of Oct 2026)
| Type | What it is | What to know |
|---|---|---|
| Input | System prompt, tool and skill definitions, retrieved chunks, whole conversation, new message | The bulk of volume; the API is stateless, so the full transcript is re-sent and charged every turn |
| Output | The answer, including code | Priced several times higher than input; main driver of latency |
| Thinking | Internal reasoning before answering | Billed as output; reported separately by Claude, OpenAI and Gemini |
| Cached input | Stable prefix stored by the provider | Claude: explicit cache_control, write ~1.25x input price, read ~0.1x; OpenAI: automatic for recently reused prompts; Gemini: implicit plus explicit |
| Image | Pictures and PDF pages | Gemini: 258 tokens per 768-pixel tile; Claude bills by image area; a scanned page often costs more than its text |
| Audio/video | Sampled per second | Transcribe first where only the words matter |
| Tool-use | Tool schemas, calls and results | Every connected MCP server adds its descriptions to input on every turn |
| Embedding | Text or images run through an embedding model | Charged at indexing; Gemini File Search: $0.15 per million tokens to index, nothing to store or query |

Source: [[source-ai-training-guide]] §2.2.

## Why it matters
- **Cost:** tokens per run times runs per month; levers are shorter prompts, caching, smaller models, fewer turns.
- **Capacity:** the [[context-window]] is one fixed budget shared by input and output.
- **Speed:** output is produced one token at a time.
- **Rate limits:** providers cap tokens per minute as well as requests; a batch job that works in testing can be throttled in production.
- **Quality:** very long contexts degrade attention; lean beats stuffed.
- **Agnosticism:** counts, costs and limits change when the model is swapped, so the eval store should record tokens per task alongside accuracy ([[ai-evals]]).

Source: [[source-ai-training-guide]] §2.2; [[source-s4-tokens-context-and-data]] [3:19].

## How it works in practice
- **Chat:** each turn re-sends the system prompt and every earlier message; output stays small; caching turns history into cheap reads. When the topic changes, start a new chat ([[source-s4-tokens-context-and-data]] [2:51]).
- **Workflow receipt:** saved prompt and tool definitions are cached; retrieved reports are new each run and dominate the bill; the answer is small ([[source-ai-training-guide]] §2.2).
- Skills stay cheap via progressive disclosure: ~80 tokens of metadata each vs. a ~2,000-token median SKILL.md ([[agent-skills]]).

> [!tip] Teach tokens early
> Stage 1 learners should see a token counter on one of their own prompts; Stage 3 workflows should log tokens per run from the first version. Cost surprises almost always come from re-sent context in loops, not from the answer ([[source-ai-training-guide]] §2.2).

Session 4 exercise: count your own prompt's input and output tokens, multiply by monthly runs, and estimate what a shorter prompt or caching would save ([[source-s4-tokens-context-and-data]] [5:36]).

## See also
[[context-window]] · [[how-ai-finds-your-data]] · [[source-s4-tokens-context-and-data]]
