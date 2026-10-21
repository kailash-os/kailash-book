# kailash-book

Kailash OS cookbook — task-oriented recipes published at
**book.kailash.tools** via GitHub Pages.

- Every recipe: Problem → Solution (real command shapes + expected
  output shapes) → Discussion → See also (O'Reilly cookbook format).
- Recipes are worked runs, never invented transcripts — output renders
  as shapes, and unfinished recipes stay explicit PENDING stubs.
- Organised by theme sections (Getting started / Scanning /
  Attack–defence pairs / Ops / Administrator); Level is per-recipe
  metadata; Top-10 collections (OWASP ML/LLM/API) render later as
  generated index views over recipe tags.
- Companion to [kailash-docs](https://github.com/kailash-os/kailash-docs)
  (docs.kailash.tools) — each recipe names and links the reference
  pages of the tools it uses.

Content is tracked on the issue tracker (cookbook parent: the repo's
first issue); the organisation rules are recorded in
`docs/adr/0001-recipe-form-and-organisation.md`. The manifest in
`kailash-packages` stays the single source of truth.

Deploy: `.github/workflows/pages.yml` renders the book and publishes
on merges to `main`. Custom domain persisted via the root `CNAME` and
repo Pages settings.

Licensed BSD-3-Clause (see `LICENSE`).

## Writing standard

Every written text in this repo follows ASD-STE100 Simplified Technical
English. The rules: one thought per sentence, 20 words per sentence or
fewer, active voice, present tense. The canonical decision record lives in
the kailash-os repo:
[`docs/adr/0004-asd-ste100-standard.md`](https://github.com/kailash-os/kailash-os/blob/master/docs/adr/0004-asd-ste100-standard.md)
([kailash-os#217](https://github.com/kailash-os/kailash-os/pull/217) carries
it). The conversion lane: [kailash-book#25](https://github.com/kailash-os/kailash-book/issues/25).
