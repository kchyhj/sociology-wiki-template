"""Phase 1 — Auto-linkify prose mentions of wiki papers in references/.

Strategy:
  - Scan references/*.md bodies (frontmatter skipped)
  - Find "Author (Year)" / "Author & Coauthor (Year)" / "Author et al. (Year)" patterns
    that lie OUTSIDE existing markdown links
  - Resolve against an index of (first_author_surname_lower, year) -> [wiki_stems]
  - If UNIQUE match (one stem), replace with markdown link
  - If multiple matches, try to disambiguate via second author; otherwise SKIP

Dry-run with --dry shows would-be changes. Apply by running without --dry.

Detects the wiki root from cwd (walks up looking for CLAUDE.md + references/).
Override with WIKI_ROOT environment variable.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


def detect_wiki_root() -> Path:
    """Walk up from cwd until a folder with CLAUDE.md + references/ is found."""
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
REF_DIR = os.path.join(ROOT, 'references')


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def read(p):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


def write(p, txt):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)


# Build the wiki ref index
ref_stems = [os.path.splitext(fn)[0] for fn in os.listdir(REF_DIR) if fn.endswith('.md')]
# Index by (first_author_lower, year): [stems]
idx_first = defaultdict(list)
# Index by (first_author_lower, second_author_lower, year): [stems]
idx_pair = defaultdict(list)
# Index by (first_author_lower, 'etal', year): [stems]
idx_etal = defaultdict(list)

stem_meta = {}  # stem -> (authors_list_lower, year)


def parse_stem(stem):
    """Return (authors_lower: list[str], year: str) or None."""
    # filename pattern: Author1[_Author2[_Author3]]_YEAR_rest
    m = re.match(r'^(.+?)_(\d{4})(?:_.*)?$', stem)
    if not m:
        return None
    prefix = m.group(1)
    year = m.group(2)
    tokens = prefix.split('_')
    # Handle "_etal" marker
    has_etal = False
    if tokens and tokens[-1].lower() in ('etal', 'et', 'al'):
        has_etal = True
        tokens = tokens[:-1]
    authors = [t.lower() for t in tokens if t]
    return authors, year, has_etal


for s in ref_stems:
    p = parse_stem(s)
    if not p:
        continue
    authors, year, has_etal = p
    stem_meta[s] = (authors, year, has_etal)
    if not authors:
        continue
    first = authors[0]
    idx_first[(first, year)].append(s)
    if len(authors) >= 2:
        idx_pair[(first, authors[1], year)].append(s)
    if has_etal:
        idx_etal[(first, 'etal', year)].append(s)


# Prose-mention regex (capturing the pattern AND its surface form):
# Match: Author1 [& | and | , | et al.] Author2 ... (YYYY)
# Surface forms we accept:
#  - "Smith (2020)"
#  - "Smith and Jones (2020)"
#  - "Smith & Jones (2020)"
#  - "Smith, Jones, & Brown (2020)"
#  - "Smith et al. (2020)"
#  - Korean: "김저자 (2024)" / "홍길동·이공저자 (2021)"
NAME_TOK = r"(?:[A-Z][A-Za-zÀ-žĀ-ž]+(?:[-'][A-Z]?[A-Za-zÀ-ž]+)*|[가-힣]{1,4})"
MENTION_RE = re.compile(
    rf"(?<![\[\w]){NAME_TOK}"
    rf"(?:\s*(?:and|&|·|,)\s*{NAME_TOK})*"
    rf"(?:\s+et\s+al\.?)?"
    rf"\s*\((\d{{4}})\)"
)

# More fine-grained extractor on a matched span
def extract_authors_year(text_span):
    """Given a matched span like 'Smith & Jones (2020)', return (authors_lower_list, year, has_etal)."""
    m = re.match(rf"({NAME_TOK}(?:\s*(?:and|&|·|,)\s*{NAME_TOK})*)\s*(et\s+al\.?)?\s*\((\d{{4}})\)", text_span)
    if not m:
        return None
    raw_names = m.group(1)
    has_etal = bool(m.group(2))
    year = m.group(3)
    # Split on connectors
    names = re.split(r"\s*(?:and|&|·|,)\s*", raw_names)
    names = [n.strip() for n in names if n.strip()]
    return [n.lower() for n in names], year, has_etal


def resolve(authors_lower, year, has_etal):
    """Return (matched_stem, was_ambiguous)."""
    if not authors_lower:
        return None, False
    first = authors_lower[0]
    # Try pair index first
    if len(authors_lower) >= 2:
        key = (first, authors_lower[1], year)
        candidates = idx_pair.get(key, [])
        if len(candidates) == 1:
            return candidates[0], False
        if len(candidates) > 1:
            return None, True
    # Try et al. index
    if has_etal:
        key = (first, 'etal', year)
        candidates = idx_etal.get(key, [])
        if len(candidates) == 1:
            return candidates[0], False
        if len(candidates) > 1:
            return None, True
    # Fall back to first-author index
    candidates = idx_first.get((first, year), [])
    if len(candidates) == 1:
        return candidates[0], False
    if len(candidates) > 1:
        # Try filtering to single-author papers only (no second author in stem)
        single = [s for s in candidates if len(stem_meta.get(s, ([],))[0]) == 1]
        if len(single) == 1:
            return single[0], False
        return None, True
    return None, False


def process_file(path, dry=True):
    """Return (replacements_made: int, ambiguous_count: int, sample_changes: list)."""
    src_stem = os.path.splitext(os.path.basename(path))[0]
    text = read(path)
    if not text:
        return 0, 0, []
    # Split off frontmatter; only mutate body
    if text.startswith('---'):
        mm = re.match(r'(---\n.*?\n---\n?)', text, re.DOTALL)
        if mm:
            fm, body = mm.group(1), text[mm.end():]
        else:
            fm, body = '', text
    else:
        fm, body = '', text

    # Carve out spans that should NOT be touched:
    #  - markdown links: [...](...) and reference-style link definitions
    #  - inline code spans `...`
    #  - bibliography lines: start with "**Bibliography**:" or "**서지**:" (Korean) — skip whole line
    # Strategy: replace these spans with placeholder tokens, then process, then restore.
    protected = []
    PLACE = "\x00P{}\x00"

    def mask(m):
        protected.append(m.group(0))
        return PLACE.format(len(protected) - 1)

    # Mask code spans
    body = re.sub(r"`[^`\n]+`", mask, body)
    # Mask markdown links (with destinations)
    body = re.sub(r"\[[^\]\n]+\]\([^)\n]+\)", mask, body)
    # Mask reference-style link defs [text]: url
    body = re.sub(r"^\[[^\]\n]+\]:\s*\S+$", mask, body, flags=re.MULTILINE)
    # Mask bibliography lines — keep author/year intact, don't auto-link the paper's own citation
    body = re.sub(r"^\*\*Bibliography\*\*:.*$", mask, body, flags=re.MULTILINE)
    body = re.sub(r"^\*\*서지\*\*:.*$", mask, body, flags=re.MULTILINE)

    replacements = 0
    ambiguous = 0
    samples = []

    def linkify(match):
        nonlocal replacements, ambiguous
        full = match.group(0)
        parsed = extract_authors_year(full)
        if not parsed:
            return full
        authors_lower, year, has_etal = parsed
        # Don't link to self
        m_self = stem_meta.get(src_stem)
        if m_self and m_self[1] == year and m_self[0] and authors_lower[0] == m_self[0][0]:
            return full
        stem, was_amb = resolve(authors_lower, year, has_etal)
        if stem is None:
            if was_amb:
                ambiguous += 1
            return full
        # Build relative link to the ref file
        new_text = f"[{full}](../references/{stem}.md)"
        replacements += 1
        if len(samples) < 3:
            samples.append(f"{full}  ->  {stem}")
        return new_text

    body = MENTION_RE.sub(linkify, body)

    # Restore protected spans
    for i, span in enumerate(protected):
        body = body.replace(PLACE.format(i), span, 1)

    new_text = fm + body
    if not dry and new_text != text:
        write(path, new_text)
    return replacements, ambiguous, samples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true', help='preview only, no writes')
    ap.add_argument('--verbose', action='store_true', help='print every file with changes')
    args = ap.parse_args()

    total_repl = 0
    total_amb = 0
    files_changed = 0
    sample_log = []
    for fn in sorted(os.listdir(REF_DIR)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(REF_DIR, fn)
        repl, amb, samples = process_file(path, dry=args.dry)
        total_repl += repl
        total_amb += amb
        if repl > 0:
            files_changed += 1
            if args.verbose:
                print(f'  {fn}: +{repl} links' + (f', {amb} ambiguous' if amb else ''))
            if len(sample_log) < 15:
                for s in samples:
                    sample_log.append(f'  {fn}: {s}')

    print()
    print('=' * 60)
    print('SUMMARY' + (' (DRY RUN)' if args.dry else ''))
    print('=' * 60)
    print(f'  Replacements applied: {total_repl}')
    print(f'  Ambiguous mentions skipped: {total_amb}')
    print(f'  Files changed: {files_changed}')
    print()
    print('Sample replacements (first 15):')
    for s in sample_log:
        print(s)


if __name__ == '__main__':
    main()
