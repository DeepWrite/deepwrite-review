from __future__ import annotations

from pathlib import Path

from lib import is_public_article_meta, is_publishable_article, read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def test_public_site_contains_only_approved_articles():
    for path in (ROOT / "site" / "_articles").glob("*/*.md"):
        ok, problems = is_publishable_article(path)
        assert ok, f"{path}: {problems}"


def test_no_issue_final_article_claims_published_without_approval():
    for path in (ROOT / "issues").glob("*-Q[1-4]/final/*/*.md"):
        meta = read_front_matter(path)
        if is_public_article_meta(meta):
            ok, problems = is_publishable_article(path)
            assert ok, f"{path}: {problems}"


def test_draft_articles_do_not_claim_publication_status():
    for path in (ROOT / "issues").glob("*-Q[1-4]/drafts/*/*.md"):
        meta = read_front_matter(path)
        assert not is_public_article_meta(meta), path
        assert meta.get("status") != "published", path
        assert meta.get("chief_editor_status") != "approved_for_publication", path
