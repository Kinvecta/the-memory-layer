---
type: source
summary: Transcript summary of Session 2, which defines an agnostic organization, the seven foundations it owns, the four levels of switch, evals for model and use-case drift, and the "no evals, no switch" playbook.
sources: ["[[raw/transcripts/s2-ai-resilience]]"]
related: ["[[source-ai-training-guide]]", "[[train-the-trainer-series]]", "[[ai-resilience]]", "[[agnostic-ai-platform]]", "[[ai-evals]]", "[[agent-skills]]", "[[source-s1-what-an-llm-is]]", "[[source-s3-safe-prompting-and-verification]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 2 - AI Resilience

**TL;DR:** Session 2 of the [[train-the-trainer-series]] (about 8 minutes) asks what an organization owns that survives a model, vendor, endpoint or harness switch. The answer is seven foundations meeting at interfaces you control, so a model swap becomes a tested, one-line configuration change. Its rule: rent the model, own the connections, the know-how and the proof.

**Source file:** [[raw/transcripts/s2-ai-resilience]]  ·  **Kind:** transcript  ·  **Date:** October 2026

## Key points
1. **Why it matters** [0:48]: models retire on the vendor's schedule, terms (prices, data handling, limits) change with little notice, and approvals can change in either direction.
2. **Agnostic defined** [1:15]: able to swap the model or the whole vendor without rebuilding work. What you rent (model, app/harness) sits on top; what you own (seven foundations) sits below, joined by interfaces you control: MCP, a vendor-neutral API schema, the skill format. "Swap the top. Keep the bottom."
3. **Four levels of switch** [1:50]: model version (most common, easiest to miss), vendor, endpoint, harness. Each is cheap only if prompts and evals are stored, the workflow layer is vendor-neutral, the endpoint lives in config, and tools and skills are portable.
4. **Four myths** [2:24]: agnostic does not mean using every vendor; a gateway alone does not make you agnostic; switching is not a migration project; agnostic does not mean lowest common denominator.
5. **Seven foundations, one loop** [2:59, 3:49]: approved MCP tools, containers, scanning, skills, code packages, multi-vendor API layer, stored evals. "Wherever you don't own one, that's where lock-in hides." See [[agnostic-ai-platform]].
6. **Config switch** [4:28]: the config file names endpoint, model version and prompt; changing model A to model B is one line, output keeps the same shape, evals pass. Always pin a named version, never "latest."
7. **Skills portability** [5:06]: registry, review, scan, pin, install in harnesses A, B, C; C fails at first because file paths differ. "Write once. Test in each harness." See [[agent-skills]].
8. **Evals** [5:39]: model drift (score drops when a new version arrives; pin and fix in config) vs. use-case drift (slow slide as data and users change; update the skill or prompt). See [[ai-evals]].
9. **New-model playbook** [6:33]: arrive, pin current, run stored evals on the new model, compare, switch in config only if it passes, keep monitoring.
10. **Exercise** [7:05]: lock-in audit of one weekly workflow against the seven foundations (owned / vendor / missing), plus a 30-day retirement scenario. Most teams' biggest gap is evals.

## Worth quoting
> Rent the model. Own the connections. Own the know-how. And own the proof.

> No evals, no switch.

> Without evals, being agnostic is a hope, not a fact.

## Pages this source updated
- [[ai-resilience]], [[agnostic-ai-platform]], [[ai-evals]], [[agent-skills]]
