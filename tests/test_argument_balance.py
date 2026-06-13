from __future__ import annotations

from pathlib import Path

from lib import is_public_article_meta, read_front_matter, read_text


ROOT = Path(__file__).resolve().parents[1]

OPPOSITION_MARKERS = (
    "strongest objection",
    "strongest opposing view",
    "strongest good-faith objection",
    "가장 강한 반론",
    "가장 강한 반대 견해",
)

EVIDENCE_DISCIPLINE_MARKERS = (
    "overall evidence level",
    "high-confidence claims",
    "전체 근거 수준",
    "전체 증거 수준",
    "높은 확신",
)


def test_major_published_articles_include_opposition_and_evidence_discipline():
    for path in (ROOT / "issues").glob("*-Q[1-4]/final/*/*.md"):
        meta = read_front_matter(path)
        if not is_public_article_meta(meta):
            continue
        text = read_text(path).lower()
        assert any(marker in text for marker in OPPOSITION_MARKERS), path
        assert any(marker in text for marker in EVIDENCE_DISCIPLINE_MARKERS), path
