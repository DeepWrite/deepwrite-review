from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from lib import is_public_article_meta, read_front_matter, read_text


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TEMPLATE_HEADINGS = {
    "Opening Issue",
    "Central Question",
    "Conceptual Clarification",
    "Evidence",
    "Competing Interpretations",
    "Policy Or Civic Implications",
    "Citations",
    "Best Opposing View",
    "Argument",
    "Evidence Strength",
    "Uncertainty Note",
    "Further Reading",
    "가장 강한 반론",
    "주장",
    "근거 강도",
    "불확실성 노트",
    "더 읽을 자료",
    "정책적·시민적 함의",
}


def english_final_articles() -> list[Path]:
    articles: list[Path] = []
    for path in sorted((ROOT / "issues").glob("*-Q[1-4]/final/en/*.md")):
        meta = read_front_matter(path)
        if is_public_article_meta(meta):
            articles.append(path)
    return articles


def public_english_article_copies() -> list[Path]:
    paths = english_final_articles()
    paths.extend(sorted((ROOT / "site" / "_articles" / "en").glob("*.md")))
    return paths


def public_article_copies() -> list[Path]:
    paths: list[Path] = []
    for path in sorted((ROOT / "issues").glob("*-Q[1-4]/final/*/*.md")):
        meta = read_front_matter(path)
        if is_public_article_meta(meta):
            paths.append(path)
    paths.extend(sorted((ROOT / "site" / "_articles").glob("*/*.md")))
    return paths


def h2_headings(path: Path) -> list[str]:
    return [line[3:].strip() for line in read_text(path).splitlines() if line.startswith("## ")]


def test_public_english_articles_declare_independent_agent_structure():
    for path in public_english_article_copies():
        meta = read_front_matter(path)
        assert meta.get("language") == "en", path
        assert meta.get("body_generation") == "independent_article_structure", path
        assert meta.get("assigned_agent"), path
        assert meta.get("independent_editorial_pass"), path


def test_public_articles_do_not_reuse_template_headings():
    for path in public_article_copies():
        hits = FORBIDDEN_TEMPLATE_HEADINGS.intersection(h2_headings(path))
        assert not hits, f"{path} still exposes template headings: {sorted(hits)}"


def test_final_english_heading_signatures_are_not_reused():
    signatures: dict[tuple[str, ...], list[Path]] = defaultdict(list)
    for path in english_final_articles():
        signatures[tuple(h2_headings(path))].append(path)

    duplicates = {signature: paths for signature, paths in signatures.items() if len(paths) > 1}
    assert not duplicates


def test_independent_dossier_and_review_match_assigned_agent():
    for article_path in english_final_articles():
        article_meta = read_front_matter(article_path)
        issue = article_meta["issue"]
        slug = article_meta["slug"]
        assigned_agent = article_meta["assigned_agent"]

        dossier = ROOT / "issues" / issue / "source_dossiers" / f"{slug}.md"
        review = ROOT / "issues" / issue / "reviews" / f"{slug}_review.md"

        dossier_meta = read_front_matter(dossier)
        review_meta = read_front_matter(review)

        assert dossier_meta.get("status") == "independent_rewrite_dossier", dossier
        assert dossier_meta.get("assigned_agent") == assigned_agent, dossier
        assert review_meta.get("status") == "independent_rewrite_checked", review
        assert review_meta.get("assigned_agent") == assigned_agent, review
