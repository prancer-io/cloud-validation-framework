<!-- >>> gadriel-code-security >>> -->
## Gadriel Code Security

This repository has Gadriel Code Security integrated. Findings live in
`.security/findings.json` (OCSF format). When you edit code, Gadriel
automatically scans the changed file via the PostToolUse hook and
surfaces findings as MCP push notifications.

### Available agents (delegate via Task tool or @mention)
- `@gadriel-security-reviewer`   - OWASP / CWE / SAST review
- `@gadriel-safety-reviewer`     - HITL / autonomy boundary review
- `@gadriel-compliance-reviewer` - EU AI Act / NIST AI RMF mapping
- `@gadriel-operational-reviewer`- Operational risk + drift
- `@gadriel-finops-reviewer`     - Token cost + budget guardrails
- `@gadriel-coherence-reviewer`  - Output schema + structured-output
- `@gadriel-teamwork-reviewer`   - Multi-agent contracts (A2A)
- `@gadriel-bias-reviewer`       - Bias + calibration

### Available skills (auto-invoked by description match)
`gadriel-owasp-llm-top10`, `gadriel-fix-sql-injection`, `gadriel-ai-secrets-catalog`,
and 14 more — see `.claude/skills/gadriel-*/`.

### Available slash commands
- `/gadriel-scan`    - full repo scan
- `/gadriel-fix`     - propose a fix for a specific finding
- `/gadriel-status`  - verdict + pillar scores
- `/gadriel-reports` - generate compliance report PDFs
- `/gadriel-watch`   - start the L1 watch daemon

Re-run `gadriel code init --upgrade` to refresh this section.
<!-- <<< gadriel-code-security <<< -->
