---
type: concept
summary: How to harden a container image for an AI workload: minimal base pinned by digest, multi-stage build, no secrets in layers, non-root, read-only filesystem and dropped capabilities.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]"]
related: ["[[container-base-image-options]]", "[[containerization]]", "[[secrets-management]]", "[[image-scanning-and-sbom]]", "[[devsecops-pipeline]]", "[[building-an-mcp-server]]"]
aliases: [hardened image, Dockerfile hardening, distroless]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Container hardening

**TL;DR:** A hardened image holds only what the app needs: no shell, no package manager, no compilers. Fewer things means fewer vulnerabilities and fewer tools for an attacker ([[source-ddb-devsecops-containers-cicd]] [4:05]). Four fixes do most of the work: minimal base pinned by digest, multi-stage build, no secrets in the image, and a non-root user.

## What it is
Deep Dive B walks a naive Dockerfile (moving base tag, everything copied in, an API key in an environment variable, running as root) through four fixes ([[source-ddb-devsecops-containers-cicd]] [4:05]):
1. **Minimal base, pinned by digest.** The vulnerability count drops sharply.
2. **Multi-stage build.** Compilers and caches stay in the build stage and never ship.
3. **No secrets in the image.** Inject keys at run time; deleting a key in a later step leaves it in the earlier layer.
4. **Non-root user** (UID 65532).
The figure's numbers are illustrative, "but the direction is real."

## Why it matters
Each layer is permanent, and anyone who can pull the image can read it ([[source-containers-cicd-brief]] §1.2). A smaller image also triages faster: often the quickest fix for a pile of findings is a newer minimal base ([[image-scanning-and-sbom]]).

## How it works
The reference Dockerfile ([[source-ddb-devsecops-containers-cicd]] [4:51]; [[source-containers-cicd-brief]] §2.4):
- Build stage `FROM <builder>@sha256:<digest> AS build`; `pip install --require-hashes` (hash-checked requirements block a tampered dependency); copy source.
- Runtime stage from a minimal image with no shell and no pip, also digest-pinned; `COPY --from=build` only the venv and source; `USER 65532`; start the server.
- No API keys anywhere; they arrive at run time ([[secrets-management]]).
- `sha256:<digest>` is a placeholder for the real digest.

Full checklist, mapped to NIST SP 800-190 ([[source-containers-cicd-brief]] §2.3):

| Control | How |
|---|---|
| Minimal/distroless base | DHI, Chainguard, distroless, `ubi-micro` |
| Multi-stage build | `FROM ... AS build`, `COPY --from=build` |
| Pin by digest | Renovate/Dependabot keep digests current |
| Non-root | `USER 65532`; K8s `runAsNonRoot: true` |
| Read-only root FS | `readOnlyRootFilesystem: true` + `emptyDir` for `/tmp` |
| Drop capabilities | `drop: ["ALL"]`, `allowPrivilegeEscalation: false` |
| Seccomp | `RuntimeDefault` |
| No secrets in images | BuildKit `--mount=type=secret` for build-time secrets |
| `.dockerignore` | `.env*`, `.git`, `*.pem`, `secrets/` |
| OCI labels | `org.opencontainers.image.source`, `.revision` |
| Pod Security Standards | namespace `enforce: restricted` |

## In practice
- Deploy Kubernetes workloads by digest with `automountServiceAccountToken: false`, resource limits, and secrets from External Secrets Operator ([[source-containers-cicd-brief]] §2.5).
- MCP servers get the same treatment: containerize (no `npx some-server@latest` at runtime), pin by digest, non-root, read-only FS, no service-account token ([[source-containers-cicd-brief]] §6.3; [[building-an-mcp-server]]).
- Choosing the base: see [[container-base-image-options]]. Chainguard's free tier is `:latest` only, so production government systems should use a paid tier, DHI, Iron Bank or UBI, and always pin the digest.

> [!warning] Hardening does not make a container a VM
> Containers share the host kernel. Agent-written or untrusted code needs gVisor, Firecracker or Kata plus minimal egress ([[source-containers-cicd-brief]] §11.3).

## See also
[[containerization]] · [[image-scanning-and-sbom]] · [[devsecops-pipeline]]
