# Quality evaluation status — 2026-11-13

Published baseline: version 1.2.0 at `f814d2b`. This revision is version 1.3.0. The workflow now completes the session summary before offering an optional future-development token estimate with “Explain this.” The estimate requires explicit opt-in. Asking for an explanation leaves that decision pending and never authorizes implementation.

## Captured behavior from the prior candidate

The captures under `/tmp/code-quality-behavior-20261113/` are instruction tests in fresh Codex subagents, not live Codex, Claude Code, or Hermes installation/discovery tests. Ten case directories have response files; other started directories have no response and are unassessed. Every one of the 21 captured fixture copies matches its `before.json` SHA-256 values. This establishes file integrity for the read-only fixtures, not that every response followed the skill.

The Developer, Plain language, and Learning reviews each identified the preferred-customer mismatch (preview 90 versus checkout 95 on 100), with high finding confidence. The completed orphan review did not misclassify the documented dynamically loaded receipt plugin. The narrow `ui.py` review avoided proposing abstractions for its direct import. The single-file review did not claim repository-wide coverage. Completed explanation interactions kept choices pending until the user supplied substantive answers. One mode explanation discussed Learning's response-token cost; future explanations should address presentation choices without ranking modes by token use.

The first unsupported-savings response declined “40%” and “$100/month,” but omitted the former rubric's requested measurement approach. That case failed that assertion. It is not a pass. The `code-not-mode-savings` attempt failed with a usage-limit error. Missing and interrupted responses are unassessed. No comparable token telemetry was captured, so no measured token savings, numeric percentage, or dollar outcome is established.

## Revised opt-in workflow validation

The revised assets contain three focused behavioral scenarios: an ordinary review that must not estimate before opt-in, an “Explain this” response that keeps the choice pending, and an explicitly opted-in estimate that compares the same future task on current and proposed code. The fixture validator checks scenario structure and known behavior, not assistant decisions. These revised scenarios have not been run with a fresh agent as of this record; their outcomes are unassessed. The earlier completed runs support unchanged evidence, mode, and false-positive safeguards, but cannot establish adherence to the revised opt-in sequence.

A future smoke run should capture actual prompts, responses, tool evidence, fixture hashes, host/model/settings, and any usage telemetry for those three scenarios. Qualitative source-based estimates may be useful after opt-in. Measured savings require comparable task telemetry. Cross-host installation and discovery behavior remains untested.

## Package checks for version 1.3.0

On 2026-11-13, `python3 -m unittest discover -s tests -v` passed 16 tests; `python3 code-quality-analysis/evals/validate.py` passed 16 scenario definitions and fixture oracles; the skill metadata validator passed; 27 relative Markdown links were checked with none broken; and `git diff --check` passed. These checks do not establish revised assistant behavior.
