# -*- coding: utf-8 -*-
"""FindBook 單檔工具：抓中文新書、登記 data.json、可選 Grok 150 點、結束快照。"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import tempfile
import threading
import time
import traceback
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime
from html import unescape
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
TAIPEI = ZoneInfo("Asia/Taipei")
PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
HAS_HAN = re.compile(r"[\u4e00-\u9fff]")
DATE_RE = re.compile(r"(20\d{2})[./年\-](\d{1,2})[./月\-](\d{1,2})")
LINE_RE = re.compile(r"^(\d{3})、")
XAI_URL = "https://api.x.ai/v1/chat/completions"
DEFAULT_MODEL = "grok-3"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_RESERVE_LOCK = threading.Lock()

CATEGORY_OPTIONS = [
    ("01_business_startup", "01 商業理財"),
    ("02_psychology_growth", "02 心理勵志"),
    ("03_natural_science", "03 自然科學"),
    ("04_healthcare", "04 醫療保健"),
    ("05_food_wellness", "05 飲食養生"),
    ("06_computer_info", "06 電腦資訊"),
    ("07_other", "07 其他"),
]
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
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&v=1",
    ],
    "02_psychology_growth": [
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&v=1",
    ],
    "04_healthcare": [
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_08/?o=5&v=1",
    ],
    "05_food_wellness": [
        "https://www.books.com.tw/web/books_nbtopm_09/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_09/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/09/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_09/?o=5&v=1",
    ],
    "06_computer_info": [
        "https://www.books.com.tw/web/books_nbtopm_19/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_19/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/19/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
    ],
    "07_other": [
        "https://www.books.com.tw/web/books_nbtopm_01/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_04/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_05/?o=5&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=1&page=1&v=1",
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
LogFn = Callable[[str], None]
StopFn = Callable[[], bool]


def _ensure_pyside6() -> None:
    try:
        import PySide6  # noqa: F401
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])


_ensure_pyside6()

from PySide6.QtCore import QDate, QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateEdit,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json_atomic(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        json.loads(temp_path.read_text(encoding="utf-8"))
        for attempt in range(4):
            try:
                os.replace(temp_path, path)
                break
            except PermissionError:
                if attempt == 3:
                    raise
                time.sleep(0.1 * (attempt + 1))
    finally:
        if temp_path.exists():
            temp_path.unlink()


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT_RE.sub("", value)


def now_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


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


def fetch_html(url: str, referer: str = "") -> str:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    contexts = [ssl.create_default_context(), ssl._create_unverified_context()]
    last_error: Exception | None = None
    for context in contexts:
        try:
            with urllib.request.urlopen(request, timeout=28, context=context) as response:
                raw = response.read()
            return raw.decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
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
        author = strip_html(author_match.group(1)).strip(" /|,，、")
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
        r'href="(https://www\.taaze\.tw/products/\d+\.html)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S | re.I,
    ):
        url = match.group(1)
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


def _stopped(should_stop: StopFn | None) -> bool:
    return bool(should_stop and should_stop())


def _log(log: LogFn | None, message: str) -> None:
    if log:
        log(message)


def enrich_if_needed(item: dict, parse_detail, referer: str, should_stop: StopFn | None) -> dict:
    if item.get("author") and item.get("published"):
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
    time.sleep(0.25)
    return item


def to_candidate(item: dict, category_id: str, from_date: str, to_date: str) -> dict:
    label = CATEGORY_LABELS[category_id]
    published = str(item.get("published") or "")
    today = datetime.now(TAIPEI).date().isoformat()
    if published:
        date_note = (
            f"來源標示出版日期為 {published}；擷取日期 {today}，"
            f"落在 {from_date} 至 {to_date} 的搜尋區間內。"
        )
    else:
        date_note = "來源未提供明確日期"
    title = str(item["title"]).strip()
    author = str(item["author"]).strip()
    extra = [part for part in title.replace("：", " ").replace(":", " ").split() if has_han(part)][:3]
    return {
        "title": title,
        "author": author,
        "sourceName": str(item.get("sourceName") or f"{item.get('sourceSite')}新書－{label}"),
        "sourceUrl": str(item["sourceUrl"]).strip(),
        "sourceDateNote": date_note,
        "tags": list(DEFAULT_TAGS[category_id]) + extra,
        "summary": f"整理「{title}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。",
        "published": published,
        "sourceSite": item.get("sourceSite", ""),
    }


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
) -> list[dict]:
    found: list[dict] = []
    for page_url in pages:
        if _stopped(should_stop) or len(found) >= buffer:
            break
        try:
            html = fetch_html(page_url, referer=referer)
        except Exception as exc:  # noqa: BLE001
            _log(log, f"{source_site} 列表失敗：{page_url} ({exc})")
            continue
        parsed = parse_list(html)
        _log(log, f"{source_site} {page_url} 解析 {len(parsed)} 筆")
        for raw in parsed:
            if _stopped(should_stop) or len(found) >= buffer:
                break
            try:
                item = enrich_if_needed(raw, parse_detail, referer, should_stop)
            except Exception as exc:  # noqa: BLE001
                _log(log, f"{source_site} 詳情失敗：{raw.get('sourceUrl')} ({exc})")
                continue
            title = str(item.get("title") or "")
            author = str(item.get("author") or "")
            if not has_han(title) or not author:
                continue
            key = normalized_key(title, author)
            if key in existing_keys or key in seen_keys:
                continue
            published = str(item.get("published") or "")
            if published and not in_date_range(published, from_date, to_date):
                continue
            seen_keys.add(key)
            item["sourceSite"] = source_site
            item["sourceName"] = source_name
            found.append(to_candidate(item, category_id, from_date, to_date))
        time.sleep(0.3)
    return found


def scrape_category(
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    quota: int,
    should_stop: StopFn | None = None,
    log: LogFn | None = None,
) -> list[dict]:
    if category_id not in CATEGORY_LABELS:
        raise ValueError(f"未知主題：{category_id}")
    buffer = max(quota + 2, int(quota * 1.2) + 1)
    label = CATEGORY_LABELS[category_id]
    seen_keys: set[str] = set()
    collected: list[dict] = []
    sources = [
        (BOOKS_URLS[category_id], parse_books_list, parse_books_detail, "博客來", f"博客來中文書－{label}新書／暢銷頁", "https://www.books.com.tw/"),
        (KINGSTONE_URLS[category_id], parse_kingstone_list, parse_kingstone_detail, "金石堂", f"金石堂新書－{label}", "https://www.kingstone.com.tw/"),
        (TAAZE_URLS[category_id], parse_taaze_list, parse_taaze_detail, "讀冊", f"讀冊新書－{label}", "https://www.taaze.tw/"),
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
        )
        collected.extend(batch)
        _log(log, f"{site}／{label} 累計合格 {len(collected)} 本")
    return collected


def candidate_payload(candidate: dict, book_id: str, from_date: str, to_date: str) -> dict:
    required = ("title", "author", "sourceName", "sourceUrl", "sourceDateNote", "tags", "summary")
    missing = [field for field in required if not candidate.get(field)]
    if missing:
        raise ValueError(f"候選缺少欄位：{', '.join(missing)}")
    if not isinstance(candidate["tags"], list):
        raise ValueError(f"{candidate['title']} 的 tags 不是陣列")
    payload = {
        "id": book_id,
        "title": str(candidate["title"]).strip(),
        "author": str(candidate["author"]).strip(),
        "sourceName": str(candidate["sourceName"]).strip(),
        "sourceUrl": str(candidate["sourceUrl"]).strip(),
        "sourceDateNote": str(candidate["sourceDateNote"]).strip(),
        "searchDateRange": {"from": from_date, "to": to_date},
        "tags": [str(tag).strip() for tag in candidate["tags"] if str(tag).strip()],
        "summary": str(candidate["summary"]).strip(),
        "updatedAt": to_date,
        "chatgptHighlights": [],
        "chatgptStatus": "pending_grok",
        "highlightsSource": "pending_grok",
    }
    work_id = str(candidate.get("workId", "")).strip()
    if work_id:
        payload["workId"] = work_id
    return payload


def book_relative_path(category_id: str, book_id: str) -> str:
    return f"Books/{category_id}/{book_id}.json"


def manifest_payload(book: dict, category_id: str) -> dict:
    payload = {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "categoryId": category_id,
        "tags": book["tags"],
        "sourceName": book["sourceName"],
        "sourceUrl": book["sourceUrl"],
        "file": book_relative_path(category_id, book["id"]),
    }
    if book.get("workId"):
        payload["workId"] = book["workId"]
    return payload


def allocate_id(category_id: str, to_date: str, ids: set[str]) -> str:
    base = f"{category_id}-{to_date.replace('-', '')}-"
    suffixes = []
    for book_id in ids:
        if not book_id.startswith(base):
            continue
        tail = book_id[len(base) :]
        if tail.isdigit():
            suffixes.append(int(tail))
    return f"{base}{max(suffixes, default=0) + 1:02d}"


def update_manifest_metadata(manifest: dict, from_date: str, to_date: str) -> None:
    books = manifest.get("books", [])
    manifest["totalBooks"] = len(books)
    manifest["searchDateRange"] = {"from": from_date, "to": to_date}
    manifest["generatedAt"] = now_iso()
    manifest["generatedFrom"] = "NewBook_Scraper.pyw reservation checkpoint"


def check_index_link(root: Path, book_id: str) -> None:
    root = Path(root).resolve()
    manifest = read_json(root / "data.json")
    matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
    if len(matches) != 1:
        raise RuntimeError(f"{book_id} 在 data.json 必須剛好出現一次")
    index_book = matches[0]
    category_id = str(index_book.get("categoryId", ""))
    relative_file = str(index_book.get("file", "")).replace("\\", "/")
    expected_file = book_relative_path(category_id, book_id)
    if relative_file != expected_file:
        raise RuntimeError(f"{book_id} 的 file 必須是 {expected_file}")
    book_path = root / relative_file
    if not book_path.is_file():
        raise RuntimeError(f"{book_id} 單書檔不存在：{relative_file}")
    book = read_json(book_path)
    for field in ("id", "categoryId", "title", "author"):
        if book.get(field) != index_book.get(field):
            raise RuntimeError(f"{book_id} 索引與單書的 {field} 不一致")
    files = [str(item.get("file", "")).replace("\\", "/") for item in manifest.get("books", [])]
    if files.count(relative_file) != 1:
        raise RuntimeError(f"{book_id} 的 file 在 data.json 不是唯一")


def reserve_one(root: Path, category_id: str, candidate: dict, from_date: str, to_date: str) -> dict:
    root = Path(root).resolve()
    with _RESERVE_LOCK:
        manifest_path = root / "data.json"
        manifest = read_json(manifest_path)
        valid_ids = {str(item.get("id", "")) for item in manifest.get("categories", [])}
        if category_id not in valid_ids:
            raise ValueError(f"未知主題 categoryId：{category_id}")
        key = normalized_key(str(candidate.get("title", "")), str(candidate.get("author", "")))
        manifest_books = manifest.get("books", [])
        existing_keys = {
            normalized_key(str(book.get("title", "")), str(book.get("author", "")))
            for book in manifest_books
        }
        if key in existing_keys:
            return {
                "status": "skipped",
                "reason": "duplicate",
                "title": str(candidate.get("title", "")),
                "author": str(candidate.get("author", "")),
                "categoryId": category_id,
            }
        book_directory = root / "Books" / category_id
        all_ids = {str(book.get("id", "")) for book in manifest_books}
        if book_directory.exists():
            all_ids.update(path.stem for path in book_directory.glob("*.json"))
        book_id = allocate_id(category_id, to_date, all_ids)
        book = candidate_payload(candidate, book_id, from_date, to_date)
        book["categoryId"] = category_id
        relative_file = book_relative_path(category_id, book_id)
        book_path = root / relative_file
        write_json_atomic(book_path, book)
        check_book = read_json(book_path)
        if check_book.get("id") != book_id or check_book.get("categoryId") != category_id:
            raise RuntimeError(f"{book_id} 單書 pending 骨架寫後驗證失敗")
        manifest = read_json(manifest_path)
        latest_keys = {
            normalized_key(str(item.get("title", "")), str(item.get("author", "")))
            for item in manifest.get("books", [])
        }
        if key in latest_keys:
            raise RuntimeError(f"{book_id} 單書檔已寫入，但 data.json 出現 reservation 衝突")
        manifest.setdefault("books", []).append(manifest_payload(book, category_id))
        update_manifest_metadata(manifest, from_date, to_date)
        write_json_atomic(manifest_path, manifest)
        check_manifest = read_json(manifest_path)
        if sum(item.get("id") == book_id for item in check_manifest.get("books", [])) != 1:
            raise RuntimeError(f"{book_id} data.json 寫後驗證失敗")
        check_index_link(root, book_id)
        return {
            "status": "committed",
            "id": book_id,
            "file": relative_file,
            "title": book["title"],
            "author": book["author"],
            "categoryId": category_id,
        }


def build_prompt(title: str, author: str) -> str:
    return f"""書名：{title}
作者：{author}
請用繁體中文，以 ChatGPT 電腦版常見的直接重點整理方式，由 Cursor Grok 4.6 整理本書 150 個重點；每點直接陳述一個具體且有資訊量的觀念、方法、因果、情境、行動或例子，且 150 點各自提供新的內容。
只輸出剛好 150 行，不要加入任何其他文字或空行。
第 1 至 150 行都使用固定三位數編號：001、002、……、150、；第一行必須是 001、，最後一行必須是 150、。
每行只能是「編號、完整重點句」。編號後立刻寫書籍重點正文，中間不得插入任何分類標籤、步驟標籤、面向標籤或包裝前綴。
禁止前言、結語、Markdown、項目符號、模型自述、分類名稱、固定小標、短標籤加冒號及符號「｜」。
嚴格禁止任何「X面第N步」或同型贅詞，例如「實作面第65步，」「決策面第74步，」「復盤面第70步，」「風險面第71步，」「溝通面第72步，」「節奏面第73步，」「指標面第74步，」「資源面第75步，」「驗證面第76步，」「習慣面第77步，」「邊界面第78步，」「回饋面第79步，」「優先面第80步，」「備援面第81步，」「學習面第82步，」；也禁止「第N步，」「XX面向，」「面向N，」等變體。
正確示例：065、釐清納瓦爾寶典情境中的關鍵取捨時，記住先界定要解決的價值問題，再選擇工具與資源配置方式。
錯誤示例：065、實作面第65步，釐清納瓦爾寶典情境中的關鍵取捨時，記住先界定要解決的價值問題，再選擇工具與資源配置方式。
正文不要重複書名、作者或章節名稱，不要使用「本書」、「作者指出」、「本章」、「這一章」、「第X章」等來源前綴，也不要讓多點使用相同開頭或固定句型。
同一本書的 150 點不得反覆出現相同的包裝字眼或句段，例如「從《書名》的閱讀情境……的課題時」、「在《書名》的脈絡中」、「以……為閱讀線索」、「處理《書名》相關選擇時特別容易被忽略」、「釐清核心課題時，記住」；每點必須直接從該點獨有的核心內容開始。
不得用同義改寫、重排字句、輪替標籤或反覆說明同一觀念來湊滿 150 點；相鄰或分散的重點都不可語意重複。"""


def extract_highlights(text: str) -> list[str]:
    found: dict[int, str] = {}
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("```"):
            continue
        match = LINE_RE.match(line)
        if not match:
            continue
        number = int(match.group(1))
        if 1 <= number <= 150:
            found[number] = line
    return [found[index] for index in range(1, 151) if index in found]


def call_xai(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }
    request = urllib.request.Request(
        XAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"xAI HTTP {exc.code}: {detail[:400]}") from exc
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError(f"xAI 沒有回傳內容：{body}")
    message = choices[0].get("message") or {}
    return str(message.get("content") or "")


def generate_highlights(title: str, author: str, api_key: str = "", model: str = DEFAULT_MODEL) -> list[str]:
    key = (api_key or os.environ.get("XAI_API_KEY") or "").strip()
    if not key:
        raise RuntimeError("未提供 xAI API Key，無法呼叫 Grok")
    text = call_xai(build_prompt(title, author), key, model=model or DEFAULT_MODEL)
    return extract_highlights(text)


def write_highlights(root: Path, book_id: str, highlights: list[str]) -> dict:
    root = Path(root).resolve()
    manifest = read_json(root / "data.json")
    matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
    if len(matches) != 1:
        raise RuntimeError(f"{book_id} 在 data.json 必須剛好出現一次")
    relative_file = str(matches[0]["file"])
    book_path = root / relative_file
    book = read_json(book_path)
    cleaned = extract_highlights("\n".join(highlights if isinstance(highlights, list) else []))
    if not cleaned:
        cleaned = extract_highlights("\n".join(str(item) for item in highlights))
    book["chatgptHighlights"] = cleaned
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "grok"
    book["highlightsCapturedAt"] = now_iso()
    book["updatedAt"] = now_iso()[:10]
    write_json_atomic(book_path, book)
    check_index_link(root, book_id)
    saved = read_json(book_path)
    return {"id": book_id, "file": relative_file, "count": len(saved.get("chatgptHighlights") or [])}


def _fingerprint(root: Path) -> tuple[str, float, int]:
    path = root / "data.json"
    manifest = read_json(path)
    generated = str(manifest.get("generatedAt") or "")
    return generated, path.stat().st_mtime, len(manifest.get("books") or [])


def wait_until_stable(root: Path, retries: int = 3, pause: float = 0.4) -> None:
    root = Path(root).resolve()
    previous = _fingerprint(root)
    for _ in range(retries):
        time.sleep(pause)
        current = _fingerprint(root)
        if current == previous:
            return
        previous = current
    raise RuntimeError("data.json 仍在變動，無法取得穩定快照")


def check_snapshot(root: Path) -> dict:
    root = Path(root).resolve()
    wait_until_stable(root)
    first = _fingerprint(root)
    manifest = read_json(root / "data.json")
    books = manifest.get("books") or []
    errors: list[str] = []
    warnings: list[str] = []
    total = manifest.get("totalBooks")
    if total != len(books):
        errors.append(f"totalBooks {total} != len(books) {len(books)}")
    ids = [str(item.get("id") or "") for item in books]
    files = [str(item.get("file") or "").replace("\\", "/") for item in books]
    dup_ids = [key for key, count in Counter(ids).items() if key and count > 1]
    dup_files = [key for key, count in Counter(files).items() if key and count > 1]
    if dup_ids:
        errors.append(f"重複 id：{', '.join(dup_ids[:8])}")
    if dup_files:
        errors.append(f"重複 file：{', '.join(dup_files[:8])}")
    indexed = set(files)
    disk_books = []
    for path in (root / "Books").rglob("*.json"):
        relative = path.relative_to(root).as_posix()
        if path.name.startswith("_"):
            warnings.append(f"忽略暫存檔 {relative}")
            continue
        disk_books.append(relative)
    extra = sorted(set(disk_books) - indexed)
    missing = sorted(indexed - set(disk_books))
    if extra:
        errors.append(f"未入索引的單書檔 {len(extra)} 個，例如 {', '.join(extra[:5])}")
    if missing:
        errors.append(f"索引指向不存在的檔案 {len(missing)} 個，例如 {', '.join(missing[:5])}")
    if len(disk_books) != len(books):
        errors.append(f"磁碟單書 {len(disk_books)} != 索引 {len(books)}")
    for item in books:
        book_id = str(item.get("id") or "")
        category_id = str(item.get("categoryId") or "")
        relative_file = str(item.get("file") or "").replace("\\", "/")
        expected = book_relative_path(category_id, book_id)
        if relative_file != expected:
            errors.append(f"{book_id} file {relative_file} != {expected}")
            continue
        path = root / relative_file
        if not path.is_file():
            continue
        try:
            book = read_json(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{book_id} JSON 無法解析：{exc}")
            continue
        for field in ("id", "categoryId", "title", "author"):
            if book.get(field) != item.get(field):
                errors.append(f"{book_id} 欄位 {field} 與索引不一致")
    second = _fingerprint(root)
    if second != first:
        raise RuntimeError("檢查期間 data.json 又被寫入，請重跑穩定快照")
    return {
        "ok": not errors,
        "totalBooks": total,
        "indexCount": len(books),
        "diskCount": len(disk_books),
        "errors": errors,
        "warnings": warnings,
        "generatedAt": first[0],
    }


class ScrapeWorker(QObject):
    log = Signal(str)
    progress = Signal(int, int, str)
    row = Signal(dict)
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
        self._stop = False

    def stop(self) -> None:
        self._stop = True

    def _should_stop(self) -> bool:
        return self._stop

    def _emit_log(self, message: str) -> None:
        self.log.emit(message)

    def run(self) -> None:
        try:
            self._run()
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(f"{exc}\n{traceback.format_exc()}")

    def _run(self) -> None:
        cfg = self.config
        categories: list[str] = cfg["categories"]
        quota: int = cfg["quota"]
        from_date: str = cfg["fromDate"]
        to_date: str = cfg["toDate"]
        make_highlights: bool = cfg["makeHighlights"]
        api_key: str = cfg["apiKey"]
        model: str = cfg["model"]
        work_id = f"findbook-{to_date.replace('-', '')}-{now_iso()[11:16].replace(':', '')}"
        self._emit_log(f"批次 workId={work_id}")
        self._emit_log("抓頁順序：博客來 → 金石堂 → 讀冊；登記寫入為單線。")
        manifest = read_json(ROOT / "data.json")
        existing_keys = {
            normalized_key(str(book.get("title", "")), str(book.get("author", "")))
            for book in manifest.get("books", [])
        }
        total_target = max(1, len(categories) * quota)
        done = 0
        committed_ids: list[str] = []
        for category_id in categories:
            if self._should_stop():
                break
            label = CATEGORY_LABELS[category_id]
            self.progress.emit(done, total_target, f"搜尋 {label}")
            self._emit_log(f"開始搜尋 {label}，配額 {quota}")
            candidates = scrape_category(
                category_id,
                from_date,
                to_date,
                existing_keys,
                quota,
                should_stop=self._should_stop,
                log=self._emit_log,
            )
            got = 0
            for candidate in candidates:
                if self._should_stop() or got >= quota:
                    break
                candidate["workId"] = work_id
                result = reserve_one(ROOT, category_id, candidate, from_date, to_date)
                title = candidate.get("title", "")
                author = candidate.get("author", "")
                if result.get("status") != "committed":
                    self._emit_log(f"略過（已存在）{title}")
                    continue
                book_id = result["id"]
                existing_keys.add(normalized_key(title, author))
                committed_ids.append(book_id)
                got += 1
                done += 1
                row = {
                    "id": book_id,
                    "title": title,
                    "author": author,
                    "categoryId": category_id,
                    "status": "已登記",
                }
                self.row.emit(row)
                self.progress.emit(done, total_target, f"已登記 {book_id}")
                self._emit_log(f"committed {book_id} {title}")
                if make_highlights:
                    try:
                        lines = generate_highlights(title, author, api_key=api_key, model=model)
                        saved = write_highlights(ROOT, book_id, lines)
                        row["status"] = f"重點 {saved['count']}"
                        self.row.emit(row)
                        self._emit_log(f"highlights {book_id} count={saved['count']}")
                    except Exception as exc:  # noqa: BLE001
                        row["status"] = "重點失敗，保留 pending"
                        self.row.emit(row)
                        self._emit_log(f"重點失敗 {book_id}：{exc}")
            if got < quota:
                self._emit_log(f"{label} 只登記 {got}/{quota} 本")
        self._emit_log("開始穩定快照檢查")
        report = check_snapshot(ROOT)
        if report.get("warnings"):
            for warning in report["warnings"][:12]:
                self._emit_log(f"快照提醒：{warning}")
        if report.get("ok"):
            self._emit_log(f"快照通過 totalBooks={report['totalBooks']} index={report['indexCount']}")
        else:
            for error in report.get("errors", [])[:20]:
                self._emit_log(f"快照問題：{error}")
        summary = (
            f"完成 workId={work_id}，新登記 {len(committed_ids)} 本。"
            f"快照 {'通過' if report.get('ok') else '有既有或新增連結問題'}。"
        )
        self.finished.emit(summary)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("FindBook 新書搜刮")
        self.resize(980, 720)
        self.thread: QThread | None = None
        self.worker: ScrapeWorker | None = None
        self._row_index: dict[str, int] = {}
        self._build()

    def _build(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        category_box = QGroupBox("主題")
        category_grid = QGridLayout(category_box)
        self.category_checks: dict[str, QCheckBox] = {}
        for index, (category_id, label) in enumerate(CATEGORY_OPTIONS):
            check = QCheckBox(label)
            check.setChecked(index < 3)
            self.category_checks[category_id] = check
            category_grid.addWidget(check, index // 4, index % 4)
        layout.addWidget(category_box)
        form_box = QGroupBox("參數")
        form = QFormLayout(form_box)
        self.quota_spin = QSpinBox()
        self.quota_spin.setRange(1, 20)
        self.quota_spin.setValue(5)
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        today = QDate.currentDate()
        self.to_date.setDate(today)
        self.from_date.setDate(today.addDays(-30))
        self.highlights_check = QCheckBox("登記後呼叫 xAI Grok 產生 150 點（需 API Key）")
        self.api_key = QLineEdit(os.environ.get("XAI_API_KEY", ""))
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.model = QLineEdit(DEFAULT_MODEL)
        form.addRow("每類本數", self.quota_spin)
        form.addRow("開始日期", self.from_date)
        form.addRow("結束日期", self.to_date)
        form.addRow(self.highlights_check)
        form.addRow("xAI API Key", self.api_key)
        form.addRow("Grok 模型", self.model)
        layout.addWidget(form_box)
        buttons = QHBoxLayout()
        self.start_button = QPushButton("開始")
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_job)
        self.cancel_button.clicked.connect(self.cancel_job)
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.cancel_button)
        buttons.addStretch(1)
        self.progress_label = QLabel("待命")
        buttons.addWidget(self.progress_label)
        layout.addLayout(buttons)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "書名", "作者", "主題", "狀態"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table, 2)
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view, 2)
        self.setCentralWidget(root)

    def selected_categories(self) -> list[str]:
        return [category_id for category_id, check in self.category_checks.items() if check.isChecked()]

    def start_job(self) -> None:
        categories = self.selected_categories()
        if not categories:
            QMessageBox.warning(self, "缺少主題", "請至少勾選一個主題。")
            return
        if self.highlights_check.isChecked() and not self.api_key.text().strip() and not os.environ.get("XAI_API_KEY"):
            QMessageBox.warning(self, "缺少 API Key", "要產生 150 點請填 xAI API Key，或取消勾選。")
            return
        self.table.setRowCount(0)
        self._row_index.clear()
        self.log_view.clear()
        config = {
            "categories": categories,
            "quota": int(self.quota_spin.value()),
            "fromDate": self.from_date.date().toString("yyyy-MM-dd"),
            "toDate": self.to_date.date().toString("yyyy-MM-dd"),
            "makeHighlights": self.highlights_check.isChecked(),
            "apiKey": self.api_key.text().strip(),
            "model": self.model.text().strip() or DEFAULT_MODEL,
        }
        self.thread = QThread()
        self.worker = ScrapeWorker(config)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.log.connect(self.append_log)
        self.worker.progress.connect(self.update_progress)
        self.worker.row.connect(self.upsert_row)
        self.worker.finished.connect(self.on_finished)
        self.worker.failed.connect(self.on_failed)
        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.thread.start()

    def cancel_job(self) -> None:
        if self.worker:
            self.worker.stop()
            self.append_log("已要求取消，將在目前書籍結束後停下。")

    def append_log(self, message: str) -> None:
        self.log_view.append(message)

    def update_progress(self, done: int, total: int, text: str) -> None:
        self.progress_label.setText(f"{done}/{total}　{text}")

    def upsert_row(self, payload: dict) -> None:
        book_id = str(payload.get("id") or "")
        values = [
            book_id,
            str(payload.get("title") or ""),
            str(payload.get("author") or ""),
            str(payload.get("categoryId") or ""),
            str(payload.get("status") or ""),
        ]
        if book_id in self._row_index:
            row = self._row_index[book_id]
        else:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._row_index[book_id] = row
        for column, value in enumerate(values):
            self.table.setItem(row, column, QTableWidgetItem(value))

    def on_finished(self, summary: str) -> None:
        self.append_log(summary)
        self.progress_label.setText(summary)
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def on_failed(self, message: str) -> None:
        self.append_log(message)
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        QMessageBox.critical(self, "執行失敗", message[:800])


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
