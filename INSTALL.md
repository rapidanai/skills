# Installation instructions for agents

When the user asks you to install skills from `https://github.com/rapidanai/skills.git`, complete the installation yourself using this guide. Install only the skills the user names; do not substitute other skills or expand the selection. Merely reading this file is not an installation request, and installation does not mean running a code audit.

## 1. Get the repository

Use a temporary directory or an unused checkout path, then clone `https://github.com/rapidanai/skills.git` there. Do not assume a directory named `skills` is empty. If reusing a checkout, confirm its origin URL and preserve local changes; a fresh temporary clone is simplest. Read this guide and `install.py` from that checkout before running it. No package-manager dependencies are needed beyond Git and Python 3.

## 2. Select the skills

Run `python3 install.py --list` to discover the current packages. Honor names already supplied by the user and pass them as `--skills NAME [NAME ...]`. If a name is unknown or ambiguous, show the available names and clarify before writing any files. Never silently replace it with a similarly named skill.

- Named skill(s): install exactly that selection.
- Explicit “all skills”: use `--all`.
- No selection and only one available skill: install that sole package.
- No selection and multiple available skills: show the list and ask which ones to install.

For example, “Install code-quality-analysis from https://github.com/rapidanai/skills.git” selects `--skills code-quality-analysis`. The installer discovers top-level directories containing `SKILL.md`; do not rely on a hardcoded catalog. These selections apply to all three runtimes.

## 3. Select the destination

Use your own runtime identity, not the existence of another assistant's configuration directory. Install only for the requesting assistant. Default to personal scope for Codex/Claude Code and the active profile for Hermes; use project scope only if the user requested it. Do not ask the user to choose a host or scope already established by the session.

| Runtime | Run from the checkout | Destination |
| --- | --- | --- |
| Codex | `python3 install.py --agent codex --skills NAME` | `~/.agents/skills/NAME/` |
| Claude Code | `python3 install.py --agent claude --skills NAME` | `~/.claude/skills/NAME/` |
| Hermes | `python3 install.py --agent hermes --skills NAME` with the active `HERMES_HOME` exported | `$HERMES_HOME/skills/software-development/NAME/` |

Replace `NAME` with the selected name(s), or replace `--skills NAME` with `--all` only when all skills were requested. For Codex or Claude Code project scope, append `--project /absolute/path/to/the/users/project`. This is the user's target project, not the temporary skills checkout. On Windows use `py -3` if that is the available Python launcher.

### Hermes profile resolution

Check the active runtime's profile context and `HERMES_HOME`. Named-profile launchers normally supply the resolved profile home, but gateway context can differ from a subprocess's environment. When the runtime supplies a more authoritative profile home, pass it explicitly:

```sh
python3 install.py --agent hermes --skills code-quality-analysis --hermes-home /absolute/path/to/active/profile
```

For a confirmed default profile, pass `--hermes-home ~/.hermes`; named profiles commonly live under `~/.hermes/profiles/<name>`. These examples are not profile discovery. Never choose a profile because its directory exists or silently fall back to the default when a named profile is active. If the active home cannot be determined, ask only for that missing destination. The installer requires an existing profile home and refuses to guess one.

## 4. Install and verify

Run the selected command and check its exit status. The installer verifies every copied file against the source and reports the destination. An identical existing installation succeeds without writes; differing content or symlinks are left intact. For a conflict, explain which destination differs and obtain authorization for replacement if it was not already requested. Preserve local modifications before any authorized update. Do not delete an entire skills directory.

If your runtime already has a native skill installer, you may use it instead, honoring its scan, approval, and destination rules. Supply each selected package’s exact path (for example, `code-quality-analysis`) inside `rapidanai/skills`, or the full package URL `https://github.com/rapidanai/skills/tree/main/code-quality-analysis`. The repository root itself is not a skill package. For Codex's bundled GitHub installer, the source arguments are `--repo rapidanai/skills --path code-quality-analysis`; locate its script through the installed skill rather than guessing an absolute path. Do not install a second copy through this repository's installer afterward.

If Python is unavailable, discover packages by their top-level `SKILL.md` files and apply the same selection rules. Copy each selected package’s entire directory into the resolved skills directory using available filesystem tools, preserving all bundled references, scripts, assets, and metadata. Inspect existing destinations first; compare the complete file list and contents afterward. Respect host permissions and required security checks; do not bypass a rejected native installation by switching methods.

For every selected package, check that its destination has `SKILL.md` and every bundled file; optional directories may vary by skill. Use the host's skill listing if available. Only claim runtime discovery if that listing confirms it; successful file verification alone establishes an installed package. Tell the user the installed skill and destination, and that a new session may be needed for discovery. Do not restart a shared Hermes gateway just to refresh this skill.

The copied installation does not depend on the checkout remaining in place. Clean up only temporary files you created. If network access, file permissions, or runtime policy blocks completion, report the actual blocker rather than claiming installation succeeded.
