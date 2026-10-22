---
type: concept
summary: Safe everyday AI use - the one rule (data only into a tool approved for its sensitivity), the two-checks-one-sign-off flow, what to do after an accidental paste, and how to write a briefing-style prompt and save it.
sources: ["[[raw/transcripts/s3-safe-prompting-and-verification]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[hallucination-and-verification]]", "[[prompt-and-skill-library]]", "[[ai-governance-and-controls]]", "[[five-stage-training-progression]]", "[[prompt-injection]]", "[[large-language-model]]"]
aliases: [prompting, the one rule, briefing prompt, safe-use flow]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Safe prompting

**TL;DR:** Safe prompting is four habits: right tool for the data, brief the AI like a new teammate, check every claim, and a person signs. The one rule every trainee must know cold is that data only goes into a tool approved for that data's sensitivity level. Prompts that work get saved, reviewed and tested in the team library.

## The one rule
> [!warning] The one rule
> Data only goes into a tool approved for that data's sensitivity level ([[source-ai-training-guide]] §4.1).

Example data-level grid (each organization has its own): public information can go almost anywhere; internal information only in an approved enterprise tool; sensitive information (personal, confidential or controlled) only in a tool approved for that level ([[source-s3-safe-prompting-and-verification]] [1:47]). The rule is applied through existing data sensitivity levels, not a new scheme ([[source-ai-training-guide]] Appendix).

## Why it matters
"One bad paste of confidential data or PII can end a program"; data handling is focus area #2, with the gap "people unsure what is allowed on which system" ([[source-ai-training-guide]] §1.4). Clear task framing is #4: "vague one-line asks, then giving up." Most AI problems at work start with a habit, not the technology ([[source-s3-safe-prompting-and-verification]] [0:44]).

## How it works: the safe-use flow
1. Data has a sensitivity level.
2. **Check 1:** is this tool approved for this data? If not, switch tools before writing a prompt.
3. Write the prompt; the AI drafts.
4. **Check 2:** does the draft pass verification ([[hallucination-and-verification]])? If not, revise and rerun.
5. A named person signs off.

"Two checks. One sign-off" ([[source-s3-safe-prompting-and-verification]] [1:11]; [[source-ai-training-guide]] §4.1).

## After an accidental paste
**Stop** (don't keep chatting or paste more to fix it). **Report** to your security or privacy contact right away. **Record** what was shared, in which tool, and when. **Follow** your incident process. "A quiet delete can make it worse" ([[source-s3-safe-prompting-and-verification]] [2:14]).

## Three duties that come with the rule
AI drafts; a person signs ([[source-s3-safe-prompting-and-verification]] [2:37]; [[source-ai-training-guide]] §4.1):
- **Human accountability:** outputs used in decisions need a named reviewer.
- **Records and transparency:** some work must be labeled AI-assisted; prompts and outputs can be records (and subject to FOIA rules).
- **Responsible use:** bias checks on outputs that affect people; know the escalation path.

## Writing a briefing prompt
Give the AI what a new teammate would need ([[source-ai-training-guide]] §5.2; [[source-s3-safe-prompting-and-verification]] [3:02]):
- **Role, task, audience, format**, plus the **source**.
- Paste the source material instead of asking it to recall facts; this matters most.
- Ask for a draft, then refine: "shorter," "add the regulation numbers," "rewrite for a GS-15."
- Example: "You are a contracting specialist. Using the attached SOW, list every deliverable with its due date in a table."

A prompt is "really a task brief," not a magic phrase ([[source-ai-training-guide]] Glossary).

## Save what works
A working prompt becomes a saved instruction: header (name, purpose, owner, inputs, approved data level), second-person review, tests with known-good outputs plus one tricky case such as a planted instruction, publish, reuse ([[source-s3-safe-prompting-and-verification]] [4:32]). See [[prompt-and-skill-library]]. This is the Stage 1 outcome in [[five-stage-training-progression]].

## In practice
Session 3 (90 minutes in the course map) exercise: rewrite "summarize this" as a briefing, run it in an approved tool, verify, then save it with two test cases ([[source-s3-safe-prompting-and-verification]] [5:23]; [[source-ai-training-guide]] §5.2). Once AI reads documents or uses tools, treat their content as untrusted ([[prompt-injection]]).

## See also
[[hallucination-and-verification]] · [[prompt-and-skill-library]] · [[ai-governance-and-controls]] · [[source-s3-safe-prompting-and-verification]]
