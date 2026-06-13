from __future__ import annotations

import csv
import datetime as dt
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
ISSUES = ROOT / "issues"
RADAR = ROOT / "radar"
TEMPLATES = ROOT / "templates"
SITE = ROOT / "site"
DOCS = ROOT / "docs"

APPROVAL_SEQUENCE = [
    "proposed",
    "commissioned",
    "approved_for_draft",
    "approved_for_review",
    "approved_for_translation",
    "approved_for_temporary_publication",
    "approved_for_publication",
]

PUBLIC_ARTICLE_STATUSES = {"temporary_publication", "published"}
TEMPORARY_PUBLICATION_STATUSES = {"temporary_publication"}
FINAL_PUBLICATION_STATUSES = {"published"}
TEMPORARY_APPROVAL_STATUSES = {"approved_for_temporary_publication"}
FINAL_APPROVAL_STATUSES = {"approved_for_publication"}
TEMPORARY_CHECK_STATUSES = {"checked_for_temporary_publication"}
FINAL_CHECK_STATUSES = {"checked"}


def today() -> dt.date:
    return dt.date.today()


def quarter_for(date: dt.date | None = None) -> str:
    date = date or today()
    quarter = (date.month - 1) // 3 + 1
    return f"{date.year}-Q{quarter}"


def iso_today() -> str:
    return today().isoformat()


def week_id(date: dt.date | None = None) -> str:
    date = date or today()
    iso = date.isocalendar()
    return f"{iso.year}-{iso.week:02d}"


def month_id(date: dt.date | None = None) -> str:
    date = date or today()
    return f"{date.year}-{date.month:02d}"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool = False) -> bool:
    ensure_dir(path.parent)
    if path.exists() and not overwrite:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    return yaml.safe_load(raw) or {}, body


def read_front_matter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    meta, _body = split_front_matter(read_text(path))
    return meta


def dump_front_matter(meta: dict[str, Any], body: str) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n" + body.lstrip()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9가-힣]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def require_issue_dirs(issue: str) -> Path:
    base = ISSUES / issue
    for subdir in [
        "source_dossiers",
        "drafts",
        "drafts/en",
        "drafts/ko",
        "reviews",
        "final",
        "final/en",
        "final/ko",
    ]:
        ensure_dir(base / subdir)
    return base


def article_paths(issue: str, slug: str) -> tuple[Path, Path]:
    return ISSUES / issue / "final" / "en" / f"{slug}.md", ISSUES / issue / "final" / "ko" / f"{slug}.md"


def is_publishable_article(path: Path) -> tuple[bool, list[str]]:
    meta = read_front_matter(path)
    problems: list[str] = []
    status = meta.get("status")
    chief_status = meta.get("chief_editor_status")
    publication_stage = meta.get("publication_stage")
    citation_status = meta.get("citation_status")
    translation_status = meta.get("translation_status")

    if status in TEMPORARY_PUBLICATION_STATUSES:
        if chief_status not in TEMPORARY_APPROVAL_STATUSES:
            problems.append("temporary article is not approved_for_temporary_publication")
        if publication_stage != "temporary":
            problems.append("temporary article publication_stage is not temporary")
        if citation_status not in TEMPORARY_CHECK_STATUSES | FINAL_CHECK_STATUSES:
            problems.append("temporary article citation_status is not temporary-checked")
        if meta.get("language") in ("en", "ko") and translation_status not in TEMPORARY_CHECK_STATUSES | FINAL_CHECK_STATUSES:
            problems.append("temporary article translation_status is not temporary-checked")
    elif status in FINAL_PUBLICATION_STATUSES:
        if chief_status not in FINAL_APPROVAL_STATUSES:
            problems.append("published article is not approved_for_publication")
        if publication_stage not in (None, "", "final"):
            problems.append("published article publication_stage is not final")
        if citation_status not in FINAL_CHECK_STATUSES:
            problems.append("published article citation_status is not checked")
        if meta.get("language") in ("en", "ko") and translation_status not in FINAL_CHECK_STATUSES | {"not_applicable"}:
            problems.append("published article translation_status is not checked or not_applicable")
    else:
        problems.append("status is not a public article status")

    if meta.get("evidence_level") in (None, "", "unassigned"):
        problems.append("evidence_level is unassigned")
    return not problems, problems


def is_public_article_meta(meta: dict[str, Any]) -> bool:
    status = meta.get("status")
    chief_status = meta.get("chief_editor_status")
    if status in TEMPORARY_PUBLICATION_STATUSES:
        return chief_status in TEMPORARY_APPROVAL_STATUSES
    if status in FINAL_PUBLICATION_STATUSES:
        return chief_status in FINAL_APPROVAL_STATUSES
    return False


def iter_issue_articles(stage: str = "final") -> list[Path]:
    files: list[Path] = []
    for issue_dir in sorted(ISSUES.glob("*-Q[1-4]")):
        for lang in ("en", "ko"):
            files.extend(sorted((issue_dir / stage / lang).glob("*.md")))
    return files


def copy_approved_articles_to_site() -> list[Path]:
    copied: list[Path] = []
    for path in iter_issue_articles("final"):
        ok, _problems = is_publishable_article(path)
        if not ok:
            continue
        meta = read_front_matter(path)
        lang = meta.get("language")
        slug = meta.get("slug") or path.stem
        target = SITE / "_articles" / lang / f"{slug}.md"
        ensure_dir(target.parent)
        shutil.copyfile(path, target)
        copied.append(target)
    return copied


def append_csv_row(path: Path, fieldnames: list[str], row: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def run(command: list[str], cwd: Path | None = None) -> int:
    return subprocess.call(command, cwd=str(cwd or ROOT))


def bundle_command() -> str:
    env_bundle = os.environ.get("BUNDLE_BIN")
    if env_bundle:
        return env_bundle
    homebrew_bundle = Path("/opt/homebrew/opt/ruby/bin/bundle")
    if homebrew_bundle.exists():
        return str(homebrew_bundle)
    found = shutil.which("bundle")
    if found:
        return found
    return "bundle"
