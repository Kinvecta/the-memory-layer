---
name: brain-ingest
description: Turn a new source in raw/ or inbox/ into linked wiki pages, then update index.md and log.md. Use when the user adds a document, transcript, article or notes to the brain, or says "ingest", "file this" or "add this to my brain".
---

# Ingest a source

**Goal:** read a source once, then spread what it teaches across the wiki. Afterward, any harness can
recall it from the index without rereading the source.

## Steps

1. **Place it.** If the source is in `inbox/` or was pasted into chat, save it under `raw/<kind>/` with a
   kebab-case name, such as `raw/articles/karpathy-llm-wiki.md`. Do not change files that are already in `raw/`.
2. **Read and discuss.** Read the whole source. Before writing anything, tell the user its 3–5 key
   takeaways and ask whether anything should be emphasized or skipped. Skip this step when running unattended.
3. **Source page.** Create `wiki/sources/<name>.md` from `templates/source.md`. Include the TL;DR,
   the key points with section references, quotes worth keeping, and `sources: ["[[raw/...]]"]`.
4. **Touch the graph.** For each concept, entity or decision the source covers:
   - First run `brain search "<term>"`. **If a page exists, update it.** Add the new claim with a
     citation, bump `updated:`, and add the source to `sources:`.
   - Create a new page from the matching template only when nothing fits.
   - If the new claim conflicts with an existing one, keep both and add a `> [!warning] Conflict` callout.
   - Link every touched page back to the source page, and to each other where related.
5. **Index.** Add one line per new page to `index.md` under the right heading, in the form
   `- [[page]] — summary`. Update the line of any page whose summary changed.
6. **Log.** Append one line to `log.md`, in the form
   `ingest · <source> · created N, updated M pages`.
7. **Re-index and check.** Run `brain index`, then `brain lint`. Fix any broken links you introduced.
8. **Commit** if this is a git repo: `ingest: <source>`.

## Quality bar

- Every claim is cited.
- No page repeats another. Link to it instead.
- Summaries in frontmatter are one sentence and specific enough to tell pages apart in the index.
- A 2,000-word transcript usually yields 1 source page, 3–8 concept or entity updates, and 0–3 new pages.
