#!/usr/bin/env bash
# gadriel-statusline-chain.sh — `gadriel code init` writes this when the
# repo already has a `statusLine` configured. Runs the previous tool's
# statusline first, then appends Gadriel's. Both commands receive the
# same Claude Code stdin JSON. Output is concatenated with ` · ` as a
# visual separator.
#
# The previous command is passed via the `PREV_STATUSLINE_CMD` env var
# (set by `.claude/settings.json`'s statusLine entry that init writes).
# A 1-second timeout on PREV keeps the bar render snappy if the upstream
# is slow or broken. If PREV is unset, empty, or fails, the wrapper emits
# only Gadriel's half — no placeholder. (Earlier versions fell back to a
# literal `▊ ruflo` placeholder for coexistence with ruflo / claude-flow;
# that made it look like ruflo was installed when it wasn't.)
#
# Swallow stderr so a flaky upstream never blocks the render.
exec 2>/dev/null

INPUT="$(cat)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run upstream statusline. PREV_STATUSLINE_CMD is the command string the
# repo had set BEFORE `gadriel code init` ran. We re-execute it through
# `sh -c` to preserve any pipes / args.
#
# CRITICAL: keep this fast. Claude Code times out the entire statusline
# render on subsequent refreshes if it ever takes too long. A 1s
# timeout AND avoiding npx-on-cold-cache is the difference between the
# bar showing every time and only showing the first session.
PREV=""
if [ -n "${PREV_STATUSLINE_CMD:-}" ]; then
    # Heuristic: if the previous command starts with `npx`, only run it
    # when the underlying tool is already on $PATH (so npx hits its hot
    # cache instead of doing a slow download). Otherwise skip.
    if [[ "$PREV_STATUSLINE_CMD" == *"npx"* ]]; then
        # Crude extract: grab the first package-looking token after npx
        # (`ruflo`, `@claude-flow/cli@latest`, etc).
        tool="$(echo "$PREV_STATUSLINE_CMD" | sed -nE 's/.*npx[[:space:]]+(-y[[:space:]]+)?([^[:space:]@]+)[[:space:]@].*/\2/p')"
        if [ -n "$tool" ] && command -v "$tool" >/dev/null 2>&1; then
            PREV="$(printf '%s' "$INPUT" \
                | timeout 1s sh -c "$PREV_STATUSLINE_CMD" 2>/dev/null \
                || echo '')"
        fi
    else
        PREV="$(printf '%s' "$INPUT" \
            | timeout 1s sh -c "$PREV_STATUSLINE_CMD" 2>/dev/null \
            || echo '')"
    fi
fi
# No fallback placeholder. If PREV is empty (no upstream configured, or
# upstream errored / timed out), the concatenation logic below emits
# Gadriel's half alone.

# Run Gadriel's own statusline.
GADRIEL="$(printf '%s' "$INPUT" \
    | node "${HERE}/gadriel-statusline.cjs" 2>/dev/null \
    || echo '')"

# Concatenate.
if [ -n "$PREV" ] && [ -n "$GADRIEL" ]; then
    printf '%s · %s' "$PREV" "$GADRIEL"
elif [ -n "$PREV" ]; then
    printf '%s' "$PREV"
else
    printf '%s' "$GADRIEL"
fi

exit 0
