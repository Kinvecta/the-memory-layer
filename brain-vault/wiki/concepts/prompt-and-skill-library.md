---
type: concept
summary: The one shared, version-controlled, reviewed and tested library of saved prompts and skills that every chat, script, workflow and harness pulls from, plus how a saved prompt becomes a skill.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s6-building-workflows]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[agent-skills]]", "[[workflows]]", "[[ai-evals]]", "[[safe-prompting]]", "[[agnostic-ai-platform]]", "[[measuring-training-results]]", "[[apis-and-endpoints]]"]
aliases: [prompt library, skill library, saved prompts]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Prompt and Skill Library

**TL;DR:** Every team keeps one shared, approved library of saved prompts and skills, and every chat, script, workflow and harness pulls from it. Entries are plain-text Markdown files with a header, clear names, versions, second-person review and two or three test cases. A prompt typed straight into a flow or script "gets lost, drifts, and cannot be audited."

## What it is
A version-controlled repository (for example Git) or an approved shared drive inside the authorized environment, holding saved prompts and [[agent-skills]] ([[source-ai-training-guide]] §3.5). It is what stops know-how from walking out the door when the person whose chat history holds the best prompts leaves ([[source-s8-agents-skills-and-running-the-program]] [0:46]).

## Why it matters
- Traceability: results can be traced to the exact prompt version that produced them.
- Portability: plain-text files are readable by people and any harness, and become skills with little change - part of foundation 4 (skills) and the eval store in foundation 7 of the [[agnostic-ai-platform]].
- Reuse is a headline success measure: "library reuse" counts saved prompts and skills and how often other teams run them ([[measuring-training-results]]).

## How it works
Six practices ([[source-ai-training-guide]] §3.5):

| Practice | What it means |
|---|---|
| One home | Git repo or approved shared drive in the authorized environment |
| Plain-text files | Markdown with a header: name, purpose, owner, inputs, approved data level |
| Clear names | team-task-version, e.g. j3-status report-summary-v2 |
| Versions | Changes go in as a new version with a one-line note; old versions stay |
| Review | A second person approves; skills with scripts also get a security review |
| Test cases | Two or three sample inputs with known-good outputs |

**Lifecycle** (Figure 18): write, review, test, publish, reuse. "Nothing reaches the library without a review and passing tests, and any change, including a new model version, sends it back through the same loop" ([[source-ai-training-guide]] §3.5). Session 6 shows it: prompt v3 runs five known-good cases plus a tricky "ignore your rules" report before release; "a new version is a new release, never an edit in place" ([[source-s6-building-workflows]] [4:32]; [[ai-evals]]).

**From saved prompt to skill.** When a reused prompt needs steps, a template or a script, it becomes a skill: the header becomes the name and description, the prompt body becomes SKILL.md's steps, supporting files go alongside, and tests (two cases plus one tricky one) attach ([[source-ai-training-guide]] §3.5; [[source-s8-agents-skills-and-running-the-program]] [3:24]).

## In practice
- Stage 1: when a prompt works, save it to the library so others reuse it instead of retyping ([[safe-prompting]]).
- Stage 2: load the saved prompt from the library and send it with the document rather than writing a new one in code ([[apis-and-endpoints]]).
- Stage 3: chain saved prompts into fixed [[workflows]]; even low-code flows (e.g. Power Automate) should reference saved, versioned files rather than prompts typed into each flow ([[source-ai-training-guide]] §5.1).
- Stage 5: package proven prompts as skills.
- The training sandbox ships a starter library: a Git repo with a few approved prompts, one skill and their test cases ([[source-ai-training-guide]] §5.2).
- Evals before release: every entry keeps sample inputs with known-good outputs plus at least one tricky case such as a planted instruction ([[prompt-injection]]).

> [!tip] Session 8 close
> One of the four next steps after the series is to "stand up the shared library" ([[source-s8-agents-skills-and-running-the-program]] [6:31]).

## See also
[[agent-skills]] · [[ai-evals]] · [[workflows]] · [[safe-prompting]]
