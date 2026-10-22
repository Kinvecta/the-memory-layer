# Lab 4 · Index, score, fix (20 min)

You need:

- a copy of `brain-vault/` (work in the copy, not the original);
- `brain-tools` installed: `pip install -e brain-tools`;
- optionally, Ollama with the embedding model: `ollama pull nomic-embed-text`.

No Ollama? Do every step anyway. The meaning and hybrid columns will repeat keyword, so compare your results with a neighbour who has Ollama.

## A · Index (4 min)

```
brain --vault ~/brain-copy index --no-embed     # keyword index only, a few seconds
brain --vault ~/brain-copy index                # adds vectors (Ollama running); first run takes several minutes
brain --vault ~/brain-copy stats
```

Write down the number of files, chunks and chunks with vectors.

## B · Score (7 min)

```
python3 run_eval.py ~/brain-copy golden.csv
```

For each question, record the rank of the right page in each mode (`-` means it was not in the top 20). Then record recall@5 and MRR for each mode.

| Measure | What it tells you |
|---|---|
| recall@5 | How many of the 6 questions had the right page in the top 5 |
| MRR | The average of 1/rank: rank 1 scores 1, rank 2 scores 0.5, a miss scores 0 |

## C · Explain (3 min)

Pick one row where the modes disagree. Explain the difference in one sentence, in terms of **words** vs. **meaning**.

## D · Fix (4 min)

`crawl walk run` is the team's nickname for the five-stage training path, and every mode misses it.

1. Open `wiki/concepts/five-stage-training-progression.md`.
2. Add `crawl walk run` at the **end** of its `aliases:` list.
3. Run `brain index` (only one file changes).
4. Run `run_eval.py` again.

What changed for row 6? What changed in the totals?

## E · Extend (2 min)

Add one real question you would ask your own brain to `golden.csv`, with the page that should answer it. Score it.

**Debrief:** Which mode won on which kind of question? What did one alias change?
