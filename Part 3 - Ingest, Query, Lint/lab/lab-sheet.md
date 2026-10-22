# Lab 3 · Ingest, query, lint, undo (20 min)

Work in a **copy** of the reference vault (`brain-vault/`) or your own brain, with the Part 2 manual and skills installed. Start your AI tool **inside** that folder.

## Setup (once)

```bash
cd brain-vault            # your copy
git init && git add -A && git commit -m "init"     # skip if it is already a git repo
brain index               # optional: refresh search
```

## A · Ingest (6 min)

1. Copy `part2-transcript.md` from this lab folder into `inbox/`.
2. Ask your AI tool: **"Ingest inbox/part2-transcript.md."**
3. Note the 3–5 takeaways it states before it writes anything.
4. When it finishes: `git add -A && git commit -m "ingest: part2-transcript"` (skip if the skill already committed).

## B · Check (3 min)

1. `git show --stat HEAD`. Count: source pages ___, updated pages ___, new pages ___.
   Expected shape: **1 source page · 3–8 updates · 0–3 new pages**, plus one line in `index.md` and one in `log.md`.
2. Open **two** new citations. Does the transcript really say that? ☐ yes ☐ no (which?)

## C · Query (4 min)

Ask both questions. Every point should carry a `[[citation]]`.

- **Q1** "What goes in a brain's AGENTS.md, and what stays out?"
- **Q2** "How do the manual, the skills and the token budget fit together?"

Save the one that needed synthesis: **"Save that answer to wiki/questions."** Then ask it again. Reads before ___, after ___.

## D · Lint (3 min)

1. Run `brain lint`.
2. Fix **one** mechanical issue (broken link, missing index line, missing frontmatter).
3. Write down **one** judgment issue for a person to decide: ________________
4. Commit: `git commit -am "lint: fixed 1"`.

## E · Undo (4 min)

1. Copy `clipped-page.md` into `inbox/` and ask: **"Ingest inbox/clipped-page.md."**
2. `git show HEAD`. Find the wrong date and the hidden instruction. Did the AI obey it? ☐ no (good) ☐ yes (stop, and tell the facilitator)
3. Undo it: `git revert HEAD --no-edit`
4. `git log --oneline -5`: both the ingest and its revert are in the history.

## Debrief

- How many pages did the ingest touch? Did any citation fail the check?
- Which lint finding needed a person, not a script?
