# Security policy

## Status

This repository is course material for **The Memory Layer** training series. It is **not actively maintained**, has no supported versions and makes no security guarantees. Content and dependencies may be outdated, and dependencies may come to include known vulnerabilities. Review and scan anything you reuse.

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private reporting instead: go to the **Security** tab and choose **Report a vulnerability**. Reports are read on a best-effort basis, with no response or fix timeline.

## What the repository does to lower risk

- No secrets, credentials, personal data, audio or video are committed. Every push and pull request is checked with a Gitleaks scan of the full history.
- `brain-tools` dependencies are audited with `pip-audit` on every push and weekly. Dependabot raises alerts and update PRs for Python packages and GitHub Actions.
- CodeQL scans the Python and JavaScript on every push and weekly.
- Third-party GitHub Actions are pinned to full commit SHAs, and workflows run with read-only tokens by default.

## Safe use of the brain tools

- Run the MCP server over `stdio` for a single user. Only use streamable HTTP behind localhost binding, origin checks and authentication.
- The server can write only to `wiki/` and `inbox/`, and it labels every read as data, not instructions. Keep those guardrails if you change it.
- Never store secrets in the vault. A synced vault is a copy of your data.
