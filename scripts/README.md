# Scripts

Maintenance scripts for the wiki. All zero-config, auto-detecting paths, Python 3.10+.

## Script Index

| Script | Purpose | When to run |
|---|---|---|
| [`lint.py`](lint.py) | Wiki Lint — 11 drift checks | Every 5-10 ingests or before push |
| [`autolink.py`](autolink.py) | Auto-linkify prose mentions of wiki papers | After any large ingest or during lint |
| [`index_papers.py`](index_papers.py) | Local RAG indexer (ChromaDB + bge-m3) | After ingest or lint |
| [`diag_ref2ref.py`](diag_ref2ref.py) | Reference-to-reference link graph diagnostic | Periodic, or after autolink |

## Dependencies

```bash
pip install pymupdf4llm chromadb sentence-transformers
```

## Path Detection

Scripts auto-detect wiki root by walking up from `cwd` until a `CLAUDE.md` is found alongside a `references/` directory. Override by setting the `WIKI_ROOT` environment variable to the wiki folder.

Edit the `detect_wiki_root()` function in each script if your filesystem layout differs.

## Lint (11 Checks)

`lint.py` runs these checks, reports findings, optionally auto-fixes safe ones:

1. **Project folder validity** — every `projects/{year}/{name}/` corresponds to a real research folder (not stale)
2. **Orphan references** — every `references/*.md` is registered in `z_references_index.md` AND referenced by at least one project's `references.md`
3. **Journal year ordering** — each `journals/*.md` has years in descending order
4. **Index synchronization** — `references/` directory matches `z_references_index.md`
5. **Frontmatter coverage** — every reference page has YAML frontmatter
6. **Tag taxonomy drift** — `#theme/*` and `#journal/*` consistent (CamelCase or snake_case, one or the other)
7. **Type field consistency** — no `book_chapter` vs `book-chapter` drift
8. **Cross-page contradictions** — same paper described inconsistently across pages
9. **Stale "recent research" claims** — category pages calling 5+ year old papers "recent"
10. **Ref→ref link audit** — prose mentions of other wiki papers should be markdown-linked (autolink candidates)
11. **Data gap detection** — papers cited 3+ times in project bibliographies but not ingested

Output: structured report with file paths and specific issues. Safe auto-fixes (tag casing, type unification) applied; manual fixes flagged.

## Autolink

`autolink.py` scans `references/*.md` for "Author (Year)" prose patterns and converts to markdown links when there's a *unique* match in the wiki. Ambiguous matches (e.g., Card 2001 ILRR vs Card 2001 JLE) are skipped and reported.

Run with `--dry` to preview, without flag to apply.

## RAG Indexer

`index_papers.py` indexes `references/`, `general/`, `projects/`, `journals/`, `claims/`, and key root files into a local ChromaDB collection using BAAI/bge-m3 embeddings. Per-file mtime tracking for incremental processing.

```bash
python scripts/index_papers.py --incremental   # only changed files
python scripts/index_papers.py --full          # all files
python scripts/index_papers.py --full --reset  # wipe + rebuild
```

DB stored at `~/rag_db/chroma/` (outside the wiki folder, machine-local).

## Diagnostic

`diag_ref2ref.py` measures the reference-to-reference link graph density:
- Current baseline (direct markdown links between references)
- Concept-page co-occurrence candidates (papers in same concept's empirical record)
- Prose-mention candidates (Author Year patterns not yet linkified)

Useful for tracking the wiki's *connection* density over time. A wiki with many references but few cross-links is much less powerful than one with the same references and a dense link graph between them.

## Adapting

Each script has a header comment explaining its functions and configuration. For different domains, customize:
- **Field/journal lists** in `lint.py` (which journals count as "tracked")
- **Tag namespace conventions** in `autolink.py` and `lint.py`
- **Theme vocabulary** in `lint.py` taxonomy drift check

The accuracy disciplines (Layer 1-4 verification, source-only rule) are not script-enforced — they're agent-enforced via CLAUDE.md instructions. The scripts catch *structural* drift.
