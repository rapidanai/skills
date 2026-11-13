# Quality evaluation status — 2026-11-13

Published baseline: version 1.3.0 at `b547f39`. Version 1.4.0 replaces optional future-development token estimates with deterministic before/after code-quality measurements for implemented changes. Read-only reviews and plans specify proposed checks without claiming an after-state.

## Prior evidence

The captures under `/tmp/code-quality-behavior-20261113/` are instruction tests in fresh Codex subagents, not live Codex, Claude Code, or Hermes installation/discovery tests. Ten case directories contain responses; the others are unassessed. All 21 fixture copies match their `before.json` SHA-256 values. The completed Developer, Plain language, and Learning reviews identified the preferred-customer mismatch (preview 90, checkout 95 on 100) with high finding confidence. Captured orphan, simple-import, and limited-coverage reviews avoided the named false findings or overclaims. Explanation interactions kept choices pending.

The prior unsupported-savings run rejected “40%” and “$100/month” but omitted the old rubric's requested measurement approach; that assertion failed. One mode explanation ranked Learning by response-token cost. The `code-not-mode-savings` agent failed with a usage-limit error. Missing and interrupted responses are unassessed. These are historical findings, not passes for the revised code-metrics workflow.

## Revised evaluation

The embedded cases now ask for reproducible planned metrics in read-only work and actual before/after measurements in an isolated implementation. A valid result compares the same source scope and counting rule, reports physical lines and added/deleted lines separately, checks the corrected discount behavior, and does not claim quality from line reduction alone. The fixture validator verifies scenario definitions and known fixture behavior only. Fresh assistant behavior on this revision remains unassessed unless a run is recorded below. Live cross-host discovery remains untested.

## Package checks for version 1.4.0

The deterministic comparison helper was tested on a line replacement that leaves total physical lines unchanged while recording one added and one deleted line. The repository suite passed 17 tests; the embedded validator passed 15 scenario definitions and fixture oracles; skill metadata validation passed. All 29 relative Markdown links and `git diff --check` passed. These package checks do not establish assistant behavior on the new workflow.
