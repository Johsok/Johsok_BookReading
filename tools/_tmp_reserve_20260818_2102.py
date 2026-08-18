# -*- coding: utf-8 -*-
"""Reserve 2026-08-18 21:02 FindBook batch: first 3 categories x 5 Chinese books."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
WORK_ID = "findbook-20260818-2102"
FROM_DATE = "2026-07-19"
TO_DATE = "2026-08-18"

TAGS = {
    "01_business_startup": ["商業", "投資", "創業", "理財"],
    "02_psychology_growth": ["心理", "勵志", "成長", "情緒"],
    "03_natural_science": ["科學", "自然", "科普"],
}

LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
}

BOOKS = {
    "01_business_startup": [
        {
            "title": "打開無路之路：放棄600萬年薪，前麥肯錫、BCG顧問的職涯覺醒，重新定義屬於你的「好工作」，找到真正值得投入的人生",
            "author": "保羅．米勒",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011058643",
            "published": "2026-08-05",
            "subjects": ("職涯選擇", "顧問工作", "人生轉向"),
        },
        {
            "title": "AI時代的資本真相：泡沫、週期與投資紀律",
            "author": "林裕豐",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011058626",
            "published": "2026-08-04",
            "subjects": ("投資週期", "資本市場", "泡沫風險"),
        },
        {
            "title": "超級代理效應：AI全面賦能時代！矽谷傳奇創業家霍夫曼寫給每個人的關鍵行動原則",
            "author": "雷德．霍夫曼、葛雷格．比托",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011059149",
            "published": "2026-08-04",
            "subjects": ("AI代理", "創業原則", "人機協作"),
        },
        {
            "title": "重壓的技術：個人資產800億！25年達成93倍報酬的操盤法",
            "author": "清原達郎",
            "sourceName": "博客來中文書新書列表－商業理財；商品頁改查三民網路書店",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015597722",
            "published": "2026-07-23",
            "subjects": ("避險基金", "集中持股", "投資紀律"),
        },
        {
            "title": "才賦自由：打造選擇權，實踐屬於你的成就樣貌",
            "author": "黃瑞仁",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
            "published": "2026-08-01",
            "subjects": ("職涯定位", "才賦整合", "選擇權"),
        },
        {
            "title": "老錢思維：告別表面富貴，從你開始活出富過三代的安穩之道與處世風格",
            "author": "拜倫．塔利",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
            "published": "2026-07-30",
            "subjects": ("財富傳承", "消費品味", "長期富足"),
        },
        {
            "title": "三明治族的慢富筆記",
            "author": "三明治先生",
            "sourceName": "博客來中文書新書列表－商業理財",
            "sourceUrl": "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
            "published": "2026-08-01",
            "subjects": ("家庭理財", "慢富", "人生複利"),
        },
    ],
    "02_psychology_growth": [
        {
            "title": "留白：少即是富，活出成熟大人的餘裕",
            "author": "橫田真由子",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-18",
            "subjects": ("餘裕", "減法生活", "自我界線"),
        },
        {
            "title": "戀愛課金：不管付出多大代價，永遠不要對愛失去信心",
            "author": "洪培芸",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-14",
            "subjects": ("親密關係", "自尊", "情感代價"),
        },
        {
            "title": "自我批評也是愛，但不是我們要的愛：一步一步克服自我懷疑，接納你就是你的美好和信心",
            "author": "戴蒙．札哈里斯",
            "sourceName": "金石堂新書－心理勵志",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2011771640362/",
            "published": "2026-08-12",
            "subjects": ("自我批評", "自我接納", "內在聲音"),
        },
        {
            "title": "你的人生，可以活在答案之外：韓國百萬學子信賴的「讀書之神」寫給迷惘世代──如何用學習打造人生選擇權",
            "author": "姜聲泰",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-12",
            "subjects": ("學習意義", "迷惘", "人生選擇權"),
        },
        {
            "title": "惡意是怎麼形成的？：從霸凌、劈腿到仇恨言論，歷時15年、全球超過250萬筆研究數據，心理學家教你揪出身邊有問題的人！",
            "author": "班雅明‧E‧席比、英格‧策特勒、莫頓‧摩沙根",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-06",
            "subjects": ("黑暗人格", "人際風險", "惡意形成"),
        },
        {
            "title": "創作之路：通往更高創造力的靈性道路",
            "author": "茱莉亞．卡麥隆",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-15",
            "subjects": ("創造力", "心靈療癒", "創作習慣"),
        },
        {
            "title": "恐懼，是最好的教練：一位奧運冠軍關於失敗、改變、未知與重生的心理鍛鍊",
            "author": "維多利亞・彭德爾頓",
            "sourceName": "博客來中文書新書列表－心理勵志",
            "sourceUrl": "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
            "published": "2026-08-10",
            "subjects": ("恐懼", "失敗復原", "心理鍛鍊"),
        },
    ],
    "03_natural_science": [
        {
            "title": "藝數摺學2：20堂用指尖探索幾何規律的藝數美學課，從對稱全等到比例相似，動手體驗數學之用與藝術之美",
            "author": "李政憲",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011057978",
            "published": "2026-08-06",
            "subjects": ("幾何", "摺紙", "數學教育"),
        },
        {
            "title": "哺乳類王朝：從恐龍陰影下竄出的邊緣生物，如何接手稱霸地球？",
            "author": "史提夫．布魯薩特",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011058997",
            "published": "2026-08-08",
            "subjects": ("演化", "化石", "哺乳類"),
        },
        {
            "title": "蝴蝶誌：一部關於人類迷戀、收藏狂熱與蝴蝶生存的自然史",
            "author": "蘿賽",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011059166",
            "published": "2026-08-08",
            "subjects": ("蝴蝶", "自然史", "生態復育"),
        },
        {
            "title": "細胞演化簡史，從能量到免疫系統：RNA拓荒、DNA登場、膜形成邊界、粒線體加入分工……從生命起源到癌症、免疫與人工智慧，重看細胞如何組成我們所知的生命",
            "author": "徐鑫",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011059128",
            "published": "2026-08-05",
            "subjects": ("細胞", "演化", "生命起源"),
        },
        {
            "title": "地球生命大歷史：發現45億年的演化故事",
            "author": "安西亞．拉奇亞",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011059605",
            "published": "2026-08-14",
            "subjects": ("地球史", "演化", "古生物"),
        },
        {
            "title": "基因圖鑑：長壽祕密×基因編輯×再生科技，生命如何無限延續？",
            "author": "海上雲",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011059227",
            "published": "2026-08-13",
            "subjects": ("基因", "長壽", "基因編輯"),
        },
        {
            "title": "動物百科圖鑑",
            "author": "本郷峻、山極壽一",
            "sourceName": "博客來中文書新書列表－自然科普",
            "sourceUrl": "https://www.books.com.tw/products/0011060035",
            "published": "2026-08-12",
            "subjects": ("哺乳動物", "生態", "圖鑑"),
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
            f"整理「{row['title']}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。"
        ),
        "workId": WORK_ID,
    }


def main() -> int:
    committed = []
    for category_id, rows in BOOKS.items():
        candidates = [payload(category_id, row) for row in rows]
        path = TOOLS / f".findbook_candidates_{category_id}_20260818_2102.json"
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
            "5",
            "--from-date",
            FROM_DATE,
            "--to-date",
            TO_DATE,
        ]
        print("RUN", category_id, flush=True)
        result = subprocess.run(cmd, cwd=ROOT, check=False)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        committed.append(category_id)
    print("reserved_categories", ",".join(committed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
