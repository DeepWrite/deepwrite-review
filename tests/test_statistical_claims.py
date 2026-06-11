from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = {
    "issue",
    "article_slug",
    "claim",
    "source_title",
    "source_url",
    "source_tier",
    "date",
    "unit",
    "geography",
    "denominator",
    "limitations",
    "evidence_level",
    "verification_status",
}


def test_evidence_logs_have_required_columns():
    for path in (ROOT / "issues").glob("*-Q[1-4]/evidence_log.csv"):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
        assert REQUIRED_COLUMNS.issubset(set(header)), path

