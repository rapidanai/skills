Use the project’s existing plan convention, or `docs/code-quality/plans/<descriptive-name>.md`. For read-only work, return the plan in chat. This template is self-contained:

1. **Context** — the SOLID / discoverability / orphan problem being addressed.
2. **Chosen canonical pattern** — for each finding, state the target pattern and why. (First place prescription is allowed.)
3. **Per-finding changes** — create / modify / delete with `file:line` refs.
4. **Sequence** — dependency order with rationale.
5. **Verification** — use test commands from `docs/code-quality/stack-discovery.md`. If a command is flagged as ambiguous in that file, prompt the user to confirm before writing it into the plan. Include change-specific smoke steps alongside the test commands.
6. **Files summary** — create / modify / delete lists.
7. **Code style & lint** — list the project's linter/code-checker command (from stack discovery) and require no new findings on changed files. Record baseline failures, missing checkers, and checks that cannot run rather than claiming success.
8. **Convention derivation** — for any NEW file (tests, scaffolding, service/class), name the sibling file(s) in the same checkout that define the canonical layout/namespace/boilerplate, and follow their conventions. If no sibling exists, state the proposed convention and its basis instead of inventing a canonical precedent.
