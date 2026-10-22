# Lab 6 · Scheduling the heartbeat

Replace `/ABSOLUTE/PATH` with your own paths. Start with the deterministic heartbeat (no `--llm`). Add the
reflect step only after you have reviewed a few runs by hand.

## macOS: launchd (recommended on a Mac)

Copy `brain-tools/examples/com.brain.heartbeat.plist` to `~/Library/LaunchAgents/`, edit the paths, then:

```bash
plutil -lint ~/Library/LaunchAgents/com.brain.heartbeat.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.brain.heartbeat.plist
launchctl kickstart gui/$(id -u)/com.brain.heartbeat     # run it once now
launchctl bootout gui/$(id -u)/com.brain.heartbeat       # remove it again
```

`StartCalendarInterval` behaviour: if the Mac is **asleep** at the scheduled time, launchd runs the job when it
wakes, and several missed times collapse into one run. If the Mac is **off**, that run is skipped.

## Linux: cron

```cron
15 6 * * *  cd /ABSOLUTE/PATH/brain-vault && /ABSOLUTE/PATH/.venv/bin/brain heartbeat --commit >> .heartbeat.log 2>&1
```

cron does not catch up: a run missed while the machine was asleep or off is skipped.

## Windows: Task Scheduler

```bat
schtasks /create /tn BrainHeartbeat /sc daily /st 06:15 /tr "C:\brain\.venv\Scripts\brain.exe --vault C:\brain\brain-vault heartbeat --commit"
```

To catch up after a missed run, open the task and tick **Run task as soon as possible after a scheduled start is missed**.

## Adding the reflect step safely

```bash
brain heartbeat --commit --llm 'claude -p --allowedTools "Read,Edit,Write"'
```

- Allow only file tools. No network, email, web or fetch tools in this session.
- Lint must be clean: while hidden characters or injection-like lines are flagged, the heartbeat skips reflect.
- Reflect proposes; it never edits `raw/` or `memory/core.md`. Core changes arrive as `inbox/core-proposal-<date>.md`.
- `--commit` gives you one commit per night. Review it with `git show`, and undo it with `git revert`.
- Check your tool's current docs for headless flags; they change often.
