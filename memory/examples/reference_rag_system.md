---
name: rag_system_docs
description: RAG system documentation. Setup file location; Python version; embedding model; ChromaDB location. Re-indexing commands.
type: reference
---

The wiki's RAG (retrieval-augmented generation) system enables cross-paper search and concept retrieval. Documentation reference.

## Canonical Documentation

```
{your-wiki-root}/RAG_SETUP.md
```

Always check this file first — it's the canonical source for RAG setup, version requirements, and operational commands.

## Default Components

The bundled `scripts/index_papers.py` uses these defaults — substitute alternatives by editing the script:

- **Python**: 3.12 recommended (3.10+ works)
- **Indexer**: `scripts/index_papers.py` in the wiki repo
- **Embedding model**: `BAAI/bge-m3` (multilingual, 8192 max seq length). Swap for any sentence-transformers-compatible model, OpenAI/Cohere embeddings, or self-hosted alternatives.
- **Vector DB**: local ChromaDB stored under `~/rag_db/` on the local machine. Swap for `lancedb`, `qdrant`, FAISS, etc.
- **MCP server** (optional): expose `search_papers` and `list_categories` to Claude Code for in-chat retrieval.

## Indexed Folders

The indexer covers:
- `references/`
- `general/`
- `projects/`
- `journals/`
- `claims/`
- Root files: `index.md`, `index_authors.md`, `index_detail.md`, `books.md`

NOT indexed (intentionally):
- `_claude_tmp/` (working scratch)
- `log.md` (operational)
- `z_*` (operational lookups, not content)

## Operations

### Incremental re-index (after ingest)

```bash
py -3.12 scripts/index_papers.py --incremental --include-raw
```

Processes only files modified since last run (mtime tracking).

### Full re-index (rare)

```bash
py -3.12 scripts/index_papers.py --full --reset
```

Wipes the collection and rebuilds. Use after schema changes or corruption.

### Rebuild history (mtime sync)

```bash
py -3.12 scripts/index_papers.py --rebuild-history
```

Reconstructs the mtime tracking from the current collection. Use when incremental is misbehaving.

## Search

Via Claude Code MCP:
- `search_papers(query, k=10)` — vector similarity search
- `list_categories()` — available filter categories

Via direct ChromaDB:
```python
import chromadb
client = chromadb.PersistentClient(path="~/rag_db/chroma")  # adjust to your DB location
collection = client.get_collection("research_wiki")
results = collection.query(query_texts=["your query"], n_results=10)
```

## Common Issues

| Issue | Fix |
|---|---|
| "Could not detect wiki root" | Set the `WIKI_ROOT` environment variable to your wiki folder, or run from inside it |
| Memory exhaustion during indexing | Reduce `ENCODE_BATCH` from 32 to 16; reduce `MAX_SEQ_LEN` from 2048 to 1024 |
| Indexing takes hours | First-time indexing time scales with wiki size; subsequent incremental runs are seconds |
| Search returns irrelevant results | Re-index after wiki content shift; verify `--include-raw` if needed |
