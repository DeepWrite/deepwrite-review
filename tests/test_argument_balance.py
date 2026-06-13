from __future__ import annotations

from pathlib import Path

from lib import is_public_article_meta, read_front_matter, read_text


ROOT = Path(__file__).resolve().parents[1]


def test_major_published_articles_include_opposing_view_and_evidence_strength():
    for path in (ROOT / "issues").glob("*-Q[1-4]/final/*/*.md"):
        meta = read_front_matter(path)
        if not is_public_article_meta(meta):
            continue
        text = read_text(path).lower()
        assert "best opposing view" in text or "가장 강한 반론" in text, path
        assert "evidence strength" in text or "근거 강도" in text, path
