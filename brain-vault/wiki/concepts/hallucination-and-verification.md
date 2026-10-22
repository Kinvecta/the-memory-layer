---
type: concept
summary: Hallucination is confident, fluent output that is false and a normal failure mode; this page covers why it happens, the claim-by-claim verification method, the six-item checklist, and why evaluation is the top-ranked skill gap.
sources: ["[[raw/transcripts/s3-safe-prompting-and-verification]]", "[[raw/transcripts/s1-what-an-llm-is]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[safe-prompting]]", "[[large-language-model]]", "[[ai-evals]]", "[[ai-governance-and-controls]]", "[[how-ai-finds-your-data]]", "[[measuring-training-results]]"]
aliases: [hallucination, verification, fact-checking AI output]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Hallucination and verification

**TL;DR:** A hallucination is confident, fluent output that is false, and it is a normal failure mode, not a rare one. The defense is to check every claim against the source before anything is used, with a named person signing off. Evaluating output and systems is the number-one focus area in the guide, and the most common team failure.

## What it is
- Glossary: "Confident, fluent output that is false." Common misuse: "Treated as rare; it is a normal failure mode that verification must catch" ([[source-ai-training-guide]] Glossary).
- Why it happens: an LLM generates the next token rather than looking things up, which makes it fluent and also "fluently wrong" ([[source-s1-what-an-llm-is]] [1:25]; [[large-language-model]]). Output also varies from run to run ([[source-s1-what-an-llm-is]] [2:47]).

## Why it matters
- Focus area #1: "Fluent but wrong answers reach briefings and decisions"; common gap: "Trusting confident tone; no test cases before release" ([[source-ai-training-guide]] §1.4).
- "The biggest mistake teams make is not evaluating AI output and workflows enough" ([[source-ai-training-guide]] §1.4, From the field).
- Unverified output is one of the three top risks, alongside data in the wrong system and prompt injection ([[source-ai-training-guide]] §1.1).
- As output gets faster and more fluent, "the scarce skill is testing whether it is right before it is used" ([[source-ai-training-guide]] §1.3).

## How verification works
Session 3's demo: a well-written draft with five claims is checked against the source memo. Date: right. Budget: wrong (source 4.2 million, draft 2.4 million). Approver's name: not in the source at all. Quote: right. Vendor count: right. Two of five claims fixed before anyone used them ([[source-s3-safe-prompting-and-verification]] [3:42]).

### The checklist
1. **Sources:** does each claim come from the material you gave it?
2. **Numbers.**
3. **Names and dates.**
4. **Quotes**, word for word.
5. **What is missing:** anything the source said that the draft left out.
6. **Tone and bias**, especially when output is about people.

Source: [[source-s3-safe-prompting-and-verification]] [4:13].

It is the second check in the safe-use flow: if the draft fails, revise and run again; then a named person signs off ([[safe-prompting]]).

## Reducing hallucination upstream
- Paste the source instead of asking the model to recall facts ([[safe-prompting]]).
- Ground with tools: a skill can say "pull the contract value from the system, never from the document text," replacing a guess with a cited record ([[source-ai-training-guide]] §3.4).
- Totals come from a structured query, not a model reading rows; check numbers read off charts and scans ([[how-ai-finds-your-data]]).
- The most important line in a good skill is its verification step ([[source-ai-training-guide]] §3.4).

## From individual checks to system evals
Verification is the person-level habit; [[ai-evals]] are the system-level version: every saved prompt, skill and workflow keeps sample inputs with known-good outputs plus one tricky case, and must pass before others use it and after any prompt or model change ([[source-ai-training-guide]] §5.2). "Errors caught in review" is a training measure ([[measuring-training-results]]). For agents, review the steps, not just the final answer ([[source-ai-training-guide]] §5.2).

## In practice
Session 3 exercise: find the three errors in an AI summary of a short memo, rewrite the prompt as a briefing, and check every claim in the new draft. Ask: what did your check catch? ([[source-s3-safe-prompting-and-verification]] [5:23]).

## See also
[[safe-prompting]] · [[ai-evals]] · [[large-language-model]] · [[source-s3-safe-prompting-and-verification]]
