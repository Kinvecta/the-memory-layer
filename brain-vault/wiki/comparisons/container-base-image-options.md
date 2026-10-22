---
type: comparison
summary: Side-by-side of container base image families as of Oct 2026 (Docker Hardened Images, Chainguard, distroless, Red Hat UBI, Iron Bank, Bitnami, Alpine/Debian-slim) with cost, hardening and when to pick each.
sources: ["[[raw/research/containers-cicd-brief]]", "[[raw/transcripts/ddb-devsecops-containers-cicd]]"]
related: ["[[container-hardening]]", "[[containerization]]", "[[image-scanning-and-sbom]]", "[[image-signing-and-provenance]]", "[[devsecops-pipeline]]"]
aliases: [base images, DHI, Chainguard, distroless, UBI, Iron Bank]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Container base image options

**TL;DR:** The base image sets most of an image's vulnerability count, so choosing a minimal, hardened base pinned by digest is the cheapest security win. As of October 2026, Docker Hardened Images are free and open source, Chainguard's free tier is `:latest`-only, distroless and UBI are free, Iron Bank serves DoD, and Bitnami's free images are gone ([[source-ddb-devsecops-containers-cicd]] [4:51]; [[source-containers-cicd-brief]] §2.2).

| Family | Who | Cost / license (Oct 2026) | Hardened? | Notes |
|---|---|---|---|---|
| **Docker Hardened Images (DHI)** | Docker | Free, Apache 2.0 since 17 Dec 2025; DHI Enterprise paid | Yes | 1,000+ images on Debian/Alpine, each with SBOM, public CVE data, SLSA Build L3 provenance and signatures; includes hardened MCP server images. Enterprise adds FIPS/STIG, <7-day critical CVE SLA, extended lifecycle |
| **Chainguard Containers** | Chainguard | Free tier: limited set, `:latest` tags only, no SLA; paid from ~$19K/yr for a team of 10 | Yes | Built on Wolfi; minimal, frequently rebuilt, near-zero CVEs; FIPS/STIG variants paid; Chainguard Libraries paid |
| **Google distroless** | Google (OSS) | Free | Minimal | Language runtime only (`static`, `base`, `cc`, `python3`, `java`, `nodejs`); no shell; `:nonroot` variants |
| **Red Hat UBI** (8/9/10; `ubi`, `ubi-minimal`, `ubi-micro`) | Red Hat | Free to redistribute | Minimal variants | RHEL-based, supported on OpenShift; many Iron Bank images rebase on UBI |
| **Iron Bank** | DoD Platform One | Free (registry1.dso.mil; account required) | Yes | Evaluated against Acceptance Baseline Criteria with an Overall Risk Assessment score; rescanned every 12 hours; approval is **not** an ATO |
| **Bitnami** | Broadcom | Paid (Bitnami Secure Images) since Sep 2025; public catalog deleted 29 Sep 2025 | Paid tier | `bitnamisecure` free `:latest` is dev-only; `bitnamilegacy` is unpatched. Audit Helm charts and Dockerfiles for `bitnami/` references |
| **Alpine / Debian-slim / Ubuntu** | Community / Canonical | Free | Not by default | Fine starting points; Canonical sells hardened "chiseled" Ubuntu (pricing unverified) |

## When to pick which
- **General default, no budget:** DHI (free, signed, with SBOM and provenance) or distroless for a language runtime. Pin by digest either way ([[container-hardening]]).
- **Chainguard:** strong for near-zero CVEs, but the free tier only offers `:latest`, so production government systems should use a paid tier, DHI, Iron Bank or UBI, and always pin the digest ([[source-containers-cicd-brief]] §2.4).
- **OpenShift / RHEL shops:** UBI (`ubi-micro` for minimal runtime).
- **DoD software factories:** Iron Bank; vendors delivering containers to DoD typically must go through it. Proxy or mirror it into the program registry ([[source-containers-cicd-brief]] §4.5, §7).
- **Need FIPS/STIG or an SLA:** paid tiers (DHI Enterprise, Chainguard paid).
- **Alpine / Debian-slim:** acceptable only with your own hardening (multi-stage, non-root, scanning); "not hardened by default."
- **Inherited `bitnami/*` references:** treat as broken or unpatched; migrate.
- **Facing a pile of findings?** "Often the fastest fix of all is a newer, minimal base image" ([[source-ddb-devsecops-containers-cicd]] [8:56]). Lab 1 in the brief compares `python:3.12` against a DHI/Chainguard/distroless image with Trivy and Grype to make the point ([[source-containers-cicd-brief]] §9.1; [[image-scanning-and-sbom]]).
- Use the builder (`-dev`) variant only in the build stage of a multi-stage build; ship the minimal runtime variant.
