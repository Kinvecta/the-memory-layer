---
type: source
summary: Transcript summary of Session 1, which defines a large language model, the parts of an AI system, the six harness types, and the chatbot vs. workflow vs. agent test.
sources: ["[[raw/transcripts/s1-what-an-llm-is]]"]
related: ["[[source-ai-training-guide]]", "[[train-the-trainer-series]]", "[[large-language-model]]", "[[ai-harness]]", "[[chatbot-workflow-agent]]", "[[apis-and-endpoints]]", "[[source-s2-ai-resilience]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 1 - What an LLM Is

**TL;DR:** The first session of the [[train-the-trainer-series]] (about 10.5 minutes) teaches vocabulary before technology: what an LLM is and is not, the harness wrapped around it, the six kinds of harness, and the one-question test that separates a chatbot, a workflow and an agent. It closes with a task-sorting exercise and bridges to Session 2's seven foundations.

**Source file:** [[raw/transcripts/s1-what-an-llm-is]]  ·  **Kind:** transcript  ·  **Date:** October 2026

## Key points
1. **Why vocabulary first** [0:51]: most confusion in AI briefings is about words. "We use ChatGPT" means a whole system; "it's an agent" is often a chatbot or a fixed workflow; "the AI did it" credits the model for what the harness allowed. The three most misused terms: AI safety, agent, workflow.
2. **What an LLM is** [1:25]: a trained engine that predicts the next token. Example: after "The report is due on," the model scores every next token and "Friday" wins, then the loop runs again. A token is about three-quarters of a word; "large" means billions of weights; "model" means the engine only. See [[large-language-model]].
3. **How a model is made** [2:12]: pretraining, post-training (follow instructions, refuse harm, use tools), deployment with frozen weights. Consequences: knowledge cutoff, no learning from your chats, anything current is fetched by the harness.
4. **Six myths** [2:47]: "it looks things up," "it learns from my chats," "it knows today's news," "same question, same answer," "wrong answers are rare," "customizing means training." All false.
5. **Several models per request** [3:29]: classifier, vision model, embedding model and reranker, language model, output classifier, then a person. See [[how-ai-finds-your-data]].
6. **The rule** [4:04]: the model thinks, skills teach it how, tools let it act, the harness decides which it gets; via an API your software becomes the harness.
7. **Same model, three harnesses** [5:08]: chat app (low reach), coding agent (high reach, acts alone a lot), your own script (you decide reach and own every control). Security approves the harness, not just the model. See [[ai-harness]].
8. **Six harness types** [5:50] and the two sizing questions [6:39]: what can it reach, and how much does it act alone.
9. **Three API front doors** [7:09]: vendor API, cloud provider, approved platform; choose by authorization and data level first ([[apis-and-endpoints]]).
10. **Chatbot, workflow, agent** [7:47]: "Who picks each step?" If you already know the steps, build a workflow ([[chatbot-workflow-agent]]).
11. **Exercise** [9:15]: sort ten tasks (answer key: chatbot 1, 4, 7, 10; workflow 2, 5, 8; agent 3, 6, 9), then audit one team tool with five questions, ending with "who approved it, and for what data?"

## Worth quoting
> That's why it's so fluent. And it's also why it can be fluently wrong.

> Same engine. Different reach. Different risk.

> Products change every month. Learn the categories, not the brand names.

## Pages this source updated
- [[large-language-model]], [[ai-harness]], [[chatbot-workflow-agent]], [[apis-and-endpoints]], [[hallucination-and-verification]], [[how-ai-finds-your-data]]
