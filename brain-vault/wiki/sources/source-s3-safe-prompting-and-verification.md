---
type: source
summary: Transcript summary of Session 3, covering the one rule for data, the accidental-paste response, briefing-style prompts, claim-by-claim verification with a six-item checklist, and saving prompts to the team library.
sources: ["[[raw/transcripts/s3-safe-prompting-and-verification]]"]
related: ["[[source-ai-training-guide]]", "[[train-the-trainer-series]]", "[[safe-prompting]]", "[[hallucination-and-verification]]", "[[prompt-and-skill-library]]", "[[ai-governance-and-controls]]", "[[source-s4-tokens-context-and-data]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source: Session 3 - Safe Prompting and Verification

**TL;DR:** Session 3 of the [[train-the-trainer-series]] (about 6.5 minutes) teaches the everyday habits of safe use: data passes an approval check, the AI gets a proper briefing, the draft is verified claim by claim, and a named person signs off. Verification gets the most time because it is the number-one gap teams have.

**Source file:** [[raw/transcripts/s3-safe-prompting-and-verification]]  ·  **Kind:** transcript  ·  **Date:** October 2026

## Key points
1. **Why** [0:44]: problems start with habits. Fluent is not correct; one bad paste of confidential data or personal information can end a program; vague in, vague out.
2. **The one rule and safe-use flow** [1:11]: data only goes into a tool approved for its sensitivity level. Check 1: is the tool approved for this data? If not, switch tools before writing a prompt. Check 2: does the draft pass verification? If not, revise and rerun. Then a named person signs off. "Two checks. One sign-off." See [[safe-prompting]].
3. **Data levels grid** [1:47] (example only; each organization has its own): public can go almost anywhere; internal only in an approved enterprise tool; sensitive (personal, confidential, controlled) only in a tool approved for that level.
4. **Accidental paste** [2:14]: stop (don't keep chatting or paste more), report to your security or privacy contact, record what was shared, in which tool, and when, then follow the incident process. "A quiet delete can make it worse."
5. **Three duties** [2:37]: human accountability (named reviewer for anything used in a decision), records and transparency (labeling; prompts and outputs can be records), responsible use (bias checks, escalation). Short version: AI drafts, a person signs. See [[ai-governance-and-controls]].
6. **Briefing prompt** [3:02]: role, task, audience, format, source. Example: contracting specialist, list every deliverable and due date, for the program manager, as a table, from the attached document. Then refine with short follow-ups. Pasting the source matters most.
7. **Verification demo** [3:42]: a fluent draft with five claims; the budget was wrong (source said 4.2 million, draft said 2.4) and the approver's name was not in the source. Two of five claims fixed. See [[hallucination-and-verification]].
8. **Checklist** [4:13]: sources, numbers, names and dates, quotes word for word, what is missing, tone and bias.
9. **Save what works** [4:32]: header (name, purpose, owner, inputs, approved data level), second-person review, tests with known-good outputs plus one tricky case such as a planted instruction, publish to the library, reuse; changes to prompt or model go back through review. See [[prompt-and-skill-library]].
10. **Exercise** [5:23]: find three errors in an AI summary, rewrite "summarize this" as a briefing, verify, then save it as an instruction with two test cases.

## Worth quoting
> Right tool for the data. Brief it like a teammate. Check every claim. And a person signs.

> That's what hallucination looks like in practice: confident, fluent, and false.

> Reporting early is what limits the damage. A quiet delete can make it worse.

## Pages this source updated
- [[safe-prompting]], [[hallucination-and-verification]], [[prompt-and-skill-library]], [[ai-governance-and-controls]]
