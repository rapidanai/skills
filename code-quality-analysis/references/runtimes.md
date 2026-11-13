# Runtime guidance

Use the host's exposed tool schemas rather than assuming tool names or parameters from another runtime.

| Host | Clarification | Analysis and delegation | Explicit invocation |
| --- | --- | --- | --- |
| Codex | Available question tool, or chat; some input tools are restricted by mode | Shell/file tools; native subagents such as `spawn_agent` when exposed and permitted | `$code-quality-analysis` |
| Claude Code | Available question tool, or chat | Native Read/Grep/Glob/Bash tools and read-only subagents when exposed and permitted | `/code-quality-analysis` |
| Hermes | `clarify` when exposed, or chat | Native file/shell tools and `delegate_task` when exposed and permitted | Ask to use `code-quality-analysis` |

Treat delegation as an optimization. Without it, perform the selected lenses as separate passes in the current session. A failed delegation does not require installing tools or changing configuration: finish that lens sequentially and disclose the limitation.

Pass the full lens brief and discovered context to each delegate; do not assume it inherits the conversation or working directory. Use the current delegation schema for roles, context, and working-directory fields. Ask for read-only analysis and no further delegation. Keep model selection as configured unless the user authorizes a change.

The same bundled plan template works in all three hosts. Honor a project’s existing plan directory; otherwise use `docs/code-quality/plans/`. Do not require `.hermes/plans/`, `.claude/plans/`, or another installed skill.
