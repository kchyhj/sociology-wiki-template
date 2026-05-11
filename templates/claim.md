# Atomic Claim Template

Use for: your synthesized position on a single question. One claim per file. Your voice.

**File location**: `claims/{descriptive_slug}.md`. Examples:
- `kr_edu_premium_cohort_divergence.md`
- `culture_nonignorable_asian_american_education.md`
- `agent_structure_dialectic_general.md`

**When to create**: when you state in conversation a position that combines 2+ references in a way none of them states alone. Claude offers; you accept.

```markdown
---
type: claim
author: your_handle
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
themes: [Stratification, Education]
references: [Paper1_Year_Journal, Paper2_Year_Journal, Paper3_Year_Journal]
related_concepts: [concept_slug_1, concept_slug_2]
related_claims: []
projects: [your_active_project]
status: working                    # working | confident | retired
---

# Claim Title — Stated as a Declarative Sentence

#type/claim #theme/Stratification #status/working #author/your_handle

## The Claim

Paragraph 1: state the claim itself. Two to four sentences in your own voice. Cite supporting references inline.

> [Illustrative example]: "The four-year college wage premium has been stable on average since 2000, but the average masks substantial cohort divergence: more recent cohorts show a sharp decline in the bottom quintile of the wage distribution, consistent with the hypothesis that mass college expansion was absorbed by within-tier stratification rather than by overall premium decline ([Author1 2021](../references/Author1_2021_Journal.md); [Author2 2023](../references/Author2_2023_Journal.md))."

Paragraph 2: scope and mechanism. Where does the claim hold? Where doesn't it? What's the mechanism you're committed to?

> [Continued]: "The pattern is sharper in private than public institutions, and sharper in one demographic group than another, suggesting the proximate channel is signaling-via-institution-prestige rather than skill premium per se. This is a structural claim about how expansion gets absorbed by stratification — not a claim about cultural or value shifts."

## Counter-evidence / Limits

Be honest about scope:

- [Paper that constrains the claim](../references/path.md) — finds attenuation only in some sub-groups.
- [Alternative explanation](../references/path.md) — different mechanism (e.g., labor demand shift) that could produce similar pattern.
- Methodological limit: the claim relies on cross-sectional panel data; longitudinal verification within-individual remains open.

## Notes / Use Cases

- 2025_ExampleProject intro paragraph 2 — argumentative move
- Lecture slide for graduate seminar: "Educational stratification" — case 3
- Potential follow-up paper: cohort decomposition of wage premium variance

## Related Claims (Future Splits)

If parts of this claim could become separate atomic claims, note them:

- **Spin-off candidate**: "Mass college expansion is absorbed by within-tier stratification, not by overall premium decline" — a general claim, could be its own atomic claim citing this case as one instance.
- **Spin-off candidate**: "Bottom-quintile wage premium decline is gendered" — narrower empirical claim, would need additional supporting evidence.
```

---

## Status Field Semantics

| Status | Meaning | Citation use |
|---|---|---|
| `working` | Tentative, exploratory. You've synthesized but haven't fully stress-tested. | Use in your own drafts. Do not externally cite. |
| `confident` | Verified across 2-3 independent sources. Used in your published work or repeatedly defended in talks. | Free use in papers, lectures, talks. |
| `retired` | Superseded by later evidence. **File kept** with explicit retirement reason. | Do not cite. The retirement reason is the historical note. |

### Transitions

- `working → confident`: when you've used the claim in a published paper, or stress-tested it across 2-3 additional references that supported it, or successfully defended it in a serious discussion.
- `confident → retired`: when later evidence contradicts the claim. Add a `## Retirement Reason` section explaining what changed; do **not** delete the file.
- `working → retired`: same as above. The file still has historical value (shows your past thinking).

---

## Discipline Reminders for Claims

1. **One claim per file.** If you can't say it in 2 paragraphs, it's two claims. Split.
2. **Prose, not bullets.** Bullets let you avoid synthesis. Prose forces you to commit.
3. **Every citation is verified.** Same Layer 1-4 protocol as references.
4. **Counter-evidence is mandatory.** A claim without limits is a slogan. Include the cases that constrain it.
5. **Status field is required.** Default `working`. Update when conditions change.
6. **First-person allowed.** "I argue", "my reading", "the conclusion I take" — this is the only layer where this voice is legitimate.
7. **Notes section is where reuse plans go.** "I'll use this for Project X" / "Lecture slide Y" — concrete future uses.

---

## Anti-Patterns

Things that look like claims but should be other layers:

### ❌ "Summary of what the field thinks"

> "The literature has converged on the view that selection explains most of the Asian American advantage."

This is a *concept page* statement, not a claim. It's not your synthesis; it's a description of where the field is. Goes in `general/asian_american/hyper_selectivity.md`'s empirical record narrative.

### ❌ "Description of a single paper's finding"

> "Hsin & Xie (2014) find academic effort explains 75-100% of the Asian American advantage."

This is a *reference page* statement. Goes in the Findings section of `references/Hsin_Xie_2014_PNAS.md`.

### ❌ "Open question / methodological note"

> "We don't really know whether selection or culture is dominant; better identification is needed."

This is not a claim — it's an observation about the field's state. Goes in a concept page's "Open Questions" section, not in claims.

### ✅ "Synthesized position that takes a side"

> "The empirical record after Kim (2025) makes cultural vertical transmission more defensible than community-level hyper-selectivity for explaining the AAAP; I take the cultural-transmission side, with the caveat that 'culture' here means family-level value/expectation transmission rather than ethnic-essentialist content."

This is a claim. It synthesizes (cites multiple papers), takes a side (cultural over community), specifies scope (what kind of "culture"), uses your voice ("I take").

---

## When in Doubt

If you're not sure whether something is a claim:

- Does the substance combine ≥ 2 papers in a way none of them does alone? → claim candidate
- Are you taking a side in a debate? → claim candidate
- Are you describing the field's state? → concept page
- Are you summarizing one paper? → reference page

The litmus test: would the source authors *recognize* their work in your statement? If yes, it's reference-page material. If they'd say "that's an interesting move, but I didn't make it" — that's a claim.
