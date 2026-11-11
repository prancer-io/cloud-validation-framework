#!/usr/bin/env bash
# Gadriel Claude Code hook shim.
#
# For most events we stay silent (telemetry / learning only) and never
# disturb the session — diagnostics are swallowed and we exit 0.
#
# `post-edit` is the exception: it runs Gadriel's inline GUARDRAIL. If the
# just-written file has a finding at/above the threshold, Gadriel prints a
# summary to stderr and exits 2 — Claude Code feeds that back to the agent
# so it fixes the code before continuing ("regenerate until clean"). We
# therefore let post-edit's stderr and exit code pass through untouched.
# Set GADRIEL_GUARDRAIL=off to disable, or =critical to only block on
# critical findings.

event="${1:-}"

resolve_bin() {
  if command -v gadriel >/dev/null 2>&1; then
    echo "gadriel"
  elif command -v gadriel-cli >/dev/null 2>&1; then
    echo "gadriel-cli"
  else
    echo ""
  fi
}

bin="$(resolve_bin)"

if [ "$event" = "post-edit" ]; then
  # Guardrail path: propagate stderr + exit code so feedback reaches Claude.
  if [ -n "$bin" ]; then
    exec "$bin" hooks "$@"
  else
    exec npx --prefer-offline --yes @gadriel-ai/cli@latest hooks "$@"
  fi
fi

# All other events: silent, never fail the session.
exec 2>/dev/null
if [ -n "$bin" ]; then
  "$bin" hooks "$@" || true
else
  npx --prefer-offline --yes @gadriel-ai/cli@latest hooks "$@" || true
fi
exit 0
