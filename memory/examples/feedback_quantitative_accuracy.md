---
name: quantitative_accuracy
description: Quote exact numbers from source tables. No approximation. Apply to coefficients, SE, p-values, N, percentages.
type: feedback
---

Quantitative claims in literature notes must be quoted exactly from the original paper's tables and figures. No approximation, no rounding, no "around X".

**Why**: Wiki link structure causes silent error propagation. A small numerical drift in one reference card shows up in concept page narrative, then in project lit review, then in the manuscript. The 30-50% effect that turns out to be 11% is the difference between a paper's central claim and a footnote. Multiple downstream papers can be corrupted by a single careless approximation.

**How to apply**:

For reference summaries, the following must be exact:
- Regression coefficients (β, OR, HR)
- Standard errors / confidence intervals
- p-values or test statistics (don't truncate to "p<.05" if paper reports p=0.023)
- Sample sizes (overall and by subgroup)
- Effect sizes (pp, log point, %)
- Comparison group proportions
- Dataset waves/years
- R² / pseudo-R²

For each quantitative claim:
- Read from the paper's table or in-text reference (not from your memory of skimming)
- Include the table/figure number in your wiki text (e.g., "β = 0.247 (Table 3, Model 4)")
- Specify units (log points vs percentage points; weighted vs unweighted)
- Specify the reference category for categorical predictors

When the PDF conversion is broken in the table area:
- Don't approximate from text. Mark "(see original)" placeholder.
- Or escalate to Layer 2 (web) — author's institutional page often has the article.
- Or leave the specific number blank (Verification Metadata notes it).

Cross-page citation of numbers:
- The reference card is the single source for the paper's numbers.
- Concept pages link to references; they don't re-quote numbers.
- Re-citing a number in a hub page is a Layer 1.5 — twice removed from source — and is a common propagation point. Avoid.
