# ADR-0002 — the ASD-STE100 writing standard

*Status:* accepted · *Date:* 2026-10-21 · *Deciders:* the operator
directive, 2026-10-20 (no permalink — the wave issues carry the record) ·
*Org record:* [kailash-os ADR 0004](https://github.com/kailash-os/kailash-os/blob/master/docs/adr/0004-asd-ste100-standard.md)

## Context

The book's prose rules came from
[ADR-0001](0001-recipe-form-and-organisation.md): the recipe anatomy, the
header table, the ref footer, and the no-invented-evidence rule. The
sentence-level register stayed free: sentence length, tense, person, and
word choice differ from recipe to recipe. The org now adds a uniform
writing rule set, and the book's pages must accept against it.

## Decision

Every written text in the book follows ASD-STE100 Simplified Technical
English. The rule set:

1. One thought per sentence. A sentence carries one fact or one instruction.
2. A sentence stays at or under 20 words.
3. The voice is active. The tense is present. Instructions sit in the imperative.
4. A non-approved verb takes one fixed approved substitution.
5. One word carries one meaning, on every page.
6. Fixed technical names stay exact: tool ids, flag names, layer names, gate names.
7. Numbers use digits, with units adjacent.
8. Rendered text carries no idioms, no slang, and no first or second person.
9. No invented facts. A command quotes the landed CLI slice. A measured number cites its record.
10. Historical records keep their filed tense and wording.

The scope, and the boundary:

- The recipe pages, the cover page, the repo README, and the recipe template
  follow the rule set.
- ADR-0001 is an accepted record. It stays as filed; this ADR supersedes
  nothing in it — the standard governs prose, and ADR-0001's structural
  rules keep their form.
- The explicit PENDING markers stay. The standard governs the prose around
  them, never the marker itself.

Enforcement:

- The conversion lane is [kailash-book#25](https://github.com/kailash-os/kailash-book/issues/25).
- One theme section rides one conversion PR; each PR keeps the
  `site-check` render green.
- The recipe gates hold through every conversion: the header table, the
  H2 anatomy headings, the ref footer, and the landed-slice command rule.

## Consequences

- Forward-written recipe prose follows the rule set from the merge day on.
- The standing prose converts section by section through the conversion lane.
- The no-invented-evidence rule and the standard's rule 9 carry the same
  discipline; a recipe that passed the one accepts against the other.
