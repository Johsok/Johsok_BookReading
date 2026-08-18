# -*- coding: utf-8 -*-
"""Reserve 2026-08-18 FindBook batch: 7 categories x 2 Chinese books."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
WORK_ID = "findbook-20260818-160700"
FROM_DATE = "2026-07-19"
TO_DATE = "2026-08-18"

TAGS = {
    "01_business_startup": ["商業", "投資", "創業", "理財"],
    "02_psychology_growth": ["心理", "勵志", "成長", "情緒"],
    "03_natural_science": ["科學", "自然", "科普"],
    "04_healthcare": ["醫療", "健康", "保健"],
    "05_food_wellness": ["飲食", "營養", "養生"],
    "06_computer_info": ["電腦", "程式", "AI"],
    "07_other": ["歷史", "文化", "生活"],
}

LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
}

BOOKS = {
    "01_business_startup": [
        {
            "title": "智慧通膨下的新商機：AI時代的稀缺能力與新護城河",
            "author": "程世嘉、蕭玉品",
            "sourceName": "博客來中文書商品頁－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011057622",
            "published": "2026-07-30",
            "subjects": ("AI商機", "護城河", "人機協作"),
        },
        {
            "title": "走出金錢焦慮：理解現實真相，真正消除不安",
            "author": "田內學",
            "sourceName": "灰熊愛讀書／金石堂新書－商業理財",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2015500204726/",
            "published": "2026-08-01",
            "subjects": ("金錢焦慮", "財務安全感", "社會資本"),
        },
    ],
    "02_psychology_growth": [
        {
            "title": "正是時候讀康德：寫給擁有愈多就愈不安的人，跟著康德活出平靜規律的人生",
            "author": "姜芝誾",
            "sourceName": "灰熊愛讀書／金石堂新書－心理勵志",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2011771638161/",
            "published": "2026-08-06",
            "subjects": ("自律", "日常規律", "不安"),
        },
        {
            "title": "該是脫困的時候了：臨床心理師帶你鬆開死結，重啟人生",
            "author": "劉仲彬",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07",
            "published": "2026-08-01",
            "subjects": ("人際困局", "自尊", "自我成長"),
        },
    ],
    "03_natural_science": [
        {
            "title": "有一種田野報告叫植物獵人",
            "author": "洪信介",
            "sourceName": "灰熊愛讀書／金石堂新書－自然科學",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2018630986296/",
            "published": "2026-08-01",
            "subjects": ("植物", "田野調查", "生態"),
        },
        {
            "title": "熵之道：高熵合金之父葉均蔚解密週期表與人生",
            "author": "葉均蔚、王惠英",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/06",
            "published": "2026-08-11",
            "subjects": ("高熵合金", "材料科學", "週期表"),
        },
    ],
    "04_healthcare": [
        {
            "title": "你的AI諮商師上線了：正確理解，安心使用，照顧自己的心",
            "author": "益田裕介",
            "sourceName": "博客來中文書新書列表－醫療保健",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/08",
            "published": "2026-08-01",
            "subjects": ("心理健康", "生成式AI", "自我照護"),
        },
        {
            "title": "我們都有小憂鬱：作者親身實測！利用療鬱象限圖的33種情緒解方，找回失去的快樂與活力",
            "author": "Hossy",
            "sourceName": "灰熊愛讀書／金石堂新書－醫療保健",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2014150616590/",
            "published": "2026-08-14",
            "subjects": ("憂鬱", "情緒復原", "生活調整"),
        },
    ],
    "05_food_wellness": [
        {
            "title": "來炊粿：軟糯的古早糕＆Ｑ潤的在地粿",
            "author": "王景茹",
            "sourceName": "灰熊愛讀書／金石堂新書－飲食養生",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2014271702714/",
            "published": "2026-08-01",
            "subjects": ("糕粿", "米食", "家常食譜"),
        },
        {
            "title": "精準抗癌湯：【日本癌症權威八大飲食法實踐版】天天這樣吃，讓癌細胞消失！120道強化免疫力、改善代謝異常的食療湯粥",
            "author": "濟陽高穗、上尾美由紀",
            "sourceName": "灰熊愛讀書／金石堂新書－飲食養生",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2014180410250/",
            "published": "2026-08-13",
            "subjects": ("食療湯粥", "代謝", "營養"),
        },
    ],
    "06_computer_info": [
        {
            "title": "StatQuest圖解神經網路與深度學習",
            "author": "Josh Starmer",
            "sourceName": "灰熊愛讀書／金石堂新書－電腦資訊",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2013120781191/",
            "published": "2026-08-01",
            "subjects": ("神經網路", "深度學習", "PyTorch"),
        },
        {
            "title": "AI Agent新紀元",
            "author": "孫大千",
            "sourceName": "灰熊愛讀書／金石堂新書－電腦資訊",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2013120781931/",
            "published": "2026-08-14",
            "subjects": ("AI代理人", "世界模型", "工作流程"),
        },
    ],
    "07_other": [
        {
            "title": "從土地到餐桌的哲學思考：探尋全球十七種糧食系統的思辨之旅",
            "author": "朱立安．巴吉尼",
            "sourceName": "灰熊愛讀書／金石堂新書－其他",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2014271702424/",
            "published": "2026-08-13",
            "subjects": ("糧食系統", "飲食文化", "永續"),
        },
        {
            "title": "趣讀臺灣史套書：《開箱臺灣史》＋《穿越臺灣趣歷史》",
            "author": "吳宜蓉、賴祥蔚",
            "sourceName": "灰熊愛讀書／金石堂新書－其他",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2017330369545/",
            "published": "2026-08-18",
            "subjects": ("臺灣史", "歷史敘事", "在地文化"),
        },
    ],
}


def payload(category_id: str, row: dict) -> dict:
    label = LABELS[category_id]
    subjects = row["subjects"]
    focus = "、".join(subjects)
    return {
        "title": row["title"],
        "author": row["author"],
        "sourceName": row["sourceName"],
        "sourceUrl": row["sourceUrl"],
        "sourceDateNote": (
            f"來源標示出版日期為 {row['published']}；擷取日期 {TO_DATE}，"
            f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
        ),
        "tags": list(dict.fromkeys([*TAGS[category_id], label, *subjects])),
        "summary": (
            f"本書由{row['author']}撰寫，內容聚焦{focus}；"
            "本次整理涵蓋核心觀念、論證脈絡與可實踐的閱讀重點。"
        ),
        "workId": WORK_ID,
    }


def main() -> int:
    committed = []
    for category_id, rows in BOOKS.items():
        candidates = [payload(category_id, row) for row in rows]
        path = TOOLS / f".findbook_candidates_{category_id}_20260818.json"
        path.write_text(
            json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        cmd = [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "reserve",
            "--category-id",
            category_id,
            "--candidates",
            str(path),
            "--limit",
            "2",
            "--from-date",
            FROM_DATE,
            "--to-date",
            TO_DATE,
        ]
        print("RUN", " ".join(cmd), flush=True)
        result = subprocess.run(cmd, cwd=ROOT, check=False)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        committed.append(category_id)
    print("reserved_categories", ",".join(committed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
