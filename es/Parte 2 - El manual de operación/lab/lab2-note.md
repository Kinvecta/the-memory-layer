# Team note: instruction files across tools

Captured 2026-10-21 during the Part 2 workshop.

- We keep one operating manual, AGENTS.md, at the root of the brain.
- CLAUDE.md and GEMINI.md contain a single import line, `@AGENTS.md`, and nothing else that conflicts with it.
- Procedures live in `skills/`; `install-skills.sh` copies them into `.claude/skills/` and `.agents/skills/`.
- Decision: the manual stays under 200 lines. Any rule that hasn't changed behavior in a month gets deleted at the monthly review.
- Owner of the manual: the brain's maintainer. Changes go through git, reviewed like code.
