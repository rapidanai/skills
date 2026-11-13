# Invocation choices

Use existing answers and ask only for missing choices. Every question offers “Explain this”; follow [modes.md](modes.md). In Learning mode, include the short explanation automatically. Explain-this requests keep the original decision pending.

1. **Presentation mode** — Developer (technical detail), Plain language (an accessible architectural summary), or Learning (technical detail with short explanations). All preserve the same analysis and before/after code token-savings comparison. Ask before substantial analysis if not supplied; never infer expertise.
2. **Deliverable** — findings only, or findings plus a proposed improvement plan? Neither authorizes implementation.
3. **Focus** — all applicable lenses, or a chosen focus? In Plain language, describe them as server code, interface code, ease of finding the right code, and potentially unused files; technical labels can follow in parentheses.
4. **Change appetite, only when a plan is requested** — Small (local changes within current structure), Moderate (coordinate improvements within the architecture), or Broad (consider architecture changes with explicit tradeoffs). This is separate from report scope and not an instruction to refactor unnecessarily.

Bundle related missing choices when the host supports it. A request for a narrow file/lens review supplies that scope; do not require irrelevant decisions. Later clarification and approval questions follow the same explanation contract.
