# -*- coding: utf-8 -*-
import json
from pathlib import Path

from _hl_g11 import BODIES as B11
from _hl_g12 import BODIES as B12
from _hl_g13 import BODIES as B13
from _hl_g14 import BODIES as B14
from _hl_g04 import BODIES as B04
from findbook_writer import validate_highlights

ROOT = Path(__file__).resolve().parent


def pack(book_id: str, bodies: list[str], title: str, author: str) -> dict:
    highlights = [f"{index:03d}、{body}" for index, body in enumerate(bodies, 1)]
    validate_highlights(book_id, highlights, title, author)
    return {"id": book_id, "highlights": highlights}


def main() -> None:
    psych = [
        pack(
            "02_psychology_growth-20260830-11",
            B11,
            "我喜歡這個功利的世界：這個世上，只要你敢，再大的不可能，都會變成可能",
            "咪蒙",
        ),
        pack(
            "02_psychology_growth-20260830-12",
            B12,
            "超快速讀書法",
            "宇都出雅巳",
        ),
        pack(
            "02_psychology_growth-20260830-13",
            B13,
            "驚人的油漆式速讀術：全民必備高效率記憶工具書！",
            "吳燦銘",
        ),
        pack(
            "02_psychology_growth-20260830-14",
            B14,
            "一日一行動的奇蹟：我這樣化習慣為複利，9個月購置新屋，一年讀完520本書",
            "柳根瑢",
        ),
    ]
    health = [
        pack(
            "04_healthcare-20260830-03",
            B04,
            "即刻救牙！良心牙醫教你一口好牙咬到100歲！",
            "木野孔司、齊藤博",
        ),
    ]
    psych_path = ROOT / ".findbook_results_20260830_batchG.json"
    health_path = ROOT / ".findbook_results_20260830_batchG4.json"
    psych_path.write_text(json.dumps(psych, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    health_path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", psych_path.name, health_path.name)


if __name__ == "__main__":
    main()
