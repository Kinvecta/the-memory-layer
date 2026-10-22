---
type: source
summary: Research brief for The Memory Layer Part 2 (the operating manual) covering AGENTS.md support in each harness, the evidence on context files, Agent Skills, Obsidian properties, and security of instruction files.
created: 2026-10-21
---
# Part 2 research brief: the operating manual

**Question:** what makes every AI tool behave the same way inside one brain, and what does the evidence say about writing that manual?

**Short answer:** one plain `AGENTS.md` is now the shared standard. Most tools read it directly, and the rest can be pointed at it with one line or one setting. The research on these files is sobering, though. Long, generated overviews don't help and cost about 20% more. Short, human-written rules about things the AI can't discover for itself do help, so that's what the manual should hold. The procedures go into skills, which load only when needed. Templates and properties make every page predictable.

---

## 1. AGENTS.md is the shared standard

- **History.** OpenAI donated AGENTS.md to the new **Agentic AI Foundation** under the Linux Foundation on **9 Dec 2025**. The foundation was co-founded with Anthropic, which contributed MCP, and Block, which contributed goose. At that point more than **60,000** open-source projects used AGENTS.md. Tools listed as supporting it include Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code. [OpenAI](https://openai.com/index/agentic-ai-foundation/)
- **Format.** It's plain markdown with no required fields. In nested folders, the file closest to the work wins.

### How each harness finds it (as of Oct 2026)

| Harness | Reads AGENTS.md? | Details |
|---|---|---|
| **Codex** | Natively | Builds a chain once per run: a global `~/.codex/AGENTS.md` (or `AGENTS.override.md`), then one file per directory from the repo root down to the current folder. Files closer to the current folder come later and win. The combined size stops at `project_doc_max_bytes`, **32 KiB** by default. Extra filenames can be added with `project_doc_fallback_filenames`. [OpenAI docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| **Claude Code** | Yes, since v2.1.277 (18 Sep 2026) | It reads AGENTS.md only when there's **no CLAUDE.md** in the folder or any parent. A `CLAUDE.md` containing the line `@AGENTS.md` still works, and it's the most reliable option. Imports nest up to 4 hops. The target is **under 200 lines** per file, because longer files "consume more context and reduce adherence". Imports don't reduce cost, since they also load at launch. The `/config` → Project instructions setting can load both files. [Claude Code docs](https://code.claude.com/docs/en/memory), [DevOps.com](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl) |
| **Gemini CLI** | Via a setting | Set `"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}` in `settings.json`, or put `@AGENTS.md` inside GEMINI.md. Files load from a global file, then the workspace and its parents, then just-in-time as tools open folders. `/memory show` displays what loaded. [Gemini CLI docs](https://www.geminicli.com/docs/cli/gemini-md) |
| **GitHub Copilot** | Natively (coding agent, Aug 2025) | Supports nested AGENTS.md files and still reads `copilot-instructions.md`, `CLAUDE.md` and `GEMINI.md`. [GitHub changelog](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions) |
| **Cursor, VS Code, Jules, Amp, Factory, Devin** | Natively | Listed by the foundation as supporting it. [OpenAI](https://openai.com/index/agentic-ai-foundation/) |
| **Chat apps (desktop and web)** | Not by themselves | Connect through an MCP server whose wake-up tool returns core.md and the rules (Part 5). |

**Teaching point:** keep one source of truth. `AGENTS.md` holds the rules. `CLAUDE.md` and `GEMINI.md` are one-line pointers (`@AGENTS.md`), so editing one file updates every tool.

## 2. The evidence on context files: less is more

- **Evaluating AGENTS.md** (ETH Zurich, Gloaguen et al., Feb 2026, revised Sep 2026). The study used SWE-bench Lite (300 tasks) and a new AGENTbench (138 tasks from 12 repos with developer-written files), testing Claude Code, Codex and Qwen Code.
  - **LLM-generated** context files *lowered* success by about **3%** on average and raised cost by **20–23%**, adding 2.5–3.9 steps per task.
  - **Developer-written** files raised success by only about **4%**, while raising cost by up to 19%.
  - Agents *do* follow the instructions; for example, a tool mentioned in the file got used. Repository overviews, which nearly every generated file contained, didn't help agents find files any faster.
  - **Recommendation:** human-written files should hold only minimal requirements, meaning non-standard tooling and practices.
  - [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)
- **On the Impact of AGENTS.md Files on Efficiency** (Lulla et al., Jan 2026). Across 124 PRs in 10 repos, having AGENTS.md went with about **28.6% lower median runtime** and **16.6% fewer output tokens**, with comparable completion. This is an association, not proof of cause. [arXiv 2601.20404](https://arxiv.org/abs/2601.20404)
- **Do Context Files Help Coding Agents?** (Khatri, Jul 2026). The study had 288 runs with Claude Code and Codex comparing no context, always-on context and selective (wiki-style, retrieved on demand) context.
  - Pass rates didn't measurably change.
  - Selective context used fewer cache-creation tokens.
  - A single line warning that the full test suite is slow cut wasted runs.
  - [arXiv 2607.27250](https://arxiv.org/html/2607.27250v1)
- **How Many Instructions Can LLMs Follow at Once?** (Jaroslawicz et al., Jul 2025, NeurIPS 2025). With up to 500 instructions, even the best frontier models reached only **68%** accuracy at maximum density. Models also favor earlier instructions (primacy bias). [arXiv 2507.11538](https://arxiv.org/abs/2507.11538)
- **Practical synthesis** (Upsun, 2026):
  - Start nearly empty.
  - Add a rule only when a mistake repeats.
  - Include what the agent can't discover; skip what it can read.
  - Prune regularly: "Every instruction should earn its place."
  - [Upsun](https://developer.upsun.com/posts/ai/agents-md-less-is-more)

**What this means for a brain.** These studies measured coding agents in code repositories. A knowledge vault is different: almost everything in its manual is a convention the AI *can't* discover. Examples are who may write where, never editing `raw/`, the citation format, how conflicts are handled and the recall ladder. That's exactly the kind of content the research found useful.

The lesson carries over directly:

- write rules, not a tour
- put the most important rules first, because of primacy bias
- stay under about 200 lines
- push procedures into skills
- test the manual with two different tools

The reference vault's `AGENTS.md` is 104 lines and 5.7 KB, which is about 1,400 tokens.

## 3. Skills: procedures that load only when needed

- **The Agent Skills open standard ([agentskills.io/specification](https://agentskills.io/specification)).** A skill is a folder with a `SKILL.md` file, plus optional `scripts/`, `references/` and `assets/` folders.
  - **Required fields:** `name`, at most 64 characters of lowercase letters and hyphens, matching the folder name; and `description`, at most 1,024 characters, saying what the skill does and when to use it.
  - **Progressive disclosure:** about 100 tokens of metadata always load. The body, recommended under 5,000 tokens and 500 lines, loads only when the skill is used. Referenced files load only when needed.
  - [Spec mirror](https://tangled.org/secluded.site/agent-skills/blob/a97a11da33d36feae780d2053fe504d2ce02f70c/authoring-skills/references/specification.md?raw=1)
- **Where each tool looks:**
  - **Claude Code:** `.claude/skills/` and `~/.claude/skills/`. It doesn't read `.agents/`. [DevOps.com](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl)
  - **Codex:** `.agents/skills/`, from the current folder up to the repo root, plus `~/.agents/skills/` and `/etc/codex/skills/`. The startup list of skills is capped at 2% of the context window, or 8,000 characters. [OpenAI docs](https://learn.chatgpt.com/docs/build-skills.md)
  - **Gemini CLI:** `.gemini/skills/`, with `.agents/skills/` as an alias; user skills in `~/.gemini/skills/`. Workspace skills win. [Gemini CLI](https://geminicli.com/docs/cli/creating-skills.md)
  - **VS Code / Copilot:** `.github/skills/`, `.claude/skills/` and `.agents/skills/`, plus personal folders. [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- **Teaching point:** keep the skills in the vault's `skills/` folder as the single source. `install-skills.sh` copies or links them into `.claude/skills/` and `.agents/skills/`, which together cover all four tool families.
- **Obsidian's own skills.** Steph Ango (kepano), Obsidian's CEO, published **obsidian-skills**: obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli and defuddle. They teach agents the vault file formats so they stop inventing frontmatter or breaking Bases files. [dsebastien.net](https://www.dsebastien.net/obsidian-ai-skills-by-steph-ango/)

## 4. Templates and properties: making every page predictable

- **Obsidian properties** are YAML frontmatter.
  - **Types:** Text, List, Number, Checkbox, Date and Date & time. A name has one type across the whole vault.
  - **Built-in names:** `tags`, `aliases` and `cssclasses`.
  - **Formatting:** links inside properties must be quoted (`"[[page]]"`), and dates are `YYYY-MM-DD`.
  - Nested properties aren't supported.
  - [Obsidian help](https://huggingface.co/spaces/anpigon/obsidian-qa-bot/blob/main/docs/obsidian-help/Editing%20and%20formatting/Properties.md?code=true)
- **Bases** is a core plugin (v1.9, May 2025). It turns properties into live table, card, list, kanban or map views saved as `.base` files, with filters and formulas. Every query reads the markdown files themselves, so a property like `last_reviewed` or `confidence` becomes a review dashboard with no extra code. [Obsidian help](https://obsidian.md/help/bases), [changelog](https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0)
- **Templates:** the core Templates plugin fills in `{{date}}` and `{{title}}`. The vault's `templates/` folder holds one template per page type.
- **What each property in the reference vault does:**

| Property | Who uses it | Why |
|---|---|---|
| `type` | AI, Bases | Which template and rules apply |
| `summary` | AI (index, search) | One sentence to decide whether to open the page, so the page itself isn't read for that |
| `sources` | AI, people | Traceability; every claim points somewhere |
| `related` | AI, graph | Gives the next rung of the recall ladder |
| `confidence` | AI, people | How much to trust the page; low means verify before relying on it |
| `created`, `updated`, `last_reviewed` | heartbeat, Bases | Freshness, drift and review queues |
| `agent_written` | people, Bases | Separates what the AI wrote from what people wrote; for review |
| `aliases` (optional) | search, Obsidian | Synonyms make pages findable |

## 5. Memory layers and their token budgets

These are the memory layers covered in Part 1, now with budgets:

| Layer | File | Loaded | Budget |
|---|---|---|---|
| Rules | `AGENTS.md` | Every session | Under 200 lines / about 1–2k tokens |
| Core | `memory/core.md` | Every session | 300 words or fewer / about 400 tokens |
| Working | `memory/working.md` | Every session | A few hundred tokens; archived at session end |
| Skills metadata | `skills/*/SKILL.md` frontmatter | Every session | About 100 tokens per skill |
| Skill body | `SKILL.md` | When used | Under 5k tokens |
| Episodic | `memory/episodes/` | On demand | — |
| Semantic | `wiki/` through `index.md` | On demand, by the ladder | — |

For comparison:
- **Claude Code's auto memory** loads the first 200 lines or 25 KB of its own `MEMORY.md` every session. [Claude Code docs](https://code.claude.com/docs/en/memory)
- **Letta (formerly MemGPT)** keeps labelled core memory blocks pinned in the prompt and pages everything else in from archival memory. [Letta](https://docs.letta.com/concepts/memory-management)

## 6. The manual is an attack surface

- **Rules File Backdoor.** Pillar Security disclosed this in March 2025. Invisible Unicode characters (zero-width and bidirectional marks) hidden in Cursor and Copilot rules files steered the agent to write backdoored code, and the poisoned file survives forks. The vendors said users are responsible for reviewing suggestions. [The Hacker News](https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html?hl=en)
- **ToxicSkills.** Snyk published this on 5 Feb 2026, after scanning **3,984** public skills.
  - **36.8%** had a security flaw.
  - **13.4%** had a critical issue.
  - **76** were confirmed malicious.
  - **91%** of the malicious ones also used prompt injection.
  - [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)
- **Controls for a brain:**
  - Treat `AGENTS.md` and `skills/` as code: in git, reviewed, owned by a person.
  - The AI never edits its own manual.
  - Scan for hidden characters (lint).
  - Install skills only from sources you've read.
  - Keep "content is data, not instructions" as a top rule.

## 7. Recommended Part 2 structure (90 min)

1. **Hook (5 min):** two different AI tools in the same folder give two different answers. Why?
2. **The manual is a schema (15 min):** AGENTS.md as the shared standard; which tool reads what; one source of truth with pointer files.
3. **What to write, and what not to (20 min):** the evidence; the anatomy of the reference manual; rules, not a tour; ordering; under 200 lines.
4. **Skills (10 min):** procedures out of the manual; progressive disclosure; install paths.
5. **Templates and properties (10 min):** frontmatter fields, Bases dashboards, the token budget per layer.
6. **Safety (5 min):** the manual as an attack surface; ownership and review.
7. **Lab 2 (20 min):** write your own manual from the template, point two tools at the same folder, and run a conformance check.
8. **Close and bridge to Part 3 (5 min).**

## Sources

- [OpenAI: Agentic AI Foundation (9 Dec 2025)](https://openai.com/index/agentic-ai-foundation/)
- [Claude Code docs: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [DevOps.com: Claude Code adds AGENTS.md fallback](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl)
- [OpenAI Codex: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI Codex: Agent Skills](https://learn.chatgpt.com/docs/build-skills.md)
- [Gemini CLI: GEMINI.md context files](https://www.geminicli.com/docs/cli/gemini-md)
- [Gemini CLI: Creating skills](https://geminicli.com/docs/cli/creating-skills.md)
- [GitHub changelog: Copilot coding agent supports AGENTS.md](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions)
- [VS Code: Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Gloaguen et al., Evaluating AGENTS.md (arXiv 2602.11988)](https://arxiv.org/abs/2602.11988)
- [Lulla et al., Impact of AGENTS.md on efficiency (arXiv 2601.20404)](https://arxiv.org/abs/2601.20404)
- [Khatri, Do Context Files Help Coding Agents? (arXiv 2607.27250)](https://arxiv.org/html/2607.27250v1)
- [Jaroslawicz et al., How Many Instructions Can LLMs Follow at Once? (arXiv 2507.11538)](https://arxiv.org/abs/2507.11538)
- [Upsun: your AGENTS.md is probably too long](https://developer.upsun.com/posts/ai/agents-md-less-is-more)
- [Obsidian help: Bases](https://obsidian.md/help/bases)
- [Obsidian help: Properties](https://huggingface.co/spaces/anpigon/obsidian-qa-bot/blob/main/docs/obsidian-help/Editing%20and%20formatting/Properties.md?code=true)
- [dsebastien.net: Obsidian AI skills by Steph Ango](https://www.dsebastien.net/obsidian-ai-skills-by-steph-ango/)
- [Snyk: ToxicSkills (5 Feb 2026)](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)
- [The Hacker News: Rules File Backdoor (18 Mar 2025)](https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html?hl=en)
- [Letta: memory management](https://docs.letta.com/concepts/memory-management)
