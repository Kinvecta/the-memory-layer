---
type: concept
summary: A workflow is a fixed, designer-defined sequence of steps that may call a model; covers how to pick one, the six-step anatomy, validation, safe runs and release habits (Stage 3).
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s6-building-workflows]]"]
related: ["[[chatbot-workflow-agent]]", "[[apis-and-endpoints]]", "[[containerization]]", "[[prompt-and-skill-library]]", "[[model-context-protocol]]", "[[five-stage-training-progression]]", "[[measuring-training-results]]", "[[ai-evals]]"]
aliases: [workflow, API-driven workflow, fixed pipeline]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Workflows

**TL;DR:** A workflow is a predefined sequence of steps, possibly with AI in some, where a designer fixes the path in advance and the script, not the model, decides each step. It is Stage 3 of the training and the stopping point for teams that only have chat and API access, yet still delivers working, containerized automation. Its main risk is breaking quietly, so every workflow validates its output and routes it to a person before delivery.

## What it is
In a chatbot the person picks every step; in a workflow "a designer, in advance; fixed path"; in an agent the AI chooses at run time ([[source-ai-training-guide]] §2.1; [[chatbot-workflow-agent]]). The glossary warns that a workflow is often "called an agent when the path is fixed and the AI makes no decisions." Example: every status report gets summarized and routed to the same inbox.

## Why it matters
Most automation does not need agents. With chat plus an API, teams can build scripted or low-code workflows - batch summaries, extraction into tables, sensitivity labeling, drafting from a template - and complete Stages 1-3 ([[source-ai-training-guide]] §2.1). Because the path is predictable, it is easier to authorize. Session 6 frames the alternative: the same prompt pasted every Monday drifts - edited one week, a step skipped the next, nobody checking the third ([[source-s6-building-workflows]] [0:00]).

## How it works
**Pick the first one** - score six signs: repeats weekly, same shape each time, known-good output, a lead already reviews it, data at an approved level, measurable time. 4/6 is enough to start ([[source-s6-building-workflows]] [2:31]).

**Anatomy: six fixed steps, one check, one person** ([[source-s6-building-workflows]] [2:56]):
1. Trigger (usually a schedule)
2. Pull inputs - through an [[model-context-protocol]] server as a fixed step
3. Saved prompt (versioned) to a pinned model through the API ([[apis-and-endpoints]])
4. Validate the output
5. A named person reviews
6. Deliver - every step writes to the audit log

Using an MCP server here keeps it a workflow, "because the script, not the model, decides when each call happens" ([[source-ai-training-guide]] §5.2).

**Validate** - format, required fields, links, recipients. One failure flags the run and routes it to a person; nothing ships ([[source-s6-building-workflows]] [3:36]).

**Run safely** - inside the Session 5 container, key injected from the secrets store, only the model endpoint and MCP server allow-listed, every run logged, a cost cap to stop runaway loops ([[source-s6-building-workflows]] [4:06]; [[containerization]], [[secrets-management]]).

**Release** - a new prompt version runs its test set (five known-good cases plus a tricky "ignore your rules" input) before it enters the library. "A new version is a new release, never an edit in place" ([[source-s6-building-workflows]] [4:32]; [[ai-evals]], [[prompt-injection]]).

## In practice
- Good candidates: status reports, meeting notes, policy summaries, email triage ([[source-ai-training-guide]] §5.2).
- Prompts live in the [[prompt-and-skill-library]], never typed directly into a flow. Low-code tools such as Microsoft Power Automate are fine if the tool itself is authorized ([[source-ai-training-guide]] §5.1).
- Stage 3 is complete when the workflow runs repeatably, flags bad output, and logs every run ([[five-stage-training-progression]]).
- Track time saved per run and workflows in production ([[measuring-training-results]]).
- Stress-test with the Session 6 "break it" scenarios: changed template, missing report, unknown link, model update, planted instruction, looping run.

> [!tip] Rule to remember
> "Fix the path. Check every output. A person approves before it ships." ([[source-s6-building-workflows]] [5:15])

## See also
[[chatbot-workflow-agent]] · [[tool-calling]] · [[ai-agents]] · [[apis-and-endpoints]]
