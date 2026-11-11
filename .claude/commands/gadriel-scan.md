---
description: Run a full Gadriel code security scan against the repo (or a scoped path)
allowed-tools: Bash(gadriel:*), Bash(jq:*), Bash(pwd)
argument-hint: [path]
---

# /gadriel-scan

Run the Gadriel code security scanner against the current repository, or scope
the scan to a specific path supplied as an argument. This is the headline entry
point for ad-hoc verification when a developer wants to confirm the repo is
clean before opening a PR.

The command shells out to the project-local `gadriel` binary (the same one the
git hooks and Claude Code hooks call), so results are identical to what CI will
see. Findings are written to `.security/findings.json` and pillar scores to
`.security/pillar-scores.json`; both are committed artifacts visible to the
team.

If `$ARGUMENTS` is empty, Gadriel scans the full repo from the project root. If
`$ARGUMENTS` is a relative path (e.g. `crates/gadriel-cli`), the scan is scoped
to that directory only — useful for tight feedback loops while iterating on a
single module.

## Usage

`/gadriel-scan [optional-path]`

Examples:

- `/gadriel-scan` — full repo scan
- `/gadriel-scan crates/gadriel-cli` — scoped scan
- `/gadriel-scan src/auth.rs` — single-file scan

## What this command does

1. Resolves the current working directory (project root).
2. Runs `gadriel code scan` against the repo, optionally scoped by `$ARGUMENTS`.
3. Streams scanner output inline so you can watch progress.
4. Writes findings + pillar scores to `.security/` for downstream tooling.
5. Exits non-zero only when a critical finding is detected (matches CI policy).

```bash
!gadriel code scan $ARGUMENTS
```
