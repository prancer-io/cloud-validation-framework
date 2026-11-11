---
name: gadriel-owasp-llm-top10
description: OWASP LLM Top 10 (2025) catalog with detection patterns and remediations. Auto-invoke for findings tagged `owasp-llm-*`, `prompt-injection`, `insecure-output-handling`, or rule IDs `CODE-W1-AI-*`, when the user asks about "LLM vulnerabilities", "prompt injection", or "model security".
---

# OWASP LLM Top 10 — Detection and Remediation

This skill teaches Claude to recognize each entry in the OWASP Top 10 for LLM Applications (2025 revision), how Gadriel detects them, and what remediation pattern to propose. Auto-invokes from the `security` pillar agent when the finding's `primary_rule_id` matches `CODE-W1-AI-*` or when the user explicitly asks about LLM/agent security.

## When this skill activates

- Finding IDs matching `CODE-W1-AI-6**` (AI-native rule range from the W1 rule pack)
- Tags: `owasp-llm-top10`, `llm01`..`llm10`, `prompt-injection`, `model-dos`, `training-data-poisoning`
- User phrasings: "is my LangChain pipeline safe", "can someone jailbreak this prompt", "LLM CVE", "prompt smuggling"
- File patterns: `*.py` importing `langchain`, `crewai`, `llama_index`; `*.ts` importing `@anthropic-ai/sdk` or `openai`; `*.yaml` with `mcp_servers` keys

## Core concepts

- **LLM01 Prompt Injection** — adversary content overrides instructions. Two sub-classes: direct (in user input) and indirect (in retrieved documents, web pages, tool outputs).
- **LLM02 Insecure Output Handling** — LLM output piped to `eval`, `os.system`, SQL, or rendered raw in a browser. Output is untrusted; treat it like user input.
- **LLM03 Training Data Poisoning** — adversary-controlled corpora bias the fine-tune or RAG index.
- **LLM04 Model DoS** — context-window exhaustion, unbounded recursion, unbounded tool loops.
- **LLM05 Supply Chain** — malicious model weights, poisoned PyPI packages, typosquat HuggingFace repos.
- **LLM06 Sensitive Information Disclosure** — system-prompt leaks, embedding inversion, memorized PII.
- **LLM07 Insecure Plugin Design** — LLM-callable tools without authz, parameter validation, or rate limits.
- **LLM08 Excessive Agency** — agents with shell, filesystem, or unrestricted HTTP without HITL gates.
- **LLM09 Overreliance** — production decisions on un-verified LLM output, especially in code suggestions.
- **LLM10 Model Theft** — exfiltration of proprietary weights, prompt templates, or fine-tune artifacts.

## Detection patterns / cheatsheet

- **LLM01 direct**: `f"{system_prompt}\n{user_input}"` with `user_input` from request body; missing delimiter sanitization.
- **LLM01 indirect**: tool output (web fetch, file read, MCP) concatenated into prompt without a `{{retrieved_content}}` sandbox tag and untrusted-content marker.
- **LLM02**: `subprocess.run(llm_response, shell=True)`, `eval(llm_response)`, `db.execute(llm_response)`, `innerHTML = llm_response`.
- **LLM03**: RAG ingestion of unsigned/unverified sources; fine-tune scripts pointing at HF datasets without `revision=` pin.
- **LLM04**: unbounded `while not stop_token` loops; tool-call recursion without `max_steps`; `max_tokens` unset on completion APIs.
- **LLM05**: `pip install <typo>`, models loaded from non-allowlisted hubs, `trust_remote_code=True` on `transformers.AutoModel`.
- **LLM06**: prompts containing `${OPENAI_API_KEY}` or `BEGIN PRIVATE KEY`; system prompts echoed in `assistant` messages.
- **LLM07**: tool definitions missing `schema`, returning raw `os.popen` output, or exposing `delete_*` / `transfer_*` operations.
- **LLM08**: agents with `tools=[bash_tool, filesystem_tool]` and no `require_human_approval` gate.
- **LLM09**: code-generation pipelines auto-merging PRs, LLM output written directly to `.tf` or `.yaml` without review.
- **LLM10**: model files served behind unauthenticated S3, signed-URLs with TTL >24h, weight files in public artifact repos.

## Remediation playbook

1. Wrap retrieved content in explicit untrusted-content delimiters (e.g. `<untrusted-document>`) and instruct the model to refuse instructions found inside.
2. Treat all LLM output as untrusted: pass through schema validation (Pydantic/Zod) before any downstream use; never `eval`/`exec`.
3. Pin model and dataset revisions with cryptographic hashes; reject `trust_remote_code=True`.
4. Set hard ceilings: `max_tokens`, `max_steps` (agent loops), `max_tool_calls_per_turn`, request-rate per user.
5. Require HITL gates on any tool that writes outside a sandbox, executes code, or moves money/credentials.
6. Redact secrets and PII from prompts before transport (ADR-090 redaction layer).
7. Log every prompt/response pair into an append-only audit log; embed for later anomaly detection.
8. Map each finding to the corresponding `LLM0x` ID in `compliance_controls` so the EU AI Act / NIST mapper skills can re-use it.

## References

- OWASP Top 10 for LLM Applications 2025 — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Gadriel rule pack `CODE-W1-AI-*` (see `docs/scenarios/code-security/` for canonical scenarios)
- ADR-086 §D4 — skills library wiring
- ADR-090 — privacy/redaction interface
