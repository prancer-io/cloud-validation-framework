---
name: gadriel-bayesian-calibration
description: Bayesian calibration for Gadriel verdicts — interpreting the {{bayes_prior}} prompt slot, reliability diagrams, ECE, post-hoc calibration (Platt, isotonic, temperature scaling). Auto-invokes for ALL agents on every finding; this is the cross-cutting skill shared by every pillar.
---

# Bayesian Calibration

This is the cross-cutting skill shared by all eight Gadriel reasoning agents (`security`, `compliance`, `safety`, `operational`, `finops`, `coherence`, `teamwork`, `bias`). It teaches Claude how to interpret the Bayesian prior injected into the agent prompt (`{{bayes_prior}}`), how the prior is updated from operator feedback, and how to express probabilistic verdicts without over- or under-confidence.

## When this skill activates

- Every agent invocation — this skill is `agents: all` in the registry.
- Tags: `calibration`, `bayes`, `confidence`, `ece`, `reliability-diagram`
- User phrasings: "is the model confident", "ECE", "calibration drift", "how reliable is this verdict"
- The prompt slot `{{bayes_prior}}` is always populated; this skill explains its semantics.

## Core concepts

- **The prior** — `bayes_prior ∈ [0, 1]` is the model-pillar-rule conditional probability `P(true positive | rule_id, pillar, project_history)`. It is computed from operator dispositions (confirm/dismiss) accumulated in the project's local store and updated online (ADR-073).
- **Use it as a tilt, not a verdict** — the agent's job is to *update* the prior with the current finding's evidence (graph context, neighbors, repro), not to echo it. A high prior with weak evidence is still weak.
- **Confidence categories**:
  - prior < 0.2 → "speculative, treat as informational unless evidence is strong"
  - 0.2 ≤ prior < 0.5 → "plausible, needs corroboration"
  - 0.5 ≤ prior < 0.8 → "likely, default to confirm if evidence aligns"
  - prior ≥ 0.8 → "strong, confirm unless evidence contradicts"
- **Posterior reporting** — the verdict's `confirmation_rationale` should say how the evidence shifted the prior ("prior 0.62 → posterior ~0.75 because cross-file taint trace lands in user-controlled input").
- **Reliability diagrams** — bucket predicted probabilities into bins, plot bin-mean vs. observed-positive rate; perfectly calibrated = diagonal.
- **Expected Calibration Error (ECE)** — `Σ (|B_i|/N) * |acc(B_i) - conf(B_i)|`; lower is better; <0.05 is good for moderate sample sizes.
- **Post-hoc calibration** — Platt scaling (logistic), isotonic regression (non-parametric, more data-hungry), temperature scaling (for neural-net logits). Applied periodically (D8/D9 feedback loop in ADR-086).
- **Drift** — model upgrades, rule pack changes, or repo composition shifts can break calibration; re-fit periodically and alarm on ECE > threshold.

## Detection patterns / cheatsheet

- Agent verdict ignores `{{bayes_prior}}` entirely (rationale doesn't reference it) → calibration not in use.
- Confirmation rate per rule_id differs by > 20% from `bayes_prior` over a 30-day window → drift.
- ECE rising over time → recalibrate.
- Operator's dismissal rate diverging across pillars (e.g., security 90% confirmed, bias 10% confirmed) → recompute per-pillar priors separately.
- High-prior findings ignored without rationale → agent under-confident; needs prompt-engineering review.
- Low-prior findings confirmed without strong evidence → agent over-confident; needs evidence guidance.

## Remediation playbook

1. Always reference the prior in `confirmation_rationale` (one sentence: "prior X, evidence Y, posterior Z").
2. When prior and evidence disagree by > 0.3, surface this in `additional_actions` so operators know the verdict was borderline.
3. Re-compute priors per (rule_id, pillar) on every operator disposition (online update is cheap — see ADR-073).
4. Plot a reliability diagram weekly per pillar; if ECE > 0.10, schedule a recalibration job.
5. Choose post-hoc method by sample size: Platt for < 1k labels, isotonic for ≥ 1k labels; never train calibration on the same set used for evaluation.
6. Detect drift via PSI (Population Stability Index) on the prior distribution; alarm on PSI > 0.2.
7. Persist calibration artifacts (intercept/slope or isotonic step function) per pillar in `~/.gadriel/store/calibration.rvf`.
8. On rule-pack upgrade, reset affected priors to the uniform default and warm them up with the next 50 dispositions before relying on them.

## Example rationale phrasing

- "Prior 0.72 (rule `CODE-W1-L3-014` historically confirmed in this repo). Cross-file taint trace from `request.json['q']` to `cursor.execute(...)` is direct with no sanitization. Posterior ~0.88; confirming."
- "Prior 0.31 (low confirm rate on this rule across recent dispositions). Evidence: single string concatenation but the variable is from a constant-string source; not a real injection. Posterior ~0.10; dismissing."
- "Prior 0.55. Evidence ambiguous — sink is in a deprecated handler that may not be reachable. Posterior ~0.50; deferring with `additional_actions: [verify-handler-reachability]`."

Following this discipline makes the audit trail readable and gives the feedback loop clean signal.

## References

- ADR-073 — Bayesian prior update protocol
- ADR-086 §D8 / §D9 — feedback loop wiring
- Guo et al. 2017 — "On Calibration of Modern Neural Networks" (temperature scaling)
- Niculescu-Mizil & Caruana 2005 — Platt scaling vs. isotonic
- ECE / reliability-diagram references — DeGroot & Fienberg 1983
- This skill is shared by all eight reasoning agents per ADR-086 §D4 (the only `agents: all` skill).
