# Philosophy — Why Accuracy First

This document explains *why* the system looks the way it does. Read it once. The folder structure, the 12 rules, the 3-layer verification protocol — none of them are arbitrary.

---

## The Problem This Solves

LLM-assisted research wikis hallucinate citations. This is well-known. What's less appreciated is **how the hallucination compounds in sociology specifically**:

1. **A wiki lit review feeds a published lit review.** Whatever the wiki says about Smith (2010) ends up in your paper. If Claude misremembered the sample size, *your* paper now says it.
2. **A published lit review feeds five other lit reviews.** Whatever your paper says, the next five authors citing you will repeat. Compounding goes silent and exponential.
3. **A wrong attribution ages quietly.** "Hyper-selectivity is fundamentally a cultural theory" propagates because nobody re-reads Lee-Zhou (2015) to verify the framing — they trust the lit review chain.
4. **Quantitative shorthand strips information.** "The effect was small" hides whether the coefficient was 0.05 or 0.005. After three lit-review hops, *nobody can recover what the original paper showed*.

Sociology is especially vulnerable because:
- Theory disputes are long and subtle (cultural vs structural vs selection explanations of inequality).
- Method names are similar (NLSY79 ≠ NLSY97, ECLS-K ≠ ELS).
- Author names cluster (the wiki has 14 papers by various Lees in Asian American sociology).
- Reviews of reviews are common practice — error doesn't get re-examined, it gets re-cited.

The system's central commitment is to make the wiki the *break point* in this chain. Whatever enters the wiki is verified; what cites the wiki inherits that verification.

---

## The Two Pillars

### Pillar 1: Source-Faithful Summaries

The wiki has one writing mode that is *not* yours: literature notes. When you summarize a paper, the only legitimate content is what the paper says.

This is harder than it sounds. The natural failure mode is:

- The paper has 5 findings; you only have time to capture 3 in detail.
- For the other 2, you remember "they roughly show X-pattern" from skimming.
- "X-pattern" is true of the literature in general, but the specific paper actually shows X-pattern *conditionally*.
- You write the unconditional version.
- A year later, you cite the unconditional version. The author the wiki summarized is now misrepresented.

The fix: **write less, with verified specificity**. Five findings with exact numbers beats ten findings with vague approximations. If you can't verify a number, leave it blank — don't approximate.

### Pillar 2: Your Voice Belongs in Claims

Synthesis is valuable. "Asian American educational attainment cannot be explained by selection alone — the cultural channel is empirically defensible after Kim (2025), Hsin & Xie (2014), and Liu & Xie (2016)" is *worth recording*.

But it doesn't belong in a literature note. It's *your synthesis* — you wrote a position that none of those papers individually wrote. Putting it in the literature note for any one of them would misrepresent that paper.

So it goes in `claims/`. The folder has different rules:
- Your voice (not the authors').
- One claim per file (atomic).
- Cited papers must exist in `references/`, verified.
- Status field tracks confidence (working / confident / retired).

The point: **make the writing mode explicit in the folder structure**. You always know whose voice you're in.

---

## Why Five Layers, Not Three

Most LLM wikis have three layers: PDFs → summaries → wiki articles. Karpathy's original works this way. joonan30's adaptation works this way.

We need five because sociology has more distinct writing modes:

| Layer | Folder | Voice | Why a distinct layer |
|---|---|---|---|
| 0 — Raw sources | `papers/papers_md/` | Author (verbatim) | Read-only. The pymupdf4llm conversion. Never edit. |
| 1 — Literature notes | `references/` | Author (your faithful summary) | Source-only rule applies. One paper, one file. |
| 2 — Concept notes | `general/` | Neutral, scholarly | Defines theory/concept. Empirical record table. Cross-paper. |
| 3 — Atomic claims | `claims/` | **Yours**, synthesized | Your position. Citations to Layer 1 paste-evidence. |
| 4 — Project hubs | `projects/` | Yours, project-bounded | RQ, methods, ongoing notes for *your* active research. |
| 5 — Index hubs | `index.md`, `index_authors.md`, etc. | Structural | Navigation, dedup, status. |

The Layer 2 vs Layer 3 split is the crucial one. Most failures in single-layer wikis come from conflating concept-page synthesis with claim synthesis. A concept page says *what the field has found about X*; a claim says *what you think about X based on what the field has found*. These are different.

---

## Why the Three-Layer Verification

The simple rule "verify your claims" is unimplementable. *How* do you verify? Read what?

The three-layer protocol gives an operational order:

```
Layer 1: Local primary source       (your PDF in papers/, conversion in papers/papers_md/)
   ↓ unavailable / broken / partial
Layer 2: Web-downloaded primary    (find paper PDF on web, download to papers_web/,
                                    convert, treat as primary — NO secondary sources)
   ↓ paper PDF unobtainable
Layer 3: LEAVE BLANK                (better empty than fabricated)
```

The order matters. Layer 1 is authoritative; Layer 2 is the same standard (the paper's own full text) via a different acquisition path. **Don't skip Layer 1 just because it's hard.** A 50-page paper takes 30 minutes to verify properly; that 30 minutes saves you 30 hours of downstream debugging when your lit review breaks.

The non-obvious rule: **Layer 1 fragments don't count**. If the PDF→.md conversion produced 30 lines of JSTOR footers and nothing else, that's Layer 1 *unavailable*, not Layer 1 *success*. Failed conversions look exactly like sparse Layer 1 success unless you check.

**Why no secondary-source tier?** An earlier version had a "secondary distillation" tier (reviews, textbooks, abstract aggregators) between web verification and leave-blank. That tier is removed because review papers compress information — using a review's summary of Smith (2010) as verification means the wiki is two layers removed from Smith. The right alternative when neither Layer 1 nor Layer 2 works is to leave the section blank. The simpler protocol forces a binary outcome: either you read the actual paper, or the section is empty. There is no middle ground where someone else's summary of the paper counts as verification.

---

## Why "Don't Write First / Delete First"

The rule operates in two modes depending on whether you're writing new content or auditing existing content. Both arrive at the same outcome — the body never carries unverified content — but they intervene at different points.

### Mode A — Don't write first (drafting a new page)

The instinct to "write something" — to fill the Topic, Theory, Data, Methods, Findings sub-sections of a new reference page from training-data plausibility — is exactly what produces hallucinations downstream. The fix is to learn to *not write the sentence in the first place* when verification hasn't happened yet.

A reference page with three sub-sections (because those are the three sections of the paper you could verify in one read) is correct. A page with seven sub-sections, two of which were "filled in from general knowledge of this literature," is the failure pattern the whole protocol is built to prevent.

If the impulse to write something arrives before the source is read, the impulse is the violation. Verify *first*, then write only what the source said.

### Mode B — Delete first (auditing existing content)

The most common failure mode in maintenance is the **caveat-as-violation-signal pattern**:

> "Notes: (Sample size may need re-verification — appears to be ~5,000 but I'm not certain.)"

This is *itself* the violation. Here's why:

1. You wrote a number you're not sure of.
2. You annotated it as uncertain.
3. The annotation is in a "Notes" section nobody reads.
4. The number is in the main body where it *will* be cited.
5. Six months later, you cite the wiki, the caveat is invisible, the number is wrong.

**The caveat doesn't fix the violation — it makes the violation comfortable.**

The rule: if a fact isn't verified, delete it. Don't annotate it. The empty section is correct. The "to be verified later" annotation will not get verified later; it will get cited as-if-verified.

### Why both modes

Mode A blocks the violation at the *write moment*. Mode B catches whatever slipped through, at the *read moment*. Without Mode A, you spend the wiki's lifetime mopping up speculative content that should never have entered the body. Without Mode B, even honest first drafts go stale as the field evolves.

The hardest version of this rule to internalize is Mode A — the instinct to fill a thin-looking section is strong, and the fix is to learn that *blank is the correct shape of an unverified section*. Trust the reader (often future you) to read blank as "not yet verified," not as "doesn't exist."

---

## Why a Claims Layer

The Zettelkasten / evergreen-notes tradition (Ahrens, Matuschak) emphasizes that the *value* of a research notebook is the synthesized positions, not the literature summaries. The summaries are *input*. The claims are *output*.

Most academic wikis stop at summaries. They never accumulate the user's voice. The wiki becomes a stale read-only repository — useful for retrieval, useless for thinking.

The `claims/` layer fixes this:

- **Atomic**: one claim per file. Forces synthesis to a defensible scope.
- **Prose**: not bullets. Writing the claim out forces you to know it.
- **Cited**: every claim points to references that support it (and, where applicable, references that constrain or contradict it).
- **Status-tracked**: `working` → `confident` → `retired`. Claims age; you can see which positions you used to hold and what changed.

The compounding effect: every paper you write should produce 3–10 new or updated claims. After two years, you have 200+ atomic positions, each citationally grounded. *That* is what the wiki gives back to you.

---

## Why Sociology-Specific Categories

The wiki could be field-neutral, but the friction of category invention is high. We anchor on [ASA section divisions](https://www.asanet.org/communities-and-sections/sections/current-sections/) — `stratification`, `labor_markets`, `race_ethnicity`, `immigration`, `gender_family`, `political_sociology`, `education` — plus `methods` and `theory` as cross-cutting.

Two crucial choices:
1. **Multi-category routing via frontmatter.** A paper can belong to stratification (primary) and education (cross). The folder is the primary; frontmatter `themes:` carries cross.
2. **Area-studies axis is independent.** `asian_american/`, `korean_society/` are not topic categories — they're cross-cutting populations. A paper can be `race_ethnicity` primary + `asian_american` area.

The journal index (`journals/ASR.md` etc.) is a *parallel* navigation, organized by where the paper was published rather than what it's about. This catches the "what's everyone publishing in ASR right now?" question without needing a separate query system.

---

## What This System Is Not

- **Not for casual reading.** Building this discipline is overhead. If you read 5 papers a month, simpler is better.
- **Not a writing tool.** It's a *literature* tool. The wiki itself isn't your manuscript; downstream writing depends on it but is a separate workflow.
- **Not a knowledge graph.** It has graph properties (paper-to-paper links, concept-to-paper links, claim-to-everything links), but the value isn't the graph — it's the *citations*.
- **Not Zettelkasten.** Closer than Karpathy's pattern but still distinct: Ahrens insists on flat numerical IDs and no folders; we use folders heavily because we have explicit writing modes per folder.
- **Not perfect.** Mature deployments accumulate hundreds of references and dozens of memory rules over months. The system catches hallucinations after they happen, the rules evolve to prevent recurrence. What you adopt here is the state that has survived that iteration — not a finished product.

---

## Final Principle

> When in doubt, **delete and verify**, not **annotate and continue**.

Every rule, every template, every script in this system enforces some version of that. If the verification protocol feels heavy, remember what it's protecting against: a single false NLSY77/NLSY97 confusion in a high-cited paper that propagated through a decade of education sociology before someone noticed.

The wiki should be slower to write than your draft. That's the trade.
