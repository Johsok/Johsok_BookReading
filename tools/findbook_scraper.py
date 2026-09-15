# -*- coding: utf-8 -*-
"""Scrape Chinese new/hot books: 博客來 first, then 金石堂／讀冊 if quota remains."""
from __future__ import annotations

import argparse
import json
import re
import ssl
import subprocess
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from html import unescape
from pathlib import Path
from typing import Callable

HAS_HAN = re.compile(r"[\u4e00-\u9fff]")
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
DATE_RE = re.compile(r"((?:19|20)\d{2})[./年\-](\d{1,2})[./月\-](\d{1,2})")
PRODUCT_ID_RE = re.compile(r"/products/([A-Z0-9]+)", re.I)
BOOKS_PID_RE = re.compile(r"/products/(001\d{7})", re.I)
TITLE_SKIP = {
    "01_business_startup": ("這樣生活，那樣工作",),
    "02_psychology_growth": ("繪本",),
    "03_natural_science": ("靈界", "怪奇", "ㄎㄧㄤ", "漫畫", "生命解碼", "人生十二堂課"),
    "04_healthcare": (
        "減脂",
        "瘦身",
        "瘦用",
        "瘦肚子",
        "增肌",
        "食譜",
        "飲食法",
        "營養科學",
        "根治飲食",
        "副食品",
        "拿鐵",
        "胎教",
        "食在",
        "食物代換",
        "吃錯",
        "瑜伽",
    ),
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

CATEGORY_LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
}

DEFAULT_TAGS = {
    "01_business_startup": ["商業", "投資", "創業", "理財"],
    "02_psychology_growth": ["心理", "勵志", "成長", "情緒"],
    "03_natural_science": ["科學", "自然", "科普"],
    "04_healthcare": ["醫療", "健康", "保健"],
    "05_food_wellness": ["飲食", "營養", "養生"],
    "06_computer_info": ["電腦", "資訊", "科技"],
    "07_other": ["其他", "生活", "人文"],
}

BOOKS_URLS = {
    "01_business_startup": [
        "https://www.books.com.tw/web/sys_saletopb/books/02/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&page=3&v=1",
    ],
    "02_psychology_growth": [
        "https://www.books.com.tw/web/sys_saletopb/books/07/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&page=3&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/sys_saletopb/books/06/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&page=3&v=1",
    ],
    "04_healthcare": [
        "https://www.books.com.tw/web/sys_saletopb/books/08/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_08/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_08/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_08/?o=5&page=3&v=1",
    ],
    "05_food_wellness": [
        "https://www.books.com.tw/web/sys_saletopb/books/09/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_09/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_09/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_09/?o=5&page=3&v=1",
    ],
    "06_computer_info": [
        "https://www.books.com.tw/web/sys_saletopb/books/19/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=3&v=1",
    ],
    "07_other": [
        "https://www.books.com.tw/web/sys_saletopb/books/01/?o=1&v=1",
        "https://www.books.com.tw/web/sys_saletopb/books/04/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_01/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_04/?o=5&v=1",
    ],
}

KINGSTONE_URLS = {
    "01_business_startup": [
        "https://www.kingstone.com.tw/newbook/book/business/",
        "https://www.kingstone.com.tw/monthpublish/book/ea/",
    ],
    "02_psychology_growth": [
        "https://www.kingstone.com.tw/newbook/book/psycho/",
        "https://www.kingstone.com.tw/monthpublish/book/eg/",
    ],
    "03_natural_science": [
        "https://www.kingstone.com.tw/newbook/book/nature/",
        "https://www.kingstone.com.tw/monthpublish/book/ei/",
    ],
    "04_healthcare": [
        "https://www.kingstone.com.tw/newbook/book/health/",
        "https://www.kingstone.com.tw/monthpublish/book/ek/",
    ],
    "05_food_wellness": [
        "https://www.kingstone.com.tw/newbook/book/food/",
        "https://www.kingstone.com.tw/monthpublish/book/el/",
    ],
    "06_computer_info": [
        "https://www.kingstone.com.tw/newbook/book/computer/",
        "https://www.kingstone.com.tw/monthpublish/book/en/",
    ],
    "07_other": [
        "https://www.kingstone.com.tw/newbook/book/literature/",
        "https://www.kingstone.com.tw/newbook/book/humanity/",
    ],
}

TAAZE_URLS = {
    "01_business_startup": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=102000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=102000",
    ],
    "02_psychology_growth": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=111000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=111000",
    ],
    "03_natural_science": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=104000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=104000",
    ],
    "04_healthcare": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=108000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=108000",
    ],
    "05_food_wellness": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=109000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=109000",
    ],
    "06_computer_info": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=119000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=119000",
    ],
    "07_other": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=101000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=101000",
    ],
}

# 讀冊歷年／年度暢銷百大（viewTagsAgent.jsp 的 p=）。用於前 5–40 年經典書。
TAAZE_CLASSIC_LISTS = {
    "01_business_startup": [
        ("20221584", "讀冊－商業歷年累計暢銷百大"),
        ("20221583", "讀冊－商業10年暢銷百大"),
        ("20221090", "讀冊－商業2021暢銷百大"),
        ("20221085", "讀冊－商業2016暢銷百大"),
        ("20221082", "讀冊－商業2013暢銷百大"),
        ("20221068", "讀冊－商業2011暢銷百大"),
    ],
    "02_psychology_growth": [
        ("20221665", "讀冊－心理勵志歷年累計暢銷百大"),
        ("20221664", "讀冊－心理勵志10年暢銷百大"),
        ("20221499", "讀冊－心理勵志2021暢銷百大"),
        ("20221212", "讀冊－心理勵志2016暢銷百大"),
        ("20221279", "讀冊－心理勵志2013暢銷百大"),
        ("20222102", "讀冊－心理勵志專題暢銷"),
        ("20221213", "讀冊－心理勵志鄰近年度暢銷百大"),
        ("20221498", "讀冊－心理勵志鄰近年度暢銷百大"),
    ],
    "03_natural_science": [
        ("20221725", "讀冊－科學歷年累計暢銷百大"),
        ("20221760", "讀冊－科學10年暢銷百大"),
        ("20221303", "讀冊－科學2021暢銷百大"),
        ("20221308", "讀冊－科學2016暢銷百大"),
        ("20221311", "讀冊－科學2013暢銷百大"),
        ("20221361", "讀冊－科學2009暢銷百大"),
    ],
    "04_healthcare": [
        ("20221522", "讀冊－醫學保健歷年累計暢銷百大"),
        ("20221521", "讀冊－醫學保健10年暢銷百大"),
        ("20221148", "讀冊－醫學保健2021暢銷百大"),
        ("20221154", "讀冊－醫學保健2016暢銷百大"),
        ("20221157", "讀冊－醫學保健2013暢銷百大"),
        ("20221159", "讀冊－醫學保健2011暢銷百大"),
    ],
    "05_food_wellness": [
        ("20221759", "讀冊－飲食10年暢銷百大"),
        ("20221104", "讀冊－飲食2013暢銷百大"),
        ("20221101", "讀冊－飲食2016暢銷百大"),
        ("20221096", "讀冊－飲食2021暢銷百大"),
        ("20221107", "讀冊－飲食2010暢銷百大"),
    ],
    "06_computer_info": [
        ("20222613", "讀冊－電腦歷年累計暢銷百大"),
        ("20221745", "讀冊－電腦2021暢銷百大"),
        ("20221746", "讀冊－電腦2020暢銷百大"),
        ("20221747", "讀冊－電腦2019暢銷百大"),
        ("20221748", "讀冊－電腦2018暢銷百大"),
        ("20221744", "讀冊－電腦2022暢銷百大"),
    ],
    "07_other": [
        ("20221626", "讀冊－華文文學歷年累計暢銷百大"),
        ("20221630", "讀冊－世界文學歷年累計暢銷百大"),
        ("20221693", "讀冊－歷史地理歷年累計暢銷百大"),
        ("20221625", "讀冊－華文文學10年暢銷百大"),
        ("20221012", "讀冊－華文文學2013暢銷百大"),
        ("20221119", "讀冊－世界文學2013暢銷百大"),
        ("20221004", "讀冊－華文文學2021暢銷百大"),
    ],
}

LogFn = Callable[[str], None]
StopFn = Callable[[], bool]


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def has_han(title: str) -> bool:
    return bool(HAS_HAN.search(title or ""))


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_iso_date(text: str) -> str:
    match = DATE_RE.search(text or "")
    if not match:
        return ""
    return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"


def in_date_range(published: str, from_date: str, to_date: str) -> bool:
    if not published:
        return True
    try:
        value = date.fromisoformat(published)
        start = date.fromisoformat(from_date)
        end = date.fromisoformat(to_date)
    except ValueError:
        return True
    return start <= value <= end


def in_classic_date_range(published: str, from_date: str) -> bool:
    """Keep reprints: only enforce the older bound. Undated classic-list rows stay."""
    if not published:
        return True
    try:
        value = date.fromisoformat(published)
        start = date.fromisoformat(from_date)
    except ValueError:
        return True
    return value >= start


SIMPLIFIED_MARKERS = re.compile(r"[国这书对门东见马风车开关头过还经个应学现电钟医语]")


def looks_simplified(text: str) -> bool:
    """True when a title/author has several simplified-only glyphs."""
    return len(SIMPLIFIED_MARKERS.findall(text or "")) >= 2


def undated_product_too_new(item: dict, to_date: str) -> bool:
    """Drop 博客來 product IDs that are newer than the search window."""
    if item.get("published"):
        return False
    url = str(item.get("sourceUrl") or "")
    match = BOOKS_PID_RE.search(url)
    if not match:
        return False
    try:
        end = date.fromisoformat(to_date)
    except ValueError:
        return False
    pid = match.group(1)
    # 0011000000+ are roughly 2022+; 0011020000+ are late-2023 to 2026 new products.
    if end < date(2022, 1, 1):
        return pid >= "0011000000"
    if end < date(2025, 1, 1):
        return pid >= "0011020000"
    return False


def fetch_html(url: str, referer: str = "") -> str:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "identity",
    }
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    contexts = [ssl.create_default_context(), ssl._create_unverified_context()]
    last_error: Exception | None = None
    for context in contexts:
        try:
            with urllib.request.urlopen(request, timeout=12, context=context) as response:
                raw = response.read()
            return raw.decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
    try:
        command = [
            "curl.exe",
            "-sL",
            "--max-time",
            "20",
            "-A",
            USER_AGENT,
            "-H",
            "Accept-Language: zh-TW,zh;q=0.9,en;q=0.8",
            "-H",
            "Accept: text/html,application/xhtml+xml",
        ]
        if referer:
            command.extend(["-e", referer])
        command.append(url)
        raw = subprocess.check_output(command)
        return raw.decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        last_error = last_error or exc
    if url.startswith("https://"):
        http_url = "http://" + url[8:]
        request = urllib.request.Request(http_url, headers=headers)
        try:
            with urllib.request.urlopen(
                request, timeout=12, context=ssl._create_unverified_context()
            ) as response:
                return response.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last_error = last_error or exc
    raise last_error or RuntimeError(f"無法讀取 {url}")


def parse_books_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    patterns = [
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h4>(.*?)</ul>',
        r'<h3>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h3>(.*?)</ul>',
        r'<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>(.{0,1200})',
        r'href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.S | re.I):
            url = match.group(1).split("?")[0]
            if url in seen:
                continue
            title = strip_html(match.group(2))
            if not title or not has_han(title) or len(title) < 2:
                continue
            block = match.group(3) if match.lastindex and match.lastindex >= 3 else ""
            author = ""
            published = ""
            if block:
                author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
                if author_match:
                    author = strip_html(author_match.group(1)).strip(" /|,，、")
                date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", block)
                if date_match:
                    published = parse_iso_date(date_match.group(1))
            seen.add(url)
            items.append(
                {
                    "title": title,
                    "author": author,
                    "sourceUrl": url,
                    "published": published,
                    "sourceSite": "博客來",
                }
            )
    return items


def parse_books_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = strip_html(author_match.group(1))
        for sep in ("出版日期", "類別", "原文作者", "譯者", "出版社"):
            author = author.split(sep)[0]
        author = author.strip(" /|,，、\">'")
    published = ""
    date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", html)
    if date_match:
        published = parse_iso_date(date_match.group(1))
    if not published:
        published = parse_iso_date(strip_html(html[:8000]))
    return title, author, published


def parse_kingstone_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'<a[^>]+href="(https://www\.kingstone\.com\.tw/basic/\d+/?)[^"]*"[^>]*>(.*?)</a>',
        html,
        re.S | re.I,
    ):
        url = match.group(1).split("?")[0]
        if url in seen:
            continue
        title = strip_html(match.group(2))
        if not title or not has_han(title) or len(title) < 2:
            continue
        seen.add(url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "金石堂",
            }
        )
    return items


def parse_kingstone_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = strip_html(author_match.group(1)).strip(" /|,，、")
    return title, author, parse_iso_date(html)


def parse_taaze_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'href="((?:https://www\.taaze\.tw)?/products/(\d+)\.html)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S | re.I,
    ):
        prod_id = match.group(2)
        url = f"https://www.taaze.tw/products/{prod_id}.html"
        if url in seen:
            continue
        title = strip_html(match.group(3))
        if not title or not has_han(title) or len(title) < 2:
            continue
        seen.add(url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "讀冊",
            }
        )
    return items


def parse_taaze_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*([^<\n]+)", html)
    if author_match:
        author = strip_html(author_match.group(1)).strip(" /|,，、")
    return title, author, parse_iso_date(html)


def parse_taaze_tag_rows(raw: str) -> list[dict]:
    """Parse one viewTagsAgent JSON page into list rows."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return []
    items: list[dict] = []
    seen: set[str] = set()
    for row in payload.get("result1") or []:
        title = str(row.get("titleMain") or "").strip()
        author = str(row.get("author") or "").strip(" /|,，、")
        prod_id = str(row.get("prodId") or "").strip()
        published = str(row.get("publishDate") or "").strip()
        if published:
            published = published[:10] if len(published) >= 10 else parse_iso_date(published)
        if not title or not has_han(title) or not author or not prod_id or prod_id in seen:
            continue
        seen.add(prod_id)
        items.append(
            {
                "title": title,
                "author": author,
                "sourceUrl": f"https://www.taaze.tw/products/{prod_id}.html",
                "published": published,
                "sourceSite": "讀冊",
            }
        )
    return items


def iter_taaze_tag_pages(list_id: str, page_size: int = 20, end_num: int = 100):
    """Yield 讀冊暢銷百大 pages; caller stops as soon as quota is filled."""
    start = 1
    while start <= end_num:
        chunk_end = min(start + page_size - 1, end_num)
        url = (
            "https://www.taaze.tw/beta/viewTagsAgent.jsp"
            f"?a=01&d=11&l=0&t=11&c=00&k=03&p={list_id}"
            f"&startNum={start}&endNum={chunk_end}&sortType=1"
        )
        raw = ""
        last_error: Exception | None = None
        for _attempt in range(2):
            try:
                raw = fetch_html(url, referer="https://www.taaze.tw/")
                last_error = None
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        if last_error is not None:
            raise last_error
        rows = parse_taaze_tag_rows(raw)
        if not rows:
            break
        yield rows
        if len(rows) < (chunk_end - start + 1):
            break
        start = chunk_end + 1


def fetch_taaze_tag_items(list_id: str, end_num: int = 100) -> list[dict]:
    """Read one 讀冊暢銷百大 list via viewTagsAgent (list JSON, not a detail page)."""
    items: list[dict] = []
    seen: set[str] = set()
    for rows in iter_taaze_tag_pages(list_id, end_num=end_num):
        for item in rows:
            url = str(item.get("sourceUrl") or "")
            if url in seen:
                continue
            seen.add(url)
            items.append(item)
    return items


def _stopped(should_stop: StopFn | None) -> bool:
    return bool(should_stop and should_stop())


def _log(log: LogFn | None, message: str) -> None:
    if log:
        log(message)


def enrich_if_needed(
    item: dict,
    parse_detail,
    referer: str,
    should_stop: StopFn | None,
) -> dict:
    """Fill author from the detail page only when the list row has no author."""
    if item.get("author"):
        return item
    if _stopped(should_stop):
        return item
    html = fetch_html(item["sourceUrl"], referer=referer)
    title, author, published = parse_detail(html)
    if title:
        item["title"] = title
    if author:
        item["author"] = author
    if published:
        item["published"] = published
    return item


def to_candidate(item: dict, category_id: str, from_date: str, to_date: str) -> dict:
    label = CATEGORY_LABELS[category_id]
    published = str(item.get("published") or "")
    today = datetime.now().date().isoformat()
    if published:
        date_note = (
            f"來源標示出版日期為 {published}；擷取日期 {today}，"
            f"落在 {from_date} 至 {to_date} 的搜尋區間內。"
        )
    else:
        date_note = "來源未提供明確日期"
    title = str(item["title"]).strip()
    author = str(item["author"]).strip()
    tags = list(DEFAULT_TAGS[category_id])
    source_name = str(item.get("sourceName") or "")
    if any(mark in source_name for mark in ("歷年", "經典", "暢銷百大")) and "經典" not in tags:
        tags.append("經典")
    return {
        "title": title,
        "author": author,
        "sourceName": str(item.get("sourceName") or f"{item.get('sourceSite')}新書－{label}"),
        "sourceUrl": str(item["sourceUrl"]).strip(),
        "sourceDateNote": date_note,
        "tags": tags,
        "summary": (
            f"整理「{title}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。"
        ),
        "published": published,
        "sourceSite": item.get("sourceSite", ""),
    }


def _fetch_pages_parallel(pages: list[str], referer: str, log: LogFn | None) -> list[tuple[str, str]]:
    """Fetch list pages in parallel. Failed URLs are skipped."""
    if not pages:
        return []
    results: list[tuple[str, str]] = []

    def _one(url: str) -> tuple[str, str]:
        return url, fetch_html(url, referer=referer)

    workers = min(4, len(pages))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_one, url): url for url in pages}
        for future in as_completed(futures):
            url = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:  # noqa: BLE001
                _log(log, f"列表失敗：{url} ({exc})")
    return results


def _accept_item(
    item: dict,
    existing_keys: set[str],
    seen_keys: set[str],
    from_date: str,
    to_date: str,
    category_id: str = "",
    classic: bool = False,
    prefer_hant: bool = False,
) -> str:
    """Return the dedupe key if the row is usable; otherwise empty."""
    title = str(item.get("title") or "")
    author = str(item.get("author") or "")
    if not has_han(title) or not author:
        return ""
    if re.search(r"简体|簡體", title) or "二手書" in title:
        return ""
    if prefer_hant and (looks_simplified(title) or looks_simplified(author)):
        return ""
    for needle in TITLE_SKIP.get(category_id, ()):
        if needle in title:
            return ""
    key = normalized_key(title, author)
    if key in existing_keys or key in seen_keys:
        return ""
    published = str(item.get("published") or "")
    if classic:
        if not in_classic_date_range(published, from_date):
            return ""
    else:
        if published and not in_date_range(published, from_date, to_date):
            return ""
        if undated_product_too_new(item, to_date):
            return ""
    return key


def _enrich_parallel(
    items: list[dict],
    parse_detail,
    referer: str,
    limit: int,
    should_stop: StopFn | None,
    log: LogFn | None,
    source_site: str,
) -> list[dict]:
    """Fetch detail pages only for rows still missing an author."""
    if not items or limit <= 0:
        return []
    filled: list[dict] = []

    def _one(raw: dict) -> dict:
        return enrich_if_needed(raw, parse_detail, referer, should_stop)

    workers = min(4, len(items), max(1, limit))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one, raw) for raw in items]
        for future in as_completed(futures):
            if _stopped(should_stop) or len(filled) >= limit:
                break
            try:
                item = future.result()
            except Exception as exc:  # noqa: BLE001
                _log(log, f"{source_site} 詳情失敗：{exc}")
                continue
            if item.get("author"):
                filled.append(item)
    return filled


def _collect_from_pages(
    pages: list[str],
    parse_list,
    parse_detail,
    source_site: str,
    source_name: str,
    referer: str,
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    seen_keys: set[str],
    buffer: int,
    should_stop: StopFn | None,
    log: LogFn | None,
    prefer_hant: bool = False,
) -> list[dict]:
    found: list[dict] = []
    if not pages or buffer <= 0 or _stopped(should_stop):
        return found

    parsed_items: list[dict] = []
    for page_url, html in _fetch_pages_parallel(pages, referer, log):
        parsed = parse_list(html)
        _log(log, f"{source_site} {page_url} 解析 {len(parsed)} 筆")
        parsed_items.extend(parsed)

    ready: list[dict] = []
    missing_author: list[dict] = []
    for raw in parsed_items:
        title = str(raw.get("title") or "")
        if not has_han(title):
            continue
        if raw.get("author"):
            ready.append(raw)
        else:
            missing_author.append(raw)

    def _take(item: dict) -> bool:
        if len(found) >= buffer or _stopped(should_stop):
            return False
        key = _accept_item(
            item,
            existing_keys,
            seen_keys,
            from_date,
            to_date,
            category_id,
            prefer_hant=prefer_hant,
        )
        if not key:
            return False
        seen_keys.add(key)
        item["sourceSite"] = source_site
        item["sourceName"] = source_name
        found.append(to_candidate(item, category_id, from_date, to_date))
        return True

    for raw in ready:
        if not _take(raw) and len(found) >= buffer:
            break

    remaining = buffer - len(found)
    if remaining > 0 and missing_author and not _stopped(should_stop):
        extra = missing_author[: remaining * 2]
        for item in _enrich_parallel(
            extra, parse_detail, referer, remaining, should_stop, log, source_site
        ):
            if not _take(item) and len(found) >= buffer:
                break
    return found


def _collect_taaze_classic(
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    seen_keys: set[str],
    buffer: int,
    should_stop: StopFn | None,
    log: LogFn | None,
    prefer_hant: bool = False,
) -> list[dict]:
    """Fill buffer from 讀冊歷年／年度暢銷百大 JSON lists; stop at quota."""
    found: list[dict] = []
    lists = TAAZE_CLASSIC_LISTS.get(category_id) or []
    for list_id, source_name in lists:
        if len(found) >= buffer or _stopped(should_stop):
            break
        rows_found = 0
        last_error: Exception | None = None
        try:
            for rows in iter_taaze_tag_pages(list_id):
                if len(found) >= buffer or _stopped(should_stop):
                    break
                rows_found += len(rows)
                for item in rows:
                    if len(found) >= buffer or _stopped(should_stop):
                        break
                    item["sourceName"] = source_name
                    key = _accept_item(
                        item,
                        existing_keys,
                        seen_keys,
                        from_date,
                        to_date,
                        category_id,
                        classic=True,
                        prefer_hant=prefer_hant,
                    )
                    if not key:
                        continue
                    seen_keys.add(key)
                    found.append(to_candidate(item, category_id, from_date, to_date))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        if last_error is not None:
            _log(log, f"讀冊經典榜失敗 {list_id}：{last_error}")
            continue
        _log(log, f"{source_name} 解析 {rows_found} 筆，累計合格 {len(found)} 本")
    return found


def scrape_category(
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    quota: int,
    should_stop: StopFn | None = None,
    log: LogFn | None = None,
    prefer_hant: bool = False,
) -> list[dict]:
    """Find extra Chinese candidates for one category. Caller stops at quota after reserve."""
    if category_id not in CATEGORY_LABELS:
        raise ValueError(f"未知主題：{category_id}")
    buffer = quota + 1
    label = CATEGORY_LABELS[category_id]
    seen_keys: set[str] = set()
    collected: list[dict] = []
    historical = False
    try:
        start = date.fromisoformat(from_date)
        end = date.fromisoformat(to_date)
        today = datetime.now().date()
        try:
            year_ago = date(today.year - 1, today.month, today.day)
        except ValueError:
            year_ago = date(today.year - 1, today.month, today.day - 1)
        # 長區間或截止日期已超過一年，改走讀冊經典榜，而不是近 30 天新書榜。
        historical = (end - start).days >= 365 * 2 or end <= year_ago
    except ValueError:
        historical = False

    if historical and category_id in TAAZE_CLASSIC_LISTS:
        _log(log, f"開始抓 讀冊經典榜／{label}，目標緩衝 {buffer} 本")
        collected.extend(
            _collect_taaze_classic(
                category_id,
                from_date,
                to_date,
                existing_keys,
                seen_keys,
                buffer,
                should_stop,
                log,
                prefer_hant=prefer_hant,
            )
        )
        _log(log, f"讀冊經典榜／{label} 累計合格 {len(collected)} 本")
        # 經典區間不要再打新書榜；新書日期幾乎都會被刷掉，只會拖時間。
        if collected:
            return collected

    sources = [
        (
            BOOKS_URLS[category_id],
            parse_books_list,
            parse_books_detail,
            "博客來",
            f"博客來中文書－{label}{'經典' if historical else ''}暢銷榜",
            "https://www.books.com.tw/",
        ),
        (
            KINGSTONE_URLS[category_id],
            parse_kingstone_list,
            parse_kingstone_detail,
            "金石堂",
            f"金石堂暢銷－{label}",
            "https://www.kingstone.com.tw/",
        ),
        (
            TAAZE_URLS[category_id],
            parse_taaze_list,
            parse_taaze_detail,
            "讀冊",
            f"讀冊暢銷－{label}",
            "https://www.taaze.tw/",
        ),
    ]
    for pages, parse_list, parse_detail, site, name, referer in sources:
        if _stopped(should_stop) or len(collected) >= buffer:
            break
        _log(log, f"開始抓 {site}／{label}，目標緩衝 {buffer} 本")
        batch = _collect_from_pages(
            pages,
            parse_list,
            parse_detail,
            site,
            name,
            referer,
            category_id,
            from_date,
            to_date,
            existing_keys,
            seen_keys,
            buffer - len(collected),
            should_stop,
            log,
            prefer_hant=prefer_hant,
        )
        collected.extend(batch)
        _log(log, f"{site}／{label} 累計合格 {len(collected)} 本")
    return collected


def load_existing_keys(root: Path) -> set[str]:
    """Build title+author keys from data.json only; do not open book files."""
    manifest = json.loads((root / "data.json").read_text(encoding="utf-8-sig"))
    return {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }


def scrape_categories(
    category_ids: list[str],
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    quota: int,
    should_stop: StopFn | None = None,
    log: LogFn | None = None,
    prefer_hant: bool = False,
) -> dict[str, list[dict]]:
    """Scrape several categories in parallel."""
    results: dict[str, list[dict]] = {}
    if not category_ids:
        return results
    workers = min(4, len(category_ids))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                scrape_category,
                category_id,
                from_date,
                to_date,
                existing_keys,
                quota,
                should_stop,
                log,
                prefer_hant,
            ): category_id
            for category_id in category_ids
        }
        for future in as_completed(futures):
            category_id = futures[future]
            results[category_id] = future.result()
    return results


def commit_candidates(
    root: Path,
    payload: dict[str, list[dict]],
    quota: int,
    from_date: str,
    to_date: str,
    work_id: str,
) -> list[dict]:
    """Reserve scraped rows in-process so the agent never writes a candidates file."""
    import sys

    tools_dir = str(Path(__file__).resolve().parent)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    from findbook_writer import reserve_one

    committed: list[dict] = []
    for category_id, items in payload.items():
        got = 0
        for item in items:
            if got >= quota:
                break
            candidate = dict(item)
            if work_id:
                candidate["workId"] = work_id
            result = reserve_one(root, category_id, candidate, from_date, to_date)
            if result.get("status") == "committed":
                result.update(
                    {
                        "sourceName": candidate.get("sourceName", ""),
                        "sourceUrl": candidate.get("sourceUrl", ""),
                        "sourceDateNote": candidate.get("sourceDateNote", ""),
                        "tags": candidate.get("tags", []),
                        "summary": candidate.get("summary", ""),
                        "workId": work_id,
                        "searchDateRange": {"from": from_date, "to": to_date},
                    }
                )
                committed.append(result)
                got += 1
    return committed


def main() -> int:
    parser = argparse.ArgumentParser(description="FindBook list-page scraper")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--category-ids", required=True, help="Comma-separated categoryId list")
    parser.add_argument("--quota", type=int, required=True)
    parser.add_argument("--from-date", required=True)
    parser.add_argument("--to-date", required=True)
    parser.add_argument(
        "--out",
        default="",
        help="Optional JSON dump keyed by categoryId; omit to avoid extra files",
    )
    parser.add_argument("--commit", action="store_true", help="Reserve into data.json after scrape")
    parser.add_argument("--work-id", default="", help="Batch workId written onto reserved books")
    parser.add_argument("--hant", action="store_true", help="Drop titles/authors with simplified glyphs")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    category_ids = [item.strip() for item in args.category_ids.split(",") if item.strip()]
    existing_keys = load_existing_keys(root)
    work_id = args.work_id.strip() or datetime.now().strftime("findbook-%Y%m%d-%H%M")
    payload = scrape_categories(
        category_ids,
        args.from_date,
        args.to_date,
        existing_keys,
        args.quota,
        log=print,
        prefer_hant=args.hant,
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out_path} categories={len(payload)} candidates={sum(len(v) for v in payload.values())}")
    if args.commit:
        committed = commit_candidates(
            root,
            payload,
            args.quota,
            args.from_date,
            args.to_date,
            work_id,
        )
        print(json.dumps({"workId": work_id, "committed": committed}, ensure_ascii=False))
        counts: dict[str, int] = {category_id: 0 for category_id in category_ids}
        for item in committed:
            counts[str(item.get("categoryId", ""))] = counts.get(str(item.get("categoryId", "")), 0) + 1
        short = [category_id for category_id in category_ids if counts.get(category_id, 0) < args.quota]
        print(
            f"committed={len(committed)} workId={work_id} "
            + " ".join(f"{key}={counts.get(key, 0)}" for key in category_ids)
        )
        if short:
            raise RuntimeError(f"未達配額：{', '.join(short)}")
        return 0
    if not args.out:
        print(json.dumps(payload, ensure_ascii=False))
        total = sum(len(items) for items in payload.values())
        print(f"categories={len(payload)} candidates={total} workId={work_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
