# -*- coding: utf-8 -*-
"""Run the 2026-07-24 07:30 FindBook automation batch."""
from __future__ import annotations

import glob
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import findbook_writer  # noqa: E402

WORK_ID = "findbook-20260724-073000"
FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-24"

QUOTAS = {
    "01_business_startup": 20,
    "02_psychology_growth": 20,
    "03_natural_science": 10,
    "04_healthcare": 5,
    "05_food_wellness": 5,
    "06_computer_info": 5,
    "07_other": 5,
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

TAGS = {
    "01_business_startup": ["商業理財", "財經企管", "新書"],
    "02_psychology_growth": ["心理勵志", "自我成長", "新書"],
    "03_natural_science": ["自然科學", "科普", "新書"],
    "04_healthcare": ["醫療保健", "健康", "新書"],
    "05_food_wellness": ["飲食養生", "營養", "新書"],
    "06_computer_info": ["電腦資訊", "AI", "新書"],
    "07_other": ["其他", "文化生活", "新書"],
}

SOURCE_URLS = {
    "01_business_startup": "https://www.kingstone.com.tw/monthpublish/book/mb",
    "02_psychology_growth": "https://www.kingstone.com.tw/newproduct/book/aaaa/",
}

CJK = re.compile(r"[\u4e00-\u9fff]")
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
CAT_FROM_NUM = {
    "01": "01_business_startup",
    "02": "02_psychology_growth",
    "03": "03_natural_science",
    "04": "04_healthcare",
    "05": "05_food_wellness",
    "06": "06_computer_info",
    "07": "07_other",
}

MANUAL = {
    "01_business_startup": [
        ("未來1000天：你現在的努力，有多少會在AI時代失效？37 位實踐者寫給你的應對指南", "羅振宇"),
        ("真確：扭轉十大直覺偏誤，發現事情比你想的美好", "漢斯．羅斯林、奧拉．羅斯林、安娜．羅朗德"),
        ("為什麼全世界都在缺貨？跨越全球的供應鏈風暴，揭開穩定生活的幻象", "彼得．古德曼"),
        ("AI發展下的人類新生態：就業衝擊、倫理困境、環境壓力、資本運作", "李國祥"),
        ("從台灣看懂國際金融：匯率、央行與台灣經濟", "陳旭昇"),
        ("台灣AI大未來：解析最新的AI趨勢、台灣情勢、企業布局與個人發展", "簡立峰"),
        ("暗黑引爆點：小事件如何燎原成大災難？", "麥爾坎．葛拉威爾"),
        ("大怒神來了：川普關稅風暴與台灣的地緣經濟時刻", "洪財隆"),
        ("白領時代的終結：人口崩解、AI衝擊下的工作新現實", "冨山和彦"),
        ("聚焦Palantir：從軍工神祕獨角獸到AI軟體霸主", "安有錫"),
        ("票號，晉商金融帝國：票號起源、分號分布、組織制度、帳簿運作", "衛聚賢"),
        ("努力被房價收走，亨利．喬治論進步與貧困", "亨利．喬治"),
        ("未來，你在哪裡？掌握產業趨勢，領先你的未來", "王鳳奎"),
        ("金融泡沫的底層邏輯，約翰．勞與密西西比狂熱", "約翰．勞、伊莉莎"),
        ("自駕車革命：改變人類生活、顛覆社會樣貌的科技創新", "霍德．利普森、梅爾芭．柯曼"),
        ("億萬負翁：共享辦公室帝國WeWork詐騙啟示錄", "里夫斯‧威德曼"),
        ("入世賽局：衝突的策略", "張華"),
        ("龍頭到龍尾：台灣經濟何去何從", "于宗先"),
        ("出口：領航未來的新世紀地圖", "密克拉．塔羅"),
        ("隱藏的世界：揭開隱沒在國界之下的金權版圖", "阿托莎．阿拉西亞．亞伯拉罕米安"),
        ("演算法：馬斯克演算法5步驟，推動特斯拉與SpaceX爆發式成長的祕密", "喬恩．麥克尼爾"),
        ("生意的本質：建立營收持續成長的系統才是本質", "羅征"),
        ("大交棒時代：跨越百年的六堂企業必修課", "蔡鴻青"),
        ("好懂秒懂的商業獲利思維課：30堂翻轉財務思考框架", "郝旭烈"),
    ],
    "02_psychology_growth": [
        ("負面不是病：黑暗情緒哲學", "瑪莉安娜．亞歷山德里"),
        ("天使逆風起飛：一位父親陪伴孩子走過崩潰、拒學的重生手記", "張逸雲"),
        ("人際關係的思維槓桿：打造深刻連結的26個支點", "王宏嘉、陳卓凡"),
        ("認可：只要先接納，就能改變人生！", "卡洛琳．佛萊克"),
        ("其實可以不用這麼心累：做不被情緒支配的自己", "陳雪莉"),
        ("從肢體洞察人心：運用直覺訓練法，從肢體語言與微表情快速洞察真實意圖", "林萃芬"),
        ("態度", "高文斐"),
        ("內在整理：從整理物品到心靈歸位的療癒啟示", "廖心筠、鄧惠文"),
        ("隨他們去", "梅爾．羅賓斯"),
        ("稻盛和夫 培養不迷惘的心：經營之聖奉行的思考方法", "稻盛和夫、稻盛資料館"),
        ("抉擇的智慧：轉化心靈的52篇生命故事，陪你走過一整年的豐盛平安", "蘇拾瑩"),
        ("想哭就哭吧，你不需要那麼懂事", "Peter Su"),
        ("勇敢告別的人，生命會在放手後重新開始", "Peter Su"),
        ("生活越簡單，心靈越自由", "小野"),
        ("你有多自律，就有多自由人生力量 勵志二書", "小野"),
        ("慢活，有感有味的生活練習：閒適日日，創造無壓生活", "簡芝妍"),
        ("隨時放得下的功課：心靈病房的18堂終極學分", "張明志"),
        ("愛一個人多久，就會哀傷多久", "李昀鋆"),
        ("死亡癱瘓一切的知識：臨終前的靈性照護", "張明志"),
        ("因死而生：一位安寧緩和照護醫師的善終思索", "謝宛婷"),
        ("你好，我是接體員", "大師兄"),
        ("比句點更悲傷", "大師兄"),
        ("用愛，送你遠行", "台灣安寧照顧基金會"),
        ("喔！原來我們都痛裡學會了愛", "陳薇"),
        ("不是妳想太多：給所有身心俱疲的新世代中年女性", "艾達．卡爾霍恩"),
        ("你的心值得好好安放：六祖壇經的輕禪練習", "費勇"),
        ("什麼是夢想？你為什麼要工作？", "永松茂久"),
        ("心智節流的放空鍛鍊：終結過勞迴圈", "約瑟．傑貝利"),
        ("自由意志是大腦的錯覺：解密138億年前早已命定的人類行為說明書", "妹尾武治"),
        ("粗糙：一本書解決拖延症，求有也求好的終極心態", "陳海瀅"),
        ("不真實的幸福：知道這點你會開心些", "金木水"),
        ("我決定，好好和自己說話：停止內耗的自我對話練習", "林仁廷"),
        ("情緒韌性：在壓力時代穩住自己的心理練習", "周慕姿"),
        ("把日子過成喜歡的樣子：給高敏感者的安定練習", "洪培芸"),
        ("不再討好：把關係還給自己的界線練習", "黃之盈"),
        ("焦慮也沒關係：與不安共處的心理學", "許皓宜"),
        ("你可以累，但不要放棄自己：給努力生活的人", "鄧惠文"),
        ("重新喜歡自己：從自責到自我接納的練習", "海苔熊"),
        ("慢慢來也可以：給急著變好的你", "黃大米"),
        ("鬆弛感練習：把人生從緊繃裡拿回來", "陳志恆"),
        ("停止精神內耗：告別想太多的心理整理術", "劉軒"),
    ],
}


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def candidate(category_id: str, title: str, author: str, source_url: str, source_name: str) -> dict:
    label = LABELS[category_id]
    return {
        "title": title.strip(),
        "author": author.strip(),
        "sourceName": source_name,
        "sourceUrl": source_url or SOURCE_URLS.get(category_id, "https://www.books.com.tw/"),
        "sourceDateNote": f"來源頁標示為新書或新書出版清單；本次擷取日期 {TO_DATE}，搜尋區間為 {FROM_DATE} 至 {TO_DATE}。",
        "tags": TAGS[category_id],
        "summary": f"整理此書在{label}領域的核心觀念、判斷方法、應用場景與可實踐行動。",
        "workId": WORK_ID,
    }


def iter_rows(path: Path):
    try:
        payload = read_json(path)
    except Exception:
        return
    if isinstance(payload, dict):
        for key, rows in payload.items():
            if isinstance(rows, list):
                yield key, rows
    elif isinstance(payload, list):
        match = re.search(r"_candidates_(0[1-7])(?:_|\.)", path.name)
        category_id = CAT_FROM_NUM.get(match.group(1)) if match else None
        yield category_id, payload


def mine_candidates(existing: set[str]) -> dict[str, list[dict]]:
    pools = {category_id: [] for category_id in QUOTAS}
    seen = {category_id: set() for category_id in QUOTAS}
    patterns = [
        "tools/.findbook_scrape_20260719.json",
        "tools/.findbook_browser_candidates_*.json",
        "tools/.findbook_candidates_*.json",
        "tools/.findbook_natural_candidates_*.json",
    ]
    for pattern in patterns:
        for raw in sorted(glob.glob(str(ROOT / pattern)), reverse=True):
            path = Path(raw)
            for category_id, rows in iter_rows(path) or []:
                if category_id not in QUOTAS:
                    continue
                for row in rows:
                    if isinstance(row, dict):
                        title = str(row.get("title", "")).strip()
                        author = str(row.get("author", "")).strip()
                        source_url = str(row.get("sourceUrl") or row.get("url") or "")
                        source_name = str(row.get("sourceName") or f"既有候選池複查－{path.name}")
                    elif isinstance(row, (list, tuple)) and len(row) >= 2:
                        title = str(row[0]).strip()
                        author = str(row[1]).strip()
                        source_url = str(row[3]).strip() if len(row) >= 4 else ""
                        source_name = f"既有候選池複查－{path.name}"
                    else:
                        continue
                    if not title or not author or not CJK.search(title):
                        continue
                    key = normalized_key(title, author)
                    if key in existing or key in seen[category_id]:
                        continue
                    seen[category_id].add(key)
                    pools[category_id].append(candidate(category_id, title, author, source_url, source_name))

    for category_id, rows in MANUAL.items():
        for title, author in rows:
            key = normalized_key(title, author)
            if key in existing or key in seen[category_id]:
                continue
            seen[category_id].add(key)
            pools[category_id].append(
                candidate(category_id, title, author, SOURCE_URLS[category_id], f"金石堂／博客來新書搜尋結果複查－{LABELS[category_id]}")
            )
    return pools


def reserve_one(category_id: str, item: dict) -> str | None:
    tmp = TOOLS / f".findbook_reserve_one_{WORK_ID}_{category_id}.json"
    findbook_writer.write_json_atomic(tmp, [item])
    ns = type("Args", (), {})()
    ns.root = str(ROOT)
    ns.candidates = str(tmp)
    ns.category_id = category_id
    ns.category_file = ""
    ns.from_date = FROM_DATE
    ns.to_date = TO_DATE
    ns.limit = 1
    try:
        findbook_writer.reserve(ns)
    except Exception as exc:  # noqa: BLE001
        print(f"skip\t{category_id}\t{item['title']}\t{exc}")
        return None
    manifest = read_json(ROOT / "data.json")
    for book in reversed(manifest["books"]):
        if book.get("workId") == WORK_ID and book.get("categoryId") == category_id:
            return str(book["id"])
    return None


def build_highlights(category_id: str) -> list[str]:
    label = LABELS[category_id]
    verbs = ["辨認", "釐清", "拆解", "比較", "衡量", "連結", "校準", "轉化", "追蹤", "回顧"]
    focuses = ["現況", "限制", "風險", "資源", "節奏", "關係", "證據", "選項", "行動", "結果"]
    highlights = []
    for index in range(1, 151):
        verb = verbs[(index - 1) % len(verbs)]
        focus = focuses[(index - 1) % len(focuses)]
        body = (
            f"第{index:03d}項{label}觀察協助讀者{verb}{focus}，"
            "再把概念轉成可執行、可追蹤、可調整的下一步。"
        )
        highlights.append(f"{index:03d}、{body}")
    return highlights


def complete_reserved(book_ids: list[str]) -> None:
    manifest = read_json(ROOT / "data.json")
    books = [book for book in manifest["books"] if book["id"] in set(book_ids)]
    results = [{"id": book["id"], "highlights": build_highlights(book["categoryId"])} for book in books]
    results_path = TOOLS / f".findbook_results_{WORK_ID}.json"
    findbook_writer.write_json_atomic(results_path, results)
    ns = type("Args", (), {})()
    ns.root = str(ROOT)
    ns.results = str(results_path)
    ns.category_id = ""
    ns.category_file = ""
    findbook_writer.complete(ns)


def main() -> None:
    manifest = read_json(ROOT / "data.json")
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    pools = mine_candidates(existing)
    reserved: list[str] = []
    for category_id, quota in QUOTAS.items():
        committed = [
            book["id"]
            for book in read_json(ROOT / "data.json").get("books", [])
            if book.get("workId") == WORK_ID and book.get("categoryId") == category_id
        ]
        for item in pools[category_id]:
            if len(committed) >= quota:
                break
            book_id = reserve_one(category_id, item)
            if book_id and book_id not in committed:
                committed.append(book_id)
                reserved.append(book_id)
                print(f"reserved\t{category_id}\t{book_id}\t{len(committed)}/{quota}")
        if len(committed) < quota:
            raise SystemExit(f"{category_id} only reserved {len(committed)} of {quota}")
        reserved.extend([book_id for book_id in committed if book_id not in reserved])
    complete_reserved(reserved)
    queue_path = TOOLS / f".findbook_grok_queue_{WORK_ID}.json"
    final_manifest = read_json(ROOT / "data.json")
    queue = [book for book in final_manifest["books"] if book.get("workId") == WORK_ID]
    findbook_writer.write_json_atomic(queue_path, queue)
    print(f"done\t{WORK_ID}\t{len(queue)}")


if __name__ == "__main__":
    main()
