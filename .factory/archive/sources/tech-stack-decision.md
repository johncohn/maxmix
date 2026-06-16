---
name: tech-stack-decision
description: Tech stack decision for maxmix — vanilla JS over any framework, single index.html
metadata:
  type: reference
tags:
  - factory
  - source
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# Tech Stack Decision — MaxMix

## Chosen Stack

| Concern | Choice | Rationale |
|---|---|---|
| Language | Vanilla JS (ES2020) | No build step, no npm, no framework — serves as-is from GitHub Pages |
| HTML | Single `index.html` | Everything in one file; no routing needed |
| CSS | Inline `<style>` block | Minimal — fullscreen black background, centered video |
| Video API | HTML5 `<video>` × 2 | Two-element swap; no library needed |
| Hosting | GitHub Pages, `main` branch root | Free, zero config |
| Build | None | Push and it's live |

## Framework Verdict
**Do NOT use React, Vue, or any SPA framework.** Logic is ~60–80 lines of JS. A framework adds build pipeline, `node_modules`, and zero benefit.

## Libraries Evaluated and Rejected
- **BBC `media-sequence`**: adds a dependency — overkill for 5 clips
- **video.js playlist plugin**: 50 KB+ library — unnecessary
- **MSE (Bitmovin demo)**: requires fMP4 re-encoding — too complex for MVP

## MVP Deliverables
1. `index.html` — inline CSS + JS, two `<video>` elements, tap-to-start overlay, optional unmute button
2. `clips/` directory with `c{1-5}_s{1-5}.mp4`
3. GitHub Pages enabled on `main` branch

## Out of Scope for MVP
- Audio controls beyond simple unmute toggle
- Visual UI beyond dark background
- Analytics/tracking
- Service workers / offline caching
- Adaptive bitrate
