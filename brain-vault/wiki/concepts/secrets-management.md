---
type: concept
summary: Where API keys and other secrets belong for AI workloads: in a secrets manager with workload identity, injected at run time, rotated and audited, never in images, repos, prompts or logs.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]", "[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]"]
related: ["[[container-hardening]]", "[[containerization]]", "[[devsecops-pipeline]]", "[[apis-and-endpoints]]", "[[ai-governance-and-controls]]", "[[image-scanning-and-sbom]]"]
aliases: [API keys, secrets, Vault, OIDC workload identity]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Secrets management

**TL;DR:** Keep API keys in an approved secrets store, injected at run time; never in code, prompts, images or logs; rotate on a schedule ([[source-ai-training-guide]] §4.1 operational controls). Deep Dive B compresses it: "Never in the image. Never in the repo. Injected at run time."

## What it is
**Wrong places** ([[source-ddb-devsecops-containers-cicd]] [5:59]): an image layer, the git repo, a CI log, a baked-in `.env` file. Anyone who can pull the image or read the repo or log has the key.

**Right path:** the key lives in a secrets manager (Vault or its open-source fork OpenBao, AWS Secrets Manager, Azure Key Vault, Google Secret Manager) -> **workload identity** via OIDC gives short-lived credentials that expire on their own -> the secret is injected into the container at run time -> the app uses it to call the LLM API. Rotate to version two with no rebuild; every read lands in the audit log.

## Why it matters
"The key was in the script" is the first problem that starts the day code calls the model: a pasted key ends up in the code, the repository and the logs ([[source-s5-apis-endpoints-and-containers]] [0:46]). Keys and network are job four of the six jobs your code takes over from the chat app, and the key landing from the secrets store is the first of the four run controls ([[source-s5-apis-endpoints-and-containers]] [1:43], [3:30]). Layers are permanent: a key added in one step and deleted in the next is still extractable, so rotate it immediately and rebuild ([[source-containers-cicd-brief]] §9.2).

## How it works
Tools ([[source-containers-cicd-brief]] §6.4):

| Tool | Notes |
|---|---|
| HashiCorp Vault (now IBM) / OpenBao | Dynamic secrets, leases, Kubernetes auth, Agent/CSI injection |
| AWS / Azure / Google secret managers | Cloud-native; GovCloud and Azure Gov regions |
| External Secrets Operator v1.3.x | Syncs the above into Kubernetes Secrets (paused Aug 2025, resumed by 2026) |
| Secrets Store CSI Driver | Mounts secrets as files without K8s Secret objects |
| CI OIDC federation | GitHub/GitLab OIDC -> cloud role; no long-lived cloud keys in CI |

For build-time secrets, use BuildKit `--mount=type=secret` so nothing lands in a layer ([[source-containers-cicd-brief]] §2.3).

## In practice
- **One key per service** (and environment), provider-side **spending limits**, and **push protection** so a key is blocked before it reaches the repo; GitHub recognizes major LLM provider key formats ([[source-ddb-devsecops-containers-cicd]] [5:59]; [[source-containers-cicd-brief]] §6.4).
- **Rotate after any CI compromise.** The March 2026 Trivy-action attack harvested CI secrets.
- **Evals** get a separate low-quota, eval-only key in a protected CI environment.
- **Detect leaks** with Gitleaks, TruffleHog (verifies whether a key is live) and Trivy's secret scanner ([[image-scanning-and-sbom]]).
- Keep production keys off laptops ([[source-ddb-devsecops-containers-cicd]] [3:06]); training sandboxes use training keys with low limits ([[source-s5-apis-endpoints-and-containers]] [5:46]).

> [!warning] Kubernetes Secrets are not encrypted by default
> They are base64-encoded in etcd unless encryption at rest is configured. Use an external secret manager plus etcd encryption ([[source-containers-cicd-brief]] §9.3).

## See also
[[container-hardening]] · [[devsecops-pipeline]] · [[ai-governance-and-controls]] · [[apis-and-endpoints]]
