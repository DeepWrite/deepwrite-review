---
issue: "2026-Q2"
date: "2026-06-13"
status: followup_scheduled
due_window: "2026-06-14 to 2026-06-15"
chief_editor_status: approved_for_review
---

# Follow-Up Plan: Full Article Rewrites

## Trigger

The June 13 anti-scaffold repair solved the mechanical table-of-contents problem, but most Q2 articles still need full prose rewrites so that article-specific editorial agents shape the argument, examples, pacing, evidence handling, and uncertainty discipline inside the body itself.

## Representative Rewrite Completed

- `ai-boom-war-economy`
  - Assigned desks: Technology Editor with Economics Editor and Data Researcher.
  - Rewrite model: compute-stack analysis, macroeconomic distribution analysis, and denominator discipline are visible in the article's prose rather than only in metadata.

## Remaining Manuscripts To Reattempt

- `editors-note-capacity-question`
- `govern-ai-before-infrastructure`
- `new-macro-fragility`
- `democracy-after-long-decline`
- `displacement-without-settlement`
- `korea-mandate-problem-local-elections`
- `korea-semiconductor-recovery-welfare-state`
- `korea-fertility-housing-pronatalism`
- `korea-constitutional-court-quiet-institutionalism`
- `universities-after-generative-ai`
- `culture-of-ai-fatalism`
- `structural-reading-list`

## Reattempt Order

1. Rework the three core frame articles first: `new-macro-fragility`, `govern-ai-before-infrastructure`, and `editors-note-capacity-question`.
2. Rework the institutional and Korea articles next, preserving official-source discipline and moving unresolved reporting tasks to dossiers.
3. Rework the education, culture, displacement, democracy, and source-map articles as separate desk voices rather than one generic article form.

## Definition Of Done

- Public English and Korean copies carry the same rewritten argument structure.
- `drafts`, `final`, and `site/_articles` copies are synchronized where appropriate while preserving draft/publication metadata.
- Source dossiers identify the assigned desk's evidence responsibilities.
- Reviews explicitly confirm that the body, not merely the headings, reflects the assigned editor or editor pair.
- Regression checks still block generic heading scaffolds and public development notes.
- Run `pytest`, `pipelines/publish_check.py`, Jekyll build, and `git diff --check` before any commit.
