---
type: entity
summary: The train-the-trainer video series built from the AI Training Guide - Sessions 1-8 plus Deep Dive A (build an MCP server) and Deep Dive B (DevSecOps containers and CI/CD), each produced as a slide deck and narrated video with a transcript.
sources: ["[[raw/transcripts/s1-what-an-llm-is]]", "[[raw/transcripts/s2-ai-resilience]]", "[[raw/transcripts/s3-safe-prompting-and-verification]]", "[[raw/transcripts/s4-tokens-context-and-data]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]", "[[raw/transcripts/s6-building-workflows]]", "[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]", "[[raw/transcripts/dda-build-an-mcp-server]]", "[[raw/transcripts/ddb-devsecops-containers-cicd]]"]
related: ["[[ai-training-guide]]", "[[five-stage-training-progression]]", "[[the-memory-layer]]", "[[2026-10-21-ai-brain-series-standalone]]", "[[measuring-training-results]]"]
aliases: [train-the-trainer, TTT series, training video series]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Train-the-Trainer Series

**TL;DR:** A ten-part video series "on using generative AI well, and safely, at work," built from the [[ai-training-guide]]: eight core sessions that climb the [[five-stage-training-progression]], plus two technical deep dives. Each part is produced as a slide deck and a narrated video with a timestamped transcript, and every session follows the same shape: why it matters, animated figures, one rule, a paper exercise, six check questions, and a bridge to the next.

## Who / what
| # | Title | Stage / focus | Length* | Source page |
|---|---|---|---|---|
| 1 | What an LLM Is | Model vs harness; chatbot, workflow, agent | ~10.5 min | [[source-s1-what-an-llm-is]] |
| 2 | AI Resilience | Seven foundations that survive a switch | ~8 min | [[source-s2-ai-resilience]] |
| 3 | Safe Prompting and Verification | Stage 1 habits | ~6.5 min | [[source-s3-safe-prompting-and-verification]] |
| 4 | Tokens, Context and How AI Finds Your Data | Tokens, finders | ~7 min | [[source-s4-tokens-context-and-data]] |
| 5 | APIs, Endpoints and Containers | Stage 2 | ~6 min | [[source-s5-apis-endpoints-and-containers]] |
| 6 | Building Workflows | Stage 3 | ~7 min | [[source-s6-building-workflows]] |
| 7 | Tools, MCP and Prompt Injection | Stage 4 | ~7.5 min | [[source-s7-tools-mcp-and-prompt-injection]] |
| 8 | Agents, Skills and Running the Program | Stage 5 + rollout | ~7 min | [[source-s8-agents-skills-and-running-the-program]] |
| A | Build an MCP Server from Scratch | Hands-on MCP build, security, release | ~20 min | [[source-dda-build-an-mcp-server]] |
| B | DevSecOps Containers, Scanning and CI-CD | Containers, scanning, signing, pipeline | ~20 min | [[source-ddb-devsecops-containers-cicd]] |

*Approximate, from the final transcript timestamp.

## Role in this brain
The transcripts are the second main source family after the guide. Session pages carry timestamped citations; concept pages cite both the guide and the sessions. The separate [[the-memory-layer]] is a standalone series, not part of this one ([[2026-10-21-ai-brain-series-standalone]]).

## Key facts
- **Deliverables per part:** a slide deck, a narrated video, and a transcript (the raw files in `raw/transcripts/`).
- **Arc:** S1-S2 are concepts and strategy; S3-S8 track Stages 1-5 (S4 adds tokens and data access between Stages 1 and 2). Each session opens by picking up the previous session's closing question ([[source-s5-apis-endpoints-and-containers]] [0:00]).
- **Shared session pattern:** cover figure; four learning goals; "why" with three real complaints; animated figures; "one idea to hold on to"; a pause-the-video exercise (Part A / Part B, paper only); six self-check questions; bridge; some end with a facilitator sandbox slide.
- **Session rules:** S5 "your code becomes the harness, so your team owns the controls"; S6 "fix the path, check every output, a person approves before it ships"; S8 "write it once, gate what leaves, measure what changes."
- **Exercises chain:** the prompt saved in Session 3 is packaged as a skill in Session 8 ([[source-s8-agents-skills-and-running-the-program]] [0:25]).
- **Deep dives:** A builds a "ticket-desk" MCP server current to the July 28, 2026 spec revision, with a thirty-minute lab; B puts it "in a box": secrets out, scan, sign, ship the same digest, fence it in. Close line: "Build it. Box it. Ship it." See [[building-an-mcp-server]], [[devsecops-pipeline]].
- **Series close** ([[source-s8-agents-skills-and-running-the-program]] [6:31]): one pilot, measured - pick a pilot workflow, take baselines, stand up the shared library, run Stage 1 for everyone, calendar the review date ([[measuring-training-results]]).
- **Relation to the guide's course map:** the guide plans six facilitator sessions (Stage 1 split in two, then one per stage); the series expands to eight plus two deep dives.

## See also
[[ai-training-guide]] · [[five-stage-training-progression]] · [[the-memory-layer]]
