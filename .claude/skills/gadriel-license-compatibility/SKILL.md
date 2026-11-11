---
name: gadriel-license-compatibility
description: Open-source license compatibility matrix — copyleft propagation, viral GPL detection, license-incompatible imports. Auto-invoke for findings tagged `license`, `license-incompat`, or rule IDs `CODE-W1-L2-*` when the matched dep has a flagged license.
---

# License Compatibility — Matrix and Detection

This skill teaches Claude the practical compatibility relationships between common open-source licenses (and the AI-era additions: OpenRAIL, Llama Community, etc.), how Gadriel detects incompatible combinations, and how to remediate.

## When this skill activates

- Findings in `CODE-W1-L2-*` with `license_finding == true`
- Tags: `license`, `license-incompat`, `copyleft`, `viral-gpl`, `commercial-incompatible`
- User phrasings: "can we ship this", "is GPL contagious here", "what license is this dep", "OpenRAIL"
- File patterns: `LICENSE`, `LICENSE.txt`, `NOTICE`, lockfiles with license metadata, model cards

## Core concepts

- **Permissive** (MIT, BSD-2/3, Apache-2.0, ISC) — embed freely; preserve copyright + license notice.
- **Weak copyleft** (LGPL, MPL-2.0) — only modified files are copyleft; dynamic linking is fine; static linking has restrictions for LGPL.
- **Strong copyleft** (GPL-2.0, GPL-3.0, AGPL-3.0) — derivative works inherit the same license; AGPL extends to network use.
- **Compatibility direction matters** — Apache-2.0 → GPL-3.0 is fine; GPL-2.0-only ↔ Apache-2.0 is incompatible (patent clauses).
- **AI-specific licenses** — OpenRAIL-M, BigScience RAIL, Llama 2/3 Community License, Stable Diffusion CreativeML — *not* OSI-approved; use restrictions apply.
- **NOTICE files** — Apache-2.0 requires NOTICE propagation; many CI pipelines forget this.

## Detection patterns / cheatsheet

| Combination                              | Verdict                                    |
|------------------------------------------|--------------------------------------------|
| MIT into Apache-2.0 project              | OK (add attribution)                       |
| Apache-2.0 into MIT project              | OK (add NOTICE)                            |
| GPL-2.0-only into Apache-2.0 project     | Incompatible (patent clauses clash)        |
| GPL-3.0 into Apache-2.0 project          | OK if final work is GPL-3.0                |
| GPL into proprietary product (linked)    | Forbidden (or relicense)                   |
| AGPL into SaaS product                   | Triggers source-disclosure obligation      |
| LGPL-3.0 dynamically linked              | OK (preserve LICENSE + ability to relink)  |
| LGPL static-linked into closed-source    | Risk — requires source on request          |
| MPL-2.0 alongside proprietary code       | OK (file-level copyleft only)              |
| OpenRAIL-M (Llama 2)                     | Use-case restrictions apply; review        |
| BUSL (HashiCorp/MongoDB)                 | Time-bombed; check Change Date             |
| SSPL                                     | Not OSI; "open core" alternative needed    |
| "UNKNOWN" / no license file              | Treat as all-rights-reserved (forbidden)   |

Detection signals:
- Lockfile entry has `license: GPL-*` while project root is Apache-2.0/MIT.
- `NOTICE` file missing in a project shipping Apache-2.0 deps.
- Model card cites "Llama 2 Community License" but product violates use-case restrictions (e.g., > 700M monthly active users, or training competing models).
- BUSL dep whose Change Date is in the future and current product use violates the additional-use grant.
- Empty `license` field in `package.json` / `Cargo.toml` / `pyproject.toml`.

## Remediation playbook

1. Identify the project's outbound license (the license you ship under); list it in the project root `LICENSE`.
2. For each dep, ensure its license is compatible "downstream" with the outbound license.
3. If you find a GPL dep in a non-GPL project:
   a. Replace with a permissive alternative (preferred).
   b. Move the GPL dep behind a process boundary (CLI invocation, microservice with stable API) so it's not a derivative work.
   c. Relicense the project to GPL/AGPL (last resort).
4. For Apache-2.0 deps, ensure a `NOTICE` file exists in your distribution; concatenate per-dep NOTICE entries.
5. For AGPL deps in a SaaS context, either publish your service source or replace the dep.
6. For Llama / OpenRAIL models, document use-case restrictions in the model card and add an acceptable-use policy.
7. For BUSL deps, track Change Date; budget for replacement before the time-bomb commercial restriction triggers.
8. Add a CI gate that fails the build on `UNKNOWN` or incompatible licenses; allowlist on a per-dep basis with justification.

## References

- SPDX License List — https://spdx.org/licenses/
- FSF compatibility matrix — https://www.gnu.org/licenses/license-compatibility.html
- OpenRAIL — https://www.licenses.ai/
- Llama 2 Community License — review per Meta's published terms
- ADR-086 §D4 — skill assigned to `compliance` agent
- Sibling skill: `gadriel-sbom-guidance`
