#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import CONFIG, RADAR, iso_today, load_yaml, write_text


def build_daily_scan(cadence: str, allow_network: bool) -> str:
    sources = load_yaml(CONFIG / "sources.yml")
    source_names = []
    for group in sources.get("seed_sources", {}).values():
        for source in group:
            source_names.append(f"- {source['name']} ({source['url']})")
    live_note = "Live network scan enabled." if allow_network else "Live network scan not run; source discovery requires configured credentials or explicit network research."
    return f"""---
date: "{iso_today()}"
cadence: "{cadence}"
status: research_stub
verification_status: unverified
---

# Editorial Radar Scan: {iso_today()}

{live_note}

This file is a collection stub. It does not assert facts, statistics, or developments.

## Signal

- TODO: Add structurally important developments after verified source review.

## Noise

- TODO: Add viral but shallow controversies to ignore.

## Discourse

- TODO: Add serious magazine, journal, and expert debates.

## Evidence

- TODO: Add primary sources, datasets, law, institutional reports, and peer-reviewed literature.

## Editorial Opportunities

- TODO: Add issue-card candidates.

## Seed Sources To Check

{chr(10).join(source_names)}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadence", choices=["daily", "weekly"], default="daily")
    parser.add_argument("--allow-network", action="store_true")
    args = parser.parse_args()
    target = RADAR / args.cadence / f"{iso_today()}.md"
    write_text(target, build_daily_scan(args.cadence, args.allow_network), overwrite=True)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

