---
name: gadriel-a2a-contracts
description: Agent-to-agent contract patterns — ack/timeout, idempotency keys, message versioning, signed envelopes. Auto-invoke for findings tagged `teamwork`, `a2a`, `agent-contract`, or rule IDs `CODE-W1-AI-6**` where the AST shows agent-to-agent message passing.
---

# Agent-to-Agent Contracts

This skill teaches Claude the *contract* patterns that make multi-agent message passing reliable: how to define a stable envelope, how to make handlers idempotent, how to time-out cleanly, and how to evolve message shapes without breaking peers. Used by the `teamwork` pillar.

## When this skill activates

- Findings with tag `teamwork`, `a2a`, `agent-contract`, `idempotency`, `message-versioning`
- User phrasings: "agent message format", "should agents retry", "how do I version this message", "agent handshake"
- File patterns: code defining agent message types (Pydantic, Zod, protobuf), LangGraph state schemas, CrewAI Task→Agent dispatch, MCP envelope construction

## Core concepts

- **Stable envelope** — every cross-agent message has the same outer shape: `{message_id, correlation_id, from, to, ts, ttl_ms, version, payload}`. The payload schema may evolve; the envelope must not.
- **At-least-once delivery + idempotency** — assume the network/retry layer will deliver duplicates; make handlers idempotent on `message_id`.
- **Ack and timeout** — every send has a deadline. If no ack by `ts + ttl_ms`, the sender treats the send as failed and the receiver MUST drop late acks.
- **Version negotiation** — `version: "1.2"`; receivers MUST refuse `1.3` if they don't support it; senders SHOULD downgrade if they detect peer version is `1.1`.
- **Signed envelopes** — when agents cross trust boundaries (different processes, different orgs), the envelope is signed; receiver verifies signature against a peer registry.
- **No shared mutable state** — agents communicate via messages; they do not reach into each other's scratchpad. State sharing is explicit, versioned, and audited.

## Detection patterns / cheatsheet

- Cross-agent call passing raw strings, no envelope — no correlation/idempotency/timeout possible.
- Handler doesn't dedupe on `message_id` — duplicate delivery causes double-effects.
- No `ttl_ms` / no timeout — caller hangs on a wedged receiver.
- No `version` field — schema evolution breaks all peers at once.
- Same `correlation_id` reused across logically separate flows — observability becomes ambiguous.
- Receiver mutates sender's state object directly (shared dict, shared graph state) — race conditions and audit gaps.
- Signed envelopes verifying with a key fetched dynamically from a URL on each call — DoS / TOCTOU surface; key should be pinned/cached.
- Acks include sender's payload data — leaks information; acks should be receipt-only.

## Remediation playbook

1. Define the envelope once in a shared crate / package; every agent imports it; never inline.
   ```typescript
   type Envelope<P> = {
     message_id: string; correlation_id: string;
     from: AgentId; to: AgentId;
     ts: string; ttl_ms: number; version: string;
     signature?: string;
     payload: P;
   };
   ```
2. Make handlers idempotent: persist `(message_id, result)` in a small KV with TTL; on duplicate, return cached result without re-running side effects.
3. Enforce timeouts: caller uses `AbortSignal` / `tokio::time::timeout`; receiver checks `now > ts + ttl_ms` and drops on expiry.
4. Version with semver; receivers expose `supported_versions` and refuse unknown majors; senders implement a negotiation handshake on first contact.
5. Sign cross-boundary envelopes with Ed25519; pin peer public keys in a peer-registry file (`.gadriel/peers.json`); rotate via versioned key updates.
6. Generate one `correlation_id` per user request and propagate through every cross-agent message; logs become a clean tree.
7. Make state sharing explicit: a "shared store" agent owns reads/writes; other agents send `read`/`write` envelopes; never share Python dicts.
8. Acks carry only `{message_id, status, ts}` — no payload echo.
9. Add a contract-test gate: a peer-version compatibility matrix run in CI.

## References

- AsyncAPI 3.0 — https://www.asyncapi.com/docs/reference/specification/v3.0.0
- CloudEvents spec — https://cloudevents.io/
- ADR-086 §D4 — skill assigned to `teamwork` agent
- Sibling skills: `gadriel-deadlock-resolution`, `gadriel-output-schema-library`, `gadriel-graph-attack-patterns`
