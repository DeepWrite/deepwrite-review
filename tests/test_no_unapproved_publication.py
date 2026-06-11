from __future__ import annotations

from pathlib import Path

from lib import is_publishable_article, read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def test_public_site_contains_only_approved_articles():
    for path in (ROOT / "site" / "_articles").glob("*/*.md"):
        ok, problems = is_publishable_article(path)
        assert ok, f"{path}: {problems}"


def test_no_issue_final_article_claims_published_without_approval():
    for path in (ROOT / "issues").glob("*-Q[1-4]/final/*/*.md"):
        meta = read_front_matter(path)
        if meta.get("status") == "published":
            ok, problems = is_publishable_article(path)
            assert ok, f"{path}: {problems}"

