---
name: code-quality-analysis
description: Use when asked for a codebase quality review, SOLID analysis, design inconsistencies, agentic discoverability, dead code, or orphaned artifacts.
license: MIT
metadata:
  version: "1.1.1"
  author: Jon Deavers
---

# Code Quality Analysis

Analyze code through four lenses: backend SOLID, frontend SOLID, agentic discoverability, and orphaned artifacts. Reports describe observed problems with verified `file:line` evidence; implementation plans prescribe changes separately.

## Runtime adaptation

This skill supports Codex, Claude Code, and Hermes. Use only tools actually available in the session; read [runtime guidance](references/runtimes.md) for your host. Resolve this skill's reference links relative to its installed directory, and project paths relative to the repository being analyzed.

No other skill, MCP server, local model, or subagent capability is required. When delegation is unavailable or disallowed, perform the selected lenses sequentially yourself with the same evidence requirements. Respect the user's scope and repository instructions.

## Workflow

### 0. Discover the stack

Check `docs/code-quality/stack-discovery.md` in the target repository. If absent, use [stack-discovery-format.md](references/stack-discovery-format.md) to discover actual source roots, test and lint commands, and framework conventions. If present, re-verify its paths and commands against current files and inspect relevant configuration history; update changed fields and the verification date. Never infer directories from framework knowledge alone.

For read-only requests or environments, retain discovery in working context and summarize it in the report instead of writing files. Otherwise save the discovery document. Do not alter application code during analysis.

### 1. Establish scope

Use [questions.md](references/questions.md) to establish report/plan scope, lens weighting, and refactor appetite. Reuse answers already supplied by the user; ask only for missing information and wait for it before analyzing. Use your host's question tool if available, or ordinary chat. A request for an audit is not authorization to implement findings.

### 2. Analyze

Read [lenses.md](references/lenses.md). Run the selected lenses using up to four independent read-only subagents when available and permitted, or sequential passes otherwise. Skip lenses with no relevant source path and record why. For static/SPA projects, the backend lens still examines build/ops tooling and auxiliary servers when present.

Give each delegate its lens brief, discovered paths, absolute repository root, scope, and the instruction to return `file:line` observations without prescriptions. Ask delegates not to delegate further. Do not seed them with suspected issues or preferred patterns. A narrow orphan-only request runs only that lens.

### 3. Verify and report

Use [report.md](references/report.md). Read every finding's cited source yourself, verify line numbers and surrounding context, and discard unsupported observations. Merge cross-lens duplicates. Distinguish framework requirements from avoidable design problems. For applicable ecosystems, consult [ecosystem notes](references/ecosystem-notes.md).

Confirm potential orphans with a second search using alternate names and dynamic-reference patterns. Lack of an internal caller does not prove a public API is unused; historical migrations can remain necessary. Report unresolved usage as uncertainty, not confirmed dead code. Explicitly distinguish lenses with no findings from skipped or incomplete lenses. Do not invent findings or propose fixes in the report.

### 4. Plan when requested

If a plan was already requested, produce it using [plan.md](references/plan.md). Otherwise offer one for all findings or a chosen subset. Follow an existing project plan convention; absent one, use `docs/code-quality/plans/<descriptive-name>.md`. For read-only work, return the plan in chat. No separate planning skill is needed.

### 5. Implement only when authorized

Implement only the approved scope in dependency order. Derive new-file conventions from the checkout. Run the relevant lint and tests identified in discovery, distinguish existing failures from regressions, and report checks that could not run. Refresh discovery when the project shape changes. Commit, push, deploy, or run database upgrades only when those actions are authorized; this skill grants no extra permission.

## Optional integrations

If an existing DESLOP MCP tool answers a narrow question, it may supplement the analysis. Verify its findings against source just like subagent output. Existing local-model delegation may be used when configured and suitable, but do not change global model settings to run this skill. Neither integration is required.
