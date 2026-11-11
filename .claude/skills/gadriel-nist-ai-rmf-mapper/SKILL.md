---
name: gadriel-nist-ai-rmf-mapper
description: NIST AI Risk Management Framework (AI RMF 1.0) function-by-function mapping — Govern, Map, Measure, Manage. Auto-invoke for compliance findings, or when the user asks about "NIST AI RMF", "AI governance", "AI risk assessment".
---

# NIST AI RMF Mapper

This skill teaches Claude how to translate Gadriel findings into the four NIST AI RMF 1.0 functions (Govern, Map, Measure, Manage) and their sub-categories so the compliance pillar can produce a NIST-aligned report. Used alongside `gadriel-eu-ai-act-mapper`; NIST is voluntary but widely required by US federal customers and a useful checklist even when EU AI Act is the primary regime.

## When this skill activates

- Any compliance finding where the user has opted into NIST reporting (`gadriel code policies set nist=true`)
- Tags: `compliance`, `nist-ai-rmf`, `govern`, `map`, `measure`, `manage`
- User phrasings: "NIST AI RMF", "AI governance framework", "Govern function", "AI 100-1"
- Reports: any output going into `.security/compliance/nist-ai-rmf/`

## Core concepts

- **Govern** — culture, policies, accountability, roles. The "human and organizational" layer.
- **Map** — context for the AI system: purpose, stakeholders, impacts, lineage. The "what is this for" layer.
- **Measure** — quantitative and qualitative assessment of trustworthiness characteristics.
- **Manage** — risk treatment, prioritization, monitoring, incident response.
- **Trustworthy characteristics (cross-cutting)**: Valid & Reliable, Safe, Secure & Resilient, Accountable & Transparent, Explainable & Interpretable, Privacy-Enhanced, Fair (with bias managed).
- **AI 600-1 (GAI Profile)** — generative-AI-specific overlay published July 2024; map GenAI findings here.

## Detection patterns / cheatsheet

| Function/Category | Code     | Gadriel finding signals                                           |
|-------------------|----------|--------------------------------------------------------------------|
| GOVERN 1.1        | GV-1.1   | No AI policy doc; no accountability owner                          |
| GOVERN 3.2        | GV-3.2   | Roles not separated; same person builds and audits                 |
| GOVERN 5.1        | GV-5.1   | Third-party AI used without contractual risk controls              |
| MAP 1.1           | MP-1.1   | System purpose not documented (no model card)                      |
| MAP 2.2           | MP-2.2   | Stakeholders/affected groups not identified                        |
| MAP 4.1           | MP-4.1   | Lineage (training data, base model) not captured                   |
| MEASURE 1.1       | MS-1.1   | No metric for accuracy/robustness                                  |
| MEASURE 2.7       | MS-2.7   | Security/resilience not measured (no red-team, no eval suite)      |
| MEASURE 2.10      | MS-2.10  | Privacy risk not measured (no DP, no PII audit)                    |
| MEASURE 2.11      | MS-2.11  | Bias/fairness not measured                                         |
| MANAGE 1.3        | MG-1.3   | Risks not prioritized                                              |
| MANAGE 2.3        | MG-2.3   | No incident response runbook for AI                                |
| MANAGE 4.1        | MG-4.1   | Continuous monitoring absent                                       |
| GAI 2.6           | GAI-2.6  | No CSAM/violent-content output filter                              |
| GAI 2.8           | GAI-2.8  | Hallucination rate not measured                                    |
| GAI 3.4           | GAI-3.4  | Provenance / watermarking absent                                   |

## Remediation playbook

1. For each finding, attach the most specific subcategory ID to `compliance_controls`: `"NIST-AI-RMF-MS-2.7"`, `"NIST-AI-RMF-GAI-3.4"`.
2. Maintain `.security/compliance/nist-ai-rmf/govern.md`, `map.md`, `measure.md`, `manage.md` — one heading per subcategory, "Yes/No/Partial" with evidence pointer.
3. Populate Govern first; it is cheap and unblocks the others (assign an owner, write a one-page AI policy, link to risks register).
4. For Measure, the Gadriel scan run itself is partial evidence; supplement with offline eval-suite results (HELM, MMLU, in-house red-team).
5. For Manage, write an incident runbook: detection → containment → eradication → recovery → post-mortem; include the rotation procedure from `gadriel-ai-secrets-catalog`.
6. For GAI overlay, document model lineage (base, fine-tune, RLHF dataset), training-data summary, and output-filtering pipeline.
7. Cross-link to EU AI Act where applicable; many controls satisfy both (e.g. MP-4.1 ≈ EU-AI-ACT-ART-10, MS-2.7 ≈ EU-AI-ACT-ART-15).
8. Re-emit the report after every release; trend deltas matter more than absolute scores for showing improvement.

## References

- NIST AI RMF 1.0 — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1 (GAI Profile, July 2024)
- NIST AI RMF Playbook (sub-category guidance)
- ADR-086 §D4 — skill assigned to `compliance` agent
- Sibling skills: `gadriel-eu-ai-act-mapper`, `gadriel-sbom-guidance`
