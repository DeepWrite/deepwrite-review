#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import CONFIG, ISSUES, RADAR, iso_today, load_yaml, quarter_for, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    args = parser.parse_args()
    config = load_yaml(CONFIG / "magazine.yml")
    domains = config["domains"]
    themes = config["general_issue_themes"]
    rows = []
    for idx in range(30):
        domain = domains[idx % len(domains)]
        theme = themes[idx % len(themes)]
        rows.append(
            f"""## {idx + 1}. {theme}

- Domain: {domain}
- Why now: TODO, verify against current-quarter evidence.
- Structural importance: TODO.
- Public importance: TODO.
- Evidence availability: TODO, source dossier required.
- Likely ideological disputes: TODO.
- Possible article type: TODO.
- Preliminary source types: Tier 1 and Tier 2 required.
- Risk of cliche or overstatement: TODO.
- Recommendation: monitor
"""
        )
    text = f"""---
issue: "{args.issue}"
date: "{iso_today()}"
status: proposed
chief_editor_status: proposed
---

# {args.issue} Candidate Topics

These are structural topic prompts, not verified contemporary claims. Before commissioning, each candidate requires live source review, Chief Editor judgment, and a source dossier.

{chr(10).join(rows)}
"""
    issue_target = ISSUES / args.issue / "agenda.md"
    radar_target = RADAR / "quarterly" / f"{args.issue}-candidate-agenda.md"
    write_text(issue_target, text, overwrite=True)
    write_text(radar_target, text, overwrite=True)
    print(issue_target)
    print(radar_target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
