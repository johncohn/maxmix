#!/usr/bin/env python3
"""Eval script for MaxMix — static HTML/JS Happy Birthday mashup site."""

import json
import re
import subprocess
import sys
from pathlib import Path


def eval_syntax_check() -> dict:
    """Check JS syntax in index.html by extracting the script block and running node --check."""
    index = Path("index.html")
    if not index.exists():
        return {"name": "syntax_check", "score": 0.0, "weight": 0.5,
                "passed": False, "details": "index.html not found"}

    content = index.read_text()
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not script_match:
        return {"name": "syntax_check", "score": 0.5, "weight": 0.5,
                "passed": False, "details": "No <script> block found in index.html"}

    js_code = script_match.group(1)
    result = subprocess.run(
        ["node", "--input-type=module", "--check"],
        input=js_code, capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        return {"name": "syntax_check", "score": 1.0, "weight": 0.5,
                "passed": True, "details": "JS syntax OK"}

    errors = (result.stdout + result.stderr).strip()[:500]
    return {"name": "syntax_check", "score": 0.0, "weight": 0.5,
            "passed": False, "details": errors}


def eval_clip_manifest() -> dict:
    """Verify all expected cx_sy.mp4 clip files are present in clips/."""
    expected = []
    for clip in range(1, 6):
        stanzas = 5 if clip == 5 else 4
        for stanza in range(1, stanzas + 1):
            expected.append(f"clips/c{clip}_s{stanza}.mp4")

    missing = [f for f in expected if not Path(f).exists()]
    present = len(expected) - len(missing)
    score = present / len(expected)
    passed = len(missing) == 0
    details = f"{present}/{len(expected)} clips present"
    if missing:
        details += f"; missing: {', '.join(missing[:5])}"
    return {"name": "clip_manifest", "score": score, "weight": 0.3,
            "passed": passed, "details": details}


def eval_sequencing_logic() -> dict:
    """Verify the sequencing algorithm in index.html matches the spec."""
    index = Path("index.html")
    if not index.exists():
        return {"name": "sequencing_logic", "score": 0.0, "weight": 0.2,
                "passed": False, "details": "index.html not found"}

    content = index.read_text()
    checks = {
        "buildSong function": bool(re.search(r'function\s+buildSong', content)),
        "pickExcept helper": bool(re.search(r'function\s+pickExcept|pickExcept', content)),
        "c5_s5 hardcoded final": bool(re.search(r'c5_s5\.mp4', content)),
        "two video elements": len(re.findall(r'<video\b', content)) == 2,
        "muted attribute": bool(re.search(r'\bmuted\b', content)),
        "playsinline attribute": bool(re.search(r'\bplaysinline\b', content)),
        "ended event listener": bool(re.search(r"addEventListener.*ended|'ended'|\"ended\"", content)),
        "no loop attribute": 'loop' not in re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL),
    }
    passed_count = sum(checks.values())
    score = passed_count / len(checks)
    failed = [k for k, v in checks.items() if not v]
    details = f"{passed_count}/{len(checks)} checks pass"
    if failed:
        details += f"; failing: {', '.join(failed)}"
    return {"name": "sequencing_logic", "score": round(score, 3), "weight": 0.2,
            "passed": score >= 0.9, "details": details}


EVALS = [eval_syntax_check, eval_clip_manifest, eval_sequencing_logic]


def main() -> None:
    results = [fn() for fn in EVALS]
    output = {"results": results}
    json.dump(output, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
