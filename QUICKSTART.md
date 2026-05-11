# Quickstart

10 minutes to a working wiki.

---

## Recommended path: VS Code + Claude Code

The easiest way to set this up is to **install [VS Code](https://code.visualstudio.com/) + the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)**, then **open the (empty) folder where you want your wiki to live (e.g., a new folder named `researchwiki`)** as the workspace and **ask Claude to walk you through setup in the chat panel**.

A natural opener:

> "I'd like to set up a research wiki using this template: https://github.com/kchyhj/sociology-wiki-template
> Please walk me through it from cloning to setup — clone the repo into this folder, customize CLAUDE.md for me, create the folder skeleton, and stop to ask whenever you need a decision from me."

Claude will clone the template, read the repo's instructions, prompt you for your name / institution / categories / language policy, run the folder-creation commands, and let you confirm each step before applying. This avoids manual CLI work and produces a wiki tailored to your settings from the first session. Most of the rest of this Quickstart is provided as reference — Claude will handle it conversationally if you let it.

If you prefer to do everything manually, the commands below work standalone.

---

## Prerequisites

- **VS Code** (recommended) + the **Claude Code extension** — or any Claude Code surface (CLI, desktop) if you prefer
- **Python 3.10+** (3.12 recommended)
- **Git**
- **Obsidian** (free, for browsing — optional but strongly recommended; any markdown editor works)

Python packages (install once):
```bash
pip install pymupdf4llm chromadb sentence-transformers
```

These are the **defaults** the bundled scripts use. Equivalent alternatives also work — you can swap freely:

| Default | Alternatives |
|---|---|
| `pymupdf4llm` (PDF→markdown conversion) | `pdfplumber`, `pdfminer.six`, MinerU, Marker, GROBID, Apple's built-in Preview text extraction |
| `ocrmypdf` (OCR recovery for scanned/image-based PDFs) | `pytesseract` directly, `marker`, MinerU, Apple Preview OCR, ABBYY FineReader |
| `chromadb` (local vector store) | `lancedb`, `qdrant`, `weaviate`, FAISS |
| `BAAI/bge-m3` (embedding model) | `bge-large`, `e5-large`, `nomic-embed`, OpenAI/Cohere embeddings |
| `Obsidian` (markdown viewer) | VS Code, Typora, Foam, Logseq, plain editor |
| `Zotero` (reference manager) | Mendeley, Paperpile, JabRef |

The structural commitments (5-layer hierarchy, 3-layer verification, source-only rule, atomic claims) do *not* depend on the tool choices. If you swap tools, update the scripts and templates accordingly; the rules stay the same.

---

## Setup

### Step 1: Clone or copy this template

```bash
# Clone the template into your wiki location
git clone https://github.com/YOUR-USERNAME/sociology-wiki-template my-wiki
cd my-wiki

# Initialize as your own git repo
rm -rf .git
git init
```

### Step 2: Customize CLAUDE.md

Open `CLAUDE.md` in the wiki root. Replace placeholders:

- `YOUR-NAME` → your handle or name
- `YOUR-INSTITUTION` → your affiliation
- `YOUR-CATEGORIES` → primary topic categories you work in
- `YOUR-WIKI-PATH` → absolute path to the wiki folder

Optionally adjust:
- **Language Policy** section — pick one of three configurations: (A) English-only, (B) single non-English language, or (C) your-language + English mirror. See CLAUDE.md → Language Policy
- **Tracked Journals** — add field-specific journals
- **Categories** — adjust the seven defaults for your subdiscipline

### Step 3: Create the folder skeleton

```bash
mkdir -p papers/papers_md papers_web/papers_web_md references claims projects
mkdir -p general/{stratification,labor_markets,race_ethnicity,immigration,gender_family,political_sociology,education,methods,theory}
mkdir -p journals/{Econ,PolSci,Psych}
touch papers/.gitkeep papers/papers_md/.gitkeep papers_web/.gitkeep papers_web/papers_web_md/.gitkeep references/.gitkeep claims/.gitkeep projects/.gitkeep
```

(These commands use bash brace expansion. On Windows, run from Git Bash or WSL. PowerShell users can create the folders manually or via a `New-Item` loop, or just let Claude handle setup via the recommended VS Code path.)

### Step 4: Create root index files

These are the master index files. Create them as empty markdown stubs:

```bash
touch index.md index_authors.md index_detail.md
touch z_references_index.md z_ingest_history.md
touch books.md log.md
```

The templates in `indexes/` show what each should look like once populated.

### Step 5: Create category landing pages

For each `general/{category}/`, create `0_index.md` using `templates/category_0_index.md`:

```bash
for cat in stratification labor_markets race_ethnicity immigration gender_family political_sociology education methods theory; do
  cp templates/category_0_index.md general/$cat/0_index.md
done
```

Edit each `0_index.md` to set the category name and one-line description.

### Step 6: Create claims hub

```bash
cp templates/claim.md claims/example_claim.md  # placeholder for first claim
```

Create `claims/0_index.md` with status sections (Confident / Working / Retired).

### Step 7: Set up Obsidian (optional)

1. Open Obsidian.
2. **Open folder as Vault** → select your wiki folder.
3. Obsidian indexes the folder. Backlinks, graph view, and search work immediately.

Obsidian doesn't modify files — Claude Code remains the primary editor. Obsidian just renders.

---

## First Paper Ingest

Let's ingest a paper end-to-end to verify the system works.

### Step A: Place a PDF

```bash
cp ~/Downloads/some_paper.pdf papers/Smith_2020_ASR.pdf
```

(Adjust the filename to match the actual paper.)

### Step B: Convert

```bash
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/Smith_2020_ASR.pdf')
open('papers/papers_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

Verify the conversion:
```bash
wc -l papers/papers_md/Smith_2020_ASR.md      # 500-3000 lines expected
head -50 papers/papers_md/Smith_2020_ASR.md   # First 50 lines = introduction?
```

**If the conversion is empty or garbage** (typical for scanned/image-based PDFs), try OCR recovery on the same PDF (still Layer 1):

```bash
# ocrmypdf: tesseract-backed, open source; default OCR tool
ocrmypdf papers/Smith_2020_ASR.pdf papers/Smith_2020_ASR.ocr.pdf
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/Smith_2020_ASR.ocr.pdf')
open('papers/papers_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

Re-verify. If OCR output is also garbage, treat Layer 1 as unavailable and escalate to Layer 2: find the paper's PDF on the web, save to `papers_web/{stem}.pdf`, convert to `papers_web/papers_web_md/{stem}.md`, and apply the same OCR-recovery pattern if needed. If neither Layer 1 nor Layer 2 yields readable text, Layer 3 = leave the relevant sub-sections blank.

### Step C: Read

Open `papers/papers_md/Smith_2020_ASR.md` in Obsidian (or your editor). Read it. Note:
- Bibliography line (authors, year, journal, vol, issue, pages).
- Sample size (exact N).
- Dataset name (exact).
- Method (specific).
- 6-10 key findings with exact numbers.

### Step D: Write the reference summary

In Claude Code (or your preferred editor), create `references/Smith_2020_ASR.md` using `templates/reference_paper.md`. Fill in:
- Frontmatter (year, authors, journal, themes, etc.)
- Topic, Theory, Data & Methods, Findings, Relevance, Scholarly Conversation, Verification Metadata
- **Source-only rule applies** — only what the paper says

This is the discipline-test step. If you find yourself writing something the paper doesn't say, stop. Empty section is correct.

### Step E: Update side files

- `z_references_index.md` — add: `Smith_2020_ASR.md | theme:Stratification | projects:[]`
- `journals/ASR.md` — add entry at top of 2020 section
- `general/stratification/0_index.md` — add to "Key Literature"
- `index_authors.md` — add Smith alphabetically
- `index_detail.md` — add new theories alphabetically

### Step F: Log

In `log.md`:
```markdown
## [2026-MM-DD] ingest | Smith_2020_ASR
- new theories added: [list]
- journals/ASR.md updated
```

### Step G: Commit

```bash
git add -A
git commit -m "First ingest: Smith 2020 ASR"
```

---

## File Your First Claim

Open a conversation with Claude Code. Make a synthesized statement combining 2+ of your now-existing references. Claude will offer to file as a claim. Accept.

Or directly create one:

```bash
cp templates/claim.md claims/your_first_claim.md
# Edit the file, fill in the claim
```

Update `claims/0_index.md` Active Claim List → Working.

---

## Run the Lint

```bash
python scripts/lint.py
```

Should report 0 issues for your one paper + one claim. If it reports issues, fix them.

---

## Run RAG Indexer

```bash
python scripts/index_papers.py --full
```

This indexes references/, claims/, general/, projects/, journals/, and key root files. With 2 files (1 reference + 1 claim), it should complete in under 1 minute.

Subsequent runs use `--incremental`:
```bash
python scripts/index_papers.py --incremental
```

The DB lives at `~/rag_db/chroma/` (outside the wiki folder, machine-local — not synced via git or OneDrive). A single-writer lock at `~/rag_db/.index.lock` prevents two indexer processes from corrupting the same DB.

**Want it to run automatically?** Copy [`.claude/settings.json.example`](.claude/settings.json.example) to `.claude/settings.json` to enable the Stop hook — Claude Code will re-index incrementally every time a session ends. The `.claude/settings.json` file is gitignored, so each machine opts in independently.

To run a one-off indexing in the background while you keep working:

```powershell
# PowerShell (Windows)
Start-Process -WindowStyle Hidden pwsh -ArgumentList "-c","python scripts/index_papers.py --incremental"
```

```bash
# Bash (Mac/Linux)
nohup python scripts/index_papers.py --incremental >/tmp/rag.log 2>&1 &
```

See [`README.md`](README.md#rag--local-semantic-search) for the full RAG section: indexing scope, model details, query patterns, and the rationale for keeping RAG navigation-only (never cite from a snippet — open the page first).

---

## Daily Workflow

Once set up, the typical session:

1. Open Claude Code in the wiki folder.
2. Claude reads `CLAUDE.md` automatically.
3. You: "Ingest the paper at `~/Downloads/new_paper.pdf`."
4. Claude: runs the ingest workflow (Workflow doc).
5. You read the source markdown in Obsidian alongside.
6. Claude writes `references/{stem}.md` following source-only rule.
7. You spot-check, ask for refinements.
8. Side files update.
9. Log entry.
10. Commit.

Per-paper time with verified Layer 1 read: 30-45 minutes. That's the trade.

---

## What to Skip Initially

When you're starting:

- **Don't run scripts/autolink.py** until you have 20+ references (otherwise nothing to link).
- **Don't write category narratives** (History of Debates, Recent Themes) until 5+ refs per category.
- **Don't create concept pages** until 3+ refs share a concept.
- **Don't ingest 10 papers in a day**. Per-paper convergence beats throughput.

Build slowly. The discipline matters more than the velocity.

---

## When Something Goes Wrong

| Problem | Solution |
|---|---|
| Conversion is broken (JSTOR header only) | Treat Layer 1 as unavailable, document in Verification Metadata, escalate to Layer 2 (web) |
| Filename conflicts with existing file | Check `z_references_index.md`; existing file gets project tag added, not re-written |
| Lint reports drift you don't want to fix | Add explicit exception in `log.md` with reason |
| Claude wants to write something the paper doesn't say | Stop. Source-only rule. Empty section is correct |
| Obsidian doesn't show the file | Refresh Obsidian; check the file actually saved |
| RAG returns no results | Check `scripts/index_papers.py --rebuild-history`; reindex if needed |

---

## Going Deeper

After your first 5-10 papers:

- Read [`PHILOSOPHY.md`](PHILOSOPHY.md) — understand *why* the rules exist
- Read [`docs/VERIFICATION_PROTOCOL.md`](docs/VERIFICATION_PROTOCOL.md) — the central discipline
- Read [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) — full procedure list
- Set up memory entries (`memory/MEMORY.md`) as you correct Claude's behaviors

After your first 50 papers:

- Start filing claims (Layer 3) actively
- Run lint regularly (every 5 ingests)
- Build out concept pages (3+ refs per concept)
- Cross-link projects via `general/{category}/0_index.md`

After your first 200 papers:

- The wiki is now a real research asset
- RAG returns useful results
- Cross-paper synthesis becomes natural
- Claims accumulate into your research voice

---

## License & Attribution

This template is MIT-licensed. Adapt freely. The accuracy disciplines and 5-layer hierarchy are the portable contributions; everything else is sociology decoration.

If you build on this and share publicly, attribution appreciated but not required.
