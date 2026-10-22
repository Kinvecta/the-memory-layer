---
type: source
summary: Summary of the Session 5 transcript on calling the model through an API, choosing and configuring an endpoint, sealing the code in a container, and the four run controls (Stage 2).
sources: ["[[raw/transcripts/s5-apis-endpoints-and-containers]]"]
related: ["[[apis-and-endpoints]]", "[[containerization]]", "[[secrets-management]]", "[[five-stage-training-progression]]", "[[train-the-trainer-series]]", "[[source-s4-tokens-context-and-data]]", "[[source-s6-building-workflows]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 5 - APIs, Endpoints and Containers

**TL;DR:** Session 5 teaches Stage 2 of the [[five-stage-training-progression]]: once code calls the model through an API, your software becomes the harness and your team owns the controls. It covers the three kinds of endpoint, four config habits that make switching a one-line change, what a container allows and blocks, and four run controls. No coding is required; learners only need to know what to ask for.

**Source file:** [[raw/transcripts/s5-apis-endpoints-and-containers]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (series edition)

## Key points
1. **Learning goals** [0:27]: explain what changes when code calls the model; choose an endpoint and keep it in config; describe what a container allows and blocks; name the four run controls.
2. **Three problems that start the day code calls the model** [0:46]: "the key was in the script" (key leaks into code, repo and logs); "we can't switch vendors" (endpoint and model name hard-coded in fifty places); "nobody knows what ran" (no record of prompt, model version or reviewer).
3. **Through the API, your software becomes the harness** [1:14]. The flow: load the saved prompt from the library, add the document, build the request with a pinned model version, send to the endpoint named in config, receive a draft, log every call. The API is not the chat app: terms, data retention and authorization differ. See [[apis-and-endpoints]].
4. **Six jobs the chat app used to do, now owned by your code** [1:43]: instructions (saved prompt in the [[prompt-and-skill-library]]), data handling, logging, keys and network, review (a person signs), cost (limits per workflow).
5. **Three front doors to the same model** [2:10]: the vendor API, a cloud provider inside your cloud account, or the organization's approved platform/gateway. The model is the same; the contract changes, so "authorize first, then pick the model."
6. **Four config habits** [2:40]: endpoint in config, not code; pin the model version, never "latest"; one request shape for every door; allow-list that endpoint as the container's only permitted address.
7. **Containers** [2:57]: inside are the exact reviewed libraries, the code and saved prompt, and a key injected at run time. Only the call to the model endpoint passes; other websites and the host's own files are blocked, so an injected instruction "has nowhere to send your data." The same scanned image is authorized and redeployed, which speeds approvals. See [[containerization]], [[egress-control-and-firewalls]].
8. **Four run controls** [3:30]: key from the secrets store, never the code ([[secrets-management]]); pinned model version, switched on purpose after tests pass ([[ai-evals]]); audit log (who, which prompt, which model, how many tokens, who reviewed); cost meter that stops at a limit ([[tokens]]).
9. **What teams can do today** [3:56]: chat only = Stage 1; chat + API = Stages 2-3 (one call from code, and a workflow); tool calling adds Stage 4; agents and skills add Stage 5.
10. **Exercise** [4:30]: Part A, find five problems in a pseudocode snippet (the hard-coded key is the usual first find); Part B, fill a blank container for a weekly contract-summary workflow: contents, one endpoint, key source, what each run logs, rate and cost limit.
11. **Facilitator sandbox** [5:46]: pre-scanned base image, low-limit training keys, made-up sample documents, starter prompt library with test cases; build once, reset per group.

## Worth quoting
> "Through the API, your software becomes the harness." [1:14]

> "The contract is what changes, so authorize first, then pick the model." [2:10]

> "Your code becomes the harness, so your team owns the controls." [4:16]

## Pages this source updated
- [[apis-and-endpoints]]
- [[containerization]]
- [[secrets-management]]
- [[five-stage-training-progression]]
- [[agnostic-ai-platform]]
- [[train-the-trainer-series]]
