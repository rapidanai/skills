# Embedded skill evaluations

These assets ship with the skill for maintainers to evaluate behavior. They are not part of normal review context and should not be loaded or executed for every invocation. No API key or third-party package is needed to validate the assets. Behavioral runs use your chosen agent host and may consume tokens.

## Asset check

From the repository root:

```sh
python3 voice-workshop/evals/validate.py
```

This checks that the scenario definitions are well formed and that the bundled profile template round-trips through `scripts/voice_profile.py` (`init` then `validate`). It does **not** show that Codex, Claude Code, or Hermes follows the skill.

## Behavioral run

1. Give the agent a small page or document to review and load the candidate skill as it would be installed. Keep evaluation answers and scoring outside its context.
2. Start a fresh context for each prompt from `cases.json`. Use a throwaway profile path so runs do not touch a real profile.
3. Capture the actual prompt, response, tool transcript, runtime, model/settings, candidate skill revision, date, and any real usage telemetry. An instruction walkthrough or a reviewer predicting behavior is not an executed behavioral run.
4. Score every `must` assertion manually against the actual output and tool evidence. Record pass/fail/unassessable with the excerpt supporting the decision.
5. Compare baseline and candidate on identical scenarios. Reuse captured evidence for unchanged behavior and mark interrupted runs unassessed.

## Scoring oracle

- **One section at a time.** A correct response presents exactly one section and then waits. Presenting several sections, or offering a rewrite before the user speaks, fails `one-section-at-a-time`.
- **No invented preferences.** Approving a section without comment produces no new profile entry. A rule inferred from silence fails `no-invented-preference`.
- **Lessons trace to decisions.** A captured lesson must include the user's before/after and reason. A rule with no evidence fails `capture-lesson`.
- **Profile location.** The profile is created at the documented path (or a user-named path), never inside the skill directory.
- **Sign-off gates advancement.** A new point raised on the current section keeps the agent on that section.
- **Apply reads first.** New copy is written only after the profile is read; a draft produced without reading it fails `apply-mode-reads-profile`.
- **Corrections are captured.** A correction to generated copy becomes a profile lesson, not a one-off edit.

## Release gates

Every assertion in a case must pass for that case to pass; missing evidence is unassessable, not a pass. Any invented preference, any edit the user did not request, or any advance past an unsigned section is a blocking behavioral failure. Do not hide these failures behind an average score.

Maintain a record with: case ID, baseline/candidate revision, host/model, repetitions, assertion results and evidence, and limitations. A small sample is a smoke test, not proof of reliable behavior at scale.
