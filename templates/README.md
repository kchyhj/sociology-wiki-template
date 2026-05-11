# Templates

Markdown templates for every note type in the wiki. Copy the relevant template, fill in the placeholders, save to the corresponding folder.

## Template Index

| Template | Use For | Saves To |
|---|---|---|
| [`reference_paper.md`](reference_paper.md) | Peer-reviewed journal article summary | `references/{stem}.md` |
| [`reference_book.md`](reference_book.md) | Scholarly book or book chapter | `references/{stem}.md` |
| [`concept.md`](concept.md) | Theory/concept/method synthesis page | `general/{category}/{concept}.md` |
| [`claim.md`](claim.md) | Atomic synthesized claim (your voice) | `claims/{slug}.md` |
| [`project_hub.md`](project_hub.md) | Active research project overview | `projects/{YYYY}/{Name}/index.md` |
| [`project_references.md`](project_references.md) | Project bibliography | `projects/{YYYY}/{Name}/references.md` |
| [`category_0_index.md`](category_0_index.md) | Category landing page | `general/{category}/0_index.md` |
| [`frontmatter_schemas.md`](frontmatter_schemas.md) | YAML frontmatter standards | (reference doc, not a template to copy) |

## Discipline by Template

Each template enforces the rules appropriate to its note layer:

| Template | Voice | Source rule | Special discipline |
|---|---|---|---|
| `reference_paper` | Authors' | Source-only — nothing the paper doesn't say | Verification Metadata required |
| `reference_book` | Authors' | Source-only by chapter | Don't summarize from book reviews |
| `concept` | Neutral scholarly | Empirical record cites verified refs | History/Recent sections only after 5+ refs |
| `claim` | Yours | Verified citations to refs | Atomicity — one claim per file |
| `project_hub` | Yours | Verified citations | Status tracking is open (use your own convention) |
| `project_references` | n/a (bibliography) | Same verification as references | Promote text-only → linked when ingest |
| `category_0_index` | Neutral scholarly | Narrative sections empty until 5+ refs | Tracked vs non-tracked journal display |

## Quick Reference — Required Fields

Every reference page must have:
- YAML frontmatter (see `frontmatter_schemas.md`)
- H1 title in `Author (Year) Title` format
- Inline `#type/*` `#theme/*` `#journal/*` tag line
- Bibliography line
- All standard sub-sections (Topic / Theory / Data & Methods / Findings / Relevance / Scholarly Conversation / Verification Metadata)

Empty sub-sections are allowed (with placeholder), but the **section header must exist**. This is for navigability and Obsidian outline rendering.

## Customizing Templates

The templates ship with sociology-specific defaults. Customize for your subfield:

1. **Reserved themes list** in `frontmatter_schemas.md` — add/remove themes for your area
2. **Standard journals** in `category_0_index.md` — adjust tracked-journal list for your subdiscipline
3. **Project hub status field** in `project_hub.md` — define your own status vocabulary (e.g., "In progress / Under review / Published") and tracking conventions
4. **Non-English handling** — templates include Korean as a worked example of non-English / non-Latin-script content. If your wiki is in another non-English language (Spanish, Chinese, Japanese, German, Arabic, etc.), substitute that language where Korean appears. If your wiki is English-only, remove the mirror sections entirely. See `CLAUDE.md` → Language Policy for the three supported configurations.

The structural disciplines (5-layer hierarchy, 3-layer verification, source-only rule, atomic claims) should *not* be customized — they're the system's contract.

## Quick Test

After installing the templates, verify your wiki works by:

1. Ingest one paper. Fill `reference_paper.md` end-to-end including Verification Metadata.
2. Run `scripts/lint.py`. Should report 0 issues for this file.
3. Run `scripts/autolink.py --dry`. Should report 0 changes (no other refs yet).
4. Create a `claims/example_claim.md` with status `working`. Re-run lint.
5. Run `scripts/index_papers.py --full`. Should index the 2 files.

If all steps pass, the wiki is operational.
