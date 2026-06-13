from __future__ import annotations

import csv
from pathlib import Path

from lib import is_public_article_meta, read_front_matter

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
PUBLIC_VERIFICATION_STATUSES = {"checked", "checked_for_temporary_publication"}


def test_evidence_logs_have_required_columns():
    for path in (ROOT / "issues").glob("*-Q[1-4]/evidence_log.csv"):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
        assert REQUIRED_COLUMNS.issubset(set(header)), path


def test_public_articles_have_public_evidence_rows():
    for issue_dir in (ROOT / "issues").glob("*-Q[1-4]"):
        evidence_path = issue_dir / "evidence_log.csv"
        if not evidence_path.exists():
            continue
        with evidence_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        public_slugs = set()
        for article in (issue_dir / "final").glob("*/*.md"):
            meta = read_front_matter(article)
            if is_public_article_meta(meta):
                public_slugs.add(meta.get("slug") or article.stem)

        for slug in public_slugs:
            slug_rows = [row for row in rows if row.get("article_slug") == slug]
            assert slug_rows, f"{issue_dir.name}/{slug} has no evidence log rows"
            for row in slug_rows:
                assert row.get("verification_status") in PUBLIC_VERIFICATION_STATUSES, row
                assert row.get("source_url"), row
                assert row.get("limitations"), row
