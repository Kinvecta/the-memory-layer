# Lab 6 · Answer key

1. `log.md` (one heartbeat line), `memory/reports/<today>.md`, and, if working memory was older than
   12 hours, a new file in `memory/episodes/`. Nothing in `raw/`, `wiki/` or `memory/core.md`.
2. Whatever your vault shows. The reference vault reports 0 issues.
3. launchd runs the job at 07:40 when the Mac wakes. cron skips it.
4. Both skip it. launchd only catches up after sleep, not after power-off.
5. `planted-clip.md` line 7 (`ignore your previous instructions`, an injection suspect) and
   `invisible-ink.md` line 4 (hidden characters, `U+E0020`, the first tag character).
6. No. Line 4 looks like a normal bullet. The instruction is written in tag characters that most editors
   don't draw, but a model can read them.
7. No. The report says `reflect step was skipped` and the log line ends `reflect skipped (quarantined)`.
   While lint flags hidden characters or instruction-like lines, the heartbeat won't hand the vault to an agent.
8. Yes. With the clippings gone, lint is clean and reflect runs (here `echo reflect`, return code 0).
   If a flagged file is a legitimate source that quotes an attack, keep it and list it in
   `memory/reviewed-flags.md` after you have read it yourself.
9. `review due` (and `stale` too if `last_reviewed` is older than 90 days).
10. Look for: edits to `raw/` or `memory/core.md` (never allowed), claims with no `sources:`, deleted text
    instead of `status: superseded` or `status: disputed`, and anything that reads like an instruction.
11. Example: "The nightly job may update `wiki/`, `memory/working.md` and `inbox/` with cited proposals;
    it never edits `raw/` or `memory/core.md`, never uses network tools, and a person reviews every commit."

Expected output of `lab6_check.py`: see `expected-output.txt`.
