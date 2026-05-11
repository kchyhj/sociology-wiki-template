# The Twelve Binding Rules

These are the operational rules that turn the philosophy into discipline. Each rule has a *why* (the failure mode it prevents) and a *how to apply* (what to do in practice).

The rules cluster into two groups: **source discipline** (rules 1-6, about what content is allowed) and **operational discipline** (rules 7-12, about how to verify and self-check).

---

## Rule 1: Source-Only Summarization

**The rule**: When summarizing a paper, write nothing that isn't in the paper. Even when a connection seems obvious, don't write it unless the authors do.

**Why**: The most common hallucination is "natural extension". You read a paper that studies X; while writing the summary, your mind makes the obvious link to Y. The link is plausible but not what the paper says. Your wiki summary now says X-implies-Y. Six months later you cite the wiki and write "Smith (2010) shows X-implies-Y". Reviewer 2 reads Smith. The paper doesn't say Y. You lose credibility.

**How to apply**:
- Before writing each sentence, ask "did the authors say this?"
- If "obviously yes but not literally" — don't write it. The "obvious extension" goes in a claim, not a reference summary.
- Theoretical attribution: only write "uses theory T" if the paper *cites* T or explicitly *names* T. Family resemblance to T isn't attribution.

---

## Rule 2: Three-Layer Verification Before Writing

**The rule**: Local primary source → web-downloaded primary PDF → leave blank. **Each layer's source is read in full** — reading only the abstract, skimming sections, or working from snippet-based summaries does not count as verification, regardless of paper length. Secondary sources (reviews, textbooks, abstracts, Wikipedia, AI summaries) are categorically excluded. See `docs/VERIFICATION_PROTOCOL.md`.

**Why**: Without explicit layers, "verify" is unimplementable. The protocol gives a strict operational order: read the actual paper *in full*, or if you don't have it locally, download its PDF from the web (no other web content allowed) and read *that* in full, or leave the section blank. There is no "consult a review or abstract" middle path — that path produces silent error compounding. And there is no "the paper is too long, I'll just read the parts that look relevant" shortcut — that path is how dataset names get confused, sample sizes get fabricated, and theoretical attributions drift.

**How to apply**:
- Read the entire paper, not just intro + conclusion. Methods, data, robustness checks, and limitations sections are where the verifiable details live.
- Every reference page ends with a Verification Metadata sub-section listing which layer was used and (for Layer 2) the URL and download date.
- Layer-skipping is the most common violation. Don't go to Layer 2 because Layer 1 is "long" — Layer 1 length is irrelevant if the PDF is available.
- Layer 1 = the actual paper, not a Layer 2 abstract dressed up as Layer 1.
- Layer 2 web access is *only* for obtaining the paper's full-text PDF. Abstracts, snippets, review summaries, AI outputs — never.
- Web-downloaded PDFs go in `papers_web/`; their conversions in `papers_web/papers_web_md/`. Parallel folders to `papers/` and `papers/papers_md/`, for audit clarity.

---

## Rule 3: Don't Write / Delete First (Two Scenarios)

**The rule has two modes, depending on whether you are *drafting* or *editing*.**

### Scenario A — Drafting a new page (DON'T WRITE)

When writing a reference, concept, or hub page **from scratch**, the default is to *not write* unverified content in the first place. Empty sub-sections are the correct state of an honest first draft.

- The temptation to fill a Topic / Theory / Data / Methods / Findings sub-section with "plausible content" or "general knowledge" from training is itself the violation.
- "I'll write something now and verify later" is the failure path. The right path: verify *first* (Layer 1 read), then write only what the source said.
- A 3-section reference page (because that's all you could verify in one read) is correct. A 7-section page with two sections quietly fabricated is the failure mode the whole protocol is built to prevent.

### Scenario B — Editing an existing page (DELETE FIRST)

When reviewing or correcting **content that is already in the body**, the default action is *delete*. Annotations like `(needs verification)`, `(추후 검증)`, `(pending)` are themselves the violation — *the comment is the signal that the content shouldn't be there*.

- When uncertain, delete the sentence. Empty section is correct.
- Never write `(추후 검증)` / `(verification pending)` / `(needs work)` in wiki body. Burden of proof is on retention, not on deletion.
- Don't separate confidence levels in body prose. Confidence belongs in the Verification Metadata sub-section, not in the main body.

**Why both modes matter**: Scenario A blocks the violation at *write-time*; Scenario B catches anything that slipped through, at *review-time*. Without Scenario A, you spend the rest of the wiki's lifetime cleaning up speculative content that should never have entered the body. Without Scenario B, even honest first drafts accumulate stale claims as the field evolves.

**The most subtle failure pattern**: writing a sentence you're not certain about, marking it `(pending)`, intending to come back. You don't come back. Six months later the caveat is invisible in the rendered Obsidian view, the wrong claim is in the main body, you cite it confidently in a paper. Both scenarios above exist to make this failure structurally impossible — Scenario A by preventing the write, Scenario B by mandating immediate deletion when you do encounter the leftover.

---

## Rule 4: Cite Only Papers in references/

**The rule**: Every inline citation in the wiki must point to an existing `references/{stem}.md` file.

**Why**: A citation in prose to a paper that doesn't exist in the wiki is a hidden integrity hole. If you mention "Smith (2010)" in a concept page but `Smith_2010_ASR.md` doesn't exist, no one knows whether the citation is correct. The wiki's self-grounding depends on every citation tracing to a verified summary.

**How to apply**:
- Before citing in prose, check `z_references_index.md` for the filename. If it exists, link. If it doesn't, either ingest the paper first or remove the citation.
- When auto-linkifying prose mentions (`scripts/autolink.py`), the linkifier only creates links to existing files. Unique-match safety prevents wrong-paper links.
- For papers you can't ingest right now: use plain text without claiming citation. "(See also Smith 2010, not yet ingested)" is acceptable as a TODO marker; "[Smith (2010)](non-existent-file.md)" is not.

---

## Rule 5: No Improvisation from Gap

**The rule**: If the wiki has no paper on a topic, say so. *"I don't have a paper on X — please add the PDF."* Never paper-over with general knowledge from training data.

**Why**: Training data is plausible, not verifiable. Sociology especially: LLMs confidently conflate NLSY79 with NLSY97, Lee-Zhou with Sue-Okazaki, the original Card-Krueger 1992 with later replications. These confusions look correct unless you check.

**How to apply**:
- When the user asks a wiki question and the relevant paper isn't ingested, the response is "I don't have this paper, please ingest first" — not "the general literature on X holds that...".
- Concept page narrative sections (`History of Debates`, `Recent Themes`) stay empty until 5+ refs ingested. Don't write them from general knowledge.

---

## Rule 6: Block the Helpful Instinct

**The rule**: When a section feels thin or empty, the instinct to fill it is the moment the violations happen. Resist.

**Why**: The "thin section" instinct is your training as a writer. You learned that empty sections look unfinished. In a wiki for citation accuracy, **empty sections are signals that verification was honest**. Filling them with plausible content is dishonesty disguised as completeness.

**How to apply**:
- When you finish a sentence and feel "I should add more here," ask: is the next sentence verified, or is it filler?
- If it's filler, stop. The section is correctly empty.
- Don't compare section lengths across reference pages. Different papers have different verifiable depth. A 3-line Limitations section reflecting an actual 3-line acknowledgment in the paper is correct; a 30-line "standard limitations" pastiche is wrong.

---

## Rule 7: Volume Is Not the Principle

**The rule**: Short pages are normal when verification is honest. Long pages are warning signs. Don't lengthen a section because it "looks thin." Match length to what the source supports.

**Why**: AI systems and writers both equate "longer" with "better." For a citation-accuracy wiki, the relationship is inverted: a 60-line reference page where every line is verified is more valuable than a 200-line page where half is filler. Volume targets create pressure to fabricate; the only valid driver of length is what the source actually says.

**How to apply**:
- Set no minimum length per section. A Methods sub-section may be three lines if the paper describes the method in three lines.
- Don't compare page lengths across papers. Compare *verifiability* across papers.
- When tempted to lengthen, ask "is the next sentence from the source, or am I supplying it?" If supplied, stop writing.
- Long pages should be conspicuous. When a reference page exceeds typical length, audit it for filler in Findings, Limitations, and Theoretical Framework — those are where bloat hides.

---

## Rule 8: No Binary Plausibility Labels

**The rule**: Never grade unverified content as "likely true," "probably correct," "plausible," or any similar binary label that splits the difference between verified and unverified. Verify it (move to body) or delete it (leave blank). The gray zone is the failure mode.

**Why**: Once a "probably true" sentence sits in the body, it's indistinguishable from a verified sentence to anyone who comes back later. The qualifier disappears in rendering, in copy-paste into a paper, in the wiki's RAG output. Plausibility labels create the illusion of epistemic transparency while functioning as covert assertions.

**How to apply**:
- Forbidden phrasings in wiki body: "(likely)", "(probably)", "(plausible)", "(reasonable estimate)", "(typical for this kind of study)", "(approximately)", "(rough order)".
- If you find yourself reaching for one of these, that's the signal the fact isn't verified. Delete the sentence.
- The Verification Metadata sub-section is the only place where confidence is graded — and even there, the grades are factual (which layer was used, what page was read), not probabilistic.

---

## Rule 9: Per-Sentence Self-Interrogation

**The rule**: Before keeping a sentence in a reference summary, ask: "is every fact in this sentence verified?"

**Why**: Bulk verification at the end doesn't work — you forget which sentences you were sure about. Per-sentence verification catches violations at the source.

**How to apply**:
- After writing each sentence in the Data, Methods, and Findings sections, re-read it. Ask: "what specific claims am I making here? Are they all in the source?"
- If a sentence has 4 verified claims and 1 inserted ("...mediated by socioeconomic background"), and the source doesn't say "mediated by socioeconomic background", **delete that phrase**. Don't keep the sentence with the inserted phrase.
- Findings sections especially: each finding's coefficient, p-value, sample size, condition must be in the source. No approximation.

---

## Rule 10: Layer 1 Fragments Don't Count

**The rule**: A `.md` conversion that's only JSTOR headers, watermarks, OCR scramble, or a fragment is **not** Layer 1 success. Treat as Layer 1 unavailable, escalate to Layer 2.

**Why**: Sparse Layer 1 looks identical to successful Layer 1 unless you check. The conversion produced *something*, you read the something, you assumed Layer 1 success. The something was a footer page.

**How to apply**:
- For each conversion, check: `wc -l papers/papers_md/{stem}.md` (should be 500-3000 lines), `grep -c "^## " papers/papers_md/{stem}.md` (should be 5-15 sections), `head -50 papers/papers_md/{stem}.md` (should be paper introduction, not bibliography or watermark).
- If any check fails, treat as Layer 1 unavailable and escalate to Layer 2.
- Document the conversion failure in Verification Metadata: "Layer 1 unavailable — conversion broken (40 lines JSTOR header only)."

---

## Rule 11: Per-Ingest Verification Metadata

**The rule**: Every reference page ends with a Verification Metadata sub-section. Without it, the page is suspect.

**Why**: The metadata is the *audit trail*. A page with `## Verification Metadata: Layer 1 full read [YYYY-MM-DD]` is trustworthy in a way that an undated unsigned page isn't.

**How to apply**:
- Every new reference page includes Verification Metadata before save.
- When you re-verify (e.g., during lint), update the `Last verification` field.
- Wiki lint flags reference pages without Verification Metadata as needing re-verification.

---

## Rule 12: Unverifiable = Blank, Not Best-Guess

**The rule**: When Layers 1-3 all fail to verify a fact, the wiki section stays empty. Not "best guess from training data", not "(approximately X)", not "(typical value for this type of study)". Empty.

**Why**: Plausible filler is the highest-frequency hallucination source. It looks correct (because it's plausible), it propagates (because it's correct-looking), it can't be corrected (because the reader has no signal it's a guess).

**How to apply**:
- Empty Limitations section because the paper has no explicit limitations? Correct.
- Empty robustness check entry because the paper doesn't show robustness checks? Correct.
- Empty mechanism interpretation because the paper doesn't propose one? Correct.
- The reader (often future you) needs to be able to trust the wiki. Empty means "not in the source"; filled means "in the source".

---

## How These Rules Get Enforced

### At write-time (during ingest)

- Claude reads the rules at every session start (`CLAUDE.md`). Each rule is a hard check.
- Don't-write-first (Rule 3, Scenario A) blocks fabrication at the moment of typing.
- Per-sentence self-interrogation (Rule 9) catches what slips through at the sentence level.
- Empty sections are explicitly *kept empty* per Rule 12. Helpful-instinct block (Rule 6) and volume-is-not-the-principle (Rule 7) reinforce this.

### At save-time

- Caveat-word grep (Rule 3 Scenario B, Rule 8) — search the diff for `(pending)`, `(needs)`, `(추후)`, `(향후)`, `(likely)`, `(probably)`, `(plausible)`, `(approximately)`. Any match means the related content must be verified or deleted, not committed.
- Verification Metadata required (Rule 11) — checked before commit.

### At lint-time (periodic)

- Wiki lint script runs 11 checks (see `docs/WORKFLOWS.md#lint`):
  - References without Verification Metadata flagged
  - References with caveat words or plausibility labels in body flagged
  - References without Layer 1 status flagged
  - Theme/type vocabulary drift flagged
  - Cross-page contradictions flagged

### Adversarial self-review (after the page feels "done")

After self-check, run a *separate* verification pass with an explicit mandate: "find the violations" — not "confirm the page is done."

- The completion instinct hides violations. A self-check that's looking for *completion* will not find what's wrong; it will find reasons the page is fine. A separate adversarial pass reframes the question.
- Concretely: re-read the page from the top with the assumption that *something is wrong*. Compare every specific magnitude, citation, dataset name, and attribution against the source. The goal is to find at least one violation. If you find none after a strict pass, the page is genuinely converged.
- For high-stakes pages (canonical references cited often), spawn a separate Agent or a fresh prompt session with the mandate phrased adversarially. Same-session self-check carries the same confirmation bias as the original write.
- This is not a separate rule — it's the *enforcement procedure* for Rules 1, 3, 6, 7, 8, 9, and 12. Without it, those rules drift toward "I checked, looks fine" rather than "I verified, no violations remain."

### At git-commit time

- Pre-commit hook (optional) runs the lint subset on changed files.
- Hooks can block commits with caveat words or missing Verification Metadata.

---

## The Twelfth-Rule Test

The strictest test of whether you're applying the rules:

> If your wiki had to be audited by a hostile reviewer who would check every single citation and quote against the source, would you stand by every page?

If yes, the rules are working. If you're nervous about specific pages, those pages need re-verification.

The wiki is the *break point* in the citation chain (Philosophy doc, Pillar 1). The break point only works if it's airtight. The twelve rules are what keep it airtight.
