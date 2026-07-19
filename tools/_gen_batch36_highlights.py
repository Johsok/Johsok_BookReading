# -*- coding: utf-8 -*-
"""Generate findbook results JSON for batch36 and run writer complete."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def numbered(lines: list[str]) -> list[str]:
    assert len(lines) == 150, len(lines)
    out = []
    for i, body in enumerate(lines, 1):
        body = body.strip()
        assert len(body) >= 12, (i, body)
        out.append(f"{i:03d}、{body}")
    return out


def write_results(book_id: str, lines: list[str]) -> Path:
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": numbered(lines)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def run_writer(category_id: str, results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def main() -> None:
    mapping = [
        ("03_natural_science-20260718-36", 36),
        ("03_natural_science-20260718-37", 37),
        ("03_natural_science-20260718-38", 38),
        ("03_natural_science-20260718-39", 39),
        ("03_natural_science-20260718-40", 40),
    ]
    written = []
    failed = []
    for book_id, n in mapping:
        bodies = json.loads(
            (ROOT / "tools" / f"_batch36_bodies_{n}.json").read_text(encoding="utf-8")
        )
        try:
            path = write_results(book_id, bodies)
            print(f"wrote {path}")
            run_writer("03_natural_science", path)
            written.append(book_id)
        except Exception as exc:  # noqa: BLE001
            failed.append((book_id, str(exc)))
            print(f"FAIL {book_id}: {exc}")
    print("WRITTEN", written)
    print("FAILED", failed)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
