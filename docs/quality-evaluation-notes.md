# Quality evaluation status — 2026-11-13

Candidate: skill version 1.2.0. Baseline: version 1.1.1 before the audience-mode changes.

## What was exercised

- The existing installer tests exercise actual copies into temporary Codex, Claude Code, and Hermes destinations, including copying the whole skill package. Multi-skill selection and existing-file protection are covered.
- The embedded validator checks all 14 scenario definitions and known fixture behavior: preferred-customer preview 90, checkout 95, ordinary-customer totals equal. This is deterministic asset validation, not assistant compliance.
- One actual baseline subagent review read the five fixture files, searched references, and executed the documented calculation with bytecode writing disabled. The prompt requested Plain language, read-only, report only, all applicable lenses, modest appetite, and token estimates. The exact model identifier and token telemetry were unavailable; the host was the current Codex agent environment. This was one run, not a repeated benchmark.

The baseline found the differing discount rules and verified their lines, did not falsely flag the documented dynamic plugin or the simple service import, and reported no file changes. It still used the rigid technical report headings. Its token paragraph rated review overhead and future savings without a structured before/after task comparison. The baseline prompt predated the user's clarification that comparisons must concern the code rather than presentation modes, so it is not a controlled before/after comparison with the final candidate prompts.

## Candidate behavioral testing remains incomplete

Three independent candidate runs were requested for Developer, Plain language, and Learning against the same fixture. All stopped with an account usage-limit error before returning candidate responses. They are **not run / unassessable**, not passes. No candidate behavioral pass rate, measured token savings, or cross-host integration claim is supported.

Static review of the revised instructions and passing asset/installer checks do not replace those runs. In particular, mode parity, explanation availability on later questions, false-evidence rejection, and estimate honesty still need actual candidate responses scored against the bundled assertions.

## Rerun before making stronger claims

Follow the embedded evaluation guide using fresh contexts. Retain each prompt, actual response/tool transcript, candidate revision, host/model/settings, assertions and supporting excerpts, before/after fixture hashes, and available token telemetry. Repeat the core scenarios and run live target-host sessions before claiming reliable integration on Codex, Claude Code, and Hermes. Treat blocked or incomplete cases as unassessable; any critical behavioral failure blocks a behavioral-validation claim.
