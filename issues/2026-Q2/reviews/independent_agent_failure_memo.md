---
issue: "2026-Q2"
date: "2026-06-13"
status: corrective_review
chief_editor_status: approved_for_temporary_publication
---

# Corrective Review: Why The Independent-Agent Standard Failed

## Finding

The original policy documents required article work to be performed by distinct editorial agents: political editor, economics editor, sociology editor, law and institutions editor, technology editor, education editor, foreign affairs editor, culture editor, source researcher, data researcher, dissent editor, fact checker, statistics checker, translation editors, and final managing editor. The June 11 production pass did not satisfy that standard. The June 12 repair corrected nine articles but left four core English originals on the older scaffold: the editor's note, the AI governance essay, the AI/war-economy leader, and the macro fragility essay.

## Immediate Cause

The retired `pipelines/substantive_2026_q2_editorial_pass.py` centralized article bodies through compact generator functions named `make_compact_en` and `make_compact_ko`. Those functions imposed the same section order, the same argument-reconstruction language, the same temporary-publication language, and similar source-limit paragraphs across unrelated articles. The later repair fixed the visible generator symbols but did not require every public English original to declare an assigned editor, use an independent article structure, or carry matching independent dossiers and reviews.

## Process Cause

The same pipeline wrote bodies, reviews, dossiers, translation checks, and publication-ready files in one pass. That collapsed role boundaries. It made a file look as if it had passed multiple editorial desks when the article body had in fact come from one scaffold.

## Metadata Cause

The public files identified broad "Codex Editorial Agents" rather than enforcing a per-article assigned editor in the generator. Agent-role prompt files existed, but the production script did not require role-specific outputs before publication.

## Review Gap

Existing tests checked publication gates, bilingual links, citation status, and required headings. They did not check repeated prose, identical section structures, public-facing development notes, whether source dossiers had been separated from article prose, or whether every public English original had an assigned editor and independent rewrite review.

## Corrective Actions Taken

- Retired the compact generation script and removed `make_compact_en` / `make_compact_ko`.
- Added `pipelines/rewrite_2026_q2_independent_articles.py`, which stores article-specific bodies and assigned agents without a shared body template.
- Rewrote the nine affected article pairs with distinct structures, cases, and argument development.
- Completed the missed four core article pairs on June 13: `editors-note-capacity-question`, `govern-ai-before-infrastructure`, `ai-boom-war-economy`, and `new-macro-fragility`.
- Moved "stronger final version" and similar reporting-path material into source dossiers and review files.
- Added a regression test blocking compact-generation symbols and public-facing reporting-path phrases in final/site article files.
- Added regression tests requiring public English originals to declare `assigned_agent`, `body_generation: independent_article_structure`, and `independent_editorial_pass`; requiring matching independent source dossiers and reviews; blocking reuse of compact heading scaffolds; and blocking duplicate final English heading signatures.

## Remaining Editorial Risk

The corrected articles are substantive temporary-publication drafts. Several still need deeper non-temporary reporting: Korean full legal texts, official election tables after NEC verification, disaggregated fertility data, fiscal and welfare tables, and systematic discourse evidence for AI fatalism. These are now recorded as dossier tasks rather than presented as article conclusions.
