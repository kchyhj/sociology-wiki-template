# Category Landing Page Template

Use for: the entry point of a `general/{category}/` folder. One per category, named `0_index.md` (the leading `0_` makes Obsidian/file managers sort it first).

**File location**: `general/{category}/0_index.md`. Examples:
- `general/stratification/0_index.md`
- `general/labor_markets/0_index.md`
- `general/race_ethnicity/0_index.md`

```markdown
# [Category Name] — [One-Line Description]

[Category one-line description.]

## Related Projects

| Project | Role | Cross-categories |
|---|---|---|
| [2025_ProjectName](../../projects/2025/2025_ProjectName/index.md) | primary | education |
| [2025_OtherProject](../../projects/2025/2025_OtherProject/index.md) | cross | education, labor_markets |

## Core Concepts

Concept definitions and theoretical commitments specific to this category. Either define concepts inline (for short ones) or link to dedicated concept pages:

- **[Concept Name](concept_slug.md)**: one-line definition.
- **[Another Concept](other_concept.md)**: one-line definition.
- **Less-developed concept (kept inline)**: full definition here (200 words or less; split to dedicated page if larger).

## History of Debates

Chronological narrative of the major debates in this category. *Not* a list of papers — a story of how the field's understanding moved.

> Example: "The 1950s saw [classical claim]; the 1980s introduced [supply-demand framing]; the 2010s saw the [economic-vs-cultural] debate dominate, with [synthesis emerging in 2015+]."

Each major moment cites a key paper. Typically 4-7 paragraphs covering 30-50 years.

Write this section *only when* the wiki has ingested 5+ references in this category. Until then, leave it as `*To be written after ingestion accumulates*`.

## Recent Themes (Last 5-10 Years)

What's currently active in the field? New methodological moves? Open questions? Unresolved debates?

Write this section *only after* the wiki has ingested papers from the past 5-10 years in this category.

## Key Literature (Ingested)

Tracked sociology journal papers shown unfolded (most prominent first by recency / centrality). Other journals collapsed in details blocks.

### By Project

#### [Project 1 Name]

- [Author (Year) *ASR*](../../references/{file}.md) — one-line relevance for this project + this category
- [Author (Year) *AJS*](../../references/{file}.md) — ...

#### [Project 2 Name]

- [Author (Year) *Dem*](../../references/{file}.md) — ...

<details>
<summary>Other-journal references (N papers)</summary>
<ul>
<li><a href="path">Author (Year) <em>ESR</em></a> — note</li>
<li><a href="path">Author (Year) <em>JEPP</em></a> — note</li>
</ul>
</details>

<details>
<summary>Non-English references (N papers)</summary>
<ul>
<li><a href="path">Author (Year) <em>Journal</em></a> — note</li>
</ul>
</details>

<!-- Optional: separate sub-blocks per non-Latin script if you have many.
     Korean example below — substitute any non-English language as needed. -->

<details>
<summary>한국 문헌 (N papers) — Korean example</summary>
<ul>
<li><a href="path">저자 (연도) <em>학술지</em></a> — 메모</li>
</ul>
</details>

## Data Sources

Major datasets used by papers in this category, with paths if institutionally maintained:

- **Dataset Name** (years covered) — short description + access info
- **Another Dataset** (years) — ...

## Sub-pages

If the category has spawned dedicated sub-pages (concept pages, sub-topic pages):

- [`hyper_selectivity.md`](hyper_selectivity.md) — concept page (12 papers in empirical record)
- [`subjective_status.md`](subjective_status.md) — sub-topic page (8 papers)

---

# [Category Name in your primary language]

(Optional **your-language mirror**, identical structure. Korean shown as one example;
substitute Spanish, Chinese, Japanese, German, etc. Use this only if your wiki follows
Language Policy Option C — your-language + English. Omit otherwise.)

Korean example:
# [범주명] — [한 줄 설명]
[본문]

[etc.]
```

---

## Discipline Rules

### Don't Write Until You Have Evidence

The two narrative sections — **History of Debates** and **Recent Themes** — should be empty (with `*pending ingest*` placeholder) until you have:
- 5+ ingested references in the category (history)
- 5+ ingested references from the past 5-10 years (recent themes)

Writing these sections from general knowledge is the violation pattern. They must reflect *what's in the wiki*, not what you know about the field.

### Tracked vs Non-Tracked Journals

Tracked journals (`ASR`, `AJS`, `SF`, `ARS`, `Dem`, `RSSM`, `WO`, `IMR`, `JMF`, `GS`, `Socius`, `ESR`, `BJS`, `SSR`, `SMR/SM`, Econ top-5, PolSci top-5, Psych top-5, and your field-specific Korean/Chinese/Japanese journals if applicable) get unfolded display. Non-tracked journals go in collapsed details blocks. Korean papers go in their own details block.

This isn't a quality judgment about non-tracked journals — it's a navigation choice. Unfolding all references makes the category page unreadable past ~30 ingests.

### Author Posts Don't Belong Here

The user's own published papers (you) belong in `journals/{Journal}.md` and `index.md` "Published" section, NOT in a separate "Author's Contributions" block within category pages. Treat them as ordinary references that happen to be authored by you.

### Inline Concept Definitions vs Dedicated Pages

A concept gets a dedicated page (`general/{category}/{concept}.md`) when:
- 3+ ingested references use it
- The category page's inline definition has grown past ~200 words
- The user's project hinges on it

Below those thresholds, keep it inline in the **Core Concepts** section.

---

## Filled-In Example (Stratification Category)

```markdown
# Stratification — Mobility, Inequality, Class, Status Attainment

The stratification category covers research on social mobility, income/wealth inequality, class structure, status attainment, and intergenerational reproduction.

## Related Projects

| Project | Role | Cross-categories |
|---|---|---|
| [2025_ExampleProject](../../projects/2025/2025_ExampleProject/index.md) | primary | education |
| [2025_PanelExample](../../projects/2025/2025_PanelExample/index.md) | primary | — |
| [2026_NationalSurveyExample](../../projects/2026/2026_NationalSurveyExample/index.md) | primary | education |

## Core Concepts

- **[Cumulative Advantage](cumulative_advantage.md)**: Matthew-effect mechanism for inequality growth across the life course.
- **[Status Attainment](status_attainment.md)**: Blau-Duncan framework of father-son occupational transmission.
- **[Horizontal Stratification](horizontal_stratification.md)**: Within-tier educational sorting as a stratification mechanism distinct from access.
- **Income Inequality**: see [`income_inequality.md`](income_inequality.md) — concept page with cross-national empirical record.

## History of Debates

The classical claim, dominant through the 1950s-1960s, was that industrial societies converge on a meritocratic occupational structure with high mobility (functionalism; Davis-Moore, Treiman). The 1980s introduced...

[continued narrative — 4-7 paragraphs]

## Recent Themes (Last 5-10 Years)

Active hubs include subjective status (Ridgeway et al.), intergenerational mobility decomposition (Chetty et al. lineage), and...

[continued]

## Key Literature (Ingested)

### 2025_ExampleProject

- [Armstrong & Hamilton (2013) *Paying for the Party*](../../references/Armstrong_Hamilton_2013_PayingParty.md) — within-class differentiation by university experience
- [Smith (2015) *Example Book Title*](../../references/Smith_2015_ExampleBook.md) — class-marriage dynamics

[etc.]
```
