Use the project’s existing plan convention, or `docs/code-quality/plans/<descriptive-name>.md`. For read-only work, return the plan in chat. This template is self-contained:

1. **Context** — the SOLID / discoverability / orphan problem being addressed.
2. **Chosen canonical pattern** — for each finding, state the target pattern and why. (First place prescription is allowed.)
3. **Per-finding changes** — create / modify / delete with `file:line` refs.
4. **Sequence** — dependency order with rationale.
5. **Verification** — use test commands from `docs/code-quality/stack-discovery.md`. If a command is flagged as ambiguous in that file, prompt the user to confirm before writing it into the plan. Include change-specific smoke steps alongside the test commands.
6. **Files summary** — create / modify / delete lists.
7. **Code style & lint** — list the project's linter/code-checker command (from stack discovery) and require no new findings on changed files. Record baseline failures, missing checkers, and checks that cannot run rather than claiming success.
8. **Convention derivation** — for any NEW file (tests, scaffolding, service/class), name the sibling file(s) in the same checkout that define the canonical layout/namespace/boilerplate, and follow their conventions. If no sibling exists, state the proposed convention and its basis instead of inventing a canonical precedent.

9. **Smallest useful change and alternatives** — prefer a local correction when sufficient; explain any proposed abstraction using actual change pressure. Include keeping the current structure when sensible.
10. **Behavior, risk, and rollback** — identify public behavior that must remain stable (or the intentional bug correction), regression checks, affected consumers, and how to revert safely. Do not describe unrun tests as passing.
11. **Optional estimate offer** — after the completed session summary, offer to estimate how proposed code improvements could reduce tokens on future development tasks. Include “Explain this.” Wait for explicit opt-in before applying [tokens.md](tokens.md).

Render in the chosen [mode](modes.md): Developer keeps technical detail; Plain language explains what would change, why, risk, and how success will be checked with an evidence trail; Learning keeps Developer detail plus a short contextual explanation per distinct change. Proposed changes remain proposals until authorized and implemented. Any clarification or approval question includes “Explain this”; Learning provides the context automatically.
