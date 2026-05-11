# Reference Book Template

Use for: scholarly books (monographs and edited volumes). For chapters in edited volumes, use `type: book-chapter` (same template, narrower scope).

**File location**: `references/{Author}_{YYYY}_{TitleAbbr}.md`. Examples:
- `Lee_Zhou_2015_AAAP.md` (book: The Asian American Achievement Paradox)
- `Bourdieu_1984_Distinction.md`
- `Smith_2015_ExampleBook.md`

```markdown
---
type: book                    # or book-chapter
year: YYYY
authors: [LastName1, LastName2]
publisher: Russell Sage       # or "University of Chicago Press" etc.
editors: [EditorLastname]     # only for book chapters
themes: [RaceEthnicity, AsianAmericans, Education]
projects: [your_active_project]
theories: [hyper_selectivity, ethnic_capital]
---

# Author1 and Author2 (YYYY) Book Title

#type/book #theme/RaceEthnicity #theory/hyper_selectivity

**Bibliography**: Author, FirstName, and FirstName Coauthor. YYYY. *Book Title*. Publisher.

For chapters:
**Bibliography**: Chapter Author, FirstName. YYYY. "Chapter Title." Pp. xx-xx in *Book Title*, edited by Editor FirstName Lastname. Publisher.

## Topic

Three to five sentences. The book's central argument, the phenomenon it addresses, the gap it fills. Books are longer than papers — expect more theoretical scope.

## Key Theory / Framework

Books usually develop a *theoretical position* over the course of multiple chapters. Identify:
- The main theoretical claim (one sentence).
- The mechanisms the authors propose (with chapter references).
- The traditions the book builds on or breaks from.

For monographs, this section is typically longer than for papers (1-2 pages of wiki text). Empirical books with field methods (ethnography, interviews) need a separate "Theoretical Framework" sub-section from "Empirical Strategy".

## Data & Methods

For empirical books:
- Field site(s), time period of fieldwork.
- Sample composition (e.g., 80 interviews + 18 months ethnography).
- Triangulation methods.
- For mixed-methods, the quantitative supplement.

For theoretical books: this section may be brief or absent. Note "theoretical work" explicitly.

## Key Findings / Chapter-by-Chapter

For monographs, structure findings as **chapter-by-chapter** rather than 6-10 findings. Each chapter gets a 1-2 paragraph summary with the key claims and the empirical support.

### Chapter 1: [Title]

Key claim: [...]. Evidence: [...]. Theoretical move: [...].

### Chapter 2: [Title]

[...]

### Chapter 3: [Title]

[...]

For edited volumes, summarize chapters relevant to your interests. Don't aim for completeness — aim for the chapters that matter to your project.

## Relevance to This Project

Your interpretation. Which arguments do you take seriously? Which chapters will you cite? Which empirical findings inform your hypotheses?

## Scholarly Conversation

Typed bullets to other wiki references:

- **builds on**: [Bourdieu (1984)](../Bourdieu_1984_Distinction.md) — habitus framework
- **extended by**: [Reay et al. (2009)](../Reay_etal_2009_Sociology.md) — applied to UK higher education
- **alternative**: [DiMaggio & Mohr (1985) *AJS*](../DiMaggio_Mohr_1985_AJS.md) — cultural capital as resource vs. signal

## Reception (Optional)

For canonical books, brief notes on:
- Major reviews (in *Contemporary Sociology*, *American Journal of Sociology*).
- Common critiques.
- Influence on subsequent work.

## Verification Metadata

- **Layer used**: Layer 1 — read chapters [list]; skimmed [list]
  (or: Layer 2 — full book PDF downloaded from {URL} on [YYYY-MM-DD] to `papers_web/{stem}.pdf`)
- **Empty sub-sections** (no Layer 1 or 2 coverage): [list]
- **Last verification**: [YYYY-MM-DD]
```

---

## Discipline Reminders for Books

1. **Don't summarize from reviews.** A book review compresses 300 pages to 1500 words; it will get the field-level framing right but miss the empirical specifics that distinguish this book.
2. **Read the actual chapters you plan to cite.** If your project uses Chapter 4's evidence, Layer 1 that chapter (your local PDF). If the book isn't in your local papers/ folder, obtain its PDF from the web (Layer 2 — store in papers_web/), then read.
3. **Author's preface/introduction states the central claim.** Read it carefully — that's the most efficient verification of the theoretical position.
4. **Edited volumes: cite specific chapters, not the volume.** "Smith (2010) in Edited Volume edited by Jones" is the right citation, not "Jones (2010)".

## Non-English Books

```
홍길동_이공저자_2021_예시도서.md       (Korean example)
张三_2020_示例图书.md                   (Chinese example)
山田_2019_例示書籍.md                  (Japanese example)
```

Frontmatter `publisher` field uses the publisher's name as published (native script when applicable — e.g., 박영스토리 for a Korean publisher, 中華書局 for a Chinese publisher). Body in the book's original language; no English mirror at the reference layer.
