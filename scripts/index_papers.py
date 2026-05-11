"""
Wiki ChromaDB indexer.

Usage:
    python scripts/index_papers.py --full          # full indexing (incremental within full)
    python scripts/index_papers.py --incremental   # only files modified since last run
    python scripts/index_papers.py --full --reset  # wipe DB + full re-index
    python scripts/index_papers.py --full --include-raw --no-dedupe

The DB is stored machine-local at ~/rag_db/ (or %USERPROFILE%/rag_db/ on Windows).
See docs/WORKFLOWS.md for ingest workflow and scripts/README.md for script usage.

Key implementation notes:
    - Cross-file batching: chunks flushed in batches of 256 (fewer embedding calls)
    - Content-hash dedup: identical-content files share one embedding (helps raw _md/ copies)
    - sentence-transformers direct call: encode batch_size configurable
"""

from __future__ import annotations

import argparse
import atexit
import getpass
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


EMBED_MODEL = "BAAI/bge-m3"
COLLECTION = "research_wiki"

UPSERT_BATCH = 256   # cross-file flush threshold (chunks)
ENCODE_BATCH = 32    # sentence-transformers internal batch_size (safe default)
MAX_SEQ_LEN = 2048   # bge-m3 default 8192 can use 17GB+ attention memory; cap at 2048


def _safe_stat(p: Path):
    """Use \\\\?\\ prefix on Windows so paths exceeding MAX_PATH(260) still stat."""
    s = str(p)
    if sys.platform == "win32" and not s.startswith("\\\\?\\"):
        s = "\\\\?\\" + s
    return os.stat(s)

INDEX_TARGETS = [
    ("references", "references"),
    ("claims", "claims"),
    ("general", "general"),
    ("projects", "projects"),
    ("journals", "journals"),
]

# Root-level master index files (semantic content, useful for RAG queries).
# Operational files (log.md, z_ingest_history.md, z_references_index.md)
# are intentionally excluded.
WIKI_ROOT_FILES = [
    "index.md",
    "index_authors.md",
    "index_detail.md",
    "books.md",
]

# raw *_md folders: paper PDFs converted to markdown, kept alongside the originals
# for ad-hoc inclusion in the RAG. Adapt the RAW_ROOTS list below to your own
# directory layout.
# Add subdirectories of your workspace root that contain converted markdown
# alongside PDFs (typically named `*_md/`). Leave empty if you don't have
# extra paper folders to index beyond the wiki's own papers/, papers/papers_md/,
# papers_web/, papers_web/papers_web_md/.
RAW_ROOTS: list[str] = [
    # "MyPapers",
    # "AnotherFolderWithSubdirsEndingIn_md",
]


def detect_wiki_root() -> Path:
    """Detect the wiki root directory.

    Walks up from cwd looking for a folder with both CLAUDE.md and references/.
    Override by setting WIKI_ROOT environment variable to the wiki root.
    """
    if "WIKI_ROOT" in os.environ:
        p = Path(os.environ["WIKI_ROOT"]).resolve()
        if (p / "CLAUDE.md").exists() and (p / "references").is_dir():
            return p
        sys.exit(f"ERROR: WIKI_ROOT={p} does not contain CLAUDE.md + references/")
    p = Path.cwd().resolve()
    while p != p.parent:
        if (p / "CLAUDE.md").exists() and (p / "references").is_dir():
            return p
        p = p.parent
    sys.exit("ERROR: Could not detect wiki root. Set WIKI_ROOT env var to the wiki folder.")


def db_root() -> Path:
    user = getpass.getuser()
    return Path(rf"C:\Users\{user}\rag_db")


# Stale-lock threshold. A full re-index of a large wiki (thousands of files,
# CPU-only) can take ~1-2h; 6h gives a comfortable margin before we treat a
# leftover lock file as orphaned from a crashed run.
STALE_LOCK_HOURS = 6


def acquire_lock(db_dir: Path) -> Path:
    """Single-writer guard. ChromaDB is SQLite-backed; two concurrent indexer
    processes writing to the same collection can corrupt the DB. This guard
    prevents that — useful when running incremental indexing in the background
    (e.g., via a Claude Code Stop hook, Task Scheduler, cron, or PowerShell
    background job).

    If a lock file exists and is younger than STALE_LOCK_HOURS, exit cleanly.
    If older, treat as orphaned (previous run crashed), remove, proceed.
    Released automatically on normal exit, sys.exit, or unhandled exception
    via atexit.
    """
    lock = db_dir / ".index.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    if lock.exists():
        age_hours = (time.time() - lock.stat().st_mtime) / 3600
        if age_hours < STALE_LOCK_HOURS:
            try:
                pid = lock.read_text(encoding="utf-8").strip()
            except Exception:
                pid = "?"
            print(
                f"[skip] another indexer is running (PID {pid}, "
                f"lock {age_hours:.1f}h old). "
                f"If you're sure it isn't, remove {lock} and retry."
            )
            sys.exit(0)
        print(f"[info] stale lock ({age_hours:.1f}h old) — removing.")
        lock.unlink(missing_ok=True)
    lock.write_text(str(os.getpid()), encoding="utf-8")
    atexit.register(lambda: lock.unlink(missing_ok=True))
    return lock


def load_history(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_history(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def chunk_by_header(text: str, max_chars: int = 2000) -> list[str]:
    """Split by ## headers; further split sections that exceed max_chars."""
    sections = re.split(r"\n(?=## )", text)
    chunks: list[str] = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        if len(sec) <= max_chars:
            chunks.append(sec)
        else:
            for i in range(0, len(sec), max_chars - 200):
                chunks.append(sec[i : i + max_chars])
    return chunks or [text.strip()]


def _safe_read(p: Path) -> str:
    """Long-path-aware read_text for Windows."""
    s = str(p)
    if sys.platform == "win32" and not s.startswith("\\\\?\\"):
        s = "\\\\?\\" + s
    with open(s, encoding="utf-8") as f:
        return f.read()


def file_content_hash(p: Path) -> str:
    """SHA-1 hash of file contents. Used for dedup decision."""
    try:
        text = _safe_read(p)
    except Exception:
        return f"err_{p.name}"
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def build_chunks(md_path: Path, category: str, base_root: Path) -> list[dict]:
    try:
        text = _safe_read(md_path)
    except FileNotFoundError:
        return []
    except UnicodeDecodeError:
        with open(
            ("\\\\?\\" + str(md_path)) if sys.platform == "win32" else str(md_path),
            encoding="utf-8", errors="ignore",
        ) as f:
            text = f.read()

    rel = md_path.relative_to(base_root).as_posix()
    title = md_path.stem

    if category == "references":
        chunks_text = [text.strip()]
    else:
        chunks_text = chunk_by_header(text)

    out = []
    for i, ch in enumerate(chunks_text):
        doc_id = hashlib.sha1(f"{rel}::{i}".encode("utf-8")).hexdigest()
        out.append(
            {
                "id": doc_id,
                "text": ch,
                "metadata": {
                    "category": category,
                    "path": rel,
                    "title": title,
                    "chunk": i,
                },
            }
        )
    return out


def iter_wiki_files(wiki_root: Path):
    for category, sub in INDEX_TARGETS:
        base = wiki_root / sub
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            yield category, p
    for name in WIKI_ROOT_FILES:
        p = wiki_root / name
        if p.exists():
            yield "root", p


def iter_raw_files(wiki_root: Path):
    """Collect .md files from configured RAW_ROOTS (paper folders alongside wiki)."""
    for root_name in RAW_ROOTS:
        root = wiki_root / root_name
        if not root.exists():
            continue
        for md_dir in root.rglob("*_md"):
            if not md_dir.is_dir():
                continue
            for p in md_dir.glob("*.md"):
                yield "raw", p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="full scan")
    parser.add_argument("--incremental", action="store_true", help="incremental scan (only modified files)")
    parser.add_argument("--reset", action="store_true", help="wipe DB before indexing")
    parser.add_argument("--include-raw", action="store_true", help="also index raw *_md/ folders configured in RAW_ROOTS")
    parser.add_argument("--raw-only", action="store_true", help="index only raw files (skip wiki content)")
    parser.add_argument("--no-dedupe", action="store_true", help="disable content-hash dedup")
    parser.add_argument("--rebuild-history", action="store_true",
                        help="rebuild z_index_history.json from existing DB chunks (no re-embedding)")
    args = parser.parse_args()

    if args.rebuild_history:
        wiki_root = detect_wiki_root()
        db_dir = db_root() / "chroma"
        history_path = db_root() / "z_index_history.json"
        acquire_lock(db_root())
        client = chromadb.PersistentClient(path=str(db_dir))
        collection = client.get_or_create_collection(name=COLLECTION)
        all_items = collection.get()
        metas = all_items.get("metadatas", [])
        history: dict[str, float] = {}
        for m in metas:
            if not m:
                continue
            path = m.get("path")
            if not path:
                continue
            full = wiki_root / path
            if full.exists():
                history[path] = full.stat().st_mtime
        save_history(history_path, history)
        print(f"[done] history rebuilt: {len(history)} files")
        return

    if not (args.full or args.incremental):
        parser.error("specify --full or --incremental")

    wiki_root = detect_wiki_root()

    db_dir = db_root() / "chroma"
    history_path = db_root() / "z_index_history.json"
    db_dir.mkdir(parents=True, exist_ok=True)
    acquire_lock(db_root())

    print(f"[info] Wiki root: {wiki_root}")
    print(f"[info] DB:       {db_dir}")
    print(f"[info] Model:     {EMBED_MODEL}")
    print(f"[info] dedup:    {'OFF' if args.no_dedupe else 'ON'}, batch={UPSERT_BATCH}, encode_batch={ENCODE_BATCH}")

    client = chromadb.PersistentClient(path=str(db_dir))

    if args.reset:
        try:
            client.delete_collection(COLLECTION)
            print("[info] dropped existing collection")
        except Exception:
            pass
        history_path.unlink(missing_ok=True)

    collection = client.get_or_create_collection(name=COLLECTION)
    history = load_history(history_path)

    files: list[tuple[str, Path]] = []
    if not args.raw_only:
        files.extend(iter_wiki_files(wiki_root))
    if args.include_raw or args.raw_only:
        files.extend(iter_raw_files(wiki_root))
    print(f"[info] target files: {len(files)} (include_raw: {args.include_raw or args.raw_only})")

    to_process: list[tuple[str, Path]] = []
    for category, p in files:
        key = p.relative_to(wiki_root).as_posix()
        mtime = _safe_stat(p).st_mtime
        prev = history.get(key)
        if args.incremental and prev and prev >= mtime:
            continue
        to_process.append((category, p))

    if not to_process:
        print("[info] no changed files; exiting.")
        return

    print(f"[info] mtime-changed files to process: {len(to_process)}")

    # ------------------------------------------------------------------
    # Dedup pre-scan
    # ------------------------------------------------------------------
    if args.no_dedupe:
        canonical = to_process
        alias_map: dict[str, list[tuple[str, Path]]] = {}
    else:
        t0 = time.time()
        hash_map: dict[str, list[tuple[str, Path]]] = {}
        for category, p in to_process:
            h = file_content_hash(p)
            hash_map.setdefault(h, []).append((category, p))

        canonical = []
        alias_map = {}
        for h, group in hash_map.items():
            # Deterministic canonical pick (sort by path)
            group.sort(key=lambda cp: str(cp[1]))
            canonical.append(group[0])
            if len(group) > 1:
                alias_map[h] = group[1:]

        n_dups = sum(len(v) for v in alias_map.values())
        elapsed = time.time() - t0
        print(f"[info] dedup: {len(canonical)} unique / {n_dups} duplicates skipped ({elapsed:.1f}s)")

    # ------------------------------------------------------------------
    # Model load (sentence-transformers direct)
    # ------------------------------------------------------------------
    print(f"[info] loading model...")
    t0 = time.time()
    model = SentenceTransformer(EMBED_MODEL)
    model.max_seq_length = MAX_SEQ_LEN
    print(f"[info] model loaded ({time.time() - t0:.1f}s, max_seq_len={MAX_SEQ_LEN})")

    # ------------------------------------------------------------------
    # Cross-file batch processing
    # ------------------------------------------------------------------
    batch_ids: list[str] = []
    batch_docs: list[str] = []
    batch_meta: list[dict] = []
    pending_files: list[tuple[str, float]] = []  # (key, mtime) entries to commit to history after flush

    encode_total_time = 0.0
    encode_calls = 0

    def flush() -> None:
        nonlocal encode_total_time, encode_calls
        if not batch_ids:
            return
        t = time.time()
        embs = model.encode(
            batch_docs,
            batch_size=ENCODE_BATCH,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        encode_total_time += time.time() - t
        encode_calls += 1
        collection.upsert(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_meta,
            embeddings=embs.tolist(),
        )
        batch_ids.clear()
        batch_docs.clear()
        batch_meta.clear()
        # Commit flushed files to history
        for k, m in pending_files:
            history[k] = m
        pending_files.clear()
        save_history(history_path, history)

    t_start = time.time()
    for idx, (category, p) in enumerate(canonical, 1):
        key = p.relative_to(wiki_root).as_posix()
        mtime = _safe_stat(p).st_mtime
        # Delete existing chunks (avoid dupes on file modification)
        try:
            collection.delete(where={"path": key})
        except Exception:
            pass

        for ch in build_chunks(p, category, wiki_root):
            batch_ids.append(ch["id"])
            batch_docs.append(ch["text"])
            batch_meta.append(ch["metadata"])

        pending_files.append((key, mtime))

        # Mark alias files (same content hash) in history without re-embedding
        if not args.no_dedupe:
            h = file_content_hash(p)
            for cat2, p2 in alias_map.get(h, []):
                a_key = p2.relative_to(wiki_root).as_posix()
                a_mtime = _safe_stat(p2).st_mtime
                # Delete existing chunks for alias files too (clean up stale entries)
                try:
                    collection.delete(where={"path": a_key})
                except Exception:
                    pass
                pending_files.append((a_key, a_mtime))

        # Flush when batch threshold reached
        if len(batch_ids) >= UPSERT_BATCH:
            flush()

        if idx % 25 == 0 or idx == len(canonical):
            rate = idx / max(time.time() - t_start, 1e-3)
            print(f"  [{idx}/{len(canonical)}] {key}  ({rate:.1f} file/s)")

    flush()
    save_history(history_path, history)

    total = collection.count()
    elapsed = time.time() - t_start
    avg_encode = encode_total_time / max(encode_calls, 1)
    print(f"[done] {datetime.now():%Y-%m-%d %H:%M}  total chunks in collection: {total}")
    print(f"       processing time: {elapsed:.1f}s, embedding calls: {encode_calls} (avg {avg_encode:.2f}s/call)")


if __name__ == "__main__":
    main()
