# -*- coding: utf-8 -*-
"""Write batch77 bodies via findbook_writer."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODIES = ROOT / "tools" / "_batch77_bodies"

BOOKS = [
    {
        "id": "04_healthcare-20260718-36",
        "categoryId": "04_healthcare",
        "title": "激素平衡瘦身課(限量附贈【14天代謝調整課表】)：啟動代謝重建，瘦得健康持久",
        "author": "許書華",
    },
    {
        "id": "04_healthcare-20260718-37",
        "categoryId": "04_healthcare",
        "title": "看透醫學謊言，找到代謝真相：逆轉肥胖、高血壓、脂肪肝，讓身體健康長壽的自救指南",
        "author": "羅伯特．勒夫金 丁亦",
    },
    {
        "id": "04_healthcare-20260718-38",
        "categoryId": "04_healthcare",
        "title": "輕鬆當爸媽，孩子更健康【最新增修版】：超人氣小兒科醫師黃瑽寧教你安心育兒",
        "author": "黃瑽寧",
    },
    {
        "id": "04_healthcare-20260718-39",
        "categoryId": "04_healthcare",
        "title": "讀懂身體的訊號：基因醫師教你逆轉健康危機",
        "author": "張家銘",
    },
    {
        "id": "04_healthcare-20260718-40",
        "categoryId": "04_healthcare",
        "title": "科學實證有效的休息100招攻略：用最短時間快速提升專注力、恢復體力和身心健康",
        "author": "加藤浩晃 陳欣如",
    },
]


def main() -> None:
    written = []
    failures = []
    for book in BOOKS:
        book_id = book["id"]
        try:
            bodies = [
                line.strip()
                for line in (BODIES / f"{book_id}.txt").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            assert len(bodies) == 150, len(bodies)
            highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
            results_path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
            results_path.write_text(
                json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )
            cmd = [
                sys.executable,
                str(ROOT / "tools" / "findbook_writer.py"),
                "complete",
                "--category-id",
                book["categoryId"],
                "--results",
                str(results_path),
            ]
            print("RUN", book_id)
            subprocess.run(cmd, cwd=str(ROOT), check=True)
            written.append(book_id)
        except Exception as exc:  # noqa: BLE001
            failures.append((book_id, str(exc)))
            print("FAIL", book_id, exc)
    print("SUCCESS", written)
    print("FAILURE", failures)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
