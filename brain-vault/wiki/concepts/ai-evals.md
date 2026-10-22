---
type: concept
summary: Evals are versioned test sets for every prompt, skill and workflow that gate release, re-run on any model or prompt change and on a schedule, and store results to catch model and use-case drift.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]"]
related: ["[[devsecops-pipeline]]", "[[agnostic-ai-platform]]", "[[prompt-and-skill-library]]", "[[hallucination-and-verification]]", "[[measuring-training-results]]", "[[prompt-injection]]", "[[workflows]]", "[[agent-skills]]", "[[tokens]]"]
aliases: [evals, evaluations, golden set, eval gate]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI evals

**TL;DR:** Every saved prompt, skill and workflow keeps a small test set (sample inputs with known-good outputs, plus at least one tricky case such as a planted instruction) that must pass before others use it and again after any prompt or model version change ([[source-ai-training-guide]] §5.2 Measuring results). In the pipeline, evals are the one AI-specific gate; stored over time, they are how you know a model swap worked.

## What it is
A version-controlled suite with expected behaviors: correctness on a golden dataset, refusal of disallowed requests, resistance to injection strings, correct tool selection and arguments for agents, output schema validity, and cost/latency budgets ([[source-containers-cicd-brief]] §6.1). It is foundation 7 of the [[agnostic-ai-platform]]: a test set per prompt, skill and workflow, kept with the code, run on a schedule and on every model or data change, with results stored ([[source-ai-training-guide]] §3.1).

## Why it matters
- **Evaluation is the core skill.** The most common failure is too little evaluation; as output gets more fluent, the scarce skill is testing whether it is right ([[source-ai-training-guide]] §1.1, §1.3, §1.4). See [[hallucination-and-verification]].
- **Two kinds of drift:** the model changing (a new version answers differently) and the use case changing (business, data or users move while the prompt stays the same). "Without them, agnostic is a hope, not a fact" ([[source-ai-training-guide]] §3.1).
- **Behavior is a build output.** The model, prompt and tools are build inputs; behavior can change when any change ([[source-ddb-devsecops-containers-cicd]] [16:41]), as can retrieval index, temperature or SDK version ([[source-containers-cicd-brief]] §6.1).

## How it works
AI gates in the pipeline ([[source-ddb-devsecops-containers-cicd]] [16:41]): model ID pinned; prompt a versioned file; tool definitions hashed so a quiet change alerts; eval gate (golden set passes, zero safety failures, every output valid); MCP/skill scan flags poisoned tool descriptions; egress proxy at runtime.

Example thresholds ([[source-containers-cicd-brief]] §6.1, §5.2): accuracy >= baseline - 2% (or >= 0.90), 0 critical safety failures, 100% JSON-schema valid, p95 latency < 8 s, cost/run < $0.05.

**Run on a schedule, not only on code change.** Pinned model IDs are fixed snapshots, but serving infrastructure can shift behavior slightly and every ID has a retirement date ([[source-containers-cicd-brief]] §6.2). Record tokens per task alongside accuracy, so a swap that doubles cost shows as drift ([[source-ai-training-guide]] §2.2; [[tokens]]). Include retrieval cases (an answer in a table or image) and track the embedding model behind each index ([[source-ai-training-guide]] §2.3).

## In practice
- Tools: Promptfoo (OpenAI announced acquisition 9 Mar 2026), DeepEval, OpenAI Evals, Inspect, LangSmith/Langfuse datasets; garak for red-team probes ([[source-containers-cicd-brief]] §6.1).
- CI: separate low-quota, eval-only key in a protected environment; pin `MODEL_ID` and `PROMPT_VERSION`; don't run paid evals on fork PRs ([[source-containers-cicd-brief]] §5.4).
- Harnesses are re-evaluated after any model or skill update ([[source-ai-training-guide]] Part 4).
- Diagnosis check: "the agent's code didn't change but its answers got worse" -> pinned model and versioned prompts, plus scheduled evals and model/prompt version in telemetry ([[source-containers-cicd-brief]] §9.2).
- Prompt authors and product owners write and maintain eval cases ([[source-containers-cicd-brief]] §8); results feed [[measuring-training-results]].

## See also
[[prompt-and-skill-library]] · [[devsecops-pipeline]] · [[prompt-injection]] · [[workflows]] · [[agent-skills]]
