# Voice profile format

The profile is the durable output of this skill. It is a plain markdown file the user owns, at `~/.voice-workshop/profile.md` unless another path was chosen. It grows as the user makes decisions, and it is meant to be read back into future writing.

## Structure

```markdown
# Voice Profile

Updated: <YYYY-MM-DD>
Sessions: <count>

## Voice in one line
<A single sentence that captures the user's voice. Revise it as the profile grows.>

## Rules
- <Imperative rule>. <Why it matters, in the user's terms.>

## Prefer
- "<phrase>" instead of "<alternative>"

## Avoid
- "<word or phrase>" — <why>

## Patterns
- Favor: <structural habit, e.g. short declarative sentences>
- Avoid: <structural habit, e.g. rule-of-three lists>

## Examples
### <short label>
- Before: "<original text>"
- After: "<edited text>"
- Why: <the reason the user gave>

## Open questions
- <A preference not yet settled; confirm next session.>
```

## How to add a lesson

A lesson has three parts: the rule, the concrete before/after, and the reason. Add all three or it is not a lesson.

1. **Rules** — the transferable, imperative form of the decision. "Use 'use', not 'utilize'." One rule per line.
2. **Prefer / Avoid** — word- and phrase-level vocabulary. These are the fastest to apply.
3. **Examples** — the evidence. Keep the before/after short; the point is to show the rule in action.
4. **Open questions** — anything the user hesitated on. Revisit it next session instead of guessing.

## Growth discipline

- **One decision, one entry.** Do not restate the same rule in two places.
- **Replace, do not stack.** When a new rule supersedes an old one, edit the old line — do not leave both.
- **Keep it scannable.** Bullets and short lines. The user should be able to read the whole profile in one pass.
- **Date the session, not every line.** One `Updated:` line and a session count is enough.
- **Never invent.** If the user did not decide it, it does not go in.

## Multiple profiles

A user may keep more than one voice (for example, personal and work). Store each as `~/.voice-workshop/<name>.md` and pass the name when invoking. `profile.md` is the default.

## Where the profile lives

Default: `~/.voice-workshop/profile.md`. If the user wants the profile kept with a project, use a path inside that project and record it so the next session finds it. Never store the profile inside this skill's own directory — a reinstall would fail against local edits.

Notes that describe one machine's arrangement are not part of the skill's behaviour. Keep them out of the published copy; the only arrangement the skill promises is the default path above.

### Verifying a moved or symlinked profile

When the user asks that the profile survive a new session, a local file is not enough — prove it. Run these checks and report the results rather than asserting success:

1. **The documented path resolves to the canonical file.** Resolve the link and compare checksums of the documented path and its target. One file, not two copies that will drift.
2. **Writes through the documented path land in the canonical file.** Timestamp the target, append through the documented path, timestamp it again — the mtime must move.
3. **The sync tool picked it up.** Ask the tool for its own status. A file sitting in a synced folder is not a synced file until the client reports it.
4. **The profile still validates.** Run `scripts/voice_profile.py validate`. It follows symlinks, so a pass confirms the documented path is readable with every required section present.

Also record the resume point in Open questions — which sections were signed off, which one is next — or a new session restarts the review from the top.
