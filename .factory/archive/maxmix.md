---
tags:
  - factory
  - project
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# Factory: maxmix

## Status
- **State**: BUILT — live on GitHub Pages
- **Live URL**: https://johncohn.github.io/maxmix/
- **Baseline Score**: 0.5166 (composite, 14 dimensions, 2026-06-16T01:20Z)
- **Current Score**: 0.5166 (no experiments yet)
- **Experiments Run**: 0
- **Kept**: 0, **Reverted**: 0

## Build Result — 2026-06-15
**CEO Verdict: PROCEED (PASS)** — All 4 phases completed correctly. Zero issues found.

### What Was Built
- 21 MP4 clips committed to `clips/` (c1_s1 through c5_s5, all under 15 MB each)
- `index.html` — single-file vanilla JS player with two-video element swap
- GitHub Pages enabled on `main` branch, status: `built`

### CEO Verification Checklist (All Pass)
- Two video elements with `muted + playsinline` ✓
- `advance()` swaps visibility and references correctly ✓
- `preload='auto'` set on standby element ✓
- Error handler gracefully skips bad clips ✓
- `loop` attribute never set (would suppress `ended` event) ✓
- Mute state synced across both elements ✓
- Tap-to-start overlay shown on autoplay rejection ✓

### Build Timeline
- Researcher → PROCEED (01:05 UTC)
- Strategist → PROCEED / PLAN APPROVED (01:09 UTC)
- Builder → completed (01:15 UTC)
- CEO review → PROCEED / PASS (post-build)

## Project Summary
Single-page static site that endlessly plays randomized mashups of "Happy Birthday" by sequencing MP4 video stanzas from 5 clips (C1–C5, S1–S5). Hosted on GitHub Pages at `https://johncohn.github.io/maxmix/` with no server-side code.

## Approved Architecture
- Vanilla JS (ES2020), single `index.html`, no framework, no build step
- Two `<video>` element swap for gapless playback
- `muted + playsinline + autoplay` + tap-to-start overlay
- Sequencing: random clip per stanza position, no consecutive repeats, always end with `c5_s5`
- Queue replenishes when fewer than 3 clips remain

## Key Decisions Made
1. **Two-video swap over single src-swap** — eliminates 100–400 ms black-frame gap between stanzas
2. **Vanilla JS / no framework** — GitHub Pages serves as-is, no build step needed
3. **Phase 3 merged into Phase 1** — clips existed locally at `/Users/jcohn/maxmix/clips/`, all under 15 MB; 100 MB limit concern was moot
4. **Never `loop` attribute** — suppresses `ended` event that drives the sequencing engine

## Anti-Patterns Enforced
- No MSE/SourceBuffer — plain MP4 + two-video swap only
- No npm/frameworks
- Never `loop` on video elements (suppresses `ended` event)
- Always `muted + playsinline` on both video elements
- No blind `git add .` or `git add -A`

## Source Notes
- [[github-pages-hosting]]
- [[sequential-video-playback]]
- [[autoplay-constraints]]
- [[sequencing-algorithm]]
- [[tech-stack-decision]]

## Strategy Snapshots
- [[strategies/maxmix-2026-06-15]] — CEO-approved build plan

## Recent Experiments
_(none yet — site is newly built)_

## Cycle Summary
- [[maxmix-cycle-2026-06-15]] — full build cycle summary, decisions, timeline, and eval baseline
