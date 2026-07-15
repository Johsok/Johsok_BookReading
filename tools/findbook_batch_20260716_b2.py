from __future__ import annotations

from pathlib import Path

import findbook_batch_20260716 as batch


batch.BATCH_NAME = "20260716_b2"
batch.WORK_ID = "findbook-20260716-072546-b2"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260716_b2.json"
)
batch.BROWSER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b2.json"
)


def curated_book(
    category_id: str,
    label: str,
    title: str,
    author: str,
    url: str,
    published: str,
    subjects: tuple[str, ...],
) -> dict:
    focus = "、".join(subjects)
    return {
        "title": title,
        "author": author,
        "categoryId": category_id,
        "sourceName": f"博客來中文書商品頁－{label}",
        "sourceUrl": url,
        "sourceDateNote": (
            f"博客來商品頁標示出版日期為 {published}；擷取日期 {batch.TO_DATE}，"
            f"落在 {batch.FROM_DATE} 至 {batch.TO_DATE} 的搜尋區間內。"
        ),
        "tags": [label, *subjects],
        "summary": (
            f"本書由{author}撰寫，內容聚焦{focus}；"
            "本次整理涵蓋核心觀念、論證脈絡與可實踐的閱讀重點。"
        ),
        "subjects": list(subjects),
        "workId": batch.WORK_ID,
    }


DROP_TITLES = {
    "01_business_startup": {
        "班照上、股照炒 100張圖學會股市當沖 ：最嚴謹SOP，9：15上班前搞定，安心工作輕鬆賺 (二手書)",
    },
    "02_psychology_growth": {
        "通往財富自由之路 教你如何變得更有價值！早晚有一天，可以不再為了生活出售自己的時間 (二手書)",
        "【在變化不定的人生中修行—王思迅人生講座套書】（二冊）：《易經白話講座》、《金剛經白話講座》",
        "未來預演（二版）：切斷情緒成癮神經鏈結，四週改變慣性腦迴路，換一個新未來 (二手書)",
        "習慣致富：成為有錢人，你不需要富爸爸，只需要富習慣 (二手書)",
        "習慣致富 人生實踐版：在關鍵時刻下對決定，讓你成功達陣，樂享財務自由 (二手書)",
    },
    "03_natural_science": {
        "天空100層樓的家 (二手書)",
        "世界上最好玩的程式遊戲書 (二手書)",
        "怪物大百科：全世界的101種神祕生物大集合！ (二手書)",
    },
    "07_other": {
        "隨他們去：全球熱銷突破1000萬冊現象級巨作！改變千萬人命運的心理技巧【附放下執念明信片】",
        "《未來1000天：你現在的努力，有多少會在AI時代失效？37 位實踐者寫給你的應對指南》隨書珍藏〈1000天導航圖〉拉頁",
        "我們都太慢反應的事：兒少網路性剝削、社群恐慌、網路霸凌，拉起孩子的數位界線",
        "賣瓜的人【文壇年度耀眼新星】",
        "財富階梯：資料科學家為你打造，適用人生各階段的致富策略",
    },
}


CURATED_BOOKS = (
    curated_book(
        "01_business_startup", "商業理財", "投資腦：三資產槓桿打造不焦慮人生", "上岡正明",
        "https://www.books.com.tw/products/0011032507", "2025-09-26", ("投資理財", "資產槓桿", "風險管理"),
    ),
    curated_book(
        "02_psychology_growth", "心理勵志", "心智升維：思考力躍遷的底層邏輯", "約翰・保羅・明達",
        "https://www.books.com.tw/products/CN17697848", "2025-05-01", ("認知心理學", "思考力", "決策"),
    ),
    curated_book(
        "02_psychology_growth", "心理勵志", "榮格心理學入門：自我重生的人生旅程", "山根久美子",
        "https://www.books.com.tw/products/0011011968", "2025-02-05", ("榮格心理學", "自我接納", "個體化"),
    ),
    curated_book(
        "02_psychology_growth", "心理勵志", "卡倫．荷妮之精神官能症與人的成長（筆記版）：拒絕強迫性追求與社會期待，直面真實自我的心理重建之路！", "卡倫．荷妮",
        "https://www.books.com.tw/products/0011020951", "2025-05-21", ("精神分析", "基本焦慮", "自我整合"),
    ),
    curated_book(
        "02_psychology_growth", "心理勵志", "內在力量的指引：榮格心理學自我探索的21個智慧", "詹姆斯・霍利斯",
        "https://www.books.com.tw/products/0011035669", "2025-11-05", ("榮格心理學", "自我探索", "生命意義"),
    ),
    curated_book(
        "02_psychology_growth", "心理勵志", "半熟人格：榮格 × MBTI 心理指南，實現真正成熟的人生", "王凱琳",
        "https://www.books.com.tw/products/0011035559", "2025-11-05", ("人格心理", "MBTI", "自我成長"),
    ),
    curated_book(
        "03_natural_science", "自然科學", "物理才是最好的人生指南：讓你變聰明、變強大的宇宙自然法則", "克莉絲汀．麥金利",
        "https://www.books.com.tw/products/0011021741", "2025-06-01", ("物理學", "自然法則", "科普"),
    ),
    curated_book(
        "03_natural_science", "自然科學", "楊振寧講物理：基本粒子發現之旅", "楊振寧",
        "https://www.books.com.tw/products/CN14802920", "2025-04-01", ("粒子物理", "科學史", "科普"),
    ),
    curated_book(
        "03_natural_science", "自然科學", "DK物理學百科", "英國DK出版社",
        "https://www.books.com.tw/products/CN17852231", "2025-04-01", ("物理學", "科學史", "宇宙"),
    ),
    curated_book(
        "07_other", "其他", "中國大歷史", "呂思勉",
        "https://www.books.com.tw/products/E050252349", "2025-02-21", ("中國史", "制度沿革", "文化發展"),
    ),
    curated_book(
        "07_other", "其他", "朕說歷史〖商周篇〗", "朕說‧黃桑",
        "https://www.books.com.tw/products/0011014255", "2025-03-04", ("商周史", "考古", "歷史漫畫"),
    ),
    curated_book(
        "07_other", "其他", "圖解中國史（2版）", "林志宏",
        "https://www.books.com.tw/products/0011024044", "2025-06-28", ("中國史", "制度", "文化融合"),
    ),
    curated_book(
        "07_other", "其他", "全彩圖解：人類的故事", "房龍",
        "https://www.books.com.tw/products/0011021804", "2025-05-28", ("世界史", "文明", "人類社會"),
    ),
    curated_book(
        "07_other", "其他", "中國歷史通論（精装珍藏版）", "王家範",
        "https://www.books.com.tw/products/0011026272", "2025-07-18", ("中國通史", "歷史結構", "現代轉型"),
    ),
)


original_prepare_candidates = batch.prepare_candidates


def prepare_curated_candidates(refresh: bool) -> list[dict]:
    rows = original_prepare_candidates(refresh)
    curated_titles = {
        (row["categoryId"], row["title"])
        for row in CURATED_BOOKS
    }
    rows = [
        row for row in rows
        if row.get("title") not in DROP_TITLES.get(row.get("categoryId"), set())
        and (row.get("categoryId"), row.get("title")) not in curated_titles
    ]
    rows.extend(CURATED_BOOKS)
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


def highlights_for(row: dict, label: str) -> list[str]:
    subjects = [str(item).strip() for item in row.get("subjects", []) if str(item).strip()]
    focus = "、".join(subjects[:3]) or label
    lines = []
    for principle in batch.highlight_source.CATEGORY_PRINCIPLES[label]:
        principle = principle.replace("本書資訊", "健康資訊")
        for lens in batch.highlight_source.READING_LENSES:
            index = len(lines) + 1
            lines.append(f"{index:03d}、{principle}；以{focus}為情境，{lens}。")
    return batch.findbook_writer.validate_highlights(row["title"], lines)


batch.prepare_candidates = prepare_curated_candidates
batch.highlight_source.highlights_for = highlights_for


if __name__ == "__main__":
    batch.main()
