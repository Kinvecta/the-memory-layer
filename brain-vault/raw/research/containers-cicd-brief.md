# Source Brief: Containers, Image Scanning and the CI/CD Pipeline for AI Workloads

**Prepared for:** 90-minute train-the-trainer session (deck + facilitator guide + ~8-min narrated video)
**Audience:** Mixed technical / non-technical staff at government, DoD and regulated organizations
**Scope:** AI workflows, MCP servers, and agent harnesses that call LLM APIs, packaged as containers and shipped through a CI/CD pipeline
**Currency:** Researched and version-checked on 20 October 2026. Items that change often (tool versions, federal policy) were checked against live sources this session. Anything not re-verified is flagged **[UNVERIFIED]**. Tool versions were pulled from the Go module proxy, PyPI and npm on 20 Oct 2026 [55].


> **General framing (added 21 Oct 2026):** This training is **general DevSecOps best practice** for anyone who builds or runs AI workloads in containers, in any organization. The government and regulated items in section 7 are optional context for audiences that need them; the core lessons (pin, scan, sign, ship the same digest, default-deny networking) apply everywhere. Sections 11 (where containers run) and 12 (firewalls and network controls) were added at the trainer's request.

---

## 0. Ten things a trainer must get right (October 2026)

1. **The federal "secure software attestation" mandate is gone.** OMB M-26-05 (23 Jan 2026) rescinded M-22-18 and M-23-16. Agencies now set risk-based software assurance policies. The CISA attestation form and SBOMs are optional contract tools, not a government-wide requirement [40].
2. **NIST SSDF is being updated.** SP 800-218 v1.1 (Feb 2022) is still the final version. **SSDF v1.2 (SP 800-218 Rev. 1)** was released as a draft on 17 Dec 2025 under EO 14306, with comments closing 30 Jan 2026. As of 20 Oct 2026, NIST's SSDF page still lists v1.2 as a draft, even though EO 14306 asked for a final version about 120 days after the draft [36][37][39]. SP 800-218A (the generative-AI profile) has been final since 26 Jul 2024 [38].
3. **CISA released "2026 Minimum Elements for an SBOM"** in late July 2026. It replaces the 2021 NTIA baseline and adds component hash, license, SBOM tool name and version, generation context, and an author signature. It explicitly covers AI and SaaS [41]. A separate CISA + G7 "SBOM for AI – Minimum Elements" came out on 13 May 2026 [42].
4. **DoD is moving from point-in-time RMF to continuous authorization.** The DoD CIO's **Cybersecurity Risk Management Construct (CSRMC)**, published 24 Sep 2025, has five phases (Design, Build, Test, Onboard, Operations) and lists cATO, DevSecOps, automation and inheritance among its tenets [43]. The **Software Fast Track (SWFT)** initiative went from pilot (2025) to a standing program in 2026. It centers on an SBOM clearinghouse, third-party assessment against SSDF, and continuous ATO [45].
5. **Your security scanner can be the attack vector.** In March 2026 the "TeamPCP" actor force-pushed 75+ tags of `aquasecurity/trivy-action` and all 7 tags of `setup-trivy`, and published a malicious Trivy v0.69.4 binary. The goal was stealing CI secrets [9]. Lesson: **pin GitHub Actions to full commit SHAs.** GitHub org policy can now enforce SHA pinning [10].
6. **Docker Hardened Images (DHI) became free and open source (Apache 2.0) on 17 Dec 2025:** more than 1,000 images on Debian and Alpine bases, each with an SBOM and SLSA Build L3 provenance. FIPS/STIG variants and SLA-backed patching remain in the paid Enterprise tier [3].
7. **Bitnami free images are gone.** Broadcom moved versioned Bitnami images behind a paid "Bitnami Secure Images" subscription and deleted the public catalog on 29 Sep 2025. Many Helm charts and Dockerfiles that referenced `bitnami/*` broke or now point at the unsupported `bitnamilegacy` [6].
8. **Market consolidation (know the new names):** tfsec is folded into Trivy [11]. Prisma Cloud became **Cortex Cloud** (Feb 2025) [24]. Google closed its Wiz acquisition on 11 Mar 2026 [25]. Snyk bought Invariant Labs, and `mcp-scan` is now **`snyk-agent-scan`** [26]. Palo Alto Networks closed its Protect AI acquisition (ModelScan's sponsor) on 22 Jul 2025, and the technology folds into Prisma AIRS [27]. OpenAI announced it would acquire Promptfoo on 9 Mar 2026 [32]. Gitleaks' original author launched **Betterleaks** (MIT) in March 2026 [22].
9. **Cosign v3 (Oct 2025)** makes the Sigstore "bundle" format, trusted-root and signing-config the defaults. Older flags are slated for removal in v4. The current release is v3.1.4 [12][55].
10. **The OWASP Top 10 for Agentic Applications (2026)** was released 9 Dec 2025. ASI04 "Agentic Supply Chain Vulnerabilities" and ASI05 "Unexpected Code Execution" map directly to this session [30].

---

## 1. Containers explained

### 1.1 Plain-language version (for non-technical staff)

- A **container image** is a sealed, labeled shipping box. It holds your application and everything it needs to run: the code, the Python runtime, the libraries, and the config defaults. It is built once and never changes.
- A **container** is that box opened and running on a computer. You can run many identical containers from one image.
- A **registry** is the warehouse where boxes are stored and checked out. Examples are Docker Hub, GitHub Container Registry, AWS ECR, Harbor, and Iron Bank's registry for DoD.
- A **Dockerfile** is the packing list and assembly instructions for the box.
- **Why it matters for AI:** an agent or MCP server that "works on my laptop" will behave the same way in staging and production, because the box is the same box. Security teams can inspect the box once, approve it, and approve the identical box again later. That idea, "one scanned image, authorized and redeployed," is the hook for the whole session.

### 1.2 Technical detail

| Concept | What it is | Key facts |
|---|---|---|
| **Image** | An immutable, content-addressed bundle: a manifest, a config JSON, and an ordered list of filesystem **layers** (tar archives) | Identified by **digest** (`sha256:...`). A tag like `:latest` or `:1.4` is a movable pointer, and the digest is the true identity. |
| **Layer** | Each filesystem-changing Dockerfile instruction (`RUN`, `COPY`, `ADD`) creates a layer | Layers are cached and shared between images. Deleting a file in a later layer does **not** remove it from earlier layers. This is why secrets "deleted" in a later step still leak. |
| **Container** | A running process (or group of processes) isolated using Linux kernel features: **namespaces** (what it can see), **cgroups** (what it can use), **capabilities**, seccomp, and SELinux/AppArmor | Shares the host kernel. |
| **Registry** | Server implementing the OCI Distribution API: push, pull, list tags, and (since OCI 1.1) **referrers** for attaching signatures/SBOMs to an image | Examples: Docker Hub, GHCR, ECR, ACR, GAR/Artifact Registry, Harbor, Quay, JFrog Artifactory, Iron Bank (registry1.dso.mil). |
| **OCI** | Open Container Initiative (Linux Foundation) standards | **Image Spec** v1.1.1, **Runtime Spec** v1.3.0, **Distribution Spec** v1.1.1 are the latest tagged releases [1][55]. OCI 1.1 added the `artifactType` and `subject` fields and the referrers API, which is how signatures, SBOMs and attestations attach to images. |

**Container vs VM**

| | Virtual machine | Container |
|---|---|---|
| Isolation boundary | Hypervisor; each VM has its own kernel | Shared host kernel; namespaces/cgroups |
| Size / start time | GBs; tens of seconds to minutes | MBs; milliseconds to seconds |
| Attack surface | Smaller shared surface (hypervisor) | Kernel is shared, so a kernel escape affects all containers on the host |
| Typical use | Whole OS workloads, strong multi-tenancy | Microservices, agents, MCP servers, CI jobs |
| Hybrids | — | gVisor, Kata Containers, and Firecracker microVMs give container ergonomics with VM-like isolation. These are useful for running **untrusted, agent-generated code**. |

**Runtimes**

- **Docker Engine / Docker Desktop:** developer-facing build-and-run tool. It uses containerd underneath.
- **containerd** (CNCF graduated): the industry-standard runtime daemon, current v2.4.2 [55]. It is the default runtime on most Kubernetes distributions.
- **CRI-O:** the Kubernetes-only runtime used by OpenShift.
- **Podman** (Red Hat): daemonless and rootless by default, with a Docker-compatible CLI. v6.x is current (v6.1.4) and v5.8.x is still maintained [55]. It is popular in government because it is rootless and RHEL-native.
- **runc / crun:** low-level OCI runtimes that actually create the container process.
- **Buildah / BuildKit / Kaniko-style builders:** build images without a privileged Docker daemon, which matters in CI.

**Orchestration (high level)**

- **Kubernetes:** the de facto orchestrator. Supported minors as of Oct 2026 are 1.37, 1.36 and 1.35, with 1.34 reaching end of life on 27 Oct 2026 [47]. It schedules containers into Pods, restarts them, scales them, and wires networking, secrets and policy.
- **Red Hat OpenShift:** enterprise Kubernetes with stricter defaults (Security Context Constraints, non-root by default). It is common in DoD and civilian agencies.
- **Managed Kubernetes:** EKS (AWS), AKS (Azure), GKE (Google). All three have GovCloud/Government regions or offerings.
- **Simpler services:** AWS ECS/Fargate, Azure Container Apps, Google Cloud Run. Fine for a single agent service.
- **DoD:** Platform One's **Big Bang** and Unicorn Delivery Service (UDS) package hardened Kubernetes stacks for DoD software factories [5] **[UNVERIFIED for 2026 naming]**.

---

## 2. Hardening the image

### 2.1 Plain language

A hardened image is a box packed with **only** what the application needs: no shell, no package manager, no compilers, no leftover tools. Fewer items in the box means fewer things that can have vulnerabilities and fewer tools an attacker can use if they get in.

### 2.2 Base image options (Oct 2026)

| Base image family | Who | Cost / license | Notes |
|---|---|---|---|
| **Docker Hardened Images (DHI)** | Docker | **Free, Apache 2.0** (since 17 Dec 2025). DHI Enterprise is paid. | 1,000+ images on Debian/Alpine. Each ships an SBOM, public CVE data, SLSA Build L3 provenance and signatures. Enterprise adds FIPS/STIG-ready images, a <7-day critical CVE SLA, and Extended Lifecycle Support. Includes hardened **MCP server** images [3]. |
| **Chainguard Containers** | Chainguard | Free tier: a limited set with `:latest` tags only and no SLA. Paid per-image or catalog (from ~$19K/yr for a team of 10, per its pricing page) | Built on Wolfi; minimal, frequently rebuilt, near-zero CVEs; FIPS and STIG-hardened variants in paid tiers. **Chainguard Libraries** (rebuilt PyPI/Maven/npm packages) are paid [4]. |
| **Google distroless** | Google (OSS) | Free | Language-runtime-only images (`static`, `base`, `cc`, `python3`, `java`, `nodejs`) with no shell; `:nonroot` variants available [8] **[UNVERIFIED: current Debian base tag]**. |
| **Red Hat UBI** (8/9/10; `ubi`, `ubi-minimal`, `ubi-micro`) | Red Hat | Free to redistribute | RHEL-based and supported on OpenShift. Many Iron Bank images rebase on UBI. UBI 10 is published [7]. |
| **Iron Bank** | DoD Platform One | Free to DoD/public (registry1.dso.mil; account required) | DoD's repository of hardened containers. Images are evaluated against **Acceptance Baseline Criteria (ABC)** and get an **Overall Risk Assessment (ORA)** score. Images must rebase on an Iron Bank base image and be built offline. Continuous monitoring rescans every 12 hours. Iron Bank approval is **not** an ATO; the program still decides [5]. |
| **Bitnami** | Broadcom | **Paid** (Bitnami Secure Images) since Sep 2025; `bitnamisecure` free `:latest` is for development only; `bitnamilegacy` is unpatched | Audit Helm charts for `bitnami/` references [6]. |
| **Alpine / Debian-slim / Ubuntu** | Community / Canonical | Free | Fine starting points but not "hardened" by default. Canonical sells hardened/"chiseled" Ubuntu images **[UNVERIFIED pricing]**. |

### 2.3 Hardening checklist (maps to NIST SP 800-190 countermeasures [2])

| Control | Why | How |
|---|---|---|
| **Minimal / distroless base** | Removes shells, package managers and extra libraries, shrinking CVE count and attacker tooling | DHI, Chainguard, distroless, or `ubi-micro` |
| **Multi-stage build** | Build tools (gcc, pip caches, git) stay in the builder stage and never ship | `FROM ... AS build` then `COPY --from=build` |
| **Pin by digest** | Tags move; digests don't. This makes builds reproducible and stops silent base-image swaps | `FROM cgr.dev/chainguard/python@sha256:...`. Renovate/Dependabot can keep digests updated. |
| **Non-root user** | Limits the damage of a container escape or RCE | `USER 65532` / `nonroot`; K8s `runAsNonRoot: true` |
| **Read-only root filesystem** | Stops malware from writing binaries and stops tampering | `readOnlyRootFilesystem: true` plus an `emptyDir` for `/tmp` |
| **Drop all Linux capabilities** | Removes privileged kernel operations | `capabilities: {drop: ["ALL"]}`, `allowPrivilegeEscalation: false` |
| **Seccomp `RuntimeDefault`** | Blocks dangerous syscalls | Pod `seccompProfile: {type: RuntimeDefault}` |
| **No secrets in images** | Layers are permanent and anyone who can pull the image can read them | Use BuildKit `--mount=type=secret` for build-time secrets; inject runtime secrets from Vault, a cloud secret manager, or External Secrets |
| **`.dockerignore`** | Prevents `.env`, `.git`, keys and notebooks from being copied in | Add `.env*`, `.git`, `*.pem`, `secrets/` |
| **Labels / metadata** | Traceability back to the source commit | OCI labels `org.opencontainers.image.source`, `.revision`, `.version` (docker/metadata-action generates these) |
| **Pod Security Standards "restricted"** | Cluster-level guardrail | Namespace label `pod-security.kubernetes.io/enforce: restricted` [60] |

### 2.4 Example: hardened Dockerfile for a Python LLM agent / MCP server

```dockerfile
# syntax=docker/dockerfile:1
# ---------- Build stage: has pip, compilers, etc. ----------
FROM cgr.dev/chainguard/python:latest-dev@sha256:<builder-digest> AS build
WORKDIR /app
COPY requirements.txt .
# Hash-pinned requirements (pip-compile --generate-hashes) block dependency substitution
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --require-hashes -r requirements.txt
COPY src/ ./src/

# ---------- Runtime stage: no shell, no pip, non-root ----------
FROM cgr.dev/chainguard/python:latest@sha256:<runtime-digest>
WORKDIR /app
COPY --from=build /app/venv /app/venv
COPY --from=build /app/src  /app/src
ENV PATH="/app/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# Chainguard/distroless runtime images already default to a non-root UID (65532)
USER 65532
EXPOSE 8080
ENTRYPOINT ["python", "-m", "src.server"]
# NOTE: No API keys here. ANTHROPIC_API_KEY / OPENAI_API_KEY etc. are injected at runtime.
```

**Trainer note:** Chainguard's free tier only offers `:latest`. For a production gov system, use a paid tier, DHI, Iron Bank or UBI, and **always pin the digest**.

### 2.5 Example: Kubernetes securityContext

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: rag-agent, namespace: ai-agents }
spec:
  replicas: 2
  selector: { matchLabels: { app: rag-agent } }
  template:
    metadata: { labels: { app: rag-agent } }
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 65532
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: agent
          image: ghcr.io/example/rag-agent@sha256:<digest>   # deploy by DIGEST, not tag
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
          resources:
            limits: { cpu: "1", memory: "1Gi" }
          envFrom:
            - secretRef: { name: llm-api-keys }   # synced by External Secrets Operator
          volumeMounts: [{ name: tmp, mountPath: /tmp }]
      volumes: [{ name: tmp, emptyDir: {} }]
```

---

## 3. Scanning: what it means and which tools do it

### 3.1 Plain language

"Scanning" means automatically inspecting code, the box, and the config for known problems before anything ships. Think of airport security for software: different machines look for different things (metal, liquids, explosives). No single scanner catches everything, so pipelines run several.

### 3.2 Vulnerability vocabulary

| Term | Meaning | Trainer framing |
|---|---|---|
| **CVE** | Common Vulnerabilities and Exposures: a unique ID for a publicly known flaw (e.g., CVE-2026-33634, the Trivy compromise) | The "license plate" for a bug |
| **CVSS** | Common Vulnerability Scoring System (v3.1 widely used; **v4.0** current). A 0–10 severity score | How bad it *could* be |
| **EPSS** | FIRST's Exploit Prediction Scoring System: the probability (0–1) that a CVE will be exploited in the wild in the next 30 days, published daily. **EPSS v4** shipped in March 2025 [49] | How likely it is to be used against you |
| **KEV** | CISA's Known Exploited Vulnerabilities catalog. Under BOD 22-01, federal civilian agencies must remediate KEV entries by the listed due dates [50] | It is *being* exploited, so fix it now |
| **VEX** | Vulnerability Exploitability eXchange: a machine-readable statement that "this CVE is not exploitable in our product because..." (OpenVEX, CycloneDX VEX, CSAF VEX) | Cuts false positives; Trivy and Grype can consume VEX |
| **Fixed / unfixed** | Whether an upstream patch exists | Gates usually fail only on *fixable* criticals/highs |

**Prioritization recipe for the deck:** treat KEV first, then high EPSS, then high CVSS, then the rest, and focus on what is fixable and reachable. EPSS research shows that patching everything rated CVSS 7+ is a lot of effort for little efficiency compared with EPSS-driven prioritization [49].

**Ecosystem caveat:** The CVE program nearly lost funding in April 2025. CISA extended MITRE's contract roughly 11 months, and in Sept 2025 published a "Quality Era" roadmap [51]. **[UNVERIFIED: contract status after March 2026. Check cve.org before delivery.]** NVD enrichment backlogs since 2024 are why scanners increasingly pull from GitHub Advisory DB, OSV and vendor feeds as well as NVD.

### 3.3 Scan categories

| Category | Question it answers | Where it runs in the pipeline |
|---|---|---|
| **Vulnerability (image/OS/package) scanning** | Does the image contain packages with known CVEs? | After build; continuously in the registry and at runtime |
| **SCA / dependency scanning** | Do my declared libraries (requirements.txt, package.json, go.mod) have CVEs, or are they malicious or outdated? | PR and build |
| **SBOM generation** | What exactly is inside? (inventory) | Build; stored and attested next to the image |
| **Secret scanning** | Did anyone commit an API key, token or password? | Pre-commit, push, PR, full-history scans |
| **Misconfiguration / IaC scanning** | Are the Dockerfile, Kubernetes YAML, Helm, Terraform or CloudFormation insecure (root, privileged, public S3)? | PR and build |
| **SAST** | Does *our* source code have insecure patterns (injection, unsafe deserialization, SSRF)? | PR |
| **DAST** | Does the *running* app respond insecurely to attacks? | Staging, after deploy |
| **License scanning** | Are we shipping GPL/AGPL or other incompatible licenses? | Build (from the SBOM) |
| **Malware scanning** | Are there known-malicious files, typosquatted packages, or backdoors? | Build and registry |
| **Model / artifact scanning (AI)** | Do model files (pickle, etc.) contain executable payloads? | When models are pulled into the build or registry |
| **Agent / MCP scanning (AI)** | Do MCP servers or agent skills contain tool-poisoning or prompt-injection payloads? | PR and periodic |

### 3.4 Tool reference table

OSS = open source; Comm = commercial. Versions as of 20 Oct 2026 [55] unless noted.

| Tool | Category | License | What it does | Example command |
|---|---|---|---|---|
| **Trivy** (Aqua) v0.76.0 | Vuln, SBOM, secrets, misconfig/IaC, license, K8s | OSS (Apache-2.0) | All-in-one scanner for images, filesystems, repos, Kubernetes and IaC. **Absorbed tfsec.** | `trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 IMAGE` / `trivy fs .` / `trivy config ./k8s` / `trivy image --format cyclonedx -o sbom.json IMAGE` |
| **Grype** (Anchore) v0.121.0 | Vuln | OSS | Image/dir/SBOM vulnerability scanner; reads Syft SBOMs and supports VEX | `grype IMAGE --fail-on high` / `grype sbom:./sbom.cdx.json` |
| **Syft** (Anchore) v1.55.0 | SBOM | OSS | Generates SPDX/CycloneDX SBOMs from images or directories | `syft IMAGE -o cyclonedx-json=sbom.cdx.json -o spdx-json=sbom.spdx.json` |
| **Docker Scout** (CLI v1.26.0) | Vuln, SBOM, policy, base-image recommendations | Comm (free tier) | Built into Docker Desktop/Hub; suggests base-image upgrades | `docker scout cves IMAGE` / `docker scout recommendations IMAGE` / `docker scout quickview` |
| **Snyk** (Open Source, Container, Code, IaC; Agent Scan) | SCA, container, SAST, IaC, AI agents | Comm (free tier) | Developer-first platform with fix PRs. Acquired Invariant Labs (Jun 2025). Agent Security launched 2026 | `snyk test` / `snyk container test IMAGE` / `snyk code test` / `snyk iac test` |
| **Anchore Enterprise** | SBOM management, vuln, policy, compliance | Comm | Built on Syft/Grype; has FedRAMP/DoD policy packs including NIST 800-190 and DISA STIG checks | `anchorectl image add IMAGE --wait` / `anchorectl image check IMAGE` |
| **Cortex Cloud** (formerly **Prisma Cloud**, originally **Twistlock**) | CNAPP: image, registry, runtime, CSPM | Comm | Palo Alto merged Prisma Cloud and Cortex CDR into Cortex Cloud (announced Feb 2025) [24]. `twistcli` is still referenced in docs | `twistcli images scan --address URL IMAGE` **[UNVERIFIED current CLI name]** |
| **Aqua Platform** | CNAPP: image, runtime, supply chain | Comm | Commercial big sibling of Trivy. Aqua says its commercial products were not affected by the March 2026 Trivy OSS compromise [9] | via platform / scanner CLI |
| **Wiz** (now Google) | CNAPP, agentless scanning, Wiz Code, Wiz CLI | Comm | Google completed the $32B acquisition on 11 Mar 2026 [25] | `wizcli docker scan --image IMAGE` **[UNVERIFIED current syntax]** |
| **Clair** (Red Hat / Quay) | Vuln (registry-side) | OSS | Static analysis engine behind Quay's scanning | Runs as a service; via `clairctl` |
| **Dependabot** | SCA + automated update PRs | Free on GitHub | Alerts and PRs for vulnerable or outdated dependencies, **including Dockerfile base images and GitHub Actions** | `.github/dependabot.yml` with `package-ecosystem: docker`, `pip`, `github-actions` |
| **Renovate** (Mend) | Automated dependency updates | OSS (+ hosted) | More configurable than Dependabot; can **pin and update image digests and Action SHAs** | `renovate.json` with `"extends": ["config:recommended", "helpers:pinGitHubActionDigests", "docker:pinDigests"]` |
| **OWASP Dependency-Check** v12.x | SCA | OSS | Matches dependencies to CVEs via CPE (NVD). Needs a free NVD API key for usable speed [23] | `dependency-check.sh --project app --scan . --nvdApiKey $KEY --failOnCVSS 7` |
| **Semgrep** CE v1.182.0 / AppSec Platform | SAST, secrets, supply chain | OSS engine (LGPL) + Comm rules/platform | Pattern-based multi-language SAST; fast; custom rules in YAML. Recommended CI: `semgrep/semgrep` container [20] | `semgrep scan --config p/python --config p/owasp-top-ten --error` / `semgrep ci` (platform) |
| **CodeQL** (GitHub) | SAST (semantic, dataflow) | Free for public repos; GitHub Advanced Security (Code Security) for private | Deep dataflow queries; results go to GitHub code scanning | `github/codeql-action/init` + `analyze`; `codeql database analyze` |
| **SonarQube** (Server / Cloud / Community Build) | SAST, code quality, quality gates | Community Build OSS; Server/Cloud Comm | Renamed in late 2024: SonarQube Server, SonarQube Cloud, SonarQube Community Build (replaces "Community Edition") [57] | `sonar-scanner -Dsonar.projectKey=app -Dsonar.qualitygate.wait=true` |
| **Checkov** (Palo Alto/Bridgecrew) v3.3.x | IaC/misconfig, secrets | OSS | Terraform, CloudFormation, K8s, Helm, Dockerfile, GitHub Actions | `checkov -d . --framework dockerfile,kubernetes,github_actions` |
| **tfsec** | IaC | OSS, **in maintenance; superseded by Trivy** | Last release v1.28.14 (May 2025) [55]. The migration guide points users to `trivy config` [11] | `trivy config ./terraform` (replacement) |
| **KICS** (Checkmarx) | IaC | OSS | 2,000+ IaC queries. **Its GitHub Action (`kics-github-action`) was also compromised in March 2026, per Wiz** [9] | `kics scan -p . --fail-on high` |
| **Gitleaks** v8.30.1 | Secrets | OSS (MIT); the GitHub Action needs a free license key for org repos [19] | Regex + entropy detection across git history | `gitleaks git . --redact --exit-code 1` (v8.19+ syntax; older: `gitleaks detect`) |
| **Betterleaks** (Aikido) | Secrets | OSS (MIT) | New successor from Gitleaks' author, launched Mar 2026 [22] | **[UNVERIFIED CLI syntax]** |
| **TruffleHog** v3.99.x | Secrets (with live **verification**) | OSS (AGPL) + Comm | 800+ detectors; checks whether found keys are live | `trufflehog git file://. --results=verified --fail` / `trufflehog docker --image IMAGE` |
| **GitHub secret scanning + push protection** | Secrets | Free for public repos; Secret Protection (paid) for private | Partner patterns (OpenAI, Anthropic, AWS, Azure and others) are revoked or notified automatically; **push protection blocks the push** [58] | Repo Settings → Code security → Secret Protection |
| **ZAP** (Zed Attack Proxy) | DAST | OSS (Apache-2.0); maintainers sponsored by Checkmarx since 2024 ("ZAP by Checkmarx") | Spider + passive/active scans of a running web app or API | `docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://staging.example` / `zap-api-scan.py -t openapi.json -f openapi` |
| **ClamAV** / YARA | Malware | OSS | Signature-based malware detection in image filesystems | `clamscan -r /extracted-rootfs` |
| **Socket**, **OSV-Scanner** (Google) | Malicious-package / SCA | Socket Comm (free tier); OSV-Scanner OSS | Socket flags typosquats and install-script malware; OSV-Scanner checks lockfiles against OSV.dev | `osv-scanner scan -r .` |
| **ModelScan** (Protect AI) v0.8.8 | AI model files | OSS (Apache-2.0) | Detects unsafe operations (code execution) in pickle, PyTorch, Keras/H5, TensorFlow SavedModel, etc. [28] | `modelscan -p ./models/` |
| **snyk-agent-scan** (formerly `mcp-scan`, Invariant Labs) v0.6.9 | MCP servers / agent skills | OSS (Apache-2.0); output marked experimental | Discovers local agent configs and MCP servers and scans tool descriptions for prompt injection and tool poisoning. **Sends tool metadata to Snyk's API for analysis** **[UNVERIFIED: confirm data flow before using on classified/CUI systems]** [26] | `uvx snyk-agent-scan@latest` (or `uvx mcp-scan@latest`, now a redirect) |
| **garak** (NVIDIA) v0.17.x | LLM red-team probes | OSS | Probes a model endpoint for jailbreaks, injection, leakage | `garak --model_type openai --model_name gpt-... --probes promptinject` |
| **Promptfoo** (OpenAI) v0.124.x | Evals + red teaming | OSS (MIT) **[UNVERIFIED post-acquisition license plans]** | YAML-defined test cases and assertions; CI-friendly | `npx promptfoo@0.124.1 eval -c promptfooconfig.yaml` |

**Deprecated / merged as of Oct 2026**

- **tfsec** → Trivy (`trivy config`) [11]
- **Twistlock** → Prisma Cloud → **Cortex Cloud** [24]
- **`mcp-scan`** → **`snyk-agent-scan`** (PyPI redirect package) [26]
- **`actions/attest-build-provenance`** → now a thin wrapper over **`actions/attest@v4`**; new work should use `actions/attest` [14]
- **SonarQube "Community Edition"** → "SonarQube Community Build" [57]
- **Bitnami public images** → paid Bitnami Secure Images / unsupported `bitnamilegacy` [6]
- **External Secrets Operator** paused releases in Aug 2025 for lack of maintainers. Development resumed with new maintainers by mid-2026 (current v1.3.x) [34][55]
- **Gitleaks** is still released (v8.30.1, Feb 2026), but its original author now builds **Betterleaks** [22]. Watch maintenance cadence.

---

## 4. Supply-chain integrity: signing, provenance, admission control, registries

### 4.1 Plain language

Scanning answers "is the box safe?" **Signing** answers "is this the *same* box we scanned, and did it really come from our factory?" It works like a tamper-evident seal plus a shipping manifest. **Admission control** is the guard at the loading dock who refuses any box without a valid seal.

### 4.2 Signing

| Tool | Model | Key facts |
|---|---|---|
| **Sigstore Cosign** v3.1.4 | **Keyless** (OIDC identity → short-lived Fulcio certificate → entry in the **Rekor** transparency log) or key-based (KMS/HSM/file) | v3 (Oct 2025) makes `--new-bundle-format`, `--trusted-root` and `--use-signing-config` defaults; legacy flags will be removed in v4 [12]. Signs **by digest**. Also attaches attestations (`cosign attest`). |
| **Notation** (Notary Project, CNCF) v1.3.2 | X.509 PKI; plugins for Azure Key Vault, AWS Signer, HashiCorp Vault | Common in Azure/AWS enterprise PKI environments; fits orgs that need CA-issued certificates rather than public transparency logs. Last release April 2025, so watch cadence [55]. |
| **GitHub Artifact Attestations** (`actions/attest@v4`) | Sigstore-based (public-good Sigstore for public repos; GitHub's instance for private) | Needs `id-token: write`, `attestations: write`, `artifact-metadata: write`. Verify with `gh attestation verify` [14]. |

**Air-gapped / classified note:** Public Sigstore (Fulcio/Rekor) needs internet. Disconnected enclaves typically run a **private Sigstore** deployment, use **key-based Cosign with an HSM/KMS**, or use **Notation with internal PKI**.

### 4.3 Provenance and attestations

- **in-toto:** a framework and attestation format. An *attestation* is a signed statement about an artifact: "this image was built from commit X by workflow Y," or "this SBOM describes digest Z," or "this image passed Trivy with 0 criticals."
- **SLSA** (Supply-chain Levels for Software Artifacts, OpenSSF). **v1.2 is the current approved spec** and adds a **Source track** alongside the **Build track** [13]:
  - **Build L1:** provenance exists (the platform generates it automatically).
  - **Build L2:** hosted build platform; provenance is **signed** by the platform, which protects against tampering after the build.
  - **Build L3:** hardened builds. Builds are isolated from one another and **signing secrets are inaccessible to user build steps**, which protects against tampering during the build, including by insiders [13].
  - GitHub-hosted runners with `actions/attest` or the SLSA GitHub generator are commonly used to reach Build L2/L3. **[Trainer caution: claiming L3 needs a review of the platform's isolation guarantees.]**
- **SBOM attestation:** attach the SBOM to the image digest as a signed attestation (`cosign attest --type cyclonedx`, or `actions/attest` with `sbom-path`).

**SBOM formats**

| Format | Steward | Current | Notes |
|---|---|---|---|
| **SPDX** | Linux Foundation; ISO/IEC 5962:2021 (v2.2.1) | SPDX 3.0.x adds AI and Dataset profiles **[UNVERIFIED: latest 3.x point release]** | Strong license-compliance heritage |
| **CycloneDX** | OWASP; **ECMA-424** | **v1.7** (21 Oct 2025): CBOM, citations, IP. v1.6 = ECMA-424 1st ed. (Jun 2024) [52] | Strong security heritage; supports ML-BOM, VEX and attestations |

CISA's 2026 Minimum Elements endorse neither format exclusively. Both support the new hash and license fields [41].

### 4.4 Admission control (enforcing "only signed, scanned images run")

| Tool | Status | Notes |
|---|---|---|
| **Kyverno** v1.19.x | **CNCF Graduated (24 Mar 2026)** [48] | Kubernetes-native YAML policies. `verifyImages` checks Cosign/Notation signatures and attestations, can **mutate tags to digests**, and can require "no critical vulns" attestations. Newer `ImageValidatingPolicy` CRDs use CEL **[UNVERIFIED: API version GA status]**. |
| **OPA Gatekeeper** v3.23.x | CNCF (OPA graduated) | Rego policies; signature verification via the external-data provider (e.g., Ratify). Kubernetes **ValidatingAdmissionPolicy** (CEL, built in) covers simple checks with no add-on. |
| **Sigstore policy-controller** v0.15.1 | Sigstore project | `ClusterImagePolicy` that requires keyless or key signatures and attestations |
| **Ratify** | CNCF Sandbox | Verifies Notation/Cosign signatures and SBOMs for Gatekeeper; used by AKS image integrity **[UNVERIFIED current status]** |

**Example Kyverno policy (classic `ClusterPolicy`)**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-signed-ai-images }
spec:
  validationFailureAction: Enforce
  webhookTimeoutSeconds: 30
  rules:
    - name: verify-cosign-keyless
      match: { any: [ { resources: { kinds: [Pod], namespaces: [ai-agents] } } ] }
      verifyImages:
        - imageReferences: ["ghcr.io/example/*"]
          mutateDigest: true          # rewrite tag -> digest
          verifyDigest: true
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/example/rag-agent/.github/workflows/release.yml@refs/heads/main"
                    rekor: { url: "https://rekor.sigstore.dev" }
          attestations:
            - type: https://cyclonedx.org/bom
              attestors:
                - entries:
                    - keyless:
                        issuer: "https://token.actions.githubusercontent.com"
                        subject: "https://github.com/example/rag-agent/.github/workflows/release.yml@refs/heads/main"
```

### 4.5 Private registries

| Registry | Type | Built-in scanning / signing |
|---|---|---|
| **Harbor** | OSS, CNCF Graduated, self-hosted | Trivy scanning built in; Cosign/Notation signature support; replication; **"prevent vulnerable images from running"** project policy; proxy cache. Good for air-gapped use. |
| **AWS ECR** | Cloud | Basic scanning (Clair-based/AWS-native) and Enhanced scanning (Amazon Inspector); signing via AWS Signer (Notation) |
| **Azure ACR** | Cloud | Defender for Cloud (Defender for Containers) scanning; Notation + Azure Key Vault signing |
| **Google Artifact Registry** | Cloud | Artifact Analysis on-push/continuous scanning; Binary Authorization for deploy-time policy |
| **JFrog Artifactory** (+ Xray) | Comm, cloud or self-hosted | Xray SCA/container scanning; remote repo can **proxy Iron Bank** |
| **Red Hat Quay** | Comm / OSS (project Quay) | Clair scanning; geo-replication; common with OpenShift |
| **GitHub Container Registry (GHCR)** | Cloud | Integrates with Actions OIDC, attestations, Dependabot |
| **Iron Bank (registry1.dso.mil)** | DoD | Source of hardened images. Proxy or mirror it into your program registry [5]. |

**Registry scanning matters because new CVEs appear after you ship.** An image that was clean on Monday can have a critical CVE by Friday. Registries and CNAPPs re-scan stored images continuously (Iron Bank: every 12 hours [5]). Feed the results back into the backlog and rebuild automatically.

---

## 5. The CI/CD pipeline end to end

### 5.1 Plain language

CI/CD is an **assembly line with inspection stations**. Every change goes down the same line. If any station finds a problem above the agreed threshold, the line stops ("breaks the build") and the change doesn't ship. Because every product goes through identical, logged inspections, approvers can trust the *line*, not just each product. That is the core idea behind continuous ATO.

### 5.2 Stages, gates and typical thresholds

| # | Stage | What happens | Typical gate (break-the-build) |
|---|---|---|---|
| 1 | **Commit** | Developer pushes to a branch; pre-commit hooks run Gitleaks/TruffleHog and linters | Any verified secret → block (GitHub push protection) |
| 2 | **PR review** | Human code review (CODEOWNERS); SAST (Semgrep/CodeQL); SCA (Dependabot/Snyk); IaC (Checkov/Trivy config); secrets | 2 approvals for prod paths; no new High/Critical SAST findings; branch protection |
| 3 | **Build** | Reproducible build on an ephemeral, hosted runner from a pinned, digest-referenced base; generate SBOM | Build must be hermetic (no ad-hoc downloads); Actions pinned by SHA |
| 4 | **Test + evals** | Unit/integration tests; **LLM evals** (golden set, red-team prompts, tool-use tests) against the **pinned model ID and prompt version** | Tests 100%; eval score ≥ baseline (e.g., ≥ 0.90 accuracy, 0 critical safety failures) |
| 5 | **Scan the image** | Trivy/Grype on the built image; license policy; ModelScan for model files; agent-scan on MCP configs | Fail on **fixable CRITICAL** (often also HIGH); fail on any **KEV**; fail on forbidden licenses (e.g., AGPL); secrets in layers = fail |
| 6 | **Sign + attest** | Cosign/Notation sign the **digest**; attach SBOM, provenance and scan-result attestations | Signing failure = fail |
| 7 | **Push to registry** | Push to a private registry (Harbor/ECR/ACR/GAR/Iron Bank mirror) | Registry policy blocks unsigned images |
| 8 | **Deploy to staging** | GitOps (Argo CD/Flux) syncs a manifest that references the **digest**; admission control verifies signature and attestations; DAST (ZAP) + smoke evals | Admission deny = no deploy; DAST High = fail |
| 9 | **Promote to prod** | **Same digest** promoted (no rebuild); change ticket auto-generated from pipeline evidence; optional manual approval (GitHub Environments) | Required reviewers for prod environment |
| 10 | **Runtime monitoring** | Falco/Tetragon runtime detections; registry rescans; OpenTelemetry traces of LLM/tool calls; audit logs; cost/token monitoring | New KEV in running image → auto-PR to rebuild; Falco critical → page |

**Exception handling:** Every "break-the-build" policy needs a documented, **time-boxed exception path**: a risk acceptance with an owner and an expiry, plus VEX statements for false positives. Otherwise teams just disable the scanner. Iron Bank's model of "justifications" for each finding is a good example [5].

### 5.3 CI/CD platforms

| Platform | Notes for gov/regulated |
|---|---|
| **GitHub Actions** | GitHub Enterprise Cloud has a FedRAMP-authorized offering **[UNVERIFIED current level]**. OIDC to cloud (no stored keys), artifact attestations, org-level SHA-pinning enforcement [10] |
| **GitLab CI/CD** | Very common in DoD (Platform One's Repo1 is GitLab). Built-in SAST/DAST/container/secret scanning templates (Ultimate tier); self-managed works air-gapped |
| **Jenkins** | Ubiquitous legacy; plugin-sprawl risk; harden with JCasC, ephemeral agents, plugin pinning |
| **Azure DevOps Pipelines** | Strong in Microsoft-centric agencies; Azure Government |
| **Tekton** (CD Foundation) + **Tekton Chains** | Kubernetes-native pipelines; Chains auto-signs task results and generates SLSA provenance; basis of OpenShift Pipelines |
| **Argo CD** v3.5.x (CNCF Graduated) / **Flux** v2.9.x (CNCF Graduated) | **GitOps**: the cluster pulls desired state from Git, which gives a full audit trail and drift detection. Flux can verify Cosign/Notation signatures on OCI artifacts natively [55] |

### 5.4 Example GitHub Actions workflow (LLM workflow container)

**Before using:** Replace every `@<SHA>` with the full 40-character commit SHA of the tag in the comment. Resolve them yourself from each action's Releases page, or let Renovate (`helpers:pinGitHubActionDigests`) or `pinact` do it. The SHAs are deliberately not filled in here because they could not be verified from this environment, and a wrong SHA is worse than none. Tags shown are the latest majors referenced in each action's README on 20 Oct 2026 [14][15][16][17][18][19][20][21].

```yaml
# .github/workflows/release.yml
name: build-scan-sign-push (LLM agent)

on:
  push:
    branches: [main]
  pull_request:

# Least privilege by default; jobs opt in to more.
permissions:
  contents: read

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}           # e.g. example/rag-agent

jobs:
  # ---------------------------------------------------------------
  # 1) Source-level checks: secrets, SAST, IaC/Dockerfile misconfig
  # ---------------------------------------------------------------
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>               # v6
        with: { fetch-depth: 0 }                   # full history for secret scanning
      - uses: gitleaks/gitleaks-action@<SHA>       # v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # required for org-owned repos

  sast:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep@sha256:<digest>       # pin the scanner image too
    steps:
      - uses: actions/checkout@<SHA>               # v6
      # Community Edition, explicit rulesets (no --config auto, which needs metrics on)
      - run: semgrep scan --config p/python --config p/owasp-top-ten --config p/secrets --error --sarif --output semgrep.sarif
      - uses: github/codeql-action/upload-sarif@<SHA>   # v4 [UNVERIFIED major]
        if: always()
        with: { sarif_file: semgrep.sarif }
    permissions:
      contents: read
      security-events: write

  iac:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>               # v6
      - name: Trivy config scan (Dockerfile, k8s manifests, Helm)
        uses: aquasecurity/trivy-action@<SHA>      # v0.36.0  (v0.35.0+ are post-incident safe)
        with:
          scan-type: config
          scan-ref: .
          severity: HIGH,CRITICAL
          exit-code: "1"

  # ---------------------------------------------------------------
  # 2) Unit tests + LLM evals (pinned model + pinned prompt version)
  # ---------------------------------------------------------------
  evals:
    runs-on: ubuntu-latest
    environment: evals                             # holds a low-quota, eval-only API key
    steps:
      - uses: actions/checkout@<SHA>               # v6
      - uses: actions/setup-python@<SHA>           # v6 [UNVERIFIED major]
        with: { python-version: "3.13" }
      - run: pip install --require-hashes -r requirements-dev.txt
      - run: pytest -q
      - name: Prompt/model regression evals (fails on any assertion failure)
        env:
          ANTHROPIC_API_KEY: ${{ secrets.EVAL_ANTHROPIC_API_KEY }}
          MODEL_ID: claude-sonnet-4-6             # pinned model ID, never an alias
          PROMPT_VERSION: v2026.10.1              # prompts are versioned files in the repo
        run: npx --yes promptfoo@0.124.1 eval -c evals/promptfooconfig.yaml --no-cache

  # ---------------------------------------------------------------
  # 3) Build -> scan image -> push -> SBOM -> sign -> attest
  # ---------------------------------------------------------------
  build:
    needs: [secrets, sast, iac, evals]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write            # push to GHCR
      id-token: write            # OIDC for keyless signing
      attestations: write        # GitHub artifact attestations
      artifact-metadata: write   # required by actions/attest@v4
      security-events: write     # upload SARIF
    steps:
      - uses: actions/checkout@<SHA>               # v6
      - uses: docker/setup-buildx-action@<SHA>     # v4

      - id: meta
        uses: docker/metadata-action@<SHA>         # v6
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,format=long
            type=ref,event=branch

      # Build locally first (not pushed) so we can scan before anything leaves CI
      - name: Build (load to local docker)
        uses: docker/build-push-action@<SHA>       # v7
        with:
          context: .
          load: true
          push: false
          tags: local/agent:scan
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Trivy image scan (gate)
        uses: aquasecurity/trivy-action@<SHA>      # v0.36.0
        with:
          image-ref: local/agent:scan
          severity: CRITICAL,HIGH
          ignore-unfixed: true
          vuln-type: os,library
          scanners: vuln,secret,misconfig
          exit-code: "1"                           # break the build
          format: sarif
          output: trivy.sarif
      - uses: github/codeql-action/upload-sarif@<SHA>   # v4 [UNVERIFIED major]
        if: always()
        with: { sarif_file: trivy.sarif }

      - name: Log in to GHCR
        if: github.event_name == 'push'
        uses: docker/login-action@<SHA>            # v4
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & push (reuses cache; identical layers)
        if: github.event_name == 'push'
        id: push
        uses: docker/build-push-action@<SHA>       # v7
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          provenance: mode=max                     # BuildKit SLSA provenance
          sbom: true                               # BuildKit SBOM attestation

      - name: Generate SBOM with Syft (CycloneDX)
        if: github.event_name == 'push'
        uses: anchore/sbom-action@<SHA>            # v0
        with:
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.push.outputs.digest }}
          format: cyclonedx-json
          output-file: sbom.cdx.json
          upload-artifact: true

      - name: Install Cosign
        if: github.event_name == 'push'
        uses: sigstore/cosign-installer@<SHA>      # v4.1.0 (installs cosign v3.x)

      - name: Sign image by digest (keyless) + attach SBOM attestation
        if: github.event_name == 'push'
        env:
          IMAGE: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.push.outputs.digest }}
        run: |
          cosign sign --yes "$IMAGE"
          cosign attest --yes --type cyclonedx --predicate sbom.cdx.json "$IMAGE"

      - name: GitHub build provenance attestation (SLSA)
        if: github.event_name == 'push'
        uses: actions/attest@<SHA>                 # v4
        with:
          subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          subject-digest: ${{ steps.push.outputs.digest }}
          push-to-registry: true
```

**How to verify (staging gate or auditor demo):**

```bash
IMAGE=ghcr.io/example/rag-agent@sha256:<digest>
cosign verify \
  --certificate-identity-regexp '^https://github.com/example/rag-agent/\.github/workflows/release\.yml@refs/heads/main$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  "$IMAGE"
cosign verify-attestation --type cyclonedx \
  --certificate-identity-regexp '^https://github.com/example/rag-agent/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com "$IMAGE"
gh attestation verify oci://$IMAGE --owner example
```

**Design notes for the facilitator**

- **Scan before push.** The image never reaches the registry if it fails.
- **Sign the digest, deploy the digest.** Tags can be re-pointed; digests can't.
- **One build, many environments.** Staging and prod run the *identical* digest. "Rebuild for prod" breaks the evidence chain.
- **Pin the scanners themselves** (Action SHAs, scanner image digests). See the Trivy incident [9].
- **Evals cost money and touch real APIs.** Use a separate, low-quota, eval-only key in a protected GitHub Environment, and don't run paid evals on untrusted fork PRs.
- Semgrep `--config auto` requires metrics to be enabled. In restricted environments use explicit or local rulesets [20] **[UNVERIFIED: still true in v1.182]**.

---

## 6. AI-specific additions

### 6.1 Evals as a pipeline gate

- **What:** a version-controlled test suite of prompts with expected behaviors: correctness on a golden dataset, refusal of disallowed requests, resistance to prompt-injection strings, correct tool selection and arguments for agents, output format/schema validity, and cost/latency budgets.
- **Why it's a gate:** LLM behavior can regress when *any* of these change: model ID, system prompt, retrieval index, tool definitions, temperature, or SDK version. Treat each as a build input.
- **Tools:** Promptfoo (OpenAI-owned since Mar 2026 [32]), DeepEval, OpenAI Evals, Inspect (UK AISI), LangSmith/Langfuse datasets, garak for red-team probes **[UNVERIFIED: individual statuses other than Promptfoo/garak]**.
- **Gate examples:** `accuracy ≥ baseline − 2%`, `0 critical safety failures`, `100% JSON-schema valid`, `p95 latency < 8s`, `cost/run < $0.05`.

### 6.2 Pin model versions and prompt versions

- **Model IDs:** Use fixed model identifiers, not moving aliases. Anthropic's docs state that a pinned ID's underlying model "remains constant for the lifetime of that ID." Aliases like `claude-sonnet-4-5` can move to newer snapshots. From the 4.6 generation onward, dateless IDs (e.g., `claude-sonnet-4-6`) are fixed snapshots, not aliases. Serving infrastructure can still change behavior slightly, and every ID has a deprecation/retirement schedule, so **evals must re-run on a schedule, not only on code change** [31].
- **Prompts:** Store system prompts, tool schemas and few-shot examples as versioned files in the repo, reviewed via PR, and stamp `PROMPT_VERSION` into logs and traces.
- **Agent harness / SDK versions:** pin in lockfiles with hashes.
- **Self-hosted models:** pin model weights by hash (e.g., Hugging Face revision commit SHA), prefer **safetensors** over pickle, and scan with ModelScan [28]. Package weights as OCI artifacts in the private registry so they get the same signing and scanning treatment.

### 6.3 Scanning MCP servers and agent skills

MCP servers are **code you run that an LLM can drive.** Threats include tool poisoning (malicious instructions hidden in tool descriptions), "rug pulls" (a tool definition changing after approval), excessive privileges, token passthrough, SSRF, and malicious local startup commands. The current MCP spec's Security Best Practices page (latest protocol revision 2026-07-28) [29]:

- **forbids token passthrough:** servers MUST NOT accept tokens not issued for them;
- requires per-client consent for proxy servers (confused deputy);
- recommends SSRF defenses: block private IP ranges and `169.254.169.254` metadata, use egress proxies;
- requires clients to show the full command before installing a local server, and recommends running local servers **sandboxed (containers)** with minimal privileges;
- recommends progressive, least-privilege OAuth scopes.

**Pipeline controls for MCP servers and skills**

1. **Source:** only from an internal allow-listed catalog (e.g., a Docker MCP Catalog custom catalog [35], DHI hardened MCP images [3], or your own Harbor project).
2. **Build:** containerize every MCP server (no `npx some-server@latest` at runtime); pin by digest; SCA + SAST like any app.
3. **Scan:** `snyk-agent-scan` (tool-description injection/poisoning) [26] plus Trivy/Grype on the image; review tool descriptions in PRs; **hash tool definitions** and alert on change (rug-pull detection).
4. **Runtime:** non-root, read-only FS, NetworkPolicy egress allow-list, no service-account token, and secrets scoped to that server only.
5. **Map to OWASP Agentic Top 10 (2026):** ASI02 Tool Misuse, ASI03 Identity & Privilege Abuse, ASI04 Agentic Supply Chain, ASI05 Unexpected Code Execution [30].

### 6.4 Secrets for API keys

| Tool | Notes |
|---|---|
| **HashiCorp Vault** (v1.21.x; now IBM) / **OpenBao** (OSS fork) | Dynamic secrets, leases, Kubernetes auth; Vault Agent / CSI driver injection **[UNVERIFIED: OpenBao maturity]** |
| **AWS Secrets Manager** / **Azure Key Vault** / **Google Secret Manager** | Cloud-native; available in GovCloud/Azure Gov regions; IAM-scoped access |
| **External Secrets Operator** v1.3.x | Syncs any of the above into Kubernetes Secrets. Paused Aug 2025, resumed by 2026 [34] |
| **Secrets Store CSI Driver** | Mounts secrets as files directly from the provider without K8s Secret objects |
| **CI OIDC federation** | GitHub/GitLab OIDC → cloud role; **no long-lived cloud keys in CI** |

**Rules:** never bake keys into images or prompts; one key per service/environment; set provider-side spend limits; rotate on schedule and after any CI compromise (the Trivy-action attack harvested CI secrets [9]); enable GitHub push protection (it recognizes major LLM provider key formats [58]).

### 6.5 Egress allow-listing

Agents can be talked into exfiltrating data (prompt injection) or calling attacker URLs (SSRF). Restrict **where the container can talk**:

- **Kubernetes NetworkPolicy:** default-deny egress, then allow DNS and the egress proxy only. NetworkPolicy works on IP/CIDR and pod labels, **not hostnames** [59].
- **FQDN-aware policy:** Cilium `toFQDNs`, Calico DNS policies, Istio egress gateway, or an explicit forward proxy (Squid, Smokescreen, Envoy) that allow-lists `api.anthropic.com`, your Azure OpenAI/Bedrock endpoint, etc.
- **Cloud private endpoints:** AWS Bedrock via VPC endpoint / PrivateLink; Azure OpenAI private endpoint. Traffic never touches the public internet, which is often required for CUI.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: agent-egress-allowlist, namespace: ai-agents }
spec:
  podSelector: { matchLabels: { app: rag-agent } }
  policyTypes: [Egress]
  egress:
    - to:   # DNS
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports: [ { protocol: UDP, port: 53 }, { protocol: TCP, port: 53 } ]
    - to:   # only the egress proxy, which allow-lists LLM API hostnames
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: egress } }
          podSelector: { matchLabels: { app: egress-proxy } }
      ports: [ { protocol: TCP, port: 3128 } ]
```

### 6.6 Model / artifact scanning

- **ModelScan** (OSS, Protect AI → Palo Alto Prisma AIRS) detects code-execution payloads in serialized models [27][28].
- Prefer **safetensors/GGUF/ONNX** over pickle-based formats; Hugging Face also scans uploads (picklescan, malware scan) **[UNVERIFIED current HF scanner set]**.
- Commercial: Prisma AIRS model security (formerly Protect AI Guardian), HiddenLayer, JFrog (ML model scanning in Artifactory/Xray) **[UNVERIFIED feature names]**.
- Include models and datasets in the SBOM (CycloneDX ML-BOM; SPDX 3 AI/Dataset profiles) per CISA/G7 AI SBOM guidance [42].

### 6.7 Logging and monitoring

| Layer | Tool | What to capture |
|---|---|---|
| **Runtime security** | **Falco** (CNCF Graduated), **Tetragon** (Cilium, eBPF), commercial CNAPP sensors | Shell spawned in container, write to read-only paths, unexpected outbound connection, privilege escalation, reads of `/var/run/secrets` |
| **Audit** | Kubernetes API audit logs; cloud audit (CloudTrail, Azure Activity, GCP Audit); registry pull/push logs; Rekor transparency log | Who deployed which digest, when, with what approval |
| **LLM/agent telemetry** | **OpenTelemetry GenAI semantic conventions**: `gen_ai.request.model`, `gen_ai.usage.input_tokens/output_tokens`, `invoke_agent`, `execute_tool` spans. Still **"Development" status** (not stable) as of mid-2026; moved to their own repo in June 2026, including MCP conventions [33] | Model ID, prompt version, tool calls and arguments (redacted), token cost, refusals, latency |
| **Backends** | Langfuse, Arize Phoenix, Datadog/Splunk/Elastic, Grafana stack | Dashboards and alerts; retain per records schedule |

---

## 7. Government and regulated context (status as of Oct 2026)

| Item | What it is | Current status |
|---|---|---|
| **NIST SP 800-218 (SSDF) v1.1** | Secure Software Development Framework: practice groups PO (Prepare the Organization), PS (Protect the Software), PW (Produce Well-Secured Software), RV (Respond to Vulnerabilities) | **Final** (Feb 2022) [36] |
| **NIST SP 800-218 Rev. 1 (SSDF v1.2)** | Update ordered by EO 14306 | **Initial public draft 17 Dec 2025**, comments closed 30 Jan 2026; **still draft on NIST's page as of 20 Oct 2026** despite the EO's ~120-day finalization target [36][37][39]. Flag as "check before delivery." |
| **NIST SP 800-218A** | SSDF Community Profile for Generative AI and Dual-Use Foundation Models; audiences are AI model producers, AI system producers, and acquirers | **Final, 26 Jul 2024** [38]. Originally tasked under EO 14110 (since revoked); the document stands as NIST guidance. |
| **NIST SP 800-190** | Application Container Security Guide: risks and countermeasures for images, registries, orchestrators, containers and host OS | **Final, Sept 2017; no revision announced** [2]. Still the canonical federal container reference. |
| **NIST SP 800-204D** | Integrating software supply chain security into DevSecOps CI/CD pipelines | **Final, Feb 2024** [53] |
| **NIST SP 800-53 Rel. 5.2.0** | Control catalog update for software update/patch practices (per EO 14306) | **Released Aug 2025** [54] |
| **EO 14028** (May 2021) | Origin of SBOM/SSDF push; directed OMB attestation memos | Still in force but **amended by EO 14144 (Jan 2025) and EO 14306 (6 Jun 2025)**. EO 14306 replaced the 14144 software-attestation provisions with NIST/NCCoE tasks (SSDF consortium by 1 Aug 2025, preliminary SSDF update by 1 Dec 2025, final ~120 days later) [39] |
| **OMB M-22-18 / M-23-16** | Required federal agencies to collect secure-development attestations (CISA Common Form) | **Rescinded by OMB M-26-05 (23 Jan 2026).** Agencies must keep software/hardware inventories and set risk-based assurance policies. The attestation form and SBOMs are optional contract terms [40] |
| **CISA SBOM guidance** | 2026 Minimum Elements for an SBOM (with NSA, FBI and international partners) | **Released late July 2026**; replaces the 2021 NTIA minimum elements; adds hash, license, tool, generation context and author signature; covers AI and SaaS [41]. **SBOM for AI – Minimum Elements** (CISA + G7), 13 May 2026 [42] |
| **CISA Secure by Design** | Pledge and principles (memory-safe languages, MFA by default, eliminating vuln classes, transparency) | Pledge launched May 2024 **[UNVERIFIED: 2026 program status]** |
| **DoD Enterprise DevSecOps document set** | Strategy Guide, **DevSecOps Fundamentals**, Reference Designs (CNCF Kubernetes, multi-cluster, AWS), Playbook, Tools & Activities Guidebook | Library set **v2.1/2.5 era (2021–2023)** **[UNVERIFIED: exact latest version on dodcio.defense.gov]** [44]. Still the reference for "software factory" architecture. |
| **DoD cATO** | Continuous ATO: authorization of the *pipeline + continuous monitoring*, not each release | Memo by DoD CIO (Feb 2022) **[UNVERIFIED cite]**; now embedded in **CSRMC** (24 Sep 2025), whose five phases are Design → Build → Test → Onboard → Operations, with tenets including automation, critical controls, continuous monitoring and ATO, DevSecOps, inheritance and reciprocity [43] |
| **DoD SWFT (Software Fast Track)** | Acquisition/authorization reform: SBOM clearinghouse, third-party SSDF assessment, continuous ATO, AI-assisted risk review | Pilot 2025; reported as a standing enterprise program in 2026 [45] **[Check DoD CIO for the latest SWFT implementation guidance]** |
| **Iron Bank / Platform One** | DoD hardened container repository and Big Bang platform | Active; ABC + ORA scoring; 12-hour rescans [5]. Vendors delivering containers to DoD software factories typically must go through Iron Bank [45]. |
| **FedRAMP** | Cloud authorization | **FedRAMP 20x:** Phase 1 (Low pilot) and Phase 2 (Moderate pilot) done; Phase 3 formalizing rules (Consolidated Rules 2026) with the pipeline opening for Class A/B/C; Class D (High) pilot planned FY27; **FedRAMP plans to stop accepting new Rev5 certifications 11 Jun 2027** (estimate). Machine-readable (OSCAL) packages are being required [46]. Key Security Indicators favor exactly the automated evidence a good pipeline produces. |
| **CMMC** (DoD contractors) | 800-171-based certification | Phase 1 effective 10 Nov 2025; Phase 2 (C3PAO) 10 Nov 2026 (per vendor summary) [45] **[UNVERIFIED primary]** |

**Trainer framing:** The *paperwork* requirements loosened (M-26-05), but the *practice* expectations moved toward automated, continuous, machine-readable evidence (SSDF 1.2, CSRMC/cATO, SWFT, FedRAMP 20x KSIs, CISA SBOM 2026). A pipeline that emits signed SBOMs, scan results and provenance is how you meet all of them with one investment.

---

## 8. Roles: who needs to know what

| Role | Needs to know | Does |
|---|---|---|
| **Executives / program managers** | Why pipelines shorten ATO timelines; cost of exceptions; vendor SBOM asks | Fund the platform; set risk appetite (thresholds); require SBOM/attestation clauses in contracts |
| **ISSO / ISSM / AO / assessors** | How to read a scan report, SBOM, signature verification and attestation; what "Iron Bank approved" does and doesn't mean | Approve the *pipeline* and its gates once (cATO); review exceptions; consume dashboards instead of screenshots |
| **Acquisition / contracting** | M-26-05 means requirements are now **agency-specific**; CISA 2026 SBOM elements; SWFT | Write SBOM (CycloneDX/SPDX), VEX, vuln-disclosure and patch-SLA clauses |
| **Product owners / analysts / prompt authors** | Prompt and model changes are code changes; evals are a gate | Write and maintain eval cases; approve prompt PRs |
| **End users / mission staff** | Use only approved agents/MCP servers; never paste keys; report odd agent behavior | Follow the approved catalog; report incidents |
| **Developers / ML engineers** | Dockerfile hardening, dependency pinning, secrets handling, MCP security rules | Fix findings, write VEX justifications, keep base images current |
| **Platform / DevSecOps engineers** | Everything in §§2–6 | Build and maintain the pipeline, registries, admission policies, runtime monitoring |
| **SOC / incident response** | Falco/OTel signals; how to trace a running digest back to its commit | Respond; trigger rebuilds and key rotation |

**"One scanned image, authorized and redeployed": how it speeds approvals**

1. The image is built once, scanned, signed and attested. Its **digest** is its identity.
2. The assessor approves the **pipeline and policies** (thresholds, signing, admission control) rather than each release.
3. Every release then produces the same machine-readable evidence package (SBOM, scan results, provenance, eval results) tied to the digest.
4. Staging and prod run the **same digest**, and admission control rejects anything else.
5. When a new CVE appears, the pipeline rebuilds on a patched base, re-runs the same gates, and redeploys **without a new ATO**, because the authorized *process* produced it. That is the cATO / CSRMC / SWFT model [43][45]. Iron Bank's reciprocity works the same way: harden once, reuse across programs [5].

---

## 9. Hands-on lab, check questions, misconceptions

### 9.1 Suggested 90-minute session outline (train-the-trainer)

| Time | Segment | Format | Materials |
|---|---|---|---|
| 0:00–0:08 | Hook: narrated video (~8 min), "One box, scanned once, trusted everywhere" | Video | Narration + scene diagrams |
| 0:08–0:20 | Concepts: image/container/registry, digest vs tag, layers (live `docker history`) | Demo + discussion | Laptop with Docker/Podman |
| 0:20–0:35 | **Lab 1, "Scan the box":** pull `python:3.12` vs a DHI/Chainguard/distroless python image; run `trivy image` and `grype` on both; compare counts; run `syft` and open the SBOM; look up one CVE's EPSS and KEV status | Pairs | Trivy, Grype, Syft pre-installed; offline DB snapshot for air-gapped rooms |
| 0:35–0:45 | **Lab 2, "Find the leak":** a seeded repo with a fake API key committed then "deleted"; run `gitleaks git .`; show the key survives in an image layer (`docker history`, `trivy image --scanners secret`) | Pairs | Seeded repo, **dummy keys only** |
| 0:45–0:55 | **Lab 3, "Harden it":** convert a naive Dockerfile to multi-stage, non-root, pinned digest; rescan; apply a `restricted` securityContext | Pairs | Starter Dockerfile |
| 0:55–1:10 | **Lab 4, "The line":** walk the GitHub Actions workflow (§5.4); trigger a failing build with a vulnerable dependency, then a failing eval (a changed system prompt drops a refusal case); fix both; watch sign + attest; `cosign verify` | Instructor-led + pairs | Template repo; GHCR; eval-only API key or a mocked LLM endpoint |
| 1:10–1:18 | **Lab 5, "Guard at the door":** apply the Kyverno policy on a kind/k3d cluster; deploy unsigned (denied) vs signed (allowed); apply the egress NetworkPolicy and show a blocked `curl` to an unlisted host (requires a CNI that enforces NetworkPolicy, e.g., Calico/Cilium) | Demo | kind + Kyverno + Calico |
| 1:18–1:25 | Gov context: M-26-05, SSDF 1.2 draft, CISA SBOM 2026, CSRMC/cATO, SWFT, FedRAMP 20x; role table | Discussion | One slide per item with status date |
| 1:25–1:30 | Check questions + trainer debrief (how to teach this to non-technical groups) | Quiz | §9.2 |

**Non-technical track variant:** Replace Labs 3–5 with a "read the evidence" exercise. Give learners a Trivy report, an SBOM excerpt, a `cosign verify` output and an eval report, and have them decide approve, conditionally approve, or reject using a one-page rubric.

**Air-gapped classroom:** pre-download the Trivy DB (`trivy image --download-db-only`, then `--skip-db-update`) and the Grype DB (`grype db import`), and use a local Harbor/registry. Use key-based Cosign instead of keyless.

### 9.2 Six check questions (with answers)

1. **Why do we deploy and sign images by digest instead of tag?**
   *Answer:* A tag such as `:latest` or `:1.2` is a movable label that can be re-pointed to different content. A digest (`sha256:...`) is a cryptographic hash of the content itself, so it guarantees the exact bytes that were scanned and approved are the bytes that run.

2. **A developer added an API key in one Dockerfile step and deleted it in the next. Is the image safe to publish? Why?**
   *Answer:* No. Each step creates a permanent layer, so the key remains in the earlier layer and anyone who can pull the image can extract it. Rotate the key immediately, rebuild using runtime secret injection or BuildKit secret mounts, and add secret scanning (Gitleaks/TruffleHog/Trivy secret scanner) to the pipeline.

3. **A scan shows 40 HIGH CVEs. What do you fix first?**
   *Answer:* Anything on CISA's KEV list, then CVEs with high EPSS (likely to be exploited soon), then fixable Critical/High by CVSS, focusing on packages actually used at runtime. Document non-exploitable ones with VEX. Often the fastest fix is switching to a minimal or hardened base image.

4. **What's the difference between scanning and signing, and why do you need both?**
   *Answer:* Scanning checks whether the content has known problems. Signing and attestation prove the content's identity and origin (who built it, from what commit) and that it hasn't been altered. Without signing, an attacker could swap a scanned image for a malicious one. Without scanning, you would be faithfully delivering vulnerable software.

5. **Your agent's code didn't change, but its answers got worse this week. Name two pipeline controls that would have caught or prevented this.**
   *Answer:* (a) Pin the model ID (no moving aliases) and version prompts and tool definitions in Git, so changes go through PR review. (b) Run evals as a gate on every change **and on a schedule**, because provider infrastructure and retrieval data can shift even with a pinned model. Also log the model ID and prompt version in telemetry to diagnose the change.

6. **In March 2026, a popular open-source scanner's GitHub Action was hijacked. What two controls limit the damage?**
   *Answer:* (a) Pin third-party Actions to full commit SHAs (enforceable by GitHub org policy) and pin scanner images by digest, so moved tags can't inject new code. (b) Least-privilege CI: short-lived OIDC credentials instead of stored secrets, minimal `permissions:`, separate eval keys with spend caps, and rapid secret rotation when a dependency is compromised.

### 9.3 Common misconceptions

| Misconception | Reality |
|---|---|
| "Containers are as isolated as VMs." | Containers share the host kernel. Use VMs or sandboxed runtimes (gVisor/Kata/Firecracker) for untrusted or agent-generated code. |
| "Zero CVEs means secure." | Scanners only find *known* issues in *recognized* packages. Logic flaws, misconfigs, prompt injection and secrets need other controls. |
| "Iron Bank approval = ATO." | Iron Bank explicitly does not grant an ATO or CtF; the program still decides [5]. |
| "SBOMs are no longer required, so we can skip them." | M-26-05 made them optional *government-wide*, but agencies may require them by contract, CISA 2026 guidance raised the baseline, and DoD SWFT centers on an SBOM clearinghouse [40][41][45]. |
| "`:latest` is fine for base images if we scan." | Without a digest you can't reproduce or prove what you scanned. Pin digests and let Renovate/Dependabot update them via PR. |
| "Our scanner is a security tool, so it's trustworthy." | Security tools are supply-chain dependencies too (Trivy/KICS Actions, March 2026) [9]. |
| "MCP servers are just config." | They are executable code with access to tools and data, and their tool descriptions are prompt input to your model. Containerize, pin, scan and egress-restrict them [29]. |
| "A model ID never changes behavior." | Weights are fixed per pinned ID, but serving infrastructure can cause minor changes, and IDs get retired. Re-run evals on a schedule [31]. |
| "NetworkPolicy can allow `api.anthropic.com`." | Standard NetworkPolicy is IP/label-based. Use FQDN-aware CNI policies or an egress proxy [59]. |
| "Kubernetes Secrets are encrypted." | By default they are base64-encoded in etcd unless encryption at rest is configured. Use an external secret manager and etcd encryption. |
| "Rebuilding for prod is safer." | It breaks the evidence chain. Promote the same signed digest. |

---

## 10. Items to re-verify immediately before delivery

1. SSDF v1.2 final status (csrc.nist.gov/projects/ssdf) [36].
2. CVE program funding/administration after March 2026 [51].
3. Exact SHAs for every GitHub Action in §5.4, and the current majors of `github/codeql-action` and `actions/setup-python`.
4. DoD DevSecOps document versions and any new SWFT/CSRMC implementation guidance [43][44][45].
5. FedRAMP 20x phase dates (the page says dates are estimates) [46].
6. Whether `snyk-agent-scan` sends data off-host (important for CUI/classified labs) [26].
7. Promptfoo's licensing after the OpenAI acquisition [32].

---

## 11. Where containers run

### 11.1 Plain language

A container image is like a shipping container: the box stays the same, but the ship, train or truck carrying it changes. The same signed image (same digest) can run on a laptop, a single server, a cloud "serverless" service, a Kubernetes cluster, or an edge device in a disconnected site. **What changes is who patches what.** The further you move toward managed services, the more of the stack the provider patches. Your own image, code, dependencies, secrets and network rules are always yours.

### 11.2 Run locations and shared responsibility

| Where it runs | Examples (Oct 2026) | You manage | Provider / platform manages | Typical use | Security notes |
|---|---|---|---|---|---|
| **Developer laptop** | Docker Desktop, Podman Desktop, Rancher Desktop, OrbStack (macOS) | Everything: the VM, the engine, images, local secrets | Desktop vendor ships engine updates | Build, test, run an MCP server locally over stdio | Use the same base image and Dockerfile as CI. Docker Desktop's Enhanced Container Isolation (Business tier) runs containers rootless inside the Desktop VM and blocks them from modifying the VM's Docker Engine [61]. Never keep production keys on the laptop. |
| **Single VM / server** | Docker Engine or Podman on Linux; Podman Quadlet / systemd units; Docker Compose | OS patching, engine, host firewall, images, secrets, logging, backups | Cloud provider: the hypervisor and physical host (if cloud VM) | Small internal tools, pilot workflows, a team MCP server | Host firewall gotcha: Docker-published ports bypass ufw (see 12.4) [62]. Run rootless Podman or a non-root user; keep the host minimal. |
| **Managed serverless containers** | AWS Fargate (ECS/EKS), Google Cloud Run, Azure Container Apps | Image, app code, IAM roles, env/secrets wiring, network/egress settings | Servers, OS, runtime, scaling, host patching | Scheduled AI workflows, HTTP MCP servers, APIs that scale to zero | With Fargate, "AWS becomes responsible for securing the underlying instance/runtime used to run your Pods" [63]. Cloud Run runs on gVisor and now offers Preview "sandboxes" for running untrusted code such as AI agent tools (requires the second-generation execution environment) [64][66]. Azure Container Apps needs a *workload profiles* environment to route egress through Azure Firewall via user-defined routes; the legacy Consumption-only type does not support UDRs or NAT Gateway [65]. |
| **Managed Kubernetes** | Amazon EKS (self-managed nodes, managed node groups, Fargate, Auto Mode), Azure AKS, Google GKE (Standard, Autopilot) | Workloads, namespaces, RBAC, NetworkPolicy, admission policy, node upgrades (unless fully managed), add-ons | Control plane (API server, etcd); node images on managed options | Many services, multi-team platforms, agent harnesses at scale | "AWS will assume additional responsibilities as you move from self-managed workers, to managed node groups, to Fargate" [63]. With managed node groups, you still upgrade node groups to the latest AMI [63]. |
| **Self-managed / enterprise Kubernetes** | Red Hat OpenShift, SUSE Rancher / RKE2, k3s, upstream kubeadm | Everything above **plus** the control plane, etcd, upgrades, CNI, ingress | Vendor provides distribution, patches, support | On-prem data centers, regulated workloads, hybrid | You own control-plane hardening and patch cadence. OpenShift and RKE2 ship hardened defaults (e.g. SCC / CIS profiles) **[UNVERIFIED: check current hardening guides]**. |
| **PaaS / app platforms** | Heroku-style platforms, Fly.io Machines, Render, App Service for Containers | Image, app config, secrets | Most of the runtime | Fast deploys of small services | Check where egress can be restricted; many PaaS products have limited egress control. Fly.io Machines use Firecracker microVMs [67]. |
| **Edge / IoT** | k3s, MicroK8s, Podman on devices, AWS IoT Greengrass, Azure IoT Edge | Devices, OS, updates over unreliable links, physical security | Little or nothing | Factory floors, vehicles, remote sites | k3s is a lightweight Kubernetes distribution often used at the edge [68]. Sign images and verify on the device; plan for offline updates. |
| **On-prem and air-gapped** | k3s / RKE2 / OpenShift with an internal registry mirror (Harbor, Artifactory, Quay) | Everything, including mirroring images and vulnerability databases across the air gap | Nobody | Classified, OT/ICS, high-security sites | k3s documents air-gap installs using a private registry or embedded registry mirror [68]. Scanners need an offline vulnerability DB copy (e.g. Trivy/Grype offline DB) moved across the gap on a schedule. |
| **CI runners** | GitHub-hosted runners, self-hosted runners, Actions Runner Controller (ARC), GitLab runners | Self-hosted: the runner host, its network, cleanup between jobs | Hosted runners: the VM, wiped after each job | Building and scanning images | Prefer ephemeral (one job, then destroyed) runners; a persistent self-hosted runner can carry malware or secrets from one job to the next. Restrict runner egress too **[UNVERIFIED: re-check GitHub's current self-hosted runner hardening docs]**. |

### 11.3 Sandboxed runtimes for untrusted or agent-written code

A normal container shares the host kernel (section 1). When the code is untrusted, for example code an AI agent wrote, a tool a model chose to run, or a customer's plugin, add a stronger boundary:

| Runtime | How it isolates | Where it is used (per public sources) |
|---|---|---|
| **gVisor** | A user-space "application kernel" (the Sentry) answers the program's system calls, so the host kernel is not directly exposed. Overhead on syscall-heavy work. | Google Cloud Run, GKE Sandbox, App Engine; reported use by OpenAI and Anthropic for code execution [67] |
| **Firecracker** | Each sandbox is a tiny KVM-backed virtual machine with its own guest kernel. Needs KVM (usually bare metal). | AWS Lambda, Vercel Sandbox, Fly.io [67]; AWS has also described it as underpinning Fargate **[UNVERIFIED: confirm current status]** |
| **Kata Containers** | A container runtime that launches each pod in a lightweight VM (using QEMU, Cloud Hypervisor or Firecracker underneath). The usual way to get a VM boundary *inside* Kubernetes. | Kubernetes `RuntimeClass` [67] |

**Rule of thumb:** trusted, reviewed code → normal hardened container. Untrusted or agent-generated code → sandboxed runtime **and** no network egress except what the task needs.

## 12. Firewalls and network controls for containers

### 12.1 Plain language

Think of a building with several locked doors: the gate at the street, the lobby, the floor, the office. Each door checks again. Container networking works the same way, from the outside in, and **in both directions**. Most teams think about who can get *in*. For AI workloads, what can get *out* matters just as much: a prompt-injected agent with open internet access can send your data anywhere. **Default deny, both directions, then allow only what the job needs.**

### 12.2 The layers, outside in

| # | Layer | What it does | Common tools / services | Notes |
|---|---|---|---|---|
| 1 | **Edge: WAF and DDoS protection** | Filters inbound web requests (injection, bots, known-bad IPs) before they reach you | AWS WAF + Shield, Azure Front Door / Application Gateway WAF, Google Cloud Armor, Cloudflare, Akamai | Inbound only. Rate-limit expensive LLM endpoints here. |
| 2 | **Cloud network firewall / security groups** | Allows or denies traffic by IP, port and protocol at the VPC/VNet level; stateful | AWS Security Groups and NACLs, Azure NSGs, Google VPC firewall rules / Cloud NGFW | IP- and port-based. FQDN support is product-specific: AWS Network Firewall domain lists match the HTTP Host header and TLS SNI rather than doing DNS lookups [69]; Google Cloud NGFW supports FQDN objects [70]. |
| 3 | **Central egress firewall / proxy** | One controlled exit for outbound traffic, with a hostname allow-list and logs | AWS Network Firewall, Azure Firewall, Google Cloud NGFW, Squid, Envoy, cloud NAT gateways | The place to enforce "only `api.anthropic.com` / `api.openai.com` / approved backends". Azure Container Apps reaches it via user-defined routes in a workload profiles environment [65]. |
| 4 | **Host firewall** | Filters traffic on the server itself | iptables / nftables, firewalld, ufw | **Gotcha:** Docker routes container traffic in the `nat` table, "effectively ignoring your firewall configuration"; Docker states that "Docker and ufw use firewall rules in ways that make them incompatible" [62]. Put your rules in the `DOCKER-USER` chain, which is processed before Docker's own rules [71], or don't publish ports on public interfaces (bind to 127.0.0.1). Docker's nftables backend is still marked experimental [62]. |
| 5 | **Kubernetes NetworkPolicy** | Pod-to-pod and pod-to-outside rules by labels, namespaces, IP blocks and ports | Built-in API, enforced by the CNI: Calico, Cilium, Antrea; GKE Dataplane V2; AKS/EKS network policy options | Start with **default-deny ingress and egress** per namespace, then allow DNS and named destinations [59]. A policy does nothing if the CNI doesn't enforce it. Standard NetworkPolicy has **no hostname field**, so it can't express "allow `api.anthropic.com`". |
| 6 | **FQDN-aware policy (CNI)** | Allow egress by DNS name | Cilium `toFQDNs` (watches DNS answers through its DNS proxy, so names map to the right IPs) [72]; GKE FQDN network policies (Dataplane V2) [73]; Calico Enterprise DNS policies | The in-cluster alternative to an egress proxy. Cilium can combine `toFQDNs` with port and L7 rules, e.g. `*.github.com` on TCP 443 only [72]. |
| 7 | **Service mesh** | Mutual TLS between services, identity-based authorization, egress gateways | Istio (incl. ambient mode), Linkerd | mTLS proves which service is calling. An Istio egress gateway funnels outbound traffic through one controlled, logged point **[UNVERIFIED: re-check current Istio egress docs before delivery]**. |
| 8 | **Inside the container** | Least privilege so that a breach can't move | Non-root, read-only root filesystem, dropped capabilities, no shell (section 2) | Not a firewall, but it limits what an attacker who gets in can do. |

### 12.3 Why hostname allow-lists need a proxy or an FQDN-aware tool

IP addresses for SaaS and LLM APIs change often and are shared by many customers behind CDNs, so an IP allow-list is either wrong or too broad. Hostname filtering needs something that sees the name: an HTTP(S) proxy (sees the `CONNECT` host), a firewall that reads the TLS SNI or HTTP Host header [69], or a CNI that watches DNS resolution [72]. Caveat: SNI- and Host-based filtering trusts what the client sends, so AWS advises adding IP-based rules where SNI manipulation is a concern [69]. Encrypted Client Hello (ECH) can hide SNI; check your firewall's handling **[UNVERIFIED]**.

### 12.4 The Docker-and-ufw gotcha, in detail

On a single Linux server, a team enables ufw ("deny incoming") and runs `docker run -p 8080:8080 mcp-server`. Port 8080 is reachable from the internet anyway, because Docker's DNAT rules divert the packets before ufw's INPUT chain sees them [62]. Fixes:

1. Bind published ports to localhost when only a local reverse proxy needs them: `-p 127.0.0.1:8080:8080`.
2. Put allow/deny rules in the `DOCKER-USER` chain (processed before Docker's rules), and add an established/related accept rule first so reply traffic still works [71].
3. Rely on the cloud security group / NSG as the real perimeter, and test from outside (`nmap` from another host) after every change.

### 12.5 Inbound vs outbound, default deny, and logging

- **Inbound:** only the ports the service needs, only from the load balancer or gateway, never directly from the internet to a pod or container.
- **Outbound (egress):** default deny. Allow DNS to the cluster resolver, the LLM API endpoint(s), approved backends (ticket system, database), and the secrets manager. Everything else is blocked and **logged**.
- **Logging:** firewall and proxy logs (who tried to reach what) go to the SIEM. A blocked egress attempt from an AI workload is a high-signal alert: it often means prompt injection or a compromised dependency.

### 12.6 Tying it to AI workloads

| Risk | Network control that limits it |
|---|---|
| Prompt injection tells the agent to send data to `attacker.example` | Egress allow-list: only the LLM API and approved backends are reachable, so the send fails and is logged |
| A malicious MCP server or package phones home | Container egress default-deny; FQDN policy per workload |
| An HTTP MCP server is exposed to the internet by accident | Security group / NSG + WAF in front; bind to localhost; Docker/ufw gotcha checked |
| DNS rebinding against a local MCP server | Bind to 127.0.0.1 and validate the Host header (see Deep Dive A) |
| Lateral movement after a container breach | NetworkPolicy default-deny between namespaces; service mesh mTLS |

**One-line takeaway:** *Same image everywhere; who patches what changes. Default deny, both directions; let the AI reach only what the job needs.*


## Sources

[1] Open Container Initiative specifications: Image Spec, Runtime Spec, Distribution Spec. https://github.com/opencontainers/image-spec · https://github.com/opencontainers/runtime-spec · https://github.com/opencontainers/distribution-spec (versions via [55])
[2] NIST SP 800-190, Application Container Security Guide (Sept 2017). https://www.nist.gov/publications/application-container-security-guide · https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-190.pdf
[3] Docker press release, "Docker Makes Hardened Images Free, Open and Transparent for Everyone" (17 Dec 2025). https://www.docker.com/press-release/docker-makes-hardened-images-free-open-and-transparent-for-everyone/
[4] Chainguard Plans & Pricing. https://chainguard.dev/pricing
[5] Iron Bank documentation, Overview. https://docs-ironbank.dso.mil/overview/ · FAQ: https://docs-ironbank.dso.mil/faq/
[6] Docker blog, "Broadcom's New Bitnami Restrictions? Migrate Easily with Docker." https://www.docker.com/blog/broadcoms-new-bitnami-restrictions-migrate-easily-with-docker/
[7] Red Hat Ecosystem Catalog, UBI 10 / ubi-minimal / ubi-micro. https://catalog.redhat.com/en/software/containers/ubi10/ubi/66f2b46b122803e4937d11ae
[8] Google distroless. https://github.com/GoogleContainerTools/distroless (not re-fetched this session)
[9] Aqua Security, "Trivy supply chain attack: what you need to know" (Mar 2026). https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know · CVE-2026-33634: https://cveawg.mitre.org/api/cve/CVE-2026-33634 · Snyk analysis: https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/
[10] GitHub Changelog, "GitHub Actions policy now supports blocking and SHA pinning actions" (15 Aug 2025). https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/
[11] tfsec-to-Trivy migration guide. https://github.com/aquasecurity/tfsec/blob/master/tfsec-to-trivy-migration-guide.md
[12] Sigstore blog, "Cosign v3 is now available" (Oct 2025). https://blog.sigstore.dev/cosign-3-0-available/
[13] SLSA v1.2: What's new and Build Track Basics. https://slsa.dev/spec/v1.2/whats-new · https://slsa.dev/spec/v1.2/build-track-basics · https://slsa.dev/blog/2025/11/announce-slsa-v1.2
[14] actions/attest (v4) and actions/attest-build-provenance (wrapper note). https://github.com/actions/attest · https://github.com/actions/attest-build-provenance
[15] docker/build-push-action README (v7; login-action v4, setup-buildx-action v4, checkout v6). https://github.com/docker/build-push-action
[16] sigstore/cosign-installer README (v4.1.0). https://github.com/sigstore/cosign-installer
[17] aquasecurity/trivy-action README (v0.36.0). https://github.com/aquasecurity/trivy-action
[18] anchore/sbom-action README (v0). https://github.com/anchore/sbom-action
[19] gitleaks/gitleaks-action README (v3; GITLEAKS_LICENSE for orgs). https://github.com/gitleaks/gitleaks-action
[20] Semgrep docs, Sample CI configurations. https://docs.semgrep.dev/semgrep-ci/sample-ci-configs
[21] docker/metadata-action README (v6). https://github.com/docker/metadata-action
[22] BleepingComputer, "Betterleaks, a new open-source secrets scanner to replace Gitleaks" (15 Mar 2026). https://bleepingcomputer.com/news/security/betterleaks-a-new-open-source-secrets-scanner-to-replace-gitleaks
[23] OWASP Dependency-Check. https://github.com/dependency-check/DependencyCheck · summary (secondary): https://appsecsanta.com/owasp-dependency-check
[24] Palo Alto Networks, "Palo Alto Networks Introduces Cortex Cloud" (13 Feb 2025). https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-introduces-cortex-cloud--the-future-of-real-time-cloud-security
[25] Google Cloud Press Corner, "Google Completes Acquisition of Wiz" (11 Mar 2026). https://www.googlecloudpresscorner.com/2026-03-11-Google-Completes-Acquisition-of-Wiz
[26] Snyk acquires Invariant Labs (Jun 2025): https://tech.eu/2025/06/24/snyk-acquires-ai-security-pioneer-invariant-labs-for-a-new-era-in-ai-safeguards/ · PyPI snyk-agent-scan: https://pypi.org/project/snyk-agent-scan/ · PyPI mcp-scan (redirect notice): https://pypi.org/project/mcp-scan/
[27] Palo Alto Networks, "Palo Alto Networks Completes Acquisition of Protect AI" (22 Jul 2025). https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-completes-acquisition-of-protect-ai
[28] ModelScan (Protect AI) on PyPI / GitHub. https://pypi.org/project/modelscan/ · https://github.com/protectai/modelscan
[29] Model Context Protocol, Security Best Practices (latest spec). https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
[30] OWASP GenAI Security Project, "OWASP Top 10 for Agentic Applications for 2026" (9 Dec 2025). https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ · list summary: https://cycode.com/blog/owasp-top-10-agentic-applications/
[31] Anthropic Claude docs, Model IDs and versions. https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
[32] SiliconANGLE, "OpenAI to acquire Promptfoo" (9 Mar 2026). https://siliconangle.com/2026/03/09/openai-acquire-promptfoo-expand-ai-application-testing-capabilities/
[33] OpenTelemetry GenAI semantic conventions. https://opentelemetry.io/docs/specs/semconv/gen-ai/ · status summary (secondary, Jul 2026): https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke
[34] Infisical, "External Secrets Operator paused" (Aug 2025, updated Jun 2026). https://infisical.com/blog/external-secrets-operator-paused
[35] Docker docs, MCP Catalog. https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/
[36] NIST CSRC, SSDF publications (page updated 6 Oct 2026). https://csrc.nist.gov/projects/ssdf/publications
[37] NIST CSRC news, Draft SSDF Version 1.2 (17 Dec 2025). https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2 · https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
[38] NIST SP 800-218A (final, Jul 2024). https://csrc.nist.gov/pubs/sp/800/218/a/final
[39] Executive Order 14306, Federal Register 90 FR (11 Jun 2025). https://www.govinfo.gov/content/pkg/FR-2025-06-11/html/2025-10804.htm
[40] Mayer Brown, "OMB Rescinds Biden-Era Software Security Memoranda" (Feb 2026; OMB M-26-05). https://www.mayerbrown.com/en/insights/publications/2026/02/omb-rescinds-biden-era-software-security-memoranda · Wiley: https://www.wiley.law/alert-OMB-Rescinds-Secure-Software-Development-Mandate-in-Favor-of-a-Risk-Based-Approach
[41] CISA 2026 Minimum Elements for SBOM: DevOps.com (31 Jul 2026) https://devops.com/cisas-2026-sbom-guidance-adds-hash-requirements-and-ai-coverage/ · FOSSA (30 Jul 2026) https://fossa.com/blog/cisa-releases-2026-minimum-sbom-elements/ (primary CISA page not fetched this session)
[42] ExecutiveGov, "CISA, G7 Partners Release AI Software Bill of Materials Guidance" (13 May 2026). https://www.executivegov.com/articles/cisa-g7-ai-software-bill-of-materials
[43] DoD CIO, Cybersecurity Risk Management Construct (24 Sep 2025). https://media.defense.gov/2025/Sep/24/2003808112/-1/-1/1/DOD-CIO-CYBER-SECURITY-RISK-MANAGEMENT-CONSTRUCT.PDF · FedTech summary: https://fedtechmagazine.com/article/2025/12/what-dods-cybersecurity-risk-management-construct
[44] DoD CIO DevSecOps library and change log. https://dodcio.defense.gov/Portals/0/Documents/Library/DoDEnterpriseDevSecOpsFundamentals.pdf · https://dodcio.defense.gov/Portals/0/Documents/Library/DoD%20Enterprise%20DevSecOps%20Change%20Log_DoD-CIO.pdf
[45] GovCIO Media, "Pentagon SWFT Responses Back Shift to Continuous Software Authorization" (2 Jan 2026). https://govciomedia.com/pentagon-swft-rfis-back-shift-to-continuous-software-authorization/ · DefenseScoop (Jun 2025): https://defensescoop.com/2025/06/09/katie-arrington-swft-software-fast-track/ · Anchore (vendor): https://anchore.com/blog/dod-swft-initiative-and-promise-of-cato-fulfilled
[46] FedRAMP 20x. https://www.fedramp.gov/20x/
[47] Kubernetes releases. https://kubernetes.io/releases/
[48] CNCF, "Cloud Native Computing Foundation Announces Kyverno's Graduation" (24 Mar 2026). https://www.cncf.io/announcements/2026/03/24/cloud-native-computing-foundation-announces-kyvernos-graduation/
[49] FIRST EPSS. https://www.first.org/epss/ · "Introducing EPSS v4": https://research.empiricalsecurity.com/research/introducing-epss-version-4
[50] CISA Known Exploited Vulnerabilities Catalog / BOD 22-01. https://www.cisa.gov/known-exploited-vulnerabilities-catalog (fetch failed this session; well-established)
[51] Infosecurity Magazine, "CISA Launches Roadmap for the CVE Program" (Sep 2025). https://www.infosecurity-magazine.com/news/cisa-launches-roadmap-cve-program/
[52] CycloneDX v1.7 release (21 Oct 2025). https://cyclonedx.org/news/cyclonedx-v1.7-released · ECMA-424: https://ecma-international.org/publications-and-standards/standards/ecma-424/
[53] NIST SP 800-204D (final, Feb 2024). https://csrc.nist.gov/pubs/sp/800/204/d/final
[54] NIST, SP 800-53 Release 5.2.0 (Aug 2025). https://www.nist.gov/news-events/news/2025/08/nist-revises-security-and-privacy-control-catalog-improve-software-update
[55] Version lookups performed 20 Oct 2026 via Go module proxy (https://proxy.golang.org/<module>/@latest), PyPI JSON API (https://pypi.org/pypi/<pkg>/json) and npm registry. Results: Trivy v0.76.0; Syft v1.55.0; Grype v0.121.0; Cosign v3.1.4; Gitleaks v8.30.1; TruffleHog v3.99.3; Kyverno v1.19.2; Gatekeeper v3.23.1; Notation v1.3.2; policy-controller v0.15.1; Argo CD v3.5.6; Flux v2.9.6; containerd v2.4.2; Podman v6.1.4 / v5.8.9; Docker Scout CLI v1.26.0; tfsec v1.28.14 (May 2025); External Secrets v1.3.2; Vault v1.21.4; OCI image-spec v1.1.1, runtime-spec v1.3.0, distribution-spec v1.1.1; Checkov 3.3.30; Semgrep 1.182.0; ModelScan 0.8.8; snyk-agent-scan 0.6.9; mcp-scan 0.4.3 (redirect); garak 0.17.1; promptfoo (npm) 0.124.1.
[56] (reserved; see [60])
[57] Sonar, "Sonar streamlines product naming." https://www.sonarsource.com/company/press-releases/sonar-streamlines-product-naming-to-reflect-core-mission-of-code-quality-and-security/
[58] GitHub Docs, Secret scanning and push protection. https://docs.github.com/en/code-security/secret-scanning (not re-fetched this session)
[59] Kubernetes Docs, Network Policies. https://kubernetes.io/docs/concepts/services-networking/network-policies/ (not re-fetched this session)
[60] Kubernetes Pod Security Standards. https://kubernetes.io/docs/concepts/security/pod-security-standards/ (not re-fetched this session)
[61] Docker Docs, Enhanced Container Isolation (Hardened Docker Desktop). https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/
[62] Docker Docs, Packet filtering and firewalls (incl. ufw incompatibility; nftables backend experimental). https://docs.docker.com/engine/network/packet-filtering-firewalls/ (fetched 21 Oct 2026)
[63] AWS, Amazon EKS Best Practices Guide: Security (shared responsibility). https://docs.aws.amazon.com/eks/latest/best-practices/security.html (fetched 21 Oct 2026)
[64] Google Cloud, Configure sandboxes for services (Cloud Run, Preview; page updated 13 Oct 2026). https://docs.cloud.google.com/run/docs/configuring/services/sandboxes
[65] Microsoft Learn, Networking in Azure Container Apps (workload profiles, UDRs, Azure Firewall, NAT Gateway). https://learn.microsoft.com/en-us/azure/container-apps/networking (fetched 21 Oct 2026)
[66] Google Cloud, Cloud Run execution environments. https://docs.cloud.google.com/run/docs/about-execution-environments
[67] Fly.io, "Firecracker vs gVisor: Sandbox Isolation for Untrusted and Agent-Generated Code" (vendor perspective). https://fly.io/learn/firecracker-vs-gvisor/ (fetched 21 Oct 2026)
[68] K3s Docs, Air-Gap Install. https://docs.k3s.io/installation/airgap
[69] AWS, Stateful domain list rule groups in AWS Network Firewall (TLS SNI / HTTP Host). https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-domain-names.html (fetched 21 Oct 2026)
[70] Google Cloud, Fully qualified domain name objects overview (Cloud NGFW). https://docs.cloud.google.com/firewall/docs/fqdn-objects-overview
[71] Docker Docs, Docker with iptables (DOCKER-USER chain). https://docs.docker.com/engine/network/firewall-iptables/ (fetched 21 Oct 2026)
[72] Cilium Docs, Locking Down External Access with DNS-Based Policies (toFQDNs). https://docs.cilium.io/en/stable/security/dns/ (fetched 21 Oct 2026)
[73] Google Cloud, Control Pod egress traffic using FQDN network policies (GKE). https://docs.cloud.google.com/kubernetes-engine/docs/how-to/fqdn-network-policies
