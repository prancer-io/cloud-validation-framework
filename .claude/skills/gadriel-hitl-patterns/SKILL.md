---
name: gadriel-hitl-patterns
description: Human-in-the-loop gate patterns — autonomy boundaries, approval gates, audit trails for high-impact actions. Auto-invoke for findings tagged `safety`, `autonomy-gate`, `hitl`, or rule IDs `CODE-W1-AI-6**` where the agent has high-impact tools (shell, financial, deletion).
---

# Human-in-the-Loop Patterns

This skill teaches Claude where in an agentic system a human approval gate belongs, what the gate must capture, and how to express it in code. Used by the `safety` pillar agent.

## When this skill activates

- Findings with tag `safety`, `autonomy-gate`, `hitl`, or `excessive-agency`
- User phrasings: "should this need approval", "what tools need a human", "autonomy levels", "kill switch"
- File patterns: code constructing agents with tool lists, especially `shell`, `bash`, `filesystem_write`, `http_post`, `transfer_*`, `delete_*`

## Core concepts

- **Reversibility scale** — most-reversible (read, draft email) → least-reversible (money transfer, prod DB delete, public post). HITL friction must scale with irreversibility.
- **Five autonomy levels** — (0) human does it, (1) agent suggests, (2) agent acts after approval, (3) agent acts then asks forgiveness, (4) agent acts in sandbox, (5) agent acts in prod autonomously. Most enterprise actions should sit at L2.
- **Gate captures four things** — what action is requested, why (model rationale), what's the blast radius (resources affected), what's the rollback path.
- **HITL fatigue** — gate everything and humans rubber-stamp; gate only the right things and humans engage. Use a budget-based policy.
- **Async gates** — for tools that wait minutes/hours, the gate is an outbox + approval API + callback; not an inline `input()`.

## Detection patterns / cheatsheet

- `agent = Agent(tools=[shell_tool, write_file_tool])` — no `require_human_approval=True` or equivalent.
- LangGraph node calling `human_approval` only on success path, not on tool-call path.
- MCP server exposes `delete_*`, `transfer_*`, or `execute_*` tools with no approval flow.
- Code path that writes to production DB / sends email / posts to Slack with no gate.
- "Auto-merge PR" or "auto-deploy on success" without a release-manager approval.
- Tool definitions where the same agent has both read-and-act capabilities on a sensitive resource (e.g., read PII + send email).
- Missing audit log of what the human approved (just a boolean is insufficient).

## Remediation playbook

1. Classify every tool by reversibility (R0 read-only, R1 idempotent write, R2 destructive, R3 financial/legal/safety).
2. Set policy: R0 no gate; R1 audit log only; R2 inline approval with rationale; R3 inline approval + second reviewer + 24h cool-down (configurable).
3. Standardize the gate envelope:
   ```json
   {
     "action_id": "uuid", "tool": "transfer_funds",
     "args": {...}, "rationale": "...",
     "blast_radius": ["account:xyz"], "rollback": "reverse_transfer(action_id)",
     "requested_by": "agent:billing-clerk", "model_id": "claude-...",
     "approved_by": null, "approved_at": null
   }
   ```
4. Persist envelopes to the same NDJSON audit log used by the security pillar.
5. For async gates, use an outbox table polled by a "approver" UI (Slack approve button, web dashboard); the agent thread blocks on a Future.
6. Add a kill-switch: a global flag that causes all R2/R3 actions to enter pending state regardless of agent autonomy config.
7. Re-prompt when approval is denied: include the human's reason in the next agent turn so the agent can adjust.
8. Test the gate path: a unit test that simulates an "R3 + no approver" scenario and asserts the agent stops, not loops.

## References

- EU AI Act Art. 14 (human oversight) — directly satisfied by this pattern
- NIST AI RMF MG-1.3, MG-2.3 — risk management functions
- Anthropic Agent SDK `human_in_the_loop` patterns
- ADR-086 §D4 — skill assigned to `safety` agent
- Sibling skills: `gadriel-eu-ai-act-mapper`, `gadriel-graph-attack-patterns`
