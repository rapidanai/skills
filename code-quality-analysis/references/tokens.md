# Before-and-after token savings

Estimate the impact of the reviewed code and proposed improvements on future AI-assisted development tasks. This is not a comparison of presentation modes. Developer, Plain language, and Learning must report the same code-impact estimates from the same evidence.

## Frame the comparison

Name a representative task, such as “add a pricing rule,” “find the correct API entry point,” or “fix this validation bug.” Describe the work needed with the current code and with a specific proposed improvement. Until implemented and checked, the after-state is hypothetical, not a measured result. If no useful improvement is supported, say so; do not invent a refactor to produce savings.

Count task work beyond code length: source/context reading, searching, reasoning, tool output, retries, tests, and all delegated agents where usage is exposed. Smaller code is not automatically cheaper to work on. More abstraction may add navigation and context costs. Keep AI development tokens distinct from the application's own LLM calls, application performance, hosting costs, and developer time. Assess application LLM-token savings only when that usage is explicitly in scope and supported by evidence; report it separately.

## Required comparison in every mode

For each significant finding/proposed change, include:

| Field | Content |
| --- | --- |
| Representative task | The same concrete future task before and after |
| Before | Current files, competing rules, searches, or likely repair steps supported by source evidence |
| After | Work with the proposed improvement; label hypothetical until validated |
| Token expenditure impact | Likely decrease / roughly unchanged / likely increase / unknown |
| Potential token savings | Low / Medium / High / Unknown, with the reason |
| Confidence and basis | Measured / source-based estimate / hypothesis; assumptions and limitations |
| Upfront change effort | Low / Medium / High / Unknown; implementation and verification cost is separate from recurring savings |

Plain language can express these fields in a short paragraph or compact table. Learning adds context, but must not change the estimate. Summarize overall impact conservatively; do not add overlapping per-finding savings. A report-only response may describe a brief hypothetical improved state solely to make the comparison intelligible; do not turn it into implementation steps or claim authorization to change code.

## Rating rules

- **Low savings:** a small, supported reduction in search, context, or repair work for the named task; a local correctness fix may have low savings despite high product importance.
- **Medium savings:** source/task evidence shows repeated competing rules, duplicated investigation, or several navigation/repair steps that a specified improvement could remove.
- **High savings:** comparable repeated-task measurements show substantial token reduction at equivalent output quality. Do not assign High from code appearance alone.
- **Unknown:** no comparable task, no supported improved state, or too little evidence. Describe the potential mechanism and what would need measuring instead of inventing a number.

Confidence: High requires comparable measurements with limitations disclosed; Medium can use concrete source/task evidence without token telemetry; Low means a hypothesis. “Roughly unchanged / no savings demonstrated” is valid. For likely increases, state additional work rather than presenting negative impact as a saving. Savings are not a severity score and should not drive unnecessary refactoring.

## Numeric estimates and validation

Prefer a qualitative before/after estimate when telemetry is absent. Do not manufacture percentages, dollar projections, or token totals. If a bounded numeric estimate is useful, show the exact workload, counting method/tokenizer, before/after inputs, excluded work, and assumptions. A count of selected source text estimates only that input context, not total task tokens or billed usage.

For measured savings, use the same task, repository fixture, model/settings, tools, cache conditions, and success criteria before and after. Include all agent/tool-context usage where exposed. Preserve provider input/output/cached/reasoning breakdowns without double counting nested fields. Repeat where feasible, reporting sample size, individual results/spread, and failures; one run is preliminary. Label incomplete telemetry as partial.

Only calculate `(baseline_tokens - improved_tokens) / baseline_tokens * 100` with a nonzero baseline and comparable measured totals. Negative savings mean increased usage. Upfront implementation tokens are a separate investment. A break-even estimate requires measured implementation usage and positive measured savings per task: `implementation_tokens / tokens_saved_per_task`; future task frequency may still be unknown.
