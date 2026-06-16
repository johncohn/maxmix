# Researcher Agent Output

- **timestamp:** 2026-06-16T01:05:32Z
- **exit_code:** 0

---

Research report written to `.factory/strategy/research.md`. Here's the summary:

---

## Key Findings

**Tech stack:** Single `index.html` + vanilla JS — no framework, no build step. Correct choice for GitHub Pages.

**Sequential playback:** Use **two `<video>` elements** (one playing, one preloading). The naive single-element src-swap produces a visible black gap between stanzas. The two-element swap — where the next clip is already buffered in the hidden element — eliminates most of this gap. MSE (Media Source Extensions) would be truly gapless but requires re-encoding all MP4s to fragmented format, which isn't worth it here.

**Autoplay constraint (biggest pitfall):** All browsers block audio autoplay without user interaction. The fix is `<video autoplay muted playsinline>` plus a "tap to start" overlay on first load. Users can then tap an unmute button. Without `muted`, autoplay silently fails on every mobile browser.

**GitHub Pages:** Perfectly suited for this. One constraint: individual files must be under 100 MB. Short "Happy Birthday" stanzas will be fine, but worth checking with `du -sh clips/*.mp4` before committing.

**Sequencing algorithm:** Simple — generate a playlist of 5 files per "song" by picking one stanza at a time with the "not same clip as previous" rule, always ending with `c5_s5`. Regenerate a new song each time the previous finishes.

**MVP deliverable:** One `index.html` file, ~80 lines of JS, deploys by pushing to `main` and enabling GitHub Pages in repo settings.
