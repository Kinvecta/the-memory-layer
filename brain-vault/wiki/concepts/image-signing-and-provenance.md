---
type: concept
summary: How signing an image by digest, attaching SBOM/provenance/scan attestations, and enforcing admission control prove the running box is the one that was scanned and built by your pipeline.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]"]
related: ["[[image-scanning-and-sbom]]", "[[devsecops-pipeline]]", "[[containerization]]", "[[container-hardening]]", "[[ai-governance-and-controls]]"]
aliases: [Cosign, Sigstore, SLSA, attestation, admission control, provenance]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Image signing and provenance

**TL;DR:** Scanning asks "is the box safe?"; signing asks "is this the same box we scanned, and did it come from our factory?" Like a tamper-evident seal plus a shipping manifest, a signature on the image digest plus attestations (SBOM, provenance, scan result) lets admission control run only signed images and deny everything else ([[source-ddb-devsecops-containers-cicd]] [10:01]).

## What it is
- **Signature:** a cryptographic seal on the image **digest**, not its tag. Tags can be re-pointed; digests can't.
- **Attestation:** a signed statement about an artifact (in-toto format): "built from commit X by workflow Y," "this SBOM describes digest Z," "passed Trivy with 0 criticals" ([[source-containers-cicd-brief]] §4.3).
- **Provenance:** who built it, from which commit, with which workflow.
- **Admission control:** the guard at the loading dock that refuses any box without a valid seal.

## Why it matters
Without signing, an attacker could swap a scanned image for a malicious one; without scanning, you would faithfully deliver vulnerable software. You need both ([[source-containers-cicd-brief]] §9.2). Signed, digest-pinned evidence is what lets an assessor approve the pipeline once and accept every release it produces, including rebuilds for new CVEs, without a new ATO ([[source-containers-cicd-brief]] §8; [[ai-governance-and-controls]]).

## How it works
Flow ([[source-ddb-devsecops-containers-cicd]] [10:01]): CI builds the image from a known commit -> **Cosign keyless signing** gives the CI job's own OIDC identity a short-lived certificate and records the signature in a public transparency log (Sigstore Fulcio + Rekor) -> attestations attach to the digest -> push to registry -> admission control checks the seal; signed runs, unsigned is denied.

**SLSA v1.2 build levels** ([[source-containers-cicd-brief]] §4.3): L1 provenance exists; L2 hosted build, provenance signed by the platform; L3 hardened, isolated builds where signing secrets are inaccessible to user build steps. Claiming L3 needs a review of the platform's isolation.

## In practice
Tools ([[source-ddb-devsecops-containers-cicd]] [10:52]; [[source-containers-cicd-brief]] §4):

| Job | Tools |
|---|---|
| Sign + attest | Cosign v3.1.4 (v3 made the bundle format default, Oct 2025), Notation (your own X.509 certs), GitHub artifact attestations (`actions/attest@v4`) |
| Registry | Harbor (OSS, Trivy built in, good air-gapped), ECR, ACR, Google Artifact Registry, Artifactory, Quay, GHCR, Iron Bank |
| Admission | Kyverno (CNCF graduated 24 Mar 2026; can rewrite tags to digests), OPA Gatekeeper + Ratify, Sigstore policy-controller |
| GitOps | Argo CD, Flux (pull desired state from git; full audit trail) |

- In CI: `cosign sign --yes IMAGE@sha256:...` then `cosign attest --type cyclonedx --predicate sbom.cdx.json`. Verify with `cosign verify --certificate-identity-regexp ... --certificate-oidc-issuer https://token.actions.githubusercontent.com` or `gh attestation verify` ([[source-containers-cicd-brief]] §5.4).
- **Air-gapped:** public Sigstore needs internet, so use a private Sigstore, key-based Cosign with an HSM/KMS, or Notation with internal PKI.
- **Promote, don't rebuild:** staging and prod run the identical digest. "Rebuild for prod" breaks the evidence chain ([[source-containers-cicd-brief]] §5.4).

## See also
[[image-scanning-and-sbom]] · [[devsecops-pipeline]] · [[containerization]]
