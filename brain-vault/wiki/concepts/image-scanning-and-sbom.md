---
type: concept
summary: How pipelines scan code, dependencies, config and container images at several stations, build an SBOM inventory, and triage findings with KEV, EPSS, CVSS and VEX.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[devsecops-pipeline]]", "[[image-signing-and-provenance]]", "[[container-hardening]]", "[[container-base-image-options]]", "[[secrets-management]]", "[[agnostic-ai-platform]]", "[[model-context-protocol]]", "[[prompt-injection]]"]
aliases: [SBOM, software bill of materials, vulnerability scanning, CVE triage, SAST, SCA, DAST]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Image scanning and SBOM

**TL;DR:** Scanning is airport security for software: different machines look for different things, so pipelines run several scanners at different stations and rescan after shipping. The SBOM is not a check but the inventory of every component in the box. Triage by exploitation, not raw score: KEV first, then high EPSS, then fixable critical/high, and document "not affected" with VEX.

## What it is
Stations along the line ([[source-ddb-devsecops-containers-cicd]] [6:58]):
- **Commit:** secret scanning catches an API key.
- **Pull request:** SAST (our code; e.g. an injection pattern), SCA (a vulnerable library), config/IaC (a container set to run as root).
- **After build:** image scan (e.g. a CVE in openssl); SBOM generated.
- **Staging:** DAST probes the running app (e.g. an open admin endpoint).
- **After shipping:** registries rescan stored images, because new CVEs appear (Iron Bank rescans every 12 hours) ([[source-containers-cicd-brief]] §4.5).

AI adds two categories: model-file scanning (pickle payloads; ModelScan) and agent/MCP scanning for tool poisoning and [[prompt-injection]] in tool descriptions (`snyk-agent-scan`, formerly `mcp-scan`) ([[source-containers-cicd-brief]] §3.3).

## Why it matters
"No single scanner catches everything. Scan early, where fixes are cheapest. And scan again later." Scanning is foundation 3 of the [[agnostic-ai-platform]]: every new package, skill or model release goes through the same checks, so vendor changes never bypass security ([[source-ai-training-guide]] §3.1). An SBOM for every image is required across all components ([[source-ai-training-guide]] Part 4).

## How it works
**Vocabulary** ([[source-containers-cicd-brief]] §3.2): **CVE** = a known flaw's ID; **CVSS** = how bad it could be (0-10); **EPSS** = probability of exploitation in the next 30 days; **KEV** = CISA's list of flaws exploited now; **VEX** = a machine-readable "not affected, and why."

**Worked triage** ([[source-ddb-devsecops-containers-cicd]] [8:56]): SBOM lists 214 components -> 40 findings. KEV: 1, blocks. High EPSS: 3, block. Fixable critical/high: 6, fix this sprint. VEX: 9, documented. Backlog: 21. The gate blocks four. "Fix what's exploited first, not just what scores highest." Often the fastest fix is a newer, minimal base image ([[container-base-image-options]]).

**SBOM formats:** SPDX (ISO/IEC 5962) and CycloneDX (ECMA-424, v1.7 as of Oct 2025). CISA's 2026 Minimum Elements (late July 2026) add component hash, license, tool, generation context and author signature and cover AI; a CISA + G7 "SBOM for AI" followed on 13 May 2026 ([[source-containers-cicd-brief]] §0, §4.3).

## In practice
Tools by category (OSS first; [[source-ddb-devsecops-containers-cicd]] [7:46]; versions as of 20 Oct 2026 in [[source-containers-cicd-brief]] §3.4):

| Category | Open source | Commercial |
|---|---|---|
| Image vulns + SBOM | Trivy (v0.76.0), Syft + Grype | Docker Scout, Snyk |
| Secrets | Gitleaks, TruffleHog (checks if live), GitHub push protection | GitHub Secret Protection |
| Our code (SAST) | Semgrep, CodeQL | Semgrep platform |
| Libraries (SCA) | OSV-Scanner, Dependency-Check; Renovate/Dependabot keep pins current | Snyk, Socket |
| Config/IaC | Trivy config (absorbed tfsec), Checkov, KICS | Cortex Cloud, Wiz |
| DAST, malware | ZAP, ClamAV | -- |

- Typical gate: `trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 IMAGE`.
- Exercise policy: block KEV, EPSS >= 0.1, and any fixable critical; time-boxed exception with an owner if no fix; VEX if the code is never called ([[source-ddb-devsecops-containers-cicd]] [17:38]).

> [!warning] "Zero CVEs means secure" is a misconception
> Scanners find only known issues in recognized packages. Logic flaws, misconfigs, prompt injection and secrets need other controls ([[source-containers-cicd-brief]] §9.3).

## See also
[[image-signing-and-provenance]] (scanning asks "is it safe?", signing asks "is it the same box?") · [[devsecops-pipeline]] · [[secrets-management]]
