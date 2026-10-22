# Research Brief: Building an AI "Second Brain" Any LLM Can Recall From

Compiled 21 Oct 2026 for the AI Brain Series. Sources are listed at the end. Re-verify tool versions
before you teach from this brief.

## 1. The core idea

A second brain is a folder of plain markdown files that both people and AI harnesses can read and write.
Obsidian is the most popular front end because it adds wikilinks, backlinks, a graph view, properties and
templates on top of plain files. None of that locks you in. The same folder works in VS Code, Logseq,
Foam, a git repo, or no editor at all. Any harness that can read files can use the folder as long-term
memory: Claude Code, Cowork, Codex CLI, Gemini CLI, Cursor, or a local model through LM Studio or Ollama.

Why this works:

- **Context windows reset.** Every session starts empty. Memory has to live outside the model.
- **Markdown is the lowest common denominator.** Every model reads it well, and every tool can open it.
  It also diffs cleanly in git.
- **Links are explicit relationships.** A `[[wikilink]]` is a connection the author chose. Embedding
  similarity only guesses at connections.

## 2. The LLM Wiki pattern (Karpathy, April 2026)

Andrej Karpathy described a "hacky collection of scripts" that turns raw documents into an
LLM-maintained wiki. The post spread widely, and the community converged on this shape:

| Layer | Purpose |
|---|---|
| `raw/` | Immutable sources: clipped articles, papers, transcripts. The LLM reads them and never edits them. |
| `wiki/` | LLM-written pages: source summaries, concepts, entities, comparisons. Humans mostly read this layer. |
| Schema file (`CLAUDE.md` / `AGENTS.md`) | Folder rules, naming, templates and workflows. Write-ups of the pattern call it the most important file, because without it output is inconsistent. |
| `index.md` | A catalog the model reads first, so it can find pages without loading everything. |
| `log.md` | An append-only record of operations. |

**Operations:**

- **Ingest.** Summarize a source, update the concept and entity pages it touches, then update the index
  and the log. One source touches many pages.
- **Query.** Read the index, then the relevant pages, and answer with citations. Good answers are saved
  as new pages, so knowledge compounds.
- **Lint.** A periodic health check for contradictions, orphans, stale claims and gaps. One community
  member described the result as a knowledge base that "heals itself."

**Why it can skip RAG at small scale.** Explicit links and summaries in an index replace
nearest-neighbor search, and every claim traces back to a readable file. Write-ups give the useful range
as roughly 100 to 10,000 high-signal documents, or about 50 to 200 sources for one person. Past that, add
hybrid search.

## 3. Memory layers (from agent-memory practice)

| Layer | Lifetime | Example file |
|---|---|---|
| Core / critical facts | Always loaded, around 100–300 words | `memory/core.md` |
| Working | One session | `memory/working.md` |
| Episodic | Dated records of what happened | `memory/episodes/2026-10-21-*.md` |
| Semantic | Distilled facts with evidence and confidence | `wiki/` pages |

A scheduled **heartbeat** turns episodic memory into semantic memory. It archives stale working memory,
reviews recent episodes, promotes durable facts, rewrites core memory, flags stale pages, and writes a
briefing.

## 4. Recall tiers

1. **Plain file access.** The harness greps and reads files. Zero setup, and it works everywhere.
2. **Index-first navigation.** Read `index.md`, then open 1–3 pages. This keeps token use low.
3. **Keyword search (BM25).** Exact terms, acronyms and names. No dependencies.
4. **Semantic search (embeddings).** Meaning-based matches using a local embedding model, such as
   `nomic-embed-text` via Ollama, or the Smart Connections plugin. A local model keeps data on the machine.
5. **Hybrid.** Keyword and semantic results merged with Reciprocal Rank Fusion. This is the best default
   once the vault passes a few hundred pages.
6. **MCP server.** Exposes search, read and remember as tools to any MCP host. Options include community
   servers built on the Obsidian Local REST API plugin, the Smart Connections MCP, or a small custom server.
7. **Official Obsidian CLI** (Obsidian 1.12, Feb 2026; native binary since 1.12.7). It knows about links:
   `move` updates wikilinks, and it supports search, backlinks, properties and tags. Caveats: the app must
   be running, exit codes are always 0 (so agents must parse the output text), and commands should run
   sequentially.

## 5. Cross-harness portability

- `AGENTS.md` is the shared manual read by Codex, Cursor, OpenCode and many other tools.
- `CLAUDE.md` can import it with `@AGENTS.md`. `GEMINI.md` can do the same.
- Skills in the Agent Skills format (`SKILL.md` folders) work in Claude Code and Cowork from
  `.claude/skills/`, and in Codex and others from `.agents/skills/`.
- Example: the open-source "obsidian-second-brain" project compiles one source tree into builds for eight
  harnesses.

## 6. Pitfalls

- **Over-capturing.** Logging every step buries the decisions that matter.
- **Unbounded context.** Loading whole folders. Go index-first and load summaries.
- **Semantic drift.** Old facts mislead. Use `last_reviewed` and `confidence` fields, and lint for stale pages.
- **Mixed authorship.** Mark agent-written pages (`agent_written: true`).
- **No undo.** Put the vault in git and make one commit per operation.
- **Prompt injection.** Clipped web content can contain instructions. Treat vault content as data.
- **Data handling.** A synced vault is a copy of your data. Follow the one rule: only data approved for
  that storage and those tools goes in.
- **Atrophy.** Critics warn that handing all summarizing to the model weakens your own understanding.
  Keep a human in the loop.

## Sources

- VentureBeat, "Karpathy shares LLM knowledge base architecture that bypasses RAG" — https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
- Starmorph, "Karpathy LLM Wiki knowledge base guide" — https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide
- MindStudio, "AI second brain: Claude Code + Obsidian architecture" — https://www.mindstudio.ai/blog/ai-second-brain-claude-code-obsidian-architecture
- eugeniughelbur/obsidian-second-brain (GitHub) — https://github.com/eugeniughelbur/obsidian-second-brain
- dsebastien, "The complete guide to the Obsidian CLI" — https://www.dsebastien.net/the-complete-guide-to-the-obsidian-cli-everything-you-can-do-from-the-terminal/
- Smart Connections MCP (GitHub) — https://github.com/msdanyg/smart-connections-mcp
- XDA, "My Obsidian vault is now the shared memory for Claude Code, Codex, and my local LLM" — https://www.xda-developers.com/my-obsidian-vault-is-shared-memory-for-claude-code-codex-and-local-llm/
