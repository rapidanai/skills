# Rapidan AI Skills

The open-source home for reusable agent skills maintained by Rapidan AI.

## Available skills

| Skill | Purpose |
| --- | --- |
| [code-quality-analysis](code-quality-analysis/SKILL.md) | Evidence-based code review covering backend and frontend SOLID principles, agentic discoverability, and orphaned artifacts. |

## Installation

Clone this repository:

```sh
git clone https://github.com/rapidanai/skills.git
```

Copy the entire `code-quality-analysis/` directory, including `references/`, into your agent's skills directory. For a Hermes profile, place it under `~/.hermes/profiles/<profile>/skills/software-development/`.

The current skill targets Hermes and uses its `clarify` and `delegate_task` tools. Other agent runtimes need equivalent clarification and delegation capabilities. The optional implementation-plan workflow uses the separate `plan` skill; local Ollama routing uses the separate `local-model-delegation` skill. Neither is bundled here. DESLOP integration is optional.

## Usage

Ask your agent to “analyze the codebase” or perform a “code quality review.” The skill discovers the project stack, clarifies scope, analyzes up to four lenses, verifies cited findings, and offers an implementation plan. Implementation requires user approval within that workflow.

## Maintenance

This repository is the canonical source for future updates. Installed copies should be refreshed from here.

The initial import preserves the November 7, 2026 update from the maintained Hermes skill, including all five reference documents. Its existing metadata version is `1.0.0`.

## License

[MIT](LICENSE), matching the imported skill's license declaration.
