# Audience modes and code-quality evaluation plan

Scope: preserve the four analysis lenses, Developer / Plain language / Learning presentation, built-in question explanations, and distributable evaluation scenarios. Replace token-economy estimates with deterministic before/after measurements of implemented code.

1. Keep verified findings, practical consequences, coverage, and false-positive safeguards across all modes.
2. For plans, name the baseline and post-change checks without inventing after values.
3. For authorized implementations, capture comparable source-line counts, added and deleted lines, finding-specific behavior, and relevant tests or lint results.
4. Exercise an ordinary read-only review and an isolated implementation scenario. Keep prior behavioral captures as historical evidence, not validation of this revision.
5. Validate the installable package, then publish.

Critical checks: line reduction is not a quality verdict; added tests may increase line count; unsupported token-cost claims are declined; dynamically loaded plugins and simple imports do not become false findings; limited coverage is stated.
