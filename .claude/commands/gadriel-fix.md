---
description: Propose and apply a remediation for a specific Gadriel finding by ID
allowed-tools: Bash(gadriel:*), Bash(jq:*)
argument-hint: <FINDING-ID>
---

# /gadriel-fix

Apply (or propose) a remediation for a specific Gadriel finding. The finding ID
is required and should match the canonical rule code emitted by the scanner —
for example `CODE-W1-L1-001`, `CODE-W1-AI-636`, or `CODE-W3-CONFIG-218`.

Gadriel looks up the rule's remediation playbook (sourced from the skill
library under `.claude/skills/gadriel-*/`), suggests a concrete edit, and —
when the rule supports it — applies the edit directly. Every fix attempt is
appended to `.security/audit/audit-log.jsonl` so the team has a reviewable
trail of automated changes.

If you call this command without an argument, Gadriel prints the usage hint
and lists the top open findings so you can pick one.

## Usage

`/gadriel-fix <FINDING-ID>`

Examples:

- `/gadriel-fix CODE-W1-L1-001` — fix a SQL injection finding
- `/gadriel-fix CODE-W1-AI-636` — fix an AI-prompt-injection finding
- `/gadriel-fix CODE-W3-CONFIG-218` — fix a config hardening finding

## What this command does

1. Validates `$ARGUMENTS` looks like a Gadriel finding ID.
2. Looks up the finding in `.security/findings.json` to confirm it is still open.
3. Loads the matching remediation skill from `.claude/skills/gadriel-*/SKILL.md`.
4. Proposes (and, when safe, applies) the fix via `gadriel code fix`.
5. Re-runs the scoped scan to confirm the finding is resolved.
6. Appends the attempt to `.security/audit/audit-log.jsonl`.

```bash
!gadriel code fix $ARGUMENTS
```
