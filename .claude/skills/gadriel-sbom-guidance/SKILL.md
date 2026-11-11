---
name: gadriel-sbom-guidance
description: SBOM generation guidance — SPDX vs CycloneDX, when each is required, common gotchas (transitive deps, base-image layers, AIBOM). Auto-invoke for compliance findings tagged `sbom`, supply-chain findings, or when the user asks about "SBOM", "SPDX", "CycloneDX", "AIBOM", "Executive Order 14028".
---

# SBOM Guidance — SPDX, CycloneDX, AIBOM

This skill teaches Claude when an SBOM is required, which format to use, how to generate one, and the common gaps that auditors flag. Used by the `compliance` pillar agent and referenced by the supply-chain rule findings.

## When this skill activates

- Findings with tag `sbom`, `supply-chain`, or `dependency-provenance`
- User phrasings: "do we need an SBOM", "SPDX vs CycloneDX", "EO 14028", "AIBOM", "model bill of materials"
- File patterns: `package-lock.json`, `Cargo.lock`, `go.sum`, `requirements.txt`, `pdm.lock`, Dockerfile (for image SBOM)

## Core concepts

- **Two mainstream formats** — SPDX (ISO/IEC 5962, Linux Foundation) and CycloneDX (OWASP). Both are valid for US Executive Order 14028 and the EU Cyber Resilience Act.
- **Use cases differ slightly** — SPDX is strong on licensing and provenance; CycloneDX is strong on vulnerability/exploitability (VEX) and AI/ML extensions (AIBOM).
- **Levels** — NTIA "minimum elements" (supplier, name, version, dependency, author, timestamp, identifier); production SBOMs include hashes (`PackageVerificationCode`/`SHA-256`).
- **AIBOM (CycloneDX 1.5+)** — adds `bom-ref` for models, datasets, services; lets you express base-model lineage and training-data summary.
- **Generation timing** — SBOMs must be generated at build time, not after; the build environment knows what was actually linked.
- **Signing** — SBOMs must be signed (cosign attestation or in-toto) to be trustworthy in a supply-chain attack scenario.

## Detection patterns / cheatsheet

- No `*.spdx.json` or `*.cdx.json` in release artifacts → missing SBOM.
- SBOM present but no signature attestation → unsigned SBOM (weak).
- Image SBOM only — no source SBOM → cannot trace dev-time deps.
- SBOM contains base-image deps but not application deps (or vice versa) → incomplete coverage.
- Lockfile in repo but no lockfile in SBOM (`No-Assertion` for many deps) → generator was source-mode without lockfile.
- Model used (HuggingFace, local) but no AIBOM entry → AI provenance missing.
- VEX statements absent → unable to attest "vulnerable but not exploitable" for known CVEs.
- License field missing on >5% of components → license-compatibility skill (see `gadriel-license-compatibility`) cannot run.

## Remediation playbook

1. Pick a format per use case: CycloneDX 1.5+ if you have AI components; SPDX 2.3 if your customer mandates ISO format. Many teams emit both.
2. Generate at build:
   - JS/TS: `npm sbom --sbom-format cyclonedx-json` or `syft scan dir:. -o cyclonedx-json`.
   - Python: `syft scan dir:.` or `cyclonedx-py environment`.
   - Go: `syft scan dir:.` or `cyclonedx-gomod app`.
   - Rust: `cargo cyclonedx` or `syft scan dir:.`.
   - Containers: `syft scan oci:ghcr.io/org/img@sha256:...`.
3. Include both build-time and runtime dependencies; for containers, generate one SBOM per stage.
4. Add the AIBOM section: list each model (`type: machine-learning-model`), base model, training dataset summary, license, hash.
5. Sign with cosign: `cosign attest --predicate sbom.cdx.json --type cyclonedx ghcr.io/org/img@sha256:...`.
6. Attach the SBOM to release artifacts (GitHub Releases, OCI registry) and link from the model card.
7. Maintain VEX (CycloneDX VEX or OpenVEX) for CVEs you've triaged but not patched; auditor expects "vulnerable, not affected, justification".
8. Re-emit on every release; treat SBOM diff as a PR-blocking signal (new transitive dep should be reviewed).

## References

- NTIA minimum elements — https://www.ntia.gov/page/software-bill-materials
- CycloneDX 1.5 — https://cyclonedx.org/specification/overview/
- SPDX 2.3 — https://spdx.github.io/spdx-spec/
- US EO 14028 § 4(e); EU CRA Article 13
- Syft — https://github.com/anchore/syft
- ADR-086 §D4 — skill assigned to `compliance` agent
- Sibling skill: `gadriel-license-compatibility`
