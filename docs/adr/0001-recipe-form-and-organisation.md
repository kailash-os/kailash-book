# ADR-0001 — recipe form & organisation contract

*Status:* accepted · *Date:* 2026-10-14 · *Deciders:* kailash-book
maintainers · *Acceptance sample:* the garak recipe posted on
[kailash-website#31 (comment)](https://github.com/kailash-os/kailash-website/issues/31#issuecomment-6122452780)

## Context

`book.kailash.tools` publishes task-oriented recipes for Kailash OS in
the O'Reilly cookbook format: Problem → Solution → Discussion → See
also. Two acceptance samples exist project-wide: the garak recipe on
kailash-website#31 (recipe anatomy + no-invented-evidence rule) and
the garak man-page on kailash-website#30 (guide-side template, now
live on docs.kailash.tools) — the book's recipes must accept against
both. The cookbook parent issue (kailash-website#31) initially
posited categories, grading, and future Top-10 collections; the
organisation had to be decided before the page skeleton hardens.

## Decision

**Sections are themes; level is metadata; collections are generated
views.**

1. **Theme sections** — Getting started / Scanning / Attack–defence
   pairs / Ops / Administrator. The nav IS the themes.
2. **Level (easy / medium / hard) is per-recipe metadata** (header
   strip field, like the garak sample's `Level:` field), not a
   navigation layer: it displays on the page, counts in the recipe
   directory, and never re-organises the book.
3. **Top-10 collections (OWASP ML/LLM/API Top-10, and any later set)
   render as build-time generated index pages over recipe tags** —
   recipes never move between sections; a collection is a view, not a
   re-parenting. Collections exist only for published tag sets and
   only when their recipes exist — never an empty view.
 4. **Recipe template** (`templates/recipe.qmd.in`): title + header
   strip (Tool / Section / Level / Time / Layer-Category / Tags), then
   Problem / Solution (+ expected output **shape** placeholders, never
   invented transcripts) / Discussion / See also (+ reference-page
   link per tool), closed by a provenance footer (verified-against pin
   + date + smoke status; anything not worked against a real pin stays
   explicit `PENDING` — the guide ADR-0001's degrade-honestly rule,
   carried over).
 5. **Cross-link rule.** Every recipe links the docs.kailash.tools
   reference page of each tool it uses
   (`https://docs.kailash.tools/reference/<tool>.html` surface) and, wherever a pair recipe needs the
   sister tool's page; recipes link neighbour recipes too. Guide
   reference pages may list recipes that use their tool — direction
   guide→book is a guide-side concern, coordinated at the guide.

**Sections-for-life rule.** A recipe is never re-parented between
theme sections once published; corrections, extensions and level
changes are fine, moving a recipe is not. Top-10 collections get their
content via tags, not moves.

## Consequences

- The reader always has one question answered: "how do I do X" —
  section = theme, header strip = specifics.
- The nav stays stable while new recipes, levels and collections
  accrue; re-organisation cost is zero by construction.
- Recipes carry a maintenance obligation identical to man pages: pin
  moves → re-work or explicitly mark stale.
- Generated Top-10 views require a registry of published collections:
  nothing renders an empty or speculative collection.
