# Concept Page Template

Use for: theory/concept/method pages that synthesize across multiple references. One concept per file.

**File location**: `general/{category}/{snake_case_slug}.md`. Examples:
- `general/asian_american/hyper_selectivity.md`
- `general/stratification/cumulative_advantage.md`
- `general/methods/difference_in_differences.md`

**When to create**: 3+ ingested references share the concept, OR your active project uses it as a measured construct, OR a section in the category's `0_index.md` has grown past ~200 words.

```markdown
---
type: concept
projects: [proj1, proj2]
theories: [theory_slug]
---

# Concept Name — One-Line Definition

**Category**: wiki/general/{category}
**Related projects**: {projects}

#type/concept #theme/Category #theory/theory_slug

## Definition

The concept's logical structure and causal mechanism. 2-4 paragraphs.

- What phenomenon does the concept explain?
- What causal mechanism does it propose?
- What's the formal statement (if any)?

Cite the originating reference inline: [Author (Year) *Journal*](../../references/{file}.md).

## Internal Variants and Debates

Concepts are rarely monolithic. Document the variants:

| Variant | Mechanism | Originating reference | Verdict |
|---|---|---|---|
| Strong version | [mechanism] | [Author (Year)](path) | [where it holds] |
| Weak version | [mechanism] | [Author (Year)](path) | [where it holds] |
| Critical alternative | [counter-mechanism] | [Author (Year)](path) | [debate state] |

In prose: explain the disagreements between camps. Don't pretend the concept is settled when it isn't.

## Operationalization

How researchers measure this concept in practice:

- **Construct measures**: variables, indices, latent constructs (with reference).
- **Identification strategies**: what design isolates the concept's effect?
- **Common pitfalls**: which measurement choices conflate this concept with others?

## Empirical Record

| Paper | Data/Identification | Result |
|---|---|---|
| [Author1 (Year) *ASR*](../../references/{file}.md) | NLSY79; OLS with school FE | Supported (β = 0.247, p<.001) |
| [Author2 (Year) *AJS*](../../references/{file}.md) | ECLS-K; DID exploiting policy shift | Conditional — holds for subgroup A only |
| [Author3 (Year) *Dem*](../../references/{file}.md) | ACS; PUMA-level | Rejected (no spillover detected) |

Keep this table current with each ingest. The table is the *empirical state of the literature*; concept pages without it are theory-only.

### Notes on the empirical record

[1-3 paragraphs] What's the current state? Where's the consensus, where's the dispute? Which moderating conditions matter? Which methodological choices change the answer?

## Adjacent Theories

How this concept relates to neighboring theoretical work:

- **Superordinate**: [parent theory] — concept is one mechanism within a broader framework
- **Competing**: [alternative concept] — explains the same phenomenon differently
- **Complementary**: [supplementing concept] — joint use enriches the explanation

Include wiki links where the adjacent theories have their own concept pages.

## Methodological Considerations

If the concept has particular methodological requirements:
- Identification strategies that work / don't work.
- Common confounders.
- Data needs.

## Open Questions

What's unresolved? What would adjudicate the debate? Where would new evidence move the field?

## See Also

- [`references/`](path-to-key-ref.md)
- [`general/{category}/{adjacent-concept}.md`](path)
- [`claims/{related-claim}.md`](path) — your synthesized positions touching this concept
```

---

## Discipline Reminders for Concept Pages

1. **Empirical record table is the heart.** Without it, the concept page is empty prose. Every entry is a verified reference.
2. **Synthesis is allowed here, in scholarly voice.** "The literature has converged on X" is fine; "I think X" goes in claims/.
3. **Cite, don't paraphrase.** Every claim about the field is backed by a wiki reference.
4. **Update with each ingest.** When you ingest a new paper that uses this concept, update the empirical record table the same session. Otherwise it drifts.
5. **Don't restate findings.** The empirical record gives the bottom-line result; the underlying paper's reference page has the details.

## When to Split a Concept Page

When a concept page exceeds ~500 lines or its empirical record exceeds ~25 entries:

- Split off sub-pages (e.g., from `cumulative_advantage.md`, split off `cumulative_advantage_education.md` and `cumulative_advantage_wages.md`).
- Keep the parent page as a high-level orientation with links to sub-pages.

## Methodological Concept Pages

For methods rather than substantive theories (`general/methods/{method}.md`):

```markdown
# Difference-in-Differences — Quasi-Experimental Identification of Treatment Effects

## Definition
## Identifying Assumption (Parallel Trends)
## Standard Implementation
## Variants
- Two-way fixed effects
- Event study
- Synthetic DID
- Staggered DID (Goodman-Bacon, Callaway-Sant'Anna, etc.)
## Pitfalls and Common Critiques
## Software
### Stata
[csdid, did_imputation, etc.]
### R
[did, fixest, etc.]
## Applied Examples (from wiki references)
| Paper | Application | Note |
| ... |
```

Methodological concept pages need *software* sections; substantive concept pages don't.
