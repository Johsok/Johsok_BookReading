# -*- coding: utf-8 -*-
"""Fix batch60 highlight lists and write remaining books."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools._gen_batch60 import (  # noqa: E402
    BOOK27,
    BOOK28,
    BOOK29,
    BOOK30,
    BOOKS,
    run_writer,
    write_results,
)

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

REPLACEMENTS = {
    "距離改變倫理：太近可能侵犯，太遠可能把人變成風景。": "距離會改變倫理判斷，太近可能侵犯，太遠則可能把人變成風景。",
    "曖昧迫使思考：確定答案太快，影像就退化成標語。": "曖昧會迫使觀者思考，若確定答案太快，影像就退化成標語。",
    "勞動史需要完整節奏：準備、施力、休息與結束。": "勞動史需要完整節奏，涵蓋準備、施力、休息與結束。",
    "站邊問題無法迴避：中立姿態常常只是隱藏立場。": "站邊問題無法迴避，因為中立姿態常常只是隱藏立場。",
    "生存條件寫進姿態：彎腰角度、步伐與握工具方式皆披露處境。": "生存條件寫進姿態之中，彎腰角度、步伐與握工具方式皆披露處境。",
    "反覆相遇改變影像倫理：從掠取轉向共同製作意義。": "反覆相遇會改變影像倫理，使關係從掠取轉向共同製作意義。",
    "戰爭與封鎖反覆考驗廚房：如何用更少材料維持熟悉味道。": "戰爭與封鎖反覆考驗廚房，逼出用更少材料維持熟悉味道的方法。",
    "季節性極端明顯：夏日莓果爆發與冬日根菜依賴形成對照。": "季節性極端明顯，夏日莓果爆發與冬日根菜依賴形成強烈對照。",
    "魚湯傳統反映河流文明：淡水魚與香料草的搭配極具地方性。": "魚湯傳統反映河流文明，淡水魚與香料草的搭配極具地方性。",
    "保存即交通：沒有鹽與煙，距離會重新變成飢餓。": "保存技術等同交通能力，沒有鹽與煙時距離會重新變成飢餓。",
    "旅行意義依靠差異：每座城鎮的酸度與煙味都不該一樣。": "旅行意義依靠差異本身，每座城鎮的酸度與煙味都不該一樣。",
    "無名死亡提醒檔案政治：誰被記錄，誰就較可能被紀念。": "無名死亡提醒人們正視檔案政治，誰被記錄，誰就較可能被紀念。",
    "和平年代仍支付戰爭利息：殘疾、寡婦家庭與教育落差。": "和平年代仍在支付戰爭利息，表現為殘疾、寡婦家庭與教育落差。",
    "倫理光譜提醒讀者：理解求生並非自動赦免所有選擇。": "倫理光譜提醒讀者理解求生並非自動赦免所有選擇。",
    "名義負責人現象說明：要懂明代行政，必須看見吏與幕。": "名義負責人現象說明要懂明代行政就必須看見吏與幕。",
    "文本即工具：同一律例在不同帖式下可寬可猛。": "文本本身就是治理工具，同一律例在不同帖式下可寬可猛。",
    "譴責人心不如重繪流程：誰簽署、誰稽核、誰可被追償。": "譴責人心不如重繪流程，釐清誰簽署、誰稽核、誰可被追償。",
}


def scrub(lines: list[str]) -> list[str]:
    out: list[str] = []
    for x in lines:
        x = x.strip()
        if "ethno" in x or "不對；延續家族" in x:
            x = "私下祭祖延續家族時間觀，用以對抗佔領當局強加的日曆。"
        if "overlay" in x:
            x = "軍事史與行政史切開後，敗因分析會停在將領性格而忽略後勤文書。"
        x = REPLACEMENTS.get(x, x)
        match = re.match(r"^([^：:]{1,12})[：:](.*)$", x)
        if match and not match.group(1).endswith(NATURAL):
            x = match.group(1) + "，" + match.group(2)
        out.append(x)
    seen: set[str] = set()
    uniq: list[str] = []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def fit150(lines: list[str], fillers: list[str] | None = None) -> list[str]:
    lines = list(lines)
    fillers = fillers or []
    while len(lines) > 150:
        lines.pop()
    for filler in fillers:
        if len(lines) >= 150:
            break
        if filler not in lines:
            lines.append(filler)
    if len(lines) != 150:
        raise SystemExit(f"len={len(lines)}")
    fixed: list[str] = []
    for x in lines:
        match = re.match(r"^([^：:]{1,12})[：:](.*)$", x)
        if match and not match.group(1).endswith(NATURAL):
            x = match.group(1) + "，" + match.group(2)
        if re.search(r"[A-Za-z]{3,}", x):
            raise SystemExit("eng: " + x)
        fixed.append(x)
    return fixed


def main() -> None:
    fill27 = [
        "共同製作意義時，被攝者不再只是材料，而成為敘事的共同作者。",
        "流通同意若被忽視，一張善意照片也可能在網絡上變成傷害工具。",
        "完成影像敘事的最後一步，是讓被再現者有機會看見並回應成品。",
    ]
    mapping = {
        "07_other-20260718-27": fit150(scrub(BOOK27), fill27),
        "07_other-20260718-28": fit150(scrub(BOOK28)),
        "07_other-20260718-29": fit150(scrub(BOOK29)),
        "07_other-20260718-30": fit150(scrub(BOOK30)),
    }

    written: list[str] = []
    failures: list[tuple[str, str]] = []
    for book in BOOKS:
        book_id = book["id"]
        if book_id not in mapping:
            continue
        try:
            path = write_results(book_id, mapping[book_id], book["title"], book["author"])
            run_writer(book["categoryId"], path)
            written.append(book_id)
            print("OK", book_id)
        except Exception as exc:  # noqa: BLE001
            failures.append((book_id, str(exc)))
            print("FAIL", book_id, exc)

    print("WRITTEN", written)
    print("FAILURES", failures)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
