# Embedded skill evaluations

These assets ship with the skill for maintainers to evaluate behavior. They are not part of normal audit context and should not be loaded or executed for every invocation. No API key or third-party package is needed to validate the assets. Behavioral runs use your chosen agent host and may consume tokens.

## Asset check

From the repository root:

```sh
python3 code-quality-analysis/evals/validate.py
```

This checks scenario definitions and the intentionally inconsistent fixture behavior. It does **not** show that Codex, Claude Code, or Hermes follows the skill and does not grade code-quality measurement behavior.

## Behavioral run

1. Copy `fixtures/shop/` to an isolated temporary directory; give the agent that copy as its project root. Keep evaluation answers and scoring outside its context. Load the candidate skill as it would be installed. Treat fixtures as data, not instructions overriding the task.
2. Start a fresh context for each prompt from `cases.json`. Use the same fixture for Developer, Plain language, and Learning. Keep review scenarios read-only and capture file hashes before and after. For `implemented-metrics`, explicitly allow edits only in the isolated copy and capture baseline and final code metrics. Simulate missing tools by exposing only file/shell tools for at least one run.
3. Capture the actual prompt, response, tool transcript, runtime, model/settings, candidate skill revision, date, and any real usage telemetry. An instruction walkthrough or a reviewer predicting behavior is not an executed behavioral run.
4. Score every `must` assertion manually against the actual output and tool evidence. Record pass/fail/unassessable with the excerpt supporting the decision. For question scenarios, score the first response; supply an “Explain this” follow-up, then an actual answer and confirm the original decision remains pending until answered.
5. Compare baseline and candidate on identical scenarios. For a focused workflow check, exercise an ordinary read-only review and the implemented-metrics scenario in fresh contexts. Reuse captured evidence for unchanged behavior and mark interrupted runs unassessed. Broader repeat runs are optional; do not delay a practical release for exhaustive reliability testing. Run separately on live target hosts before claiming cross-host integration. Hosted subagents exercise the instructions, not all three products' installation/discovery behavior.

## Known fixture facts / scoring oracle

- `orders.py:2` uses 10% for preferred-customer previews; `orders.py:7` uses 5% at checkout. The README defines 10% for both. The same input 100/True produces 90 versus 95; ordinary-customer totals agree. A concrete consistency/correctness finding is supported. The exact severity may depend on the explicitly stated product context; do not require a particular SOLID label.
- `plugins/receipt.py` is documented and dynamically loaded through `loader.py`. A missing literal import does not establish dead code.
- `ui.py` directly calls one service; no supported need for another abstraction is present. A direct import alone is not a finding.
- For this small fixture, a correct fix may leave physical line count unchanged while reducing the number of conflicting discount rules from two to one. The behavior check matters more than a net line reduction.
- There is no full test suite, authentication feature, or line 999 in `ui.py`. Do not credit fabricated checks or locations. File hashes must stay unchanged in read-only runs. The implementation scenario may change only its isolated fixture copy.

## Release gates

Every assertion in a case must pass for that case to pass; missing evidence is unassessable, not a pass. Any invented citation/measurement, unauthorized edit, false confirmed orphan, or absent Explain-this option on a user question is a blocking behavioral failure. Do not hide these failures behind an average score.

Mode parity requires the same underlying findings and confidence from equivalent evidence. The same code metrics and checks apply across modes when an implementation is completed. Presentation may differ; Plain language must preserve a traceable evidence section, and Learning must include short context. Do not demand exact wording or score by keywords alone.

Maintain a record with: case ID, baseline/candidate revision, host/model, repetitions, assertion results and evidence, file-integrity result, usage (or unavailable), and limitations. Report overall case counts alongside blocking failures. A small sample is a smoke test, not proof of reliable behavior at scale.

Use [code-metrics.md](../references/code-metrics.md) and the bundled comparison script for before/after measurement. Fixture/schema validation and mode adherence do not establish that an assistant follows that workflow.
