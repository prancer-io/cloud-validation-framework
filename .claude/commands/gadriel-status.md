---
description: Show the current Gadriel pillar verdict and finding counts
allowed-tools: Bash(gadriel:*), Bash(jq:*)
---

# /gadriel-status

Print a one-screen verdict of the repo's current security posture: the pillar
scores (from `.security/pillar-scores.json`), the open finding counts by
severity (from `.security/findings.json`), and the headline pass/fail gate that
CI will enforce.

This is the fastest way to answer the question "is this repo green?" without
running a full scan. The numbers come from the last persisted scan results, so
if you have just edited code, run `/gadriel-scan` first to refresh them.

The command prefers `gadriel code report --summary` when the binary is
available because the report subcommand applies the same severity-weighting
rules as CI. If `gadriel` is not on PATH, the fallback path reads the JSON
files directly with `jq` and prints a degraded summary so you still get
actionable numbers.

## Usage

`/gadriel-status`

## What this command does

1. Calls `gadriel code report --summary` to produce the verdict text.
2. Displays per-pillar scores (Pillars 1-8) with pass/fail markers.
3. Displays finding counts grouped by severity (critical / high / medium / low).
4. Surfaces the top 5 open findings as a quick triage list.
5. Exits 0 when the repo is green, non-zero when any critical finding is open.

```bash
!gadriel code findings
```
