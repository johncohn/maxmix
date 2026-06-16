---
name: sequential-video-playback
description: Two-video element swap technique for gapless sequential MP4 playback in the browser
metadata:
  type: reference
tags:
  - factory
  - source
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# Sequential Video Playback — MaxMix

## Three Approaches Evaluated

### 1. Single `<video>` src-swap (baseline — rejected)
Listen for `ended`, change `.src`, call `.load()` then `.play()`. Causes 100–400 ms black-frame gap. Perceptible and jarring for song stanzas.

### 2. Two-video element swap (RECOMMENDED)
Two `<video>` elements overlaid. Active one plays (visible); passive one preloads next clip (hidden). On `ended`: swap visibility, play preloaded clip, load next-next into hidden element.

```javascript
// As soon as vidA starts, load next into vidB
// On vidA 'ended': show vidB, hide vidA, play vidB, load next-next into vidA
```

- Eliminates most gap — next clip already buffered
- Works with plain MP4, no re-encoding
- ~50 lines of vanilla JS
- Remaining risk: 1–2 frame (~16–33 ms) swap flash if MP4 has non-zero initial PTS → mitigate with `preload="auto"` and wait for `canplaythrough` before swapping

### 3. Media Source Extensions (MSE — skipped)
Truly gapless but requires fragmented MP4 (fMP4/CMAF) re-encoding and ~200+ lines of complex buffer management. Overkill for this project.

## Decision
Two-video swap is the approved approach. MSE and third-party players are explicitly out of scope.

## Sources
- [MDN: HTMLMediaElement: ended event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/ended_event)
- [MDN: Media Source Extensions API](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API)
