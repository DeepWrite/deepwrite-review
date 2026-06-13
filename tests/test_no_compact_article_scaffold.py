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


def test_compact_generation_functions_are_retired():
    for path in (ROOT / "pipelines").glob("*.py"):
        text = read_text(path)
        assert "make_compact_en" not in text, path
        assert "make_compact_ko" not in text, path


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
