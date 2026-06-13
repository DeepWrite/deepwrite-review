# DeepWrite Review

DeepWrite Review is a Markdown-first, English-Korean bilingual quarterly magazine repository for producing a serious online review of politics, economy, society, technology, law, education, culture, and global affairs.

The system is designed for continuous editorial radar, weekly editor briefs, monthly topic maps, quarterly issue production, source dossiers, evidence review, bilingual translation, and GitHub Pages publication. It does not automatically publish final articles. Every issue and article remains an editorial submission until the Chief Editor approves it.

## Architecture

- Static site generator: Jekyll, chosen for native GitHub Pages compatibility, simple Markdown collections, Liquid templates, and a low-maintenance Ruby toolchain.
- Source content: Markdown files with YAML front matter.
- Editorial workspace: `/issues`, `/radar`, `/templates`, `/config`, and `/prompts`.
- Public site source: `/site`.
- Built output: `/docs` when building locally or in GitHub Actions.
- Validation: Python tests under `/tests`, plus GitHub Actions gates.

## Local Setup

```bash
cd deepwrite-review
bundle install
python3 -m pip install -r requirements.txt
```

Build the site:

```bash
bundle exec jekyll build --source site --destination docs
```

Serve locally:

```bash
bundle exec jekyll serve --source site --destination docs --livereload
```

Run editorial and publication checks:

```bash
pytest
python3 pipelines/publish_check.py
```

## Editorial Radar

The radar scripts create reviewable files without publishing them.

```bash
python3 pipelines/radar_scan.py --cadence daily
python3 pipelines/editorial_brief.py
python3 pipelines/topic_map.py
python3 pipelines/generate_issue.py --issue 2026-Q2
```

Live research and external source fetching require credentials or explicit API configuration. Where credentials are unavailable, scripts create clearly marked TODO and unverified research stubs instead of fabricating sources or statistics.

## Chief Editor Approval Gates

Every article must move through this sequence:

1. proposed
2. commissioned
3. approved_for_draft
4. approved_for_review
5. approved_for_translation
6. approved_for_temporary_publication
7. approved_for_publication

No article may appear on the public site unless it is explicitly approved for either temporary or permanent publication.

Temporary public articles must have:

- `chief_editor_status: approved_for_temporary_publication`
- `status: temporary_publication`
- `publication_stage: temporary`
- `citation_status: checked_for_temporary_publication`
- `evidence_level` is assigned
- `translation_status: checked_for_temporary_publication` where applicable

Permanent public articles must have:

- `chief_editor_status: approved_for_publication`
- `status: published`
- `publication_stage: final` or no `publication_stage`
- `citation_status: checked`
- `evidence_level` is assigned
- `translation_status: checked` where applicable

The tests and `pages.yml` deployment workflow enforce these rules.

## Bilingual Article Pairing

Final issue files live in:

- English: `/issues/YYYY-QN/final/en/article-slug.md`
- Korean: `/issues/YYYY-QN/final/ko/article-slug.md`

Each article has stable `slug`, `language`, `translation_of`, and `counterpart_url` front matter. The site publishes approved articles to `/en/:slug/` and `/ko/:slug/`, with a visible language toggle on every article page.

## Weekly Brief Submission

`.github/workflows/weekly_editorial_brief.yml` runs weekly, creates `/radar/weekly/YYYY-WW-editorial-brief.md`, and opens or updates a pull request for Chief Editor review when repository permissions allow it. It never deploys public content.

## Monthly Topic Maps

`.github/workflows/monthly_topic_map.yml` consolidates weekly briefs into `/radar/monthly/YYYY-MM-topic-map.md` and submits the result for review through a pull request.

## Quarterly Issue Scaffolds

`.github/workflows/quarterly_issue_scaffold.yml` creates a new `/issues/YYYY-QN` folder with agenda, decision log, evidence log, reports, and candidate topic placeholders. It opens a review pull request and does not draft articles until the Chief Editor approves the agenda, table of contents, article list, thesis, and dossiers.

## Approving Or Rejecting Topics

Edit `/issues/YYYY-QN/chief_editor_decisions.md` and mark each decision explicitly:

- `approve`
- `revise`
- `reject`
- `hold`

The repository treats silence as non-approval.

## Generating Drafts

After approval:

```bash
python3 pipelines/research_dossier.py --issue 2026-Q2 --slug example-slug
python3 pipelines/draft_article.py --issue 2026-Q2 --language en --slug example-slug
```

Drafts are created with TODO sections and strict citation warnings. They are not published.

## Translation Workflow

Translate only after the source article is approved for translation:

```bash
python3 pipelines/translate_article.py --issue 2026-Q2 --source-language en --slug example-slug
python3 pipelines/bilingual_check.py --issue 2026-Q2 --slug example-slug
```

The translation report flags missing sections, citation drift, and bilingual link problems.

## GitHub Pages Deployment

`pages.yml` builds the Jekyll site and deploys only after publication-branch merges pass all checks. Drafts, unapproved articles, unchecked citations, and unchecked translations fail the build.

## Evidence Logs

Evidence logs live at `/issues/YYYY-QN/evidence_log.csv`. Each major factual or statistical claim should include source, date, unit, geography, denominator, limitations, evidence tier, verification status, and article slug.

## Regional Mix And Korean Sources

For 2026-Q2, the issue should be roughly 70 percent global or transnational structural issues and 30 percent Republic of Korea issues.

Korea coverage should rely on Korean raw sources for facts and evidence: official statistics, legislation, court decisions, Constitutional Court decisions, National Assembly records, government reports, Bank of Korea publications, public datasets, election data, official speeches, transcripts, and institutional policy documents.

Korean-language columns, opinion essays, critical essays, and already-synthesized Korean articles may be used only as evidence of discourse, media attention, or agenda-setting. They should not be used as raw evidence for DeepWrite Review's own factual or causal claims.

## Authorship And AI Assistance

The default public byline is `DeepWrite Review Editorial Desk`, with Codex assistance disclosed plainly. Korean responsibility should be shown as `손제연 책임편집자`.

Do not use fictional personal bylines or real public figures as placeholder authors.

## Human Responsibilities

TODOs that require the Chief Editor or external credentials:

- GitHub repository creation and Pages settings.
- Any private API keys or paid research databases.
- Approval of quarterly theme, table of contents, commissioned article list, theses, dossiers, final English text, final Korean text, and publication merge.
- Final legal review of licensing and copyright policy.
- Human review of sensitive political concepts and contested claims.
