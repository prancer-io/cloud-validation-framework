---
name: gadriel-token-cost-estimator
description: Token-cost math, per-call pricing, ceiling enforcement, model-tier selection. Auto-invoke for findings tagged `finops`, `cost-anomaly`, `token-budget`, or rule IDs `CODE-W1-COST-*`, and when the user asks about "token cost", "pricing", "context-window optimization", "model tier".
---

# Token Cost Estimator

This skill teaches Claude how to estimate the per-call cost of an LLM invocation, how to detect cost-anomaly patterns in code/config, and how to propose cost-reducing rewrites. Used by the `finops` pillar.

## When this skill activates

- Findings in `CODE-W1-COST-*` or any finding the orchestrator routes to the FinOps reviewer
- Tags: `finops`, `cost-anomaly`, `token-budget`, `model-tier`, `context-bloat`
- User phrasings: "how much does this cost per call", "can we use Haiku here", "context too large", "spend forecast"
- File patterns: code with model invocations, RAG pipelines, batch-completion scripts, observability dashboards

## Core concepts

- **Per-call cost formula** — `cost = (input_tokens / 1M) * input_price + (output_tokens / 1M) * output_price`. Cached input has a separate (cheaper) rate where available; cache writes have a one-time premium.
- **Model tiers** — pick the cheapest model that meets task quality. Tier ladder: small (Haiku/Mini/Flash) → mid (Sonnet/4-mini) → large (Opus/4o/Pro). Default to mid; downshift when prompt + few-shot is enough.
- **Cost ceilings** — three layers: per-call cap (`max_tokens`), per-task budget (sum across an agent run), per-tenant daily budget (rate limit + alerting).
- **Prompt caching** — Anthropic prompt caching (5m, 1h) and OpenAI Cached Input (auto) deliver 5-10x reduction for stable system prompts. Cache should be on by default for any system prompt > 1k tokens.
- **Context-window discipline** — long contexts are expensive even when irrelevant; retrieval (RAG) + summarization beats packing-the-window in cost and accuracy.
- **Embeddings are 100x cheaper** — for filtering, similarity, classification, use embeddings, not generation.

## Detection patterns / cheatsheet

- `max_tokens` not set → unbounded output cost.
- Looping over a list of N items with one `chat.completions.create` per item, no batching → 1x→Nx cost.
- Retrieval that pulls top-k=50 chunks of 1k tokens each → 50k tokens of context per call.
- System prompt > 4k tokens with no caching directive (`cache_control: ephemeral`).
- Model selected = Opus/4o/Pro for tasks that are extractive or yes/no (small model would suffice).
- Sampling with `temperature > 0` for deterministic tasks → wasted retries.
- No retry-backoff budget → exponential cost on degraded provider.
- Embedding-then-generate pattern where embedding alone would answer (e.g., classification).

## Remediation playbook

1. Always set `max_tokens` per call; clamp to the smallest value the schema requires.
2. Replace per-item loops with batch APIs (OpenAI Batch, Anthropic batches) when latency permits — 50% discount.
3. Set retrieval `top_k` based on token budget: budget=4k tokens / chunk_size = top_k; don't blindly pick 50.
4. Apply prompt caching for stable system prompts: split message into static (cached) and dynamic (not cached) blocks.
5. Pick model tier with a written rule per task type:
   - Classification/extraction → small.
   - Summarization/Q&A → mid (with caching).
   - Multi-step reasoning, long-form → large (rare; budget alarm).
6. Add a budget guard: per-tenant daily cap that returns HTTP 429 (with retry-after) when exceeded.
7. For RAG, cap context at a token budget (e.g., 6k) and let retrieval pick the densest chunks; trim quoted matches before generation.
8. Emit per-call cost into the audit log; weekly review of top 1% expensive calls reveals 80% of waste.

## Worked estimate

Suppose a RAG Q&A endpoint with system prompt 2k tokens, retrieved context 6k tokens, user question 200 tokens, answer 400 tokens. At Claude Sonnet pricing (illustrative: $3/M input, $15/M output):

- Without caching: input 8,200 tokens → ~$0.025; output 400 → ~$0.006; total ~$0.031.
- With prompt caching on the 2k system prompt: cached read at 10% rate → ~$0.0006 on those 2k; saving ~$0.005 (16%) per call.
- Switching to Haiku for extractive sub-queries (price floor): often a 10-12x reduction; sometimes a quality drop — eval before committing.

The optimization order is: set `max_tokens` (free, always), enable caching (cheap), trim retrieval (medium), downshift model (eval first).

## References

- Anthropic prompt caching docs — https://docs.anthropic.com/en/docs/prompt-caching
- OpenAI cached input pricing — https://platform.openai.com/docs/guides/prompt-caching
- ADR-086 §D4 — skill assigned to `finops` agent
- Gadriel cost-policy doc: `.security/compliance/finops/budget.md` (per-tenant)
- Sibling skills: `gadriel-output-schema-library` (short structured outputs reduce cost)
