---
type: source
summary: Transcript of Deep Dive B, a ~19-minute narrated session on shipping AI workloads as one hardened, scanned, signed container image through a gated CI/CD line with default-deny networking.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]"]
related: ["[[source-containers-cicd-brief]]", "[[devsecops-pipeline]]", "[[containerization]]", "[[image-scanning-and-sbom]]", "[[image-signing-and-provenance]]", "[[container-hardening]]", "[[secrets-management]]", "[[egress-control-and-firewalls]]", "[[ai-evals]]", "[[train-the-trainer-series]]", "[[source-dda-build-an-mcp-server]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Deep Dive B - DevSecOps, Containers, Scanning and CI/CD

**TL;DR:** Deep Dive B teaches non-engineers and engineers alike how to "ship one box we can trust, and keep trusting": build a minimal image pinned by digest, keep secrets out of it, scan it at every stage, sign it, promote the same digest to production, and fence it in with default-deny networking in both directions. It is the companion to [[source-dda-build-an-mcp-server]] ("Build it. Box it. Ship it.") and is built on [[source-containers-cicd-brief]].

**Source file:** [[raw/transcripts/ddb-devsecops-containers-cicd]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (series recorded Oct 2026)

## Key points
1. **Four outcomes** [0:32]: explain DevSecOps, images and where containers run; read a hardened Dockerfile and a scan report; walk the CI/CD line and its gates; set default-deny rules in both directions. No engineering background assumed.
2. **Three problems a pipeline solves** [0:56]: "it worked on my laptop"; "forty high findings, now what?"; and "the scanner was the attack" (March 2026 hijack of a popular scanner's GitHub Action to steal CI secrets). See [[devsecops-pipeline]].
3. **DevSecOps loop** [1:33]: plan (threat model), code (secret scanning, SAST), build (pinned base, SBOM), test (scans plus AI evals), release (signing), deploy (admission), operate (secrets, firewalls), monitor (runtime alerts, rescans). "Shift left, and keep watching right."
4. **Image, container, registry, digest vs tag** [2:18]: "A tag can move. A digest can't." See [[containerization]].
5. **Where it runs** [3:06]: laptop, single server, serverless containers, Kubernetes, edge/air-gapped. Who patches what changes; your image, code, keys and network rules are always yours. Untrusted (agent-written) code needs gVisor, Firecracker or Kata.
6. **Four hardening fixes** [4:05]-[4:51]: minimal base pinned by digest, multi-stage build, no secrets in the image, non-root user (UID 65532); hash-checked requirements. Base-image options compared in [[container-base-image-options]]; detail in [[container-hardening]].
7. **Secrets** [5:59]: never in image, repo, CI log or baked `.env`; secrets manager plus OIDC workload identity, injected at run time, rotated without rebuild, audited. See [[secrets-management]].
8. **Scanning stations and tools** [6:58]-[7:46]: secret scan at commit, SAST/SCA/config in PR, image scan after build, SBOM as inventory, DAST in staging, registry rescans. See [[image-scanning-and-sbom]].
9. **Triage** [8:56]: 214 SBOM components -> 40 findings -> KEV (1) and high EPSS (3) block, 6 fixable crit/high this sprint, 9 VEX, 21 backlog. "Fix what's exploited first, not just what scores highest."
10. **Signing and admission** [10:01]-[10:52]: Cosign keyless, attestations (SBOM, provenance, scan result), admission control denies unsigned images; air-gapped uses private Sigstore, HSM keys or Notation. See [[image-signing-and-provenance]].
11. **The line** [11:50]-[12:41]: a failing fixable critical stops the build; same digest in staging and prod; every exception needs an owner and expiry. Annotated GitHub Actions: read-only permissions, SHA-pinned actions, scan before push, sign the digest.
12. **Trivy incident** [13:44]: tag-pinned workflows ran attacker code after tags were force-pushed; SHA-pinned workflows did not.
13. **Firewalls** [14:31]-[15:27]: six network layers; the Docker/ufw gotcha; egress proxy with hostname allow-list. See [[egress-control-and-firewalls]].
14. **AI gates** [16:41]: pin model ID, version prompts, hash tool definitions, eval gate (golden set, zero safety failures, valid outputs), MCP/skill scan; run evals on a schedule. See [[ai-evals]], [[model-context-protocol]], [[prompt-injection]].
15. **Exercise and checks** [17:38]-[18:27]: find 8+ problems in a Dockerfile and pipeline (hint: "or true"); triage six findings (KEV, EPSS >= 0.1, fixable critical block); six check questions.

## Worth quoting
> "One box, scanned once, trusted everywhere." [0:00]

> "Pin everything. Scan before it ships. Sign it, and ship the same digest." [17:23]

> "A blocked outbound attempt from an AI workload is a high-signal alert." [15:27]

## Pages this source updated
- [[devsecops-pipeline]]
- [[containerization]]
- [[container-hardening]]
- [[container-base-image-options]]
- [[secrets-management]]
- [[image-scanning-and-sbom]]
- [[image-signing-and-provenance]]
- [[egress-control-and-firewalls]]
- [[ai-evals]]
