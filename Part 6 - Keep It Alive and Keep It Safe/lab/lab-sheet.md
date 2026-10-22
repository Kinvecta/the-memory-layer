# Lab 6 · Lab sheet

Use a copy of your vault that is a git repo. If you only have the reference vault:

```bash
cp -R brain-vault ~/brain-copy && cd ~/brain-copy && git init -q && git add -A && git commit -qm baseline
export BRAIN_VAULT=~/brain-copy
```

## A. Run the heartbeat once by hand (4 min)

```bash
brain heartbeat --commit
git log --oneline -2 && git show --stat HEAD
```

1. Which files did the heartbeat change? ______________________________
2. Open `memory/reports/<today>.md`. How many lint issues? ______

## B. Put it on a schedule (5 min)

Pick your OS in `schedule-configs.md`. Load the job, then run it once now (`launchctl kickstart …` on a Mac).

3. Your Mac sleeps through 06:17 and you open the lid at 07:40. What happens with launchd? With cron?
   ______________________________
4. The laptop was **off** at 06:17. What happens? ______________________________

## C. Plant two bad clippings (5 min)

```bash
cp lab/planted-clip.md lab/invisible-ink.md "$BRAIN_VAULT/inbox/"
brain lint
brain heartbeat --commit --llm "echo reflect"
tail -1 "$BRAIN_VAULT/log.md"
```

5. Which line did lint flag in each file? ______________________________
6. Open `invisible-ink.md` in your editor. Can you see the hidden instruction? ______
7. Did the reflect step run? Why or why not? ______________________________

Shortcut: `python3 lab/lab6_check.py ~/brain-copy` does steps C and D in a temp copy and prints the result.

## D. Review like a human (4 min)

8. Delete the two clippings (they're attacks, not sources) and run `brain heartbeat --commit --llm "echo reflect"` again.
   Did reflect run this time? ______
9. Pick one wiki page. Add `review_after:` with a date in the past, run `brain lint`. Which section lists it? ______
10. Read `git show HEAD`. Name one change you would reject, or write "none". ______________________________

## E. Your rule (2 min)

11. Write the one sentence you'd put in your own `AGENTS.md` about what the nightly job may and may not change.
    ______________________________
