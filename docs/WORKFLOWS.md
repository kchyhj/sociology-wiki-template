# Workflows

Step-by-step procedures for the most common wiki operations.

---

## Ingest a New Paper

**When**: You have a PDF you want as a literature note in the wiki.

**Steps**:

1. **Check for existing summary.** Search `z_references_index.md` for the filename stem.
   - If exists: do *not* re-write. Update the projects list and add a project-specific sub-section in `## Relevance` of the existing file.
   - If new: proceed.

2. **Place PDF**:
   ```bash
   cp ~/Downloads/paper.pdf papers/{stem}.pdf
   ```
   where `{stem}` follows file-naming convention (`Author_YYYY_Journal.md`).

3. **Convert to markdown**:
   ```bash
   python -c "
   import pymupdf4llm
   md = pymupdf4llm.to_markdown('papers/{stem}.pdf')
   open('papers/papers_md/{stem}.md','w',encoding='utf-8').write(md)
   "
   ```

4. **Layer 1 verification.** Check the conversion:
   ```bash
   wc -l papers/papers_md/{stem}.md         # 500-3000 lines expected
   head -50 papers/papers_md/{stem}.md      # First 50 lines = introduction, not bibliography/header?
   grep -c "^## " papers/papers_md/{stem}.md # 5-15 section headers expected
   ```
   - If checks pass: read source full. Note the data set name, sample size, methods, key findings with exact numbers.
   - If checks fail: first try **OCR recovery** on the *same* PDF (still Layer 1):
     ```bash
     ocrmypdf papers/{stem}.pdf papers/{stem}.ocr.pdf
     python -c "import pymupdf4llm; open('papers/papers_md/{stem}.md','w',encoding='utf-8').write(pymupdf4llm.to_markdown('papers/{stem}.ocr.pdf'))"
     ```
     Re-run the sanity check. If OCR also fails, escalate to **Layer 2** — find the paper's PDF on the web, download to `papers_web/{stem}.pdf`, convert to `papers_web/papers_web_md/{stem}.md`, then read. Web is for the paper's own PDF only — no abstracts, no review summaries, no Wikipedia. Apply the same OCR-recovery pattern on the web-downloaded PDF if its conversion is also broken. If neither Layer 1 nor Layer 2 yields readable text, **Layer 3 = leave the relevant sub-sections blank** (do not substitute secondary sources).

5. **Write `references/{stem}.md`** using [`templates/reference_paper.md`](../templates/reference_paper.md) or [`templates/reference_book.md`](../templates/reference_book.md).
   - Source-only rule applies (only what the paper says).
   - Per-sentence self-interrogation (Rule 9).
   - Empty sub-sections allowed; never write filler.

6. **Update side files**:
   - `z_references_index.md` — add entry: `Author_YYYY_Journal.md | theme:Stratification | projects:[your_project]`
   - `journals/{Abbr}.md` — add entry at top of the year section (newest year first; within year, append)
   - `general/{category}/0_index.md` — add to "Key Literature" section under the appropriate project sub-heading
   - `index_authors.md` — insert author(s) at alphabetical position
   - `index_detail.md` — add new theories/concepts/methods (alphabetical)
   - If 3+ ingested papers share a theory: create or update `general/{category}/{theory}.md` concept page (its empirical record table)

7. **Verification Metadata.** Before closing the file, add:
   ```markdown
   ## Verification Metadata
   - Layer used: Layer 1 — papers/papers_md/{stem}.md — full read [YYYY-MM-DD]
     (or: Layer 2 — papers_web/papers_web_md/{stem}.md — downloaded from {URL} on [YYYY-MM-DD], version: preprint / accepted / published)
   - Empty sub-sections (verification incomplete): (list, if any)
   - Last verification: [YYYY-MM-DD]
   ```

8. **Log**:
   ```markdown
   ## [YYYY-MM-DD] ingest | {stem}
   - new theories added: [list]
   - new concept page: (if any)
   - journals/{abbr}.md updated
   ```

9. **One paper at a time.** Do not start another ingest until this one is fully closed.

---

## File a Claim

**When**: In conversation, the user makes a synthesized statement combining multiple papers. Claude offers to file as a claim.

**Triggers Claude recognizes**:
- Claim signals: "I think", "my position is", "it seems", "the conclusion is" (and equivalents in other languages — e.g., Korean "내가 보기엔", "내 입장은")
- Synthesis: user binds 2+ papers in one sentence
- Reuse: "I'll use this later", "remember this"
- Explicit: "file this as a claim"

**Steps** (after user accepts):

1. **Verify all cited references exist.** Each cited paper must be in `references/`. If user mentioned a paper not in the wiki, ask: ingest first or remove from claim?

2. **Determine status.** Default `working`. If user has used this position in published work or repeatedly defended it, candidate `confident`.

3. **Choose filename** (descriptive snake_case slug): e.g., `kr_edu_premium_cohort_divergence.md`, `culture_nonignorable_asian_american.md`.

4. **Write `claims/{slug}.md`** using [`templates/claim.md`](../templates/claim.md).
   - User's voice preserved verbatim.
   - One claim per file (atomicity).
   - Prose, not bullets.
   - Counter-evidence section required (be honest about scope).

5. **Update `claims/0_index.md`** "Active Claim List" section, in the appropriate status block.

6. **Two-way linking (optional but recommended)**:
   - In the cited reference's `## Scholarly Conversation` section (or `## Relevance`), add a back-pointer:
     ```markdown
     - **referenced in claim**: [Claim Title](../claims/{slug}.md) — short note
     ```
   - In the relevant concept page's `## Adjacent Theories` section (if applicable).

7. **Log**:
   ```markdown
   ## [YYYY-MM-DD] claim | {slug}
   - status: working / confident
   - cited references: [list]
   - related concepts: [list]
   ```

---

## Create a Concept Page

**When**: 3+ ingested references share a theory/concept and there's no dedicated page yet.

**Steps**:

1. **Identify category.** Which `general/{category}/` does the concept belong to? (Primary topic.)

2. **Choose filename**: `general/{category}/{snake_case_slug}.md`. E.g., `hyper_selectivity.md`, `cumulative_advantage.md`.

3. **Write the page** using [`templates/concept.md`](../templates/concept.md).
   - Definition + variants + operationalization + empirical record table + adjacent theories.
   - Empirical record table is the heart — every entry is a verified reference.

4. **Cross-link**:
   - From `general/{category}/0_index.md` "Core Concepts" — add bullet with link.
   - From each cited reference's `## Theory / Framework` — replace inline theory mention with `[Theory Name](../../general/{category}/{slug}.md)`.

5. **Update `index_detail.md`** — add the concept alphabetically.

6. **Log**:
   ```markdown
   ## [YYYY-MM-DD] concept | general/{category}/{slug}
   - threshold: 3 ingested references share this concept
   - empirical record: N entries
   ```

---

## Start a New Project

**When**: You're beginning a new research project that warrants its own hub.

**Steps**:

1. **Choose project name**: `{YYYY}_{ShortName}` (year of project start + short slug).

2. **Create folder**: `projects/{YYYY}/{ProjectName}/`.

3. **Write `index.md`** using [`templates/project_hub.md`](../templates/project_hub.md).
   - Status, research question, hypotheses, data, methods (use whatever status convention you prefer).

4. **Write `references.md`** using [`templates/project_references.md`](../templates/project_references.md).
   - Empty alphabetical sections (`With Summary Page` and `Without Summary Page`) ready for entries.

5. **Add to master `index.md`**:
   - Insert under the primary category section.
   - Status: `In progress`.

6. **Update relevant `general/{category}/0_index.md`**:
   - Add to "Related Projects" table.

7. **Log**:
   ```markdown
   ## [YYYY-MM-DD] project | {YYYY}_{ProjectName}
   - primary category: stratification (or whatever)
   - cross-categories: education, race_ethnicity
   - area: asian_american (if applicable)
   ```

---

## Run Wiki Lint

**When**: Periodically — every 5-10 ingests, or when starting a new project, or before pushing to GitHub.

**Steps**:

1. **Run lint script**:
   ```bash
   python scripts/lint.py
   ```

2. **Review findings**. The script reports:
   - Orphan references (not in any project's references.md)
   - Journals not in year-descending order
   - Frontmatter coverage gaps
   - Tag taxonomy drift (CamelCase vs snake_case inconsistency)
   - Type field drift (`book_chapter` vs `book-chapter`)
   - Cross-page contradictions (same paper described differently in two places)
   - Stale "recent research" claims (cited as recent but 5+ years old)
   - Prose mentions missing markdown link
   - Data gaps (papers cited 3+ times but not ingested)

3. **Apply safe fixes automatically**. The script can fix:
   - Tag casing normalization
   - Type field unification
   - Year ordering in journal files

4. **Manual fixes for**:
   - Cross-page contradictions (which version is correct? — verify against source)
   - Stale claims (which paper supersedes? — manual research)
   - Data gaps (ingest decision)

5. **Re-run lint** until all issues are resolved or explicitly accepted (with comment in `log.md`).

6. **Commit and push**:
   ```bash
   git -C wiki add -A
   git -C wiki commit -m "Wiki lint YYYY-MM-DD: {summary of changes}"
   git -C wiki push
   ```

7. **Log**:
   ```markdown
   ## [YYYY-MM-DD] lint | wiki
   - {N} stale claims fixed
   - {N} orphan references identified (no project linkage)
   - {N} prose mentions auto-linked (Step 10)
   - {N} data gap candidates flagged for ingestion
   ```

---

## Move a Project Between Years

**When**: A project started in 2024 is still active in 2026; you want to update the year folder.

**Rule**: Move the wiki folder, don't re-create.

**Steps**:

1. `mv projects/2024/{ProjectName} projects/2026/{ProjectName}`
2. Update master `index.md` — remove from 2024 section, add to 2026.
3. Update `general/{category}/0_index.md` "Related Projects" — update the link path.
4. Grep for the old path across the wiki and update any references.
5. Log:
   ```markdown
   ## [YYYY-MM-DD] move | {ProjectName}
   - from: projects/2024/{ProjectName}
   - to: projects/2026/{ProjectName}
   - reason: still active in 2026
   ```

---

## Delete a Project (or Archive)

**When**: A project has been completed (published) or abandoned.

**Three paths**:

### Path A — Published, becomes the canonical reference of that paper

1. Update `projects/{YYYY}/{ProjectName}/index.md` Status to "Published" with journal + year.
2. Add the published paper to the appropriate `journals/{Abbr}.md`.
3. Keep the project folder for the historical record (it has the analysis history).
4. Optionally move to `projects/Published/` if you want active-vs-published separation.

### Path B — Archived externally

If you maintain a separate archive folder (e.g., `archive/` or `old_projects/`) for completed projects:

1. Move the *external* (non-wiki) project folder into the archive.
2. **Keep** `wiki/projects/{YYYY}/{ProjectName}/` — wiki state survives the external folder move.

### Path C — Abandoned

1. Delete `wiki/projects/{YYYY}/{ProjectName}/` entirely.
2. Remove from master `index.md`.
3. Remove from `general/{category}/0_index.md`.
4. Log:
   ```markdown
   ## [YYYY-MM-DD] delete | {ProjectName}
   - reason: abandoned, no longer pursued
   ```

---

## Update Memory

**When**: User corrects a behavior or confirms a non-obvious approach.

**Steps**:

1. **Categorize**: `feedback` | `project` | `reference` | `user` (see `memory/README.md`).

2. **Choose filename**: `memory/{type}_{descriptive_slug}.md`. E.g.:
   - `feedback_summary_source_only.md`
   - `project_kr_far_right.md`
   - `reference_zotero_workflow.md`

3. **Write the entry** with frontmatter:
   ```yaml
   ---
   name: {short name}
   description: {one line, used for relevance scoring in future sessions}
   type: feedback
   ---

   {Content. For feedback: rule + Why + How to apply.}
   ```

4. **Update `memory/MEMORY.md`** index — add one line under the matching section:
   ```
   - [{Title}]({filename}.md) — {one-line hook}
   ```

5. Memory entries are loaded into Claude's context at session start. Keep them concise. The body of a feedback entry is rarely more than 5-10 lines.

---

## RAG Re-Index

**When**: After significant wiki changes (5+ ingests, lint sweep, refactor).

**Steps**:

1. **Run incremental indexer**:
   ```bash
   python scripts/index_papers.py --incremental
   ```
   This indexes only files modified since last run (using mtime).

2. For a full rebuild (rare): `--full --reset`.

3. The script outputs:
   - Number of files indexed
   - Embedding calls (cost indicator)
   - Total chunks in collection

4. Test the index: `python scripts/index_papers.py --rebuild-history` if mtimes got desynced.

---

## End-of-Session Checklist

Before closing a Claude Code session:

1. **All open ingests finished?** No half-done reference pages.
2. **All log entries written?** `log.md` updated for every operation.
3. **Side files updated?** `z_references_index.md`, journal files, category indexes.
4. **Verification Metadata?** Every new reference page has it.
5. **No caveat words?** `grep -i "(pending\|추후)" *.md` shows zero.
6. **Lint clean?** Recent changes pass lint.

If yes to all, commit and push.

If no, finish the open ones before closing. The discipline depends on it.
