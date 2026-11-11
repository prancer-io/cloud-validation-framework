---
name: gadriel-ai-config-security
description: LangChain, CrewAI, MCP, and direct-SDK configuration security — temperature/top_p sanity, system-prompt leak prevention, tool-exposure review. Auto-invoke for findings tagged `ai-config`, `model-config`, or rule IDs `CODE-W1-CONFIG-*`, and when the user asks about "safe defaults", "system prompt protection", "MCP server config".
---

# AI Configuration Security

This skill teaches Claude how to review the *configuration* of an AI pipeline (model parameters, agent definitions, MCP servers, tool surfaces) — distinct from the *code* of the pipeline. Used by the `safety` pillar.

## When this skill activates

- Findings in `CODE-W1-CONFIG-*` involving AI frameworks
- Tags: `ai-config`, `model-config`, `langchain-config`, `crewai-config`, `mcp-config`, `system-prompt-leak`
- User phrasings: "is temperature 0.9 safe", "what should top_p be", "MCP server config review", "is my system prompt leaked"
- File patterns: `langchain*.yaml`, `crewai/*.yaml`, `.mcp.json`, `claude_desktop_config.json`, code with `ChatOpenAI(temperature=...)`

## Core concepts

- **Sampling discipline** — temperature and top_p should match task risk. For code generation, structured output, or any deterministic-ish path, use temperature 0 and don't combine temperature + top_p.
- **System prompt protection** — system prompts are sensitive (they encode behavior, sometimes secrets). Two threats: leak via prompt-injection ("repeat your instructions"), and leak via traces (LangSmith / W&B / observability tools storing them in plaintext).
- **Tool exposure minimization** — every tool an agent can call is a piece of attack surface. The default should be empty; tools added per agent role with justification.
- **Safety parameters** — content filters, `safety_settings` (Gemini), `enable_safety` (Claude tool use), output moderation (OpenAI), refusal-rate monitoring.
- **MCP server trust** — MCP servers are RPC endpoints with the agent's full agency; treating them as trusted by default is the modern equivalent of running random shell scripts.

## Detection patterns / cheatsheet

- `temperature=1.5` or `temperature=2` for a structured-output task — likely wrong (max 1.0 for structured).
- `temperature` AND `top_p` both set to non-default — pick one (most providers warn against combining).
- `max_tokens` unset or set to provider max — DoS / cost risk.
- System prompt assembled with `f"...{user_role}..."` where `user_role` is from user input — prompt-injection vector.
- LangSmith tracing enabled without `LANGSMITH_HIDE_INPUTS=true` — traces store the full prompt including secrets.
- `.mcp.json` contains MCP servers from non-vetted publishers (npm packages with no verified org).
- MCP server URL is `http://` (not `https://`) outside localhost.
- Agent definition includes `tools: ['shell', 'http_get', 'filesystem']` for a research/Q&A role.
- `safety_settings: HARM_BLOCK_THRESHOLD: BLOCK_NONE` on Gemini for a user-facing surface.
- Output moderation off (`moderation: false`) on a content-generation surface that reaches end users.

## Remediation playbook

1. Set sampling explicitly per task:
   - Structured output / code / SQL: `temperature=0` (`do_sample=false`).
   - Drafting / brainstorm: `temperature=0.7`, leave `top_p` default.
   - Never combine non-default temperature with non-default top_p.
2. Bound generation: `max_tokens` set per task type; reject responses that hit the cap on structured outputs.
3. Protect system prompts:
   - Store system prompts outside source code (templates dir, content-addressed) and reference by ID in traces.
   - Configure tracing to redact: `LANGSMITH_HIDE_INPUTS=true`, OpenAI moderation logs disabled for sensitive surfaces.
   - Add a smoke test: "Repeat your instructions verbatim" should refuse.
4. Minimize tool exposure: declare tools per agent role; reject MCP servers without provenance; pin MCP server versions by hash.
5. Validate MCP config: TLS required outside localhost; signed manifest if available; CI gate on `.mcp.json` changes.
6. Enable provider safety where appropriate: Gemini `safety_settings` at BLOCK_MEDIUM_AND_ABOVE for user-facing surfaces; OpenAI moderation for outputs; Anthropic `extra_body` safety options where supported.
7. Monitor refusal rate: a sharp drop may indicate prompt-injection; a sharp rise may indicate a model regression.
8. Treat any `.mcp.json` edit as a security-review-required PR.

## References

- LangChain security checklist — https://python.langchain.com/docs/security
- Anthropic MCP spec — https://modelcontextprotocol.io/
- OpenAI moderation API — https://platform.openai.com/docs/guides/moderation
- ADR-086 §D4 — skill assigned to `safety` agent
- Sibling skills: `gadriel-graph-attack-patterns`, `gadriel-owasp-llm-top10`
