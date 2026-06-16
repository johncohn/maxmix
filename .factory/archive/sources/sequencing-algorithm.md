---
name: sequencing-algorithm
description: Clip sequencing algorithm for randomized Happy Birthday mashup — rules, pseudo-code, edge cases
metadata:
  type: reference
tags:
  - factory
  - source
  - maxmix
source: factory-archivist
date: 2026-06-15
---

# Sequencing Algorithm — MaxMix

## File Structure
```
clips/c{1-5}_s{1-5}.mp4
```
- C1–C4: stanzas S1–S4
- C5: stanzas S1–S5 (only clip with S5)
- Total: 21 files

## Song Rules
1. S1: random clip from {1,2,3,4,5}
2. S2: random clip ≠ S1's clip
3. S3: random clip ≠ S2's clip
4. S4: random clip ≠ S3's clip
5. S5: always `c5_s5` (hardcoded)
6. Repeat indefinitely

## Implementation
```javascript
const NUM_CLIPS = 5;

function pickExcept(exclude) {
  const choices = [1,2,3,4,5].filter(n => n !== exclude);
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
```

## Edge Cases
- **S4 from clip 5 before c5_s5**: allowed — different files, no conflict
- **No S5 for C1–C4**: correct — only C5 has S5; algorithm hardcodes `c5_s5`
- **`loop` attribute**: never set — prevents `ended` event from firing
- **Error handling**: add `error` handler to gracefully skip a bad clip
