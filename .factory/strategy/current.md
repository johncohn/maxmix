## Build Plan — MaxMix Happy Birthday Mashup Site
## Generated: 2026-06-15

### Overview

Single-page static site serving randomized "Happy Birthday" mashups via sequential MP4 stanza playback. Hosted on GitHub Pages at `https://johncohn.github.io/maxmix/`. Main deliverable: one `index.html` using vanilla JS two-video element swap for seamless stanza transitions. No build step, no npm, no framework.

---

### Phase 1 — Project Scaffold + git/GitHub Setup

#### Issue #1: Initialize repo and push to GitHub

- Init git repo at `/Users/jcohn/factory-projects/maxmix`
- Create `clips/` directory with `.gitkeep` placeholder (video files will be added in Phase 3)
- Create `.gitignore` (ignore `.DS_Store`, `Thumbs.db`)
- Create minimal `README.md`: "MaxMix — Happy Birthday mashup player"
- Create the GitHub repo if it doesn't exist:
  ```bash
  gh repo create johncohn/maxmix --public --source=. --remote=origin --push
  ```
  If repo already exists, add remote and push:
  ```bash
  git remote add origin https://github.com/johncohn/maxmix.git
  git push -u origin main
  ```
- Initial commit includes `clips/.gitkeep`, `.gitignore`, `README.md`

**Acceptance:** `git remote -v` shows `johncohn/maxmix`; repo visible on GitHub with initial commit.

---

### Phase 2 — Core index.html Implementation

#### Issue #2: Build index.html — two-video swap player + sequencing logic

Implement `index.html` as a single self-contained file with inline `<style>` and `<script>`. No external dependencies.

**HTML structure:**
```html
<body>                          <!-- black background, overflow:hidden -->
  <video id="vidA" autoplay muted playsinline></video>
  <video id="vidB" muted playsinline style="display:none"></video>
  <div id="overlay">            <!-- full-screen tap-to-start, removed on first play -->
    <span>Tap to Start</span>
  </div>
  <button id="muteBtn">🔇</button>  <!-- fixed bottom-right, toggles muted -->
</body>
```

**Sequencing algorithm:**
```javascript
const CLIPS = [1, 2, 3, 4, 5];

function pickExcept(exclude) {
  const pool = CLIPS.filter(n => n !== exclude);
  return pool[Math.floor(Math.random() * pool.length)];
}

function buildSong() {
  const s1 = CLIPS[Math.floor(Math.random() * CLIPS.length)];
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
```

**Two-video swap logic:**
- Maintain `queue[]` of upcoming clip paths; when queue has fewer than 3 clips remaining, append another `buildSong()`
- `active` and `standby` variables reference the two video elements; swap references on each transition
- On `active.ended`:
  1. Show `standby`, hide `active`
  2. Call `standby.play()`
  3. Load `queue.shift()` into `active` (`active.src = next; active.load()`)
  4. Swap `active` ↔ `standby` references
- Preload: set `standby.src` and `standby.preload = "auto"` immediately after each swap so it buffers while active plays
- Error handler: on `active.error`, advance queue and load next clip (skip bad file gracefully)
- Never set `loop` attribute — it suppresses the `ended` event

**Autoplay and tap-to-start:**
```javascript
// Attempt silent autoplay on load
const p = vidA.play();
if (p !== undefined) {
  p.catch(() => {
    // Browser blocked autoplay — show overlay
    overlay.style.display = 'flex';
  });
}
// Overlay tap: resume play and dismiss
overlay.addEventListener('click', () => {
  active.play().then(() => overlay.remove());
}, { once: true });
```

**Unmute toggle:**
```javascript
muteBtn.addEventListener('click', () => {
  vidA.muted = vidB.muted = !vidA.muted;
  muteBtn.textContent = vidA.muted ? '🔇' : '🔊';
});
```

**CSS (inline `<style>`):**
- `body`: `margin:0; background:#000; overflow:hidden`
- `video`: `position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); max-width:100vw; max-height:100vh`
- `#overlay`: `position:fixed; inset:0; background:rgba(0,0,0,0.75); display:flex; align-items:center; justify-content:center; color:#fff; font-size:2rem; cursor:pointer; z-index:10`
- `#muteBtn`: `position:fixed; bottom:1rem; right:1rem; z-index:20; background:rgba(0,0,0,0.5); border:none; color:#fff; font-size:1.5rem; padding:0.5rem; cursor:pointer; border-radius:4px`

**Acceptance:** `index.html` served from repo root via `python3 -m http.server` plays stanzas in sequence; no black-frame gap between stanzas; overlay dismisses on tap; unmute toggle works; song loops indefinitely with fresh randomization each cycle.

---

### Phase 3 — Commit Video Clips

#### Issue #3: Verify clip sizes and commit clips/ to repo

- Run `du -sh clips/*.mp4` to confirm every file is under 100 MB (GitHub's hard per-file limit for plain git)
- Remove `clips/.gitkeep` added in Phase 1
- Stage and commit all MP4 files:
  ```bash
  git rm clips/.gitkeep
  git add clips/
  git commit -m "add video clip stanzas (cx_sy.mp4)"
  git push
  ```
- If any file exceeds 100 MB: do not commit — see **Deferred** section

**Acceptance:** `git ls-files clips/` lists all expected `cx_sy.mp4` files (c1_s1 through c5_s5 per the clip manifest); `git push` succeeds with no LFS warnings.

---

### Phase 4 — Enable GitHub Pages + Verify Deployment

#### Issue #4: Enable GitHub Pages and confirm live URL

- Enable GitHub Pages via gh CLI:
  ```bash
  gh api repos/johncohn/maxmix/pages \
    --method POST \
    -f source[branch]=main \
    -f source[path]=/
  ```
  (If Pages is already enabled, this is a no-op; check with `gh api repos/johncohn/maxmix/pages`)
- Poll until build completes:
  ```bash
  gh api repos/johncohn/maxmix/pages --jq '.status'
  # should return "built"
  ```
- Confirm site is live at `https://johncohn.github.io/maxmix/`
- Smoke-test checklist:
  - Overlay appears on load
  - Tapping overlay starts video playback
  - Stanzas play in sequence, each from a different clip (verify visually)
  - Song always ends with `c5_s5`
  - A new randomized song begins immediately after the previous one ends
  - Unmute button works on desktop and mobile

**Acceptance:** `https://johncohn.github.io/maxmix/` is publicly accessible and passes the smoke-test checklist above.

---

### Anti-patterns to Avoid

- **No MSE/SourceBuffer** — plain MP4 with two-video swap is approved; MSE requires fMP4 re-encoding and adds complexity with no perceptible benefit for 5-second stanzas
- **No npm/frameworks** — vanilla JS only; no React, Vue, build pipeline, or `node_modules`
- **Never set `loop` on video elements** — it suppresses the `ended` event that drives sequencing
- **Always include `muted` + `playsinline`** — omitting either causes silent autoplay failure on Chrome mobile and iOS Safari
- **No single-video src-swap** — produces 100–400 ms black-frame gap; use two-video swap with preloading
- **No `git add .` or `git add -A` blindly** — stage only intended files to avoid accidentally committing large binaries or secrets

---

## Deferred

- **MP4 files exceed 100 MB per file**: If any stanza file is at or above the 100 MB GitHub per-file limit, the user must choose one of: (a) re-encode at lower bitrate (`ffmpeg -crf 28 -i input.mp4 output.mp4`) to bring files under the limit, or (b) initialize Git LFS (`git lfs install && git lfs track "*.mp4"`) before committing — note that free GitHub accounts have 1 GB/month LFS bandwidth. The Builder will report exact sizes in Issue #3 before this decision is required.
