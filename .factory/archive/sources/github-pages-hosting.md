---
name: github-pages-hosting
description: GitHub Pages feasibility and file-size constraints for serving MP4 clips
metadata:
  type: reference
tags:
  - factory
  - source
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# GitHub Pages Hosting — MaxMix

## Findings

GitHub Pages is fully viable for the maxmix static site. Setup: enable Pages in repo Settings → `main` branch root → live at `https://johncohn.github.io/maxmix/`.

**Critical constraint — file size:**
- Hard limit: **100 MB per individual file** (git push; browser UI limit is 25 MB)
- Repo size: keep under 1 GB; GitHub flags repos over 5 GB
- Not designed for heavy media traffic — rate limiting may appear at scale

**Implication for short "Happy Birthday" stanzas (a few seconds each):** sizes should be well within limit. Verify with `du -sh clips/*.mp4` before committing. If any file exceeds 100 MB, re-encode with `ffmpeg -crf 28` or fall back to Git LFS (1 GB/month bandwidth cap on free tier).

## Sources
- [GitHub Pages official documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub community: Uploading large MP4 files onto Git Pages](https://github.com/orgs/community/discussions/22302)
