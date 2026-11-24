---
name: voice-workshop
description: Use when reviewing a page or doc to capture the user's writing voice.
license: MIT
metadata:
  version: "1.0.0"
  author: Jon Deavers
---

# Voice Workshop

Review a page or document one section at a time with the user, edit the copy toward their voice, and record every decision in a living voice profile. The profile is the durable output: it accumulates the user's preferences so future writing needs less editing.

This skill edits copy and maintains the profile. It does not publish, deploy, or commit anything unless the user asks.

## Runtime adaptation

This skill supports Codex, Claude Code, and Hermes. Use only the tools available in the session; read [runtime guidance](references/runtimes.md) for your host. Resolve reference links relative to this skill's installed directory and content paths relative to the user's project.

## Workflow

### 0. Resolve the target and load the profile

Take the page or document from the invocation — the text the user typed after the slash command. If none was given, ask which page or doc to review and wait for the answer.

The voice profile lives at `~/.voice-workshop/profile.md`. If it does not exist, create it from [the template](templates/profile.md) before editing anything. A user-named profile uses `~/.voice-workshop/<name>.md`. See [profile format](references/profile-format.md).

Read the profile first. Its rules are active guidance for every edit this session.

### 1. Read the target and list its sections

Read the whole page or doc, then enumerate its sections in order — headings for a document, or the natural blocks of a page (hero, body, calls to action). Show the list and confirm where to start.

### 2. Review one section at a time

Follow [the review loop](references/review-loop.md) for each section:

1. Present the section's current text verbatim, formatted to read.
2. Wait for the user's reaction. Let them speak first; do not pre-emptively offer rewrites.
3. Apply their corrections exactly, then show the revised section in full.
4. Get a sign-off before advancing. Do not start the next section until the current one is approved.

### 3. Capture the lesson

Once a section is signed off, extract the transferable lesson and append it to the profile using [profile format](references/profile-format.md). A lesson is a rule plus the concrete before/after that justifies it. Record only what the user actually decided — never infer a preference from silence.

Confirm the update in one line, then continue.

### 4. Close

When the review ends, summarize: sections edited, lessons captured, and the profile path. Offer to apply the profile to other pages or to use it when writing new content.

## Pitfalls

- Do not dump the whole page at once. One section, then wait.
- Do not invent preferences. Every lesson needs the user's explicit choice behind it.
- Do not rewrite copy the user has not asked you to touch.
- Do not treat your own taste as the user's voice.
- Do not let the profile accumulate sediment: when a new rule replaces an old one, remove the old wording.

## Verification

- Every edited section was shown to the user and signed off.
- Every profile entry traces to a specific user decision.
- The profile file exists at the documented path with the required sections.
