---
type: concept
summary: Why every harness and model-calling workflow runs sealed in a container image identified by digest, what a container allows and blocks, and where containers run.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]", "[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]"]
related: ["[[container-hardening]]", "[[container-base-image-options]]", "[[devsecops-pipeline]]", "[[egress-control-and-firewalls]]", "[[secrets-management]]", "[[image-signing-and-provenance]]", "[[agnostic-ai-platform]]", "[[apis-and-endpoints]]", "[[ai-harness]]", "[[prompt-injection]]"]
aliases: [containers, Docker, Podman, container image]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Containerization

**TL;DR:** Any harness, and any workflow that calls a model API, runs in a container (Docker or Podman) inside the approved environment; it is the one rule for every stage after chat ([[source-ai-training-guide]] §3.2). A container image is a sealed box built once and identified by its digest, so the same reviewed, scanned bytes run everywhere and get authorized once.

## What it is
- **Image:** a sealed box holding your code, the runtime and libraries, built once and never changed. Each filesystem-changing Dockerfile line makes a **layer**; layers stack into the image ([[source-ddb-devsecops-containers-cicd]] [2:18]).
- **Digest:** a `sha256:` fingerprint of the image's exact bytes, its true identity. A **tag** like `latest` is a movable label. "A tag can move. A digest can't."
- **Container:** the image running; many identical containers can run from one image. **Registry:** the warehouse (Docker Hub, GHCR, ECR, Harbor, Iron Bank) ([[source-containers-cicd-brief]] §1).
- Containers share the host kernel (namespaces, cgroups), unlike VMs. For untrusted or agent-written code use a sandboxed runtime: gVisor, Firecracker or Kata Containers ([[source-containers-cicd-brief]] §1.2, §11.3).

## Why it matters
The guide lists four things a container gives AI work ([[source-ai-training-guide]] §3.2):

| Gives you | Why it matters |
|---|---|
| Pinned dependencies | The code and libraries that were reviewed are the ones that run |
| Isolation from the host | A hijacked model or bad script cannot reach other apps or files |
| Network limited to approved endpoints | Injected instructions have nowhere to send data |
| One defined artifact | Assessors scan, authorize and redeploy the same image, which faster ATOs depend on |

It also kills "it worked on my laptop": staging and production run the same box ([[source-ddb-devsecops-containers-cicd]] [0:56]). Containers are foundation 2 of the [[agnostic-ai-platform]]: the authorization attaches to the image, not the model.

## How it works
Session 5 shows what sits inside: the exact reviewed libraries, your code and saved prompt, and a key injected at run time. There is one way out, to the approved model endpoint; other websites and the host's files are blocked ([[source-s5-apis-endpoints-and-containers]] [2:57]). That ties containers to [[secrets-management]], [[egress-control-and-firewalls]] and defense against [[prompt-injection]].

**Where it runs** ([[source-ddb-devsecops-containers-cicd]] [3:06]; [[source-containers-cicd-brief]] §11): laptop (Docker Desktop, Podman; keep production keys off it), single server (you patch OS, engine, host firewall), serverless containers (Fargate, Cloud Run, Azure Container Apps; provider patches servers), Kubernetes (EKS, AKS, GKE, OpenShift; you own workloads, network and admission policy), edge or air-gapped (k3s plus a registry mirror; you own everything). Same image everywhere; who patches what changes. Your image, code, keys and network rules are always yours.

## In practice
- Build images through the [[devsecops-pipeline]], harden them ([[container-hardening]]), pick a base from [[container-base-image-options]], and deploy by digest after signing ([[image-signing-and-provenance]]).
- Rule of thumb: trusted, reviewed code -> hardened container; untrusted or agent-generated code -> sandboxed runtime and no egress beyond what the task needs ([[source-containers-cicd-brief]] §11.3).
- Exception: a hosted low-code platform cannot be containerized by the team; its own authorization stands in ([[source-ai-training-guide]] §3.2).
- Facilitators: build a Stage 2 sandbox once from a pre-scanned base image with low-limit training keys ([[source-s5-apis-endpoints-and-containers]] [5:46]).

## See also
[[apis-and-endpoints]] · [[ai-harness]] · [[building-an-mcp-server]] · [[ai-governance-and-controls]]
