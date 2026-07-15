from __future__ import annotations

from pathlib import Path

import findbook_batch_20260716_b2 as prior


batch = prior.batch
batch.BATCH_NAME = "20260716_b3"
batch.WORK_ID = "findbook-20260716-073605-b3"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260716_b3.json"
)
batch.BROWSER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b3.json"
)
batch.prepare_candidates = prior.original_prepare_candidates
EXTRA_QUERIES = {
    "02_psychology_growth": (
        "焦慮", "情緒管理", "原生家庭", "心理諮商", "自我接納", "正念", "自信", "親密關係",
    ),
}
batch.CATEGORIES = tuple(
    batch.CategorySpec(
        spec.category_id,
        spec.label,
        spec.quota,
        spec.queries + EXTRA_QUERIES.get(spec.category_id, ()),
    )
    for spec in batch.CATEGORIES
)

DROP_TITLES = {
    "01_business_startup": {
        "班照上、股照炒 100張圖學會股市當沖 ：最嚴謹SOP，9：15上班前搞定，安心工作輕鬆賺 (二手書)",
        "【《阿甘投資法》金句印簽版套書】（《阿甘投資法：規劃篇》《阿甘投資法：執行篇》（二書）",
        "輝達黃仁勳：人工智慧晶片的成吉思汗 (二手書)",
    },
    "02_psychology_growth": {
        "通往財富自由之路 教你如何變得更有價值！早晚有一天，可以不再為了生活出售自己的時間 (二手書)",
        "未來預演（二版）：切斷情緒成癮神經鏈結，四週改變慣性腦迴路，換一個新未來 (二手書)",
        "【在變化不定的人生中修行—王思迅人生講座套書】（二冊）：《易經白話講座》、《金剛經白話講座》",
        "習慣致富：成為有錢人，你不需要富爸爸，只需要富習慣 (二手書)",
        "習慣致富 人生實踐版：在關鍵時刻下對決定，讓你成功達陣，樂享財務自由 (二手書)",
        "有錢人的習慣，和你不一樣：10個生活習慣，註定你是低薪族，或者變有錢（暢銷修訂版） (二手書)",
        "與成功有約：高效能人士的七個習慣（全新修訂版） (二手書)",
        "鉤癮效應：創造習慣新商機 (二手書)",
        "慢慢致富：告別金錢焦慮，77天思考練習不再害怕負債、低薪、沒工作，打造財務幸福循環 (二手書)",
        "財富自由心理學：療癒金錢焦慮，修練致富心態",
    },
    "03_natural_science": {
        "天空100層樓的家 (二手書)",
        "世界上最好玩的程式遊戲書 (二手書)",
        "怪物大百科：全世界的101種神祕生物大集合！ (二手書)",
        "生命解碼：從量子物理、數學演算，探索人類意識創造宇宙的生命真相 (二手書)",
    },
    "04_healthcare": {
        "不用計算卡路里，越吃越瘦的新陳代謝飲食 (二手書)",
    },
    "05_food_wellness": {
        "吃對鹽飲食奇蹟：減鹽才是現代的亂病之源！真正的好鹽，大量攝取也沒關係！日本養生專家的好鹽救命飲食 (二手書)",
        "物性飲食‧非吃不可與少吃為妙的全食物養生法：搞懂食物的個性和偏性，家常飲食也能勝過珍稀大補（上＋下）（全兩冊） (二手書)",
        "腎臟病低蛋白．低鹽飲食全書【最新增訂版】：親切圖解營養學＋簡單照做健康食譜，全面預防腎功能惡化 (二手書)",
        "腎臟病低蛋白．低鹽飲食全書：這樣吃就對了！40組健康餐X151道常備菜 (二手書)",
        "天天這樣吃，讓癌細胞消失：癌症被治癒的人都吃這些，日本抗癌權威八大飲食法，轉移、復發、癌末通通都有救",
        "愛吃青菜的鱷魚 (二手書)",
    },
    "07_other": {
        "隨他們去：全球熱銷突破1000萬冊現象級巨作！改變千萬人命運的心理技巧【附放下執念明信片】",
        "《未來1000天：你現在的努力，有多少會在AI時代失效？37 位實踐者寫給你的應對指南》隨書珍藏〈1000天導航圖〉拉頁",
        "我們都太慢反應的事：兒少網路性剝削、社群恐慌、網路霸凌，拉起孩子的數位界線",
        "賣瓜的人【文壇年度耀眼新星】",
        "財富階梯：資料科學家為你打造，適用人生各階段的致富策略",
    },
}

FILL_QUERIES = {
    "01_business_startup": ("企業策略", "領導管理", "創業管理", "職場管理"),
    "02_psychology_growth": (
        "正念", "原生家庭", "心理諮商", "自我接納", "自信", "親密關係", "情緒療癒", "內向", "拖延", "韌性",
    ),
    "03_natural_science": ("物理", "生物", "天文", "數學", "化學", "地球科學"),
    "04_healthcare": ("疾病", "照護", "健康檢查"),
    "05_food_wellness": ("營養", "健康飲食", "料理", "代謝"),
}

OTHER_BOOKS = (
    prior.curated_book(
        "07_other", "其他", "大英博物館裡的世界史", "霍吉淑、拉丹・阿卡巴尼亞、T. 理查．布朗頓、亞歷山卓．葛林",
        "https://www.books.com.tw/products/0011017735", "2025-03-27", ("世界史", "博物館", "文明交流"),
    ),
    prior.curated_book(
        "07_other", "其他", "世界史綱", "林恩．桑戴克",
        "https://www.books.com.tw/products/0011030428", "2025-09-10", ("世界史", "文化史", "文明"),
    ),
    prior.curated_book(
        "07_other", "其他", "臺灣史是什麼？〖作者親簽版〗", "吳密察",
        "https://www.books.com.tw/products/0011011988", "2025-02-05", ("臺灣史", "史料", "歷史敘事"),
    ),
    prior.curated_book(
        "07_other", "其他", "圖解世界史", "小松田直",
        "https://www.books.com.tw/products/0011028319", "2025-08-09", ("世界史", "文化交流", "全球史"),
    ),
    prior.curated_book(
        "07_other", "其他", "臺灣的由來", "連橫",
        "https://www.books.com.tw/products/0011033459", "2025-09-28", ("臺灣史", "臺灣通史", "歷史文獻"),
    ),
)

CURATED_BOOKS = OTHER_BOOKS + (
    prior.curated_book(
        "05_food_wellness", "飲食養生", "營養學（第五版）",
        "葉松鈴、沈佳錚、江淑華、潘怡君、詹婉卿、蔡一賢、楊斯涵、雲文姿、楊玉如、徐于淑、黃哲慧、張智傑、潘子明",
        "https://www.books.com.tw/products/0011018656", "2025-01-01",
        ("營養素", "均衡飲食", "生命期營養"),
    ),
)


def prepare_b3_candidates(refresh: bool) -> list[dict]:
    if refresh or not batch.MASTER_CANDIDATES.exists():
        rows = prior.original_prepare_candidates(refresh)
    else:
        rows = batch.findbook_writer.read_json(batch.MASTER_CANDIDATES)
    curated_titles = {row["title"] for row in CURATED_BOOKS}
    rows = [
        row for row in rows
        if row.get("title") not in DROP_TITLES.get(row.get("categoryId"), set())
        and row.get("title") not in curated_titles
    ]
    rows.extend(CURATED_BOOKS)

    manifest = batch.findbook_writer.read_json(batch.ROOT / "data.json")
    used_keys = {
        batch.findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
        if book.get("workId") != batch.WORK_ID
    }
    used_urls = {
        str(book.get("sourceUrl", "")).strip()
        for book in manifest.get("books", [])
        if book.get("workId") != batch.WORK_ID
    }
    selected_keys = {
        batch.findbook_writer.normalized_key(row.get("title", ""), row.get("author", ""))
        for row in rows
    }
    selected_urls = {str(row.get("sourceUrl", "")).strip() for row in rows}

    for spec in batch.CATEGORIES:
        current = [row for row in rows if row.get("categoryId") == spec.category_id]
        for keyword in FILL_QUERIES.get(spec.category_id, ()):
            if len(current) >= spec.quota:
                break
            page = batch.fetch_search(keyword)
            for candidate in batch.parse_items(page, spec, keyword):
                title = candidate.get("title", "")
                if title in DROP_TITLES.get(spec.category_id, set()):
                    continue
                if any(marker in title for marker in ("套書", "全套", "全兩冊")):
                    continue
                key = batch.findbook_writer.normalized_key(title, candidate.get("author", ""))
                url = str(candidate.get("sourceUrl", "")).strip()
                if key in used_keys or key in selected_keys or url in used_urls or url in selected_urls:
                    continue
                current.append(candidate)
                rows.append(candidate)
                selected_keys.add(key)
                selected_urls.add(url)
                if len(current) >= spec.quota:
                    break
        if len(current) != spec.quota:
            raise RuntimeError(f"{spec.category_id} 複核補書後只有 {len(current)} 本，未達 {spec.quota} 本")

    order = {spec.category_id: index for index, spec in enumerate(batch.CATEGORIES)}
    rows.sort(key=lambda row: order[row["categoryId"]])
    expected = {spec.category_id: spec.quota for spec in batch.CATEGORIES}
    actual = {
        category_id: sum(row.get("categoryId") == category_id for row in rows)
        for category_id in expected
    }
    keys = {
        batch.findbook_writer.normalized_key(row.get("title", ""), row.get("author", ""))
        for row in rows
    }
    if actual != expected or len(keys) != len(rows):
        raise RuntimeError(f"複核後候選不正確：counts={actual} unique={len(keys)}/{len(rows)}")
    batch.findbook_writer.write_json_atomic(batch.MASTER_CANDIDATES, rows)
    return rows


batch.prepare_candidates = prepare_b3_candidates


if __name__ == "__main__":
    batch.main()
