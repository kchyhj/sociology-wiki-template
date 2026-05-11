---
name: no_unverified_claims_delete_first
description: When you find an unverified claim during review, the default action is delete, not annotate. Caveats are themselves the violation signal.
type: feedback
---

When you find a wiki claim that can't be verified, the default action is **delete**, not annotate. Caveat comments like `(needs verification)` or `(추후 검증)` are themselves the violation signal.

**Why**: The caveat-as-violation-signal is a typical failure mode. A sample size gets annotated "(approximately 5,000 — verify)". The annotation sits in the wiki indefinitely. When the wiki is later cited, the reader (or future you) doesn't re-read the parenthetical caveat. The cited number becomes "around 5,000" in a manuscript. The actual sample might be 8,425. Months-old caveat is invisible at citation time, so the wrong number reaches publication. The fix is to delete the uncertainty at write time, not annotate it.

**How to apply**:

- Never write `(pending)`, `(needs verification)`, `(추후 검증)`, `(향후 확인)`, `(TBD)`, `(approximately)`, `(probably)` in wiki body text.
- If a fact is unverified, **delete the sentence containing it**.
- An empty section is correct. Don't write "(this section needs to be filled)" — just leave it empty with the section header.
- Verification Metadata sub-section is where uncertainty *can* live (e.g., "Layer 1 unavailable — Findings section incomplete"). Not in the body.
- During lint sweeps, `grep -i "(pending\|approximately\|probably\|verify later\|추후\|향후)"` and treat hits as deletion candidates, not annotation candidates.
