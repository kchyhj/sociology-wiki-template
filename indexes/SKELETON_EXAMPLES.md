# Index Skeletons — Worked Examples

All seven master index files at a glance. Copy the relevant skeleton to your wiki root, then grow each as you ingest. Each is shown as an illustrative skeleton with placeholder content; substitute your projects, authors, and theories.

For the **purpose** of each file (why it exists, what drift it prevents), see [`README.md`](README.md) in this folder.

---

## `index.md` — Master Navigation

```markdown
# Research Wiki Master Index

Last updated: YYYY-MM-DD

## Additional Indexes

- [**references/**](references/) — All literature notes (papers and books)
- [**claims/**](claims/0_index.md) — Atomic synthesized claims (your voice)
- [**index_authors.md**](index_authors.md) — Author index
- [**index_detail.md**](index_detail.md) — Concept/theory/method index
- [**books.md**](books.md) — Books chronological
- [**log.md**](log.md) — Operation log

---

## Projects by Category

### Stratification — Mobility, Inequality, Class

| Project | Status | Cross-categories |
|---|---|---|
| [2026_ProjectName](projects/2026/2026_ProjectName/index.md) | In progress | education |
| [2025_OtherProject](projects/2025/2025_OtherProject/index.md) | In progress | — |

### Race & Ethnicity — Inequality by Race, Ethnic Groups

| Project | Status | Cross-categories |
|---|---|---|
| [2025_ExampleProject](projects/2025/2025_ExampleProject/index.md) | In progress | stratification, education |

### Immigration — Assimilation, Integration

| Project | Status | Cross-categories |
|---|---|---|
| (no active projects) | — | — |

### Gender & Family — Fertility, Marriage

| Project | Status | Cross-categories |
|---|---|---|
| ... | ... | ... |

### Political Sociology — Far-right, Trust, Attitudes

| Project | Status | Cross-categories |
|---|---|---|
| ... | ... | ... |

### Education — Attainment, Schooling

| Project | Status | Cross-categories |
|---|---|---|
| ... | ... | ... |

### Labor Markets (cross-category only)

(No primary projects; used as cross-category by stratification/race/gender projects.)

---

## Published

Published papers:

- [2024 Project — *Journal Name*](projects/Published/2024_Project/index.md) — published YYYY

---

## Notes

- New projects: add under primary category, with cross-categories noted
- Status changes: update the line; move folder if convention dictates
- The master index is updated at project start, status change, and category re-assignment
```

---

## `index_authors.md` — Author Index

```markdown
# Author Index

Alphabetical cross-cutting index of every author in the wiki's references. Each entry chains all of the author's papers via `·` separator.

**Sorting rules**:
- Last-name first, lowercase-insensitive
- Hyphenated names (Tomaskovic-Devey) treated as single units
- Prepositions (van, de) — sort by main last name (e.g., "van Kerm" → V section, sort by "Kerm")
- Non-Latin scripts: native script in dedicated section, sorted by native alphabet

---

## A

- **Abascal, Maria** · [Abascal & Baldassarri 2015 AJS](../references/Abascal_Baldassarri_2015_AJS.md) · [Abascal 2020 ASR](../references/Abascal_2020_ASR.md)
- **Acemoglu, Daron** · [Acemoglu 2002 JEL](../references/Acemoglu_2002_JEL.md) · [Acemoglu et al. 2008 AER](../references/Acemoglu_etal_2008_AER.md)
- **Alba, Richard** · [Alba & Nee 1997 IMR](../references/Alba_Nee_1997_IMR.md)
- ...

## B

- **Bartik, Timothy** · [Bartik 1991 *Who Benefits from State and Local Economic Development*](../references/Bartik_1991_WhoBenefits.md)
- **Becker, Gary** · [Becker & Tomes 1986 JLE](../references/Becker_Tomes_1986_JLE.md)
- ...

## C

- **Card, David** · [Card 2001 ILRR](../references/Card_2001_ILRR.md) · [Card 2001 JLE](../references/Card_2001_JLE.md) · [Card & DiNardo 2002 JLE](../references/Card_DiNardo_2002_JLE.md)
- ...

(...continuing through Z...)

## Z

- **Zhou, Min** · [Lee & Zhou 2015 AAAP](../references/Lee_Zhou_2015_AAAP.md)
- ...

---

## Non-Latin-Script Authors (Optional Sections)

Authors whose names are written in scripts that don't sort naturally with the Latin alphabet go in dedicated sections by script. Korean shown below as a worked example; the same pattern applies to Chinese, Japanese, Cyrillic, Arabic, Devanagari, etc. Omit these sections entirely if your wiki has no non-Latin-script authors.

### 한국 저자 (가나다순) — Korean example

#### ㄱ

- **홍길동** · [Smith 2025 ASR](../references/Smith_2025_Example_ASR.md) · [Smith & Jones 2023 SSR](../references/Smith_Jones_2023_Example_SSR.md) · [홍길동·이공저자 2021 (예시도서)](../references/홍길동_이공저자_2021_예시도서.md)
- **김재한** · ...

#### ㅂ

- **이공저자** · [홍길동·이공저자 2021](../references/홍길동_이공저자_2021_예시도서.md)

#### ㅅ

- **박저자** · [박저자·홍길동 2021 (젠더사회이동예시)](../references/박저자_홍길동_2021_젠더사회이동예시.md)

### 中文作者 (按拼音) — Chinese example

- **张三** · ...
- **李四** · ...

### 日本人著者 (五十音順) — Japanese example

- **山田** · ...
- **佐藤** · ...

### Кириллица — Cyrillic example

- ...

---

## Maintenance

- Add new authors at alphabetical position during ingest (don't append to end)
- Chain new papers to existing author entries with `·` (don't create duplicate entries)
- Multi-author papers: the paper appears under each author's entry
- Hyphenated names: single sort unit (Tomaskovic-Devey under T, not D)
- Cross-check during lint Step 6 (alphabetical ordering)
```

---

## `index_detail.md` — Concept / Theory / Method Index

```markdown
# Concept / Theory / Method Index

Alphabetical cross-cutting index of every concept, theory, and method appearing in the wiki's reference frontmatter or concept pages.

**Sorting rules**: Same as `index_authors.md`. Latin alphabetical for English/Romanized terms; native alphabet for non-Latin scripts.

---

## A

- **achievement_paradox** → [concept page](../general/asian_american/achievement_paradox.md) · refs: [Hsin & Xie 2014](../references/Hsin_Xie_2014_PNAS.md) · [Lee et al. 2024 ARS](../references/Lee_etal_2024_ARS.md) · ...
- **assortative_mating** → [concept page](../general/gender_family/assortative_mating.md) · refs: [Schwartz & Mare 2005](../references/Schwartz_Mare_2005_Dem.md) · ...
- **assimilation** → [concept page](../general/immigration/assimilation.md) · refs: [Alba & Nee 1997 IMR](../references/Alba_Nee_1997_IMR.md) · ...
- ...

## B

- **boundaryless_career** → refs: [Arthur & Rousseau 1996](../references/Arthur_Rousseau_1996_BoundarylessCareer.md)
- ...

## C

- **cumulative_advantage** → [concept page](../general/stratification/cumulative_advantage.md) · refs: [DiPrete & Eirich 2006 ARS](../references/DiPrete_Eirich_2006_ARS.md) · ...
- **cultural_capital** → [concept page](../general/culture/cultural_capital.md) · refs: ...

## D

- **decomposition_methods** → [method page](../general/methods/decomposition_methods.md) · refs: ...
- **difference_in_differences** → [method page](../general/methods/difference_in_differences.md) · refs: ...

## H

- **human_capital** → refs (many papers) ...
- **hyper_selectivity** → [concept page](../general/asian_american/hyper_selectivity.md) · refs: ...

## M

- **measurement_error** → refs: ...
- **model_minority** → [concept page](../general/asian_american/model_minority.md) · refs: ...

## S

- **status_attainment** → [concept page](../general/stratification/status_attainment.md) · refs: ...
- **status_reproduction** → [concept page](../general/stratification/status_reproduction.md) · refs: ...

## (continuing through Z...)

---

## Methods (Cross-Listed)

For ease of access, methods are listed both above (alphabetical with concepts) and here (methods-only):

- **decomposition_methods** → [method page](../general/methods/decomposition_methods.md)
- **difference_in_differences** → [method page](../general/methods/difference_in_differences.md)
- **fixed_effects** → [method page](../general/methods/fixed_effects.md)
- **instrumental_variables** → [method page](../general/methods/instrumental_variables.md)
- **multilevel_modeling** → [method page](../general/methods/multilevel_modeling.md)
- **propensity_score** → [method page](../general/methods/propensity_score.md)

---

## 개념·이론 (한국어 가나다 순) — Korean example

For Korean-language theory terms (substitute any non-English language):

### ㄱ

- **계급 재생산** → refs: ...
- **계층 이동** → refs: ...

---

## Maintenance

- Add new theories at alphabetical position when ingesting a paper with new frontmatter `theories:` values
- Chain new references to existing entries (don't duplicate)
- Concept page link added when a dedicated page is created (3+ references threshold)
- Singleton theories (appearing in only one paper) are listed but without concept page link
- Lint Step 8 checks alphabetical ordering and detects taxonomy drift (e.g., `hyper_selectivity` vs `hyperselectivity`)
```

---

## `z_references_index.md` — Master Reference Filename List

```markdown
# Master Reference Filename Index

The wiki's dedup protection layer. **Always grep this file before ingesting a new paper.**

Format (one paper per line):
```
{stem}.md | theme:{primary_theme} | projects:[{proj1}, {proj2}]
```

If a paper's stem is already in this index, it's already ingested — do NOT re-write.

Used by:
- `scripts/lint.py` (cross-checks against `references/` directory listing)
- Manual grep during ingest workflow Step 0

---

## A

```
Abascal_2020_ASR.md | theme:Immigration | projects:[2025_ImmigrationExample]
Abascal_Baldassarri_2015_AJS.md | theme:Immigration | projects:[]
Abbott_2005_HES.md | theme:Stratification | projects:[2025_ExampleProject]
Abbott_2006_Mobility.md | theme:Stratification | projects:[2025_ExampleProject]
Acemoglu_2002_JEL.md | theme:LaborMarkets | projects:[]
Acemoglu_etal_2008_AER.md | theme:PoliticalSociology | projects:[]
Adao_etal_2019_QJE.md | theme:Methods | projects:[2024_UnionExample]
Aghion_etal_1999_JEL.md | theme:Stratification | projects:[]
AkerlofKranton_2005_JEP.md | theme:EconomicSociology | projects:[]
Alba_2009_BlurringColorLine.md | theme:RaceEthnicity | projects:[]
Alesina_Giuliano_2015_JEL.md | theme:Culture | projects:[2025_AnotherProject]
Alesina_Tabellini_2024_JEL.md | theme:Immigration | projects:[]
...
```

(Continuing through Z and non-Latin script names...)

## K

```
Smith_2025_Example_ASR.md | theme:RaceEthnicity | projects:[2025_AsnAmExample]
Author_Coauthor_2021_BookTitle.md | theme:Education | projects:[]
Smith_Jones_2023_Example_SSR.md | theme:RaceEthnicity | projects:[2025_AsnAmExample]
Smith_Jones_2024_Example_IMR.md | theme:RaceEthnicity | projects:[2025_AsnAmExample]
Author_Coauthor_2013_Journal.md | theme:Demography | projects:[2025_HistoricalExample]
Author_Coauthor_2016_Journal.md | theme:Demography | projects:[2025_HistoricalExample]
Author_Coauthor_2019_Journal.md | theme:Stratification | projects:[2025_HistoricalExample]
...
```

## 한국어 (Korean filenames) — example non-Latin section

```
김저자_2024_한국학술지.md | theme:PoliticalSociology | projects:[2026_PolSocExample]
홍길동_이공저자_2021_예시도서.md | theme:Education | projects:[]
박저자_홍길동_2021_젠더사회이동예시.md | theme:GenderFamily | projects:[]
```

(Add similar sections per script — 中文 / 日本語 / Кириллица / etc. — as needed.)

---

## Maintenance

- Add new entry on every reference ingest (Workflow Step 5)
- Update `projects:` list when a paper joins a new project
- Remove entries when a reference is deleted (rare; should match `references/` listing)
- Lint Step 4 cross-checks against `references/` directory

## Lint Diff Command

```bash
ls references/ | sort > /tmp/refs_dir.txt
grep -oE '^[^ |]+' z_references_index.md | sort > /tmp/refs_index.txt
comm -3 /tmp/refs_dir.txt /tmp/refs_index.txt    # entries that differ
```

Differences indicate either orphan files (in directory but not index) or stale index entries (in index but no file).
```

---

## `log.md` — Operation Log

```markdown
# Wiki Operation Log

Every wiki operation is logged here. Format: `## [YYYY-MM-DD] op | title` for grep-friendly history.

Operation types: `ingest` | `lint` | `move` | `delete` | `refactor` | `backup` | `schema` | `claim` | `project` | `concept`

---

## [2026-05-11] ingest | Smith_2026_ASR
- new theories added: status_reproduction (already existed in index)
- journals/ASR.md updated
- index_authors.md: Smith added at S section
- z_references_index.md: entry added with theme:Stratification, projects:[2025_ExampleProject]

## [2026-05-10] schema | reorganize categories
- created general/asian_american/ folder + 0_index.md
- moved 12 papers from race_ethnicity/ to asian_american/ (frontmatter themes updated)
- updated index.md project list

## [2026-05-10] claim | claims/edu_premium_cohort_divergence
- status: working
- cited references: Author_Coauthor_2021_BookTitle.md, Author_2023_PanelData_Journal.md
- related concepts: cumulative_advantage, horizontal_stratification

## [2026-05-08] lint | wiki-wide
- 2 orphan references identified — added to 2025_ExampleProject/references.md
- 14 prose mentions auto-linked via autolink.py (Lint Step 10)
- 1 data gap candidate flagged: Author_2024_ASR (cited 4× across projects, not ingested)

## [2026-05-05] move | 2024_RetiredProject
- from: projects/2024/2024_RetiredProject
- to: projects/Published/2024_RetiredProject
- status: In progress → Published

## [2026-05-03] ingest | Jones_2023_AJS
- new theories: relative_deprivation (also added to index_detail.md)
- new concept page: general/political_sociology/relative_deprivation.md (3rd reference using this theory)
- journals/AJS.md updated

## [2026-05-01] refactor | rename 5 files
- Author_Coauthor_2013.md → Author_Coauthor_2013_Journal.md (add journal abbr)
- Author_Coauthor_2016.md → Author_Coauthor_2016_Journal.md
- Author_Coauthor_2019.md → Author_Coauthor_2019_Journal.md
- All backlinks auto-updated across 11 referencing files

## [2026-04-28] project | 2025_ExampleProject
- primary category: stratification
- cross-categories: education
- bootstrap completed with 32 references

## [2026-04-25] backup | GitHub
- Wiki pushed to github.com/{your-handle}/research-wiki (commit abc1234)
- RAG re-indexing completed (1240 chunks)

## [2026-04-22] ingest | Brown_etal_2025_Dem
- new theories: spatial_inequality
- journals/Dem.md updated
- index_authors.md: Brown added to B section (3 papers chained)

---

## Useful Greps

```bash
# Last 20 operations
grep "^## \[" log.md | tail -20

# All ingests in 2026
grep "^## \[2026-" log.md | grep "ingest"

# Count operations by type
grep -oE "^## \[[0-9-]+\] (\w+)" log.md | awk '{print $3}' | sort | uniq -c
```
```

---

## How to Use This File

1. Identify which index file you need (see [`README.md`](README.md) for purposes).
2. Copy that section's skeleton into your wiki root with the filename matching the heading (e.g., `index_authors.md`, `log.md`).
3. Replace placeholders with your actual content.
4. Grow each index as you ingest references and start projects.

The skeletons are **illustrative** — they show the structure and example entries, not required content. Substitute project names, author names, theory slugs as fits your work.
