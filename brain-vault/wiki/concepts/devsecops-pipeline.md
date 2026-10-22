---
type: concept
summary: The DevSecOps loop and gated CI/CD line every AI component (MCP server, workflow, harness) passes through, from commit to runtime monitoring, shipping one signed digest.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[image-scanning-and-sbom]]", "[[image-signing-and-provenance]]", "[[container-hardening]]", "[[secrets-management]]", "[[egress-control-and-firewalls]]", "[[ai-evals]]", "[[containerization]]", "[[ai-governance-and-controls]]", "[[building-an-mcp-server]]"]
aliases: [DevSecOps, CI/CD, CI-CD pipeline, software factory]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# DevSecOps pipeline

**TL;DR:** DevSecOps means security is part of every stage, not one gate at the end. MCP servers, API workflows and harnesses are software, so they go through the same pipeline as any code; prompts, skills and tool descriptions are part of that code, and the one AI-specific addition is the eval step ([[source-ai-training-guide]] Part 4). The rule: pin everything, scan before it ships, sign it, and ship the same digest.

## What it is
A loop ([[source-ddb-devsecops-containers-cicd]] [1:33]): **plan** (threat model) -> **code** (secret scanning, static analysis) -> **build** (pinned base, SBOM) -> **test** (scans and, for AI, [[ai-evals]]) -> **release** (signing) -> **deploy** (admission checks) -> **operate** (secrets, firewalls) -> **monitor** (runtime alerts, rescans) -> back to plan. Security-at-the-end finds everything at once and sends every fix back through every stage. "Shift left, and keep watching right."

CI/CD is "an assembly line with inspection stations": if any station finds a problem over the limit, the line stops ([[source-containers-cicd-brief]] §5.1).

## Why it matters
It fixes "it worked on my laptop," "forty high findings, now what?" and "the scanner was the attack" ([[source-ddb-devsecops-containers-cicd]] [0:56]). Because every change goes through identical, logged inspections, approvers can trust the line rather than each release, which is the idea behind continuous ATO ([[source-containers-cicd-brief]] §5.1, §8; see [[ai-governance-and-controls]]).

## How it works
Ten stages and typical gates ([[source-containers-cicd-brief]] §5.2):
1. **Commit:** pre-commit secret scan; any verified secret blocks (push protection).
2. **PR review:** human review, SAST, SCA, IaC, secrets; no new high/critical SAST findings.
3. **Build:** ephemeral runner, digest-pinned base, SBOM; actions pinned by SHA.
4. **Test + evals:** against the pinned model ID and prompt version; e.g. >= 0.90 accuracy, 0 critical safety failures.
5. **Scan image:** fail on fixable critical (often high), any KEV, forbidden licenses, secrets in layers.
6. **Sign + attest** the digest. 7. **Push** to a private registry that blocks unsigned images.
8. **Staging:** GitOps deploy by digest, admission check, DAST and smoke evals.
9. **Promote** the same digest to prod, no rebuild. 10. **Runtime monitoring:** Falco/Tetragon, registry rescans, OpenTelemetry traces, cost monitoring.

Detail lives in [[image-scanning-and-sbom]], [[image-signing-and-provenance]] and [[egress-control-and-firewalls]].

## In practice
- **Annotated GitHub Actions pattern** ([[source-ddb-devsecops-containers-cicd]] [12:41]): `permissions: contents: read` by default; jobs opt in; actions pinned to full commit SHA (never invent one; "a wrong SHA is worse than none"); Semgrep fails on findings; build and load locally; Trivy scan with exit code 1; push only after the scan passes; Cosign signs by digest and attaches the SBOM; add signed build provenance.
- **Pin the scanners too.** In March 2026 attackers force-pushed 75+ tags of `aquasecurity/trivy-action` to steal CI secrets; SHA-pinned workflows kept running good code. GitHub org policy can now enforce SHA pinning ([[source-containers-cicd-brief]] §0).
- **Exceptions** must be time-boxed with an owner and expiry, plus VEX for false positives, or teams just switch the scanner off.
- **Evals** use a separate low-quota, eval-only key in a protected environment; don't run paid evals on fork PRs.
- **Per-component controls** (build-time and run-time for MCP server, workflow, harness) are tabled in [[ai-governance-and-controls]]; across all three, a new prompt, skill or server version is a new release, not an edit in place ([[source-ai-training-guide]] Part 4).

> [!warning] "Or true" defeats the gate
> The Deep Dive B exercise hides `|| true` after a scan step: the scan runs but can never fail the build ([[source-ddb-devsecops-containers-cicd]] [17:38]).

## See also
[[container-hardening]] · [[secrets-management]] · [[containerization]] · [[building-an-mcp-server]]
