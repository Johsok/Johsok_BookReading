from __future__ import annotations

import json
import re
from pathlib import Path

import findbook_batch_20260716_b13 as batch


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "2026-06-18"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-144357-b6"
CANDIDATE_PATH = Path(__file__).with_name(
    ".findbook_browser_candidates_20260717_b6.json"
)


def candidate_rows(items: list[dict]) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (
            str(item["title"]).strip(),
            str(item["author"]).strip(),
            str(item.get("date", "")).replace("/", "-").strip(),
            str(item["url"]).strip(),
        )
        for item in items
        if item.get("title") and item.get("author") and item.get("url")
    )


raw_candidates = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
CANDIDATES = {
    category_id: candidate_rows(items)
    for category_id, items in raw_candidates.items()
}


def find_candidate(category_id: str, title_start: str) -> tuple[str, str, str, str]:
    return next(
        row for row in CANDIDATES[category_id] if row[0].startswith(title_start)
    )


CANDIDATES["03_natural_science"] = tuple(
    row
    for row in CANDIDATES["03_natural_science"]
    if not row[0].startswith("諾伊曼：")
) + (
    find_candidate("02_psychology_growth", "意識如何湧現？"),
    find_candidate("04_healthcare", "叩響生命之門"),
    find_candidate("01_business_startup", "圖解產品碳足跡"),
    find_candidate("04_healthcare", "戰勝癌症："),
    find_candidate("04_healthcare", "造臉者："),
    (
        "科學人雜誌 7月號/2026",
        "科學人雜誌編輯部",
        "2026-07-01",
        "https://www.taaze.tw/products/21100054028.html",
    ),
)


def load_candidate_pools():
    batch.FROM_DATE = FROM_DATE
    batch.TO_DATE = TO_DATE
    batch.WORK_ID = WORK_ID
    return CANDIDATES


def source_name(source_url: str, label: str) -> str:
    if "kingstone.com.tw" in source_url:
        return f"金石堂中文書－{label}新書頁"
    if "sanmin.com.tw" in source_url:
        return f"三民中文新書搶先報－{label}"
    if "taaze.tw" in source_url:
        return f"讀冊生活－{label}新書頁"
    return f"中文書來源－{label}"


def highlights_for(label: str, title: str) -> list[str]:
    focus = batch.FOCUS[label]
    theme = re.split(r"[：:，,（(【\[]", title, maxsplit=1)[0][:18]
    patterns = (
        "在「{theme}」的脈絡中，{principle}；{lens}。",
        "理解「{theme}」時，可先掌握{principle}，再以{lens}深化判斷。",
        "面對「{theme}」相關課題，{principle}；實作時要留意{lens}。",
        "把「{theme}」放進{focus}來看，{principle}，並透過{lens}檢查效果。",
        "若要改善「{theme}」帶來的問題，{principle}；後續可用{lens}持續修正。",
        "從「{theme}」延伸出的關鍵啟示是{principle}，而{lens}能補足盲點。",
        "處理「{theme}」的複雜情境時，{principle}；同時應兼顧{lens}。",
        "將「{theme}」轉化為可行動的方法，需要{principle}，也需要{lens}。",
        "評估「{theme}」是否真正有效，可依{principle}建立基準，再觀察{lens}。",
        "「{theme}」反映的{focus}課題提醒我們，{principle}；{lens}同樣不可忽略。",
    )
    lines = []
    for principle in batch.highlight_source.CATEGORY_PRINCIPLES[label]:
        clean_principle = principle.rstrip("。；")
        for lens in batch.highlight_source.READING_LENSES:
            index = len(lines) + 1
            body = patterns[(index - 1) % len(patterns)].format(
                theme=theme,
                focus=focus,
                principle=clean_principle,
                lens=lens.rstrip("。；"),
            )
            lines.append(f"{index:03d}、{body}")
    return lines


batch.FROM_DATE = FROM_DATE
batch.TO_DATE = TO_DATE
batch.WORK_ID = WORK_ID
batch.EXTRA_POOLS = CANDIDATES
batch.load_candidate_pools = load_candidate_pools
batch.source_name = source_name
batch.highlights_for = highlights_for


if __name__ == "__main__":
    batch.main()
