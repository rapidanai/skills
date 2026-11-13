# Ecosystem-specific checks

Apply only when the discovered stack makes these relevant. Confirm against the actual code and framework version.

- Framework-mandated callbacks, hooks, globals, and feature-switch conventions are not automatically SOLID violations. Look for avoidable problems beyond the extension contract.
- In Evennia, inspect round-trip persistence of nested attributes and framework wrappers; verify whether dialogue/history is preserved before diagnosing serialization loss.
- For Moodle backup/restore handlers discovered by naming convention, inspect whether structure steps actually define and restore content. A discoverable but empty handler can silently omit data without being orphaned.
- For LLM-backed analysis helpers, distinguish an omitted `findings` key from an explicit empty list. The latter can legitimately mean no findings; do not synthesize issues just because the list is empty.
- Sibling dependencies outside the repository may not appear in its Git status. Identify the scope boundary and seek authorization before changing those dependencies.
- Before generating tests or classes in a plan, find sibling examples that establish namespaces, boilerplate, and layout. If none exist, document the proposed convention and its basis.
