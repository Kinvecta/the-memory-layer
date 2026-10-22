"""Score a golden set against brain search in three modes.

Usage:  python3 run_eval.py <vault> golden.csv
golden.csv columns: question, expected (part of the page path), type
Prints the rank of the expected page in each mode (- = not in the top 20),
then recall@5 and MRR (mean of 1/rank) per mode. Needs brain-tools installed.
"""
import csv, json, subprocess, sys

vault, gold = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(gold, encoding="utf-8")))
MODES = ("keyword", "semantic", "hybrid")


def pages(q, mode):
    out = subprocess.run([sys.executable, "-m", "brain.cli", "--vault", vault, "--json",
                          "search", q, "-k", "20", "--mode", mode],
                         capture_output=True, text=True, check=True).stdout
    seen = []
    for hit in json.loads(out):
        if hit["path"] not in seen:
            seen.append(hit["path"])
    return seen


tot = {m: [0, 0.0] for m in MODES}
print(f"{'question':40} {'kw':>4} {'sem':>5} {'hyb':>4}   expected")
for r in rows:
    cells = []
    for m in MODES:
        rk = next((i + 1 for i, p in enumerate(pages(r["question"], m)) if r["expected"] in p), None)
        tot[m][0] += bool(rk and rk <= 5)
        tot[m][1] += 1 / rk if rk else 0
        cells.append(str(rk or "-"))
    print(f"{r['question'][:40]:40} {cells[0]:>4} {cells[1]:>5} {cells[2]:>4}   {r['expected']}")
n = len(rows)
print()
for m in MODES:
    hits, rr = tot[m]
    print(f"{m:9} recall@5 {hits}/{n}   MRR {rr / n + 1e-9:.2f}")
