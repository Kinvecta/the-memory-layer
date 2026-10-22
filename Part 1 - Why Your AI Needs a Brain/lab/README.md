# Lab 1: The same questions, with and without a brain (25 min)

**Goal:** see the difference between an AI with no memory and the same AI pointed at a brain. Then watch the brain grow by one source.

**You need:**
- Any AI tool that can read and write local files: a coding agent, a desktop chat app with a files connector, or an IDE assistant.
- A **copy** of `../../brain-vault/`. Don't work in the master copy.
- Optional: Obsidian, to open the vault copy and watch pages change.

**Data rule:** use only the vault and `lab-note.md`. Don't paste in real work data.

## Setup (before the timer)

```bash
cp -R "../../brain-vault" ~/memory-layer-lab-vault
cd ~/memory-layer-lab-vault && git init -q && git add -A && git commit -qm "lab start"
```

## A. Baseline (5 min)

Open your AI tool **outside** the vault, with no files attached. Ask the three questions in `questions.md`. Write down each answer and whether the tool sounded sure.

## B. With the brain (8 min)

1. Start the same tool **inside** `~/memory-layer-lab-vault`, so it reads `AGENTS.md`.
2. Ask the same three questions.
3. Open every `[[citation]]` it gives. Does the page say what the answer claims?

## C. Feed it (8 min)

1. Copy `lab-note.md` into the vault's `inbox/` folder.
2. Ask: "Ingest inbox/lab-note.md following skills/brain-ingest/SKILL.md."
3. Ask question 3 again. What changed, and which page does it cite now?
4. Read the last lines of `log.md`, then run `git diff --stat`.

## D. Debrief (4 min)

- Which answers changed between A and B?
- Did every citation hold up?
- How many pages did one note touch in step C?

## Stretch

From `../../brain-tools`:

```bash
pip install -e .
brain --vault ~/memory-layer-lab-vault search "recall ladder tokens"
brain --vault ~/memory-layer-lab-vault lint
```
