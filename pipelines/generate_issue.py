#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lib import ISSUES, TEMPLATES, iso_today, quarter_for, read_text, require_issue_dirs, write_text


def issue_files(issue: str) -> dict[str, str]:
    return {
        "agenda.md": f"""---
issue: "{issue}"
status: proposed
chief_editor_status: proposed
created: "{iso_today()}"
---

# {issue} Candidate Agenda

No theme, table of contents, commissioned article list, thesis, source dossier, draft, translation, or publication decision is approved yet.

Run:

```bash
python3 pipelines/select_topics.py --issue {issue}
```
""",
        "chief_editor_decisions.md": f"""---
issue: "{issue}"
status: active
chief_editor: "Jeyoun Son"
chief_editor_ko: "손제연"
---

# Chief Editor Decisions

Silence is not approval. Use `approve`, `revise`, `reject`, or `hold`.

## Quarterly Theme

- Decision: hold
- Date:
- Notes:

## Final Table Of Contents

- Decision: hold
- Date:
- Notes:

## Commissioned Article List

- Decision: hold
- Date:
- Notes:

## Publication Merge

- Decision: hold
- Date:
- Notes:
""",
        "issue_en.md": f"""---
issue: "{issue}"
language: en
title: "DeepWrite Review {issue}"
chief_editor_status: proposed
status: draft
---

# DeepWrite Review {issue}

Draft issue scaffold. No article is approved for publication.
""",
        "issue_ko.md": f"""---
issue: "{issue}"
language: ko
title: "DeepWrite Review {issue}"
chief_editor_status: proposed
status: draft
---

# DeepWrite Review {issue}

초안용 호 골격입니다. 발행 승인된 글은 없습니다.
""",
        "bibliography.bib": "% Add only verified sources. Do not add fabricated citations.\n",
        "factcheck_report.md": f"---\nissue: \"{issue}\"\nstatus: not_started\n---\n\n# Fact-Check Report\n\nNo submitted article yet.\n",
        "statistics_report.md": f"---\nissue: \"{issue}\"\nstatus: not_started\n---\n\n# Statistical Reliability Report\n\nNo submitted statistical claims yet.\n",
        "translation_report.md": f"---\nissue: \"{issue}\"\nstatus: not_started\n---\n\n# Translation Consistency Report\n\nNo submitted translations yet.\n",
        "uncertainty_note.md": f"---\nissue: \"{issue}\"\nstatus: draft\n---\n\n# Issue Uncertainty Note\n\n- TODO.\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    base = require_issue_dirs(args.issue)
    for relative, content in issue_files(args.issue).items():
        write_text(base / relative, content, overwrite=args.force)
    evidence_template = read_text(TEMPLATES / "evidence_log_template.csv")
    write_text(base / "evidence_log.csv", evidence_template, overwrite=args.force)
    print(f"Issue scaffold ready: {base.relative_to(ISSUES.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
