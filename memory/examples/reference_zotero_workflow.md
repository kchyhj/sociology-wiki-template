---
name: zotero_integration_workflow
description: Zotero MCP integration. Local API must be enabled. references.bib path. BBT citekey rules and duplicate handling.
type: reference
---

Zotero Local API and the Better BibTeX (BBT) plugin enable the wiki ↔ Zotero integration. Reference for the integration setup and common operations.

## Local API

Zotero's Local API (HTTP server) must be enabled for MCP integration:

```
Zotero → Edit → Preferences (or Settings on Mac)
  → Advanced → Config Editor
  → Search "httpServer.enabled"
  → Set to `true`
  → Restart Zotero
```

When disabled (default):
- BBT citation keys generated as placeholders, not real keys
- Cannot merge duplicates programmatically
- MCP queries return errors

## references.bib Path

The canonical bibliography file is at the OneDrive root:

```
{OneDrive root}/references.bib
```

Where OneDrive root is one of:
Cross-device users may have multiple paths to detect (desktop / laptop / etc.). Store the actual paths in this memory entry on each device, or use a `WIKI_ROOT` environment variable.

This is the *unified* bib database. Project-specific `Overleaf/references.bib` files exist but are historical or project-bound supplements. New LaTeX manuscripts should reference the OneDrive root version.

LaTeX path from a project's Overleaf folder:
```
\bibliography{../../../../references}   % relative path from your manuscript folder to the bib file
```

## BBT Citekey Rules

BBT (Better BibTeX) generates citekeys with the user's configured pattern. Common patterns:

- `Author:Year` (Aaron:1978)
- `Author_Year` (Acemoglu_2008)
- `Author_etalYear` (Abadie_etal2023)

These differ from wiki filename convention (`Author_Year_Journal`), so direct mapping from wiki stem to BBT key is not 1:1. Use the `bibkey:` frontmatter field in wiki references to record the BBT key when available.

## Adding to Zotero

When the wiki ingests a new paper, optionally add to Zotero via MCP. Before adding:

1. **Grep references.bib** for the bibliography (author + year + title fragment) to check for existing entry.
2. If exists: use the existing BBT key; do not duplicate.
3. If not: `mcp__zotero__add_from_file` (or equivalent).

Duplicate management:
- Manual merge in Zotero (Edit → Find Duplicates) when duplicates accumulate.
- Programmatic merge requires Local API enabled.

## Common Issues

| Issue | Diagnosis | Fix |
|---|---|---|
| BBT keys are placeholder strings | Local API disabled | Enable in Zotero config |
| Wiki autolink can't find Zotero key | `bibkey:` field missing in frontmatter | Manual lookup in references.bib + frontmatter update |
| Zotero MCP times out | Zotero not running, or Local API disabled | Start Zotero, verify config |
