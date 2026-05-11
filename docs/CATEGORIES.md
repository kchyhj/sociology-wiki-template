# Categories and Journals

The wiki's category structure and tracked journal list. Customize for your subdiscipline.

---

## Topic Categories (ASA-Aligned)

Default seven categories, anchored on [ASA section divisions](https://www.asanet.org/communities-and-sections/sections/current-sections/). Each has its own folder under `general/` with `0_index.md` as the landing page.

| Category | Folder | Covers |
|---|---|---|
| Stratification | `general/stratification/` | Mobility, inequality, class, status attainment, life-course |
| Labor Markets | `general/labor_markets/` | Wages, employment, occupations, polarization, unions |
| Race & Ethnicity | `general/race_ethnicity/` | Inequality by race, ethnic groups, discrimination, segregation |
| Immigration | `general/immigration/` | Assimilation, integration, second-generation, generation gaps |
| Gender & Family | `general/gender_family/` | Fertility, marriage, gender inequality, household division |
| Political Sociology | `general/political_sociology/` | Far-right, populism, political trust, electoral behavior |
| Education | `general/education/` | Attainment, schooling, credentialism, college choice |

### Cross-Cutting Categories

These exist for methodological/theoretical work that doesn't fit a substantive topic:

| Category | Folder | Covers |
|---|---|---|
| Methods | `general/methods/` | DID, IV, fixed effects, decomposition, multilevel, etc. — substantive *methods* papers (not papers applying methods) |
| Theory | `general/theory/` | Structuration, field theory, social capital, etc. — cross-cutting theoretical frameworks |

### Area-Studies Categories (Independent Axis)

Population/area focus is *orthogonal* to topic. A paper can be in topic + area:

| Category | Folder | Notes |
|---|---|---|
| Asian Americans | `general/asian_american/` | Often pairs with race_ethnicity, education, immigration |
| Korean Society | `general/korean_society/` | Often pairs with stratification, gender_family, political_sociology |
| (Add your area) | `general/{your_area}/` | E.g., `latin_america/`, `east_asia/`, `africa/` |

Frontmatter convention: a paper's primary category is its *topic* category; area categories go in a separate `area_category` field or in the `themes` list.

---

## Tracked Journals

Journals get their own `journals/{Abbr}.md` file listing all ingested papers from that journal, newest-first. When a paper is ingested and its journal is "tracked", the wiki auto-registers it.

### Sociology (Always Tracked)

| Journal | Abbreviation | File |
|---|---|---|
| American Sociological Review | ASR | `journals/ASR.md` |
| American Journal of Sociology | AJS | `journals/AJS.md` |
| Social Forces | SF | `journals/SF.md` |
| Annual Review of Sociology | ARS | `journals/ARS.md` |
| Demography | Dem | `journals/Dem.md` |
| Research in Social Stratification and Mobility | RSSM | `journals/RSSM.md` |
| Work and Occupations | WO | `journals/WO.md` |
| International Migration Review | IMR | `journals/IMR.md` |
| Journal of Marriage and Family | JMF | `journals/JMF.md` |
| Gender & Society | GS | `journals/GS.md` |
| Socius | Socius | `journals/Socius.md` |
| European Sociological Review | ESR | `journals/ESR.md` |
| British Journal of Sociology | BJS | `journals/BJS.md` |
| Social Science Research | SSR | `journals/SSR.md` |
| Sociological Methods & Research | SMR | `journals/SMR.md` |
| Sociological Methodology | SM | `journals/SM.md` |

### Adjacent Fields (Recommended)

| Field | Journals | Path |
|---|---|---|
| Economics top-5 | AER, ECMA, JPE, QJE, REStud + JEP, JEL | `journals/Econ/` |
| Political Science top-5 | APSR, AJPS, JOP, BJPS, CPS | `journals/PolSci/` |
| Psychology top-5 | ARP, PsychBull, PsychRev, JPSP, PsychSci | `journals/Psych/` |
| Field-specific | (e.g., 한국사회학, 경제와사회 for Korean sociology) | `journals/{native_name}.md` |

These get tracked if your work crosses fields. If not (e.g., pure ethnography lab), drop them.

### Adding a Journal to Tracking

When you ingest a paper from a journal not yet tracked, decide:

1. Is this likely to be a recurring ingestion source? → Add to tracked
2. One-off paper? → Leave untracked

Add a tracked journal by:
- Create `journals/{Abbr}.md` with the journal name as H1
- Add entry to CLAUDE.md's tracked journals table
- Add the journal abbreviation to your wiki's reserved `journal` frontmatter values

---

## Standard Abbreviation Table

The abbreviations Claude uses in citations and frontmatter:

| Journal | Abbreviation |
|---|---|
| American Sociological Review | ASR |
| American Journal of Sociology | AJS |
| Social Forces | SF |
| Annual Review of Sociology | ARS |
| Annual Review of Political Science | ARPS |
| Demography | Dem |
| Research in Social Stratification and Mobility | RSSM |
| Work and Occupations | WO |
| International Migration Review | IMR |
| Journal of Marriage and Family | JMF |
| Gender & Society | GS |
| Socius | Socius |
| European Sociological Review | ESR |
| British Journal of Sociology | BJS |
| Social Science Research | SSR |
| Sociological Methods & Research | SMR |
| Sociological Methodology | SM |
| American Economic Review | AER |
| Quarterly Journal of Economics | QJE |
| Journal of Political Economy | JPE |
| Econometrica | ECMA |
| Review of Economic Studies | REStud |
| Journal of Economic Perspectives | JEP |
| Journal of Economic Literature | JEL |
| Journal of Labor Economics | JLE |
| Industrial and Labor Relations Review | ILRR |
| American Political Science Review | APSR |
| American Journal of Political Science | AJPS |
| Journal of Politics | JOP |
| British Journal of Political Science | BJPS |
| Comparative Political Studies | CPS |
| Annual Review of Psychology | ARP |
| Psychological Bulletin | PsychBull |
| Psychological Review | PsychRev |
| Journal of Personality and Social Psychology | JPSP |
| Psychological Science | PsychSci |
| 한국사회학 | (full Korean name in citations and filenames) |
| 경제와사회 | (full Korean name) |

For journals not in this list, use the most common short form. Consistency matters; once you use an abbreviation, stick with it. Wiki lint catches drift.

---

## Customization

For your subdiscipline, edit:

1. **`CATEGORIES.md`** (this file) — adjust the topic categories
2. **`CLAUDE.md`** — update the tracked journals table
3. **`templates/frontmatter_schemas.md`** — update reserved `themes` and `journal` values
4. **`general/{category}/0_index.md`** — create landing pages for each customized category

Don't fragment categories prematurely. Start with the seven defaults. Split a category only when one folder exceeds ~50 reference pages.

---

## Why Two Axes (Topic + Area)

A paper on Korean educational stratification belongs in two places conceptually:
- *Topic*: education / stratification
- *Area*: Korean society

Single-axis categorization forces a bad choice — either put it in education and lose Korea-cross-referencing, or invent a "Korean education" category that becomes a singleton.

Two-axis categorization keeps both:
- Folder placement: `general/education/` (topic primary)
- Frontmatter: `themes: [Education, Stratification, Korea]`
- Linked from: `general/korean_society/0_index.md` "Education" sub-section

The two axes are *independent*. Most papers have one topic and zero areas (single-topic, non-area). Some papers have two areas (comparative). Rare papers have multiple topics + multiple areas.

The single-folder constraint (one paper goes in one folder) means: pick the topic that's most central to the paper's argument. Cross-references handle the rest.
