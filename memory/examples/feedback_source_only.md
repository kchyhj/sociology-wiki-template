---
name: source_only_summarization
description: No fabricated content in literature notes. Every sentence in references/*.md must trace to the paper. Empty sections are correct.
type: feedback
---

When writing literature notes in `wiki/references/{stem}.md`, every sentence must trace to the actual paper. If the paper doesn't say it, the summary doesn't say it.

**Why**: The typical failure mode is plausible fabrication. An ingestion summary writes confident-sounding content about a paper's data section (specific dataset names, sample sizes, mechanism descriptions) — none of which appears in the actual paper. The wrong content then gets cited downstream in a project hub, then in a lit review draft, then in a co-authored manuscript. By the time the error is caught (often months later, often by a reviewer or co-author), citation chains across multiple artifacts need correction. The fix is preventing fabrication at the ingest step, not catching it later.

**How to apply**:

- Before each sentence in a reference summary, ask: "Did the authors say this?"
- "Obviously implies X" is not the same as "stated X". Don't extrapolate.
- Empty sub-sections are correct when the paper has nothing to put there.
- Theory attribution requires explicit citation in the source — "looks Bourdieusian" doesn't count.
- Quantitative claims must be exact from the paper's tables. No approximation.

When the instinct to fill an empty section appears: stop. The empty section is the honest report. The "filled but plausible" section is what corrupts the citation chain.
