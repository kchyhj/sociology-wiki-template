# Sociology Research Wiki

A complete LLM-assisted research wiki system for sociologists, optimized for **citation accuracy** over token efficiency or (AI-judged) document completeness. Captures literature notes, atomic claims, concept pages, project hubs, and the disciplines that keep them from drifting into hallucination.

The template is carefully built, but turning it into a working personal wiki still requires substantial additional setup and ongoing verification. Treat any suggestion that promises a shortcut around that work as untrue.

Adapted from [Karpathy's LLM Wiki](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285) and [joonan30's adaptation](https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959), with two additions that mattered for our use case:

1. **Three-layer source verification protocol** — every fact in the wiki passes through *local primary source → web-downloaded primary PDF → leave blank*. Secondary sources (reviews, textbooks, abstracts, Wikipedia, AI summaries) are categorically excluded.
2. **Atomic claims layer** (Ahrens-style permanent notes) — separates *source-faithful summaries* from *your synthesized voice*.

The system runs as a Claude Code project. The wiki is plain markdown + Obsidian-compatible. Skills, memory, and scripts are bundled.

**Language**: three configurations supported — English-only (default), single non-English language (your primary language throughout), or **your-language + English mirror** (primary language with English mirror after `---` divider, useful for bilingual readers and English-speaking collaborators). Pick in [`CLAUDE.md`](CLAUDE.md) → Language Policy. Templates show Korean as a worked example; substitute your language anywhere Korean appears. Reference summaries always match the source paper's language.

**한국어 문서**: 본 시스템의 핵심 문서 한국어판 — [`README.ko.md`](README.ko.md) (개요), [`PHILOSOPHY.ko.md`](PHILOSOPHY.ko.md) (설계 근거), [`QUICKSTART.ko.md`](QUICKSTART.ko.md) (셋업·인제스트·린트 절차 상세).

---

## Why This Exists

The general problem: LLM-assisted wikis hallucinate citations. The well-known patterns — "Smith (2010) showed X" when no such paper exists, NLSY79 confused with NLSY97, coefficient `0.110` summarized as "about 50%" — propagate silently. In sociology this is especially damaging because:

- **Citation chains are long.** A wrong attribution in your wiki shows up in your lit review, then in your published paper, then in someone else's lit review citing yours.
- **Lit reviews compound.** What gets in the wiki becomes what you cite *for years*.
- **Quantitative shorthand is dangerous.** "Effect sizes were modest" hides whether the coefficient was 0.05 or 0.5.
- **Theory attribution drifts.** "Hyper-selectivity is a cultural theory" sounds plausible until you realize Lee-Zhou explicitly *opposes* the cultural framing.

The system is designed for sociologists doing theory-grounded quantitative research — the kind of work where a single dataset-name confusion or fabricated coefficient can propagate through a multi-year project arc. It assumes you publish in mainstream sociological journals where citation accuracy is reviewer-scrutinized, read papers at a volume where LLM assistance becomes necessary, and care about your wiki being trustworthy as your *own* downstream citation source.

The verification protocol and binding rules are the response to the failure mode this system addresses: a single ingestion error (e.g., a paper's data section filled with plausible-but-fabricated content) can cascade into multiple downstream errors that take months to detect and correct. The procedures here are intended to prevent that cascade at the wiki layer.

### A note on the trade-off

This design prioritizes **citation accuracy over speed and token economy**. AI systems have a strong bias toward efficiency, and every plausible efficiency move — skimming the paper instead of reading it, summarizing from the abstract, batching ingestion, accepting "looks reasonable" output without verification — turns into a hallucination downstream. The trade-off is deliberate: each paper takes longer to ingest and consumes more LLM context, but what enters the wiki is verifiable. If a workflow change would save time at the expense of verification depth, the answer is no.

---

## What's In This Repository

| Folder | Purpose |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Main Claude Code routing — instructions Claude reads on every session |
| [`PHILOSOPHY.md`](PHILOSOPHY.md) | Design rationale: why accuracy-first, why 5 note layers, why this folder structure |
| [`QUICKSTART.md`](QUICKSTART.md) | 10-minute setup for a new researcher |
| [`docs/`](docs/) | Core documentation (note hierarchy, verification protocol, accuracy rules, workflows) |
| [`templates/`](templates/) | Markdown templates for every note type (reference, concept, claim, project, category) |
| [`memory/`](memory/) | Persistent memory entries (feedback rules, references, projects) with examples |
| [`indexes/`](indexes/) | Master index file templates (author index, concept/theory/method index, master reference list) |
| [`scripts/`](scripts/) | Maintenance scripts: lint, ref→ref auto-linkifier, RAG indexer, link graph diagnostic |

---

## The Five Layers of Notes

This is the central design commitment. Each layer has a single voice; mixing the voices is the most common failure mode in single-layer wikis.

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 5 — Index hubs (index.md, index_authors, index_detail) │
│ Structure: navigation, dedup, status                          │
├──────────────────────────────────────────────────────────────┤
│ Layer 4 — Project hubs (projects/{year}/{name}/)             │
│ Voice: yours, project-bounded                                 │
├──────────────────────────────────────────────────────────────┤
│ Layer 3 — Atomic claims (claims/)                            │
│ Voice: yours, synthesized — Ahrens permanent notes            │
├──────────────────────────────────────────────────────────────┤
│ Layer 2 — Concept notes (general/{category}/)                │
│ Voice: neutral, scholarly — definition + empirical record     │
├──────────────────────────────────────────────────────────────┤
│ Layer 1 — Literature notes (references/)                     │
│ Voice: authors' — source-faithful, never your interpretation  │
├──────────────────────────────────────────────────────────────┤
│ Layer 0 — Raw sources (papers/papers_md/*.md from PDFs)               │
│ Read-only, never edit                                         │
└──────────────────────────────────────────────────────────────┘
```

The architectural rule: claims (Layer 3) build on concepts (Layer 2) which build on references (Layer 1). Never the reverse. A reference summary never imports interpretation from a claim; a claim never silently rewrites what a reference says about itself.

Rationale for the 5-layer structure: [`PHILOSOPHY.md`](PHILOSOPHY.md) → "Why Five Layers, Not Three". Templates for each layer: [`templates/`](templates/).

---

## The Three-Layer Verification Protocol

Every factual claim in the wiki — dataset name, sample size, regression coefficient, citation lineage, theoretical attribution — passes through this protocol *before* it gets written:

```
Layer 1 — LOCAL PRIMARY SOURCE
   Read the paper itself. PDF in papers/ + pymupdf4llm conversion at papers/papers_md/{stem}.md.
   ↓ conversion broken (empty/scan/garbage)
   OCR recovery: re-extract with ocrmypdf or equivalent (still Layer 1)
   ↓ OCR also fails or PDF unavailable
Layer 2 — WEB-DOWNLOADED PRIMARY SOURCE
   Find the paper's PDF on the web, download to papers_web/{stem}.pdf, convert,
   then treat as primary source. ONLY the paper's own PDF — no abstracts, no review summaries.
   ↓ conversion broken
   OCR recovery: re-extract with ocrmypdf or equivalent on the downloaded PDF
   ↓ OCR also fails or paper PDF cannot be obtained anywhere
Layer 3 — LEAVE BLANK
   The wiki section stays empty. Better empty than fabricated.
```

**Hard rules:**
- No "verification pending" caveats. Verify now or delete now.
- No skipping layers because the primary is hard to read. Broken conversion → try OCR recovery on the same PDF first; only escalate to Layer 2 if OCR also fails.
- A `.md` conversion that's just JSTOR headers and footnotes is **not** Layer 1 success.
- **No secondary sources at any layer**: reviews, textbooks, abstracts, Wikipedia, Google Scholar snippets, AI summaries — all categorically excluded.
- Layer 2 web access is *only* for obtaining the paper's full-text PDF, nothing else.
- Layer 2 downloads are stored in a parallel folder structure (`papers_web/` + `papers_web/papers_web_md/`) for audit and provenance.
- **OCR is a recovery step, not a layer.** It re-extracts text from the same PDF when the default conversion fails; the source's primary-source status is preserved.

Full explanation: [`docs/VERIFICATION_PROTOCOL.md`](docs/VERIFICATION_PROTOCOL.md).

---

## The Twelve Binding Rules

The verification protocol is reinforced by twelve operational rules. Claude loads these from `CLAUDE.md` at every session start and applies them as hard checks during ingestion. They cluster into **source discipline** (1–6, what content is allowed) and **operational discipline** (7–12, how to verify and self-check).

### Source discipline (1–6)

1. **Source-only summarization**: write nothing that isn't in the paper, even if the connection seems obvious.
2. **Three-layer verification before writing**: local primary source → web-downloaded primary PDF → leave blank. Each layer's source is read **in full** — abstracts, skims, and snippet-based summaries are not verification. Secondary sources (reviews, abstracts, Wikipedia, AI summaries) are categorically excluded.
3. **Don't write / Delete first** (two scenarios): when *drafting* a new page, don't write unverified content in the first place. When *editing* an existing page, unverified content is deleted, not annotated with `(needs verification)`.
4. **Cite only papers in `references/`**: inline citations must point to existing wiki files. If `Smith_2010_ASR.md` doesn't exist, ingest it first or remove the citation.
5. **No improvisation from gap**: "I don't have a paper on X — please add the PDF" beats fabricating from training data.
6. **Block the helpful instinct**: "this section feels thin" is the moment violations happen. Thin is correct.

### Operational discipline (7–12)

7. **Volume is not the principle**: short pages are normal; long pages are warning signs. Match length to what the source supports — don't lengthen because a section "looks thin."
8. **No binary plausibility labels**: never grade unverified content as "likely true," "plausible," or "approximately X." Verify (move to body) or delete (leave blank). The gray zone is the failure mode.
9. **Per-sentence self-interrogation**: each sentence must answer "is every fact in this sentence verified?" If any claim is uncertain, the sentence comes out.
10. **Layer 1 fragments don't count**: a `.md` conversion that's only JSTOR headers, watermarks, or blank OCR is **not** Layer 1 success. Escalate to Layer 2.
11. **Per-ingest verification metadata**: every reference page ends with a Verification Metadata sub-section noting which layers were used and what was confirmed.
12. **Unverifiable = blank, not best-guess**: training-data plausibility is not verification.

Full explanation with operational examples: [`docs/ACCURACY_RULES.md`](docs/ACCURACY_RULES.md).

---

## Memory System

Persistent memory entries that survive across Claude Code sessions. The memory captures:

- **Feedback rules**: corrections you've given Claude that should never need repeating ("don't add unverified citations", "don't use 'task' for research aim", "this user prefers concise responses")
- **Project context**: what's in flight, deadlines, why a decision was made (with absolute dates, not "Thursday")
- **References**: external systems (Linear projects, Slack channels, Grafana dashboards) and what they're authoritative for

Examples included in [`memory/examples/`](memory/examples/) demonstrate the patterns: rule + **Why** + **How to apply**. Mature memory systems accumulate dozens of entries over months of corrections; the examples here are representative starting points.

---

## Indexes — The Wiki's Spine

Seven master index files that prevent drift as the wiki accumulates literature notes:

- `index.md` — Project status by category (master navigation)
- `index_authors.md` — Every author alphabetical (with dedicated sections for non-Latin scripts)
- `index_detail.md` — Every concept, theory, method (alphabetical, with cross-references)
- `z_references_index.md` — Every reference filename (prevents duplicate ingests)
- `z_ingest_history.md` — Per-project ingest timestamps (incremental processing)
- `log.md` — operations log in a standard format (`## [YYYY-MM-DD] op | title` for grep-friendly history)

Worked skeletons of all seven files in one place: [`indexes/SKELETON_EXAMPLES.md`](indexes/SKELETON_EXAMPLES.md).

The two `z_*` files exist because **dedup-on-write is too late** — a duplicate Smith_2010_ASR.md slightly differing from the canonical one is a citation-disaster waiting to happen.

---

## Scripts

| Script | Purpose |
|---|---|
| [`scripts/lint.py`](scripts/lint.py) | Wiki Lint — 11 drift checks (orphan refs, journal year ordering, frontmatter coverage, tag taxonomy drift, type field consistency, cross-page contradictions, stale claims, prose mention auto-link audit, data gap detection) |
| [`scripts/autolink.py`](scripts/autolink.py) | Auto-linkify prose mentions of other wiki papers (Author Year → markdown link, with unique-match safety) |
| [`scripts/index_papers.py`](scripts/index_papers.py) | Local RAG indexer (ChromaDB + sentence-transformers/bge-m3), incremental, content-hashed dedup |
| [`scripts/diag_ref2ref.py`](scripts/diag_ref2ref.py) | Link graph diagnostic — baseline, concept co-occurrence candidates, prose mention recovery |

All scripts are zero-config: detect OneDrive/home root automatically, work on Windows/Mac/Linux, no external service dependencies.

---

## RAG — Local Semantic Search

The wiki ships with a local RAG indexer ([`scripts/index_papers.py`](scripts/index_papers.py)) so you can search across references, claims, concepts, projects, and journals semantically. Everything runs on your machine — no external API, no data leaves the device.

### What gets indexed

- **By default**: `references/`, `claims/`, `general/`, `projects/`, `journals/`, plus the four root index files (`index.md`, `index_authors.md`, `index_detail.md`, `books.md`).
- **Excluded**: `log.md`, `z_ingest_history.md`, `z_references_index.md` — operational files, noise in semantic search.
- **Optional**: raw paper conversions in `papers/papers_md/` and `papers_web/papers_web_md/`, gated behind `--include-raw`. Off by default because the wiki summaries are already source-faithful distillations and raw conversions inflate the index without proportional retrieval gain.

### Storage and model

- ChromaDB (SQLite-backed) at `~/rag_db/chroma/` — outside the wiki folder, machine-local. Intentionally not synced via git or OneDrive; each machine indexes itself.
- Embedding model: `BAAI/bge-m3` via `sentence-transformers`. Cross-file batching (256 chunks), content-hash dedup, `max_seq_len=2048` to cap attention memory.
- The DB is a derived artifact — losing it just means re-running `--full` once.

### Running indexing

```bash
python scripts/index_papers.py --incremental   # only files changed since last run
python scripts/index_papers.py --full          # full scan (mtime-aware within full)
python scripts/index_papers.py --full --reset  # wipe DB and rebuild from scratch
```

`--incremental` is the everyday command; cold-start cost is the embedding-model load (~10–30s depending on hardware), after which only changed files are re-embedded.

### Automation

Indexing is **explicit by design** — the wiki is your source of truth, the index is a navigation cache, and the workflow should reinforce that asymmetry. But re-indexing after every ingest by hand gets tedious. Three patterns, in increasing degrees of automation:

**Claude Code Stop hook (recommended).** Re-index every time a Claude Code session ends. Copy [`.claude/settings.json.example`](.claude/settings.json.example) to `.claude/settings.json` and the hook activates. The Stop hook is gitignored so it's per-user — each machine opts in independently.

**Background job (one-off async).** When you want indexing to run while you keep working in the same session:

```powershell
# PowerShell (Windows)
Start-Process -WindowStyle Hidden pwsh -ArgumentList "-c","python scripts/index_papers.py --incremental"
```

```bash
# Bash (Mac/Linux)
nohup python scripts/index_papers.py --incremental >/tmp/rag.log 2>&1 &
```

**Scheduled (Task Scheduler / cron).** For unattended periodic re-indexing — overkill for most users, but robust if you ingest from multiple machines or via watchers.

### Concurrency safety

`index_papers.py` uses a file-based single-writer lock (`~/rag_db/.index.lock`). Two concurrent indexer processes against the same ChromaDB can corrupt the SQLite store; the lock exits cleanly if another run is in progress, and auto-clears locks older than 6 hours (orphaned from crashed runs). This makes the background and Stop-hook patterns above safe by default — if a Stop hook fires while a previous job is still running, the second one just exits.

### Querying the index

The template ships the indexer, not a query client. Two patterns work:

1. **Direct ChromaDB access from Python** — `chromadb.PersistentClient(path="~/rag_db/chroma")` and query the `research_wiki` collection.
2. **MCP server in front of the DB** — expose the collection as a tool for Claude Code, so RAG search becomes a normal tool call during conversation.

Either way: RAG returns wiki page paths. **Open the page and read it before citing from it.** The snippet RAG hands back is for navigation; the verified content is on disk in the page itself. Skipping the read-the-page step is exactly the failure mode the 12 binding rules exist to prevent.

---

## Sociology-Specific Adaptations

Default categories follow [ASA section divisions](https://www.asanet.org/communities-and-sections/sections/current-sections/):

- stratification, labor_markets, race_ethnicity, immigration, gender_family, political_sociology, education
- Plus methods, theory (cross-cutting)
- Plus area studies (e.g., asian_american, korean_society) — independent axis

Tracked journals (auto-registered on ingest):
- **Sociology**: ASR, AJS, SF, ARS, Dem, RSSM, WO, IMR, JMF, GS, Socius, ESR, BJS, SSR, SMR/SM
- **Adjacent fields**: Econ top-5 (AER, ECMA, JPE, QJE, REStud), PolSci top-5 (APSR, AJPS, JOP, BJPS, CPS), Psych top-5 (ARP, PsychBull, PsychRev, JPSP, PsychSci)
- **Korean**: 한국사회학, 경제와사회

Adapt the category list and journal table for your subfield; everything else is field-neutral.

---

## Comparison With Related Systems

| System | Voice / philosophy | What it adds |
|---|---|---|
| Karpathy's LLM Wiki (2024) | "Stay grounded in actual papers." Pioneered the 3-tier PDF → sources → wiki pattern. | Foundation |
| Ahrens (Smart Notes / Zettelkasten, 2017) | "Permanent notes in your own words." Atomic claims as the value layer. | Inspired our claims/ layer |
| joonan30's adaptation (2025) | "Four rules: no web search, wiki-first answer, re-read PDF, say-I-don't-know." | Response-time discipline |
| **This system** (2026) | Accuracy at ingest-time + claims layer + sociology-specific scaffold. | 3-layer verification, 12 binding rules, 5-layer hierarchy |

For each related system, see the original publications/repos listed in the table above.

---

## Portability — Using With Other AI Agents

**Claude Code is recommended, but the system works with any agent that supports a system-prompt file.**

### What's AI-agnostic

- The wiki itself (plain markdown, Obsidian-compatible)
- All scripts in [`scripts/`](scripts/) — Python, no AI dependency
- The disciplines: 3-layer verification, 12 binding rules, 5-layer hierarchy, source-only rule
- The RAG indexer ([`scripts/index_papers.py`](scripts/index_papers.py)) — local ChromaDB, no external API

### What's Claude-specific (and how to adapt)

| Claude Code feature | Equivalent in other agents |
|---|---|
| `CLAUDE.md` (auto-loaded system prompt) | **OpenAI Codex CLI**: `AGENTS.md` (auto-loaded) · **Cursor**: `.cursor/rules/*.mdc` or `.cursorrules` · **Aider**: `CONVENTIONS.md` (via `--read`) · **Continue**: `.continuerc.json` system prompt field |
| `memory/` + `MEMORY.md` (auto-accumulating across sessions) | No equivalent. Either inject `memory/*.md` contents into the system prompt each session, or move them into the agent's static rules file (Cursor Project Rules, Aider conventions, etc.) |
| `.claude/settings.json` Stop hook (auto re-index on session end) | No direct equivalent in most agents. Alternatives: git `post-commit` hook, OS file watcher (`watchdog`, PowerShell `Register-ObjectEvent`), or Task Scheduler / cron |

### Adapting in 3 steps (e.g., switching to Cursor or Codex CLI)

1. **Copy the system prompt.** `cp CLAUDE.md AGENTS.md` (Codex) or `cp CLAUDE.md .cursorrules` (Cursor). One-time operation; from here the agent loads it automatically.
2. **Decide on memory.** Either (a) append the contents of `memory/examples/*.md` to the system prompt file once, or (b) load them on demand when relevant. Auto-accumulation is lost — you'll add lessons manually when the agent makes a mistake worth recording.
3. **Replace the Stop hook.** Add to `.git/hooks/post-commit`:
   ```bash
   python scripts/index_papers.py --incremental &
   ```
   The lock guard in `index_papers.py` keeps concurrent runs safe.

The scripts (`lint.py`, `autolink.py`, `index_papers.py`, `diag_ref2ref.py`) need no changes.

### Caveat — model instruction-following

The disciplines are written down, but *adherence* depends on the model. The 12 binding rules ask for strong self-restraint ("don't write unverified content; delete what's already there"), which not all models honor equally:

- **Claude (Sonnet / Opus)** — follows long instruction sets, holds to self-restraint rules well. The system was designed against Claude and works most naturally there.
- **GPT-4 / GPT-5 (Codex)** — strong tool use, but more prone to filling blanks with "general knowledge" rather than leaving them empty. Watch for fabricated data set names or sample sizes.
- **Gemini** — middling adherence to long system prompts; improving on tool use.
- **Smaller / local models (GPT-OSS, Llama variants, etc.)** — usually too easily distracted by the prompt-completion instinct to follow rules like "leave the section blank when unverifiable." Not recommended for ingestion work; possibly fine for routine search.

**Recommended verification before committing to a non-Claude agent**: ingest one paper end-to-end and check whether the agent (a) reads the full Layer 1 conversion, (b) leaves unverified sub-sections blank, (c) refuses to invent a citation when one is missing. If any of these fail, the agent isn't suitable for this workflow regardless of how good it is at other things.

---

## Quickstart

The **recommended path**: install [VS Code](https://code.visualstudio.com/) with the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code), open the (empty) folder where you want your wiki to live (e.g., a new folder named `researchwiki`), and paste the following into the Claude Code chat panel:

> "I'd like to set up a research wiki using this template: https://github.com/kchyhj/sociology-wiki-template
> Please walk me through it from cloning to setup — clone the repo into this folder, customize CLAUDE.md for me, create the folder skeleton, and stop to ask whenever you need a decision from me."

Claude clones the template, reads the repo's instructions, prompts you for your details, and runs the setup commands with confirmation. The result is a wiki tailored to your settings in a single session, no manual CLI work required.

If you prefer a manual setup, [`QUICKSTART.md`](QUICKSTART.md) walks through the same steps as commands you can run yourself.

---

## License

MIT (default — edit [`LICENSE`](LICENSE) if you want CC-BY-NC or similar).

The structural pattern is what's portable. The specific category lists, skills, and tooling are starting points to customize.

---

## Acknowledgments

- Andrej Karpathy — original LLM Wiki pattern
- joonan30 — generalization to research domains
- Sönke Ahrens — Smart Notes / Zettelkasten / permanent notes pattern
- Andy Matuschak — evergreen notes vocabulary
- The Claude Code team at Anthropic — Skills + Memory infrastructure that makes the persistence layer work

This system is the result of one researcher redesigning the workflow several times to prevent recurring errors from citation hallucination. Your mileage may vary, but the verification protocol travels.
