# Installation instructions for agents

When the user asks you to install skills from `https://github.com/rapidanai/skills.git`, complete the installation yourself using this guide. The repository currently supplies one skill, `code-quality-analysis`; install that package. Merely reading this file is not an installation request, and installation does not mean running a code audit.

## 1. Get the repository

Use a temporary directory or an unused checkout path, then clone `https://github.com/rapidanai/skills.git` there. Do not assume a directory named `skills` is empty. If reusing a checkout, confirm its origin URL and preserve local changes; a fresh temporary clone is simplest. Read this guide and `install.py` from that checkout before running it. No package-manager dependencies are needed beyond Git and Python 3.

## 2. Select the destination

Use your own runtime identity, not the existence of another assistant's configuration directory. Install only for the requesting assistant. Default to personal scope for Codex/Claude Code and the active profile for Hermes; use project scope only if the user requested it. Do not ask the user to choose a host or scope already established by the session.

| Runtime | Run from the checkout | Destination |
| --- | --- | --- |
| Codex | `python3 install.py --agent codex` | `~/.agents/skills/code-quality-analysis/` |
| Claude Code | `python3 install.py --agent claude` | `~/.claude/skills/code-quality-analysis/` |
| Hermes | `python3 install.py --agent hermes` with the active `HERMES_HOME` exported | `$HERMES_HOME/skills/software-development/code-quality-analysis/` |

For Codex or Claude Code project scope, append `--project /absolute/path/to/the/users/project`. This is the user's target project, not the temporary skills checkout. On Windows use `py -3` if that is the available Python launcher.

### Hermes profile resolution

Check the active runtime's profile context and `HERMES_HOME`. Named-profile launchers normally supply the resolved profile home, but gateway context can differ from a subprocess's environment. When the runtime supplies a more authoritative profile home, pass it explicitly:

```sh
python3 install.py --agent hermes --hermes-home /absolute/path/to/active/profile
```

For a confirmed default profile, pass `--hermes-home ~/.hermes`; named profiles commonly live under `~/.hermes/profiles/<name>`. These examples are not profile discovery. Never choose a profile because its directory exists or silently fall back to the default when a named profile is active. If the active home cannot be determined, ask only for that missing destination. The installer requires an existing profile home and refuses to guess one.

## 3. Install and verify

Run the selected command and check its exit status. The installer verifies every copied file against the source and reports the destination. An identical existing installation succeeds without writes; differing content or symlinks are left intact. For a conflict, explain which destination differs and obtain authorization for replacement if it was not already requested. Preserve local modifications before any authorized update. Do not delete an entire skills directory.

If your runtime already has a native skill installer, you may use it instead, honoring its scan, approval, and destination rules. Supply the exact package path `code-quality-analysis` inside `rapidanai/skills`, or the full package URL `https://github.com/rapidanai/skills/tree/main/code-quality-analysis`. The repository root itself is not a skill package. For Codex's bundled GitHub installer, the source arguments are `--repo rapidanai/skills --path code-quality-analysis`; locate its script through the installed skill rather than guessing an absolute path. Do not install a second copy through this repository's installer afterward.

If Python is unavailable, copy the entire `code-quality-analysis/` directory into the resolved skills directory using available filesystem tools, preserving the reference tree and `agents/openai.yaml`. Inspect existing destinations first; compare the complete file list and contents afterward. Respect host permissions and required security checks; do not bypass a rejected native installation by switching methods.

Check that the destination has `SKILL.md`, `agents/openai.yaml`, and every document under `references/`. Use the host's skill listing if available. Only claim runtime discovery if that listing confirms it; successful file verification alone establishes an installed package. Tell the user the installed skill and destination, and that a new session may be needed for discovery. Do not restart a shared Hermes gateway just to refresh this skill.

The copied installation does not depend on the checkout remaining in place. Clean up only temporary files you created. If network access, file permissions, or runtime policy blocks completion, report the actual blocker rather than claiming installation succeeded.
