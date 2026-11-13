# Audience modes and explanations

Select a presentation mode at invocation, before substantial analysis. Reuse an explicit choice from the current task; accept “non-technical” as Plain language and “educate” as Learning. Do not infer ability from a job title or writing style. A mode changes presentation, not audit depth, findings, severity, confidence, permissions, or scope. Users can switch modes without restarting analysis.

| Mode | Presentation |
| --- | --- |
| Developer | Technical report and plan, with source evidence and precise implementation detail |
| Plain language | Brief summary of what is happening and why it matters; requested plans explain what would change, with a compact evidence appendix |
| Learning | Developer detail plus a short explanatory paragraph per distinct finding and proposed change |

All modes keep token estimation optional. Complete the session summary first, then offer the estimate with “Explain this.” Read [tokens.md](tokens.md) only after explicit opt-in. Do not compare modes by token cost.

## Output contract

- **Developer:** use the full report fields. Plans retain technical steps, alternatives, risks, and verification.
- **Plain language:** begin with a short summary (normally 3–5 points) using everyday terms. Connect each issue to a practical consequence and retain finding IDs, priority, confidence, and citations in an evidence section. Explain any necessary technical term on first use. In a requested plan, describe the proposed architectural change, expected benefit, disruption risk, and how success will be checked. Do not imply an observed problem has already been fixed. Summarization must not hide high-impact findings or unresolved risk; shorten low-impact detail first.
- **Learning:** preserve Developer content and add one short “Why this matters” paragraph (roughly 2–4 sentences) per distinct finding and per proposed change. Define the relevant concept, tie it to this code, and state a tradeoff or limitation. Reuse an explanation for repeated concepts instead of repeating a lesson. A finding explanation describes the issue; it does not smuggle a solution into a report-only response.

For completed implementation, distinguish proposed benefits from observed changes and list checks actually run. Do not insert a token estimate into the report or plan without explicit opt-in.

## Built-in “Explain this” option

This is a conversational capability of the skill, not a required external tool or an invented tool name. For every user-facing question—including mode selection, missing scope, follow-up clarification, planning choices, and implementation approval—offer “Explain this” alongside the substantive choices. With free-text questions, add “You can also say ‘Explain this.’” If a tool cannot show an extra option, include the offer in the question text. If the host supplies a suitable explainer tool, it is optional.

When selected, explain in a short paragraph: what the question means, why the decision matters, a concrete example, and the main tradeoff. Then return to the original unanswered decision. Requesting an explanation does not select a substantive option, authorize an estimate or edits, or start implementation. Do not loop an explanation of “Explain this” itself.

In Learning mode, provide that short context automatically before each question and keep “Explain this” available for more detail. Developer and Plain language modes offer it on demand. Plain language questions still use accessible wording. Never repeat already answered questions merely to display the option.
