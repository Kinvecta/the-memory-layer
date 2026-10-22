# Part 3 Research Brief: Ingest, query, lint (making knowledge compound)

*The Memory Layer, Part 3. Researched 21 Oct 2026. Every claim is tied to a source in the list at the end. Anything I could not verify is marked as unverified.*

## 1. The LLM Wiki pattern (Karpathy, April 2026)

Karpathy posted "LLM Knowledge Bases" on X in early April 2026 and followed it with the `llm-wiki` gist on **4 Apr 2026** [1][2]. The gist describes three operations:

- **Ingest:** "You drop a new source into the raw collection and tell the LLM to process it." He adds that "A single source might touch 10-15 wiki pages." *Our course says 3–8 pages per ingest. That is more conservative than Karpathy's figure, so say it is a deliberate choice for beginners.*
- **Query:** "You ask questions against the wiki." He also says "good answers can be filed back into the wiki as new pages."
- **Lint:** "Periodically, ask the LLM to health-check the wiki." He notes the LLM is also good at suggesting new questions to ask and new sources to find.
- **index.md** is "a catalog of everything in the wiki", and "The LLM updates it on every ingest." **log.md** is "an append-only record of what happened and when."

**Short quotes for slides (all from the gist [2]):**
- "the LLM is rediscovering knowledge from scratch on every question."
- "The knowledge is compiled once and then kept current, not re-derived on every query."
- "the wiki is a persistent, compounding artifact."
- "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
- "The wiki is just a git repo of markdown files."
- "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means."

**Scale and reception.** Secondary write-ups put his own wiki at about 100 articles and 400K words [3][4]. I could not fetch the original X post to confirm that figure. Sanity says the post approached 22M views [4]. One architectural review reports 5,000 gist stars in eight days and about 15 implementations in the first week [5]. That figure is secondary and unverified.

**Community implementations:** Astro-Han/karpathy-llm-wiki (Agent Skills for Claude Code, Cursor and Codex) [6], toolboxmd/karpathy-wiki [7], GD4AI/obsidian-llm-wiki (an Obsidian plugin) [8], and the `llm-wiki` GitHub topic [9].

**Critiques worth teaching:** the schema file (CLAUDE.md or AGENTS.md) is the real "compiler spec"; plain index files reportedly stop scaling beyond about 200 pages; and nothing marks old claims as stale or replaced [5]. Teams found that concurrent ingests forked the wiki and rebuilds overwrote human corrections [4].

## 2. "Compile once" vs. "retrieve every time": the honest evidence

**For compiling:**
- **GraphRAG** (Microsoft, 2024) builds an entity graph and community summaries ahead of time. On global sensemaking questions over 1M-token corpora, it beat vector RAG on comprehensiveness (about 72–83% win rate) and diversity. Its root-level summaries used only about 2–3% of the tokens [10].
- **RAPTOR** (ICLR 2024) pre-builds a tree of recursive summaries. Paired with GPT-4, it improved "the best performance on the QuALITY benchmark by 20% in absolute accuracy" [11].

**Against it, or mixed (2026 studies that test the LLM Wiki directly):**
- A preregistered comparison (Cochran, arXiv 2605.18490; 24 papers, 13 questions) found the wiki better at cross-paper synthesis. However, the wiki used **about 21× more tokens per query**, plain RAG matched it on single facts, and the "winner depended on the baseline, scorer and judge" [12].
- **WiCER** (Huerta, arXiv 2605.07068) found that blind compilation **over-compressed**: a 50% length target produced 12%. Wrong answers rose to 53–60%, against 17% from the raw documents. A compile, evaluate and refine loop (in effect, lint) cut wrong answers from 55% to 25% [13].
- A progressive-disclosure ablation on a **709-page** LLM-maintained wiki found that serving an index first plus a retrieval tool cut answer cost by **30–58%** with no loss of quality [14].

**Teaching takeaway.** Compiling wins on synthesis and on answers you will reuse. Raw retrieval still wins on exact facts. This is why the recall ladder ends at **raw/** and why lint is essential: lint is what catches facts lost during compression. Zettelkasten practitioners name the failure on the other side the **"Collector's Fallacy"**: "'to know about something' isn't the same as 'knowing something'" [15].

## 3. Summarization and citation reliability

- **Vectara Hallucination Leaderboard** (summaries of 7,700+ articles, updated 11 May 2026): rates range from **1.8% to 24.2%**, and frontier models sit around 5–12% (GPT-5.4 at 7.0%, Claude Sonnet 4.6 at 10.6%) [16]. Rates rise with document length and complexity [17].
- **Tow Center / CJR (Mar 2025):** 8 AI search tools were asked to identify the source of 200 news excerpts. They were wrong more than **60%** of the time, from Perplexity at 37% to Grok 3 at 94%. Of ChatGPT's 134 wrong answers, only 15 hedged [18][19].
- **EBU/BBC (Oct 2025):** more than 3,000 answers from assistants, checked by 22 public broadcasters in 18 countries. **45%** had a significant issue and **31%** had serious sourcing problems [20].
- **Generative search verifiability** (Liu et al., EMNLP 2023): only **51.5%** of sentences were fully supported by their citations, and **74.5%** of citations supported their sentence [21].
- **Fabricated references** (Walters & Wilder, *Sci. Reports* 2023): 55% of GPT-3.5's citations and 18% of GPT-4's were fabricated. Of the real ones, 43% and 24% respectively had substantive errors [22].

**Why "cite every claim" plus a human spot-check.** A citation makes a claim checkable, but these studies show citations are often wrong, and even LLM judges disagree on groundedness (ρ = 0.04 in [12]). So a person should open 2–3 citations per ingest.

## 4. Update before create: entity resolution and dedup

- **Mem0** (2025) formalizes "search before create": for each new fact it retrieves the 10 most similar memories, and the LLM picks **ADD / UPDATE / DELETE / NOOP** [23]. In ingest terms, update the existing page and create a new one only if nothing matches.
- **Neo4j Agent Memory** normalizes names, merges automatically at a score of 0.90 or above, *flags for review* between 0.85 and 0.90, and treats embedding similarity "as a hint, not proof" [24]. Teach the same rule: when unsure, the agent proposes a merge and the human decides.
- **Conflict callout** (Obsidian syntax [25]). Put `> [!warning] Conflict` on the first line of a blockquote; `caution` and `attention` are aliases. A `-` after the type, as in `> [!warning]-`, makes the callout start folded. Suggested pattern:
  ```
  > [!warning] Conflict: launch date
  > [[source-a]] says March 2026; [[source-b]] says June 2026. Unresolved.
  ```
  Keeping both claims follows Sanity's lesson that conflict decisions must survive rebuilds [4].

## 5. Lint for knowledge bases

**Mechanical checks:**
- **Obsidian CLI** (introduced in 1.12, Feb 2026) has `orphans`, `deadends` and `unresolved` commands, plus `backlinks`, `properties` and `search` [26]. Obsidian CEO kepano claimed the `orphans` command is "54x faster than grep, 70,000x cheaper than MCP" [27]. That is a vendor claim from an X post.
- The community plugin **"Find orphaned files and broken links"** [28].
- **Dataview** orphan query: `list from "" where length(file.inlinks) = 0 and length(file.outlinks) = 0` [29].
- **Obsidian Bases** (core since 1.9, May 2025) gives table views filtered by properties [30]. Use it for stale `updated:` dates or missing frontmatter.

**Docs-as-code analogues:**
- **lychee**: a Rust link checker for Markdown and HTML [31].
- **markdownlint**: structure and style rules for Markdown [32].
- **Vale**: rule-based prose linting [33].

**Why links rot.** Pew (2024) found that **38%** of web pages from 2013 were gone by 2023, and that **54%** of Wikipedia pages have at least one dead reference link [34]. That is an argument for keeping an immutable copy of each source in raw/ rather than only a URL.

Judgment checks (contradictions, missing concepts, uncited claims) need the LLM. Use WiCER's probe-and-repair loop as the evidence that they pay off [13].

## 6. Git as the undo button

- **Claude Code checkpoints** (`/rewind` or Esc Esc) do *not* track changes made through Bash or most subagent edits, and the docs call them "Not a replacement for version control" [35]. **Cursor checkpoints** are local, cleaned up automatically, and "not version control" [36].
- **Aider:** "Whenever aider edits a file, it commits those changes with a descriptive commit message." `/undo` discards the last change and `/diff` reviews it [37]. This is a vendor precedent for one commit per operation.
- **Git worktrees:** Claude Code's `--worktree` gives each parallel session its own branch and files, "so edits in one session never touch files in another" [38]. Use this to run two ingests in parallel safely.
- **`git revert` vs `reset`.** `revert <sha>` adds a new commit that undoes a bad ingest and keeps the history. `reset --hard` erases the history. Teach revert by default.

## 7. Ingest-specific risks (brief, since Part 6 covers them)

- **Prompt injection.** OWASP LLM01:2025: "Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files." Mitigations: mark external content as untrusted and require human approval for privileged actions [39]. The academic origin is Greshake et al. 2023 [40]. Anthropic reported a **23.6%** attack success rate across 123 tests for its browser agent, reduced to **11.2%** with mitigations [41].
- **Over-capturing.** See the Collector's Fallacy [15]. WiCER shows the reverse failure, over-compression [13]. The 1 / 3–8 / 0–3 page budget guards against both.

## 8. Evidence cards

1. **"60%+ wrong"**: AI search tools misidentified the source of news excerpts in more than 60% of tests [18].
2. **"45% / 31%"**: share of AI news answers with a significant issue, and with serious sourcing problems [20].
3. **"51.5%"**: share of generative-search sentences fully supported by their citations [21].
4. **"1.8–24.2%"**: hallucination rates when summarizing a single document; frontier models are about 5–12% [16].
5. **"55% → 25%"**: wrong answers from a compiled wiki before and after compile, evaluate and refine (lint) [13].
6. **"21×"**: tokens per query for a wiki agent vs. single-round RAG. Compiling has a cost [12].
7. **"38%"**: share of 2013 web pages gone by 2023, which is why you keep raw/ copies [34].
8. **"23.6% → 11.2%"**: prompt-injection success rate before and after mitigations [41].

## Analogies for non-engineers

1. **Ingest = a librarian shelving a new book.** They update the card catalog (index.md), cross-reference related shelves (concept pages) and note it in the acquisitions log (log.md). *Map back:* one source page, 3–8 updated pages, plus index and log entries.
2. **Compile vs. retrieve = a ledger vs. a shoebox of receipts.** RAG digs through the shoebox for every question. The wiki is the ledger, balanced as each receipt comes in. You keep the shoebox (raw/) for audits.
3. **Search before create = a hospital's patient records.** Before opening a new chart, the clerk checks whether "Bob Smith, DOB…" already exists. Duplicate charts are how errors happen. *Map back:* ADD, UPDATE or NOOP; when unsure, flag the possible duplicate for review.
4. **Lint = a spell-checker plus an editor.** The spell-checker finds broken links and orphan pages mechanically. The editor notices that chapter 3 contradicts chapter 7. You need both.
5. **Git = track changes with a time machine.** Every ingest is one tracked edit you can review and reject. `revert` is "undo, with a note saying you undid it", never tearing out pages.

## Sources

1. Karpathy, "LLM Knowledge Bases" (X) https://x.com/karpathy/status/2039805659525644595
2. Karpathy, llm-wiki gist https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
3. DAIR.AI Academy https://academy.dair.ai/blog/llm-knowledge-bases-karpathy
4. Sanity, "Taking Karpathy's wiki to work" https://www.sanity.io/blog/taking-karpathys-wiki-to-work
5. "The Schema Is the Product" https://cozypet.github.io/llm-wiki-schema/
6. https://github.com/Astro-Han/karpathy-llm-wiki
7. https://github.com/toolboxmd/karpathy-wiki/tree/main/
8. https://github.com/gd4ai/obsidian-llm-wiki
9. https://github.com/topics/llm-wiki
10. Edge et al., GraphRAG https://arxiv.org/html/2404.16130v2
11. Sarthi et al., RAPTOR https://www.arxiv.org/abs/2401.18059
12. Cochran, RAG vs LLM-Compiled Wiki https://arxiv.org/abs/2605.18490
13. Huerta, WiCER https://arxiv.org/html/2605.07068
14. Cochran, Progressive Disclosure ablation https://arxiv.org/html/2607.04576
15. Tietze, "The Collector's Fallacy" https://www.zettelkasten.de/posts/collectors-fallacy
16. Vectara leaderboard https://github.com/vectara/hallucination-leaderboard
17. Vectara, next-gen leaderboard https://vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard
18. CJR Tow Center https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
19. Nieman Lab https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/
20. EBU/BBC News Integrity report https://www.bbc.co.uk/aboutthebbc/documents/news-integrity-in-ai-assistants-report.pdf (summary: https://www.infodocket.com/2025/10/22/bbc-largest-study-of-its-kind-shows-ai-assistants-misrepresent-news-content-45-of-the-time-regardless-of-language-or-territory/)
21. Liu et al., Verifiability in Generative Search Engines https://arxiv.org/abs/2304.09848v2
22. Walters & Wilder 2023 https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/
23. Mem0 paper https://arxiv.org/pdf/2504.19413
24. Neo4j Agent Memory, resolution and dedup https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/
25. Obsidian Help, Callouts https://obsidian.md/help/callouts
26. Obsidian CLI guide https://www.dsebastien.net/the-complete-guide-to-the-obsidian-cli-everything-you-can-do-from-the-terminal/
27. kepano (X) https://x.com/kepano/status/2022305748735381751
28. https://community.obsidian.md/plugins/find-unlinked-files
29. Obsidian forum, Find orphan notes https://forum.obsidian.md/t/find-orphan-notes/817/15
30. Obsidian 1.9.0 changelog https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0
31. lychee https://github.com/lycheeverse/lychee
32. markdownlint https://github.com/DavidAnson/markdownlint
33. Vale https://vale.sh/
34. Pew, "When Online Content Disappears" https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/
35. Claude Code checkpointing https://code.claude.com/docs/en/checkpointing
36. Cursor checkpoints https://docs.cursor.com/agent/chat/checkpoints
37. Aider git docs https://aider.chat/docs/git.html
38. Claude Code worktrees https://code.claude.com/docs/en/worktrees.md
39. OWASP LLM01:2025 https://genai.owasp.org/llmrisk/llm01-prompt-injection/
40. Greshake et al. 2023 https://arxiv.org/abs/2302.12173v2
41. Anthropic Claude for Chrome (via Simon Willison) https://simonwillison.net/2025/Aug/26/piloting-claude-for-chrome/
