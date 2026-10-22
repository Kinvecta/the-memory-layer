---
type: concept
summary: The seven foundations an organization owns - approved MCP tools, containers, scanning, skills, approved packages, a multi-vendor API workflow framework, and stored evals - that let it swap models or vendors without rebuilding its work.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]"]
related: ["[[ai-resilience]]", "[[model-context-protocol]]", "[[containerization]]", "[[image-scanning-and-sbom]]", "[[agent-skills]]", "[[apis-and-endpoints]]", "[[ai-evals]]", "[[devsecops-pipeline]]", "[[ai-governance-and-controls]]"]
aliases: [seven foundations, agnostic AI workforce, vendor-agnostic platform]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Agnostic AI Platform (the Seven Foundations)

**TL;DR:** An organization is agnostic when it can swap the model, or the whole vendor, without rebuilding its work. That takes seven foundations it owns itself - none belongs to a model vendor. They form one loop that ends in stored evals watching for model drift and use-case drift, so a fix stays local.

## What it is
Part 3 of the [[ai-training-guide]] defines seven foundations "every use case in this guide runs on" ([[source-ai-training-guide]] §3.1):

| # | Foundation | What the organization must have | Why it keeps you agnostic |
|---|---|---|---|
| 1 | Approved MCP servers and tools | Catalog of authorized MCP servers, one per data source or system, tied to allowed use cases | The data connection is yours; any MCP-speaking harness can use it ([[model-context-protocol]]) |
| 2 | Containers and isolated environments | Pre-approved base images, a runtime in each enclave, network allow-lists | Authorization attaches to the image, not the model ([[containerization]]) |
| 3 | Scanning tools | Dependency, image and secret scanning, plus review of prompts, skills and tool descriptions as code | Vendor changes never bypass security ([[image-scanning-and-sbom]]) |
| 4 | Skills | Internal library of versioned, reviewed SKILL.md skills | Know-how installs in any compatible harness ([[agent-skills]]) |
| 5 | Code packages and libraries | Internal registry of approved packages, pinned versions, an SBOM per image | Built from known, scanned components |
| 6 | Workflows on a multi-vendor API framework | A layer speaking OpenAI, Anthropic and Google formats (and open-source servers), with prompts, endpoint and model version pinned in config | Changing models is a configuration change, not a rewrite ([[apis-and-endpoints]]) |
| 7 | Stored evals for model and use-case drift | A test set per prompt, skill and workflow, run on a schedule and on every change, results kept over time | "Without them, agnostic is a hope, not a fact" ([[ai-evals]]) |

## Why it matters
Models, vendors and apps keep changing ([[ai-resilience]]). The leadership summary lists these seven as "what to standardize" ([[source-ai-training-guide]] §1.1). Endpoints illustrate it: the same model is reachable through a vendor API, a cloud provider (AWS Bedrock, Azure, Vertex AI) or an approved platform, and with the endpoint in config, pinned versions and one request shape, a switch is a one-line change ([[source-s5-apis-endpoints-and-containers]] [2:40]).

## How it works
Figure 13 draws one loop: a use case enters, meets each foundation in order, and ends in evals that watch two kinds of drift ([[source-ai-training-guide]] §3.1):
- **Model drift** - a new version answers differently.
- **Use-case drift** - the business, data or users move while the prompt stays the same.

When either appears, "the fix is local: swap the model in configuration, or update a skill or prompt and send it back through review." MCP connections, containers, scanners, packages and eval history stay put, "which is what lets an organization treat models as interchangeable parts."

## In practice
- Skills and MCP servers are both open formats, so a whole skill-plus-tools package moves to another harness without rework ([[source-ai-training-guide]] §3.4).
- Each foundation flows through the [[devsecops-pipeline]]; governance mappings: NIST AI RMF's "measure" function is the eval store; ISO/IEC 42001 gives the seven foundations an audit structure ([[source-ai-training-guide]] Appendix; [[ai-governance-and-controls]]).
- Session 2 of the [[train-the-trainer-series]] teaches this as "what your organization owns that survives a switch."

## See also
[[ai-resilience]] · [[ai-evals]] · [[apis-and-endpoints]] · [[prompt-and-skill-library]]
