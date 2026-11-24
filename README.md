# Rapidan AI Skills

Reusable agent skills for **Codex, Claude Code, and Hermes**.

## Install with your agent

Give your Codex, Claude Code, or Hermes agent this request:

```text
Install code-quality-analysis from https://github.com/rapidanai/skills.git
```

The agent should clone the repository, follow [INSTALL.md](INSTALL.md), install for its own runtime, and verify the files. Name one or more skills in your request, or explicitly ask for all skills. If several skills are available and you have not chosen, the agent will show the list and ask. You do not need to choose folders or run commands yourself. Codex and Claude Code default to personal installation; Hermes uses its active profile. Existing differing copies are preserved for review. Network access and permission to write the destination are required.

**For agents:** [INSTALL.md](INSTALL.md) is the installation procedure. Discover packages with `python3 install.py --list` and install only the requested selection. The repository root is not a skill package.

## Available skills

| Skill | Purpose |
| --- | --- |
| [code-quality-analysis](code-quality-analysis/SKILL.md) | Evidence-based review of backend/frontend SOLID principles, agentic discoverability, and orphaned artifacts. |
| [voice-workshop](voice-workshop/SKILL.md) | Captures the user's writing voice in a living profile, then applies it when writing new copy. |

## Quick install

Requires Git and Python 3. Clone once:

```sh
git clone https://github.com/rapidanai/skills.git
cd skills
```

Install for your user account (available across local projects):

```sh
# Codex
python3 install.py --agent codex --skills code-quality-analysis

# Claude Code
python3 install.py --agent claude --skills code-quality-analysis

# Hermes (inside a session with its active HERMES_HOME exported)
python3 install.py --agent hermes --skills code-quality-analysis
```

Run the command for your assistant. For Hermes outside an active session, pass `--hermes-home /absolute/path/to/active/profile` as described in [INSTALL.md](INSTALL.md). On Windows, use `py -3` instead of `python3` if needed. Start a new assistant session after installing.

To install for one existing project instead:

```sh
python3 install.py --agent codex --skills code-quality-analysis --project /path/to/project
python3 install.py --agent claude --skills code-quality-analysis --project /path/to/project
```

The installer copies the entire skill, including references and Codex UI metadata. It does not change assistant settings, install dependencies, or overwrite existing skills. Project installations can be committed with your project for teammates.

### Choose skills

```sh
python3 install.py --list
python3 install.py --agent codex --skills code-quality-analysis
python3 install.py --agent codex --all
```

`--skills` accepts one or more space-separated names. The same selection options work with `--agent claude` and `--agent hermes`. Unknown names fail before any installation; existing conflicts are checked across the selection before copying. If no selection is given, a sole available skill is installed; multiple available skills require `--skills` or explicit `--all`.

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
$code-quality-analysis Review this repository. Developer mode, report only, all applicable lenses.
```

In Claude Code:

```text
/code-quality-analysis Review this repository. Developer mode, report only, all applicable lenses.
```

In Hermes, ask to use `code-quality-analysis` with the same scope. Natural requests such as “analyze the codebase” or “find orphaned code” can also activate the skill.

The skill asks for a presentation mode and missing scope, discovers the stack, analyzes the selected lenses, verifies source citations, and provides a ranked report. It can also produce a self-contained implementation plan. Subagents are optional: when unavailable, the same checks run sequentially. No additional skills, MCP servers, or local models are required. A read-only request keeps discovery and plans in the conversation.

## Choose a presentation mode

| Mode | What you receive |
| --- | --- |
| **Developer** | Technical findings, source citations, confidence, and practical consequences |
| **Plain language** | An accessible architectural summary with a compact evidence trail; requested plans explain proposed changes, benefits, risks, and validation |
| **Learning** | Developer detail plus a short explanation of each distinct finding and proposed change |

All modes use the same analysis depth. “Non-technical” and “educate” are accepted as aliases. You can switch modes during the review. Every question offers **Explain this**; Learning provides that context automatically. An explanation does not choose an answer or authorize changes.

For read-only reviews, the skill reports observed findings and names useful checks for a proposed fix. After an authorized implementation, it compares measured code quality before and after on the same scope: physical source lines, added and deleted lines, finding-specific behavior, and relevant test or lint results. A line reduction alone does not establish an improvement. See [the measurement guide](code-quality-analysis/references/code-metrics.md).

For example:

```text
Use code-quality-analysis in Plain language mode. Review all applicable lenses, stay read-only, and include a small-change plan with reproducible before/after checks.
```

### Voice workshop

In Codex:

```text
$voice-workshop docs/home.md
```

In Claude Code and Hermes:

```text
/voice-workshop docs/home.md
```

The text after the command is the page or doc to review; with none, the skill asks for it. It presents one section at a time, edits the copy toward your voice, and records each decision — the rule, the before/after, and the reason — in a profile at `~/.voice-workshop/profile.md`. The profile grows across sessions, so future writing needs less editing. Ask for new copy instead of a review and the same profile is applied to the draft. See [the skill](voice-workshop/SKILL.md).

## Quality and embedded evaluations

The skill requires practical evidence before recommending abstraction, separates unsupported suspicions from findings, and reports incomplete coverage. Its four lenses are not a comprehensive security, performance, accessibility, or correctness audit.

The installable package includes [15 behavioral scenarios and a small fixture](code-quality-analysis/evals/README.md), covering audience modes, Explain this, false positives, evidence verification, read-only work, and deterministic code-quality measurement. [voice-workshop](voice-workshop/evals/README.md) ships [11 behavioral scenarios](voice-workshop/evals/cases.json) covering target resolution, one-section-at-a-time pacing, lesson capture, sign-off gating, applying the profile to new copy, and the always-on choice. They load only when evaluating a skill, not during normal reviews.

```sh
python3 code-quality-analysis/evals/validate.py
python3 voice-workshop/evals/validate.py
```

This validates the evaluation definitions and fixture behavior; it does not run an assistant or measure implemented changes. See [evaluation status](docs/quality-evaluation-notes.md) for what has and has not been tested.

## Update or uninstall

Run `git pull --ff-only` in this checkout to get updates. Identical reinstallations succeed without changes. To replace a differing installation, first back up any local edits and remove **only the installed `code-quality-analysis` directory** from the location above, then rerun the installer. Removing that directory also uninstalls the skill. Restart your assistant session afterward. Avoid duplicate personal and project copies unless you intend to manage both.

## Development

This repository is the canonical source; update installed copies from here.

```sh
python3 -m unittest discover -s tests -v
```

Tests install into temporary directories and check personal/project destinations, complete package copying, and protection of existing installations. They do not run live Codex, Claude Code, or Hermes sessions.

Version `1.4.0` adds deterministic before/after code-quality measurement for implemented changes. Version `1.3.0` introduced an optional token estimate, which `1.4.0` removes. Version `1.2.0` added audience modes, built-in explanations, stronger evidence rules, and embedded evaluations. Version `1.1.1` added URL-driven agent installation guidance, a Hermes profile-aware installer, and verified repeat installations. Version `1.1.0` introduced runtime-neutral instructions and Codex/Claude Code support. The original `1.0.0` import came from the maintained November 7, 2026 Hermes package.

## License

[MIT](LICENSE), copyright Rapidan Intelligent Automations & Jon Deavers.
