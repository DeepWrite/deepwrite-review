#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, TEMPLATES, iso_today, quarter_for, read_text, require_issue_dirs, slugify, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--language", choices=["en", "ko"], default="en")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    slug = slugify(args.slug)
    require_issue_dirs(args.issue)
    template = "article_template_en.md" if args.language == "en" else "article_template_ko.md"
    text = read_text(TEMPLATES / template)
    text = text.replace("YYYY-QN", args.issue).replace("todo-slug", slug).replace("YYYY-MM-DD", iso_today())
    if args.title:
        text = text.replace("TODO: English title", args.title).replace("TODO: Korean title", args.title)
        text = text.replace("TODO: English Title", args.title).replace("TODO: Korean Title", args.title)
    target = ISSUES / args.issue / "drafts" / args.language / f"{slug}.md"
    created = write_text(target, text, overwrite=args.force)
    print(f"{'created' if created else 'exists'}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

