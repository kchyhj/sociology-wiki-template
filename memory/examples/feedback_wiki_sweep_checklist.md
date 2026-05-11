---
name: wiki_sweep_per_file_checklist
description: Mandatory per-file procedure during wiki lint sweeps. Per-file conscious check prevents Layer 1 skipping under load.
type: feedback
---

During wiki lint sweeps (re-verifying many reference files in sequence), follow this procedure consciously at the start of each file. Per-file checklist prevents Layer 1 skipping when fatigue or scale pressures into shortcuts.

**Why**: When sweeping 50+ files in a session, the instinct is to batch — "I'll Layer 1 a sample, Layer 2 the rest". This *reliably* produces violations. The fix is a per-file conscious gate: each file gets the full procedure, no shortcuts.

**How to apply**:

For each file in a sweep:

### Step 1 — Read existing content + frontmatter
- Read `references/{stem}.md` body in full.
- Note the frontmatter (`authors`, `year`, `journal`, `themes`, `theories`).
- Note the current Verification Metadata.
- Check `index_authors.md` to confirm author entry is correct.

### Step 2 — Locate primary source
- `glob` for the primary source: `papers/papers_md/{stem}.md` (Layer 1) or `papers_web/papers_web_md/{stem}.md` (Layer 2 from prior session).
- If neither exists locally, the paper has never been Layer-1 or Layer-2 verified.

### Step 3 — Primary source viability check (MOST OFTEN SKIPPED)
- `wc -l papers/papers_md/{stem}.md` — should be 500-3000 lines.
- `head -50 papers/papers_md/{stem}.md` — first 50 lines should be introduction body, NOT:
  - JSTOR "This content downloaded from..." footer (the whole file is footer)
  - HeinOnline / SSRN watermark
  - OCR scramble (broken characters, no readable text)
  - Empty / mostly blank (typical for scanned/image-based PDFs)
  - PostScript metadata dump (from `.ps` direct conversion)
- If any of these patterns appear: try **Step 3.5 (OCR recovery)** before declaring Layer 1 unavailable.

### Step 3.5 — OCR recovery (still Layer 1)
- Run OCR on the same PDF: `ocrmypdf papers/{stem}.pdf papers/{stem}.ocr.pdf`, then re-convert with pymupdf4llm into `papers/papers_md/{stem}.md`.
- Re-run the Step 3 viability checks. If body text is now readable → Layer 1 success via OCR. Record `via OCR (ocrmypdf)` in Verification Metadata.
- If OCR output is still broken → Layer 1 truly unavailable. Escalate to Step 4.

### Step 4 — Layer 2 if needed: download the paper's PDF
- Search the web for the paper's full-text PDF (author's website, preprint server, journal open access, repository service).
- **No abstracts, no review summaries, no secondary sources.** If only secondary sources exist, Layer 2 fails — proceed to Layer 3.
- Download to `papers_web/{stem}.pdf`.
- Convert with pymupdf4llm to `papers_web/papers_web_md/{stem}.md`.
- Re-run viability checks. If the web-downloaded PDF's conversion is also broken, apply the same OCR-recovery pattern (`ocrmypdf` → re-convert) — still Layer 2.
- Read the converted markdown carefully (data + methods + findings).

### Step 5 — Layer 3 (if Layer 1 + Layer 2 both fail, including OCR recovery)
- The relevant sub-sections of the reference page **stay blank**.
- Do not substitute any secondary source.
- The Verification Metadata documents this state.

### Step 6 — Corrections + Verification Metadata
- Apply corrections to the body (delete unverified, fill only verified).
- Update Verification Metadata noting which layer was used (with URL and download date for Layer 2).
- Don't write "verification pending" — verify now or delete now.

### Step 7 — Pre-close self-check
- Body has only currently-verified facts?
- Verification Metadata reflects current verification (not historical)?
- No "(추후)" / "(향후)" / "(pending)" caveats? Grep before close.

The procedure adds ~5 minutes per file. The alternative (skipping the check) accumulates errors silently across the sweep, often discovered months later when downstream citations break.
