from __future__ import annotations

from pathlib import Path

from lib import read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def test_published_articles_have_stable_counterpart_links():
    articles = {}
    for path in (ROOT / "site" / "_articles").glob("*/*.md"):
        meta = read_front_matter(path)
        if meta.get("status") == "published":
            articles[(meta.get("language"), meta.get("slug"))] = meta

    for (language, slug), meta in articles.items():
        other = "ko" if language == "en" else "en"
        assert (other, slug) in articles, f"missing counterpart for {language}/{slug}"
        assert meta.get("counterpart_url") == f"/{other}/{slug}/"

