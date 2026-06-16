# Factory Configuration

## Goal
Continuously improve the MaxMix website — a randomized Happy Birthday mashup player that sequences MP4 video stanzas across 5 clips and loops forever, hosted on GitHub Pages.

## Scope

### Modifiable
- index.html
- eval/**/*.py
- README.md

### Read-only
- clips/**
- .gitignore

## Guards
- Do not delete or overwrite existing tests
- Do not modify files outside the declared scope
- Do not introduce secrets or credentials into the repository
- Do not modify files in clips/ — video assets are immutable
- Never set the loop attribute on video elements (breaks ended event sequencing)
- Always keep muted and playsinline attributes on video elements

## Eval

### Command
```bash
python3 eval/score.py
```

### Threshold
0.85

## Target Branch
main

## Smoke Test
```bash
curl -sf https://johncohn.github.io/maxmix/ -o /dev/null -w "%{http_code}" | grep -q 200
```

## Constraints
- Prefer small, incremental changes over large rewrites
- The site must remain a single index.html with no build step and no npm dependencies
- Each change must pass all 3 eval dimensions (syntax_check, clip_manifest, sequencing_logic)
- The sequencing rules are sacred: S1-S4 each from a different clip than the prior, S5 always c5_s5
