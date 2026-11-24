# Applying the profile

The workshop builds the profile; this file is how the profile gets used. The profile at `~/.voice-workshop/profile.md` is the user's voice, and any copy the agent writes for that user should follow it.

## The preflight

Before generating or editing user-facing copy — a page, a post, an email, an ad, a headline — read the profile and apply it:

1. Read `~/.voice-workshop/profile.md`. If it does not exist, write normally and offer to build one with the workshop.
2. Apply its **Rules**, **Prefer**, **Avoid**, and **Patterns** to the draft. These are the user's decisions; treat them as requirements, not suggestions.
3. Where the profile is silent, write normally. Do not invent a voice rule the profile does not state.
4. If a rule is ambiguous for this piece, ask one question rather than guessing.

The profile guides the copy; it is not a checklist to quote back. The reader should feel the voice, not see the rule.

## The feedback loop

When the user corrects copy the agent wrote, that correction is a new lesson:

- Capture it the same way the workshop does: a rule plus the before/after that justifies it (see [profile format](profile-format.md)).
- Append it to the profile and confirm in one line.
- Do not wait for a formal review session. A correction during generation is exactly the signal the profile exists to collect.

This is what keeps the profile growing: every draft that gets corrected makes the next draft closer.

## Setting it up: always-on or skills-only

The preflight only fires if the agent is told to run it, and there are two levels. They trade off differently, so when the user asks the skill to apply their voice, ask which they want and explain the trade-off before wiring anything.

**Always-on** — a standing instruction in the agent's context, so the profile is checked for *every* writing request, including one-off copy typed in chat ("draft a LinkedIn post").

- Pros: catches everything; the voice stays consistent even outside the named content skills.
- Cons: occupies a little of the agent's context in every session, including sessions with nothing to do with writing.

**Skills-only** — the check lives inside the content skills (blog, landing page, email, ads).

- Pros: no per-session cost; the check runs exactly when a content skill runs.
- Cons: misses ad-hoc writing that does not go through a named skill.

Neither is wrong, and they combine. Always-on suits someone who writes in chat often; skills-only suits someone whose writing mostly goes through the named skills.

### Wiring the choice

| Host | Always-on | Skills-only |
| --- | --- | --- |
| Hermes | `skills.auto_load: [voice-workshop]` in `config.yaml` | nothing to set |
| Codex | one line in `AGENTS.md` | nothing to set |
| Claude Code | one line in `CLAUDE.md` | nothing to set |

The always-on line, whatever the host: "Before writing user-facing copy, read `~/.voice-workshop/profile.md` and apply it."

After wiring, state what was set and where, so the user can change it later.

## What this is not

- Not a style filter applied after the fact. Read the profile first, then write.
- Not a reason to skip the workshop. The profile is only as good as the lessons captured in it.
