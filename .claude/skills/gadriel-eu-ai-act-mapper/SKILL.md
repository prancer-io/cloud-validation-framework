---
name: gadriel-eu-ai-act-mapper
description: EU AI Act article-by-article mapping — translate Gadriel findings into the obligations they trigger (Art. 9 risk-mgmt, Art. 10 data governance, Art. 13 transparency, Art. 14 human oversight, Art. 15 accuracy/robustness/cybersec). Auto-invoke for compliance findings or when the user asks about "EU AI Act", "high-risk system", "Annex III".
---

# EU AI Act Mapper

This skill is owned by the `compliance` pillar agent. It teaches Claude how to translate a security/safety/operational finding into the specific EU AI Act obligation that is implicated, and how to record that mapping in the finding's `compliance_controls[]` list so the auto-generated compliance PDF can group it correctly.

## When this skill activates

- Any finding where the invoking agent is `compliance-reviewer`
- Tags: `compliance`, `eu-ai-act`, `high-risk-ai`, `annex-iii`, `transparency-obligation`
- User phrasings: "is this in scope of the AI Act", "do we need a CE marking", "high-risk classification"
- File patterns: `MODEL_CARD.md`, `DATA_GOVERNANCE.md`, model-registry manifests, RAG ingestion configs

## Core concepts

- **Risk tiers** — Unacceptable (Art. 5, prohibited), High-risk (Annex III + Annex I, heavy obligations), Limited-risk (transparency only), Minimal (no obligations).
- **High-risk identification** — most enterprise AI lands here if it is used in employment, education, credit, law-enforcement, biometrics, critical infrastructure, or essential public services (Annex III).
- **GPAI obligations** — General-purpose AI models have a separate, stacked obligation set (Art. 51-56): documentation, copyright policy, training-data summary; systemic-risk GPAI also has model-eval, incident-reporting, cybersecurity.
- **Timelines** — Prohibited practices: applicable Feb 2025; GPAI obligations: Aug 2025; High-risk: Aug 2026 (most); Annex I high-risk: Aug 2027.
- **Mapping discipline** — every Gadriel finding tagged `eu-ai-act` must list the specific Article(s) in `compliance_controls`, not just "AI Act".

## Detection patterns / cheatsheet

| Article | Obligation                              | Gadriel finding signals                                     |
|---------|-----------------------------------------|-------------------------------------------------------------|
| Art. 9  | Risk management system                  | No `risks.md` / no risk register / no mitigation log        |
| Art. 10 | Data governance                         | Training data not documented; provenance not captured       |
| Art. 11 | Technical documentation                 | No model card; missing capabilities/limitations             |
| Art. 12 | Logging                                 | Inference logs not retained / not append-only               |
| Art. 13 | Transparency / instructions for use     | User-facing AI doesn't disclose AI nature                   |
| Art. 14 | Human oversight                         | Autonomous agent with no HITL gate (see `gadriel-hitl-patterns`) |
| Art. 15 | Accuracy, robustness, cybersecurity     | Any `security`/`safety` finding overlaps here               |
| Art. 16 | Quality management                      | No QMS process documented                                   |
| Art. 50 | Transparency for limited-risk           | Chatbot doesn't disclose; deepfake not watermarked          |
| Art. 51 | GPAI classification                     | GPAI used without disclosure of base model                  |
| Art. 53 | GPAI documentation                      | No training-data summary; no copyright policy               |
| Art. 55 | GPAI systemic risk                      | FLOPs > 10^25 threshold without notification                |

## Remediation playbook

1. Classify the system: walk Annex III categories; if any match, declare high-risk and emit a notice into `.security/compliance/eu-ai-act/classification.md`.
2. For each implicated Article, attach the article ID to `compliance_controls`: `"EU-AI-ACT-ART-15"`, `"EU-AI-ACT-ART-14"`.
3. Maintain a `risks.md` register: hazard, likelihood, mitigation, residual risk, owner; reference from Art. 9 mapping.
4. Produce a model card (Art. 11) using HuggingFace's template extended with Annex IV fields; commit to repo.
5. Make logs append-only and timestamped (Art. 12); the Gadriel audit log (NDJSON) is sufficient if retained ≥ 6 months.
6. Add a user-facing AI disclosure where Art. 13/50 apply: "You are interacting with an AI system."
7. For GPAI, document training-data summary and copyright-respect policy (Art. 53); link from the model card.
8. When emitting the compliance PDF, group findings by Article so the operator can attest article-by-article.

## Classification quick test

Walk these in order; first match wins:

1. Does the system use any practice in Art. 5? (subliminal manipulation, social scoring, untargeted facial-recognition scraping) — if yes: prohibited, stop shipping.
2. Is the system listed in Annex I (safety component of regulated product) or Annex III (employment, education, credit, etc.)? If yes: high-risk.
3. Is the system a GPAI model (training compute > 10^23 FLOPs, or marketed as general-purpose)? If yes: GPAI obligations stack on top of any high-risk obligations.
4. Does the system interact with end users (chatbot, deepfake generator)? If yes: limited-risk transparency obligations (Art. 50).
5. None of the above: minimal risk, no specific obligations.

## References

- Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Annex III (high-risk categories) and Annex IV (technical documentation)
- ALTAI assessment list — https://digital-strategy.ec.europa.eu/en/library/assessment-list-trustworthy-artificial-intelligence-altai
- ADR-086 §D4 — skill assigned to `compliance` agent
- Sibling skills: `gadriel-nist-ai-rmf-mapper`, `gadriel-hitl-patterns`
