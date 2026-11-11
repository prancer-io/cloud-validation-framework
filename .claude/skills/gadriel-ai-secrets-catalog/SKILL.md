---
name: gadriel-ai-secrets-catalog
description: AI-native secrets catalog — API key, token, and credential patterns for every major model provider and vector-DB. Auto-invoke for findings tagged `secret-leak`, `hardcoded-credential`, or rule IDs `CODE-W1-L1-*` when the leaked material is an LLM/AI provider key.
---

# AI-native Secrets Catalog

This skill teaches Claude the canonical secret-format regexes for every model provider, vector database, and MCP-adjacent service that Gadriel scans for. It activates from the `security` agent on any `secret-leak`-tagged finding so the agent can confirm the leaked material is a real credential and propose the correct rotation procedure.

## When this skill activates

- Finding IDs in `CODE-W1-L1-*` (raw text/secret scan layer) where the rule's `secret_provider` field is non-empty
- Tags: `secret-leak`, `hardcoded-credential`, `api-key`, `model-credential`, `mcp-token`
- User phrasings: "rotate the leaked key", "what kind of secret is this", "is this a real OpenAI key"
- File patterns: `.env*`, `.envrc`, `*.yaml`/`*.toml` config, source files containing `Bearer sk-` or `hf_` prefixes

## Core concepts

- **High-entropy + provider prefix** — modern AI keys combine a stable prefix (`sk-`, `hf_`, `r8_`) with a high-entropy suffix; the prefix lets us classify without false positives from base64 blobs.
- **Revocation cost varies** — OpenAI/Anthropic keys revoke instantly via dashboard; Bedrock IAM keys may require role rotation; HuggingFace tokens may need re-upload of artifacts.
- **Blast radius** — model keys often map to a billing account, so a leak is also a financial DoS vector (related to `gadriel-token-cost-estimator`).
- **Pre-receive vs. post-history** — once a secret is committed, rotation is mandatory even if removed; git history is not a defence.
- **MCP server tokens** — MCP transports carry tokens that grant access to a downstream agent's tool surface; equivalent in blast radius to a service account.

## Detection patterns / cheatsheet

| Provider              | Prefix / regex                                         | Notes                                  |
|-----------------------|--------------------------------------------------------|----------------------------------------|
| OpenAI                | `sk-[A-Za-z0-9]{20,}`, `sk-proj-[A-Za-z0-9_-]{40,}`    | Project keys are newer, longer         |
| Anthropic             | `sk-ant-[A-Za-z0-9_-]{90,}`                            | Constant length per key tier           |
| HuggingFace           | `hf_[A-Za-z0-9]{30,}`                                  | Read/write distinguished by scope only |
| Replicate             | `r8_[A-Za-z0-9]{32,}`                                  | Single-scope                           |
| Cohere                | `[A-Za-z0-9]{40}` + `CO_API_KEY` env name               | No prefix; rely on context             |
| Mistral               | `[A-Za-z0-9]{32}` + `MISTRAL_API_KEY` env name          | No prefix; rely on context             |
| Google AI / Gemini    | `AIza[0-9A-Za-z_-]{35}`                                 | Shared format with Google Cloud keys   |
| AWS Bedrock           | `AKIA[0-9A-Z]{16}` + `aws_secret_access_key`            | Standard AWS access-key pair           |
| Azure OpenAI          | 32-hex key + endpoint URL                               | Pair (key, endpoint) both needed       |
| LangSmith             | `lsv2_pt_[A-Za-z0-9]{32,}_[A-Za-z0-9]{10}`              | Tracing token                          |
| Weights & Biases      | `[a-f0-9]{40}`                                          | Lacks prefix; check filename/env       |
| Pinecone              | UUIDv4 + `PINECONE_API_KEY` env                         | Vector DB                              |
| Weaviate              | `WCD_API_KEY` env, JWT-shaped                           | Cluster-scoped                         |
| Qdrant                | `QDRANT_API_KEY` env, opaque token                      | Cluster-scoped                         |
| Generic Bearer        | `Authorization: Bearer [A-Za-z0-9._-]{20,}`             | Always confirm provider context        |

Look for these in: `.env` files, dockerfiles, K8s `Secret` manifests with `stringData`, hardcoded strings in Python/TS, `git config` files, and inside `mcp_servers` blocks in `claude_desktop_config.json` / `.mcp.json`.

## Remediation playbook

1. Confirm the leak by classifying with the provider's prefix; if ambiguous (no prefix), check surrounding context (env-var name, URL).
2. Rotate immediately at the provider dashboard; do **not** wait for the fix PR to merge.
3. Replace literal value with an environment variable read at runtime; never put it in a default value.
4. Add the file/path to `.gitignore` and `.gitleaksignore` if it's a local example; otherwise move to a secret manager (Vault, AWS Secrets Manager, 1Password CLI).
5. Purge from history when feasible (`git filter-repo --invert-paths --path .env`); force-push with team coordination.
6. If the key was active in production, query provider billing/usage logs for unauthorized calls before the rotation timestamp.
7. Document the rotation in the audit log with reason `secret-leak-rotation` for compliance evidence.

## References

- ADR-090 (Privacy/redaction) — redaction patterns reuse this catalog
- Gadriel rule pack `CODE-W1-L1-*` (raw scan layer)
- Provider docs: OpenAI rotation, Anthropic key management, HuggingFace tokens
- Sigstore + cosign for artifact signing when secrets are also signing keys
