#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

from lib import ISSUES, article_paths, iso_today, quarter_for, read_front_matter, read_text, slugify, write_text


def headings(path):
    if not path.exists():
        return []
    return re.findall(r"^##+\s+(.+)$", read_text(path), flags=re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()
    slug = slugify(args.slug)
    en, ko = article_paths(args.issue, slug)
    problems = []
    if not en.exists():
        problems.append("missing English final article")
    if not ko.exists():
        problems.append("missing Korean final article")
    en_meta = read_front_matter(en)
    ko_meta = read_front_matter(ko)
    if en_meta and ko_meta:
        if en_meta.get("slug") != ko_meta.get("slug"):
            problems.append("slug mismatch")
        if en_meta.get("counterpart_url") != f"/ko/{slug}/":
            problems.append("English counterpart_url mismatch")
        if ko_meta.get("counterpart_url") != f"/en/{slug}/":
            problems.append("Korean counterpart_url mismatch")
        if len(headings(en)) != len(headings(ko)):
            problems.append("heading count differs")
    status = "blocked" if problems else "checked"
    text = f"""---
issue: "{args.issue}"
slug: "{slug}"
date: "{iso_today()}"
status: "{status}"
---

# Bilingual Consistency Check: {slug}

## Result

{status}

## Problems

{chr(10).join(f'- {p}' for p in problems) if problems else '- None detected by structural check.'}

## Manual Review Still Required

- Thesis preservation
- Nuance and qualification preservation
- Citation equivalence
- Korean prose quality
- English prose quality
"""
    target = ISSUES / args.issue / "reviews" / f"{slug}_bilingual_check.md"
    write_text(target, text, overwrite=True)
    print(target)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

