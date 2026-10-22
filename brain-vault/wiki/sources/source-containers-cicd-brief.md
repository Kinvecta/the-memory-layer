---
type: source
summary: Research brief (version-checked 20 Oct 2026) behind Deep Dive B covering containers, hardening, scanning tools, signing, the CI/CD pipeline, AI-specific gates, government context, run locations and firewalls.
sources: ["[[raw/research/containers-cicd-brief]]"]
related: ["[[source-ddb-devsecops-containers-cicd]]", "[[devsecops-pipeline]]", "[[containerization]]", "[[image-scanning-and-sbom]]", "[[image-signing-and-provenance]]", "[[container-hardening]]", "[[container-base-image-options]]", "[[secrets-management]]", "[[egress-control-and-firewalls]]", "[[ai-evals]]", "[[ai-governance-and-controls]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Containers, Image Scanning and CI/CD Brief

**TL;DR:** The detailed reference behind [[source-ddb-devsecops-containers-cicd]], written for a 90-minute train-the-trainer session for mixed technical and non-technical staff. It is framed (21 Oct 2026) as general DevSecOps best practice; the government material in its section 7 is optional context. Tool versions were pulled from package registries on 20 Oct 2026 and shaky items are flagged [UNVERIFIED].

**Source file:** [[raw/research/containers-cicd-brief]]  ·  **Kind:** notes (research brief)  ·  **Date:** 2026-10-20 (framing note 2026-10-21)

## Key points
1. **Ten things to get right (Oct 2026)** (§0): OMB M-26-05 (23 Jan 2026) rescinded the federal secure-software attestation memos; SSDF v1.2 is still a draft; CISA's 2026 Minimum Elements for an SBOM (late July 2026) adds hash, license, tool and author signature and covers AI; DoD CSRMC (24 Sep 2025) pushes continuous ATO; the March 2026 Trivy-action compromise; Docker Hardened Images free (Apache 2.0) since 17 Dec 2025; Bitnami free images deleted 29 Sep 2025; market renames (Cortex Cloud, Google-Wiz, `snyk-agent-scan`, OpenAI-Promptfoo); Cosign v3; OWASP Agentic Top 10 (9 Dec 2025).
2. **Containers explained** (§1): image, layer, container, registry, OCI; container vs VM; runtimes (containerd, CRI-O, Podman); Kubernetes 1.35-1.37 supported. See [[containerization]].
3. **Hardening** (§2): base-image table, 11-item checklist mapped to NIST SP 800-190, a hardened Python Dockerfile and a restricted Kubernetes securityContext. See [[container-hardening]], [[container-base-image-options]].
4. **Scanning** (§3): CVE/CVSS/EPSS/KEV/VEX vocabulary, prioritization recipe, nine scan categories (including model-file and MCP/agent scanning), and a large tool table with versions. See [[image-scanning-and-sbom]].
5. **Supply-chain integrity** (§4): Cosign, Notation, GitHub attestations; SLSA v1.2 build levels; SPDX vs CycloneDX; admission with Kyverno, Gatekeeper, policy-controller; private registries. See [[image-signing-and-provenance]].
6. **Pipeline** (§5): ten stages with break-the-build gates, time-boxed exception path, CI/CD platforms, a full annotated GitHub Actions workflow and `cosign verify` commands. See [[devsecops-pipeline]].
7. **AI additions** (§6): evals as a gate with sample thresholds; pin model and prompt versions; scanning MCP servers and skills; secrets for API keys; egress allow-listing; model-file scanning; OpenTelemetry GenAI telemetry. See [[ai-evals]], [[secrets-management]], [[model-context-protocol]].
8. **Government context** (§7) and **roles** (§8): paperwork loosened, practice moved toward automated, machine-readable evidence; "one scanned image, authorized and redeployed" is how pipelines speed approvals. See [[ai-governance-and-controls]].
9. **Labs, check questions, misconceptions** (§9): five labs, a non-technical "read the evidence" variant, air-gapped classroom tips, 11 misconceptions.
10. **Where containers run** (§11) and **firewalls** (§12): shared-responsibility table, sandboxed runtimes, eight network layers, Docker/ufw gotcha. See [[egress-control-and-firewalls]].
11. **Re-verify before delivery** (§10): SSDF status, CVE program funding, action SHAs, SWFT/CSRMC guidance, FedRAMP 20x dates, `snyk-agent-scan` data flow, Promptfoo licensing.

## Worth quoting
> "A pipeline that emits signed SBOMs, scan results and provenance is how you meet all of them with one investment." (§7)

> "Rebuilding for prod is safer." -- "It breaks the evidence chain. Promote the same signed digest." (§9.3)

> "Same image everywhere; who patches what changes. Default deny, both directions." (§12.6)

## Pages this source updated
- [[containerization]]
- [[container-hardening]]
- [[container-base-image-options]]
- [[image-scanning-and-sbom]]
- [[image-signing-and-provenance]]
- [[devsecops-pipeline]]
- [[secrets-management]]
- [[egress-control-and-firewalls]]
- [[ai-evals]]
