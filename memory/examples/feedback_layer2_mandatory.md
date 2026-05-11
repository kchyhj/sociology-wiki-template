---
name: layer2_mandatory_when_layer1_unavailable
description: When Layer 1 (local primary source) is unavailable, escalate to Layer 2 — find the paper's PDF on the web, download to papers_web/, treat as primary. Never substitute secondary sources.
type: feedback
---

When Layer 1 is unavailable (broken conversion, no PDF, can't access), **escalate to Layer 2** as the next step. Don't jump directly to Layer 3 (leave blank) without trying Layer 2.

**Crucial constraint**: Layer 2 is *only* about obtaining the paper's full-text PDF from the web. It is NOT about reading abstracts, review summaries, Wikipedia, or any other secondary source. The acquisition path changes (local file → web download), but the verification target stays the same: the paper's own full text.

**Why no secondary-source fallback**: An earlier version of the protocol included a Layer 3 "secondary distillation" tier (review papers, textbook chapters). That tier is removed. Reviews compress information — they say "Smith finds X" but don't say *how much* or *under what method*. Using a review as verification means the wiki is two layers removed from the actual paper. The right alternative when neither Layer 1 nor Layer 2 works is to leave the section blank.

**Where to look for the paper's PDF (Layer 2)**:

1. **Author's institutional or personal website** — most papers are hosted by at least one author.
2. **Preprint servers**: SSRN, NBER, IZA, arXiv, OSF, PsyArXiv. Note the version (preprint vs accepted vs published).
3. **Repository services**: ResearchGate, Academia.edu (some host with author permission).
4. **Journal's open-access version** if available.
5. **Institutional library access** if you have credentials.

**What is NOT Layer 2**:

- ❌ Journal abstract pages (abstracts compress findings)
- ❌ Google Scholar snippets / citation cards
- ❌ Wikipedia
- ❌ Review papers, textbook chapters, handbook summaries
- ❌ Author bio pages (only confirms paper exists, not its content)
- ❌ AI summaries from any tool
- ❌ Citation snippets from other papers ("Smith finds X" in some other paper)

If the paper's full-text PDF cannot be obtained from the web, **Layer 3 = leave blank**. Do not substitute any of the above.

**How to apply**:

When Layer 1 source check fails, before going to Layer 2 try **OCR recovery on the same local PDF** (still Layer 1):

```bash
ocrmypdf papers/{stem}.pdf papers/{stem}.ocr.pdf
python -c "import pymupdf4llm; open('papers/papers_md/{stem}.md','w',encoding='utf-8').write(pymupdf4llm.to_markdown('papers/{stem}.ocr.pdf'))"
```

If OCR recovers readable text → Layer 1 success (note `via OCR` in Verification Metadata). If OCR also fails:

1. **WebSearch** for the paper title + authors + year. Goal: find a downloadable PDF.
2. **Download** the PDF to `papers_web/{stem}.pdf`.
3. **Convert** with pymupdf4llm to `papers_web/papers_web_md/{stem}.md`.
4. **If web PDF conversion is also broken** (web PDFs can be scanned too), repeat OCR recovery on `papers_web/{stem}.pdf`.
5. **Read** the converted markdown as you would Layer 1 — full read of data, methods, findings.
6. **Update Verification Metadata** with the URL, download date, version, and whether OCR was used:

```markdown
## Verification Metadata
- Layer used: Layer 2 — papers_web/papers_web_md/{stem}.md — downloaded from {URL} on 2026-05-11, version: published, via OCR (ocrmypdf)
- Empty sub-sections: (only if PDF also missing pages/sections after OCR)
- Last verification: 2026-05-11
```

If Layer 2 also fails (no PDF anywhere on the web, or OCR also failed):
- **Layer 3 = leave blank**. Do not substitute reviews, abstracts, or any secondary source.

The Verification Metadata is what makes the wiki auditable — any reader can see exactly how each fact was verified.
