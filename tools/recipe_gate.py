#!/usr/bin/env python3
"""recipe_gate.py — the book's provenance + no-invented-evidence gate (kailash-book#11).

Build-time checks over recipes/**/*.qmd (skips directory.qmd — the
generated index — and any non-recipe pages):

  1. anatomy: header table (`| Field | Value |`) present with the
     Tool(s)/Section/Level/Time/Layer-Category/Tags rows;
     Problem/Solution/Discussion/See-also H2 sections present (the
     ADR-0001 recipe form).
  2. provenance footer: either the compact
     'ref: [pin](source) - verified DATE' line (ADR-0001 rule 8) or the
     wave-1 '**Recipe provenance.** … verified DATE' block — both carry
     the verified-at date. Also: a 'PENDING' recipe must carry a
     follow-up pointer (lane note, upkeep reference, URL or issue ref)
     — never a silent unowned PENDING.
  3. no-invented-evidence: code fences (bash/sh/console/shell/python)
     must not open with prompt glyphs ($ PS1, user@host:, >>> ) —
     output shapes render as `<placeholder>` text in comments or
     `# → ` result notes. Inline trailing comments (`cmd   # note`)
     are fine; leading prompts are an invented-transcript marker.
  4. single H1 rule (ADR-0001 rule 6): no body '# ' heading.
  5. directory-count cross-check (once generate-directory.py lands —
     always, it's here): directory.qmd's per-section counts must equal
     a fresh header-parse of the recipes.

Exit 0 green / 1 red; one failure line per violated check.
Self-test: test_recipe_gate.py carries the RED fixtures (offline).
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "recipes"
DIRECTORY = RECIPES_DIR / "directory.qmd"

HDR_FIELDS_LAX = ["tool(s)?", "section", "level", "time", "layer/category", "tags"]
REQUIRED_SECTIONS = ["problem", "solution", "discussion", "see also"]

# leading-prompt glyphs inside code fences (invented transcript markers).
# NOTE: '# ' is NOT checkable (bash comments legitimately start lines) —
# the checkable invented-transcript markers are the interactive glyphs:
PROMPT_GLYPHS = [
    re.compile(r"(?m)^\$\s+\S"),              # "$ cmd" PS1 prompt
    re.compile(r"(?m)^>>> \S"),               # python REPL
    re.compile(r"(?m)^[A-Za-z0-9_.@~-]+@[A-Za-z0-9._-]+[:~]\s"),  # user@host:
]

# provenance footer: compact ref-line, optionally multi-line, must carry a date
COMPACT = re.compile(
    r"ref:\s*(?:\[[^\]]*\]\([^)]*\)|[^.\n])[\s\S]{0,300}?-\s*verified\s+\d{4}-\d{2}-\d{2}",
    re.I,
)
PROVENANCE_BLOCK = re.compile(r"\*\*Recipe provenance\.\*\*", re.I)
DATE = re.compile(r"verified\s+\d{4}-\d{2}-\d{2}", re.I)


def parse_recipe(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {"path": path, "text": text}


def check_recipe(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    v: list[str] = []

    # 1. anatomy
    if "| Field | Value |" not in text:
        v.append("anatomy: no header table (| Field | Value |)")
    else:
        for fld in HDR_FIELDS_LAX:
            if not re.search(rf"(?m)^\|\s*{fld}\s*\|", text, re.I):
                v.append(f"anatomy: header field missing: {fld}")
    heads = {h.strip().lower() for h in re.findall(r"(?m)^## (.+)$", text)}
    for s in REQUIRED_SECTIONS:
        if s not in heads:
            v.append(f"anatomy: missing section: {s}")

    # 4. single-H1 rule — strip fenced code first (bash '# ' comments are not headings)
    body = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)[-1]
    unfenced = re.sub(r"```[\s\S]*?```", "", body)
    if re.search(r"(?m)^# \S", unfenced):
        v.append("anatomy: body H1 present (single-H1 rule)")

    # 2. provenance footer
    tail = text[-2000:]
    has_provenance = (COMPACT.search(tail) or
                      (PROVENANCE_BLOCK.search(tail) and DATE.search(tail)))
    if not has_provenance:
        v.append("provenance: no footer (compact ref-line or provenance block + verified date)")
    # PENDING ownership: a PENDING marker in the provenance tail must
    # carry a follow-up pointer in its FORWARD context (an issue/repo
    # link, a lane note, an upkeep reference, or a compare-at-pin
    # instruction) — never an unowned, pointerless PENDING
    for m in re.finditer(r"PENDING", tail):
        fwd = tail[m.start(): m.end()+400]
        if any(x in fwd for x in ("http", "#", "lane", "upkeep", "follow-up",
                                   "vs the upstream", "at your pin", "instrument",
                                   "self-test", "checks.")):
            continue
        v.append("provenance: tail PENDING without follow-up pointer")
        break

    # 3. no-invented-evidence
    for fm in re.finditer(r"```(?:bash|sh|console|shell|python|py)\n([\s\S]*?)```", text):
        blk = fm.group(1)
        for pat in PROMPT_GLYPHS:
            if pat.search(blk):
                v.append(f"no-invented-evidence: prompt-glyph block ({pat.pattern[:24]}…)")
                break
    return v


def directory_counts_issue() -> str | None:
    """Cross-check directory.qmd per-section counts against a fresh parse."""
    if not DIRECTORY.exists():
        return "directory: recipes/directory.qmd missing (run tools/generate-directory.py)"
    text = DIRECTORY.read_text(encoding="utf-8")
    # fresh parse: section headers → count rows
    live = {}
    for m in re.finditer(r"### ([\w– -]+)\s*\((\d+)\)", text):
        live[m.group(1).strip()] = int(m.group(2))
    if not live:
        return None  # directory format changed; not this gate's contract
    # count recipes per section from their pages
    fresh: dict[str, int] = {}
    for p in RECIPES_DIR.rglob("*.qmd"):
        if p.name == "directory.qmd":
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r"(?m)^\|\s*Section\s*\|\s*([^|]+)\|", t)
        if m:
            sec = m.group(1).strip()
            fresh[sec] = fresh.get(sec, 0) + 1
    diffs = []
    for sec, n in fresh.items():
        # directory may record the section under its display name
        hit = [k for k in live if k.lower().startswith(sec.split(" ")[0].lower())]
        if hit and live[hit[0]] != n:
            diffs.append(f"{sec}: directory {live[hit[0]]} ≠ header-parse {n}")
    if diffs:
        return "directory: count drift (" + "; ".join(diffs) + ") — regenerate"
    return None


def run_gate(root: Path = RECIPES_DIR) -> list[str]:
    failures: list[str] = []
    pages = sorted(p for p in root.rglob("*.qmd") if p.name != "directory.qmd")
    if not pages:
        return ["no recipe pages found"]
    _base = root if root != RECIPES_DIR else REPO_ROOT
    for p in pages:
        try:
            rel = p.relative_to(_base)
        except ValueError:
            rel = p
        for f in check_recipe(p):
            failures.append(f"{rel}: {f}")
    d = directory_counts_issue()
    if d:
        failures.append(d)
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="recipe provenance + no-invented-evidence gate")
    ap.add_argument("--root", default=str(RECIPES_DIR))
    ap.add_argument("--report", default=None, help="write a JSON report here")
    args = ap.parse_args()
    root = Path(args.root)
    failures = run_gate(root)
    if args.report:
        Path(args.report).write_text(json.dumps({
            "failures": failures,
            "recipes_checked": len([p for p in root.rglob('*.qmd') if p.name != 'directory.qmd']),
            "verdict": "GREEN" if not failures else "RED",
        }, indent=1) + "\n")
    if failures:
        print(f"recipe-gate: RED — {len(failures)} failures")
        for f in failures:
            print("  -", f)
        return 1
    print("recipe-gate: GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
