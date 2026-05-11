# Sociology Research Wiki — Claude Code Instructions

This file is read by Claude on every session. It defines the wiki's structure, accuracy rules, and the workflows Claude follows.

**Replace `YOUR-NAME` and `YOUR-WIKI-PATH` placeholders before first use.**

---

## Identity

User is a sociologist at `YOUR-INSTITUTION` doing literature-heavy quantitative research. Active projects span `YOUR-CATEGORIES` (e.g., stratification, race & ethnicity, political sociology). Wiki is the primary literature management system; all paper-grade work flows through it.

## Language Policy

This wiki supports three configurations. **Pick one** by editing this section:

### Option A — English-only

Everything in English. Easiest. Recommended unless you regularly read papers or write notes in another language.

### Option B — Single non-English language

The wiki operates in your primary language (Spanish, Chinese, Japanese, Korean, German, etc.). Reference summaries match the source paper's language; concept pages, project hubs, claims are all in your language.

### Option C — Your-language + English mirror (bilingual)

Your primary language for the main body, with English mirror sections after a `---` divider in concept pages, project hubs, and claims. Useful when:
- You read and publish in two languages
- You collaborate with English-speaking co-authors who need to follow the wiki
- You want the wiki's RAG/search to work in both languages

Currently configured: **Option [A/B/C — fill in]**. If Option B or C, the primary non-English language is **[your language — fill in]**.

### Applied per layer

- **Conversation with Claude**: any language; Claude responds in the user's last language.
- **Reference summaries** (`references/*.md`): single language matching the source paper. An English paper's summary is in English; a paper written in your primary language is summarized in that language.
- **Concept pages, project hubs, claims**: follow the chosen Option above.
- **Index files, log**: usually English (structural files; pick one language and stay consistent).

---

## THE TWELVE BINDING RULES

These are not guidelines. They are the conditions on every wiki write.

### Source Discipline (Rules 1–6)

1. **Source-only summarization.** When summarizing a paper, write nothing that isn't in the paper. Even if a connection seems obvious, don't write it unless the authors do.
2. **Three-layer verification before writing.** Local primary source → web-downloaded primary PDF → leave blank. **Each layer's source is read in full** — reading only the abstract, skimming, or working from snippet-based summaries does not count as verification, no matter how long the paper is. Web access is *only* for obtaining the paper's own full-text PDF; secondary sources (reviews, abstracts, Wikipedia, AI summaries) are categorically excluded. Skipping layers is the most common violation. See [`docs/VERIFICATION_PROTOCOL.md`](docs/VERIFICATION_PROTOCOL.md).
3. **Don't write / Delete first** (two scenarios). When *drafting* a new reference, concept, or hub page, don't write unverified content in the first place — empty sub-sections are the correct default. When *editing* an existing page, unverified content found in the body is deleted, not preserved with `(to be re-verified)` annotations. Burden of proof is on retention.
4. **Cite only papers in `references/`.** Inline citations must point to existing wiki files. If `Smith_2010_ASR.md` doesn't exist, ingest it first or remove the citation.
5. **No improvisation from gap.** "I don't have a paper on X — please add the PDF" beats fabricating an answer.
6. **Block the helpful instinct.** "This section feels thin" is the signal you're about to fabricate. The thin section is correct.

### Operational Discipline (Rules 7–12)

7. **Volume is not the principle.** Short pages are normal when verification is honest; long pages are warning signs. Don't lengthen a section because it "looks thin." Match length to what the source supports.
8. **No binary plausibility labels.** Never grade unverified content as "likely true," "probably correct," or "plausible." Verify it (move to body) or delete it (leave blank). The gray zone is the failure mode.
9. **Per-sentence self-interrogation.** Before keeping a sentence, ask: "is every fact in this sentence verified?" If any fact (citation, dataset name, sample size, coefficient, attribution) is uncertain, the sentence comes out.
10. **Layer 1 fragments don't count.** A `.md` conversion that's only JSTOR headers, watermarks, or blank OCR is **not** Layer 1 success. Escalate to Layer 2.
11. **Per-ingest verification metadata.** Each new reference page ends with a Verification Metadata sub-section noting which layers were used and what was confirmed.
12. **Unverifiable = blank, not best-guess.** Training-data plausibility is not verification.

Full rationale: [`docs/ACCURACY_RULES.md`](docs/ACCURACY_RULES.md).

---

## Wiki Structure

```
your-wiki/
├── CLAUDE.md                    # This file
├── README.md                    # Public-facing overview
├── index.md                     # Master navigation (project status by category)
├── log.md                       # Operation log (## [YYYY-MM-DD] op | title format)
├── books.md                     # Books ingested, chronological
├── index_authors.md             # Author index (alphabetical + CJK section)
├── index_detail.md              # Concept/theory/method index (alphabetical)
├── z_references_index.md        # Master reference filename list (dedup)
├── z_ingest_history.md          # Per-project ingest timestamps (incremental)
├── papers/                      # Layer 1 — your own PDFs, never edit
├── papers/papers_md/                     # Layer 1 conversions (read-only, pymupdf4llm)
├── papers_web/                  # Layer 2 — PDFs downloaded from web during verification
├── papers_web/papers_web_md/                 # Layer 2 conversions
├── references/                  # Layer 1 — literature notes, source-faithful
├── general/                     # Layer 2 — concept pages by ASA category
│   ├── stratification/0_index.md
│   ├── labor_markets/0_index.md
│   ├── race_ethnicity/0_index.md
│   ├── immigration/0_index.md
│   ├── gender_family/0_index.md
│   ├── political_sociology/0_index.md
│   ├── education/0_index.md
│   ├── methods/0_index.md
│   └── theory/0_index.md
├── claims/                      # Layer 3 — atomic claims in your voice
│   ├── 0_index.md
│   └── {slug}.md
├── journals/                    # Per-journal paper lists (tracked subset)
│   ├── ASR.md, AJS.md, SF.md, ARS.md, Dem.md, ...
│   ├── Econ/, PolSci/, Psych/   # Top-5 of adjacent fields
│   └── {field_specific}.md      # e.g., 한국사회학.md for Korean journals
└── projects/                    # Layer 4 — project hubs (year/name/)
    └── {YYYY}/{project_name}/
        ├── index.md
        └── references.md
```

---

## File Naming

### References (`references/`)
- Single author: `{LastName}_{YYYY}_{JournalAbbr}.md`
- Two authors: `{LastName1}_{LastName2}_{YYYY}_{Journal}.md`
- 3+ authors: `{FirstAuthor}_etal_{YYYY}_{Journal}.md`
- Books: `{Author}_{YYYY}_{TitleAbbr}.md`
- Non-English / non-Latin-script papers: native script in filename — e.g., `김저자_2024_한국학술지.md` (Korean), `张三_李四_2023_中国学刊.md` (Chinese), `山田_2022_社会学評論.md` (Japanese), `García_2021_RevistaEspañola.md` (Spanish)

### Other notes
- Concept pages: `{snake_case_slug}.md` (e.g., `hyper_selectivity.md`)
- Claims: `{descriptive_slug}.md` (e.g., `kr_edu_premium_cohort_divergence.md`)
- Project hubs: `{YYYY}_{ShortName}/index.md`

---

## Adding a New Paper — Workflow

### Step 0: Check for existing summary
Search `z_references_index.md`. If the filename stem exists, *do not re-write*. Update the projects list and add a project-specific sub-section in `## Relevance`.

### Step 1: Place PDF and convert
```bash
cp ~/Downloads/paper.pdf papers/{stem}.pdf
python -c "import pymupdf4llm; \
  open('papers/papers_md/{stem}.md','w',encoding='utf-8').write( \
  pymupdf4llm.to_markdown('papers/{stem}.pdf'))"
```

### Step 2: Layer 1 verification
**Read the full `papers/papers_md/{stem}.md`**. Confirm:
- Bibliography (authors, year, journal, volume, issue, pages) — match the source's stated metadata, not extrapolation.
- Sample size, data set name (exact), waves/years.
- Method (OLS / DID / IV / fixed effects / multilevel / etc.).
- Key findings with specific numbers.

**If the conversion is broken** (JSTOR headers only, blank OCR, scrambled pages): treat as Layer 1 unavailable, escalate to **Layer 2**:

```bash
# Find the paper's PDF on the web (author site, preprint server, journal open access).
# Download to papers_web/.
cp ~/Downloads/{stem}.pdf papers_web/{stem}.pdf

# Convert.
python -c "import pymupdf4llm; \
  open('papers_web/papers_web_md/{stem}.md','w',encoding='utf-8').write( \
  pymupdf4llm.to_markdown('papers_web/{stem}.pdf'))"

# Then read papers_web/papers_web_md/{stem}.md as you would Layer 1.
```

**Web is for the paper's full PDF only** — no abstracts, no review summaries, no AI summaries, no Wikipedia. If the paper's PDF cannot be obtained from the web either, **Layer 3 = leave the relevant sub-sections blank**. Do not substitute secondary sources. Document the layer used in Verification Metadata, including URL and download date for Layer 2.

### Step 3: Write `references/{stem}.md`
Apply [`templates/reference_paper.md`](templates/reference_paper.md). Source-only rule applies. Sub-sections that you cannot verify stay blank.

### Step 4: Update side files
- `z_references_index.md` — add stem with project tag
- `journals/{Abbr}.md` — add entry (newest year on top; within-year additions append)
- `general/{category}/0_index.md` — add to "Key Literature" section
- `index_authors.md` — add author(s) at alphabetical position. Non-Latin scripts (Korean / Chinese / Japanese / Cyrillic / Arabic / etc.) go in dedicated sections sorted by their native alphabet
- `index_detail.md` — add new theories/concepts/methods alphabetically
- If 3+ ingested papers share a theory: create/update `general/{category}/{theory}.md`

### Step 5: Log
```markdown
## [YYYY-MM-DD] ingest | {stem}
- new theories: list
- new concept page (if any)
- journals/{abbr}.md updated
```

---

## Citation Format

Standard inline citation:
```markdown
[Author (Year) *JournalAbbr*](../references/{File}.md)
```

When prose mentions another wiki paper, **always linkify** if the paper exists. Plain text mentions are link-graph holes. Run [`scripts/autolink.py`](scripts/autolink.py) periodically to auto-recover missed links.

For typed relationships (extends, critiques, replicates), use the `## 학술 대화 / Scholarly Conversation` section in each reference page — see template.

---

## The Atomic Claims Layer (`claims/`)

This folder holds **your synthesized positions in your own voice**, backed by verified citations. Distinct from:
- `references/` (authors' voice, source-faithful)
- `general/` (neutral concept pages)

When the user makes a synthesized claim in conversation ("X seems to be Y, given Smith and Jones"), offer to file it as a claim note. The user's voice is preserved verbatim; Claude verifies the citations.

Status field: `working` (tentative) | `confident` (verified, used in your published work) | `retired` (superseded, kept with explicit reason).

Filing triggers:
- **Claim signals**: "I think", "my position is", "it seems", "the conclusion is"
- **Synthesis signals**: user binds 2+ papers in one sentence
- **Reuse signals**: "I'll use this later", "remember this"

Full procedure: [`docs/WORKFLOWS.md#claims`](docs/WORKFLOWS.md).

---

## Wiki Lint

Run periodically (every 5–10 ingests, or starting a new project). The lint script checks 11 drift categories — orphan references, journal year ordering, frontmatter coverage, tag taxonomy drift (CamelCase vs snake_case), type field consistency, cross-page contradictions, stale "recent research" claims, ref→ref auto-link audit, data gap detection.

```bash
python scripts/lint.py
```

Auto-applies safe fixes (tag normalization, type unification). Reports findings that need user judgment.

After lint, push wiki to git:
```bash
git -C wiki add -A && git -C wiki commit -m "Wiki lint YYYY-MM-DD" && git -C wiki push
```

---

## Memory

Persistent rules accumulated across sessions. The `MEMORY.md` index points to discrete entries in `memory/`. Each entry has a name, description, type, and body.

Types:
- `feedback` — corrections you've given, with **Why** and **How to apply**
- `project` — context about active projects (deadlines, stakeholders, decisions)
- `reference` — pointers to external systems (Linear, Slack, Grafana, etc.)
- `user` — facts about the user (role, preferences, knowledge)

Update memory whenever the user corrects a behavior or confirms a non-obvious approach. See [`memory/README.md`](memory/README.md).

---

## What NOT to Do

- **No web search to fill wiki gaps** (Rule 5). The wiki is the source of truth at response time.
- **No "general knowledge" augmentation** of paper summaries. If the paper doesn't say it, the summary doesn't say it.
- **No quantitative summaries** ("approximately 50%") when the source has exact numbers — quote the number.
- **No theory-of-X attributions** unless the source explicitly cites the theorist.
- **No bullet-list claims** in the claims/ folder. Prose forces synthesis.
- **No deferred verification** — verify or delete, never "later".
- **No mass-edits across multiple references** in one operation. One paper at a time.

---

## When You're Unsure

The order of operations when Claude isn't sure how to proceed:

1. Check the relevant template in [`templates/`](templates/).
2. Check the relevant doc in [`docs/`](docs/).
3. Check related entries in [`memory/`](memory/).
4. Ask the user before writing.

The cost of pausing to confirm is low; the cost of fabricating a citation is months of downstream cleanup.
