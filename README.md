# Rapidan AI Skills

Reusable agent skills for **Codex, Claude Code, and Hermes**.

## Available skills

| Skill | Purpose |
| --- | --- |
| [code-quality-analysis](code-quality-analysis/SKILL.md) | Evidence-based review of backend/frontend SOLID principles, agentic discoverability, and orphaned artifacts. |

## Quick install

Requires Git and Python 3. Clone once:

```sh
git clone https://github.com/rapidanai/skills.git
cd skills
```

Install for your user account (available across local projects):

```sh
# Codex
python3 install.py --agent codex

# Claude Code
python3 install.py --agent claude
```

Run either command, or both if you use both assistants. On Windows, use `py -3` instead of `python3` if needed. Start a new assistant session after installing.

To install for one existing project instead:

```sh
python3 install.py --agent codex --project /path/to/project
python3 install.py --agent claude --project /path/to/project
```

The installer copies the entire skill, including references and Codex UI metadata. It does not change assistant settings, install dependencies, or overwrite existing skills. Project installations can be committed with your project for teammates.

### Manual installation

Copy the entire `code-quality-analysis/` directory into the appropriate location:

| Assistant | Personal skills directory | Project skills directory |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Hermes | Your active profile’s `skills/software-development/` | Follow your Hermes profile configuration |

For example, a personal Codex installation ends at `~/.agents/skills/code-quality-analysis/SKILL.md`. For a named Hermes profile, the usual destination is `~/.hermes/profiles/<profile>/skills/software-development/code-quality-analysis/`.

These are local installations. Hosted/cloud sessions need the skill available in their own supported environment. See the official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills) for discovery rules and hosted-session limitations.

## Use it

In Codex:

```text
$code-quality-analysis Review this repository. Report only, all four lenses, moderate refactor appetite.
```

In Claude Code:

```text
/code-quality-analysis Review this repository. Report only, all four lenses, moderate refactor appetite.
```

In Hermes, ask to use `code-quality-analysis` with the same scope. Natural requests such as “analyze the codebase” or “find orphaned code” can also activate the skill.

The skill discovers the stack, establishes scope, analyzes the selected lenses, verifies source citations, and provides a ranked report. It can also produce a self-contained implementation plan. Subagents are optional: when unavailable, the same checks run sequentially. No additional skills, MCP servers, or local models are required. A read-only request keeps discovery and plans in the conversation.

## Update or uninstall

Run `git pull --ff-only` in this checkout to get updates. Before reinstalling, back up any local edits and remove **only the installed `code-quality-analysis` directory** from the location above, then rerun the installer. Removing that directory also uninstalls the skill. Restart your assistant session afterward. Avoid duplicate personal and project copies unless you intend to manage both.

## Development

This repository is the canonical source; update installed copies from here.

```sh
python3 -m unittest discover -s tests -v
```

Tests install into temporary directories and check personal/project destinations, complete package copying, and protection of existing installations. They do not run live Codex, Claude Code, or Hermes sessions.

Version `1.1.0` adds runtime-neutral instructions, Codex metadata, and Codex/Claude Code installation. The original `1.0.0` import came from the maintained November 7, 2026 Hermes package.

## License

[MIT](LICENSE), copyright Jon Deavers.
