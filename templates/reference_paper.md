# Reference Paper Template

Use for: peer-reviewed journal articles. For books, see [`reference_book.md`](reference_book.md).

**File location**: `references/{stem}.md` where stem is `{LastName}_{YYYY}_{JournalAbbr}.md` (single author), `{LastName1}_{LastName2}_{YYYY}_{Journal}.md` (two), or `{FirstAuthor}_etal_{YYYY}_{Journal}.md` (3+).

```markdown
---
type: paper
year: YYYY
authors: [LastName1, LastName2]
journal: ASR
themes: [Stratification, Education]
projects: [your_active_project]
theories: [theory_slug_1, theory_slug_2]
---

# Author1 and Author2 (YYYY) Full Paper Title

#type/paper #theme/Stratification #journal/ASR #theory/theory_slug_1

**Bibliography**: Author, FirstName, and FirstName Coauthor. YYYY. "Title." *Journal* Vol(Issue):pp-pp.

## Topic

Two to three sentences. What the paper studies; why it matters in the field; the puzzle or gap it addresses.

## Key Theory / Framework

Do not list theories — describe how each is applied. If hypotheses are derived from a theory, state them:

> Theory X predicts Y; the authors test this by [specific method/variable].

Multiple theoretical strands get separate paragraphs. Note where the paper *primarily* sits theoretically (which tradition).

## Data & Methods

Specifications:
- **Data source**: exact name (NLSY79 not "NLSY", ECLS-K not "ECLS")
- **Country/region**: as stated by authors
- **Time period**: years/waves
- **N**: exact (not "approximately")
- **Unit of analysis**: person / household / firm / county / etc.
- **Dependent variable(s)**: precise definition
- **Key independent variables**: precise definitions
- **Controls**: list the substantive ones (not "standard demographic controls" — say what)
- **Method**: name the technique. For DID/IV/RDD/PSM/multilevel/Heckman, the identification assumption.
- **Identification strategy**: if causal, what variation is being exploited?

For complex methods (DID, IV, decomposition), explain the logic in 2-3 sentences plus the assumption that makes it credible.

## Key Findings

Structure 6-10 findings as sub-section headers. Each finding contains:

- **(a) Specific numbers**: coefficients, effect sizes, N, R², p-value or significance, table or figure reference.
- **(b) Mechanism interpretation**: what do the authors say is going on?
- **(c) Conditional or heterogeneous**: which subgroups, periods, conditions modify the effect?
- **(d) Robustness checks**: which alternative specifications preserve the result?
- **(e) Theoretical implication**: what do the authors think this means for the theory?

The Key Findings section is typically as long as Theory + Data combined. Bullet lists are forbidden — write each finding as a paragraph.

### Finding 1: [descriptive header]

Coefficient β = 0.247 (SE 0.041, p<0.001) in the main specification (Table 2, Model 3, N=24,365). The authors interpret this as [mechanism]. The pattern is stronger in [subgroup] (β = 0.318 vs β = 0.176 in the comparison group; Table 4) and survives [specific robustness check]. They argue this supports [theory implication].

### Finding 2: [next descriptive header]

[Same structure.]

## Relevance to This Project

Your interpretation is allowed *only* in this section. Be specific about:
- Which of your project's research questions this paper informs.
- Which of your hypotheses this paper supports or constrains.
- Which methodological move you'll adapt.

Avoid restating findings — explain how you'll use them.

## Scholarly Conversation

Typed bullets to other wiki references. Vocabulary:
- **builds on** (cites and extends)
- **extended by** (later work develops this)
- **alternative** (different explanation of same phenomenon)
- **critiqued by** (later work disagrees)
- **replicates** (replication study)
- **boundary case** (paper that defines the limits of when this finding holds)

Format:

- **builds on**: [Hirschman & Wong (1986) *SF*](../Hirschman_Wong_1986_SF.md) — earlier cohort baseline for the AAAP pattern
- **extended by**: [Kim (2025) *ASR*](../Smith_2025_Example_ASR.md) — re-examined with 1940 census full-count
- **alternative**: [Lee & Zhou (2015) *AAAP*](../Lee_Zhou_2015_AAAP.md) — community-level hyper-selectivity instead of family-level transmission

If you can't state a typed relationship, omit the bullet — don't pad. Routine in-prose citations to other wiki papers are inline-linked, not duplicated here.

## Verification Metadata

- **Layer used**: Layer 1 — `papers/papers_md/{stem}.md` — full read [YYYY-MM-DD]
  (or: Layer 2 — `papers_web/papers_web_md/{stem}.md` — downloaded from {URL} on [YYYY-MM-DD], version: preprint / accepted / published)
- **Empty sub-sections** (no Layer 1 or 2 coverage of the topic): [list, if any]
- **Last verification**: [YYYY-MM-DD]
```

---

## Discipline Reminders

1. **Source-only rule**: every sentence in the body must trace to the paper. If the paper doesn't say it, don't write it.
2. **No approximations**: "N around 5,000" → "N = 4,892". If you can't get exact, leave blank.
3. **No theory by association**: if Bourdieu isn't cited, don't write "Bourdieusian framework".
4. **No general-knowledge filler**: "standard limitations of cross-sectional design" is the violation pattern — only write what the paper states.
5. **Conditional findings matter**: "the effect is X" hides that the paper found "the effect is X among group Y but not Z". Capture the condition.

## Non-English Papers

Reference summaries always match the source paper's language. A paper in your primary language is summarized in that language; an English paper in English. No mirror at the reference layer — that's reserved for concept pages, project hubs, and claims (and only under Language Policy Option C).

Filenames use the paper's native script when applicable:

```
김저자_2024_한국학술지.md            (Korean)
张三_李四_2023_中国学刊.md            (Chinese)
山田_2022_社会学評論.md              (Japanese)
García_2021_RevistaEspañola.md       (Spanish — Latin with diacritics)
```

Frontmatter `authors:` uses the same script as the filename (`authors: [김저자]`, `authors: [张三, 李四]`, etc.). Theory slugs can stay English (`status_attainment`, `hyper_selectivity`) for cross-language graph consistency, or use your primary language if your wiki standardizes that way. Pick one convention and stay consistent — the wiki lint catches drift.
