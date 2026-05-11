"""References-to-references link analysis.

Measures:
  (a) Current ref->ref direct markdown links (baseline)
  (b) Concept-page co-occurrence (candidate links: papers appearing in same
      concept page's 실증 기록 / Empirical Record table)
  (c) Inline prose mentions of other wiki papers (Author Year patterns)

Detects the wiki root from cwd (walks up looking for CLAUDE.md + references/).
Override with WIKI_ROOT environment variable.
"""
import os, re, sys
from collections import defaultdict, Counter
from pathlib import Path


def detect_wiki_root() -> Path:
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


ROOT = str(detect_wiki_root())
SKIP = {'.git', '_claude_tmp', '.obsidian'}

REF_DIR = os.path.join(ROOT, 'references')
GEN_DIR = os.path.join(ROOT, 'general')


def iter_md(d):
    for r, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for fn in files:
            if fn.endswith('.md'):
                yield os.path.join(r, fn)


def read(p):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


# Build set of existing reference filenames (stems)
ref_files = [os.path.basename(p) for p in iter_md(REF_DIR)]
ref_stems = {os.path.splitext(f)[0] for f in ref_files}
print(f'Total reference files: {len(ref_files)}')

# ---------- (a) Baseline: direct ref->ref markdown links ----------
ref_to_ref_links = defaultdict(set)   # src_stem -> {dst_stem, ...}
ref_outbound_total = Counter()        # src_stem -> total links emitted
ref_inbound_from_ref = Counter()      # dst_stem -> count of inbound from refs

# Match [text](anything_ending_in_<stem>.md) where stem is a ref file stem
link_pat = re.compile(r'\]\(([^)]+\.md)\)')

for p in iter_md(REF_DIR):
    src = os.path.splitext(os.path.basename(p))[0]
    body = read(p)
    for url in link_pat.findall(body):
        base = os.path.splitext(os.path.basename(url))[0]
        if base in ref_stems and base != src:
            ref_to_ref_links[src].add(base)
            ref_outbound_total[src] += 1
            ref_inbound_from_ref[base] += 1

n_total_pairs = sum(len(v) for v in ref_to_ref_links.values())
n_refs_with_any_out = len(ref_to_ref_links)
print(f'\n=== (a) BASELINE: direct ref->ref markdown links ===')
print(f'  Total ref->ref edges (unique pairs): {n_total_pairs}')
_pct = (100.0 * n_refs_with_any_out / len(ref_stems)) if ref_stems else 0.0
print(f'  Reference files with at least 1 outbound ref-link: {n_refs_with_any_out} / {len(ref_stems)} ({_pct:.1f}%)')
print(f'  Mean outbound (among refs with any): {n_total_pairs/max(n_refs_with_any_out,1):.2f}')
print(f'\n  Most ref->ref-linking source files (top 15):')
for s, edges in sorted(ref_to_ref_links.items(), key=lambda x: -len(x[1]))[:15]:
    print(f'    {len(edges):4d}  {s}')
print(f'\n  Most ref->ref-linked targets (top 15):')
for t, n in sorted(ref_inbound_from_ref.items(), key=lambda x: -x[1])[:15]:
    print(f'    {n:4d}  {t}')

# ---------- (b) Concept-page co-occurrence (candidate links) ----------
# For each concept page, extract all reference stems linked from it.
# Any two such refs are *thematically co-located*. Build pairwise candidates.

concept_pages_with_refs = {}  # concept_page_relpath -> set(ref_stems)
for p in iter_md(GEN_DIR):
    if os.path.basename(p) == '0_index.md':
        continue
    body = read(p)
    refs_here = set()
    for url in link_pat.findall(body):
        base = os.path.splitext(os.path.basename(url))[0]
        if base in ref_stems:
            refs_here.add(base)
    if len(refs_here) >= 2:
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        concept_pages_with_refs[rel] = refs_here

print(f'\n=== (b) CANDIDATE LINKS: co-occurrence in concept pages ===')
print(f'  Concept pages with >=2 ref-links: {len(concept_pages_with_refs)}')

# Build candidate co-occurrence count: pair -> #shared concept pages
pair_count = Counter()
pair_origins = defaultdict(set)  # pair -> {concept_pages}
for cp, refs in concept_pages_with_refs.items():
    refs_list = sorted(refs)
    for i in range(len(refs_list)):
        for j in range(i + 1, len(refs_list)):
            pair = (refs_list[i], refs_list[j])
            pair_count[pair] += 1
            pair_origins[pair].add(cp)

# Subtract: pairs that ALREADY have a direct ref->ref link in either direction
existing_pairs = set()
for s, dsts in ref_to_ref_links.items():
    for d in dsts:
        existing_pairs.add(tuple(sorted((s, d))))

new_candidate_pairs = {p: n for p, n in pair_count.items() if p not in existing_pairs}
print(f'  Total unique co-occurring pairs: {len(pair_count)}')
print(f'  Pairs WITHOUT existing direct ref->ref link (candidates): {len(new_candidate_pairs)}')
print(f'  Candidate pairs co-occurring in 2+ concept pages: '
      f'{sum(1 for n in new_candidate_pairs.values() if n >= 2)}')
print(f'  Candidate pairs co-occurring in 3+ concept pages: '
      f'{sum(1 for n in new_candidate_pairs.values() if n >= 3)}')

# Surface highest-value candidates: pairs co-occurring in 3+ concept pages
print(f'\n  Top 25 candidate pairs (3+ co-occurrences, no existing link):')
hi = sorted(new_candidate_pairs.items(), key=lambda x: -x[1])[:25]
for (a, b), n in hi:
    origins = list(pair_origins[(a, b)])[:3]
    print(f'    {n}x   {a}  <->  {b}')
    for o in origins:
        print(f'         in: {o}')

# ---------- (c) Per-reference candidate count ----------
ref_candidate_neighbors = defaultdict(set)
for (a, b), n in new_candidate_pairs.items():
    if n >= 2:
        ref_candidate_neighbors[a].add((b, n))
        ref_candidate_neighbors[b].add((a, n))

# How many existing references have NO ref->ref outbound but >=2 candidates available?
no_links_with_candidates = [s for s in ref_stems
                            if s not in ref_to_ref_links
                            and s in ref_candidate_neighbors]
print(f'\n  Reference files with 0 ref->ref links AND >=2-cooccur candidates: {len(no_links_with_candidates)}')
print(f'  (these are the best backfill targets)')

# ---------- (c2) Plain Author_Year mentions in prose ----------
# Heuristic: look for "AuthorLastname (YYYY)" or "AuthorLastname & AuthorLastname (YYYY)"
# Check if matches any wiki ref stem
print(f'\n=== (c) PROSE MENTIONS of wiki papers (heuristic) ===')
# Index ref stems by author + year for fast lookup
stem_index = defaultdict(list)  # (lastname_first_token_lower, year) -> [stems]
for s in ref_stems:
    m = re.match(r'^([A-Za-zÀ-ž가-힣]+)(?:_[A-Za-z가-힣_]+)*_(\d{4})', s)
    if m:
        stem_index[(m.group(1).lower(), m.group(2))].append(s)

# For each ref page, find "Author (YYYY)" patterns and check matches
prose_mentions = defaultdict(set)
for p in iter_md(REF_DIR):
    src = os.path.splitext(os.path.basename(p))[0]
    body = read(p)
    # Strip frontmatter
    if body.startswith('---'):
        mm = re.match(r'---\n.*?\n---\n?', body, re.DOTALL)
        if mm:
            body = body[mm.end():]
    # Match "Word (YYYY)" — Word is alphabetic 2+ chars
    for m in re.finditer(r'([A-Z][A-Za-zÀ-ž]+|[가-힣]{2,3})\s*(?:&\s*[A-Z][A-Za-zÀ-ž]+\s*|et\s+al\.\s*)?\((\d{4})\)', body):
        name = m.group(1).lower()
        year = m.group(2)
        candidates = stem_index.get((name, year), [])
        for c in candidates:
            if c != src:
                prose_mentions[src].add(c)

n_prose_pairs = sum(len(v) for v in prose_mentions.values())
n_with_prose = len(prose_mentions)
print(f'  Refs with at least 1 prose mention of another wiki paper: {n_with_prose}')
print(f'  Total prose-mention edges (directional): {n_prose_pairs}')

# Pairs that exist in prose but NO markdown link
prose_only = defaultdict(set)
for src, mentions in prose_mentions.items():
    for dst in mentions:
        if dst not in ref_to_ref_links.get(src, set()):
            prose_only[src].add(dst)

n_prose_only = sum(len(v) for v in prose_only.values())
print(f'  Prose-mention edges WITHOUT corresponding markdown link: {n_prose_only}')
print(f'  (these mentions could be auto-linked)')

# Sample some prose-only edges
print(f'\n  Sample prose-mention edges to auto-link (first 15):')
flat = []
for src, dsts in prose_only.items():
    for d in dsts:
        flat.append((src, d))
for src, dst in flat[:15]:
    print(f'    {src}  ->  {dst}')

print()
print('=== SUMMARY ===')
print(f'  Baseline ref->ref edges:     {n_total_pairs}')
print(f'  Concept co-occur candidates: {sum(1 for n in new_candidate_pairs.values() if n>=2)} (2+ cooccur) / {len(new_candidate_pairs)} (any)')
print(f'  Prose-mention auto-linkable: {n_prose_only}')
print(f'  Refs with 0 outbound:        {len(ref_stems) - n_refs_with_any_out}')
