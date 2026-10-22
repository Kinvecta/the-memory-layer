---
type: source
summary: Summary of the Session 8 (final) transcript on skills and progressive disclosure, treating skills as code, combining skill + tools + model, agent guardrails, the shared library, and running the program by stage, role and measure.
sources: ["[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[agent-skills]]", "[[ai-agents]]", "[[prompt-and-skill-library]]", "[[five-stage-training-progression]]", "[[measuring-training-results]]", "[[train-the-trainer-series]]", "[[source-s7-tools-mcp-and-prompt-injection]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 8 - Agents, Skills and Running the Program

**TL;DR:** The final session teaches Stage 5 and then how to run the training program itself. A skill is an onboarding guide the AI loads only when needed; combined with tools and a model inside a harness, it produces the same reviewed, cited, checked result for anyone. Agents run in a container with an approval gate on anything that leaves, and the program is judged by measured change in work, not course completions.

**Source file:** [[raw/transcripts/s8-agents-skills-and-running-the-program]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (series edition)

## Key points
1. **Opening picture** [0:00]: inside the harness, a skill holds the method, the model brings judgment, tools bring facts and actions, and a person approves what leaves.
2. **Three ways programs stall** [0:46]: know-how walks out the door (best prompts in one person's chat history); unchecked skills get installed (in one audit, roughly a third of public-registry skills had a security flaw); courses end at Stage 1 and nobody checks whether work changed.
3. **How a skill loads** [1:16]: six skills installed, only names and descriptions load; a matching request loads the full instructions, then only the needed file (the template). Total about 2,500 tokens, around 1% of the window. "Dozens installed. One loaded." A vague description is a skill that never fires. See [[agent-skills]], [[context-window]].
4. **Treat every skill like code** [1:45]: read every file before installing; scan and pin the version; install only from the internal registry; run skills with scripts in a container; a person approves any agent-rewritten skill; decide who may install skills before turning them on.
5. **Skill + tools + model** [2:11]: contract review example - skill brings checklist, template and the rule "dollar figures come only from the system"; model calls the contracts MCP server, a PDF reader and a code runner, checks totals against the record; a person approves before write-back.
6. **Agent with guardrails** [2:50]: agent runs in a container, plans, reads the tracker, checks rows, loops; every step logged; an email send holds at the approval gate until a person reviews the steps. "Review the steps, not just the answer." See [[ai-agents]].
7. **Library** [3:24]: saved prompt becomes a skill - header becomes name and description, body becomes steps, template and tests attach (two cases plus one tricky one), second-person review, version, one home; chat, scripts and agents all pull from it ([[prompt-and-skill-library]]).
8. **Stages and their risks** [3:49]: Stage 1 wrong tool for the data; Stage 2 leaked keys; Stage 3 bad output passed on; Stage 4 unapproved actions; Stage 5 untested skills. Everyone does Stage 1 (leaders plus a demo), analysts stop at Stage 3, technical staff go to Stage 5 ([[five-stage-training-progression]]).
9. **Measure** [4:32]: example numbers only - time per report 6h to 2h; corrections in review 9 to 3; library reuse 0 to 4 teams; workflows in production 0 to 2. Take baselines before training, track security findings, and test every prompt, skill and workflow before release and after any change ([[measuring-training-results]]).
10. **Exercise** [5:21]: Part A, package the Session 3 prompt - name, description, three requests that should trigger it and two that should not; a partner plays the model reading only the description. Part B, plan a pilot rollout: workflow, roles to stages, three measures with baselines, a review date.
11. **Close** [6:31]: recaps all eight sessions; next steps - pick one pilot workflow, take baselines, stand up the shared library, run Stage 1 for everyone, calendar the review date.

## Worth quoting
> "Dozens installed. One loaded. And a vague description is a skill that never fires." [1:16]

> "Write it once, as a skill. Gate what leaves. Measure what changes." [5:08]

> "If any of your measures counts courses instead of work, swap it out." [5:21]

## Pages this source updated
- [[agent-skills]]
- [[ai-agents]]
- [[prompt-and-skill-library]]
- [[five-stage-training-progression]]
- [[measuring-training-results]]
- [[train-the-trainer-series]]
