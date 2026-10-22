---
type: concept
summary: What a model API is, how it differs from the chat app, the three kinds of endpoint (vendor, cloud provider, approved platform), and the config habits and run controls that keep API use portable and safe.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]"]
related: ["[[ai-harness]]", "[[containerization]]", "[[secrets-management]]", "[[agnostic-ai-platform]]", "[[workflows]]", "[[five-stage-training-progression]]", "[[egress-control-and-firewalls]]"]
aliases: [API, application programming interface, model endpoint]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# APIs and Endpoints

**TL;DR:** An API lets your own software send requests to a model with no vendor chat app in between, which makes your software the harness and puts your team in charge of instructions, data handling, logging and security. The same model is reachable through three kinds of endpoint, chosen by authorization and data level first and by model second. Keep the endpoint in config, pin the model version, and allow-list only that endpoint.

## What it is
An API (application programming interface) is "a direct, programmatic way for software to send requests to a model and get responses back" ([[source-ai-training-guide]] §2.1). Examples: Anthropic's Claude API, the OpenAI API, Google's Gemini API, and cloud-hosted versions in approved regions. The common confusion is treating it as the consumer app: through an API "your own software becomes the harness," and terms, data retention and authorization differ from the chat apps ([[source-ai-training-guide]] §2.1; [[ai-harness]]).

## Why it matters
Session 5 names three problems that start the day code calls the model: a key pasted into the script ends up in the repo and logs; endpoint and model name hard-coded "in fifty places" block a vendor switch; and nobody knows which prompt, model version or reviewer produced a result ([[source-s5-apis-endpoints-and-containers]] [0:46]). The chat app used to do six jobs that your code now owns: instructions, data handling, logging, keys and network, review, and cost ([[source-s5-apis-endpoints-and-containers]] [1:43]).

## How it works
**Three front doors to the same model** ([[source-ai-training-guide]] §2.1):

| Endpoint | Examples | What it means |
|---|---|---|
| Vendor's own API | Claude API, OpenAI API, Gemini API | Vendor terms apply; security must approve the vendor directly; newest models arrive here first |
| Cloud provider's hosted version | AWS Bedrock, Azure OpenAI / Azure AI Foundry, Google Vertex AI | Runs inside a cloud boundary you may already have approved, with the same identity, logging and network controls; versions can lag the vendor |
| Approved platform or medium | Company AI platform or gateway, approved low-code tool | Several models behind one approved front door; still use a vendor-neutral schema to stay portable |

The model is identical; the contract is not, so "authorize first, then pick the model" ([[source-s5-apis-endpoints-and-containers]] [2:10]).

**Request flow:** load the saved prompt from the [[prompt-and-skill-library]], add the document, build the request with a pinned model version, send it to the endpoint named in config, receive a draft, log every call ([[source-s5-apis-endpoints-and-containers]] [1:14]).

**Four config habits** ([[source-s5-apis-endpoints-and-containers]] [2:40]): endpoint in config, not code; pin the model version, never "latest"; one request shape for every door; allow-list that endpoint as the container's only permitted address ([[egress-control-and-firewalls]]).

**Four run controls** ([[source-s5-apis-endpoints-and-containers]] [3:30]): key from the secrets store ([[secrets-management]]); pinned version switched only after tests pass ([[ai-evals]]); an audit log of who ran it, which prompt, which model, how many [[tokens]], and who reviewed; a cost meter that stops at a limit.

## In practice
- Stage 2 exercise: containerize a short script that sends one saved prompt plus a document and saves the answer; done when the container builds, reaches only the approved endpoint, and keys never appear in code or logs ([[source-ai-training-guide]] §5.1; [[five-stage-training-progression]]).
- Chat plus API already unlocks Stages 1-3, including scheduled [[workflows]] ([[source-ai-training-guide]] §2.1).
- Every API-calling script runs in a container ([[containerization]]); a hosted low-code tool relies on its own authorization instead.
- Foundation 6 of the [[agnostic-ai-platform]] is a workflow layer that speaks the OpenAI, Anthropic and Google request formats, so changing models is a configuration change.

> [!warning] Common Stage 2 mistake
> The API key in the script is the most common first find in the Session 5 code-review exercise ([[source-s5-apis-endpoints-and-containers]] [4:30]).

## See also
[[ai-harness]] · [[containerization]] · [[secrets-management]] · [[workflows]] · [[agnostic-ai-platform]]
