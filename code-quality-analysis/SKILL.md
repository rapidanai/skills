---
name: code-quality-analysis
description: "Use when asked to analyze a codebase for design coherence, SOLID violations, orphaned artifacts, or agentic discoverability. Triggers on 'analyze the codebase', 'code quality review', 'find design inconsistencies', 'make this more agent-friendly', 'apply SOLID', 'find dead code', 'clean up the codebase', 'find orphaned code'."
version: 1.0.0
author: Jon Deavers
license: MIT
metadata:
  hermes:
    tags: [code-quality, analysis, solid, refactoring, discoverability]
    related_skills: [plan, requesting-code-review, simplify-code, local-model-delegation]
---

# Code Quality Analysis

Analyze any codebase through four lenses: **SOLID violations** (backend), **SOLID violations** (frontend), **agentic discoverability**, and **orphaned artifacts** — whether the codebase is tidy and easy for a new agent to navigate correctly.

You are in discovery mode. Do not seed subagents with named files, known issues, or "canonical" patterns — those are theirs to find.

## The loop

**Step 0 — Stack discovery**
Check for `docs/code-quality/stack-discovery.md` in the project root.
- **Not found**: consult [stack-discovery-format.md](references/stack-discovery-format.md), run full discovery using terminal and read_file/search_files, and write the file.
- **Found**: re-verify — confirm key source paths still exist as directories, test commands still appear in their source files, and check `git log --oneline -5` for config-touching commits since the last verified date. Update only changed fields and refresh the `## Last verified` timestamp. Do not consult stack-discovery-format.md unless rewriting the file from scratch.

**Step 1 — Clarify**
Use the `clarify` tool to ask the 3 questions in [questions.md](references/questions.md). Wait for answers before proceeding. Present the three choices for scope/focus/refactor-appetite cleanly so the user can pick.

**Step 2 — Analyze**
Load [lenses.md](references/lenses.md) for the per-agent briefs. Determine which paths to pass each delegate based on the discovery file. Launch up to 4 delegate_task subagents in parallel, one per lens. Pass each agent its relevant paths from `docs/code-quality/stack-discovery.md` via the `context` field. Skip any agent whose primary path is recorded as "not present" in the discovery file — note the skip in the report. Exception: on a static/SPA repo with no backend root, still run Agent 1 against build/ops tooling (`scripts/`, `bin/`, `tools/`) and auxiliary servers rather than skipping it (see lenses.md).

Each delegate receives:
- Its lens-specific instructions (from lenses.md)
- The relevant paths from stack-discovery.md
- The project root so it can cd/tool there
- An explicit instruction: return `file:line` observations only — no prescriptions

IMPORTANT delegate_task constraints for this skill:
- Subagents are leaf agents (role='leaf') — they CANNOT use delegate_task, clarify, or memory themselves
- Pass ALL needed context in the `context` field — subagents have no conversation history
- Each subagent gets a fresh terminal session — it must cd to the project root
- Subagent summaries are self-reports — verify key findings by reading cited files yourself in step 3

**Cost-saver: route Agent 4 (orphaned artifacts) to a local Ollama model.**
Agent 4 is mostly deterministic grep/search_file operations — checking if imports exist, whether files are referenced, cross-referencing routes against API clients. It's the lowest-reasoning lens and runs well on a local 12B+ model like `gemma4-hermes:latest` or `qwen3:14b`. To route it:
1. Load the `local-model-delegation` skill for setup details.
2. Configure `delegation.provider: local-ollama` and `delegation.model: gemma4-hermes:latest` in your profile config so `delegate_task` subagents use the local model by default.
3. Or pin it per-run by passing a one-off override via the delegation config if you don't want to set a global default.

Agents 1, 2, and 3 (SOLID backend, SOLID frontend, discoverability) should stay on the frontier model — they need architectural reasoning to evaluate SRP/OCP/DIP violations and pattern legibility.

**Caveats for local model on Agent 4:**
- Per `local-model-delegation` Patterns: the local model is fine for **drafting, not shipping** — treat its output as a first pass. Verify all `file:line` citations in step 3 before including them in the report.
- Local models may miss dynamic references (string interpolation, eval, `require(variable)`) more often than frontier models. The "confirmation rule" in lenses.md (second-pass grep with alternative search terms) is especially important when Agent 4 runs locally.
- If the orphan analysis covers a codebase with very large directories (1000+ files), be mindful of local model context limits (~8K for Gemma models). The `qwen3:14b` or `qwen2.5:14b` models handle larger context better for big repos.

**Step 3 — Report**
Synthesize findings into a ranked report using the format in [report.md](references/report.md). For each finding cited by a subagent, verify the `file:line` reference by reading the actual file before including it in the report. Merge cross-lens duplicates per the cross-lens merge rule. Output the report to the user.

**Step 4 — Offer a plan**
Ask: *"Want an implementation plan? All findings, a severity band, or a subset you name?"* If yes, load the `plan` skill and write to `.hermes/plans/` using [plan.md](references/plan.md).

**Step 5 — Execute the plan (when user says "implement it")**
After the plan is saved and approved, implement it file by file:

1. Start with the **lowest-severity findings** (cosmetic/doc fixes) — these are quick wins and build momentum
2. Move to **medium findings** — structural improvements that don't change interfaces
3. End with **high findings** — abstraction changes that touch multiple files
4. After each logical group, **commit with a descriptive message**
5. **Run the linter/codechecker** on every new or changed file before the final commit — iterate to zero findings (see stack-discovery for the command)
6. **Run the test suite** to verify nothing is broken
7. Update `stack-discovery.md` if the codebase shape changed
8. Push all branches

**Key execution sequence** (from this session's mod_rapidanai refactor):
- Doc fixes (README, upgrade template comment) → commit
- CLI portability fix → commit  
- Test additions for new methods → commit
- Core abstraction refactor + version bump → commit
- Push → run DB upgrade
- Update the audit document

## Relationship to DESLOP MCP tools

This skill describes the Hermes-native analysis workflow (subagent-based, conversational). The intellectual content feeds into the **Software Development (sw_*) domain** of DESLOP's domain hierarchy (see `docs/hierarchy.md` in the DESLOP repo for the full design).

| Skill lens | DESLOP hierarchy | Mode | Tier |
|---|---|---|---|
| Orphaned artifacts | `sw_arch_dead_code` (Code Architecture) | Deterministic | Free |
| Complexity | `sw_arch_complexity` (Code Architecture) | Deterministic | Free |
| Consistency | `sw_arch_consistency` (Code Architecture) | Deterministic | Free |
| SOLID backend + frontend | `sw_arch_solid` (Code Architecture) | LLM | Paid |
| Agentic discoverability | `sw_arch_discoverability` (Code Architecture) | LLM | Paid |
| BC smell shims | `sw_arch_bc_smell` (Code Architecture) | Hybrid | Paid |

DESLOP's Software Development domain has 5 additional categories beyond Code Architecture: Dependency Hygiene (`sw_deps_*`), Test Quality (`sw_test_*`), Git Hygiene (`sw_git_*`), Documentation Hygiene (`sw_docs_*`), and Config & Boilerplate (`sw_config_*`). These cover analysis this skill does not address natively.

When the DESLOP MCP server is available, **prefer calling its individual `sw_*` tools** over running the full Hermes workflow for narrow questions. This skill's native workflow is suited for comprehensive ad-hoc audits where interactive clarification is needed; the MCP tools suit repeated analysis and CI/CD integration.

## Hard rules

- Do not skip step 0 or step 1.
- Do not tell step 2 subagents what to find — just the lens and paths.
- Every observation cites `file:line`. Uncited observations are discarded.
- The report describes; only the plan prescribes.
- If a category has no findings, say so explicitly. Do not invent findings.
- Verify at least one `file:line` citation per subagent finding by reading the file yourself before reporting.
- Only change what the user asks for in step 4.

## Common Pitfalls

0. **Lacking directory validation in Stack Discovery.** Always verify core paths exist using tools like `search_files` rather than guessing directories. Incorrect configurations will derail downstream subagents.
1. **Evennia Custom Attribute Serialization Constraints.** In Evennia (MUD framework) deployments, custom attributes (like conversation `history` list of dicts) can fail silently or get stripped out under systemdb attributes due to nested framework wrappers. Always serialize dialogue arrays or nested matrices to explicit JSON strings (`json.dumps`/`json.loads`) when targeting Evennia database attributes.
2. **Subagent over-promising.** A subagent may claim it "found violations" without returning specific file:line references. If a subagent returns vague findings, read the relevant files yourself before concluding.
3. **Out-of-Repo Dependency Modifications.** Sibling dependencies or integrated frameworks (like an adjacent MUD directory) may lie outside the core repository's local git status check, causing changes to look unmodified. Ensure direct verification steps on absolute files outside the main package layout.
4. **Sequential file processing limits.** Running loops of `read_file` or broad multi-turn file inspection can hit platform context/run limits. Prioritize fast regex queries with `search_files` to find target areas first.
5. **Forgetting to load the plan skill.** Step 4 needs the `plan` skill loaded to write `.hermes/plans/` with the correct structure.
6. **Passing too little context to subagents.** Each subagent needs at minimum: its lens brief, the relevant paths, the project root, and that it must return `file:line` observations only.
7. **Treating subagent output as verified.** Subagent results are self-reports. Always sample-verify a few `file:line` citations before including them in the final report.
8. **Bypassing clarify.** The 3 questions define scope — running the full 4-lens analysis when the user only wants orphans wastes tokens.
9. **Local model context blowout.** If Agent 4 runs on a Gemma model (~8K effective context) and the project has 1000+ files, the subagent may hit its context ceiling mid-analysis. Switch to `qwen3:14b` or `qwen2.5:14b` for large repos, or narrow Agent 4's path scope in the discovery step.
10. **Forgetting to verify local model output.** Local models have higher hallucination rates on `file:line` citations. When Agent 4 runs locally, manually verify every finding's cited line numbers in step 3 — don't trust them at face value.
11. **Framework-mandated patterns flagged as SOLID violations.** Subagents will report things like Moodle's `global $DB` inside `*_add_instance`/`*_update_instance` callbacks, or `*_supports()` match expressions, as DIP/OCP violations. These are framework idioms, not smells. The SOLID lens briefs must say "do not report framework-mandated patterns as violations" (see lenses.md), and step 3 should filter any that slip through.
12. **Plan-generated code ignores ecosystem conventions.** When step 4 produces NEW files (tests, scaffolding, service classes), the plan must derive their layout, namespace, and boilerplate from sibling code in the same checkout — not from general knowledge. This session: a Moodle test was written with namespace `mod_rapidanai` in `tests/` using the wrong namespace pattern, costing 5 fix-recheck loops. The canonical pattern was sitting in `mod/book/tests/` and `mod/assign/tests/` the whole time.
13. **No linter/code-checker pass in verification.** Many projects ship a code-style checker (Moodle `local_codechecker`, phpcs, ESLint, ruff, clippy, gofmt). The plan's verification must include running it on every new/changed file and iterating to zero before declaring done. Stack discovery should capture the lint command (see stack-discovery-format.md) so it's on hand.
14. **Backup/restore stubs can be empty without looking orphaned.** Moodle discovers backup/restore handlers by naming convention (`backup_<name>_activity_task.class.php`), so they're not "orphaned" in the source-code sense — but they can be empty stubs that silently lose data on course import/export. The orphaned-artifacts agent should check that backup structure steps actually define content elements, not just return empty arrays. Add to the Agent 4 brief: for any `backup/moodle2/` files, verify `define_my_steps()` adds a real structure step (not just a no-op).
16. **LLM response parsing: auto-generate findings for missing key.** When building LLM-powered DESLOP sub-tools, use `response.get("findings")` (no default) rather than `response.get("findings", [])`. This lets you distinguish between "LLM omitted findings" (None → auto-generate) and "LLM returned empty list" ([] → trust the LLM's explicit output). Both solid.py and discoverability.py had this bug.

## Verification Checklist

- [ ] `docs/code-quality/stack-discovery.md` exists and is current, or was created in step 0
- [ ] Step 1 (clarify) was completed before analysis began
- [ ] Subagents launched in parallel where paths are present
- [ ] Each subagent received: lens brief, relevant paths, project root, "no prescriptions" instruction
- [ ] Report deduplicates cross-lens findings
- [ ] Every finding in the report has at least one `file:line` citation verified by reading the file
- [ ] No solutions were proposed in the report (only in the optional plan)
- [ ] Plan (if requested) uses `.hermes/plans/` path via the `plan` skill