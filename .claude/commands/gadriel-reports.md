---
description: Generate all Gadriel compliance PDFs (one per pillar plus the umbrella report)
allowed-tools: Bash(gadriel:*)
---

# /gadriel-reports

Generate the full set of Gadriel compliance PDFs and drop them into
`.security/compliance/`. Each of the eight pillars produces its own report
(L1 input handling, L2 output handling, L3 data layer, L4 identity, AI, API,
container, config) and a top-level umbrella report rolls the per-pillar
findings into a single executive summary.

These PDFs are the artifacts auditors and compliance reviewers consume — the
underlying JSON in `.security/findings.json` is canonical, but the PDFs render
the same facts against the frameworks the team has opted into (EU AI Act,
NIST AI RMF, OWASP LLM Top 10, etc.). Re-run this command after each
significant scan so the committed PDFs stay in sync with the live findings.

The command takes no arguments. Output paths are deterministic so the PDFs
overwrite cleanly between runs and the git diff stays small.

## Usage

`/gadriel-reports`

## What this command does

1. Runs `gadriel code report --format pdf --all-pillars --fail-on render-only`.
2. Writes one PDF per pillar to `.security/compliance/<pillar>.pdf`.
3. Writes the umbrella report to `.security/compliance/umbrella.pdf`.
4. Re-emits framework-mapped reports (EU AI Act, NIST AI RMF, OWASP, etc.).
5. Prints the list of generated files with their sizes for quick review.

A PARTIAL compliance verdict is the normal state for any repo with open
findings; it is **not** a rendering failure. `--fail-on render-only` makes the
command exit 0 when the PDFs render successfully (reserving a non-zero exit for
a true rendering failure — missing template, typst error, no findings.json) so
the slash command completes cleanly instead of looking like it failed.

```bash
!gadriel code report --format pdf --all-pillars --fail-on render-only
```
