# Indexes — The Wiki's Spine

Seven master index files at the wiki root that prevent drift across hundreds of literature notes. Each addresses a specific drift mode.

These are the *structural* layer of the wiki (Layer 5 in the note hierarchy). They contain no original prose — they're navigation, dedup protection, and history.

---

## Index Files

| File | Purpose | Format |
|---|---|---|
| `index.md` | Master navigation — project status by category | Table per category |
| `index_authors.md` | Every author alphabetical (Latin + dedicated sections for non-Latin scripts) | Sectioned alphabetical |
| `index_detail.md` | Every concept, theory, method alphabetical | Sectioned alphabetical |
| `books.md` | Book-length references chronological | Year-grouped list |
| `z_references_index.md` | Master reference filename list — dedup protection | One stem per line |
| `z_ingest_history.md` | Per-project ingest timestamps — incremental processing | Timestamped table |
| `log.md` | Operation log — every wiki operation | Time-stamped entries |

Worked skeletons of each file: [`SKELETON_EXAMPLES.md`](SKELETON_EXAMPLES.md).

---

## Why These Exist

### `index.md` — Project navigation

Without a master project list, you lose track of what's active across many concurrent projects. The index groups projects by topic category and shows current status.

### `index_authors.md` — Cross-reference navigation

"Show me everything by Smith" is one grep against `index_authors.md`. Without it, you'd grep across every reference file in the wiki. The index is a *cross-cutting* navigation orthogonal to category folders.

Non-Latin-script sections are critical for researchers working with sources in Korean / Chinese / Japanese / Cyrillic / Arabic / Devanagari / etc. — those names sort by their native script, not Latin transliteration. Omit these sections if your wiki has no non-Latin-script authors.

### `index_detail.md` — Concept/theory/method navigation

"Show me everything that uses hyper-selectivity" or "show me all DID applications". These cross-cutting queries are answered by `index_detail.md` plus the linked references.

### `books.md` — Book-specific surfacing

Books deserve separate listing because:
- Books are typically more central than papers in theoretical lineage
- Books accumulate over multi-year timelines (chronological ordering matters)
- A user might want "all books by Bourdieu" or "what books does my wiki have on culture"

Books are NOT registered in `journals/` (no journal). They're in `books.md` instead.

### `z_references_index.md` — Dedup protection

**This file is critical**. Before ingesting a paper, grep this index for the filename stem. If present, the paper is already ingested; do *not* re-write.

The wiki's most insidious failure mode is silent duplication — two different `Smith_2010_ASR.md` files with slightly different content. `z_references_index.md` prevents this.

Format is minimal: one stem per line, with optional metadata (theme, projects):

```
Author_Year_Journal.md | theme:Stratification | projects:[proj1, proj2]
```

### `z_ingest_history.md` — Incremental processing

Per-project ingest timestamps. When re-ingesting a project's references folder, only files modified *after* the last ingest are processed.

```
2026-05-10 14:32 | 2025_ExampleProject | initial ingest, 24 references
2026-06-15 09:18 | 2025_ExampleProject | +3 references (Smith 2026, Jones 2026, Brown 2025)
```

### `log.md` — Operation history

Every wiki operation (ingest / lint / move / delete / refactor / claim) gets a `log.md` entry. Format `## [YYYY-MM-DD] op | title` is greppable:

```bash
grep "^## \[" log.md | tail -20    # last 20 operations
grep "^## \[" log.md | grep "ingest" | wc -l    # total ingests
```

This is the wiki's audit trail. If a paper has surprising content, `log.md` says when it was added and what other operations happened around then.

---

## Maintenance Discipline

These index files are *updated on every relevant operation*, not periodically. The discipline:

- Ingest a paper → update `z_references_index.md`, `index_authors.md`, `index_detail.md`, `journals/{Abbr}.md`
- File a claim → update `claims/0_index.md`
- Start a project → update `index.md`
- Run a lint → log to `log.md`
- Move/delete → log + update all affected indexes

The lint script catches drift (orphan references, missing index entries), but the *real* defense is updating on each operation.

---

## Non-Latin-Script Sorting in `index_authors.md`

For non-Latin-script author names, create a dedicated section per script (one per writing system you have authors in). Sort by the native alphabet, not by Latin transliteration. Examples:

### Korean (가나다순)

```markdown
## 한국 저자 (가나다순)

### ㄱ
- **홍길동** · [Kim 2025 ASR](../references/Smith_2025_Example_ASR.md) · [홍길동·이공저자 2021](../references/홍길동_이공저자_2021_예시도서.md)
- **김재한** · ...

### ㄴ
...
```

Korean sort order:
- Consonants: ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ
- Vowels (after first consonant): ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
- Batchim: none → ㄱ ㄲ ㄳ ㄴ ... ㅎ

### Chinese (按拼音 or by stroke count)

```markdown
## 中文作者
- **张三** · ...
- **李四** · ...
```

### Japanese (五十音順)

```markdown
## 日本人著者
- **山田** · ...
```

### Other scripts

Same pattern: section heading in the native script (with a brief English label if helpful), sort by the script's native alphabet. Each author's entry chains their papers via `·` separator. Don't create separate entries for the same author — that's a duplication failure.

---

## Example File Templates

See [`SKELETON_EXAMPLES.md`](SKELETON_EXAMPLES.md) for filled-in skeletons of all seven index files in one place. Copy the relevant section and replace placeholders with your data.
