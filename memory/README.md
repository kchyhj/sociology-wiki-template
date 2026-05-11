# Memory System

Persistent rules and context that survive across Claude Code sessions. The memory captures behavioral corrections, project context, and references to external systems — things that should never need re-explanation.

---

## How It Works

Claude Code's memory system uses two files:

1. **`MEMORY.md`** — index file. Always loaded into Claude's context at session start.
2. **`{type}_{slug}.md`** — individual memory entries, referenced from the index.

When a memory becomes relevant, Claude reads the specific entry file. Most entries are 5-20 lines. The index file is the navigation; entries are the content.

---

## Memory Types

### `user` — Facts about you

Your role, expertise, preferences, knowledge.

Examples:
- "User is a quantitative sociologist publishing in ASR/AJS/SF/Demography."
- "User reads [your primary language] and English. Default to [your primary language] unless user writes in English." (substitute Spanish / Chinese / Japanese / etc.)
- "User has 10 years of Stata expertise; React is new — frame frontend explanations in terms of backend analogues."

### `feedback` — Corrections you've given

The most important type. When you correct Claude's behavior, save it. When you confirm a non-obvious approach, also save (positive feedback prevents over-correction).

Structure: rule + **Why** + **How to apply**.

Examples in this folder:
- [`feedback_source_only.md`](examples/feedback_source_only.md) — no fabricated content in summaries
- [`feedback_verification_protocol.md`](examples/feedback_verification_protocol.md) — 3-layer verification ordering
- [`feedback_no_unverified.md`](examples/feedback_no_unverified.md) — delete don't annotate
- [`feedback_quantitative_accuracy.md`](examples/feedback_quantitative_accuracy.md) — quote numbers, don't approximate
- [`feedback_recheck_protocol.md`](examples/feedback_recheck_protocol.md) — re-verification when reusing

### `project` — Active project context

Who, what, when, why for ongoing projects.

Always **absolute dates** ("2026-03-15"), not relative ("Thursday"), so the memory survives time passage.

Examples:
- "Merge freeze 2026-03-05 for mobile release cut."
- "Auth middleware rewrite is driven by legal/compliance, not tech debt."

### `reference` — External systems

Pointers to where information lives outside the wiki.

Examples:
- "Pipeline bugs tracked in Linear project INGEST."
- "Grafana board grafana.internal/d/api-latency for oncall latency."

---

## When to Save Memory

### ✅ Save when

- User explicitly says "remember this"
- User corrects a behavior ("don't add unverified citations", "stop adding em-dashes")
- User confirms a non-obvious approach ("yes, the single bundled PR was right — keep doing that")
- User shares persistent context about themselves
- User references an external system you'll need again

### ❌ Don't save

- One-off task details
- Code patterns derivable from current files
- Git history (use `git log`)
- Already-documented in `CLAUDE.md`
- Ephemeral project state ("in progress today")

---

## Memory Entry Format

```yaml
---
name: short_descriptive_name
description: one-line description (used for relevance scoring in future sessions, be specific)
type: feedback                       # user | feedback | project | reference
---

(For feedback: rule first, then Why, then How to apply.)

Rule statement.

**Why**: Reason the user gave — often a past incident or strong preference.

**How to apply**: When/where this kicks in.

(For project: fact + Why + How to apply.)

Project fact.

**Why**: Motivation — constraint, deadline, stakeholder ask.

**How to apply**: How this shapes future suggestions.

(For reference: pointer + what it's authoritative for.)

External system + URL/path.
What kind of information is found there.
When to consult it.

(For user: facts about the user, prose form.)
```

---

## `MEMORY.md` Index Format

The index file is *always* loaded; keep it under 200 lines. One line per entry.

```markdown
# Memory Index

- [Title of entry](filename.md) — one-line hook explaining when relevant
- [Title of entry](filename.md) — one-line hook
...
```

The "hook" is the discriminator — when Claude scans the index, it uses the hook to decide whether to load the full entry.

---

## Examples in This Folder

See [`examples/`](examples/) for ~10 sanitized representative entries, mostly `feedback` type (the most numerous in practice). Each demonstrates:

- The minimal structure (frontmatter + body)
- Rule + Why + How to apply pattern
- One specific learning per entry (atomicity)

Mature memory systems accumulate dozens of entries over months as the user corrects behaviors and confirms approaches. The examples in this folder represent the patterns; additional entries are domain-specific repetitions of those same patterns.

---

## Maintenance

- **Update** a memory when its rule evolves. Don't accumulate near-duplicates.
- **Delete** a memory when it no longer applies (e.g., project finished, user changed practice).
- **Index hygiene**: when an entry is updated/deleted, update `MEMORY.md` to match. The index drifting from the entry files is a common failure mode.

The lint script (Step 6 in main lint) checks that every memory file is in the index and every index entry has an existing file.
