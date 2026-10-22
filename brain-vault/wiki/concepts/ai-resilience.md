---
type: concept
summary: AI resilience means an organization can swap the model, endpoint, harness or whole vendor without rebuilding its work; covers the four levels of switch, the rent-vs-own split, myths about being agnostic, and the "no evals, no switch" playbook.
sources: ["[[raw/transcripts/s2-ai-resilience]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[agnostic-ai-platform]]", "[[ai-evals]]", "[[apis-and-endpoints]]", "[[agent-skills]]", "[[model-context-protocol]]", "[[prompt-and-skill-library]]", "[[ai-harness]]"]
aliases: [vendor agnostic, agnostic, model switching, lock-in]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI resilience

**TL;DR:** An organization is resilient (agnostic) when it can swap the model, or the whole vendor, without rebuilding its work. It rents the model and harness and owns seven foundations that meet them at interfaces it controls, so a switch is a tested, one-line configuration change. The rule: rent the model; own the connections, the know-how and the proof.

## What it is
At the top is what you rent: the model and the app or [[ai-harness]] around it; expect both to change. At the bottom is what you own: the seven foundations of the [[agnostic-ai-platform]]. They meet at interfaces you control: MCP ([[model-context-protocol]]), a vendor-neutral API schema, and the skill format. "Swap the top. Keep the bottom" ([[source-s2-ai-resilience]] [1:15]; [[source-ai-training-guide]] §3.1).

- **Connections** = MCP tools and the API layer.
- **Know-how** = skills and prompts.
- **Proof** = stored evals.

([[source-s2-ai-resilience]] [6:16])

## Why it matters
The model you use today will not be next year's: models retire and older versions are switched off on the vendor's schedule; prices, data handling and limits change with little notice; and security approvals can change in either direction ([[source-s2-ai-resilience]] [0:48]).

## Four levels of switch
| Switch | Example | Note |
|---|---|---|
| Model version | Same vendor, newer model | Most common, easiest to miss |
| Vendor | Different model family | |
| Endpoint | Same model, different door (vendor API to cloud provider) | See [[apis-and-endpoints]] |
| Harness | Different app or agent tool | |

Each is cheap only if prompts and evals are stored, the workflow layer is vendor-neutral, the endpoint lives in configuration, and tools and skills are portable ([[source-s2-ai-resilience]] [1:50]).

## Myths
- "Agnostic means using every vendor." No: it means being able to switch, usually while running one.
- "A gateway makes us agnostic." It helps, but prompts, tools, skills and tests tied to one vendor still lock you in.
- "Switching is a migration project." With config and evals it is a tested one-line change.
- "Agnostic means lowest common denominator." No: use each vendor's best features through interfaces you own.

([[source-s2-ai-resilience]] [2:24])

## How it works
- **Config switch:** the config file names the endpoint, model version and prompt. Change model A to model B; output keeps the same fields; evals pass again. Change configuration, not code, and pin a named version, never "latest" ([[source-s2-ai-resilience]] [4:28]; [[source-ai-training-guide]] §2.1, §4.1).
- **Skills:** registry, review, scan, pin, install in each harness; expect one to fail first (e.g. file paths differ). "Write once. Test in each harness" ([[source-s2-ai-resilience]] [5:06]; [[agent-skills]]).
- **Evals:** detect model drift (score drops on a new version; pin and fix in config) and use-case drift (slow slide as data and users change; update the skill or prompt) ([[source-s2-ai-resilience]] [5:39]; [[ai-evals]]).
- The embedding model behind an index is the one swap config cannot do alone; it requires re-indexing ([[embeddings-and-vector-search]]).

## New-model playbook
1. A new model arrives. 2. Pin your current version. 3. Run stored evals on the new model. 4. Compare; if it fails, stay pinned and retry later. 5. If it passes, switch in configuration. 6. Keep monitoring for drift. **No evals, no switch** ([[source-s2-ai-resilience]] [6:33]).

## In practice
Session 2 lock-in audit: for one weekly workflow, mark each foundation owned / vendor-owned / missing; then imagine the model retires in 30 days: is the model named in config or code, which evals prove a replacement, which prompts or skills change, who approves? Most teams' biggest gap is evals ([[source-s2-ai-resilience]] [7:05]).

## See also
[[agnostic-ai-platform]] · [[ai-evals]] · [[apis-and-endpoints]] · [[source-s2-ai-resilience]]
