# Lab 1 answer key (facilitators)

## A. Baseline (no brain)

- **Q1:** a general tool may give *some* staged adoption model, but not this program's five stages. A good tool says it doesn't know this guide.
- **Q2:** the tool cannot know. A guess like "60 minutes" or a made-up series name is a hallucination. Point it out (Session 3).
- **Q3:** a generic answer at best. "Recall ladder" is this brain's term.

## B. With the brain

- **Q1:** the five stages are:
  1. chat with saved instructions
  2. calling the model through the API, in a container
  3. containerized workflows
  4. tool calling
  5. a harness with agents and skills

  Cites `[[five-stage-training-progression]]`, and may also cite `[[source-ai-training-guide]]`.
- **Q2:** each classroom part runs 90 minutes, and the series is called "The Memory Layer" (formerly the working title AI Brain Series). Cites `[[2026-10-21-series-named-the-memory-layer]]` and/or `[[the-memory-layer]]`. Core memory may answer this without opening a page.
- **Q3:** the rungs run cheapest first: core, index, search, links, raw. Each rung costs more input tokens, and everything in the context window is paid for on every turn. Cites `[[recall-ladder]]` and `[[tokens]]` or `[[context-window]]`.

## C. After ingesting lab-note.md

Expect a pass to look like this:
- a new source page in `wiki/sources/` (for example `source-lab-note-recall-ladder-check`)
- an update to `[[recall-ladder]]` with the pilot numbers, labeled as practice data
- possibly a decision page or a decision line
- an index line for each new page, and a new `ingest` line in `log.md`

Q3's answer should now cite the pilot numbers: 8 of 10 questions stopped at or before the index, and going straight to raw/ cost about 30k tokens versus about 6k. Look for whether the AI **kept the "practice data" label**. If it dropped the label, that is a teaching moment about provenance.

## Common snags

- **The tool started outside the vault**, so it never read AGENTS.md. Restart it inside the folder.
- **The tool edited `raw/`.** That breaks the schema. Point to AGENTS.md §2 and revert with `git checkout -- raw/`.
- **The tool created a duplicate concept page** instead of updating `recall-ladder`. Ask it to merge the two and run `brain lint`.
