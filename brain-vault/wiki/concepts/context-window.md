---
type: concept
summary: The context window is the fixed token budget a model can consider at once, shared by input and output; covers what fills it, why long chats get expensive and forgetful, and how caching, retrieval and progressive disclosure keep it lean.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s4-tokens-context-and-data]]"]
related: ["[[tokens]]", "[[how-ai-finds-your-data]]", "[[large-language-model]]", "[[agent-skills]]", "[[ai-harness]]"]
aliases: [context, context length, context limit]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Context window

**TL;DR:** The context window is how much text a model can consider at once: one fixed token ([[tokens]]) budget shared by input and output. It is not memory; once something falls outside the window, it is gone. Documents, tool definitions, retrieved chunks and the conversation all compete for it, which is why retrieval, caching and progressive disclosure exist.

## What it is
- Glossary definition: "How much text a model can consider at once." Common misuse: "Mistaken for memory; once outside the window, it is gone" ([[source-ai-training-guide]] Glossary).
- It is a fixed budget shared by input and output together ([[source-ai-training-guide]] §2.2).
- Memory is different: information a tool saves and reuses across sessions, which the harness feeds back in ([[source-ai-training-guide]] Glossary; [[large-language-model]]).

## How it fills
In order, per Session 4 ([[source-s4-tokens-context-and-data]] [2:18]):
1. System prompt
2. Tool definitions (every connected MCP server adds its descriptions)
3. Chat history
4. Retrieved documents, usually the biggest block
5. The new question
6. Room reserved for the answer

The system prompt and tool definitions are identical every time, so they can be cached and re-read cheaply. On the receipt, input is the bulk of the bill, cached reads are cheap, and output is small.

## Why it matters
Two of Session 4's three common complaints trace here ([[source-s4-tokens-context-and-data]] [0:49]):
- **"It forgot what I said."** Long chats fill the window and early turns get dropped.
- **"The bill surprised us."** The API is stateless, so every turn re-sends the whole conversation; input grows each turn while output stays small ([[source-ai-training-guide]] §2.2).

Quality also suffers: very long contexts degrade attention, so stuffing the window is not free even when it fits; lean, well-organized context tends to produce better answers ([[source-ai-training-guide]] §2.2).

## Keeping it lean
- **New topic, new chat** ([[source-s4-tokens-context-and-data]] [2:51]).
- **Cache the stable prefix:** system prompt, tool definitions, reference documents.
- **Retrieve, don't stuff:** "put it all in context" only suits small, stable sets; larger sets need a finder ([[how-ai-finds-your-data]]). Claude Projects keeps project knowledge in context while it fits, then switches to a knowledge search tool that expands capacity up to 10x (as of Oct 2026) ([[source-ai-training-guide]] §2.3).
- **Progressive disclosure:** skills load metadata first (~80 tokens each) and the full SKILL.md (~2,000-token median) only when triggered, keeping the window free for the work ([[agent-skills]]; [[source-ai-training-guide]] §3.3).
- **Connect only the tools you need**, since each server's descriptions ride along every turn.
- **Swapping models changes the limit**, because tokenizers differ ([[tokens]]).

## In practice
Teach the fill order with a diagram of one request, then show a three-turn chat growing. The rule from Session 4: "Send less. Cache what's stable. Fetch with the finder that fits" ([[source-s4-tokens-context-and-data]] [5:24]).

## See also
[[tokens]] · [[how-ai-finds-your-data]] · [[agent-skills]] · [[source-s4-tokens-context-and-data]]
