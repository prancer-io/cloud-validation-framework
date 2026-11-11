---
description: Start the Gadriel L1 watch daemon for low-latency on-save scanning
allowed-tools: Bash(gadriel:*)
---

# /gadriel-watch

Start the Gadriel L1 watch daemon, which monitors the working tree for file
changes and re-runs the relevant per-file scanners on save. This is the
tight-loop developer experience: edit a file, get findings in under a second
without manually triggering a scan.

The watcher runs in the foreground and prints structured progress lines for
each scan cycle. Stop it with Ctrl-C; the daemon flushes any pending results
to `.security/findings.json` before exiting. Only L1 scanners run in watch
mode (the cheap, syntax-level checks); the deeper L3/L4 scanners only run via
`/gadriel-scan` or in CI to keep the watch loop fast.

If a Gadriel daemon is already running for this project, the command refuses
to start a second instance and points you at the existing process. Use
`/gadriel-status` to see the current daemon's pid and uptime.

## Usage

`/gadriel-watch`

## What this command does

1. Verifies no other Gadriel watch daemon is running for this project.
2. Starts `gadriel code watch` against the project root.
3. Subscribes to filesystem events (with debounce) for source files.
4. Re-runs L1 scanners on changed files and updates `.security/findings.json`.
5. Streams a single line per scan cycle so progress is visible.

```bash
!gadriel code watch
```
