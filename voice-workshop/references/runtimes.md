# Runtime guidance

Use the host's exposed tool schemas rather than assuming tool names from another runtime.

| Host | Explicit invocation | Profile path |
| --- | --- | --- |
| Codex | `$voice-workshop <page or doc>` | `~/.voice-workshop/profile.md` |
| Claude Code | `/voice-workshop <page or doc>` | `~/.voice-workshop/profile.md` |
| Hermes | `/voice-workshop <page or doc>` (installed skills are slash commands) | `~/.voice-workshop/profile.md` |

In every host, the text after the command is the page or doc to review. With no text, ask for it and wait.

## Tools

- Read files with the host's file tool (`read_file` in Hermes; Read in Claude Code; shell/file tools in Codex).
- Edit files with the host's edit tool (`patch` and `write_file` in Hermes).
- Ask a question with the host's question tool when exposed (`clarify` in Hermes), otherwise in chat.

## Path resolution

`~` resolves to the user's home directory on every host. On Windows, resolve it to `%USERPROFILE%`. Create the `~/.voice-workshop/` directory if it is missing. Never store the profile inside this skill's own directory — a reinstall would fail against local edits.
