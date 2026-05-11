---
name: recheck_protocol
description: When reusing wiki content (citing in a new paper, repeating a claim in a draft), re-verify at the layer the original was verified. Don't trust your own past wiki as authoritative without re-check.
type: feedback
---

When you're about to reuse wiki content — citing a reference in a new manuscript, repeating a claim from your own claims/ folder, drawing on a concept page — re-verify at the layer the original was verified. Don't treat your own past wiki as authoritative without re-check.

**Why**: Wiki content ages. The Verification Metadata says "Layer 1: full read [2024-12-03]". It's now 2026-05. In the intervening time, you might have:
- Revised the wiki (the claim may have shifted)
- Read newer literature that contradicts (the claim may be retired-worthy)
- Have a clearer understanding (the prior summary may be wrong)

Treating past wiki as authoritative-without-recheck is the same failure mode as treating training-data plausibility as verification.

**How to apply**:

Before citing a wiki entry in a new manuscript:
- Check the Verification Metadata date.
- If > 12 months ago, re-check Layer 1 on the load-bearing claims you'll cite.
- If < 12 months, spot-check the section you're drawing from.
- Update Verification Metadata after re-check.

Before repeating a claim from `claims/` folder in a new draft:
- Read the claim's body and counter-evidence section.
- If status is `working`, treat as draft-only (do not externally cite).
- If status is `confident`, verify the claim still holds against any newly ingested counter-evidence.
- If new evidence contradicts: update the claim, possibly to `retired`.

Before drawing on a concept page's empirical record:
- Re-read the cited references in the table.
- Verify your characterization of "supported / rejected / conditional" still holds.
- Update if needed.

The wiki is a *break point* in the citation chain (Philosophy doc). Break points need maintenance. Recheck is the maintenance.
