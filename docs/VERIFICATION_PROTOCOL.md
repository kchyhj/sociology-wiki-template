# The Three-Layer Verification Protocol

Every factual claim in the wiki — dataset name, sample size, regression coefficient, citation lineage, theoretical attribution — passes through this protocol *before* it's written.

This is the single most important piece of operational discipline in the system. Skipping layers is the most common failure pattern. This doc explains the order, the folder convention, and why secondary sources are excluded.

---

## The Protocol

```
Layer 1 — LOCAL PRIMARY SOURCE
   Read the paper itself. PDF in papers/ + pymupdf4llm conversion at papers/papers_md/{stem}.md.
   ↓ conversion broken (empty/garbage/scan)
   OCR recovery: re-extract with ocrmypdf or equivalent (still Layer 1 — same PDF)
   ↓ OCR also fails or PDF unavailable
Layer 2 — WEB-DOWNLOADED PRIMARY SOURCE
   Search the web for the PDF of the paper itself. Download to papers_web/{stem}.pdf,
   convert to papers_web/papers_web_md/{stem}.md, then treat as primary source.
   Web is used ONLY to obtain the paper's PDF. Abstracts, review summaries,
   Google Scholar snippets, Wikipedia entries, and other secondary sources are NOT permitted.
   ↓ conversion broken
   OCR recovery: re-extract with ocrmypdf or equivalent on the downloaded PDF
   ↓ OCR also fails or paper PDF cannot be obtained from any web location
Layer 3 — LEAVE BLANK
   The wiki section stays empty. Better empty than fabricated.
```

**Three layers, not four. No "secondary distillation" tier.** Reviews, textbook summaries, abstract aggregators, and any source that is not the paper's own full text are categorically excluded from verification.

**OCR is a recovery step, not a layer.** It re-extracts text from the *same* PDF when the default conversion fails (typically because the PDF is image-based or has a corrupted text layer). It preserves the source's primary-source status — only the text-extraction tool changes. Applies at both Layer 1 and Layer 2.

---

## Why Three Layers, Not Four

An earlier version of this protocol included a Layer 3 "secondary distillation" tier (review papers, textbooks, abstract aggregators) as a fallback when both local and web-downloaded PDFs failed.

That tier is removed. The reasoning:

1. **Secondary sources compress information.** A review paper says "Smith finds effort explains most of the gap"; it doesn't say *how much* or *under what method*. Using the review as verification source means the wiki's "verified" content is two layers removed from the actual paper.
2. **Compression discards conditions.** The conditional findings, robustness checks, and exact specifications that matter most for sociology accuracy are exactly what review papers drop.
3. **Citation chain corruption.** When you cite Smith via a review's summary, then later cite the wiki via your paper, the eventual reader is three steps removed from Smith. The original meaning erodes at each step.
4. **The right alternative is leaving blank.** If you can't access the paper itself (even from the web), the wiki simply doesn't have that fact. The empty section is correct.

The simpler protocol forces a binary outcome: either you read the actual paper, or the section is empty. There is no middle ground where "I read someone else's summary of the paper" counts as verification.

---

## Folder Convention

Two parallel folder structures separate Layer 1 (local) from Layer 2 (web-downloaded):

```
papers/                # Layer 1 — your own PDFs
└── {stem}.pdf         # PDF you obtained through library access, author's website, conference proceedings, etc.

papers/papers_md/               # Layer 1 conversions
└── {stem}.md          # pymupdf4llm conversion of papers/{stem}.pdf

papers_web/            # Layer 2 — web-downloaded PDFs (during verification)
└── {stem}.pdf         # PDF you downloaded from the web specifically to verify a wiki fact

papers_web/papers_web_md/           # Layer 2 conversions
└── {stem}.md          # pymupdf4llm conversion of papers_web/{stem}.pdf
```

**Why separate folders?**

- Audit trail: any reader of the wiki can see which papers were "you brought to the wiki" vs "Claude/you fetched from web during verification".
- Re-verification: when a future lint sweep needs to re-confirm, the `papers_web/` folder is a candidate to re-download (in case the original web source is gone).
- Provenance: the Verification Metadata in each reference page notes whether the source was `papers/` or `papers_web/`. The folder distinction is structural.

**Conversion command (same for both)**:

```bash
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/{stem}.pdf')   # or papers_web/{stem}.pdf
open('papers/papers_md/{stem}.md','w',encoding='utf-8').write(md)  # or papers_web/papers_web_md/{stem}.md
"
```

---

## Layer 1 — Local Primary Source

The paper is in `papers/{stem}.pdf` and a conversion exists at `papers/papers_md/{stem}.md`.

### Sanity check the conversion

A `.md` conversion can fail in characteristic ways. Check before relying on it as Layer 1:

```bash
wc -l papers/papers_md/{stem}.md           # 500-3000 lines is normal
grep -c "^## " papers/papers_md/{stem}.md  # 5-15 section headers typical
head -50 papers/papers_md/{stem}.md        # First 50 lines = paper introduction body
```

If the conversion is broken (JSTOR header only, OCR scramble, watermark only, blank fragments, empty body — typical for scanned/image-based PDFs), **try OCR recovery first** before escalating to Layer 2. A sparse conversion is not Layer 1 success — it's Layer 1 failure that's easy to mistake for success.

### OCR recovery (Layer 1 retry, same PDF)

When `pymupdf4llm` produces empty/garbage output, the PDF likely has no embedded text layer (e.g., a scanned reproduction). Run OCR on the local PDF and re-convert:

```bash
# Option A: ocrmypdf (tesseract-backed; open source; recommended default)
#   choco install ocrmypdf  /  brew install ocrmypdf  /  pip install ocrmypdf
ocrmypdf papers/{stem}.pdf papers/{stem}.ocr.pdf
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/{stem}.ocr.pdf')
open('papers/papers_md/{stem}.md','w',encoding='utf-8').write(md)
"

# Option B: marker / MinerU (LLM-backed; better for tables/equations in quant papers)
# Option C: Apple Preview (macOS, GUI single-file fallback)
```

Re-run the sanity check on the new `papers/papers_md/{stem}.md`. If it now looks like normal body text → Layer 1 success via OCR. Record this in Verification Metadata: `Layer 1 — via OCR (ocrmypdf)`.

If OCR output is still garbage (severely degraded scan, handwriting, non-Latin scripts without language data) → Layer 1 unavailable. Escalate to Layer 2.

### Full-read obligation

When the conversion is good, read it. Note:
- Bibliography (authors, year, journal, volume, issue, pages)
- Dataset name (exact: NLSY79 ≠ NLSY97, ECLS-K ≠ ELS)
- Sample size (exact)
- Method (specific identification strategy)
- Key findings with specific numbers

Per-sentence verification: each summary sentence must trace to the source.

---

## Layer 2 — Web-Downloaded Primary Source

When Layer 1 is unavailable, the *only* permitted action is: find the paper's PDF on the web, download it, convert, treat as primary.

### Where to look (in order)

1. **Author's institutional or personal website** — most papers are hosted by at least one author for non-commercial download.
2. **Preprint servers**: SSRN, NBER, IZA, arXiv, OSF, PsyArXiv. The pre-publication version is acceptable; note the version in Verification Metadata.
3. **Repository services**: ResearchGate, Academia.edu (some host published versions with author permission).
4. **Journal's open-access version** if the journal offers one.
5. **Institutional library access** if you have credentials.

### What is NOT permitted in Layer 2

The web is used **only** to obtain the paper's full-text PDF. The following secondary sources are categorically prohibited as verification source:

- ❌ Journal abstract pages (insufficient — abstracts compress findings)
- ❌ Google Scholar snippets / citation cards
- ❌ Wikipedia entries
- ❌ Review papers, textbook chapters, handbook summaries
- ❌ Conference talk recordings or slides
- ❌ Blog posts, news articles, podcast discussions
- ❌ Author's CV listing or institutional bio page (only confirms the paper exists, not its content)
- ❌ Citation snippets from other papers ("Smith 2010 finds X" — that's another paper's claim about Smith, not Smith itself)
- ❌ AI summaries from any tool
- ❌ Database descriptions ("the NLSY79 is a longitudinal study of...") — useful for context but not verification of a paper's claim

If the paper's full-text PDF cannot be obtained from the web, Layer 2 has failed. Proceed to Layer 3 (leave blank). Do not substitute a secondary source.

### Storing the download

```bash
# Download the PDF (browser save-as, wget, curl, etc.) to papers_web/
cp ~/Downloads/Smith_2010_ASR.pdf papers_web/Smith_2010_ASR.pdf

# Convert
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers_web/Smith_2010_ASR.pdf')
open('papers_web/papers_web_md/Smith_2010_ASR.md','w',encoding='utf-8').write(md)
"

# Then read papers_web/papers_web_md/Smith_2010_ASR.md as you would a Layer 1 source.
```

### OCR recovery at Layer 2

Web-downloaded PDFs can also be image-based (older papers, JSTOR scans, some institutional archives). Apply the same OCR recovery as Layer 1, but on the `papers_web/` PDF:

```bash
ocrmypdf papers_web/{stem}.pdf papers_web/{stem}.ocr.pdf
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers_web/{stem}.ocr.pdf')
open('papers_web/papers_web_md/{stem}.md','w',encoding='utf-8').write(md)
"
```

Record `via OCR (ocrmypdf)` in Verification Metadata along with the URL and download date. If OCR also fails, Layer 2 is unavailable → Layer 3 (leave blank).

### Provenance metadata

Note in the Verification Metadata:
- Where the PDF was obtained (URL or author site)
- Which version (preprint, accepted manuscript, published version)
- Date of download
- Whether OCR was used

This audit trail matters because web sources can disappear.

---

## Layer 3 — Leave Blank

If the paper's PDF cannot be obtained from Layer 1 *or* Layer 2, the wiki section stays empty.

Not "filled in with general knowledge". Not "best guess from training data". Not "(verification pending)". Empty.

The reader of the wiki (often future you) needs to be able to *trust* what's there. Filling sections with plausible content destroys that trust. An empty section is correct.

---

## Hard Rules

These rules eliminate the most common violation patterns:

1. **No "(verification pending)" annotations.** The annotation is the violation signal. Verify now or delete now.
2. **No "(추후 검증)" / "(향후 확인)"** in any language. Same rule.
3. **No layer-skipping.** Don't go to Layer 2 because Layer 1 is "long". Read it.
4. **No Layer 1 success on broken conversion.** Check the file before claiming Layer 1 read.
5. **No secondary source verification.** Reviews, textbooks, abstracts — never. Layer 2 is the paper's full PDF, nothing else.
6. **No general knowledge augmentation.** If your knowledge of the field tells you the paper "probably uses X method", but the paper doesn't say so, don't write it.
7. **No best-guessing numbers.** "Sample around 5000" is not verified. Either you have the exact N or you have nothing.
8. **No theory attribution by association.** If the paper doesn't cite Theory T, don't write "this is in the T tradition" even when it obviously is.
9. **Layer 1 or Layer 2 is mandatory** for any paper that gets a reference card. If neither is available, the paper does not get a reference card — it stays in `references.md` as a text-only citation candidate.

---

## Verification Metadata in Each Reference Page

Every reference page ends with this sub-section:

```markdown
## Verification Metadata
- **Layer used**: Layer 1 — `papers/papers_md/Smith_2010_ASR.md` — full read [YYYY-MM-DD]
  (or: Layer 2 — `papers_web/papers_web_md/Smith_2010_ASR.md`, downloaded from {URL} on [YYYY-MM-DD],
  version: preprint / accepted manuscript / published)
- **Empty sub-sections** (no Layer 1 or 2 coverage of the topic): [list, if any]
- **Last verification**: [YYYY-MM-DD]
```

This metadata is the *signature* of accuracy work. A reference page without verification metadata is suspect. One with metadata noting "Layer 1: full read [date]" or "Layer 2: web-downloaded from {URL}" is trustworthy.

When the wiki gets lint-checked, references without verification metadata get flagged for re-verification.

---

## The Anti-Pattern Gallery

Here's how violations actually look in practice.

### Anti-pattern 1: Substituting a secondary source

> "Smith (2010) shows X — confirmed via the Smith chapter in Lee et al. (2024) Annual Review."

The Annual Review chapter says Smith shows X. But it compresses the claim. Smith (2010) might actually show X-conditional-on-Y; the review dropped Y. Using the review as verification is forbidden — verify against Smith (2010) itself or leave blank.

### Anti-pattern 2: Abstract scraping

> "Smith (2010) abstract reports a 30% effect. ✓ Verified via journal abstract page."

Abstracts compress. The actual paper's findings table may show 28.4% in one specification and 32.1% in another. Abstract scraping is forbidden — get the full PDF or leave blank.

### Anti-pattern 3: Plausible fabrication

> "Authors use a fixed effects model to control for unobserved heterogeneity at the school level."

If you didn't read the actual methods section, you don't know if it's fixed effects, random effects, OLS with school controls, or none of the above. "Probably fixed effects" is not verification.

### Anti-pattern 4: The deferred caveat

> "Sample is NLSY (likely NLSY79 but need to verify)."

You wrote "likely NLSY79". You'll come back to verify. You won't. Six months later you cite the wiki, the parenthetical caveat is invisible, you confidently write "Smith uses NLSY79". The paper used NLSY97.

### Anti-pattern 5: AI summary as substitute

> "Per the AI's reading of the paper, the main finding is X."

Not allowed. Verification is reading the paper yourself (or a competent agent reading it from the actual PDF). An AI summary of an abstract scraped from a journal page is not Layer 1 or 2.

---

## The Cost-Benefit

Layer 1 verification — a careful full read of the paper — is the real time cost of this system. It's slower than LLM-assisted skimming. Slower is the trade.

The cost of skipping:
- A brief saving on ingestion
- Hours of downstream debugging when your manuscript is returned with a "this isn't what the cited paper shows" comment
- Days of credibility recovery when a single hallucinated citation gets propagated through a citation chain

The expected payoff: verification at the wiki layer prevents errors from compounding across the artifacts that cite the wiki later.

---

## When You Don't Have Time

You always have time. If you don't have time to verify at Layer 1 or Layer 2, you don't have time to ingest the paper. Save the PDF candidate, skip the wiki entry, do it next week.

A wiki with 200 verified references is more valuable than a wiki with 800 partly-fabricated references. The first is a citation you can trust; the second is a citation chain that breaks at random.
