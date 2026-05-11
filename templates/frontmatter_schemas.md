# Frontmatter Schemas

YAML frontmatter conventions for each note type. Consistency across files enables Obsidian Dataview queries, RAG metadata filtering, and lint checks.

---

## Reference (Paper)

```yaml
---
type: paper
year: YYYY                              # integer
authors: [LastName1, LastName2]         # inline list, no quotes for ASCII names
journal: ASR                            # journal abbreviation (see CATEGORIES.md)
themes: [Stratification, Education]     # CamelCase, see standardized list
projects: [your_active_project]         # list of project slugs; [] if not project-bound
theories: [theory_slug_1, theory_slug_2] # snake_case theory slugs
needs_verification: false               # boolean — true if Layer 1 incomplete
---
```

Field semantics:
- `type`: always `paper` for journal articles. (Reserved values: `paper`, `book`, `book-chapter`, `concept`, `method`, `claim`)
- `authors`: surname only, in order of appearance. Korean: `[김저자]`. Multi-author: `[Smith, Jones, Brown]`.
- `journal`: standardized abbreviation. See `docs/CATEGORIES.md` for canonical list.
- `themes`: CamelCase. Reserved: `Stratification, LaborMarkets, RaceEthnicity, Immigration, GenderFamily, PoliticalSociology, Education, Methods, EconomicSociology, Demography, Culture, Theory, History, AsianAmericans, Korea`. Add new themes only after 3+ ingested papers warrant it.
- `projects`: list of project name slugs. Empty `[]` for theme-collected (not project-bound) papers.
- `theories`: snake_case theory slugs. Consistency matters — `hyper_selectivity` not `Hyper-Selectivity` or `hyperselectivity`.

---

## Reference (Book)

```yaml
---
type: book                              # or book-chapter
year: YYYY
authors: [LastName1, LastName2]
publisher: Russell Sage Foundation      # spell out the publisher
editors: [EditorLastname]               # only for book-chapter
themes: [RaceEthnicity, AsianAmericans]
projects: [your_active_project]
theories: [hyper_selectivity]
---
```

Differences from paper:
- `publisher` instead of `journal`
- `editors` field for chapters in edited volumes
- `type: book` for monographs, `type: book-chapter` for chapters

---

## Concept Page

```yaml
---
type: concept
projects: [proj1, proj2]                # projects that use this concept
theories: [theory_slug]                 # the theory this concept centers on
---
```

Notes:
- Concept pages don't need `year`, `authors`, or `themes` (the category folder *is* the theme).
- `projects` lists all active projects using this concept (informs lint of "concept page abandonment" if all projects retire).

---

## Method Page

```yaml
---
type: method
projects: [proj1, proj2]
methods: [method_slug]                  # primary slug for this method
software: [stata, r, python]            # platforms where common implementations exist
---
```

Notes:
- Method pages have a `software` field for cross-referencing implementation guides.

---

## Atomic Claim

```yaml
---
type: claim
author: your_handle                     # the wiki owner
date_created: YYYY-MM-DD                # required
date_updated: YYYY-MM-DD                # required, update on substantive edits
themes: [Stratification, Education]     # CamelCase, from reserved set
references: [Paper1_Year_J, Paper2_Year_J] # wiki reference file stems supporting the claim
related_concepts: [concept_slug_1]      # concept pages the claim touches
related_claims: []                      # other claim slugs (extensions, contrasts)
projects: [your_active_project]         # projects where the claim is used
status: working                         # working | confident | retired
---
```

Status semantics:
- `working`: tentative, exploratory. Default for new claims.
- `confident`: verified, used in published work.
- `retired`: superseded. Keep file with retirement reason.

---

## Project Hub Index

Project hub `index.md` doesn't use YAML frontmatter (it's a structural document, not a notes document). The information that would go in frontmatter is in the body's bibliographic block.

Project `references.md` likewise has no frontmatter.

---

## Index Files

Root-level master index files (`index.md`, `index_authors.md`, `index_detail.md`, `books.md`, `z_references_index.md`, `z_ingest_history.md`, `log.md`) have no YAML frontmatter. They're structural.

---

## Standardized Vocabulary

### Reserved `themes` (CamelCase)

```
Stratification, LaborMarkets, RaceEthnicity, Immigration, GenderFamily,
PoliticalSociology, Education, Methods, EconomicSociology, Demography,
Culture, Theory, History, AsianAmericans, Korea
```

(Add new themes only when 3+ ingested papers warrant the category. Don't fragment.)

### Reserved `type` values

```
paper, book, book-chapter, concept, method, claim
```

(Note: hyphenated `book-chapter`, not underscored. Consistency matters for lint.)

### Inline tag conventions

In the body of the file (not frontmatter), use Obsidian-style hashtags for navigation:

- `#type/paper`, `#type/book`, `#type/concept`, `#type/method`, `#type/claim`
- `#theme/Stratification`, `#theme/RaceEthnicity` (CamelCase, match frontmatter)
- `#journal/ASR`, `#journal/AJS`, etc. (uppercase, match journal abbreviation)
- `#theory/{theory_slug}` (snake_case, match frontmatter)
- `#project/{project_slug}` (match project folder name)
- `#status/working`, `#status/confident`, `#status/retired` (claims only)
- `#author/your_handle` (claims only — wiki owner's handle)

Inline tag placement: immediately under the H1 title, on its own line.

---

## Lint Discipline

The wiki lint script (Step 6) checks:
- `themes` values come from reserved set
- `type` values come from reserved set
- `status` values come from reserved set (for claims)
- Inline `#theme/*` and `#journal/*` tags match frontmatter values
- No mixed casing (e.g., `#theme/Stratification` and `#theme/stratification` in same wiki — should be consistent)

When the lint flags drift, the fix is mechanical (CamelCase + reserved vocabulary). Don't argue with the lint — fix and move on.

---

## Backward Compatibility

If your wiki has historical inconsistencies (mixed casing, fragmented theme list, etc.), run a normalization sweep once before adopting these schemas. The lint script can do most of this automatically — see `scripts/lint.py`. After the sweep, the schemas become the contract going forward.
