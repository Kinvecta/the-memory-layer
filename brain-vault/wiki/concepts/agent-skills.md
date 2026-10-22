---
type: concept
summary: Agent skills are SKILL.md folders of instructions, templates and scripts that a harness loads only when a task matches; covers anatomy, progressive disclosure costs, portability across harnesses, supply-chain risk and why skills plus tools make a harness powerful.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[prompt-and-skill-library]]", "[[ai-harness]]", "[[ai-agents]]", "[[tool-calling]]", "[[model-context-protocol]]", "[[context-window]]", "[[agnostic-ai-platform]]", "[[containerization]]"]
aliases: [skill, skills, SKILL.md, Agent Skills]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Agent Skills

**TL;DR:** A skill is a folder of written instructions plus optional scripts and reference files that a harness loads only when a task calls for it - "an onboarding guide that the AI loads only when it's needed." The open SKILL.md format (agentskills.io, December 2025) runs in most major harnesses, so know-how written once is portable. A skill is software: read, scan, pin and review it before anyone installs it.

## What it is
A skill tells the AI *how* to do a job well; it does not change the model, and it is not a tool ([[source-ai-training-guide]] §2.1). The format started at Anthropic, was released as an open standard in December 2025, and most major harnesses now read it ([[source-ai-training-guide]] §3.3).

Anatomy:
```
report-writer/
  SKILL.md       required: name, description, then the instructions
  reference.md   optional: deeper detail, read only when needed
  templates/     optional: formats to fill in
  scripts/       optional: code the agent can run
```
The description line matters most: it is what the AI reads to decide whether the skill fits ([[source-ai-training-guide]] §3.3). "A vague description is a skill that never fires" ([[source-s8-agents-skills-and-running-the-program]] [1:16]).

## Why it matters
- **Cheap at scale (progressive disclosure).** Across Anthropic's 17 public skills, one analysis measured about 80 tokens of always-on metadata per skill versus a median ~2,000 tokens for a full SKILL.md ([[source-ai-training-guide]] §3.3). Session 8's worked example totals about 2,500 tokens, around 1% of the [[context-window]]: "Dozens installed. One loaded."
- **Portable know-how.** Grok Build picks up Claude skills; Hugging Face ships one repo for Claude Code, Codex and Gemini CLI. Limits are practical: scripts need the same runtime, and one project porting 55 skills to Grok Build had to rewrite file paths and tool names ([[source-ai-training-guide]] §3.3). Skills are foundation 4 of the [[agnostic-ai-platform]].
- **Method plus facts.** Tools give facts and actions; skills give "steps in order, templates, reference files, what to verify, what never to do." Together: consistency, grounding, self-checking, safety by construction, token economy ([[source-ai-training-guide]] §3.4).

## How it works
Loading happens in levels: (1) names and descriptions of all installed skills; (2) the full SKILL.md when a request matches; (3) only the specific file needed, such as a template ([[source-s8-agents-skills-and-running-the-program]] [1:16]). Platform specifics as of October 2026: Claude loads by description match; ChatGPT/Codex activate via @, /skills or $, or implicitly, and are off by default on Enterprise/Edu until an admin enables them; Gemini CLI uses an activate_skill tool; Gemini app skills replaced Gems (launched September 30, 2026); Hermes writes and edits its own skills ([[source-ai-training-guide]] Appendix).

## In practice
> [!warning] A skill is software
> A Snyk audit found 36.82% of analyzed ClawHub skills had at least one security flaw, and Cisco researchers found one that quietly exfiltrated data ([[source-ai-training-guide]] §3.3).

Treat every skill like code ([[source-s8-agents-skills-and-running-the-program]] [1:45]):
1. Read every file before it is installed.
2. Scan it and pin the version ([[image-scanning-and-sbom]]).
3. Install only from the internal registry.
4. Run any skill with scripts inside a container ([[containerization]]).
5. A person approves any skill an agent rewrites.
6. Decide who may install, write and share skills before turning them on.

Worked example: a contract-review skill holds the checklist, template and the rule that dollar figures come only from the contracts system; tools are a contracts MCP server, a PDF reader and a code runner; the harness logs and gates write-back ([[source-ai-training-guide]] §3.4). Test that each skill triggers when it should and not otherwise; the Session 8 exercise has a partner play the model, reading only the description against three should-trigger and two should-not requests.

## See also
[[prompt-and-skill-library]] · [[ai-agents]] · [[model-context-protocol]] · [[ai-harness]]
