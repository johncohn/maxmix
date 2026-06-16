# Research Report — MaxMix Happy Birthday Mashup Site

## Project Summary

A single-page static website that endlessly plays randomized mashups of "Happy Birthday" by
sequencing MP4 video stanzas from 5 clips. Each clip (C1–C5) has 4–5 stanzas (S1–S5), stored as
`cx_sy.mp4`. A "song" is assembled from one stanza per position (S1–S5), choosing a different clip
each time, and always ending with `c5_s5`. The site must host on GitHub Pages with no server-side
code.

---

## 1. Hosting: GitHub Pages

**Verdict: Fully viable with one critical constraint.**

GitHub Pages serves static files (HTML, JS, CSS, MP4) directly from a repo branch. Setup is trivial:
enable Pages in repo Settings → choose `main` branch root. The site will be live at
`https://johncohn.github.io/maxmix/` (or custom domain).

**Critical constraint — file size:**
- Hard limit: **100 MB per individual file** (via git push; browser UI limit is 25 MB)
- Repo size: strongly recommended under 1 GB; GitHub flags repos over 5 GB
- GitHub Pages is not designed for heavy media serving — rate limiting may appear if traffic is heavy

**Implication:** If any MP4 clip stanza exceeds 100 MB, it cannot be committed to git directly and
Git LFS would be required (which complicates GitHub Pages serving). Short stanzas of "Happy Birthday"
(a few seconds each) should be well within limits. Verify clip sizes with `du -sh clips/*.mp4` before
committing.

---

## 2. Sequential Video Playback — Core Challenge

### 2a. Simple `ended`-event approach (baseline)

The simplest implementation: one `<video>` element, listen for the `ended` event, set `.src` to the
next clip, call `.load()` then `.play()`.

```javascript
videoEl.addEventListener('ended', () => {
  videoEl.src = nextClip();
  videoEl.load();
  videoEl.play();
});
```

**Problem:** Changing `src` and calling `load()` causes a brief blank/black frame gap between clips
— typically 100–400 ms depending on network and browser. For stanzas of a song this gap will be
perceptible and jarring.

### 2b. Two-video element swap (recommended for this project)

Use two `<video>` elements overlaid. One plays (visible); the other preloads the next clip in the
background (hidden). When the current clip ends, swap visibility instantly and start the preloaded
one. Meanwhile, preload the one-after-next into the now-hidden element.

```html
<video id="vidA" autoplay muted playsinline></video>
<video id="vidB" muted playsinline style="display:none"></video>
```

```javascript
// As soon as vidA starts playing, load next clip into vidB
// On vidA 'ended': show vidB, hide vidA, play vidB, load next-next into vidA
```

**Advantages:**
- Eliminates most of the gap — the next clip is already buffered
- Works with plain MP4 files, no re-encoding needed
- No third-party libraries
- ~50 lines of vanilla JS

**Remaining gap risk:** The swap itself takes one or two frames (~16–33 ms). For MP4 files with a
non-zero initial PTS, a flash may still be visible. Setting `preload="auto"` on the hidden element
and waiting for `canplaythrough` before swapping helps.

### 2c. Media Source Extensions (MSE) — advanced, skip for MVP

MSE allows appending raw coded video bytes to a `SourceBuffer` for truly gapless playback. However:
- Requires **fragmented MP4 (fMP4/CMAF)** format, not plain MP4 — clips would need re-encoding with
  `ffmpeg -movflags frag_keyframe+empty_moov`
- Significantly more complex (fetch → ArrayBuffer → append → manage buffer lifecycle)
- Overkill for 5-second stanzas where the two-video swap approach is sufficient
- **Not recommended for MVP**

---

## 3. Autoplay Constraints — Critical

Modern browsers block autoplaying media with audio unless the user has interacted with the page.

**The universal workaround: `muted + playsinline + autoplay`**

```html
<video autoplay muted playsinline></video>
```

- `muted` — required for autoplay without prior user interaction (Chrome, Firefox, Safari)
- `playsinline` — required on iOS Safari to prevent forcing full-screen and to allow autoplay
- `autoplay` — tells browser to start when ready

**Result:** Video plays silently on load. User must tap/click an unmute button to hear audio.

**Programmatic play() must handle rejection:**

```javascript
const playPromise = video.play();
if (playPromise !== undefined) {
  playPromise.catch(() => {
    // Show a "tap to play" overlay; remove it on user click, then play()
  });
}
```

**iOS-specific note:** On iOS Safari, even `muted + playsinline` may not autoplay without a prior
user gesture in some configurations. The safest fallback is showing a full-screen "tap to start"
overlay that triggers `video.play()` on the first touch event.

---

## 4. Sequencing Algorithm

### File naming structure
```
clips/c1_s1.mp4  clips/c1_s2.mp4  clips/c1_s3.mp4  clips/c1_s4.mp4
clips/c2_s1.mp4  clips/c2_s2.mp4  clips/c2_s3.mp4  clips/c2_s4.mp4
clips/c3_s1.mp4  clips/c3_s2.mp4  clips/c3_s3.mp4  clips/c3_s4.mp4  clips/c3_s5.mp4
clips/c4_s1.mp4  clips/c4_s2.mp4  clips/c4_s3.mp4  clips/c4_s4.mp4
clips/c5_s1.mp4  clips/c5_s2.mp4  clips/c5_s3.mp4  clips/c5_s4.mp4  clips/c5_s5.mp4
```

### Rules
1. S1: random clip from {1,2,3,4,5}
2. S2: random clip ≠ S1's clip
3. S3: random clip ≠ S2's clip
4. S4: random clip ≠ S3's clip
5. S5: always clip 5 (`c5_s5`)
6. Repeat from step 1 indefinitely

### Implementation (pseudo-code)

```javascript
const NUM_CLIPS = 5;

function pickExcept(exclude) {
  const choices = [1, 2, 3, 4, 5].filter(n => n !== exclude);
  return choices[Math.floor(Math.random() * choices.length)];
}

function buildSong() {
  const s1 = Math.ceil(Math.random() * NUM_CLIPS);
  const s2 = pickExcept(s1);
  const s3 = pickExcept(s2);
  const s4 = pickExcept(s3);
  return [
    `clips/c${s1}_s1.mp4`,
    `clips/c${s2}_s2.mp4`,
    `clips/c${s3}_s3.mp4`,
    `clips/c${s4}_s4.mp4`,
    `clips/c5_s5.mp4`,
  ];
}

// Build a queue: generate songs lazily as previous ones finish
```

---

## 5. Recommended Tech Stack

| Concern | Choice | Rationale |
|---|---|---|
| Language | Vanilla JS (ES2020) | No build step, no npm, no framework — GitHub Pages serves as-is |
| HTML | Single `index.html` | Everything in one file; no routing needed |
| CSS | Inline or `<style>` block | Minimal styling — fullscreen black background, centered video |
| Video API | HTML5 `<video>` × 2 | Two-element swap; no library needed |
| Hosting | GitHub Pages, `main` branch root | Free, zero config, already the target repo |
| Build | None | Push and it's live |

**Framework verdict:** Do NOT use React, Vue, or any SPA framework. The logic is ~60–80 lines of JS.
A framework adds a build pipeline, a `node_modules` directory, and complexity that has zero benefit
here. Vanilla JS is the correct choice.

---

## 6. Potential Pitfalls

### P1 — Gap/flash between stanzas (HIGH risk)
The single `<video>` src-swap approach will produce an audible gap and visual black frame between
stanzas. **Mitigation:** two-video swap with preloading, waiting for `canplaythrough` event before
transition.

### P2 — Autoplay blocked (HIGH risk on mobile)
Without `muted + playsinline`, autoplay will silently fail on Chrome mobile and iOS Safari. On iOS,
even muted autoplay may require a user gesture. **Mitigation:** "tap to start" overlay; detect
`play()` promise rejection.

### P3 — GitHub Pages file size (MEDIUM risk)
MP4 clip files approaching or exceeding 100 MB cannot be committed. **Mitigation:** check sizes
before committing; re-encode at lower bitrate if needed (`ffmpeg -crf 28`); as last resort, use
Git LFS (note: Git LFS bandwidth on free GitHub is limited to 1 GB/month).

### P4 — iOS full-screen hijack (MEDIUM risk)
Without `playsinline`, iOS Safari forces the video into full-screen native player, breaking the
page layout. **Mitigation:** always include `playsinline`.

### P5 — `ended` event not firing (LOW risk)
If `loop` attribute is set, `ended` never fires. Never set `loop` on these elements. Also, `ended`
fires only when the video naturally reaches the end — not on error. Add an `error` handler to
gracefully skip a bad clip.

### P6 — c5_s5 always last but S4 might also be from c5 (edge case)
If S4 picks clip 5 (allowed, since the restriction is "not same as S3"), then `c5_s4` plays
immediately before `c5_s5`. These are different files so no conflict, but they're from the same
clip back-to-back. The spec does not prohibit this — it's acceptable behavior.

### P7 — Not all clips have S5 (LOW risk)
Only `c5` has `s5` (based on the "last one has S5" description). The algorithm hardcodes `c5_s5`
as the final stanza, so this is not an issue as long as `c5_s5.mp4` exists.

---

## 7. MVP Scope

**What's needed for a working MVP:**
1. `index.html` — single file with inline CSS + JS
2. `clips/` directory — already exists per spec
3. GitHub Pages enabled on `main` branch

**What index.html must do:**
- Full-viewport black background, video centered
- Two `<video>` elements (one hidden) with `muted playsinline`
- "Tap to start" overlay (shown on initial load, hidden on first play)
- Optional unmute button (bottom-right corner)
- Playlist generator using sequencing rules
- Two-video swap on `ended` with preloading of next clip
- Loop: when queue drains, generate a new song and append to queue

**What is explicitly out of scope for MVP:**
- Audio controls beyond a simple unmute toggle
- Visual UI beyond a simple dark background
- Any analytics or tracking
- Service workers / offline caching
- Multiple quality levels or adaptive bitrate

---

## 8. Similar Projects / Prior Art

- **BBC `media-sequence` library** (github.com/bbcrd/media-sequence): HTML5 media sequencing API
  that chains clips via a playlist. Well-documented but adds a dependency; overkill for 5 clips.
- **video.js playlist plugin**: Mature but heavyweight (50 KB+ library) — unnecessary here.
- **MSE demo by Bitmovin** (github.com/bitmovin/mse-demo): Good reference for truly gapless but
  requires fMP4 re-encoding.

No archive prior knowledge on similar projects was found in `.factory/archive/`.

---

## Sources

- [MDN: Autoplay guide for media and Web Audio APIs](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
- [MDN: HTMLMediaElement: ended event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/ended_event)
- [Chrome Developers: Autoplay policy in Chrome](https://developer.chrome.com/blog/autoplay)
- [MDN: Media Source Extensions API](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API)
- [GitHub Pages official documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub community: Uploading large MP4 files onto Git Pages](https://github.com/orgs/community/discussions/22302)
- [Mux: Video autoplay considered harmful](https://www.mux.com/blog/video-autoplay-considered-harmful)
- [SiteLint: Fixing HTML video autoplay in Safari and iOS](https://www.sitelint.com/blog/fixing-html-video-autoplay-blank-poster-first-frame-and-improving-performance-in-safari-and-ios-devices)
