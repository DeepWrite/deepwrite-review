#!/usr/bin/env python3
from __future__ import annotations

from lib import ROOT, bundle_command, run


def main() -> int:
    return run([bundle_command(), "exec", "jekyll", "build", "--source", "site", "--destination", "docs"], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
