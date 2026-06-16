---
name: autoplay-constraints
description: Browser autoplay policy constraints and workarounds for HTML5 video with audio
metadata:
  type: reference
tags:
  - factory
  - source
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# Autoplay Constraints — MaxMix

## The Problem
Modern browsers block autoplaying media with audio unless the user has first interacted with the page.

## Universal Workaround
```html
<video autoplay muted playsinline></video>
```

- `muted` — required for autoplay without user interaction (Chrome, Firefox, Safari)
- `playsinline` — required on iOS Safari: prevents full-screen takeover and enables autoplay
- `autoplay` — tells browser to start when ready

Result: video plays silently on load. User taps an unmute button to hear audio.

## Programmatic play() must handle rejection
```javascript
const playPromise = video.play();
if (playPromise !== undefined) {
  playPromise.catch(() => {
    // Show "tap to play" overlay; remove on user click, then play()
  });
}
```

## iOS-specific
Even `muted + playsinline` may not autoplay without a prior user gesture in some iOS Safari configurations. **Safest fallback:** full-screen "tap to start" overlay that triggers `video.play()` on first touch.

**Also critical:** Never set the `loop` attribute on these elements — it prevents the `ended` event from firing.

## Sources
- [MDN: Autoplay guide for media and Web Audio APIs](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
- [Chrome Developers: Autoplay policy in Chrome](https://developer.chrome.com/blog/autoplay)
- [Mux: Video autoplay considered harmful](https://www.mux.com/blog/video-autoplay-considered-harmful)
- [SiteLint: Fixing HTML video autoplay in Safari and iOS](https://www.sitelint.com/blog/fixing-html-video-autoplay-blank-poster-first-frame-and-improving-performance-in-safari-and-ios-devices)
