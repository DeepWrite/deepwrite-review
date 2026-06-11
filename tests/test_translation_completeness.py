from __future__ import annotations

from pathlib import Path

from lib import read_front_matter


ROOT = Path(__file__).resolve().parents[1]


def test_public_translations_are_checked():
    for path in (ROOT / "site" / "_articles").glob("*/*.md"):
        meta = read_front_matter(path)
        if meta.get("status") == "published":
            assert meta.get("translation_status") in {"checked", "not_applicable"}, path
            assert meta.get("translation_of") is not None, path

