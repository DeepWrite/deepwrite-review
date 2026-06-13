from __future__ import annotations

from pathlib import Path

from lib import is_public_article_meta, read_front_matter, read_text


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PUBLIC_REVIEW_LANGUAGE = [
    "This draft",
    "The draft should",
    "Final review should",
    "Final fact-check should",
    "이 초안",
    "최종 검토 단계",
    "최종 사실검증 단계",
]


def article_files():
    return list((ROOT / "issues").glob("*-Q[1-4]/final/*/*.md")) + list((ROOT / "site" / "_articles").glob("*/*.md"))


def test_publishable_articles_have_checked_citations_and_no_placeholders():
    for path in article_files():
        meta = read_front_matter(path)
        text = read_text(path)
        if is_public_article_meta(meta):
            assert meta.get("citation_status") in {"checked", "checked_for_temporary_publication"}, path
            assert "TODO" not in text, path
            assert "fabricated" not in text.lower(), path
            for phrase in FORBIDDEN_PUBLIC_REVIEW_LANGUAGE:
                assert phrase not in text, f"{path} exposes internal review language {phrase!r}"
