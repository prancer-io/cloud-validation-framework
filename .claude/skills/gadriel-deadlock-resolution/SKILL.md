---
name: gadriel-deadlock-resolution
description: Multi-agent deadlock patterns — circular waits, supervisor-loop starvation, tool-contention. Auto-invoke for findings tagged `teamwork`, `deadlock`, `livelock`, `starvation`, or rule IDs `CODE-W1-AI-6**` where the graph contains cycles or shared mutexes.
---

# Deadlock Detection and Resolution

This skill teaches Claude to recognize the common deadlock, livelock, and starvation patterns in multi-agent systems, how Gadriel's graph scanner flags them, and how to resolve them via topology change or protocol change. Used by the `teamwork` pillar.

## When this skill activates

- Findings with tag `teamwork`, `deadlock`, `livelock`, `starvation`, `cycle`, `tool-contention`
- User phrasings: "agents stuck waiting", "supervisor loop", "no progress", "infinite handoff"
- File patterns: graph definitions (LangGraph, AutoGen), code with explicit locks/semaphores between agent threads, shared scratchpads, MCP servers acting as agent dispatchers

## Core concepts

- **Deadlock vs. livelock vs. starvation** — deadlock: no agent makes progress; livelock: agents make moves but no work completes; starvation: one agent never gets scheduled.
- **Coffman conditions** — mutual exclusion + hold-and-wait + no preemption + circular wait. Break any one to prevent deadlock.
- **Common multi-agent variants**:
  - **Handoff cycle**: A→B→A with no exit condition.
  - **Supervisor loop**: supervisor re-dispatches the same sub-task to the same agent on every failure.
  - **Tool-contention**: agents serialize on a single MCP tool / DB row / external API quota.
  - **Mutex over LLM call**: agent A holds a lock while waiting on a slow LLM call → B starves.
  - **Ack-wait**: A waits for B's ack, B waits for A's ack (peer mode without a tiebreaker).
- **Detection signals from logs** — same `correlation_id` re-entering the same agent > N times; same tool call repeating with identical args; per-agent inflight time growing unboundedly.
- **Timeouts are the universal cure** — any wait without a timeout is a potential deadlock.

## Detection patterns / cheatsheet

- Graph definition has a back-edge with no `should_continue` predicate and no `max_iterations`.
- Supervisor agent reads `last_message.role == "tool"` and unconditionally re-dispatches.
- Two agents acquiring two shared locks in different orders (classic AB/BA deadlock).
- Tool definition with a per-tool global lock (`with global_lock:`) instead of per-resource lock.
- `await asyncio.wait(...)` with no `timeout`.
- Retry policy `retry_forever` / `max_retries=infinity` on a flaky downstream.
- Two peer agents sending request envelopes to each other in parallel, each expecting a reply before responding.
- Shared state mutated under a lock that's held during a network call.

## Remediation playbook

1. Bound graph iterations: every cyclic graph has `max_steps` and an explicit exit condition (`if state.steps >= max_steps: return halt`).
2. Replace supervisor loops with bounded retries: `max_retries_per_subtask=3`; after that escalate to a human (`gadriel-hitl-patterns`).
3. Acquire locks in a fixed global order: assign each lock a numeric ID; always acquire low→high.
4. Don't hold locks across LLM/network calls — fetch the value under lock, release, then call out, then re-acquire to commit.
5. Add timeouts everywhere: every `await` has a deadline; every tool call has a timeout; every queue receive has a timeout.
6. For peer mutual-wait, introduce a tiebreaker (lexicographic agent ID, random priority) so one side proceeds.
7. Per-resource locks not per-tool: lock the row/key/object, not the entire endpoint.
8. Emit a "no-progress" alarm: if the same `correlation_id` is in-flight > N seconds, raise an incident; auto-cancel after 2N seconds.
9. Build a regression: a test that constructs a deliberate handoff cycle and asserts the orchestrator halts within `max_steps`.

## Diagnostic recipe

When a "stuck" report arrives, walk the steps in order:

1. Get the `correlation_id`; pull every audit-log row with that ID.
2. Build the message graph: nodes = agents, edges = sends. Look for cycles.
3. For each node, list `last_seen_at` and `last_tool_call`. A node with no `last_seen_at` movement for > expected SLA is the wait-point.
4. Identify what the wait-point is waiting on: another agent's ack, a tool result, a lock, a queue.
5. Apply the matching remediation from the playbook; resist the urge to "just restart" without recording the root cause.

## References

- Coffman et al. 1971 — System Deadlocks
- Akka / Erlang supervision-tree patterns
- LangGraph `should_continue` / `max_steps` patterns
- ADR-086 §D4 — skill assigned to `teamwork` agent
- Sibling skills: `gadriel-a2a-contracts`, `gadriel-graph-attack-patterns`, `gadriel-hitl-patterns`
