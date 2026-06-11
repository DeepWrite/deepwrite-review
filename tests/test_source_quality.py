from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_source_hierarchy_has_required_tiers():
    data = yaml.safe_load((ROOT / "config" / "sources.yml").read_text(encoding="utf-8"))
    hierarchy = data["source_hierarchy"]
    assert {"tier_1", "tier_2", "tier_3", "tier_4"}.issubset(hierarchy)
    assert "discourse" in hierarchy["tier_4"]["prohibition"].lower()


def test_magazine_requires_primary_sources_for_major_work():
    policy = (ROOT / "config" / "source_policy.md").read_text(encoding="utf-8")
    assert "No major article may rely only on opinion pieces" in policy
    assert "Tier 1" in policy

