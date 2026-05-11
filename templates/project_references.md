# Project References Template

Use for: bibliography of an active research project. One per project. Companion to `index.md`.

**File location**: `projects/{YYYY}/{ProjectName}/references.md`

```markdown
# Project Title — References

Alphabetical project bibliography. Includes all papers cited in the project's lit review or anchoring its analysis.

## With Summary Page (Ingested)

These papers have a `references/{stem}.md` summary in the wiki.

- [**Author1, FirstName, and FirstName Coauthor (Year)** "Title" — *Journal* Vol(Issue):pp-pp](../../../references/{stem}.md) — one-line note on project-specific relevance
- [**Author (Year)** *Book Title* — Publisher](../../../references/{stem}.md) — one-line note
- [**Author1 et al. (Year)** "Title" — *Journal* Vol(Issue):pp](../../../references/{stem}.md) — one-line note

(Continue alphabetically. Books and papers in same alphabetical sort by first author.)

## Without Summary Page (Text Citation Only)

Papers cited in the project but not (yet) ingested as wiki summaries. Plain text, no link.

- **Author, FirstName (Year)** "Title" — *Journal* Vol(Issue):pp-pp — one-line note
- **Author1 and Author2 (Year)** "Title" — *Journal* — one-line note

(These are candidates for future ingestion. The wiki lint can detect repeat citations across projects in this section and recommend ingestion.)

## Non-English References (Optional Section)

(Separate section per non-Latin script, sorted by the script's native alphabet. Korean shown below as a worked example; substitute Spanish, Chinese, Japanese, etc. as needed. Omit entirely if your project uses only English-language sources.)

### Korean references — example

#### With Summary Page

- [**저자 (Year)** "제목" — *학술지* Vol(Issue):pp](../../../references/{stem}.md) — 한 줄 메모
- [**저자1, 저자2 (Year)** *서명* — 출판사](../../../references/{stem}.md) — 한 줄 메모

#### Without Summary Page (Text Citation Only)

- **저자 (Year)** "제목" — *학술지* Vol(Issue):pp-pp — 한 줄 메모

### Chinese / Japanese / other non-Latin references

Same structure as Korean, with section heading in the native script (e.g., `## 中文文献`, `## 日本語文献`, `## Литература на русском`). Sort by native alphabet.
```

---

## Discipline Rules

### Alphabetical Order Strictly

By first author's surname. Books and papers integrated (don't separate by type within a section). Non-Latin-script references go in their own per-script section, sorted by the script's native alphabet (e.g., Korean references sorted 가나다순, Chinese by pinyin or stroke count, Japanese by 五十音, etc.).

For multi-author papers, alphabetize by *first* author. "Smith, Jones, and Brown" goes under S.

### One-Line Notes

The note after each entry explains *why this paper is in this project's bibliography*. Be specific:

- ❌ "Important paper on the topic"
- ✅ "Provides baseline AAAP pattern in 1940 cohort — anchors H1"
- ❌ "Used for methods"
- ✅ "Adapted their DID specification (their eq. 4) for our Korea analysis"

The note is for *future you* to know why this citation is here without re-reading the paper.

### Don't Duplicate Across Sections

If a paper has a summary page (`references/{stem}.md`), it goes in the **With Summary Page** section only. Not also in the **Without Summary Page** section.

Wiki lint check 8(d) catches this duplication.

### When to Promote from "Without" to "With"

Triggers:
- The paper is cited 3+ times across multiple projects' references.md — high return on ingestion
- You're about to cite the paper in your manuscript — need verified summary
- You're stress-testing a hypothesis that depends on this paper's evidence
- The paper appears in 2+ concept page empirical records

Once you ingest, **move the entry** from "Without Summary Page" to "With Summary Page" and replace the plain text with a markdown link.

### Path Conventions

From `projects/{YYYY}/{Name}/references.md`, the path to `references/{stem}.md` is `../../../references/{stem}.md`:

- `..` → projects/{YYYY}/{Name}
- `../..` → projects/{YYYY}
- `../../..` → projects/
- `../../../references/{stem}.md` → references/{stem}.md (the canonical summary)

This is verbose but explicit. Don't use `../../wiki/references/` (assuming wiki is the root); the wiki *is* the working directory.

---

## Example (Filled-In)

```markdown
# 2025 Asian American Strategic Adaptation Historical — References

Alphabetical project bibliography for the 2025_AsnAmExample project.

## With Summary Page (Ingested)

- [**Feliciano, Cynthia (2005)** "Educational Selectivity in U.S. Immigration" — *Demography* 42(1):131-152](../../../references/Feliciano_2005_Dem.md) — original measurement of immigrant educational selectivity; anchors REA construct
- [**Feliciano, Cynthia, and Yader Lanuza (2017)** "An Immigrant Paradox?" — *ASR* 82(1):211-241](../../../references/Feliciano_Lanuza_2017_ASR.md) — REA framework applied to second-generation outcomes; supports H2
- [**Hirschman, Charles, and Morrison G. Wong (1986)** "The Extraordinary Educational Attainment of Asian Americans" — *SF* 65(1):1-27](../../../references/Hirschman_Wong_1986_SF.md) — 1940-1980 cohort time series; rejects culture-essentialist explanation
- [**Hsin, Amy, and Yu Xie (2014)** "Explaining Asian Americans' Academic Advantage" — *PNAS* 111(23):8416-8421](../../../references/Hsin_Xie_2014_PNAS.md) — effort vs cognitive ability decomposition; mechanism for H3
- [**Author, FirstName (2025)** "AAAP in 1940" — *ASR* (forthcoming)](../../../references/Smith_2025_Example_ASR.md) — author's own pre-1965 evidence rejecting hyper-selectivity; anchors H1
- [**Lee, Jennifer, and Min Zhou (2015)** *The Asian American Achievement Paradox* — Russell Sage](../../../references/Lee_Zhou_2015_AAAP.md) — community-level hyper-selectivity hypothesis; alternative tested

## Without Summary Page (Text Citation Only)

- **Sun, Yongmin (1998)** "The Academic Success of East-Asian-American Students" — *SF* 76(4):1219-1262 — earlier mechanism comparison; cite for theoretical lineage
- **Goyette, Kimberly, and Yu Xie (1999)** "Educational Expectations of Asian American Youths" — *SE* 72(1):22-36 — parent-child expectations gap; cite for cultural channel

## Non-English References

(none in this project — section omitted)
```

---

## Maintenance

- **Add entries as you cite.** Don't batch.
- **Promote from text-only to linked when you ingest.** Move the entry, don't duplicate.
- **Remove entries you decide not to cite.** Citations that don't end up in the manuscript shouldn't clutter the project's bibliography.
- **Re-check alphabetical order** during project hub edit sessions.
