---
type: source
summary: Summary of the Session 6 transcript on building fixed AI workflows (Stage 3) - picking a first task, the six-step workflow anatomy, validation checks, safe containerized runs, test-then-version releases and four success measures.
sources: ["[[raw/transcripts/s6-building-workflows]]"]
related: ["[[workflows]]", "[[chatbot-workflow-agent]]", "[[five-stage-training-progression]]", "[[prompt-and-skill-library]]", "[[measuring-training-results]]", "[[train-the-trainer-series]]", "[[source-s5-apis-endpoints-and-containers]]", "[[source-s7-tools-mcp-and-prompt-injection]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 6 - Building Workflows

**TL;DR:** Session 6 teaches Stage 3: chaining saved prompts into a fixed pipeline that the script, not the model, controls. It gives a six-point checklist for choosing a first workflow, a six-step anatomy (trigger, inputs, prompt, validate, review, deliver), validation that flags rather than passes bad output, and a test-then-version release habit. Its message: teams with only chat plus API access already have enough for working automation.

**Source file:** [[raw/transcripts/s6-building-workflows]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (series edition)

## Key points
1. **Opening picture** [0:00]: the same task done by hand three Mondays running drifts (prompt edited, step skipped, nobody checks); one fixed lane runs the same steps every time, with a check.
2. **Three complaints** [0:55]: "we paste the same prompt every Monday"; "it broke, and nobody noticed" (workflows fail quietly when inputs change); "we can't get agents approved" (you don't need them yet).
3. **Who picks each step** [1:22]: chatbot = the person, each turn; workflow = a designer, in advance; agent = the AI, at run time, then a person reviews. See [[chatbot-workflow-agent]].
4. **Where to stop** [2:01]: chat plus an API is enough for scripted or low-code workflows, with MCP servers as fixed steps ([[model-context-protocol]]). That is "working, containerized automation."
5. **Pick a first workflow: six-point score** [2:31]: repeats weekly; same shape every time; known-good output exists; a lead already reviews it; data is at an approved level; time is measurable. A weekly status report scores 6/6. Four out of six is enough to start.
6. **Anatomy: six fixed steps, one check, one person** [2:56]: trigger (usually a schedule) -> inputs pulled through an MCP server -> saved prompt v2 to a pinned model via the API -> validate output -> named person reviews -> deliver. Every step writes to the audit log. "The script decides each step, not the model."
7. **Validation** [3:36]: four checks on the draft - format, required fields, links, recipients. One failure (an unexpected link) flags the run and routes it to a person; nothing is delivered.
8. **Run it safely** [4:06]: same container as Session 5; key injected from the secrets store; model endpoint and MCP server allow-listed, everything else blocked; every run logged; a cost limit stops runaway loops. See [[containerization]], [[secrets-management]].
9. **Release** [4:32]: prompt v3 runs the test set (five known-good cases plus a tricky "ignore your rules" report); only after passing does v3 go to the team library, logged. "A new version is a new release, never an edit in place." See [[prompt-and-skill-library]], [[ai-evals]].
10. **Measure** [5:00]: time saved per run, errors caught in review, workflows in production, prompt reuse by other teams; time the task by hand first for a baseline ([[measuring-training-results]]).
11. **Exercise** [5:30]: Part A, design a workflow card (trigger, inputs, steps as saved prompts, check, reviewer and delivery). Part B, break it with six scenarios: changed input template, missing report, unknown link, updated model version, "ignore your rules" text, a looping run. Anything that passes silently is a missing check.
12. **Bridge** [6:41]: Session 7 hands the step choice to the model via tools ([[tool-calling]]).

## Worth quoting
> "In a workflow, the path is fixed before it runs." [1:22]

> "Bad output is flagged, never passed on." [3:36]

> "Fix the path. Check every output. A person approves before it ships." [5:15]

## Pages this source updated
- [[workflows]]
- [[chatbot-workflow-agent]]
- [[prompt-and-skill-library]]
- [[measuring-training-results]]
- [[five-stage-training-progression]]
- [[train-the-trainer-series]]
