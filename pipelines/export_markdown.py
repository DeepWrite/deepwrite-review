#!/usr/bin/env python3
from __future__ import annotations

from lib import copy_approved_articles_to_site


def main() -> int:
    copied = copy_approved_articles_to_site()
    for path in copied:
        print(path)
    if not copied:
        print("No approved published articles exported.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

