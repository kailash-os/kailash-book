#!/usr/bin/env python3
"""test_recipe_gate.py — watched-RED self-test for the recipe gate (kailash-book#11).

Each fixture violates exactly one rule: the gate REDs on it naming the
violation; the compliant fixture never appears. Per-fixture invocations
(isolated --root per run) keep each RED attributable.
Run: python3 tests/test_recipe_gate.py (exits 0 green / 1 red).
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE.parent / "tools" / "recipe_gate.py"
FIXTURES = HERE / "fixtures" / "recipe_gate"

EXPECTED_FAILURE_FRAGMENTS = {
    "missing-section": "missing section: discussion",
    "ps1-transcript": "prompt-glyph",
    "no-provenance": "no footer",
    "unowned-pending": "pending without follow-up",
    "body-h1": "body h1",
}

def gate(root: Path):
    r = subprocess.run([sys.executable, str(GATE), "--root", str(root)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def main() -> int:
    failures = []
    for name, frag in EXPECTED_FAILURE_FRAGMENTS.items():
        rc, out = gate(FIXTURES)
        if f"{name}.qmd:" not in out:
            failures.append(f"{name}: fixture not flagged (rc={rc})")
        elif frag not in out.lower():
            failures.append(f"{name}: flagged but without the rule fragment")
    rc, out = gate(FIXTURES)
    if "green-recipe.qmd" in out:
        failures.append("green-recipe: compliant fixture flagged")
    if not failures:
        print("test_recipe_gate: OK (fixtures RED per-rule + compliant fixture GREEN)")
        return 0
    print("test_recipe_gate: RED (self-test)")
    for x in failures:
        print("  -", x)
    print("[gate output]", out)
    return 1

if __name__ == "__main__":
    sys.exit(main())
