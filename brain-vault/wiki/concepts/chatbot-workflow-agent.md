---
type: concept
summary: How to tell a chatbot, a workflow and an agent apart using one test (who picks each step), with examples, risks, and when to choose a workflow over an agent.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s1-what-an-llm-is]]"]
related: ["[[large-language-model]]", "[[ai-harness]]", "[[workflows]]", "[[ai-agents]]", "[[five-stage-training-progression]]", "[[tool-calling]]"]
aliases: [chatbot vs workflow vs agent, agentic]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Chatbot vs. workflow vs. agent

**TL;DR:** Chatbots, workflows and agents are three different things, and the test is one question: who picks each step? In a chatbot the person does, one message at a time; in a workflow ([[workflows]]) a designer fixes the path in advance; in an agent ([[ai-agents]]) the AI picks its own steps at run time. If you already know the steps, build a workflow.

## What it is
| | Chatbot / assistant | Workflow | Agent |
|---|---|---|---|
| Who decides the steps | The person, one message at a time | A designer, in advance; fixed path | The AI, at run time, toward a goal |
| What it does | Answers or drafts in a conversation | Runs the same sequence every time (AI may be one step) | Plans, uses tools, checks results, repeats until done |
| Example | Asking for a summary of a memo | Every status report summarized and routed to the same inbox | "Find every contract expiring this quarter and draft renewal notices" |
| Main risk | Wrong answer accepted as fact | Breaks quietly when inputs change | Mistakes compound across steps and actions |

Source: [[source-ai-training-guide]] §2.1; [[source-s1-what-an-llm-is]] [7:47].

## Why it matters
Telling AI, workflows and agents apart is focus area #3 in the guide's ranked list; the common gap is "calling everything an 'agent'; building an agent where a fixed workflow would do." Picking the right level of autonomy keeps risk in proportion ([[source-ai-training-guide]] §1.4). "Agent" and "workflow" are two of the three most misused terms, with "AI safety" ([[source-s1-what-an-llm-is]] [0:51]). The glossary notes "agent" "now gets slapped on almost any product," and "agentic" is a spectrum, not yes/no; most agentic tools today are lightly autonomous ([[source-ai-training-guide]] Glossary).

## How it works
- **Chatbot:** you ask, it answers, you decide what happens next.
- **Workflow:** the same fixed path every run; the script or automation platform, not the model, decides each step, so the path is predictable and easier to authorize ([[source-ai-training-guide]] §2.1).
- **Agent:** loops through plan, act and check until the goal is met, then a person reviews.

> [!tip] Rule of thumb
> If you already know the steps, build a workflow. It is more predictable, easier to approve, and easier to test ([[source-s1-what-an-llm-is]] [7:47]).

## What your environment allows
| Environment offers | What teams can do | Stages |
|---|---|---|
| Chat only | Manual prompting, shared templates, copy-paste workflows | 1 |
| Chat + API | Scripted or low-code workflows calling the model; MCP servers as fixed steps | 1-3 |
| Chat + API + tool calling | Workflows that look things up or take approved actions | 1-4 |
| Full harness with tools, skills or agents | AI picks its own steps, with approval gates | 1-5 |

Teams limited to chat and API can stop at Stage 3 and still get working automation ([[source-ai-training-guide]] §2.1; [[five-stage-training-progression]]).

## In practice
Session 1 exercise: sort ten real tasks into chatbot, workflow or agent. Answer key in the session: chatbot 1, 4, 7, 10; workflow 2, 5, 8; agent 3, 6, 9. "If you said 'it depends on who picks the steps,' you've got the idea" ([[source-s1-what-an-llm-is]] [9:15]).

## See also
[[workflows]] · [[ai-agents]] · [[tool-calling]] · [[ai-harness]] · [[five-stage-training-progression]]
