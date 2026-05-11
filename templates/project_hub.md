# Project Hub Template

Use for: an active research project's index page. One per project. Two files per project: `index.md` (this template) and `references.md` (next template).

**File location**: `projects/{YYYY}/{ProjectName}/index.md` where YYYY is the project's start year and ProjectName is a short slug.

```markdown
# Project Title

## Status
- **Status**: [Your tracking convention — e.g., "In progress", "Drafting", "Under review", "Published"]

## Bibliographic Information
- **Authors**: [list]
- **Year**: YYYY (if known)
- **Journal / Venue**: [if applicable]

## Research Question
1-3 sentences. The puzzle the project addresses.

## Theoretical Framework
The theoretical commitment(s) the project makes. Cross-reference concept pages:
- [Concept 1](../../../general/{category}/{concept}.md)
- [Concept 2](../../../general/{category}/{concept}.md)

Argue the framework briefly. What does this theory predict? What would falsify it?

## Hypotheses
Numbered hypotheses, stated explicitly:
- **H1**: ...
- **H2**: ...
- **H3** (conditional): ...

## Data
- **Source**: dataset name (e.g., NLSY79, PSID, GSS, BHPS, SOEP — or a domain-specific dataset such as KLIPS, KGSS for Korea)
- **Period**: years/waves
- **Sample**: target population, exclusions, final N
- **Variables**: DV, key IVs, controls

## Methods
- Identification strategy
- Estimation technique
- Robustness checks planned

## Findings (Current State)
What's been confirmed; what's open. This section is *iterative* — update as analyses complete.

### Confirmed
- [Finding 1]: [evidence]
- [Finding 2]: [evidence]

### Open
- [Open question 1]
- [Open question 2]

## Notes
Date-stamped notes on decisions, debates, references that surfaced:
- **YYYY-MM-DD**: [decision or note]
- **YYYY-MM-DD**: [decision or note]

## Related Resources
- [`references.md`](references.md) — project bibliography
- Active claims: [list of `claims/{slug}.md` files relevant to this project]
- Active concept pages: [list of `general/{category}/{concept}.md` files]

---

# [Project Title in your primary language]

(Optional **your-language mirror**, identical structure. Use only if your wiki follows
Language Policy Option C — your-language + English. Substitute any non-English language;
Korean shown below as a worked example.)

Korean example:
# 프로젝트 제목
## 상태
- **Status**: In progress
## 연구 질문
...

[etc.]
```

---

## Multi-Project Discipline

When the project hub gets long (>300 lines), consider:

- Move detailed notes to a `notes.md` in the same folder.
- Move detailed analysis logs to `analysis_log.md`.
- Keep `index.md` as overview + cross-references.

Don't split too eagerly — a project hub with all-in-one structure is easier to read than five sub-files.

---

## Category Routing

Each project has a primary category (one of stratification, labor_markets, etc.) and optional cross-categories. Set in frontmatter:

```yaml
primary_category: stratification
cross_categories: [education, race_ethnicity]
```

Or in the project hub's Bibliographic Information block:
```markdown
- **Primary category**: stratification
- **Cross-categories**: education, race_ethnicity
- **Area category** (independent axis): asian_american (if applicable)
```

Multi-category routing means the project will appear under multiple `general/{category}/0_index.md` "Active Projects" lists. Inevitable for cross-cutting work; handled by frontmatter + manual update of category landing pages.
