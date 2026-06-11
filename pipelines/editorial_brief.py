#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import RADAR, iso_today, read_text, week_id, write_text


def latest_daily_items(limit: int = 7) -> list[str]:
    files = sorted((RADAR / "daily").glob("*.md"))[-limit:]
    return [f"- `{path.name}`: {read_text(path).splitlines()[0] if path.exists() else 'missing'}" for path in files]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", default=week_id())
    args = parser.parse_args()
    items = latest_daily_items()
    target = RADAR / "weekly" / f"{args.week}-editorial-brief.md"
    text = f"""---
week: "{args.week}"
date: "{iso_today()}"
status: draft
chief_editor_status: proposed
---

# Weekly Editorial Brief: {args.week}

## Five Strongest Developments Of The Week

- TODO: Requires verified research. No development should be listed without source review.

## Three Slow-Burn Structural Trends

- TODO.

## Strongest Newly Published Reports Or Datasets

- TODO.

## Notable Arguments From Serious Magazines And Journals

- TODO.

## Topics That Deserve Chief Editor Attention

- TODO.

## Topics To Ignore Despite Online Attention

- TODO.

## Suggested Article Commissions

- TODO.

## Decisions Requested From The Chief Editor

- Decide whether any listed topic should move from monitor to develop.

## Inputs Reviewed

{chr(10).join(items) if items else '- No daily radar files found.'}
"""
    write_text(target, text, overwrite=True)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

