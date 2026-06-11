#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, dump_front_matter, iso_today, quarter_for, read_front_matter, read_text, require_issue_dirs, slugify, split_front_matter, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--source-language", choices=["en", "ko"], default="en")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    slug = slugify(args.slug)
    target_lang = "ko" if args.source_language == "en" else "en"
    source = ISSUES / args.issue / "final" / args.source_language / f"{slug}.md"
    if not source.exists():
        source = ISSUES / args.issue / "drafts" / args.source_language / f"{slug}.md"
    if not source.exists():
        print(f"missing source article: {source}")
        return 2
    meta, _body = split_front_matter(read_text(source))
    if meta.get("chief_editor_status") != "approved_for_translation" and not args.force:
        print("blocked: source article is not approved_for_translation. Use --force only to create a clearly marked translation scaffold.")
        return 3
    require_issue_dirs(args.issue)
    meta.update(
        {
            "language": target_lang,
            "translation_of": f"/{args.source_language}/{slug}/",
            "counterpart_url": f"/{args.source_language}/{slug}/",
            "translation_status": "not_started",
            "chief_editor_status": "proposed",
            "status": "draft",
            "date": iso_today(),
        }
    )
    title = "TODO: Korean translation title" if target_lang == "ko" else "TODO: English translation title"
    body = f"""# {title}

> Translation scaffold only. Do not publish.

## Translation Work

TODO: Produce a polished {target_lang} version preserving thesis, structure, evidence, citations, and qualifications.

## Terminology Notes

- TODO.

## Translation Risks

- TODO.
"""
    target = ISSUES / args.issue / "drafts" / target_lang / f"{slug}.md"
    created = write_text(target, dump_front_matter(meta, body), overwrite=args.force)
    print(f"{'created' if created else 'exists'}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

