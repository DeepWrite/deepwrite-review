#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import RADAR, iso_today, month_id, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", default=month_id())
    args = parser.parse_args()
    weekly = sorted((RADAR / "weekly").glob("*.md"))
    target = RADAR / "monthly" / f"{args.month}-topic-map.md"
    text = f"""---
month: "{args.month}"
date: "{iso_today()}"
status: draft
chief_editor_status: proposed
---

# Monthly Topic Map: {args.month}

## Consolidated Developments

- TODO: Consolidate verified weekly developments.

## Slow-Burn Themes

- TODO.

## Possible Issue Themes

- TODO.

## Ranked Candidate Essays

| Rank | Working Title | Domain | Evidence Availability | Recommendation |
| --- | --- | --- | --- | --- |
| 1 | TODO | TODO | TODO | monitor |

## Quarterly Candidate Pool Recommendations

- TODO.

## Weekly Briefs Reviewed

{chr(10).join(f'- `{path.name}`' for path in weekly) if weekly else '- No weekly briefs found.'}
"""
    write_text(target, text, overwrite=True)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

