---
type: concept
summary: How to judge whether AI training worked - five measures (time saved, errors caught, library reuse, workflows in production, security findings) with baselines taken before training, plus evals before every release.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s6-building-workflows]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[five-stage-training-progression]]", "[[ai-evals]]", "[[prompt-and-skill-library]]", "[[workflows]]", "[[train-the-trainer-series]]", "[[ai-training-guide]]"]
aliases: [training metrics, measuring results]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Measuring Training Results

**TL;DR:** "Training succeeds when work changes, not when courses finish." Track a handful of work measures from the first cohort, with baselines taken before training starts: time saved per task, errors caught in review, library reuse, workflows in production, and security findings. Every prompt, skill and workflow also passes its own tests before release and after any change.

## What it is
The measurement plan in Part 5 of the [[ai-training-guide]] ([[source-ai-training-guide]] §5.2):

| Measure | How to collect it | Why it matters |
|---|---|---|
| Time saved per task | Time a repeat task before and after, per workflow or saved prompt | The clearest case for leadership and funding |
| Errors caught in review | Count corrections reviewers make to AI-assisted products | Shows whether verification habits work |
| Library reuse | Number of saved prompts and skills, and how often other teams run them | Know-how is spreading, not staying with one person |
| Workflows in production | Count of scheduled workflows with review steps | Progress past Stage 1 |
| Security findings | Data-handling slips, blocked connections, failed skill reviews | Where retraining is needed |

The leadership summary compresses this to four: time saved per task, errors caught in review, library reuse, workflows in production ([[source-ai-training-guide]] §1.1).

## Why it matters
One of three ways AI programs stall is that "courses end at Stage 1. People finish training, but nobody checks whether the work changed" ([[source-s8-agents-skills-and-running-the-program]] [0:46]). Leaders also tend to see demos rather than business outcomes; focus area 7 is explaining AI to leadership with outcomes and timelines ([[source-ai-training-guide]] §1.4). Time saved per run is how a workflow "builds the case for wider adoption" (§5.2).

## How it works
1. **Baselines first.** Time the task by hand before training or before the workflow goes live ([[source-s6-building-workflows]] [5:00]).
2. **Track after numbers.** Session 8 illustrates with explicitly example figures: time per report 6h -> 2h; corrections in review 9 -> 3; library reuse 0 -> 4 teams; workflows in production 0 -> 2 ([[source-s8-agents-skills-and-running-the-program]] [4:32]).
3. **Add security findings** alongside productivity measures.
4. **Evals before release.** Every saved prompt, skill and workflow keeps a small test set - sample inputs with known-good outputs plus at least one tricky case such as a planted instruction - and must pass it before others use it and again after any prompt or model version change ([[source-ai-training-guide]] §5.2; [[ai-evals]]).

## In practice
- Leaders' Stage 1 success criterion: name one pilot with a success measure ([[five-stage-training-progression]]).
- Session 8 exercise: plan one pilot - the workflow, which roles go to which stage, three measures with baselines, and a review date. "If any of your measures counts courses instead of work, swap it out" ([[source-s8-agents-skills-and-running-the-program]] [5:21]).
- Series close: pick one pilot workflow, take baselines, stand up the shared [[prompt-and-skill-library]], run Stage 1 for everyone, and put the review date in the calendar.
- Stored eval results over time double as drift monitoring for the [[agnostic-ai-platform]].

> [!tip] Rule to remember
> "Write it once, as a skill. Gate what leaves. Measure what changes."

## See also
[[ai-evals]] · [[five-stage-training-progression]] · [[workflows]]
