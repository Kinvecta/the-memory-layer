---
type: source
summary: Summary of the October 2026 AI Training Guide for Teams Adopting Generative AI, its five parts, glossary and appendix, and which roles should read which sections.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[ai-training-guide]]", "[[train-the-trainer-series]]", "[[five-stage-training-progression]]", "[[agnostic-ai-platform]]", "[[chatbot-workflow-agent]]", "[[ai-harness]]", "[[tokens]]", "[[how-ai-finds-your-data]]", "[[ai-governance-and-controls]]", "[[measuring-training-results]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: AI Training Guide (October 2026 edition)

**TL;DR:** A tool-agnostic, industry-agnostic guide that takes teams from "we have access to AI" to "we use it safely and well," through five stages that give the AI more control only as people prove they can contain and check it. Everything past basic chat runs in a container, and the organization owns seven foundations that keep it vendor-agnostic. It is the master source for the [[train-the-trainer-series]].

**Source file:** [[raw/guide/ai-training-guide-oct-2026]]  ·  **Kind:** guide  ·  **Date:** October 2026

## Structure: five parts plus reference

| Part | What it covers | Main wiki pages |
|---|---|---|
| 1 Orientation | At a glance, purpose and audience, where things are heading, where people need to focus (ranked gaps) | [[ai-training-guide]], [[ai-evals]] |
| 2 How the pieces work | Chatbot vs. workflow vs. agent, parts of an AI system, API endpoints, MCP, tokens, how AI finds data, the other models in a harness | [[chatbot-workflow-agent]], [[ai-harness]], [[apis-and-endpoints]], [[model-context-protocol]], [[tokens]], [[how-ai-finds-your-data]] |
| 3 The platform the organization owns | Seven foundations, containerization, skills deep dive, skills plus tools, prompt and skill library | [[agnostic-ai-platform]], [[containerization]], [[agent-skills]], [[prompt-and-skill-library]] |
| 4 Security, policy and governance | The one rule, prompt injection, operational controls, DevSecOps by component | [[ai-governance-and-controls]], [[prompt-injection]], [[devsecops-pipeline]] |
| 5 The training program | Five stages, practical tool use by stage, how far each role goes, course map, training environment, measuring results | [[five-stage-training-progression]], [[measuring-training-results]] |
| Glossary + Appendix | Key terms and common misuse; diagram color key; skills by platform; governance frameworks; recommended courses | [[large-language-model]], [[agent-skills]] |

## Who reads what (§1, "How to read this guide")
- **Leaders:** Part 1, the seven foundations that open Part 3, and the "How far each role goes" table in Part 5.
- **Analysts and operators:** Part 2, then Part 5 through Stage 3.
- **Engineers and security staff:** all five parts, with Parts 3 and 4 as the working reference.
- **Facilitators:** Part 5 end to end, with the Appendix tables as handouts.

## Key points
1. **Five stages** (§1.1, §5.1): chatbot with saved instructions; an API call in a container; containerized API workflows; tool calling with approval gates; an agent harness with skills. Chat-plus-API teams can stop at Stage 3 and still get working automation. See [[five-stage-training-progression]].
2. **Ranked focus areas** (§1.4): 1 evaluating output and systems, 2 data handling, 3 telling AI, workflows and agents apart, 4 clear task framing, 5 spotting automatable workflows, 6 working with tools and agents, 7 explaining AI to leadership.
3. **The harness, not the model, decides what AI can see and do** (§2.1). Endpoint is chosen by authorization and data level first, model second; keep it in config ([[ai-harness]], [[apis-and-endpoints]]).
4. **Tokens drive cost, capacity, speed, rate limits, quality and portability** (§2.2); "cost surprises almost always come from re-sent context in loops" ([[tokens]], [[context-window]]).
5. **Six ways AI fetches data**, combined by the harness; an index is a copy of your data (§2.3) ([[how-ai-finds-your-data]], [[embeddings-and-vector-search]]).
6. **Seven foundations** make an organization agnostic: approved MCP tools, containers, scanning, skills, approved packages, a multi-vendor API framework, stored evals (§3.1) ([[agnostic-ai-platform]], [[ai-resilience]]).
7. **The one rule** (§4.1): data only goes into a tool approved for that data's sensitivity level ([[safe-prompting]]). Top risks: data in the wrong system, unverified output, prompt injection.
8. **Role targets** (§5.2): all personnel Stage 1 in 2-3 hours; leaders Stage 1 plus demo in a half day; analysts Stage 3 in 2-3 days; technical staff Stage 5 in 5-8 days.
9. **Measures** (§1.1, §5.2): time saved per task, errors caught in review, library reuse, workflows in production, security findings ([[measuring-training-results]]).

## Worth quoting
> The model thinks, skills teach it how, tools let it act, and the harness decides which of those it gets.

> Data only goes into a tool approved for that data's sensitivity level.

> Without them, agnostic is a hope, not a fact.

## Pages this source updated
- [[ai-training-guide]], [[five-stage-training-progression]], [[large-language-model]], [[chatbot-workflow-agent]], [[ai-harness]], [[tokens]], [[context-window]], [[how-ai-finds-your-data]], [[embeddings-and-vector-search]], [[hallucination-and-verification]], [[safe-prompting]], [[ai-resilience]], [[agnostic-ai-platform]], [[measuring-training-results]]
