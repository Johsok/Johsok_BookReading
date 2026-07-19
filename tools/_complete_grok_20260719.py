# -*- coding: utf-8 -*-
"""Write Grok highlight results via findbook_writer.complete."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_writer  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    args = parser.parse_args()
    ns = argparse.Namespace(
        root=str(ROOT),
        results=args.results,
        category_id=None,
        category_file=None,
    )
    return findbook_writer.complete(ns)


if __name__ == "__main__":
    raise SystemExit(main())
