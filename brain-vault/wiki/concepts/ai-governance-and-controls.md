---
type: concept
summary: The governance layer of the AI Training Guide: the one rule (data only goes into a tool approved for its sensitivity level), human accountability, operational controls (secrets, audit logs, version pinning, rate limits), per-component build and run-time controls, and the frameworks behind them as of Oct 2026.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]"]
related: ["[[prompt-injection]]", "[[devsecops-pipeline]]", "[[secrets-management]]", "[[ai-evals]]", "[[safe-prompting]]", "[[ai-harness]]", "[[model-context-protocol]]", "[[tool-calling]]", "[[egress-control-and-firewalls]]"]
aliases: ["AI governance", "the one rule", "AI security policy"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI governance and controls

**TL;DR:** Every trainee must know one rule cold: data only goes into a tool approved for that data's sensitivity level. Behind it sit human accountability (AI drafts, a person signs), operational controls for API, workflow and harness work, and a DevSecOps pipeline every AI component passes through before it is trusted. Prompts, skills and tool descriptions are code, not an exception to it.

## What it is
Part 4 of the [[ai-training-guide]] ([[source-ai-training-guide]] Part 4). Core topics (§4.1):
- **Confidential data and PII handling:** what counts, how to strip or avoid it, what to do after an accidental paste.
- **Human accountability:** AI drafts; a person signs. Outputs used in decisions need a named reviewer.
- **Records and transparency:** when AI-assisted work must be labeled; prompts and outputs may be subject to records and FOIA rules.
- **Responsible use:** bias checks on outputs that affect people, and escalation paths.

Safe-use flow (Figure 19): two checks, one sign-off. If the data is not cleared for the tool, switch tools before writing a prompt. If the draft fails verification, revise and rerun ([[safe-prompting]], [[hallucination-and-verification]]).

## Why it matters
Through an API your own software becomes the harness, so your team owns the instructions, data handling, logging and security controls (§2.1; [[ai-harness]]). As tools and agents arrive, risks like [[prompt-injection]] grow with each stage, and controls must live in the harness, the server and the network, not in the model.

## How it works
**Operational controls for Stages 2-5** (§4.1):

| Control | What to do |
|---|---|
| Secrets | Approved secrets store, injected at run time; never in code, prompts, images or logs; rotate on a schedule ([[secrets-management]]) |
| Audit logging | Who ran what, prompt version, model version, inputs, outputs, tool actions; retain per records rules |
| Model version pinning | Call a specific version, not "latest"; rerun library test cases before switching |
| Rate and cost limits | Per-workflow limits so a loop or error cannot run up usage |

**Per-component controls** (§4.1):
- **MCP server:** pinned, scanned dependencies; peer-reviewed tool descriptions; one least-privilege service account; read-only by default. At run time: egress only to its backing system, action tools only where the harness enforces approval, every call logged, schemas validated, rate limits. Owned by the backing system's team with security review ([[building-an-mcp-server]]).
- **API workflow:** versioned prompts, passing test set, keys from the secrets store, pinned model; output validation and a human review gate before delivery. Owned by the workflow team, with a named reviewer per run ([[workflows]]).
- **Harness (agent):** approved image, skills reviewed and pinned from an internal registry, permission config in the repo; no host access, per-user identity, approval gates, retained transcripts, injection monitoring, a kill switch, re-evaluation after model or skill updates. Owned by platform team with the authorizing official ([[ai-agents]]).

Across all three: identity and access control, an SBOM for every image ([[image-scanning-and-sbom]]), and change control where a new version is a new release, not an edit in place. The one AI-specific pipeline step is evaluation: test sets must pass before build and again when the model version changes ([[ai-evals]], [[devsecops-pipeline]]).

## In practice
**Frameworks (as of October 2026)** (guide appendix):
- **NIST AI RMF 1.0** and its 2024 Generative AI Profile: "measure" maps to the eval store; the risk list maps to Part 4.
- **ISO/IEC 42001:** certifiable AI management-system standard.
- **EU AI Act:** risk-tiered, obligations phasing in from 2025; needs logging, documentation and human oversight.
- **OWASP Top 10 for LLM Applications:** led by prompt injection.
- **SOC 2 and existing data policy:** the one rule uses your existing sensitivity levels, not a new scheme.

> [!tip] Gate by action, not by model
> Read tools run freely from approved sources; action tools wait for a person ([[source-s7-tools-mcp-and-prompt-injection]] 5:47).

## See also
[[prompt-injection]] · [[devsecops-pipeline]] · [[container-hardening]] · [[egress-control-and-firewalls]] · [[measuring-training-results]]
