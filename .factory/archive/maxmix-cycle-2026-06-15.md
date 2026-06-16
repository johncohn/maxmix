---
tags:
  - factory
  - cycle-summary
  - maxmix
project: maxmix
date: 2026-06-15
source: factory-archivist
---

# MaxMix — Build Cycle Summary (2026-06-15)

## What Was Built

Single-page static site (`index.html`) that endlessly plays randomized "Happy Birthday" mashups by sequencing MP4 video stanzas. Hosted on GitHub Pages with no server-side code, no build step, and no npm dependencies.

**Live URL:** https://johncohn.github.io/maxmix/

### Deliverables
- 21 MP4 clips in `clips/` — c1_s1 through c5_s5, all under 15 MB each
- `index.html` — self-contained vanilla JS player (~200 lines inline)
- GitHub repo: `johncohn/maxmix` (public), Pages enabled on `main` branch

## Agent Timeline (UTC, 2026-06-16)

| Time | Agent | Verdict |
|------|-------|---------|
| 01:02 | Sprint started (build mode) | — |
| 01:02–01:05 | Researcher | PROCEED |
| 01:05–01:07 | Archivist (research) | — |
| 01:08–01:09 | Strategist | PLAN APPROVED |
| 01:10–01:12 | Archivist (strategy) | — |
| 01:12–01:15 | Builder | PROCEED / PASS |
| 01:16–01:17 | Archivist (build progress) | — |
| 01:20 | Eval scored | 0.5166 composite |

## Baseline Eval Score

| Metric | Value |
|--------|-------|
| Composite | **0.5166** |
| Dimensions | 14 |
| Passed | false |
| Evaluated | 2026-06-16T01:20:05Z |

The eval runner detected `no_factory` state before scoring (factory config re-initialized inline). Score reflects the initial static site; no experiments have been run yet.

## Key Decisions Made

1. **Two-video element swap** — eliminated 100–400 ms black-frame gap between stanzas; rejected single `src` swap and MSE/SourceBuffer approaches
2. **Vanilla JS, no framework** — GitHub Pages serves static files as-is; no build pipeline needed
3. **Clips committed to git** — all 21 MP4s were already at `/Users/jcohn/maxmix/clips/` and under 15 MB each; Phase 3 (upload) collapsed into Phase 1
4. **Never set `loop` on video elements** — suppresses the `ended` event that drives the sequencing engine; this was an explicit anti-pattern enforced throughout

## Architecture

```
index.html
├── <video id="vidA"> — active/visible element
├── <video id="vidB"> — preloading standby (display:none)
├── #overlay — full-screen tap-to-start (removed on first play)
└── #muteBtn — fixed bottom-right, syncs muted state across both elements

Sequencing:
  buildSong() → queue of (clipN, stanzaM) tuples
  - S1: random clip
  - S2–S4: random, no repeat of previous
  - S5: always c5_s5 (ending stanza)
  - Queue replenishes when < 3 clips remain

advance() on 'ended' event:
  - src-sets standby element with next clip
  - sets preload='auto' on standby
  - swaps visibility/play/pause
```

## Anti-Patterns Enforced
- No MSE/SourceBuffer
- No npm / no framework / no build step
- Never `loop` attribute on video elements
- Always `muted + playsinline` on both video elements
- No blind `git add -A`

## Experiments
None — this is the initial build cycle. Experiments begin in the next sprint.

## Related Archive Entries
- [[strategies/maxmix-2026-06-15]] — CEO-approved build plan
- [[sources/sequential-video-playback]] — two-video swap research
- [[sources/autoplay-constraints]] — browser autoplay policy research
- [[maxmix]] — project dashboard
