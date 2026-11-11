---
name: gadriel-output-schema-library
description: JSON Schema patterns for structured LLM output — strict schemas, refusal handling, retry-on-parse-fail, common gotchas. Auto-invoke for findings tagged `coherence`, `schema`, `structured-output`, or rule IDs `CODE-W1-AI-6**` where the agent emits machine-parsable output.
---

# Output Schema Library

This skill teaches Claude how to design strict JSON Schemas for structured LLM output (function calling, tool use, OpenAI's `response_format`, Anthropic's tool use), how to handle refusals, and how to recover from malformed output. Used by the `coherence` pillar.

## When this skill activates

- Findings with tag `coherence`, `schema`, `structured-output`, `parse-fail-loop`
- User phrasings: "JSON Schema for", "function calling schema", "why is the LLM output failing parse", "strict mode"
- File patterns: Pydantic models used as tool schemas, Zod schemas in TS tool definitions, raw JSON Schemas, OpenAPI specs reused for tool I/O

## Core concepts

- **Strict mode** — providers support a "strict" variant that constrains generation to the schema (OpenAI Structured Outputs, Anthropic tool use with `input_schema`). Use strict mode whenever the consumer is code, not a human.
- **Closed schemas** — `additionalProperties: false`, every property in `required`, no `anyOf` of dissimilar shapes. Strict mode often *requires* closed schemas.
- **Refusal carriers** — schemas should always allow the model to refuse: a top-level `refusal: string | null` field is the cleanest pattern.
- **Discriminated unions** — for multi-shape outputs (e.g., `action: "create" | "delete" | "update"`), use a string `discriminator` and `oneOf`; do not rely on shape-matching.
- **Field count discipline** — fewer fields → more reliable. If a schema has > 20 fields, split into two calls (extract, then enrich).
- **No `format` quirks** — `format: date-time` is well-supported; `format: email`, `format: uri` enforcement varies; do server-side validation.

## Detection patterns / cheatsheet

- `additionalProperties: true` (or unset) on a tool input schema — model may emit junk fields the parser accepts but downstream code ignores.
- Optional fields in a strict-mode call (`"optional"` in OpenAI strict) — strict mode requires all fields in `required`; mark unused as nullable.
- Schema uses `anyOf` across disparate shapes without a discriminator — frequent parse fail.
- Code calls `json.loads(llm_output)` without try/except and without a re-prompt retry path.
- Re-prompt loop has no max-iteration cap — runaway cost on persistent parse fail.
- Schema lacks a `refusal` field — model emits "I cannot..." in a string field, breaking type assumptions downstream.
- Numeric fields without `minimum`/`maximum` — model emits implausible values.
- Long enums with similar values — model confuses them; use distinct, short tokens.

## Remediation playbook

1. Enable strict mode at the provider level (`response_format: {type: "json_schema", strict: true}` or Anthropic tool with `input_schema`).
2. Make every schema closed: `additionalProperties: false`; list every field in `required`; use `["string","null"]` for optional.
3. Add a top-level `refusal` field: `{ "refusal": ["string","null"], ... }`. Branch on refusal before parsing the rest.
4. For multi-shape outputs, use a discriminator:
   ```json
   {"oneOf": [
     {"type":"object","required":["kind","data"],"properties":{"kind":{"const":"create"},"data":{"$ref":"#/$defs/Create"}}},
     {"type":"object","required":["kind","data"],"properties":{"kind":{"const":"delete"},"data":{"$ref":"#/$defs/Delete"}}}
   ]}
   ```
5. On parse fail: capture the malformed output, send a follow-up turn with the error message, retry once; on second failure escalate to human.
6. Cap retries (max 1-2) and budget cost (`max_tokens` per retry).
7. Validate with a real validator (`jsonschema` in Python, `ajv` in JS, `serde_json` + `schemars` in Rust) — don't trust the model's claim of validity.
8. Maintain a `schemas/` directory of reusable building blocks (Address, Money, Identifier, Refusal); compose schemas from these rather than inlining.

## Common reusable building blocks

Keep these in a shared `schemas/_lib.json`:

- `Refusal`: `{"type":"object","required":["refused","reason"],"properties":{"refused":{"const":true},"reason":{"type":"string"}}}`.
- `Identifier`: `{"type":"string","pattern":"^[A-Z0-9_-]{4,64}$"}`.
- `Money`: `{"type":"object","required":["amount_minor","currency"],"properties":{"amount_minor":{"type":"integer","minimum":0},"currency":{"enum":["USD","EUR","GBP"]}}}`.
- `Citation`: `{"type":"object","required":["doc_id","span"],"properties":{"doc_id":{"$ref":"#/$defs/Identifier"},"span":{"type":"array","items":{"type":"integer"},"minItems":2,"maxItems":2}}}`.

Compose these into per-task schemas instead of inlining; the model picks up the patterns and emits more reliably.

## References

- OpenAI Structured Outputs — https://platform.openai.com/docs/guides/structured-outputs
- Anthropic tool use — https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- JSON Schema 2020-12 — https://json-schema.org/draft/2020-12/release-notes
- ADR-086 §D4 — skill assigned to `coherence` agent
- Sibling skills: `gadriel-a2a-contracts`, `gadriel-token-cost-estimator`
