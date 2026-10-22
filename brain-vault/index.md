---
type: index
updated: 2026-10-21
---
# Index

The catalog of this brain. **Read this first**, pick the 1–3 pages whose summaries fit, and open only those. One line per page: `[[page]] — summary`.

## Start here
- [[the-memory-layer]] — The Memory Layer - a standalone training playlist on building a second brain in markdown/Obsidian that any LLM harness can recall from, founded on the AI Training Guide and Train-the-Trainer material.
- [[2026-10-21-ai-brain-series-standalone]] — The Memory Layer is a standalone playlist (not part of Train-the-Trainer), seeded with the training guide and series material as founding knowledge, built to the full retrieval stack.
- [[2026-10-21-series-named-the-memory-layer]] — The second-brain playlist is named "The Memory Layer" (formerly AI Brain Series), with 90-minute classroom parts.
- [[llm-wiki-pattern]] — The LLM Wiki pattern - an LLM maintains a linked markdown wiki compiled from immutable raw sources, navigated through an index instead of a vector database.
- [[agent-memory-layers]] — The four memory layers of an AI second brain - core, working, episodic and semantic - and the heartbeat job that promotes facts between them.
- [[recall-ladder]] — The recall ladder - the cheapest-first order an AI uses to find knowledge in the brain (core.md, index.md, search, links, raw/) and why stopping early saves tokens.
- [[ai-training-guide]] — The AI Training Guide for Teams Adopting Generative AI (October 2026 edition) - a tool- and industry-agnostic guide in PDF, HTML and Markdown, organized in five parts plus glossary and appendix, that the train-the-trainer series is built from.
- [[train-the-trainer-series]] — The train-the-trainer video series built from the AI Training Guide - Sessions 1-8 plus Deep Dive A (build an MCP server) and Deep Dive B (DevSecOps containers and CI/CD), each produced as a slide deck and narrated video with a transcript.
- [[five-stage-training-progression]] — The guide's five-stage training path ordered by how much control the AI has - chat with saved instructions, API in a container, containerized workflows, tool calling, and harness with skills - with exercises, exit criteria, risks and how far each role goes.

## Foundations — what the model is and what it sees
- [[large-language-model]] — What a large language model (LLM) is, how it is made, what it is not (six common myths), and why it is only one of several models inside a harness.
- [[chatbot-workflow-agent]] — How to tell a chatbot, a workflow and an agent apart using one test (who picks each step), with examples, risks, and when to choose a workflow over an agent.
- [[ai-harness]] — The harness is the app or platform around a model (interface, instructions, memory, permissions, tool loop, logging) that decides what the model can see and do; covers the six harness types and how to size one up.
- [[tokens]] — What a token is (about four characters or three-quarters of a word), the eight token types and how each is priced as of Oct 2026, and why tokens drive cost, capacity, speed, rate limits, quality and model portability.
- [[context-window]] — The context window is the fixed token budget a model can consider at once, shared by input and output; covers what fills it, why long chats get expensive and forgetful, and how caching, retrieval and progressive disclosure keep it lean.
- [[how-ai-finds-your-data]] — The six ways AI fetches data (whole context, semantic, keyword, agentic, structured, multimodal), which finder fits each data type, how major products retrieve as of Oct 2026, and why an index is a copy of your data.
- [[embeddings-and-vector-search]] — How embedding models turn text and images into vectors for semantic search (classic RAG), what they are good and bad at, the role of rerankers, embedding token costs, and why the embedding model is baked into every index.

## Safe use and verification
- [[safe-prompting]] — Safe everyday AI use - the one rule (data only into a tool approved for its sensitivity), the two-checks-one-sign-off flow, what to do after an accidental paste, and how to write a briefing-style prompt and save it.
- [[hallucination-and-verification]] — Hallucination is confident, fluent output that is false and a normal failure mode; this page covers why it happens, the claim-by-claim verification method, the six-item checklist, and why evaluation is the top-ranked skill gap.
- [[ai-governance-and-controls]] — The governance layer of the AI Training Guide: the one rule (data only goes into a tool approved for its sensitivity level), human accountability, operational controls (secrets, audit logs, version pinning, rate limits), per-component build and run-time controls, and the frameworks behind them as of Oct 2026.
- [[prompt-injection]] — Prompt injection is when instructions hidden in content the AI reads take over its behavior; OWASP ranks it the number-one LLM risk, and it is stopped by layered defenses and by removing one of three ingredients.

## Building with AI — API to agents
- [[apis-and-endpoints]] — What a model API is, how it differs from the chat app, the three kinds of endpoint (vendor, cloud provider, approved platform), and the config habits and run controls that keep API use portable and safe.
- [[workflows]] — A workflow is a fixed, designer-defined sequence of steps that may call a model; covers how to pick one, the six-step anatomy, validation, safe runs and release habits (Stage 3).
- [[tool-calling]] — Tool calling lets a model ask for a function to fetch facts or take actions while the harness checks, runs and logs it; read tools run freely, action tools wait for a person, and every result is data.
- [[model-context-protocol]] — MCP is the open JSON-RPC standard (current revision 2026-07-28, governed by the Linux Foundation's AAIF) for plugging tools, resources and prompts into any harness through host, client and server roles.
- [[building-an-mcp-server]] — How to build a current (2026-07-28 spec, v2 SDK) MCP server safely, using the ticket-desk example: tight schemas, a confirm-first action, stderr logging, Inspector tests, tool-list snapshots, OAuth without token passthrough, and a 12-point hardening checklist.
- [[ai-agents]] — An AI agent pursues a goal by choosing its own steps and using tools in a plan-act-check loop; covers when to use one, Stage 5 guardrails (container, logging, approval gates, step review) and common misuse of the term.
- [[agent-skills]] — Agent skills are SKILL.md folders of instructions, templates and scripts that a harness loads only when a task matches; covers anatomy, progressive disclosure costs, portability across harnesses, supply-chain risk and why skills plus tools make a harness powerful.
- [[prompt-and-skill-library]] — The one shared, version-controlled, reviewed and tested library of saved prompts and skills that every chat, script, workflow and harness pulls from, plus how a saved prompt becomes a skill.

## Owning the platform — resilience and DevSecOps
- [[ai-resilience]] — AI resilience means an organization can swap the model, endpoint, harness or whole vendor without rebuilding its work; covers the four levels of switch, the rent-vs-own split, myths about being agnostic, and the "no evals, no switch" playbook.
- [[agnostic-ai-platform]] — The seven foundations an organization owns - approved MCP tools, containers, scanning, skills, approved packages, a multi-vendor API workflow framework, and stored evals - that let it swap models or vendors without rebuilding its work.
- [[containerization]] — Why every harness and model-calling workflow runs sealed in a container image identified by digest, what a container allows and blocks, and where containers run.
- [[container-hardening]] — How to harden a container image for an AI workload: minimal base pinned by digest, multi-stage build, no secrets in layers, non-root, read-only filesystem and dropped capabilities.
- [[devsecops-pipeline]] — The DevSecOps loop and gated CI/CD line every AI component (MCP server, workflow, harness) passes through, from commit to runtime monitoring, shipping one signed digest.
- [[image-scanning-and-sbom]] — How pipelines scan code, dependencies, config and container images at several stations, build an SBOM inventory, and triage findings with KEV, EPSS, CVSS and VEX.
- [[image-signing-and-provenance]] — How signing an image by digest, attaching SBOM/provenance/scan attestations, and enforcing admission control prove the running box is the one that was scanned and built by your pipeline.
- [[secrets-management]] — Where API keys and other secrets belong for AI workloads: in a secrets manager with workload identity, injected at run time, rotated and audited, never in images, repos, prompts or logs.
- [[egress-control-and-firewalls]] — Layered, default-deny network controls in both directions for AI containers, with an egress proxy hostname allow-list so a prompt-injected agent can reach only the LLM API and approved backends.
- [[ai-evals]] — Evals are versioned test sets for every prompt, skill and workflow that gate release, re-run on any model or prompt change and on a schedule, and store results to catch model and use-case drift.

## Running the program
- [[measuring-training-results]] — How to judge whether AI training worked - five measures (time saved, errors caught, library reuse, workflows in production, security findings) with baselines taken before training, plus evals before every release.

## Comparisons
- [[container-base-image-options]] — Side-by-side of container base image families as of Oct 2026 (Docker Hardened Images, Chainguard, distroless, Red Hat UBI, Iron Bank, Bitnami, Alpine/Debian-slim) with cost, hardening and when to pick each.
- [[mcp-transports-stdio-vs-http]] — Side-by-side of MCP's two current transports, stdio for one local user and streamable HTTP for shared or remote servers, with security differences, common errors and a decision guide (HTTP+SSE is deprecated).

## Decisions
- _(none yet — the brain-query skill saves good answers here)_

## Sources (one per raw file)
- [[source-ai-training-guide]] — Summary of the October 2026 AI Training Guide for Teams Adopting Generative AI, its five parts, glossary and appendix, and which roles should read which sections.
- [[source-containers-cicd-brief]] — Research brief (version-checked 20 Oct 2026) behind Deep Dive B covering containers, hardening, scanning tools, signing, the CI/CD pipeline, AI-specific gates, government context, run locations and firewalls.
- [[source-dda-build-an-mcp-server]] — Summary of the Deep Dive A transcript, a hands-on build of the "ticket-desk" MCP server on the July 2026 spec and v2 SDKs, covering primitives, wire format, confirmation, transports, testing, OAuth, threats and release lifecycle.
- [[source-ddb-devsecops-containers-cicd]] — Transcript of Deep Dive B, a ~19-minute narrated session on shipping AI workloads as one hardened, scanned, signed container image through a gated CI/CD line with default-deny networking.
- [[source-mcp-build-brief]] — Summary of the research brief (verified 20 Oct 2026) behind Deep Dive A, covering the 2026-07-28 MCP spec, v2 SDK versions, transports, OAuth authorization, real MCP incidents, a 12-point hardening checklist and change control.
- [[source-s1-what-an-llm-is]] — Transcript summary of Session 1, which defines a large language model, the parts of an AI system, the six harness types, and the chatbot vs. workflow vs. agent test.
- [[source-s2-ai-resilience]] — Transcript summary of Session 2, which defines an agnostic organization, the seven foundations it owns, the four levels of switch, evals for model and use-case drift, and the "no evals, no switch" playbook.
- [[source-s3-safe-prompting-and-verification]] — Transcript summary of Session 3, covering the one rule for data, the accidental-paste response, briefing-style prompts, claim-by-claim verification with a six-item checklist, and saving prompts to the team library.
- [[source-s4-tokens-context-and-data]] — Transcript summary of Session 4, covering what a token is, token types and costs, how the context window fills, why long chats get expensive, and the six finders AI uses to fetch data.
- [[source-s5-apis-endpoints-and-containers]] — Summary of the Session 5 transcript on calling the model through an API, choosing and configuring an endpoint, sealing the code in a container, and the four run controls (Stage 2).
- [[source-s6-building-workflows]] — Summary of the Session 6 transcript on building fixed AI workflows (Stage 3) - picking a first task, the six-step workflow anatomy, validation checks, safe containerized runs, test-then-version releases and four success measures.
- [[source-s7-tools-mcp-and-prompt-injection]] — Summary of the Session 7 narrated video transcript covering tool calling, how MCP plugs tools into any harness, prompt injection and its three ingredients, and the six layered defenses.
- [[source-s8-agents-skills-and-running-the-program]] — Summary of the Session 8 (final) transcript on skills and progressive disclosure, treating skills as code, combining skill + tools + model, agent guardrails, the shared library, and running the program by stage, role and measure.
- [[source-second-brain-research-brief]] — Summary of the Oct 2026 research brief on building an LLM-readable second brain - the LLM Wiki pattern, memory layers, recall tiers, cross-harness portability and pitfalls.

## Saved answers
- _(none yet — the brain-query skill saves good answers here)_
