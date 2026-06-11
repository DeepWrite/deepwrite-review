from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from lib import bundle_command


ROOT = Path(__file__).resolve().parents[1]


def test_jekyll_pages_builds():
    bundle = bundle_command()
    if shutil.which(bundle) is None and not Path(bundle).exists():
        pytest.skip("Bundler is not installed in this environment")
    result = subprocess.run(
        [bundle, "exec", "jekyll", "build", "--source", "site", "--destination", "docs"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout
