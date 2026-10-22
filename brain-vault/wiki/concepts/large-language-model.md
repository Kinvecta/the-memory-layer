---
type: concept
summary: What a large language model (LLM) is, how it is made, what it is not (six common myths), and why it is only one of several models inside a harness.
sources: ["[[raw/transcripts/s1-what-an-llm-is]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[ai-harness]]", "[[tokens]]", "[[context-window]]", "[[hallucination-and-verification]]", "[[chatbot-workflow-agent]]", "[[how-ai-finds-your-data]]", "[[embeddings-and-vector-search]]"]
aliases: [LLM, model, language model]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Large language model (LLM)

**TL;DR:** An LLM is a trained engine that predicts the next piece of text one token ([[tokens]]) at a time; everything it does, from memos to code, comes from repeating that one step. Its weights are frozen once deployed, so it does not look things up or learn from your chats; the [[ai-harness]] around it fetches, remembers and acts. That same mechanism makes it fluent and also makes it fluently wrong.

## What it is
- **Definition:** "the trained engine that predicts and produces text" ([[source-ai-training-guide]] Glossary). "Large" means billions of learned settings called weights; "model" means the engine only, not the app around it ([[source-s1-what-an-llm-is]] [1:25]).
- **The next-token loop:** given "The report is due on," the model scores every possible next token, picks "Friday," appends it, and runs again with "Friday" now in context ([[source-s1-what-an-llm-is]] [1:25]).
- Examples of models: Claude, GPT, Gemini. The model "reads, reasons and writes" ([[source-ai-training-guide]] §2.1).

## Why it matters
People credit or blame the model for what the harness allowed or blocked ([[source-ai-training-guide]] §2.1). Knowing the model is only the engine explains why the same model can be safe in one app and risky in another, and why "customizing AI" usually means prompts, skills and retrieval, not training.

## How it works: three stages
1. **Pretraining:** learns language and patterns by predicting the next token across an enormous amount of text.
2. **Post-training:** tuned to follow instructions, refuse harmful requests, and use tools.
3. **Deployment:** weights are frozen and a harness is wrapped around it.

Consequences: the model has a knowledge cutoff, does not learn from your chats, and sees anything current only because the harness fetched it ([[source-s1-what-an-llm-is]] [2:12]).

## Six myths (all false)
| Belief | Reality |
|---|---|
| "It looks things up." | It generates; it fetches only if the harness gives it a tool. |
| "It learns from my chats." | Weights are frozen; "memory" is the harness saving notes and feeding them back. |
| "It knows today's news." | Only up to its cutoff, plus whatever is fetched. |
| "Same question, same answer." | Output varies run to run. |
| "Wrong answers are rare." | Confident, fluent errors are a normal failure mode ([[hallucination-and-verification]]). |
| "Customizing means training." | Usually good prompts, skills and retrieval are enough. |

Source: [[source-s1-what-an-llm-is]] [2:47]; the glossary adds that RAG "does not change the model" and fine-tuning is rarely needed ([[source-ai-training-guide]] Glossary).

## Not the only model in the request
A single request usually passes through several models: a classifier screens the question, a vision model reads scans, an embedding model ([[embeddings-and-vector-search]]) and a reranker find passages, the language model writes, another classifier screens output, and a person checks the numbers. "The language model is the star, but it writes near the end" ([[source-s1-what-an-llm-is]] [3:29]). The guide lists embedding models, rerankers, vision and document models, speech models, classifiers and safety models, and generation models for images and code, each a dependency to record ([[source-ai-training-guide]] §2.3). See [[how-ai-finds-your-data]].

## In practice
- Paste the source rather than asking the model to recall facts ([[safe-prompting]]).
- Expect variation and errors; verify before use.
- Pin a named model version, never "latest" ([[ai-resilience]]).

## See also
[[ai-harness]] · [[chatbot-workflow-agent]] · [[tokens]] · [[context-window]] · [[source-s1-what-an-llm-is]]
