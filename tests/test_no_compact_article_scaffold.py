from __future__ import annotations

from pathlib import Path

from lib import read_text


ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN_PUBLIC_PHRASES = [
    "Final Reporting Path",
    "최종 취재 경로",
    "A stronger final version should",
    "final version should",
    "temporary publication is not a loophole",
    "임시 발행은 검토를 우회",
]

FORBIDDEN_GENERATED_HEADINGS = [
    "## Opening Issue",
    "## Central Question",
    "## Conceptual Clarification",
    "## Evidence",
    "## Competing Interpretations",
    "## Policy Or Civic Implications",
    "## Citations",
    "## Best Opposing View",
    "## Argument",
    "## Evidence Strength",
    "## Uncertainty Note",
    "## Further Reading",
    "## 가장 강한 반론",
    "## 주장",
    "## 근거 강도",
    "## 불확실성 노트",
    "## 더 읽을 자료",
    "## 정책적·시민적 함의",
]

FORBIDDEN_GENERATED_HEADING_SET = set(FORBIDDEN_GENERATED_HEADINGS)


def test_compact_generation_functions_are_retired():
    for path in (ROOT / "pipelines").glob("*.py"):
        text = read_text(path)
        assert "make_compact_en" not in text, path
        assert "make_compact_ko" not in text, path


def test_independent_rewrite_pipeline_does_not_emit_generic_headings():
    text = read_text(ROOT / "pipelines" / "rewrite_2026_q2_independent_articles.py")
    for line in text.splitlines():
        assert line.strip() not in FORBIDDEN_GENERATED_HEADING_SET


def test_q2_article_files_do_not_retain_generic_headings():
    article_roots = [
        ROOT / "issues" / "2026-Q2" / "drafts",
        ROOT / "issues" / "2026-Q2" / "final",
        ROOT / "site" / "_articles",
    ]
    for root in article_roots:
        for path in root.glob("*/*.md"):
            for line in read_text(path).splitlines():
                assert line.strip() not in FORBIDDEN_GENERATED_HEADING_SET, path


def test_public_articles_do_not_expose_reporting_path_notes():
    public_roots = [
        ROOT / "issues" / "2026-Q2" / "final",
        ROOT / "site" / "_articles",
    ]
    for root in public_roots:
        for path in root.glob("*/*.md"):
            text = read_text(path)
            for phrase in FORBIDDEN_PUBLIC_PHRASES:
                assert phrase not in text, f"{path} exposes {phrase!r}"


def test_public_pages_do_not_show_stale_issue_state():
    public_pages = [
        ROOT / "site" / "pages" / "index.md",
        ROOT / "site" / "pages" / "archive.md",
        ROOT / "site" / "pages" / "current.md",
    ]
    stale_phrases = [
        "drafting pending",
        "publication pending",
        "the rest of the issue remains in production",
    ]
    for path in public_pages:
        text = read_text(path)
        for phrase in stale_phrases:
            assert phrase not in text, f"{path} exposes stale issue state {phrase!r}"
