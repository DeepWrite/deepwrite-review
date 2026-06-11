#!/usr/bin/env python3
from __future__ import annotations

from lib import ROOT, run


def main() -> int:
    return run(["python3", "-m", "pytest"], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())

