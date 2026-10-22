# The Memory Layer, Part 4: Recall at scale (keyword, semantic, hybrid)

Research brief, 22 Oct 2026. Bracketed numbers refer to the Sources list.

## 1. When an index file stops being enough

- **Karpathy's index.md (gist created 4 Apr 2026).** He calls index.md "a catalog of everything in the wiki." The LLM "reads the index first to find relevant pages, then drills into them." His scale claim: "This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)." He adds that "at small scale the index file is enough, but as the wiki grows you want proper search." For that he points to qmd, "a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device" [1].
- **The critique.** The "LLM Wiki v2" gist says index.md "works up to maybe 100-200 pages. Beyond that, the index itself becomes too long for the LLM to read in one pass, and you need real search." In a reply, the author puts the break at "200-500 documents" [2]. This is practitioner opinion, not a measurement.
- **Why not just load everything?**
  - *Lost in the Middle* (Liu et al., 2023; TACL 2024) found a U-shaped accuracy curve: the middle of a long context is used worst. With GPT-3.5 and 20 documents, accuracy with the answer in the middle was 53.8%. That is *below* its closed-book score with no documents at all (56.1%) [3].
  - *Context Rot* (Chroma, Jul 2025) tested 18 models, and performance fell as input grew, even on simple tasks. A single distractor already hurt. On LongMemEval, focused prompts of about 300 tokens beat full prompts of about 113k tokens [4].
  - *NoLiMa* (ICML 2025) asked questions with minimal word overlap with the answer. At 32K tokens, 10 of 12 long-context models fell below half their short-context score. GPT-4o went from 99.3% to 69.7% [5].
  - Anthropic's rule of thumb: under about 200k tokens (roughly 500 pages), just put everything in the prompt. Above that, retrieve [6].

## 2. BM25

BM25 is the standard keyword ranking function from the probabilistic relevance framework (Robertson & Zaragoza, 2009) [7]. It is the default in Lucene, Elasticsearch and OpenSearch.

**Plain English.** A page scores higher when it uses your query words more. This is *term frequency*, with diminishing returns: the tenth mention adds far less than the second, and **k1** sets how fast the curve flattens. Rare words count more than common ones. This is *inverse document frequency*: "SQLite" in your vault is a strong signal, while "the" is not. Long pages get a mild penalty so they can't win just by containing more words. This is *length normalization*, and **b** (from 0 to 1) sets its strength.

**Typical values.** Elasticsearch and Lucene default to k1 = 1.2 and b = 0.75 [8]. The commonly cited range for k1 is about 1.2 to 2.0, so brain-tools' k1 = 1.4 / b = 0.75 is conventional.

**A strong baseline.** BEIR (Thakur et al., 2021) tested zero-shot retrieval across 18 datasets and concluded: "BM25 is a robust baseline" [9]. In 2025, BM25 also did "very well" on LIMIT, where dense embedders failed [10].

**When keywords win.** Exact names, acronyms (RMF, ATO), error codes (`ORA-01017`), ticket numbers, IDs, version strings and rare jargon.

## 3. Embeddings and semantic search

**What an embedding is.** A model maps text to a vector, for example 768 numbers, that acts as coordinates for its meaning. *Cosine similarity* measures the angle between two vectors: 1 means the same direction and about 0 means unrelated. "Car" and "vehicle" appear in similar contexts during training, so their vectors point the same way even though they share no letters.

**brain-tools' model: nomic-embed-text v1.5** [11][12]
- 137M parameters and 768 dimensions, with Matryoshka truncation to 512, 256, 128 or 64 dimensions.
- 8,192-token native context. Ollama lists 2K, which is plenty for 220-word chunks.
- Apache-2.0 license, with open weights and training data.
- Required prefixes: "the text prompt must include a task instruction prefix." Use `search_query:` for queries and `search_document:` for documents. The other prefixes are `clustering:` and `classification:`.
- 274 MB download in Ollama.

**Local alternatives**
- **EmbeddingGemma** (Sep 2025): 308M parameters, 768 dimensions, 2K context, under 200 MB of RAM when quantized, and over 100 languages. Google calls it the top open multilingual embedder under 500M parameters on MTEB [13]. It is qmd's default embedder [14].
- **Qwen3-Embedding** (0.6B, 4B and 8B; Apache-2.0): 32K context. The 8B model ranked #1 on MTEB multilingual with 70.58 as of 5 Jun 2025 [15].
- **bge-m3**: 567M parameters, 8K context, and dense, sparse and multi-vector output [16].
- **mxbai-embed-large**: 670 MB, with a 512-token context [17].

**MTEB landscape.** A March 2026 roundup lists Qwen3-Embedding-8B, NV-Embed-v2 (non-commercial), Gemini embedding-001 and voyage-3-large near the top. It also warns that MTEB averages many task types, so read the retrieval nDCG@10 column and test on your own data [18][19].

**Privacy.** With Ollama, both the note text and the vectors stay on your machine and in your local SQLite file. No embedding API ever sees them.

**Weaknesses.** Embeddings struggle with exact tokens (IDs, codes, rare names), numbers ("2023 budget" vs "2024 budget") and negation ("projects *not* on Postgres" lands near "projects on Postgres").

**LIMIT** (Weller et al., Google DeepMind and JHU, Aug 2025) [10]
- The paper proves that a single vector of dimension *d* can only represent a bounded number of distinct top-k result sets.
- Even with vectors optimized directly on the test set, the extrapolated breaking point is about 500k documents at d=512 and about 1.7M at d=768.
- On a deliberately simple "who likes X?" dataset, Qwen3, Gemini Embedding, GritLM and E5-Mistral all struggled, while BM25 did very well.

## 4. Hybrid search and Reciprocal Rank Fusion

**Origin.** Cormack, Clarke & Büttcher, SIGIR 2009: "k = 60 was fixed during a pilot investigation and not altered." The authors note the exact value isn't critical [20].

> **RRF score(d) = Σ over each ranked list r of 1 / (k + rank_r(d)),  k = 60**

**Worked example.** A page ranked #1 by BM25 and #3 by embeddings scores 1/61 + 1/63 ≈ 0.032. A page ranked #1 in only one list scores ≈ 0.016, so agreement wins. Because RRF uses ranks only, BM25 scores and cosine scores never need to be on the same scale. brain-tools adds a small bonus on top so curated wiki pages outrank raw sources.

**Evidence**
- **Anthropic Contextual Retrieval** (Sep 2024), measuring failure as 1 − recall@20 [6]:

  | Setup | Failure rate | Change from baseline |
  |---|---|---|
  | Baseline | 5.7% | — |
  | Contextual embeddings | 3.7% | −35% |
  | Plus contextual BM25 | 2.9% | −49% |
  | Plus reranking | 1.9% | −67% |

- **Elastic** (Jul 2023), averaged over BEIR: RRF hybrid improved nDCG@10 by 18% over BM25 and 1.4% over ELSER alone [21].
- **OpenSearch** (Feb 2025): RRF hybrid beat neural-only on 6 of 6 BEIR sets and beat BM25 on 5 of 6. The exception was TREC-COVID (−3%) [22]. So hybrid is not *always* better than BM25.
- **Weaviate** (Aug 2023): score-based fusion recalled about 6% more than rank-based fusion on FiQA. The fusion method matters at the margin [23].

**Rerankers in one line.** A slower model reads the query and each candidate together and re-orders the top 50–150 results. In Anthropic's test, this step took failure reduction from 49% to 67%.

## 5. Chunking

- **Strategies.** Fixed-size chunking splits every N tokens. Recursive or heading-aware chunking splits on headings, then paragraphs, then sentences. Semantic chunking splits where embedding similarity between neighbouring sentences drops.
- **Chroma** (Jul 2024): chunking choice swung recall by up to 9%. A recursive splitter scored 88.1 recall at 200 tokens and 89.5 at 400 tokens. The common 800-token / 400-overlap default scored 85.4. Overlap didn't help a large embedder but did help a small one. Caveat: a small corpus and synthetic queries [24].
- **NVIDIA** (Jun 2025): page-level chunks were the most accurate (0.648) and the most consistent. 128 and 2,048 tokens both underperformed, and the best size varied by dataset [25].
- **Vectara** (Oct 2024): "the computational costs associated with semantic chunking are not justified by consistent performance gains" [26].
- **What this means for brain-tools.** 220 words is about 290 tokens, which sits in the 200–400 token sweet spot. Splitting on headings is free structure, and dropping overlap matches Chroma's findings. qmd, by comparison, uses about 900 tokens with 15% overlap [14].
- **Why summaries and aliases help.** A chunk like "It cut costs 20%" is meaningless on its own. Anthropic prepends 50–100 tokens of document context to each chunk [6]. Adding each note's `summary` and `aliases` to its chunks is a cheap version of that, with no LLM needed. It also gives BM25 the synonyms (for example "RAG" for "retrieval-augmented generation").

## 6. Measuring recall

**Metrics in plain words**
- **Recall@k:** the share of the right pages that made the top k.
- **MRR:** 1 divided by the rank of the first right page (1, 0.5, 0.33…), averaged over all questions.
- **nDCG@k:** rewards putting the most relevant pages highest, with lower positions discounted. BEIR and MTEB report nDCG@10 [9].

**Golden set**
- Write 20–50 real questions, each paired with the page or pages that should answer it.
- Mix them: about a third exact terms, a third paraphrases, and a third multi-page questions.
- Store them as BEIR-style qrels: `query_id, page_path, relevance`.
- Ragas `IDBasedContextRecall` compares retrieved IDs with reference IDs and needs no LLM, which fits page paths well [27].

**Scoring sheet.** Use one row per question with these columns: expected page; rank under keyword, semantic and hybrid; hit@5 (yes/no); and 1/rank. Average the columns. Re-run after any change to chunking, aliases or k1/b.

## 7. Evidence cards

1. **"~100 sources, ~hundreds of pages."** Karpathy's own limit for using index.md alone [1].
2. **53.8% < 56.1%.** A buried answer did worse than having no documents at all (GPT-3.5) [3].
3. **10 of 12 models fell below half their short-context score at 32K tokens.** GPT-4o went from 99.3% to 69.7% [5].
4. **18 of 18 models** degraded as input length grew [4].
5. **−49% / −67%.** Failed retrievals cut by contextual embeddings plus BM25, and then by adding a reranker [6].
6. **"BM25 is a robust baseline."** BEIR, across 18 datasets [9].
7. **+18% nDCG@10.** RRF hybrid vs BM25 alone, averaged over BEIR [21].
8. **k = 60**, "fixed during a pilot investigation and not altered" (2009) [20].

## 8. Analogies for non-engineers

1. **BM25 is a back-of-book index.** Look up "ORA-01017" and it sends you to page 212. Rare words make the best entries, and a page that mentions a term five times is probably about it. *Map back:* BM25 is an automatic index that weights rare words and stops long chapters from cheating.
2. **Embeddings are a librarian who knows meaning.** Ask about "fixing my car" and she brings the vehicle-maintenance binder, but she's shaky on part #4471-B. *Map back:* embeddings match synonyms but can miss exact codes.
3. **RRF is two judges merging ranked lists.** One judges wording and the other judges meaning. Their scores use different scales, so you don't average them; you reward whatever both rank highly. *Map back:* each list contributes 1/(60 + rank), so agreement rises to the top.
4. **Chunking is recipe cards with good titles.** A 40-page chapter is hard to search. A card titled "Lasagna (aka pasta al forno), serves 8" is easy to find. *Map back:* each chunk is a card, and the summary and aliases are its title and nicknames.
5. **An eval set is a quiz with an answer key.** You only know whether a new study method works by retaking the same quiz. *Map back:* the golden set is the quiz, Recall@5 and MRR are the grade, and you retake it after every change.

## Not verified

- The 100–200 and 200–500 page thresholds come from one practitioner [2]. They are not benchmarks.
- I could not confirm the MTEB #1 as of Oct 2026. Check [19] live.
- I did not retrieve LIMIT's exact recall@100 figures or a benchmark that quantifies negation failures.
- I confirmed the k1 and b defaults only from Elastic's documentation. I did not retrieve Robertson & Zaragoza's exact sentence on the recommended range.

## Sources

1. Karpathy, "llm-wiki" gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. rohitg00, "LLM Wiki v2": https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
3. Liu et al., "Lost in the Middle": https://arxiv.org/abs/2307.03172
4. Chroma, "Context Rot": https://www.trychroma.com/research/context-rot
5. Modarressi et al., "NoLiMa": https://huggingface.co/papers/2502.05167
6. Anthropic, "Introducing Contextual Retrieval": https://www.anthropic.com/news/contextual-retrieval
7. Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond": https://ir.webis.de/anthology/2009.ftir_journal-ir0anthology0volumeA3A4.0/
8. Elasticsearch similarity documentation: https://www.elastic.co/guide/en/elasticsearch/reference/6.x/index-modules-similarity.html
9. Thakur et al., "BEIR": https://arxiv.org/abs/2104.08663
10. Weller et al., "On the Theoretical Limitations of Embedding-Based Retrieval": https://arxiv.org/abs/2508.21038
11. nomic-embed-text-v1.5 model card: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
12. Ollama, nomic-embed-text: https://ollama.com/library/nomic-embed-text
13. Google, "Introducing EmbeddingGemma": https://developers.googleblog.com/introducing-embeddinggemma/
14. tobi/qmd: https://github.com/tobi/qmd
15. Qwen3-Embedding model card: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
16. Ollama, bge-m3: https://ollama.com/library/bge-m3
17. Ollama, mxbai-embed-large: https://ollama.com/library/mxbai-embed-large
18. PremAI, embedding models for RAG (2026): https://www.premai.io/blog/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/
19. MTEB leaderboard: https://huggingface.co/spaces/mteb/leaderboard
20. Cormack, Clarke & Büttcher, "Reciprocal Rank Fusion" (SIGIR 2009): https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf
21. Elastic, hybrid retrieval: https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid
22. OpenSearch, RRF for hybrid search: https://opensearch.org/?p=4023
23. Weaviate, hybrid search fusion algorithms: https://weaviate.io/blog/hybrid-search-fusion-algorithms
24. Chroma, "Evaluating Chunking Strategies": https://trychroma.com/research/evaluating-chunking
25. NVIDIA, chunking strategy: https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/
26. Qu, Bao & Tu, "Is Semantic Chunking Worth the Computational Cost?": https://arxiv.org/abs/2410.13070
27. Ragas, Context Recall: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/
