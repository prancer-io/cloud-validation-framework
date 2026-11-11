---
name: gadriel-api-security-patterns
description: REST, GraphQL, gRPC, and OpenAPI security patterns — authn, authz, rate limits, schema validation, mass assignment. Auto-invoke for findings tagged `api-security` or rule IDs `CODE-W1-API-*`, and when the user asks about "API hardening", "GraphQL query depth", "rate limit", "OpenAPI security".
---

# API Security Patterns — REST, GraphQL, gRPC

This skill activates whenever Gadriel detects an HTTP/GraphQL/gRPC surface area with a security gap. It teaches Claude both the canonical defenses (OWASP API Top 10) and the framework-specific spelling.

## When this skill activates

- Finding IDs in `CODE-W1-API-*`
- Tags: `api-security`, `owasp-api-top10`, `bola`, `mass-assignment`, `graphql-depth`, `grpc-reflection`
- User phrasings: "is my API rate-limited", "how to harden GraphQL", "should I expose this endpoint"
- File patterns: `openapi.yaml`, `*.proto`, `schema.graphql`, FastAPI routers, Express routers, gRPC service definitions

## Core concepts

- **OWASP API Top 10 (2023) baseline** — BOLA, broken authn, BOPLA, unrestricted resource consumption, BFLA, unrestricted access to sensitive flows, SSRF, security misconfig, improper inventory management, unsafe consumption of APIs.
- **Schema-first design** — every endpoint has a request and response schema; rejection is at the edge, not the handler.
- **Defense in depth** — gateway (rate limit, WAF) → service (authn) → handler (authz on resource) → DB (row-level security).
- **Public vs. internal surfaces** — internal-only endpoints should not be reachable over the internet; service mesh + mTLS is the modern baseline.
- **Query-cost accounting** — for GraphQL and bulk-fetch REST, compute a cost per request and budget per principal.

## Detection patterns / cheatsheet

- **BOLA**: handler reads `request.path_params.id` and queries DB without checking `record.owner_id == user.id`.
- **Mass assignment**: `User(**request.json())` or `Object.assign(user, req.body)` — server-controlled fields overwritable by client.
- **No rate limit**: framework lacks any `@limiter` or `rate_limit` middleware; gateway config absent.
- **GraphQL unbounded depth**: no `depth_limit` plugin; nested types referencing each other (User→posts→author→posts).
- **GraphQL unbounded breadth**: no `cost_analysis` plugin; aliasing same field N times is allowed.
- **gRPC reflection exposed**: `reflection.Register(grpcServer)` in production binary.
- **gRPC missing TLS**: `grpc.NewServer()` without `grpc.Creds(tlsCreds)`.
- **OpenAPI**: spec missing `security:` block at root, or scheme defined but not applied per-operation.
- **OpenAPI**: response schema with `additionalProperties: true` and sensitive fields like `password_hash`.
- **JWT in query string**: token bound to `?token=` rather than `Authorization` header → logged in nginx access logs.
- **CORS misconfig**: `Access-Control-Allow-Origin: *` with `Allow-Credentials: true` (browser refuses but other clients won't).

## Remediation playbook

1. Replace direct ID lookups with `repo.get_for_user(record_id, current_user)` returning 404 (not 403) on miss to avoid enumeration.
2. For mass-assignment, define an explicit input DTO (Pydantic / Zod / proto message) and never spread untrusted input into ORM constructors.
3. Add per-principal rate limits at the gateway: `100 req/min/user` for authenticated, `20 req/min/IP` for unauthenticated; back with Redis counters.
4. GraphQL: install `graphql-depth-limit` (depth ≤ 7) and `graphql-cost-analysis` (cost ≤ 1000); reject anonymous introspection.
5. gRPC: disable reflection in prod build; require TLS everywhere; use `grpc-go`'s `tap.ServerInHandle` for cheap per-request authz.
6. OpenAPI: declare `securitySchemes` and apply at the operation level (`security: [bearerAuth: []]`); set `additionalProperties: false` on every model.
7. Move JWTs to `Authorization: Bearer ...`; rotate signing keys via JWKS; reject `alg: none`.
8. Fix CORS: explicit origin allowlist; only set `Allow-Credentials: true` for the same-origin case.
9. Add a contract-test gate: regenerate OpenAPI from code, diff against committed spec; block PR on drift.

## Framework-specific spelling

- **FastAPI**: depend on `current_user = Depends(get_current_user)`; never read `request.headers["X-User-Id"]`. Use `Path(...)` + `Depends(check_ownership)` for resource lookups.
- **Express/Next API routes**: middleware order matters — auth before parser before handler; CSRF middleware before any state-changing route.
- **Rails**: `before_action :authenticate_user!` + `before_action :authorize_resource`; use `strong_parameters` (`params.require(:user).permit(:name)`) to block mass assignment.
- **gRPC-Go**: `grpc_auth.UnaryServerInterceptor` for authn; per-method authz via `grpc.UnaryInterceptor` chain.

## References

- OWASP API Security Top 10 (2023) — https://owasp.org/API-Security/
- gRPC security best practices — https://grpc.io/docs/guides/auth/
- GraphQL armor — https://github.com/escape-technologies/graphql-armor
- ADR-086 §D4 — skill assigned to `security` agent
