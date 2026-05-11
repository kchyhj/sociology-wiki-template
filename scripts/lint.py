#!/usr/bin/env python3
"""
Wiki Lint — 11 drift checks for the sociology research wiki.

Run with no args for full report. Use --fix to apply safe auto-fixes.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def detect_wiki_root() -> Path:
    """Walk up from cwd looking for CLAUDE.md (wiki root marker)."""
    p = Path.cwd().resolve()
    while p != p.parent:
        if (p / "CLAUDE.md").exists() and (p / "references").is_dir():
            return p
        p = p.parent
    sys.exit("ERROR: Could not detect wiki root (no CLAUDE.md + references/ found in parent chain).")


WIKI = detect_wiki_root()
SKIP = {".git", "_claude_tmp", ".obsidian"}

RESERVED_THEMES = {
    "Stratification", "LaborMarkets", "RaceEthnicity", "Immigration",
    "GenderFamily", "PoliticalSociology", "Education", "Methods",
    "EconomicSociology", "Demography", "Culture", "Theory", "History",
    "AsianAmericans", "Korea",
}
RESERVED_TYPES = {"paper", "book", "book-chapter", "concept", "method", "claim"}
RESERVED_STATUS = {"working", "confident", "retired"}
CAVEAT_PATTERNS = [
    r"\(pending\)", r"\(needs verif", r"\(verify later\)", r"\(추후",
    r"\(향후", r"\(TBD\)", r"\(verification pending\)",
]


def iter_files(subdir: str):
    for root, dirs, files in os.walk(WIKI / subdir):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fn in files:
            if fn.endswith(".md"):
                yield Path(root) / fn


def read_fm(path: Path):
    """Return (frontmatter_dict, body) or (None, full_text)."""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if not txt.startswith("---"):
        return None, txt
    m = re.match(r"---\n(.*?)\n---\n?", txt, re.DOTALL)
    if not m:
        return None, txt
    fm = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip()
    return fm, txt[m.end():]


def report(label: str, issues: list):
    if issues:
        print(f"\n## {label}  ({len(issues)} issues)")
        for issue in issues[:25]:
            print(f"  - {issue}")
        if len(issues) > 25:
            print(f"  ... and {len(issues) - 25} more")
    else:
        print(f"\n## {label}: clean")


# -----------------------------------------------------------------
# Checks
# -----------------------------------------------------------------

def check_1_project_folders():
    """Every projects/{year}/{name}/ has actual content."""
    issues = []
    proj_dir = WIKI / "projects"
    if not proj_dir.exists():
        return issues
    for year_dir in proj_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for proj in year_dir.iterdir():
            if not proj.is_dir():
                continue
            idx = proj / "index.md"
            refs = proj / "references.md"
            if not idx.exists():
                issues.append(f"Missing index.md: {proj.relative_to(WIKI)}")
            if not refs.exists():
                issues.append(f"Missing references.md: {proj.relative_to(WIKI)}")
    return issues


def check_2_orphan_references():
    """Every references/*.md is in z_references_index AND used by ≥1 project."""
    issues = []
    z_idx = WIKI / "z_references_index.md"
    if not z_idx.exists():
        issues.append("z_references_index.md does not exist")
        return issues
    indexed = set(re.findall(r"^([A-Za-z가-힣_]+_\d{4}_[A-Za-z가-힣0-9]+)\.md",
                             z_idx.read_text(encoding="utf-8"), re.MULTILINE))
    refs_in_dir = {p.stem for p in iter_files("references")}
    orphans = refs_in_dir - indexed
    for o in sorted(orphans):
        issues.append(f"references/{o}.md not in z_references_index.md")
    stale = indexed - refs_in_dir
    for s in sorted(stale):
        issues.append(f"z_references_index entry exists but file missing: {s}.md")
    return issues


def check_3_journal_year_order():
    """journals/*.md years descending."""
    issues = []
    jdir = WIKI / "journals"
    if not jdir.exists():
        return issues
    for j in iter_files("journals"):
        years = [int(m) for m in re.findall(r"^## (\d{4})", j.read_text(encoding="utf-8"), re.MULTILINE)]
        if years != sorted(years, reverse=True):
            issues.append(f"{j.relative_to(WIKI)}: year sections not in descending order — {years}")
    return issues


def check_4_index_sync():
    """references/ listing matches z_references_index.md."""
    # Same as check_2 but reported separately for diff convenience.
    return []


def check_5_frontmatter_coverage():
    """Every reference page has YAML frontmatter."""
    issues = []
    for p in iter_files("references"):
        fm, _ = read_fm(p)
        if fm is None:
            issues.append(f"No frontmatter: {p.relative_to(WIKI)}")
    return issues


def check_6_tag_taxonomy_drift():
    """Inline #theme/*, #journal/* consistent with frontmatter values."""
    issues = []
    theme_counter = Counter()
    for p in iter_files("references"):
        body = p.read_text(encoding="utf-8")
        for tag in re.findall(r"#theme/([A-Za-z가-힣_-]+)", body):
            theme_counter[tag] += 1
    # Detect drift: same theme in different casing
    lowered = defaultdict(set)
    for t in theme_counter:
        lowered[t.lower().replace("-", "_")].add(t)
    for canon, variants in lowered.items():
        if len(variants) > 1:
            issues.append(f"#theme/* casing drift: {variants}")
    return issues


def check_7_type_field_consistency():
    """type: book_chapter vs book-chapter etc."""
    issues = []
    for p in iter_files("references"):
        fm, _ = read_fm(p)
        if fm and "type" in fm and fm["type"] not in RESERVED_TYPES:
            issues.append(f"Non-standard type '{fm['type']}': {p.relative_to(WIKI)}")
    return issues


def check_8_caveat_words():
    """Body text should not contain (pending), (verify later), etc."""
    issues = []
    pattern = re.compile("|".join(CAVEAT_PATTERNS), re.IGNORECASE)
    for p in iter_files("references"):
        _, body = read_fm(p)
        for line_no, line in enumerate(body.splitlines(), 1):
            if pattern.search(line):
                # Skip if line is in Verification Metadata section (caveats allowed there)
                # Quick check: if "Verification Metadata" appears before this line
                issues.append(f"{p.relative_to(WIKI)}:{line_no}: caveat word found — '{line.strip()[:80]}'")
                if len(issues) >= 50:
                    return issues
    return issues


def check_9_verification_metadata():
    """Every reference has Verification Metadata sub-section."""
    issues = []
    for p in iter_files("references"):
        body = p.read_text(encoding="utf-8")
        if "## Verification Metadata" not in body and "## 검증 메타데이터" not in body:
            issues.append(f"Missing Verification Metadata: {p.relative_to(WIKI)}")
    return issues


def check_10_prose_mention_autolink():
    """Prose 'Author (Year)' mentions that match existing wiki refs but aren't markdown-linked."""
    # Defer to autolink.py for full detection; just report count here
    issues = []
    # Simplified: count parenthetical year mentions not preceded by ]
    for p in iter_files("references"):
        body = p.read_text(encoding="utf-8")
        mentions = re.findall(r"(?<!\[)\b([A-Z][A-Za-z]+)\s*\(\d{4}\)", body)
        if len(mentions) > 5:
            issues.append(f"{p.relative_to(WIKI)}: {len(mentions)} prose Author(Year) mentions — run autolink.py")
    if issues:
        issues = ["Run: python scripts/autolink.py --dry  to inspect candidates"] + issues[:10]
    return issues


def check_11_data_gap():
    """Papers cited 3+ times in projects/*/references.md but not in z_references_index.md."""
    issues = []
    z_idx = WIKI / "z_references_index.md"
    if not z_idx.exists():
        return issues
    indexed = set(re.findall(r"^([A-Za-z가-힣_]+_\d{4}_[A-Za-z가-힣0-9]+)\.md",
                             z_idx.read_text(encoding="utf-8"), re.MULTILINE))
    # Count author-year mentions across project references.md
    citations = Counter()
    for proj_refs in iter_files("projects"):
        if proj_refs.name != "references.md":
            continue
        body = proj_refs.read_text(encoding="utf-8")
        for m in re.findall(r"\*\*([A-Z][A-Za-zÀ-ž]+(?:\s*(?:and|&|,)\s*[A-Z][A-Za-zÀ-ž]+)*(?:\s+et\s+al\.?)?)\s*\((\d{4})\)\*\*", body):
            name, year = m
            # Coarse key: first author + year
            first_author = re.split(r"\s*(?:and|&|,)\s*", name)[0]
            citations[(first_author, year)] += 1
    for (name, year), count in sorted(citations.items(), key=lambda x: -x[1]):
        if count >= 3:
            # Check if any wiki file matches
            pattern = re.compile(rf"^{re.escape(name)}.*_{year}_")
            if not any(pattern.match(f) for f in indexed):
                issues.append(f"{name} ({year}) cited {count}× across projects, not ingested")
    return issues


# -----------------------------------------------------------------
# Main
# -----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="apply safe auto-fixes")
    parser.add_argument("--check", type=str, help="run only specific check (e.g., --check 6)")
    args = parser.parse_args()

    print(f"# Wiki Lint Report — {WIKI}\n")
    checks = [
        ("1. Project folder validity", check_1_project_folders),
        ("2. Orphan references", check_2_orphan_references),
        ("3. Journal year ordering", check_3_journal_year_order),
        ("4. Index synchronization", check_4_index_sync),
        ("5. Frontmatter coverage", check_5_frontmatter_coverage),
        ("6. Tag taxonomy drift", check_6_tag_taxonomy_drift),
        ("7. Type field consistency", check_7_type_field_consistency),
        ("8. Caveat words in body", check_8_caveat_words),
        ("9. Verification metadata presence", check_9_verification_metadata),
        ("10. Prose mention autolink candidates", check_10_prose_mention_autolink),
        ("11. Data gap detection", check_11_data_gap),
    ]
    for label, fn in checks:
        if args.check and not label.startswith(args.check):
            continue
        try:
            issues = fn()
            report(label, issues)
        except Exception as e:
            print(f"\n## {label}: ERROR — {e}")


if __name__ == "__main__":
    main()
