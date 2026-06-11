#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, TEMPLATES, iso_today, quarter_for, read_text, require_issue_dirs, slugify, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--slug", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    slug = slugify(args.slug)
    require_issue_dirs(args.issue)
    rubric = read_text(TEMPLATES / "review_rubric.md")
    text = f"""---
issue: "{args.issue}"
slug: "{slug}"
date: "{iso_today()}"
status: draft
---

# Review: {slug}

{rubric}

## Fact Checker

- TODO.

## Statistics Checker

- TODO.

## Dissent Editor

- TODO.

## Style Editor

- TODO.
"""
    target = ISSUES / args.issue / "reviews" / f"{slug}_review.md"
    created = write_text(target, text, overwrite=args.force)
    print(f"{'created' if created else 'exists'}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

