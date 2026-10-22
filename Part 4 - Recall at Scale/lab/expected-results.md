# Lab 4 · Expected results (facilitators)

Reference vault, brain-tools (chunker v2), nomic-embed-text via Ollama, fresh index. Ranks: 1 = top; `-` = not in the top 20.

## B · Before the fix

```
question                                   kw   sem  hyb   expected
streamable HTTP vs stdio                    1     1    1   mcp-transports-stdio-vs-http
cosign                                      1     1    1   image-signing-and-provenance
how do I stop a web page from hijacking     2     4    1   prompt-injection
why does the assistant forget everything    5     2    3   agent-memory-layers
which model should I pick if the vendor     4     1    1   ai-resilience
crawl walk run                              -     -    -   five-stage-training-progression

keyword   recall@5 5/6   MRR 0.49
semantic  recall@5 5/6   MRR 0.63
hybrid    recall@5 5/6   MRR 0.72
```

## D · After adding `crawl walk run` at the end of the aliases of `wiki/concepts/five-stage-training-progression.md`

```
question                                   kw   sem  hyb   expected
streamable HTTP vs stdio                    1     1    1   mcp-transports-stdio-vs-http
cosign                                      1     1    1   image-signing-and-provenance
how do I stop a web page from hijacking     2     4    1   prompt-injection
why does the assistant forget everything    5     2    3   agent-memory-layers
which model should I pick if the vendor     4     1    1   ai-resilience
crawl walk run                              1     3    1   five-stage-training-progression

keyword   recall@5 6/6   MRR 0.66
semantic  recall@5 6/6   MRR 0.68
hybrid    recall@5 6/6   MRR 0.89
```

## C · Good explanations

- **hijacking my AI assistant → prompt-injection:** keyword 2, meaning 4, hybrid 1. Both judges rank it high, so fusion puts it first.
- **forget everything between chats → agent-memory-layers:** keyword 5, meaning 2. The page talks about memory and sessions, not "forget" or "chats", so meaning wins.
- **vendor disappears → ai-resilience:** keyword 4, meaning 1. A paraphrase of "switching models and vendors".

## Notes

- Without Ollama the semantic and hybrid columns repeat keyword (`brain search` falls back).
- Putting the alias first instead of last nudges the meaning rank (1 instead of 3), because aliases are part of the embedded text. Either way, measure.
- A brain-tools upgrade that changes chunking makes `brain index` rebuild everything once (several minutes with vectors).
- Extra practice questions: `extra-questions.csv` (8 more, all found by hybrid).
