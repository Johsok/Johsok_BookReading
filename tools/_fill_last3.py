# -*- coding: utf-8 -*-
"""One-shot: restore 05/07 candidates, scrape historical 06, reserve all."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402
import findbook_writer as w  # noqa: E402

WORK_ID = "findbook-20260913-1938"
FROM_DATE = "1986-09-13"
TO_DATE = "2021-09-13"
OUT = ROOT / "tools" / ".findbook_candidates_findbook-20260913-1938.json"


def add_work(cands: list[dict]) -> list[dict]:
    for item in cands:
        item["workId"] = WORK_ID
        item["title"] = str(item.get("title", "")).strip()
        item["author"] = str(item.get("author", "")).strip()
    return cands


FOOD = add_work(
    [
        {
            "title": "我的義大利麵 EASY PASTA：60種醬汁 X 30種麵條，變化千百種餐桌風味～",
            "author": "松露玫瑰",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100585254.html",
            "sourceDateNote": "來源標示出版日期為 2011-11-09；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "我的義大利麵", "經典"],
            "summary": "整理「我的義大利麵 EASY PASTA：60種醬汁 X 30種麵條，變化千百種餐桌風味～」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2011-11-09",
            "sourceSite": "讀冊",
        },
        {
            "title": "詹姆士帶你輕鬆煮",
            "author": "詹姆士",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100677011.html",
            "sourceDateNote": "來源標示出版日期為 2013-10-24；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "詹姆士帶你輕鬆煮", "經典"],
            "summary": "整理「詹姆士帶你輕鬆煮」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2013-10-24",
            "sourceSite": "讀冊",
        },
        {
            "title": "養麵種，不失敗！天然酵母作麵包：380張圖解秘訣大公開！第一次也能大成功！",
            "author": "黑田容子",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100581700.html",
            "sourceDateNote": "來源標示出版日期為 2011-09-30；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "養麵種，不失敗！天然酵母作麵包", "經典"],
            "summary": "整理「養麵種，不失敗！天然酵母作麵包：380張圖解秘訣大公開！第一次也能大成功！」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2011-09-30",
            "sourceSite": "讀冊",
        },
        {
            "title": "冰箱食材收納保鮮真簡單",
            "author": "Green Life生活收納編輯部",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100657464.html",
            "sourceDateNote": "來源標示出版日期為 2012-07-05；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "冰箱食材收納保鮮真簡單", "經典"],
            "summary": "整理「冰箱食材收納保鮮真簡單」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2012-07-05",
            "sourceSite": "讀冊",
        },
        {
            "title": "完美牛排全書：12道全世界都在享用的經典牛排食譜",
            "author": "王永賢",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100610088.html",
            "sourceDateNote": "來源標示出版日期為 2012-04-25；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "完美牛排全書", "經典"],
            "summary": "整理「完美牛排全書：12道全世界都在享用的經典牛排食譜」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2012-04-25",
            "sourceSite": "讀冊",
        },
        {
            "title": "Carol不藏私料理廚房（超值家常年菜版）",
            "author": "胡涓涓（Carol）",
            "sourceName": "讀冊－飲食2013暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100769928.html",
            "sourceDateNote": "來源標示出版日期為 2015-12-25；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["飲食", "營養", "養生", "Carol不藏私料理廚房（超值家常年菜版）", "經典"],
            "summary": "整理「Carol不藏私料理廚房（超值家常年菜版）」在飲食養生領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2015-12-25",
            "sourceSite": "讀冊",
        },
    ]
)

OTHER = add_work(
    [
        {
            "title": "漢娜的遺言（新版）",
            "author": "傑伊‧艾夏",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100809991.html",
            "sourceDateNote": "來源標示出版日期為 2017-03-21；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "漢娜的遺言（新版）", "經典"],
            "summary": "整理「漢娜的遺言（新版）」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2017-03-21",
            "sourceSite": "讀冊",
        },
        {
            "title": "生命中的美好缺憾",
            "author": "約翰‧葛林",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100650730.html",
            "sourceDateNote": "來源標示出版日期為 2013-04-09；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "生命中的美好缺憾", "經典"],
            "summary": "整理「生命中的美好缺憾」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2013-04-09",
            "sourceSite": "讀冊",
        },
        {
            "title": "四的法則",
            "author": "伊恩．柯德威、達斯汀．湯瑪遜",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100191662.html",
            "sourceDateNote": "來源標示出版日期為 2006-07-31；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "四的法則", "經典"],
            "summary": "整理「四的法則」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2006-07-31",
            "sourceSite": "讀冊",
        },
        {
            "title": "小王子：最值得珍藏的名家譯本（星空版）（二版）",
            "author": "翁端．聖-戴克思修伯里",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100829701.html",
            "sourceDateNote": "來源標示出版日期為 2017-11-01；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "小王子", "經典"],
            "summary": "整理「小王子：最值得珍藏的名家譯本（星空版）（二版）」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2017-11-01",
            "sourceSite": "讀冊",
        },
        {
            "title": "第十二個天使",
            "author": "奧格‧曼迪諾",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100076847.html",
            "sourceDateNote": "來源標示出版日期為 2008-12-24；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "第十二個天使", "經典"],
            "summary": "整理「第十二個天使」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2008-12-24",
            "sourceSite": "讀冊",
        },
        {
            "title": "獻給阿爾吉儂的花束【新譯本】",
            "author": "丹尼爾．凱斯",
            "sourceName": "讀冊－世界文學歷年累計暢銷百大",
            "sourceUrl": "https://www.taaze.tw/products/11100243466.html",
            "sourceDateNote": "來源標示出版日期為 2010-09-13；擷取日期 2026-09-13，落在 1986-09-13 至 2021-09-13 的搜尋區間內。",
            "tags": ["其他", "生活", "人文", "獻給阿爾吉儂的花束【新譯本】", "經典"],
            "summary": "整理「獻給阿爾吉儂的花束【新譯本】」在其他領域的核心觀念、判斷方法、適用情境與可實踐行動。",
            "published": "2010-09-13",
            "sourceSite": "讀冊",
        },
    ]
)


def parse_sanmin(html: str) -> list[dict]:
    items = []
    seen = set()
    for match in re.finditer(
        r'href="(/Product/Index/[^"]+)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S | re.I,
    ):
        url = "https://www.sanmin.com.tw" + match.group(1).split("?")[0]
        if url in seen:
            continue
        title = s.strip_html(match.group(2))
        if not title or not s.has_han(title) or len(title) < 2:
            continue
        seen.add(url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "三民",
            }
        )
    return items


def parse_sanmin_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = s.strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = s.strip_html(author_match.group(1)).strip(" /|,，、")
    return title, author, s.parse_iso_date(html)


def pid_ok(url: str) -> bool:
    match = s.BOOKS_PID_RE.search(url)
    if not match:
        return True
    # 0010930000+ on 博客來 is mostly 2021 下旬之後新品，這批要前5–40年經典。
    return match.group(1) < "0010930000"


def scrape_computer(existing_keys: set[str]) -> list[dict]:
    seen: set[str] = set()
    found: list[dict] = []

    def take(item: dict, source_name: str) -> None:
        if len(found) >= 6:
            return
        item["sourceName"] = source_name
        if item.get("sourceSite") == "博客來" and not pid_ok(item.get("sourceUrl") or ""):
            return
        key = s._accept_item(
            item, existing_keys, seen, FROM_DATE, TO_DATE, "06_computer_info"
        )
        if not key:
            return
        seen.add(key)
        found.append(s.to_candidate(item, "06_computer_info", FROM_DATE, TO_DATE))

    print("retry TAAZE computer lists")
    for list_id, name in s.TAAZE_CLASSIC_LISTS["06_computer_info"]:
        if len(found) >= 6:
            break
        try:
            rows = s.fetch_taaze_tag_items(list_id)
            print(name, "rows", len(rows))
        except Exception as exc:  # noqa: BLE001
            print(name, "FAIL", exc)
            continue
        for item in rows:
            if len(found) >= 6:
                break
            take(item, name)

    if len(found) < 6:
        print("博客來 computer lists with old pid filter")
        pages = [
            "https://www.books.com.tw/web/sys_saletopb/books/19/?o=1&v=1",
            "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
            "https://www.books.com.tw/web/books_topm_19/?o=5&page=2&v=1",
            "https://www.books.com.tw/web/books_topm_19/?o=5&page=3&v=1",
        ]
        parsed: list[dict] = []
        for url, html in s._fetch_pages_parallel(pages, "https://www.books.com.tw/", print):
            parsed.extend(s.parse_books_list(html))
        for item in parsed:
            if len(found) >= 6:
                break
            take(item, "博客來中文書－電腦資訊經典暢銷榜")

    if len(found) < 6:
        print("三民 程式設計搜尋")
        urls = [
            "https://www.sanmin.com.tw/search/index?kw=%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88&kind=1",
            "https://www.sanmin.com.tw/search/index?kw=Python&kind=1",
            "https://www.sanmin.com.tw/search/index?kw=Excel&kind=1",
        ]
        for page in urls:
            if len(found) >= 6:
                break
            try:
                html = s.fetch_html(page, referer="https://www.sanmin.com.tw/")
            except Exception as exc:  # noqa: BLE001
                print("三民 FAIL", page, exc)
                continue
            rows = parse_sanmin(html)
            print("三民", page, "rows", len(rows))
            need = []
            for raw in rows:
                if not s.has_han(str(raw.get("title") or "")):
                    continue
                if raw.get("author"):
                    take(raw, "三民暢銷－電腦資訊")
                else:
                    need.append(raw)
            extra = s._enrich_parallel(
                need[:12],
                parse_sanmin_detail,
                "https://www.sanmin.com.tw/",
                6 - len(found),
                None,
                print,
                "三民",
            )
            for item in extra:
                if len(found) >= 6:
                    break
                take(item, "三民暢銷－電腦資訊")

    print("computer candidates", len(found))
    for item in found:
        print(" ", item.get("published"), "|", item["title"], "|", item["author"])
    return add_work(found)


def reserve_category(category_id: str, candidates: list[dict]) -> list[str]:
    committed = []
    skipped = []
    for candidate in candidates:
        if len(committed) >= 5:
            break
        result = w.reserve_one(ROOT, category_id, candidate, FROM_DATE, TO_DATE)
        if result.get("status") == "committed":
            committed.append(result["id"])
            print("committed", result["id"], result["title"])
        else:
            skipped.append(str(candidate.get("title", "")))
            print("skipped", candidate.get("title"), result.get("reason"))
    print(category_id, "committed", len(committed), "skipped", len(skipped))
    if len(committed) != 5:
        raise SystemExit(f"{category_id} 只有 {len(committed)} 本")
    return committed


def main() -> None:
    existing_keys = s.load_existing_keys(ROOT)
    computer = scrape_computer(existing_keys)
    payload = {
        "05_food_wellness": FOOD,
        "06_computer_info": computer,
        "07_other": OTHER,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)

    ids = []
    ids.extend(reserve_category("05_food_wellness", FOOD))
    ids.extend(reserve_category("07_other", OTHER))
    ids.extend(reserve_category("06_computer_info", computer))
    print("ALL", ",".join(ids))


if __name__ == "__main__":
    main()
