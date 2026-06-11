#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, TEMPLATES, iso_today, quarter_for, read_text, require_issue_dirs, slugify, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    slug = slugify(args.slug)
    require_issue_dirs(args.issue)
    text = read_text(TEMPLATES / "dossier_template.md")
    text = text.replace("YYYY-QN", args.issue).replace("todo-slug", slug).replace("YYYY-MM-DD", iso_today())
    if args.title:
        text = text.replace("TODO", args.title, 1)
    target = ISSUES / args.issue / "source_dossiers" / f"{slug}.md"
    created = write_text(target, text, overwrite=args.force)
    print(f"{'created' if created else 'exists'}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

