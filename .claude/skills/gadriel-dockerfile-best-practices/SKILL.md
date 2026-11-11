---
name: gadriel-dockerfile-best-practices
description: Container security and efficiency patterns — CIS Docker Benchmark, root user, latest tag, secret-bake, image-bloat. Auto-invoke for findings tagged `container`, `dockerfile`, or rule IDs `CODE-W1-CONTAINER-*`, and when the user asks about "Dockerfile review", "Kubernetes hardening", "image scan".
---

# Dockerfile and Container Best Practices

This skill teaches Claude to review Dockerfiles, compose files, and Kubernetes manifests against the CIS Docker Benchmark and Gadriel's container-hardening rule pack. Used by both the `security` and `operational` pillars.

## When this skill activates

- Finding IDs in `CODE-W1-CONTAINER-*`
- Tags: `dockerfile`, `image-bloat`, `root-user`, `secret-bake`, `cis-docker`
- User phrasings: "is this Dockerfile production-ready", "should we use alpine", "why is image size so large", "container running as root"
- File patterns: `Dockerfile*`, `*.Dockerfile`, `docker-compose*.yml`, `*.dockerignore`, K8s `kind: Pod|Deployment` manifests

## Core concepts

- **Least privilege** — run as a non-root UID; drop `CAP_*` capabilities; use a read-only root filesystem when possible.
- **Reproducibility** — pin base images by digest (`@sha256:...`), pin package versions; `:latest` is forbidden in production.
- **Small attack surface** — distroless or `-slim` images; no shells, package managers, or debug tooling in the final stage.
- **No secrets in layers** — `ARG`/`ENV` for build-time secrets, BuildKit `--secret`, never `COPY .env`.
- **Multi-stage builds** — compile in a builder stage, copy only artifacts to the runtime stage.
- **Defensible defaults** — `USER`, `WORKDIR`, `HEALTHCHECK`, explicit `EXPOSE`, `STOPSIGNAL`.
- **Provenance** — sign images with cosign; attach SBOM (see `gadriel-sbom-guidance`).

## Detection patterns / cheatsheet

- **No USER directive** → container runs as root.
- **`FROM ubuntu:latest`** → unpinned tag.
- **`apt-get install` without `--no-install-recommends`** and missing `rm -rf /var/lib/apt/lists/*` → bloated layers.
- **`COPY . /app`** without a `.dockerignore` → secrets and test data leak in.
- **`ARG SECRET_TOKEN`** then `ENV SECRET=${SECRET_TOKEN}` → secret baked into image history.
- **`RUN curl ... | sh`** → unsigned remote script execution at build time.
- **No `HEALTHCHECK`** → orchestrator cannot detect a wedged process.
- **`ADD <url>`** when `COPY` would suffice → unintended TLS-trusting fetch.
- **K8s: `securityContext.runAsRoot: true`** or missing `runAsNonRoot: true`.
- **K8s: `hostNetwork: true`, `hostPID: true`** without explicit justification.
- **K8s: `privileged: true`** anywhere outside a documented infra-tooling namespace.
- **Compose file with `privileged: true`** or `cap_add: [ALL]`.

## Remediation playbook

1. Add `USER 1000:1000` (or a named non-root user) near the end of the Dockerfile.
2. Pin base images: `FROM python:3.12-slim@sha256:<digest>`; update digests via Renovate/Dependabot.
3. Switch to multi-stage builds: `FROM ... AS builder` then `FROM gcr.io/distroless/python3` for runtime.
4. Replace `COPY .` with explicit `COPY src/ ./src/` plus a real `.dockerignore` listing `.env`, `.git`, `node_modules`, `__pycache__`, `*.pem`.
5. Use BuildKit secrets: `RUN --mount=type=secret,id=npmrc npm ci` instead of `ARG NPM_TOKEN`.
6. Add `HEALTHCHECK CMD curl -fsS http://localhost:8080/health || exit 1`.
7. K8s pod spec hardening:
   ```yaml
   securityContext:
     runAsNonRoot: true
     runAsUser: 1000
     readOnlyRootFilesystem: true
     allowPrivilegeEscalation: false
     capabilities: { drop: ["ALL"] }
   ```
8. Sign images: `cosign sign --key cosign.key ghcr.io/org/app@<digest>`; attach SBOM (`cosign attach sbom`).
9. Add a CI gate that fails on any finding in `CODE-W1-CONTAINER-*` at severity `high` or above.

## References

- CIS Docker Benchmark v1.6.0 — https://www.cisecurity.org/benchmark/docker
- NIST SP 800-190 — Application Container Security Guide
- ADR-086 §D4 — skill is shared by `security` and `operational` agents
- Distroless: https://github.com/GoogleContainerTools/distroless
- BuildKit secrets: https://docs.docker.com/build/building/secrets/
