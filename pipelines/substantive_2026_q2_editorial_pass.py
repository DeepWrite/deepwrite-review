#!/usr/bin/env python3
from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write(
        "This pipeline was retired on 2026-06-12 because it generated repeated "
        "compact article bodies through shared body-builder functions. Use "
        "pipelines/rewrite_2026_q2_independent_articles.py instead.\n"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
