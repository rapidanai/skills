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

## Wiring it in

The preflight only fires if the agent is told to run it. Pick the layer that fits the host:

- **Global instructions.** Add one line to the agent's standing context — `AGENTS.md`, `CLAUDE.md`, or the host's memory: "Before writing user-facing copy, read `~/.voice-workshop/profile.md` and apply it." This catches every writing task, including ad-hoc ones.
- **Content skills.** In each skill that generates copy (blog, landing page, email, ads), add the preflight as its first step. This makes the check part of a skill that is already loading.
- **Hermes auto-load.** Set `skills.auto_load: [voice-workshop]` so the skill — and this convention — is present in every session.

Use more than one if you want belt and suspenders; they do not conflict.

## What this is not

- Not a style filter applied after the fact. Read the profile first, then write.
- Not a reason to skip the workshop. The profile is only as good as the lessons captured in it.
