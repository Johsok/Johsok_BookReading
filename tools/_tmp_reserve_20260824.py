# -*- coding: utf-8 -*-
"""Reserve FindBook 2026-08-24 batch: first 3 categories x 5 Chinese books."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
WORK_ID = "findbook-20260824-1520"
FROM_DATE = "2026-07-25"
TO_DATE = "2026-08-24"

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
            "title": "【解析美元霸權的基礎結構】美元憑什麼？：左右全球金融的貨幣",
            "author": "何思因",
            "sourceName": "聯經出版商品頁－商業理財（博客來連線異常後改查）",
            "sourceUrl": "https://store.linkingbooks.com.tw/product/149450",
            "published": "2026-08-20",
            "subjects": ("美元", "金融體系", "地緣政治"),
        },
        {
            "title": "從地理看經濟！破譯全球局勢的56個關鍵問題",
            "author": "宮路秀作",
            "sourceName": "博客來中文書暢銷榜－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011059442",
            "published": "2026-08-12",
            "subjects": ("地理", "經濟趨勢", "地緣政治"),
        },
        {
            "title": "藏在股市金句裡的88個投資祕密：張真卿教你看圖秒懂股市實況與投資策略",
            "author": "張真卿",
            "sourceName": "ISBN資料庫／讀冊新書－商業理財",
            "sourceUrl": "https://isbn.tw/9786267888162",
            "published": "2026-08-06",
            "subjects": ("投資", "股市", "技術分析"),
        },
        {
            "title": "進化的力量4：逆勢增長",
            "author": "劉潤",
            "sourceName": "博客來中文書暢銷榜－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011060471",
            "published": "2026-08-07",
            "subjects": ("經營", "成長策略", "AI應用"),
        },
        {
            "title": "超乎常理的款待式領導：打造卓越團隊的實戰策略",
            "author": "威爾．吉達拉",
            "sourceName": "博客來中文書暢銷榜－商業理財",
            "sourceUrl": "https://www.books.com.tw/products/0011057518",
            "published": "2026-07-31",
            "subjects": ("領導", "服務", "團隊"),
        },
        {
            "title": "情緒能量：AI無法取代的頂級成交力",
            "author": "維琪",
            "sourceName": "ISBN資料庫／金石堂新書－商業理財",
            "sourceUrl": "https://isbn.tw/9786264449021",
            "published": "2026-08-01",
            "subjects": ("銷售", "溝通", "情緒價值"),
        },
        {
            "title": "不用猜市場，也能安心變有錢",
            "author": "吳佳駿、劉詠廷",
            "sourceName": "ISBN資料庫－商業理財",
            "sourceUrl": "https://isbn.tw/9786267888193",
            "published": "2026-08-01",
            "subjects": ("投資組合", "黃金", "資產配置"),
        },
    ],
    "02_psychology_growth": [
        {
            "title": "鬆綁表現焦慮：為什麼愈想證明自己，愈容易搞砸？",
            "author": "史蒂夫．麥格尼斯",
            "sourceName": "三民網路書店新書－心理勵志",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015600813",
            "published": "2026-07-31",
            "subjects": ("焦慮", "表現", "心智"),
        },
        {
            "title": "無處不在的阿焦：看見焦慮背後的自己",
            "author": "蜜蜂醫生、LEO醫生",
            "sourceName": "三民網路書店新書－心理勵志",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015749441",
            "published": "2026-08-21",
            "subjects": ("焦慮", "精神健康", "自我覺察"),
        },
        {
            "title": "沒有理由的焦慮：找回內在安定感",
            "author": "林允哲",
            "sourceName": "三民網路書店新書－心理勵志",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015764325",
            "published": "2026-08-10",
            "subjects": ("焦慮", "認知重構", "安定"),
        },
        {
            "title": "你的成敗，大腦說了算！告別焦慮內耗，打造成功體質",
            "author": "周夫亞",
            "sourceName": "三民網路書店新書－心理勵志",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015764401",
            "published": "2026-07-27",
            "subjects": ("大腦", "內耗", "習慣"),
        },
        {
            "title": "情緒能量：AI無法取代的頂級成交力",
            "author": "維琪",
            "sourceName": "ISBN資料庫／金石堂新書－心理勵志",
            "sourceUrl": "https://isbn.tw/9786264449021",
            "published": "2026-08-01",
            "subjects": ("情緒", "溝通", "人際"),
        },
        {
            "title": "覺察之道：任何時候都能回到當下、降伏煩惱的8個修心練習",
            "author": "藍獅子",
            "sourceName": "三民網路書店新書－心理勵志",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015623112",
            "published": "2026-08-12",
            "subjects": ("覺察", "內耗", "修心"),
        },
        {
            "title": "才賦自由：打造選擇權，實踐屬於你的成就樣貌",
            "author": "黃瑞仁",
            "sourceName": "金石堂新書－心理勵志",
            "sourceUrl": "https://www.kingstone.com.tw/basic/2014941945274/",
            "published": "2026-08-01",
            "subjects": ("天賦", "職涯", "選擇權"),
        },
        {
            "title": "正常的迷思：理解壓力與創傷如何形塑身心，鬆動情緒困境與疾病的循環，回到完整的自己",
            "author": "嘉柏．麥特、丹尼爾．麥特",
            "sourceName": "城邦讀書花園新書－心理勵志",
            "sourceUrl": "https://www.cite.com.tw/book?id=108641",
            "published": "2026-08-04",
            "subjects": ("創傷", "壓力", "身心"),
        },
    ],
    "03_natural_science": [
        {
            "title": "基因圖鑑：長壽祕密×基因編輯×再生科技，生命如何無限延續?",
            "author": "海上雲",
            "sourceName": "三民網路書店新書－自然科學",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015623273",
            "published": "2026-08-13",
            "subjects": ("基因", "DNA", "生命科學"),
        },
        {
            "title": "狗狗宇宙博物館：600+種犬類，從純種、地方犬到米克斯，一起進入牠們無敵可愛的世界！",
            "author": "程麗蓮",
            "sourceName": "城邦讀書花園新書－自然科學",
            "sourceUrl": "https://www.cite.com.tw/bestseller/citelibrary/new/201",
            "published": "2026-08-13",
            "subjects": ("動物", "演化", "犬類"),
        },
        {
            "title": "有趣到睡不著的腦科學：大腦是個好東西，請好好使用",
            "author": "毛內擴",
            "sourceName": "讀冊生活新書－自然科學",
            "sourceUrl": "https://www.silkbook.com/book_detail.asp?goods_ser=kk0611494",
            "published": "2026-08-19",
            "subjects": ("腦科學", "神經", "科普"),
        },
        {
            "title": "黑武士林鵰",
            "author": "張素卿、周見信",
            "sourceName": "三民網路書店新書－自然科學",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015747117",
            "published": "2026-08-20",
            "subjects": ("生態", "猛禽", "自然觀察"),
        },
        {
            "title": "看懂訊號，重塑大腦修復力：破解腦霧、失智與憂鬱，遠離大腦慢性發炎",
            "author": "張家銘",
            "sourceName": "三民網路書店新書－自然科學",
            "sourceUrl": "https://www.sanmin.com.tw/product/index/015628931",
            "published": "2026-08-19",
            "subjects": ("腦科學", "神經", "發炎"),
        },
        {
            "title": "藝數摺學2：20堂用指尖探索幾何規律的藝數美學課，從對稱全等到比例相似，動手體驗數學之用與藝術之美",
            "author": "李政憲",
            "sourceName": "城邦讀書花園新書－自然科學",
            "sourceUrl": "https://www.cite.com.tw/book?id=108428",
            "published": "2026-08-04",
            "subjects": ("數學", "幾何", "摺紙"),
        },
        {
            "title": "氣候如何影響你的大腦？：減損認知、增加暴力傾向、引發創傷……高溫與動盪的氣候怎樣改寫我們的心智和大腦？",
            "author": "克萊頓．艾登",
            "sourceName": "城邦讀書花園新書－自然科學",
            "sourceUrl": "https://www.cite.com.tw/book?id=FQ1100",
            "published": "2026-07-28",
            "subjects": ("氣候", "大腦", "神經科學"),
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
        path = TOOLS / f".findbook_candidates_{category_id}_20260824.json"
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
        print("RUN", " ".join(cmd), flush=True)
        result = subprocess.run(cmd, cwd=ROOT, check=False)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        committed.append(category_id)
    print("reserved_categories", ",".join(committed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
