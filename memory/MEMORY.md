# Memory Index

This file is always loaded into Claude's context at session start. Keep under 200 lines. One line per memory entry: `- [Title](filename.md) — one-line hook`.

Memory entries live in `memory/{type}_{slug}.md` files; this index points to them.

## Feedback (Behavior Corrections)

- [Source-only summarization](examples/feedback_source_only.md) — no fabricated content in literature notes
- [Three-layer verification protocol](examples/feedback_verification_protocol.md) — local primary → web-downloaded primary PDF → leave blank; secondary sources prohibited
- [No unverified claims](examples/feedback_no_unverified.md) — delete unverified content, don't annotate
- [Quantitative accuracy](examples/feedback_quantitative_accuracy.md) — quote exact numbers from source tables, no approximation
- [Re-verification protocol](examples/feedback_recheck_protocol.md) — when reusing wiki content, re-verify at the layer the original was verified
- [Wiki sweep checklist](examples/feedback_wiki_sweep_checklist.md) — mandatory per-file procedure during lint sweeps
- [Layer 2 mandatory](examples/feedback_layer2_mandatory.md) — when Layer 1 fails, find paper PDF on web (papers_web/); no secondary sources permitted

## Project (Active Context)

(Add absolute-date project entries here as projects evolve.)

## Reference (External Systems)

- [Zotero integration workflow](examples/reference_zotero_workflow.md) — Local API enable; references.bib path; BBT citekey rules
- [RAG system docs](examples/reference_rag_system.md) — `RAG_SETUP.md` at OneDrive root is canonical; bge-m3 + ChromaDB

## User (Profile)

(Add stable facts about the user here.)
