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
 6. **Page structure (single-H1 rule).** The YAML `title:` renders
   as the page's only H1; the body carries NO top-level heading line
   — the anatomy (Problem / Solution / Discussion / See also) is
   H2 (`##`) throughout, with anchors as Quarto auto-generates them.
   rationale: a `title:` + a body `#` heading produced two H1s per
   page and broke the book's numbering/TOC ordering (caught in the
   same-day content pass, 2026-10-14); the cover page (index.qmd)
   carries no body H1 either.
 7. **Header table (not a strip).** The page's first block under the
   title is a two-column table (Tool | Section | Level | Time |
   Layer/Category | Tags), values hyperlinked where a surface exists
   (reference pages, category pages) — replaces the earlier pipe-strip
   line (wave-2 decision, 2026-10-14); template
   `templates/recipe.qmd.in` is the shape.
 8. **Provenance footnote = the guide's compact form (wave-2
   decision, 2026-10-14).** After the `---` rule: one line —
   `ref: [<pin>](pin-source URL) - verified <date>` — the pin text
   hyperlinked to its pin source (nvfetcher `_sources/generated.nix`
   or the flake lock), exactly like the generated reference pages on
   docs.kailash.tools; a one-line extra (smoke/missing-surface note +
   link) only when honest. Long provenance paragraphs were dropped as
   wordy (user 2026-10-14: "make it small and a hyperlink saying
   'ref: PR or something with lock'").

 9. **Code-block spacing.** `docs/custom.css` (wired in `_quarto.yml`
    format.html.css) gives `pre` blocks 1.6em vertical margins +
    1.1em padding + 1.6 line-height — wave-2 readability decision
    (2026-10-14).

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
