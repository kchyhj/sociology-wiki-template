---
name: three_layer_verification_protocol
description: Verification ordering — local primary source → web-downloaded primary PDF → leave blank. Secondary sources prohibited at every layer. Never skip Layer 1.
type: feedback
---

Verification of every wiki fact follows a strict three-layer order:

1. **Layer 1**: local primary source (the actual paper, via `papers/{stem}.pdf` + `papers/papers_md/{stem}.md`)
2. **Layer 2**: web-downloaded primary source (paper's full PDF found online, downloaded to `papers_web/{stem}.pdf`, converted to `papers_web/papers_web_md/{stem}.md`, then treated as primary). **Web access is for the paper's own PDF only** — no abstracts, no review summaries, no Wikipedia, no AI summaries, no other secondary sources.
3. **Layer 3**: leave blank.

**Why**: Skipping Layer 1 is the most common violation pattern. The skip is rationalized as "the paper is long" or "the conversion is broken" — but a broken conversion is a Layer 1 *unavailable* signal, not a Layer 1 *success* signal. Sparse conversions look identical to successful ones unless you check.

The protocol previously included a "secondary distillation" tier (reviews, textbooks). That tier is removed: secondary sources compress information and produce silent error compounding. The binary outcome — read the actual paper or leave blank — is more rigorous.

**How to apply**:

- For every reference page, check the conversion first: `wc -l papers/papers_md/{stem}.md` (should be 500-3000), `head -50 papers/papers_md/{stem}.md` (should be introduction body, not bibliography/header).
- If checks fail: try **OCR recovery** on the same PDF first (`ocrmypdf {stem}.pdf {stem}.ocr.pdf` → re-convert with pymupdf4llm). OCR is a recovery step within the current layer, not a separate layer. Only if OCR also fails, treat Layer 1 as unavailable and escalate to Layer 2.
- Layer 2 web-downloaded PDFs can also be image-based (scanned older papers, JSTOR scans). Apply the same OCR-recovery pattern on `papers_web/{stem}.pdf` if its conversion is broken.
- Layer 2 is the paper's full PDF only — never an abstract, a review summary, or anything else from the web.
- Web-downloaded PDFs go in `papers_web/`; their conversions in `papers_web/papers_web_md/`. Audit-clear separation from local `papers/` and `papers/papers_md/`.
- If neither Layer 1 nor Layer 2 yields readable text (after OCR), the relevant wiki sub-section stays blank. No filler.
- "Read the abstract" is not Layer 1 or 2. Layer 1/2 is reading the data section + methods + findings carefully from the paper's full text.
- Verification Metadata required at the end of every reference page, noting which layer was used and whether OCR was applied.
