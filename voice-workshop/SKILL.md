---
name: voice-workshop
description: Use when capturing or applying the user's writing voice.
license: MIT
metadata:
  version: "1.1.0"
  author: Jon Deavers
---

# Voice Workshop

Build a living record of the user's writing voice, then use it. **Capture** reviews a page or document one section at a time and records every decision in a profile at `~/.voice-workshop/profile.md`. **Apply** reads that profile and writes new copy in the user's voice. The profile is the durable output: it accumulates the user's preferences so future writing needs less editing.

This skill edits copy and maintains the profile. It does not publish, deploy, or commit anything unless the user asks.

## Two modes

- **Capture** — the user names a page or doc to review. Run the capture workflow below.
- **Apply** — the user asks for new copy (a page, post, email, ad). Read the profile and write in the user's voice; see [applying the profile](references/applying.md). Do not run the review loop unless asked.

If the invocation is ambiguous, ask which the user wants.

## Runtime adaptation

This skill supports Codex, Claude Code, and Hermes. Use only the tools available in the session; read [runtime guidance](references/runtimes.md) for your host. Resolve reference links relative to this skill's installed directory and content paths relative to the user's project.

## Capture workflow

### 0. Resolve the target and load the profile

Take the page or document from the invocation — the text the user typed after the slash command. If none was given, ask which page or doc to review and wait for the answer.

The voice profile lives at `~/.voice-workshop/profile.md`. If it does not exist, create it from [the template](templates/profile.md) before editing anything. A user-named profile uses `~/.voice-workshop/<name>.md`. See [profile format](references/profile-format.md).

Before creating anything, check for a broken symlink. If the path is a symlink whose target is missing, restore the target from the documented mirror instead of writing a blank profile over it — a fresh profile silently discards every decision the user has made. On the first write of a session, bump `Sessions` and update the `Updated:` date.

Read the profile first. Its rules are active guidance for every edit this session.

### 1. Read the target and list its sections

Read the whole page or doc, then enumerate its sections in order — headings for a document, or the natural blocks of a page (hero, body, calls to action). Show the list and confirm where to start.

When the page is already recorded in the profile, still start where the user says — normally the top. The profile's Examples show which sections were already decided; present each one's current text and confirm it rather than re-arguing it. A settled decision reopens only if the user reopens it.

When the target is a web page backed by a local build (dev server or preview URL), read the source file on disk rather than extracting from the URL: the source gives verbatim copy and the real heading hierarchy, while rendered text loses the emphasis spans and section order. Use the browser only to confirm what actually renders.

Edit the source, never the build output. On a component-built site the copy lives in a page component (e.g. `src/pages/*.jsx`) and its styles in a sibling `.css`; a prerendered `dist/**/*.html` is generated and gitignored, so an edit there is erased by the next build. Locate the component first by searching the repo for a distinctive phrase from the copy, change it there, then rebuild and re-run the prerender step before screenshotting the result.

On a Vite-style site the loop is a build followed by a separate prerender pass. Redirect the build to a log (`npx vite build > /tmp/vb.log 2>&1; echo "EXIT=$?"; tail -20 /tmp/vb.log`) — the terminal tool mistakes a bare `vite build` for a long-lived server and refuses to run it in the foreground. Check the exit code before prerendering; a failed build leaves the old `dist` in place and the prerender silently renders stale copy. After prerendering, confirm the change landed in the generated HTML (`grep -o '<new phrase>' dist/<route>.html`) and only then screenshot the served page.

### 2. Review one section at a time

Follow [the review loop](references/review-loop.md) for each section:

1. Present the section's current text verbatim, formatted to read.
2. Wait for the user's reaction. Let them speak first; do not pre-emptively offer rewrites.
3. Apply their corrections exactly, then show the revised section in full.
4. Get a sign-off before advancing. Do not start the next section until the current one is approved.

### 3. Capture the lesson

Once a section is signed off, extract the transferable lesson and append it to the profile using [profile format](references/profile-format.md). A lesson is a rule plus the concrete before/after that justifies it. Record only what the user actually decided — never infer a preference from silence.

When the user states a standing rule — a cliché they always want avoided, a construction they hate — capture it immediately, before the section is signed off. Standing rules are global: they govern every remaining section and every future page. Record the rule under Rules or Avoid, then scan the rest of the document for the same violation and flag each instance as you reach it. Flagging is not rewriting: say where the violation is and let the user decide. The user should not have to catch the same cliché five times.

Confirm the update in one line, then continue.

### 4. Close

When the review ends, summarize: sections edited, lessons captured, and the profile path. Offer to apply the profile to other pages or to use it when writing new content.

If the review stops early — the session is ending, or the user wants to pick it up later — write the status into the profile's Open questions: which sections were signed off, which remain, any unresolved decision, and the source files that hold the copy. Record it as status, never as a command to resume — a later session still starts where the user says, normally the top, and reads the note only to know what is already settled. A profile that records only the lessons leaves the next session answering "where did we leave off" from memory instead of from the source tree.

## Applying the profile

When the user asks for new copy rather than a review, read `~/.voice-workshop/profile.md` and apply its Rules, Prefer, Avoid, and Patterns to the draft. Capture any correction the user makes as a new lesson, the same way the capture workflow does.

When the user asks the skill to apply their voice, ask whether the preflight should be **always-on** or **skills-only**, explain the trade-off, then wire it for the host and say what was set. Full protocol: [applying the profile](references/applying.md).

## Pitfalls

- Do not dump the whole page at once. One section, then wait.
- Do not invent preferences. Every lesson needs the user's explicit choice behind it.
- Do not rewrite copy the user has not asked you to touch.
- Do not treat your own taste as the user's voice.
- Do not let the profile accumulate sediment: when a new rule replaces an old one, remove the old wording.
- The profile is private state, not part of the skill. It holds the user's own voice and their clients' business — never commit it to a public skills repo, quote it into a published skill, or ship a template containing it. A local mirror (a symlink into a synced folder) is a backup, not a publish: it protects the user's decisions and does nothing for anyone who installs the skill.
- Keep machine-specific notes out of this skill's own files. A path that exists on one machine is what leaks into a public copy; record it outside the skill, or mark it for removal and verify the published copy is clean.
- Do not hold a standing rule until the section is approved. A rule the user frames as "I always want to avoid this" is global and durable — write it to the profile the moment it is spoken, then apply it to the remaining sections.
- When the target is a single-line minified HTML file, the patch tool's diff returns the entire file and is unreadable. Verify the edit with a targeted grep on the changed string instead of reading the diff.
- Do not silently enable always-on. Ask, explain the trade-off, and name what you changed.
- When the user rejects a visual element rather than the words — a label chip, a badge, a tag — the fix is a component and CSS change, not a copy edit. Record the visual preference in the profile under Patterns with its before/after, and check whether the same element appears elsewhere on the page before the user has to point at it again. Report the other instances and let them decide; structural labels that mark states may still be justified.
- A rejected label gets one of two treatments, and the choice is not automatic. Ask what the label was carrying. If it restated something the surrounding copy already says, remove it and let the sentence carry the idea — numbered step chips in an eyebrow are the usual case, because the section name already gives the order and the number only makes the reader count. If it named an idea the copy does not otherwise state, replace it with a graphic watermark rather than a different chip. The user's standing preference for the watermark case: a small line-art icon set behind the text at low opacity, bleeding past the block's corner, instead of a black rectangle naming the idea. Build one icon family and reuse it — same stroke weight, same viewBox, same opacity band, same corner — so the marks read as a set. Pick the icon from the caption's subject, not from the label's words: a caption about a decision window gets a stopwatch, a caption about a solved chore gets a clipboard, a caption about photographs gets a camera.
- Implement the watermark as an inline SVG child of the text block: the block needs `position:relative` and `overflow:hidden`, the mark is `position:absolute` bled past the corner (`right`/`bottom` negative) at roughly 8–13% ink, and the copy needs `position:relative;z-index:1` so it stays above. When the mark is a prop on a shared caption component, gate it (`mark ? ' cb-cap--mark' : ''`) so blocks that still want a label keep working. Verify by reading the computed style and bounding box in the browser, not by eye alone.
- For the remove branch: when the element comes from a shared component, do not delete it from the component — that silently strips it from every sibling page. Make the prop optional (`{n && <span …>}`) and drop the prop at the one call site, then prove the scope by counting the token in each prerendered page (`grep -o 'class-token' dist/<route>.html | wc -l`). Report the sibling pages that still show it and let the user decide whether the whole set should change; a case study split across two pages goes out of step the moment only one is swept.
- Do not enumerate a page's sections by grepping every heading tag when the page embeds before/after mockups — each mock repeats the same copy, so results come back several times over and bury the real structure. Filter to top-level sections and their chapter labels, strip the nested mock markup, and present each section's copy once.
- When the user gives a directional correction rather than exact wording — "tone it down", "make it more relatable", "say this differently" — do not wait for them to write the line. Draft two or three candidates, apply the strongest one, show the revised section in full, and list the alternates in one line so they can swap. Record the applied line as the lesson with the user's direction behind it.
- Designer and CRO shorthand is not the owner's language. When copy describes a page, use the words the business owner uses — "homepage" not "first screen," "above the fold," "hero," or "landing page." A sole proprietor has a homepage; designers have first screens. This is a category of correction, not a one-off: expect it to recur wherever marketing copy borrows design vocabulary.
- Scale the stakes to the business. A one-person operation does not have "everything that mattered" buried; it has a homepage that skipped the reason to call. When a line reads as dramatic, the fix is usually to shrink the claim to the size of the business rather than to soften the adjectives. Critic language — "buried," "everything," "destroyed" — is the tell.
- A terminology correction is a rename, not a one-line edit. When the user swaps a word for their preferred term ("first screen" → "homepage"), grep the source for the old term and change every user-facing occurrence — headings, body copy, mock captions, alt text, slider labels — then rebuild and verify. Clichéd constructions are the opposite: flag each instance and let the user decide.

## Verification

- Every edited section was shown to the user and signed off.
- Every profile entry traces to a specific user decision.
- The profile file exists at the documented path with the required sections. When the user asked that it survive a new session, the documented path resolves to a backed-up canonical file and writes were verified through it — see [verifying a moved profile](references/profile-format.md). Do not report "preserved" on the strength of having written a local file.
- New copy was written only after reading the profile, and any correction was captured.
- Every change was confirmed in the rebuilt, rendered page — grep the prerendered output for the new string and screenshot the section — not just in the source diff.
