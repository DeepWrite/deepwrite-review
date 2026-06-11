from __future__ import annotations

from pathlib import Path

from lib import read_front_matter, read_text


ROOT = Path(__file__).resolve().parents[1]


def article_files():
    return list((ROOT / "issues").glob("*-Q[1-4]/final/*/*.md")) + list((ROOT / "site" / "_articles").glob("*/*.md"))


def test_publishable_articles_have_checked_citations_and_no_placeholders():
    for path in article_files():
        meta = read_front_matter(path)
        text = read_text(path)
        if meta.get("status") == "published" or meta.get("chief_editor_status") == "approved_for_publication":
            assert meta.get("citation_status") == "checked", path
            assert "TODO" not in text, path
            assert "fabricated" not in text.lower(), path

