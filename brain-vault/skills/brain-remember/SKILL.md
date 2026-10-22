---
name: brain-remember
description: Capture a durable fact, decision, preference or open thread into working memory during a session. Use when the user says "remember", "note that", "we decided", or when a session produces something future sessions need.
---

# Remember

1. Write a single self-contained line that still makes sense months from now. Name the subject and give
   the date context, for example: "Deep Dive C will be split into 4 parts (decided 2026-10-21)."
2. Pick a kind: `fact`, `decision`, `preference`, `todo` or `observation`.
3. Run `brain remember "<line>" --kind <kind>`, or call `brain_remember` over MCP.
4. **Decisions** also deserve a page. Create `wiki/decisions/<yyyy-mm-dd>-<slug>.md` from
   `templates/decision.md`, add it to the index, and log it.

**Do not capture:** routine steps, things already in the wiki, secrets, or personal details about other
people. Over-capturing buries the signal.

At session end, run `brain archive --title "<what this session was about>"`. That moves working memory
into `memory/episodes/`.
