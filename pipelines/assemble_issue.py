#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, is_publishable_article, quarter_for, read_front_matter, require_issue_dirs, write_text


def article_list(issue: str, lang: str) -> list[str]:
    rows = []
    for path in sorted((ISSUES / issue / "final" / lang).glob("*.md")):
        ok, problems = is_publishable_article(path)
        meta = read_front_matter(path)
        if ok:
            rows.append(f"- [{meta.get('title', path.stem)}](/{lang}/{meta.get('slug', path.stem)}/)")
        else:
            rows.append(f"- {path.stem}: not publishable ({'; '.join(problems)})")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    base = require_issue_dirs(args.issue)
    for lang, heading in (("en", "Table Of Contents"), ("ko", "목차")):
        rows = article_list(args.issue, lang)
        text = f"""---
issue: "{args.issue}"
language: {lang}
title: "DeepWrite Review {args.issue}"
chief_editor_status: proposed
status: draft
---

# DeepWrite Review {args.issue}

## {heading}

{chr(10).join(rows) if rows else '- No publishable articles yet.'}
"""
        write_text(base / f"issue_{lang}.md", text, overwrite=args.force or True)
    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

