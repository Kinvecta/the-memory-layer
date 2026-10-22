# Lab 2: write a manual, test it with two tools (20 min)

**Goal:** a short operating manual for your own brain that two different AI tools both follow the same way.

**You need:**
- A copy of `brain-vault/` (or your own brain folder) under git.
- Two different AI tools that can read local files, for example a coding agent and a CLI agent.

## Steps

**A. Draft (6 min)**
1. Copy `AGENTS.template.md` to the root of your brain as `AGENTS.md`. If you're using the reference vault, compare yours with its `AGENTS.md`.
2. Fill the seven short sections. Stay under about 100 lines.
3. Write only what the AI can't discover by itself. Put the most important rules first.

**B. Point (3 min)**
1. Create `CLAUDE.md` and `GEMINI.md`, each containing only `@AGENTS.md`.
2. For Gemini CLI you can instead add AGENTS.md to `context.fileName` in `.gemini/settings.json`.
3. Run `brain-tools/install-skills.sh <your-brain>` so both tools can find the skills.

**C. Test (8 min)**
1. Copy `lab2-note.md` and `lab2-injection.md` into your `inbox/`.
2. Run the six prompts in `conformance-test.md` in both tools.
3. Use fresh sessions, started inside the folder.
4. Score each prompt.

**D. Fix (3 min)**
1. Change one rule for the worst failure.
2. Start a new session and re-run that prompt.

**Stretch:**
- Run `brain lint`. It now also flags hidden Unicode characters and a manual over 200 lines or 32 KB.
- Open `views/review.base` in Obsidian to see the review queue built from page properties.

## Files

- `AGENTS.template.md`: the manual template
- `conformance-test.md`: six prompts, pass criteria and a score sheet
- `lab2-note.md`: a normal note to ingest
- `lab2-injection.md`: a note with a planted instruction, which must not be followed
- `answer-key.md`: expected behavior, common failures and fixes (facilitator)
