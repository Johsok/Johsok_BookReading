# -*- coding: utf-8 -*-
"""Find_eBooks：從官方公開介面搜尋並下載免費／開放取用電子書。"""

from __future__ import annotations

import calendar
import csv
import gzip
import hashlib
import html as html_lib
import importlib
import io
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import uuid
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime
from email.message import Message
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


APP_NAME = "Find_eBooks"
APP_VERSION = "1.1.1"
USER_AGENT = (
    f"{APP_NAME}/{APP_VERSION} "
    "(https://github.com/Johsok/Johsok_BookReading; "
    "human-initiated low-volume official API client)"
)
MAX_DOWNLOAD_BYTES = 500 * 1024 * 1024
NETWORK_TIMEOUT = 20
DOWNLOAD_TIMEOUTS = {
    "ws-export.wmcloud.org": 120,
    "zh.wikibooks.org": 90,
}
READ_CHUNK = 128 * 1024
ALLOWED_EXTENSIONS = {"epub", "pdf", "txt"}

FORMAT_PREFERENCES: Dict[str, Tuple[str, ...]] = {
    "EPUB 優先": ("epub", "pdf", "txt"),
    "PDF 優先": ("pdf", "epub", "txt"),
    "純文字優先": ("txt", "epub", "pdf"),
    "任一可用格式": ("epub", "pdf", "txt"),
}

LANGUAGE_OPTIONS: Dict[str, str] = {
    "中文（繁體／簡體）": "zh",
    "全部語言": "all",
    "英文": "en",
    "日文": "ja",
}

LANGUAGE_ALIASES: Dict[str, Set[str]] = {
    "zh": {"zh", "zho", "chi", "cmn", "chinese", "中文", "漢語", "汉语"},
    "en": {"en", "eng", "english", "英文", "英語", "英语"},
    "ja": {"ja", "jpn", "japanese", "日文", "日本語", "日语"},
}

SOURCE_LABELS = {
    "oapen": "OAPEN 開放學術書",
    "openlibrary": "Open Library／Internet Archive",
    "gutenberg": "Project Gutenberg",
    "wikisource_zh": "中文維基文庫（EPUB／PDF）",
    "wikibooks_zh": "中文維基教科書頁面（PDF）",
}

SOURCE_ORDER = (
    "wikisource_zh",
    "wikibooks_zh",
    "openlibrary",
    "gutenberg",
    "oapen",
)

SOURCE_DOWNLOAD_DOMAINS: Dict[str, Tuple[str, ...]] = {
    "oapen": ("library.oapen.org",),
    "openlibrary": ("archive.org",),
    "gutenberg": ("gutenberg.pglaf.org",),
    "wikisource_zh": ("ws-export.wmcloud.org",),
    "wikibooks_zh": ("wikibooks.org", "wikimedia.org"),
}


def _build_logger() -> logging.Logger:
    logger = logging.getLogger(APP_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    try:
        base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / APP_NAME / "logs"
        base.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            base / "Find_eBooks.log",
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(message)s")
        )
        logger.addHandler(handler)
    except Exception:
        logger.addHandler(logging.NullHandler())
    return logger


LOGGER = _build_logger()


class RequestCancelled(Exception):
    """使用者取消背景工作。"""


class ProviderError(Exception):
    """單一資料來源的可恢復錯誤。"""


@dataclass
class DownloadOption:
    url: str
    extension: str
    mime_type: str = ""
    label: str = ""
    expected_md5: str = ""
    expected_size: Optional[int] = None


@dataclass
class EbookRecord:
    source: str
    source_id: str
    title: str
    authors: List[str]
    date_text: str
    date_start: date
    date_end: date
    date_kind: str
    license_text: str
    language: str
    details_url: str
    downloads: List[DownloadOption]
    rank: int = 0
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def author_text(self) -> str:
        return "; ".join(self.authors) if self.authors else "作者不詳"


@dataclass
class DownloadOutcome:
    record: EbookRecord
    status: str
    message: str
    path: str = ""
    option: Optional[DownloadOption] = None


@dataclass
class SearchConfig:
    topic: str
    start_date: date
    end_date: date
    target_count: int
    output_dir: Path
    workers: int
    format_preference: str
    language_code: str
    sources: List[str]


def wait_or_cancel(cancel_event: threading.Event, seconds: float) -> None:
    if seconds <= 0:
        return
    if cancel_event.wait(seconds):
        raise RequestCancelled()


def parse_retry_after(headers: Message) -> Optional[float]:
    value = headers.get("Retry-After") if headers else None
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return None


class HostPolicy:
    """限制同一主機的同時連線數與起始請求頻率。"""

    def __init__(self, concurrency: int, interval: float) -> None:
        self.semaphore = threading.BoundedSemaphore(concurrency)
        self.interval = interval
        self.lock = threading.Lock()
        self.next_start = 0.0

    def acquire(self, cancel_event: threading.Event) -> None:
        while not self.semaphore.acquire(timeout=0.2):
            if cancel_event.is_set():
                raise RequestCancelled()
        try:
            with self.lock:
                now = time.monotonic()
                delay = max(0.0, self.next_start - now)
                self.next_start = max(now, self.next_start) + self.interval
            wait_or_cancel(cancel_event, delay)
        except Exception:
            self.semaphore.release()
            raise

    def release(self) -> None:
        self.semaphore.release()


HOST_POLICIES: Dict[str, HostPolicy] = {
    "openlibrary.org": HostPolicy(1, 1.05),
    "archive.org": HostPolicy(4, 1.0),
    "www.gutenberg.org": HostPolicy(1, 2.0),
    "gutenberg.pglaf.org": HostPolicy(1, 2.0),
    "library.oapen.org": HostPolicy(2, 0.35),
    "zh.wikisource.org": HostPolicy(2, 0.5),
    "zh.wikibooks.org": HostPolicy(2, 0.5),
    "ws-export.wmcloud.org": HostPolicy(1, 1.0),
    "www.wikidata.org": HostPolicy(2, 0.5),
}
DEFAULT_HOST_POLICY = HostPolicy(2, 0.5)


class NetworkClient:
    def __init__(self, cancel_event: threading.Event) -> None:
        self.cancel_event = cancel_event

    def _policy(self, url: str) -> HostPolicy:
        return HOST_POLICIES.get(urlparse(url).hostname or "", DEFAULT_HOST_POLICY)

    def request_bytes(
        self,
        url: str,
        accept: str,
        max_bytes: int = 20 * 1024 * 1024,
        retries: int = 3,
    ) -> Tuple[bytes, Message, str]:
        last_error: Optional[BaseException] = None
        for attempt in range(retries):
            if self.cancel_event.is_set():
                raise RequestCancelled()
            policy = self._policy(url)
            policy.acquire(self.cancel_event)
            response = None
            try:
                request = Request(
                    url,
                    headers={
                        "User-Agent": USER_AGENT,
                        "Accept": accept,
                        "Accept-Encoding": "identity",
                    },
                )
                response = urlopen(request, timeout=NETWORK_TIMEOUT)
                content_length = safe_int(response.headers.get("Content-Length"))
                if content_length and content_length > max_bytes:
                    raise ProviderError("來源回應超過安全大小限制")
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ProviderError("來源回應超過安全大小限制")
                return data, response.headers, response.geturl()
            except HTTPError as exc:
                last_error = exc
                if exc.code == 429 or 500 <= exc.code < 600:
                    delay = parse_retry_after(exc.headers) or min(8.0, 1.2 * (2**attempt))
                else:
                    raise ProviderError(f"HTTP {exc.code}: {urlparse(url).hostname}") from exc
            except (URLError, TimeoutError, OSError) as exc:
                last_error = exc
                delay = min(8.0, 1.2 * (2**attempt))
            finally:
                try:
                    if response is not None:
                        response.close()
                finally:
                    policy.release()
            if attempt + 1 < retries:
                wait_or_cancel(self.cancel_event, delay)
        raise ProviderError(f"網路請求失敗：{last_error}")

    def get_json(self, url: str) -> Any:
        data, _, _ = self.request_bytes(url, "application/json")
        try:
            return json.loads(data.decode("utf-8-sig"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ProviderError("來源回傳的 JSON 無法解析") from exc

    def get_xml(self, url: str) -> bytes:
        data, _, _ = self.request_bytes(
            url, "application/atom+xml, application/xml;q=0.9, text/xml;q=0.8"
        )
        return data

    def download_to(
        self,
        option: DownloadOption,
        destination: Path,
        progress_callback: Optional[Any] = None,
        source: str = "",
    ) -> Tuple[int, str]:
        url = normalize_http_url(option.url)
        if source and not is_allowed_download_url(source, url):
            raise ProviderError("下載網址不在該平台的官方網域白名單")
        policy = self._policy(url)
        last_error: Optional[BaseException] = None
        part_path = destination.parent / f".find_ebooks_{uuid.uuid4().hex}.part"
        max_attempts = 2 if (urlparse(url).hostname or "") in DOWNLOAD_TIMEOUTS else 3
        for attempt in range(max_attempts):
            if self.cancel_event.is_set():
                raise RequestCancelled()
            policy.acquire(self.cancel_event)
            response = None
            try:
                request = Request(
                    url,
                    headers={
                        "User-Agent": USER_AGENT,
                        "Accept": "application/epub+zip, application/pdf, text/plain, application/octet-stream;q=0.8",
                        "Accept-Encoding": "identity",
                    },
                )
                download_timeout = DOWNLOAD_TIMEOUTS.get(
                    urlparse(url).hostname or "", NETWORK_TIMEOUT
                )
                response = urlopen(request, timeout=download_timeout)
                final_url = normalize_http_url(response.geturl())
                if source and not is_allowed_download_url(source, final_url):
                    raise ProviderError("下載重新導向到非官方網域，已拒絕儲存")
                expected_length = safe_int(response.headers.get("Content-Length"))
                if expected_length and expected_length > MAX_DOWNLOAD_BYTES:
                    raise ProviderError("檔案超過 500 MB 安全限制")
                if option.expected_size and option.expected_size > MAX_DOWNLOAD_BYTES:
                    raise ProviderError("檔案超過 500 MB 安全限制")
                total = 0
                digest = hashlib.md5() if option.expected_md5 else None
                destination.parent.mkdir(parents=True, exist_ok=True)
                with part_path.open("wb") as output:
                    while True:
                        if self.cancel_event.is_set():
                            raise RequestCancelled()
                        chunk = response.read(READ_CHUNK)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > MAX_DOWNLOAD_BYTES:
                            raise ProviderError("檔案超過 500 MB 安全限制")
                        output.write(chunk)
                        if digest:
                            digest.update(chunk)
                        if progress_callback:
                            progress_callback(total, expected_length or option.expected_size)
                if expected_length is not None and total != expected_length:
                    raise ProviderError("下載內容不完整")
                if option.expected_size is not None and total != option.expected_size:
                    raise ProviderError("檔案大小與來源資料不符")
                if digest and digest.hexdigest().lower() != option.expected_md5.lower():
                    raise ProviderError("檔案 MD5 驗證失敗")
                validate_download(part_path, option.extension)
                os.replace(str(part_path), str(destination))
                return total, response.geturl()
            except RequestCancelled:
                raise
            except HTTPError as exc:
                last_error = exc
                if exc.code == 429 or 500 <= exc.code < 600:
                    delay = parse_retry_after(exc.headers) or min(8.0, 1.2 * (2**attempt))
                else:
                    raise ProviderError(f"HTTP {exc.code}") from exc
            except ProviderError:
                raise
            except (URLError, TimeoutError, OSError) as exc:
                last_error = exc
                delay = min(8.0, 1.2 * (2**attempt))
            finally:
                try:
                    if response is not None:
                        response.close()
                finally:
                    policy.release()
                try:
                    if part_path.exists():
                        part_path.unlink()
                except OSError:
                    pass
            if attempt + 1 < max_attempts:
                wait_or_cancel(self.cancel_event, delay)
        raise ProviderError(str(last_error or "下載失敗"))


def normalize_http_url(url: str) -> str:
    parsed = urlparse((url or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ProviderError("來源提供了不安全或無效的下載網址")
    if parsed.scheme == "http":
        parsed = parsed._replace(scheme="https")
    return urlunparse(parsed)


def is_allowed_download_url(source: str, url: str) -> bool:
    try:
        hostname = (urlparse(normalize_http_url(url)).hostname or "").lower().rstrip(".")
    except ProviderError:
        return False
    allowed_domains = SOURCE_DOWNLOAD_DOMAINS.get(source, ())
    return any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in allowed_domains
    )


def validate_download(path: Path, extension: str) -> None:
    extension = extension.lower().lstrip(".")
    if path.stat().st_size <= 0:
        raise ProviderError("下載檔案是空的")
    if extension == "pdf":
        with path.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                raise ProviderError("下載內容不是有效 PDF")
    elif extension == "epub":
        if not zipfile.is_zipfile(path):
            raise ProviderError("下載內容不是有效 EPUB")
        try:
            with zipfile.ZipFile(path) as archive:
                names = set(archive.namelist())
                if "META-INF/container.xml" not in names:
                    raise ProviderError("EPUB 缺少必要的 container.xml")
        except zipfile.BadZipFile as exc:
            raise ProviderError("EPUB 壓縮檔已損壞") from exc
    elif extension == "txt":
        with path.open("rb") as handle:
            sample = handle.read(4096)
        lowered = sample.lstrip().lower()
        if lowered.startswith((b"<!doctype html", b"<html", b"<?xml")):
            raise ProviderError("下載連結回傳網頁而非文字書")
        if sample and sample.count(b"\x00") > max(2, len(sample) // 20):
            raise ProviderError("下載內容不像純文字檔")
    else:
        raise ProviderError("不支援的檔案格式")


def validate_existing_download(path: Path, option: DownloadOption) -> None:
    validate_download(path, option.extension)
    size = path.stat().st_size
    if option.expected_size is not None and size != option.expected_size:
        raise ProviderError("既有檔案大小與來源資料不符")
    if option.expected_md5:
        digest = hashlib.md5()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(READ_CHUNK), b""):
                digest.update(chunk)
        if digest.hexdigest().lower() != option.expected_md5.lower():
            raise ProviderError("既有檔案 MD5 與來源資料不符")


def parse_metadata_date(value: Any) -> Optional[Tuple[date, date, str]]:
    if value is None:
        return None
    text = str(value).strip()
    match = re.search(r"(?<!\d)(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", text)
    if not match:
        return None
    year = int(match.group(1))
    if year < 1 or year > 9999:
        return None
    month_text, day_text = match.group(2), match.group(3)
    try:
        if not month_text:
            return date(year, 1, 1), date(year, 12, 31), "year"
        month = int(month_text)
        if not day_text:
            last_day = calendar.monthrange(year, month)[1]
            return date(year, month, 1), date(year, month, last_day), "month"
        exact = date(year, month, int(day_text))
        return exact, exact, "day"
    except ValueError:
        return None


def ranges_overlap(
    item_start: date, item_end: date, selected_start: date, selected_end: date
) -> bool:
    return item_start <= selected_end and item_end >= selected_start


def first_nonempty(values: Iterable[Any], default: str = "") -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def safe_int(value: Any) -> Optional[int]:
    try:
        number = int(value)
        return number if number >= 0 else None
    except (TypeError, ValueError):
        return None


def metadata_map(raw: Any) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    if isinstance(raw, dict):
        for key, value in raw.items():
            for item in ensure_list(value):
                if isinstance(item, dict):
                    item = item.get("value", "")
                if item is not None and str(item).strip():
                    result.setdefault(str(key), []).append(str(item).strip())
        return result
    for item in ensure_list(raw):
        if not isinstance(item, dict):
            continue
        key = item.get("key") or item.get("name")
        value = item.get("value")
        if key and value is not None and str(value).strip():
            result.setdefault(str(key), []).append(str(value).strip())
    return result


def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(char for char in value if char.isalnum())


def detected_language_codes(value: str) -> Set[str]:
    normalized = unicodedata.normalize("NFKC", value or "").casefold()
    tokens = {
        token
        for token in re.split(r"[\s,;/|()\[\]]+", normalized)
        if token
    }
    tokens.update(
        token.replace("_", "-").split("-", 1)[0]
        for token in list(tokens)
        if token
    )
    detected: Set[str] = set()
    for code, aliases in LANGUAGE_ALIASES.items():
        if tokens.intersection(aliases) or any(
            alias in normalized for alias in aliases if len(alias) > 2
        ):
            detected.add(code)
    return detected


def canonical_language(value: str) -> str:
    detected = detected_language_codes(value)
    for preferred in ("zh", "en", "ja"):
        if preferred in detected:
            return preferred
    return normalize_key(value)


def language_matches(value: str, requested_code: str) -> bool:
    if requested_code == "all":
        return True
    return requested_code in detected_language_codes(value)


def openlibrary_language_code(requested_code: str) -> str:
    return {"zh": "chi", "en": "eng", "ja": "jpn"}.get(requested_code, "")


def wikidata_publication_date(entity: Any) -> Optional[Tuple[str, date, date]]:
    if not isinstance(entity, dict):
        return None
    claims = entity.get("claims") or {}
    for property_id in ("P577", "P571"):
        for claim in ensure_list(claims.get(property_id)):
            try:
                value = claim["mainsnak"]["datavalue"]["value"]
                raw_time = str(value.get("time") or "")
                precision = int(value.get("precision") or 9)
            except (KeyError, TypeError, ValueError, AttributeError):
                continue
            match = re.match(r"^\+(\d{1,4})-(\d{2})-(\d{2})T", raw_time)
            if not match:
                continue
            year, month, day = (int(part) for part in match.groups())
            if not 1 <= year <= 9999:
                continue
            if precision == 8:
                start_year = max(1, (year // 10) * 10)
                end_year = min(9999, start_year + 9)
                return (
                    f"約 {start_year:04d}–{end_year:04d}",
                    date(start_year, 1, 1),
                    date(end_year, 12, 31),
                )
            if precision == 7:
                start_year = max(1, ((year - 1) // 100) * 100 + 1)
                end_year = min(9999, start_year + 99)
                return (
                    f"約 {start_year:04d}–{end_year:04d}",
                    date(start_year, 1, 1),
                    date(end_year, 12, 31),
                )
            if precision < 7:
                continue
            if precision >= 11 and month >= 1 and day >= 1:
                date_text = f"{year:04d}-{month:02d}-{day:02d}"
            elif precision >= 10 and month >= 1:
                date_text = f"{year:04d}-{month:02d}"
            else:
                date_text = f"{year:04d}"
            parsed = parse_metadata_date(date_text)
            if parsed:
                return date_text, parsed[0], parsed[1]
    return None


WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def safe_filename_component(value: str, max_length: int = 150) -> str:
    text = unicodedata.normalize("NFKC", value or "")
    text = "".join(char for char in text if unicodedata.category(char)[0] != "C")
    text = re.sub(r'[<>:"/\\|?*]+', "_", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    if not text:
        text = "未命名電子書"
    if text.upper() in WINDOWS_RESERVED:
        text = "_" + text
    if len(text) > max_length:
        text = text[:max_length].rstrip(" .")
    return text


def make_book_basename(record: EbookRecord) -> str:
    title = safe_filename_component(record.title, 90)
    author = safe_filename_component(record.authors[0] if record.authors else "作者不詳", 45)
    source_id = safe_filename_component(record.source_id, 30)
    return safe_filename_component(
        f"{title} - {author} [{record.source}-{source_id}]", 180
    )


def csv_safe_cell(value: Any) -> str:
    """避免外部書目文字在試算表中被當成公式執行。"""
    text = "" if value is None else str(value)
    if text.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text
    return text


def is_within_directory(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except (OSError, ValueError):
        return False


def solr_quote(value: str) -> str:
    escaped = re.sub(r'([+\-!(){}\[\]^"~*?:\\/])', r"\\\1", value.strip())
    return f'"{escaped}"'


def option_extension(mime_type: str, name_or_url: str) -> Optional[str]:
    mime = (mime_type or "").split(";", 1)[0].strip().lower()
    lowered = (name_or_url or "").lower().split("?", 1)[0]
    if mime in {"application/epub+zip", "application/epub"} or lowered.endswith(".epub"):
        return "epub"
    if mime == "application/pdf" or lowered.endswith(".pdf"):
        return "pdf"
    if mime.startswith("text/plain") or lowered.endswith((".txt", ".txt.utf-8")):
        return "txt"
    return None


def unique_options(options: Iterable[DownloadOption]) -> List[DownloadOption]:
    seen: Set[Tuple[str, str]] = set()
    result: List[DownloadOption] = []
    for option in options:
        if option.extension not in ALLOWED_EXTENSIONS:
            continue
        key = (option.url, option.extension)
        if key not in seen:
            seen.add(key)
            result.append(option)
    return result


class Provider:
    key = ""
    label = ""

    def search(
        self,
        topic: str,
        selected_start: date,
        selected_end: date,
        limit: int,
        language_code: str,
        client: NetworkClient,
        cancel_event: threading.Event,
    ) -> List[EbookRecord]:
        raise NotImplementedError


class OapenProvider(Provider):
    key = "oapen"
    label = SOURCE_LABELS[key]

    def search(
        self,
        topic: str,
        selected_start: date,
        selected_end: date,
        limit: int,
        language_code: str,
        client: NetworkClient,
        cancel_event: threading.Event,
    ) -> List[EbookRecord]:
        query = (
            f"{solr_quote(topic)} AND "
            "dc.date.issued_dt:"
            f"[{selected_start.isoformat()}T00:00:00Z TO "
            f"{selected_end.isoformat()}T23:59:59Z]"
        )
        params = {
            "query": query,
            "expand": "metadata,bitstreams",
            "limit": str(min(max(limit * 2, 20), 100)),
            "offset": "0",
        }
        url = "https://library.oapen.org/rest/search?" + urlencode(params)
        payload = client.get_json(url)
        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = (
                payload.get("items")
                or payload.get("results")
                or payload.get("searchResults")
                or []
            )
        else:
            items = []

        records: List[EbookRecord] = []
        for index, item in enumerate(items):
            if cancel_event.is_set():
                raise RequestCancelled()
            record = self._parse_item(item, selected_start, selected_end, index)
            if record and language_matches(record.language, language_code):
                records.append(record)
            if len(records) >= limit:
                break
        return records

    def _parse_item(
        self, item: Any, selected_start: date, selected_end: date, rank: int
    ) -> Optional[EbookRecord]:
        if not isinstance(item, dict):
            return None
        metadata = metadata_map(item.get("metadata"))
        type_values = " ".join(metadata.get("dc.type", [])).casefold()
        if (
            "chapter" in type_values
            or "book part" in type_values
            or "bookpart" in type_values
        ):
            return None
        title = first_nonempty(
            metadata.get("dc.title", []) + [item.get("name"), item.get("title")]
        )
        if not title:
            return None
        authors = (
            metadata.get("dc.contributor.author", [])
            or metadata.get("dc.creator", [])
            or metadata.get("dc.contributor", [])
        )
        date_text = first_nonempty(metadata.get("dc.date.issued", []))
        parsed_date = parse_metadata_date(date_text)
        if not parsed_date:
            return None
        item_start, item_end, _ = parsed_date
        if not ranges_overlap(item_start, item_end, selected_start, selected_end):
            return None
        options: List[DownloadOption] = []
        bitstreams = item.get("bitstreams") or item.get("files") or []
        for stream in ensure_list(bitstreams):
            if not isinstance(stream, dict):
                continue
            bundle = str(stream.get("bundleName") or stream.get("bundle") or "")
            if bundle and bundle.upper() != "ORIGINAL":
                continue
            name = str(stream.get("name") or stream.get("fileName") or "")
            mime = str(stream.get("mimeType") or stream.get("mime") or "")
            extension = option_extension(mime, name)
            retrieve_link = (
                stream.get("retrieveLink")
                or stream.get("downloadLink")
                or stream.get("url")
            )
            if not extension or not retrieve_link:
                continue
            options.append(
                DownloadOption(
                    url=urljoin("https://library.oapen.org", str(retrieve_link)),
                    extension=extension,
                    mime_type=mime,
                    label="OAPEN ORIGINAL",
                    expected_size=safe_int(stream.get("sizeBytes") or stream.get("size")),
                )
            )
        options = unique_options(options)
        if not options:
            return None
        handle = first_nonempty(
            [item.get("handle")]
            + metadata.get("dc.identifier.uri", [])
            + [item.get("uuid"), item.get("id")]
        )
        source_id = handle.rsplit("/", 1)[-1] if handle else str(item.get("uuid") or rank)
        if handle.startswith("http"):
            details_url = handle
        elif "/" in handle:
            details_url = "https://library.oapen.org/handle/" + handle.strip("/")
        else:
            details_url = "https://library.oapen.org/"
        rights = first_nonempty(
            metadata.get("dc.rights", [])
            + metadata.get("dc.rights.uri", [])
            + metadata.get("oapen.license", []),
            "OAPEN 開放取用",
        )
        language_values = metadata.get("dc.language", [])
        language = "; ".join(language_values) if language_values else "未標示"
        return EbookRecord(
            source=self.key,
            source_id=source_id,
            title=title,
            authors=authors,
            date_text=date_text,
            date_start=item_start,
            date_end=item_end,
            date_kind="出版日期（OAPEN metadata）",
            license_text=rights,
            language=language,
            details_url=details_url,
            downloads=options,
            rank=rank,
        )


class OpenLibraryProvider(Provider):
    key = "openlibrary"
    label = SOURCE_LABELS[key]

    def search(
        self,
        topic: str,
        selected_start: date,
        selected_end: date,
        limit: int,
        language_code: str,
        client: NetworkClient,
        cancel_event: threading.Event,
    ) -> List[EbookRecord]:
        query = (
            f"{solr_quote(topic)} AND ebook_access:public AND "
            f"first_publish_year:[{selected_start.year} TO {selected_end.year}]"
        )
        ol_language = openlibrary_language_code(language_code)
        if ol_language:
            query += f" AND language:{ol_language}"
        fields = (
            "key,title,author_name,first_publish_year,ia,ebook_access,"
            "language,public_scan_b"
        )
        params = {
            "q": query,
            "fields": fields,
            "limit": str(min(max(limit * 2, 12), 50)),
        }
        payload = client.get_json("https://openlibrary.org/search.json?" + urlencode(params))
        docs = payload.get("docs", []) if isinstance(payload, dict) else []
        candidates: List[Tuple[int, Dict[str, Any], List[str]]] = []
        for index, doc in enumerate(docs):
            if not isinstance(doc, dict):
                continue
            if str(doc.get("ebook_access", "")).lower() != "public":
                continue
            if doc.get("public_scan_b") is False:
                continue
            ia_ids = [str(value) for value in ensure_list(doc.get("ia")) if value]
            if ia_ids:
                candidates.append((index, doc, ia_ids[:3]))
            if len(candidates) >= min(max(limit, 8), 50):
                break

        records: List[EbookRecord] = []
        if not candidates:
            return records
        with ThreadPoolExecutor(max_workers=min(4, len(candidates))) as executor:
            futures = {
                executor.submit(
                    self._resolve_candidate,
                    index,
                    doc,
                    ia_ids,
                    selected_start,
                    selected_end,
                    client,
                ): index
                for index, doc, ia_ids in candidates
            }
            for future in as_completed(futures):
                if cancel_event.is_set():
                    for pending in futures:
                        pending.cancel()
                    raise RequestCancelled()
                try:
                    record = future.result()
                    if record and language_matches(record.language, language_code):
                        records.append(record)
                except RequestCancelled:
                    raise
                except Exception as exc:
                    LOGGER.info("Open Library candidate skipped: %s", exc)
        records.sort(key=lambda item: item.rank)
        return records[:limit]

    def _resolve_candidate(
        self,
        rank: int,
        doc: Dict[str, Any],
        ia_id: Any,
        selected_start: date,
        selected_end: date,
        client: NetworkClient,
    ) -> Optional[EbookRecord]:
        year = safe_int(doc.get("first_publish_year"))
        parsed_date = parse_metadata_date(year)
        if not parsed_date:
            return None
        item_start, item_end, _ = parsed_date
        if not ranges_overlap(item_start, item_end, selected_start, selected_end):
            return None
        ia_ids = [str(value) for value in ensure_list(ia_id) if value][:3]
        selected_ia_id = ""
        metadata: Dict[str, Any] = {}
        options: List[DownloadOption] = []
        for candidate_ia_id in ia_ids:
            try:
                metadata_payload = client.get_json(
                    "https://archive.org/metadata/"
                    + quote(candidate_ia_id, safe="")
                )
            except ProviderError as exc:
                LOGGER.info("IA edition skipped id=%s error=%s", candidate_ia_id, exc)
                continue
            if not isinstance(metadata_payload, dict):
                continue
            candidate_metadata = metadata_payload.get("metadata") or {}
            restricted = first_nonempty(
                [
                    candidate_metadata.get("access-restricted-item")
                    if isinstance(candidate_metadata, dict)
                    else "",
                    metadata_payload.get("is_dark"),
                    metadata_payload.get("nodownload"),
                ]
            ).casefold()
            if restricted in {"true", "1", "yes"}:
                continue
            candidate_options: List[DownloadOption] = []
            for file_info in ensure_list(metadata_payload.get("files")):
                if not isinstance(file_info, dict):
                    continue
                name = str(file_info.get("name") or "")
                format_name = str(file_info.get("format") or "")
                lowered_name = name.casefold()
                lowered_format = format_name.casefold()
                if (
                    not name
                    or "encrypted" in lowered_name
                    or "encrypted" in lowered_format
                    or lowered_name.endswith((".gz", ".zip"))
                    or file_info.get("private") is True
                    or str(file_info.get("private", "")).lower() == "true"
                ):
                    continue
                extension = option_extension("", name)
                if extension == "epub" and "epub" not in lowered_format:
                    continue
                if extension == "pdf" and "pdf" not in lowered_format:
                    continue
                if extension == "txt" and not any(
                    marker in lowered_format for marker in ("text", "djvu")
                ):
                    continue
                if not extension:
                    continue
                size = safe_int(file_info.get("size"))
                if size and size > MAX_DOWNLOAD_BYTES:
                    continue
                download_url = (
                    "https://archive.org/download/"
                    + quote(candidate_ia_id, safe="")
                    + "/"
                    + quote(name, safe="/")
                )
                candidate_options.append(
                    DownloadOption(
                        url=download_url,
                        extension=extension,
                        mime_type="",
                        label=format_name or "Internet Archive file",
                        expected_md5=str(file_info.get("md5") or ""),
                        expected_size=size,
                    )
                )
            candidate_options = unique_options(candidate_options)
            if candidate_options:
                selected_ia_id = candidate_ia_id
                metadata = (
                    candidate_metadata if isinstance(candidate_metadata, dict) else {}
                )
                options = candidate_options
                break
        if not selected_ia_id or not options:
            return None
        title = str(doc.get("title") or metadata.get("title") or "").strip()
        if not title:
            return None
        authors = [str(value) for value in ensure_list(doc.get("author_name")) if value]
        if not authors and isinstance(metadata, dict):
            authors = [str(value) for value in ensure_list(metadata.get("creator")) if value]
        key = str(doc.get("key") or "")
        rights_parts: List[str] = []
        for field_name in ("licenseurl", "rights", "possible-copyright-status"):
            for value in ensure_list(metadata.get(field_name)):
                text = str(value).strip()
                if text and text not in rights_parts:
                    rights_parts.append(text)
        license_text = (
            "Open Library 公開閱讀項目；Internet Archive 不保證版權狀態"
        )
        if rights_parts:
            license_text += "；來源權利資料：" + " / ".join(rights_parts)
        return EbookRecord(
            source=self.key,
            source_id=selected_ia_id,
            title=title,
            authors=authors,
            date_text=str(year),
            date_start=item_start,
            date_end=item_end,
            date_kind="作品首版年（Open Library）",
            license_text=license_text,
            language="; ".join(
                str(value) for value in ensure_list(doc.get("language")) if value
            )
            or "未標示",
            details_url=urljoin("https://openlibrary.org", key),
            downloads=options,
            rank=rank,
        )


class GutenbergProvider(Provider):
    key = "gutenberg"
    label = SOURCE_LABELS[key]
    ATOM = "{http://www.w3.org/2005/Atom}"

    def search(
        self,
        topic: str,
        selected_start: date,
        selected_end: date,
        limit: int,
        language_code: str,
        client: NetworkClient,
        cancel_event: threading.Event,
    ) -> List[EbookRecord]:
        catalog_data = self._load_catalog(client)
        try:
            csv_text = gzip.decompress(catalog_data).decode("utf-8-sig")
        except (OSError, EOFError, UnicodeError) as exc:
            LOGGER.warning("Cached Gutenberg catalog is invalid; refreshing: %s", exc)
            catalog_data = self._load_catalog(client, force_refresh=True)
            try:
                csv_text = gzip.decompress(catalog_data).decode("utf-8-sig")
            except (OSError, EOFError, UnicodeError) as refresh_exc:
                raise ProviderError("Project Gutenberg 官方壓縮書目已損壞") from refresh_exc

        normalized_topic = unicodedata.normalize("NFKC", topic).casefold().strip()
        topic_tokens = [
            token for token in re.findall(r"\w+", normalized_topic, flags=re.UNICODE) if token
        ]
        if not topic_tokens:
            topic_tokens = [normalized_topic]
        scored: List[Tuple[int, date, EbookRecord]] = []
        reader = csv.DictReader(io.StringIO(csv_text))
        for index, row in enumerate(reader):
            if index % 500 == 0 and cancel_event.is_set():
                raise RequestCancelled()
            if str(row.get("Type") or "").strip().casefold() != "text":
                continue
            date_text = str(row.get("Issued") or "").strip()
            parsed_date = parse_metadata_date(date_text)
            if not parsed_date:
                continue
            item_start, item_end, _ = parsed_date
            if not ranges_overlap(item_start, item_end, selected_start, selected_end):
                continue
            title = str(row.get("Title") or "").strip()
            authors_text = str(row.get("Authors") or "").strip()
            subjects = str(row.get("Subjects") or "").strip()
            bookshelves = str(row.get("Bookshelves") or "").strip()
            locc = str(row.get("LoCC") or "").strip()
            haystack = unicodedata.normalize(
                "NFKC", " ".join((title, authors_text, subjects, bookshelves, locc))
            ).casefold()
            if not all(token in haystack for token in topic_tokens):
                continue
            book_id = str(row.get("Text#") or "").strip()
            if not book_id.isdigit():
                continue
            title_folded = unicodedata.normalize("NFKC", title).casefold()
            subject_folded = unicodedata.normalize(
                "NFKC", f"{subjects} {bookshelves}"
            ).casefold()
            score = 1
            if normalized_topic and normalized_topic in title_folded:
                score += 8
            if normalized_topic and normalized_topic in subject_folded:
                score += 5
            score += sum(1 for token in topic_tokens if token in title_folded) * 2
            downloads = self._catalog_download_options(book_id)
            authors = [value.strip() for value in authors_text.split(";") if value.strip()]
            record = EbookRecord(
                source=self.key,
                source_id=book_id,
                title=title or f"Project Gutenberg #{book_id}",
                authors=authors,
                date_text=date_text,
                date_start=item_start,
                date_end=item_end,
                date_kind="Gutenberg 上架日（非紙本初版日）",
                license_text="Project Gutenberg：依美國公版狀態提供",
                language=str(row.get("Language") or "未標示").strip(),
                details_url=f"https://www.gutenberg.org/ebooks/{book_id}",
                downloads=downloads,
                rank=index,
            )
            if not language_matches(record.language, language_code):
                continue
            scored.append((score, item_start, record))
        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        for rank, (_, _, record) in enumerate(scored[:limit]):
            record.rank = rank
        return [item[2] for item in scored[:limit]]

    def _load_catalog(
        self, client: NetworkClient, force_refresh: bool = False
    ) -> bytes:
        catalog_url = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.gz"
        cache_path: Optional[Path] = None
        try:
            cache_root = Path(os.environ.get("LOCALAPPDATA", Path.home())) / APP_NAME / "cache"
            cache_root.mkdir(parents=True, exist_ok=True)
            cache_path = cache_root / "pg_catalog.csv.gz"
            if (
                not force_refresh
                and cache_path.exists()
                and cache_path.stat().st_size > 100_000
                and time.time() - cache_path.stat().st_mtime < 7 * 24 * 60 * 60
            ):
                return cache_path.read_bytes()
        except OSError:
            cache_path = None

        data, _, _ = client.request_bytes(
            catalog_url,
            "application/gzip, application/octet-stream;q=0.9",
            max_bytes=15 * 1024 * 1024,
            retries=3,
        )
        if cache_path is not None:
            temporary = cache_path.with_name(cache_path.name + f".{uuid.uuid4().hex}.part")
            try:
                temporary.write_bytes(data)
                os.replace(str(temporary), str(cache_path))
            except OSError:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass
        return data

    @staticmethod
    def _catalog_download_options(book_id: str) -> List[DownloadOption]:
        mirror_base = f"https://gutenberg.pglaf.org/cache/epub/{book_id}/pg{book_id}"
        options: List[DownloadOption] = []
        label = "Gutenberg 官方鏡像"
        options.extend(
            [
                DownloadOption(
                    mirror_base + "-images.epub",
                    "epub",
                    "application/epub+zip",
                    label,
                ),
                DownloadOption(
                    mirror_base + ".epub",
                    "epub",
                    "application/epub+zip",
                    label,
                ),
                DownloadOption(
                    mirror_base + ".txt", "txt", "text/plain", label
                ),
            ]
        )
        return unique_options(options)

    def _parse_feed(
        self,
        xml_data: bytes,
        feed_url: str,
        selected_start: date,
        selected_end: date,
        rank_offset: int = 0,
    ) -> Tuple[List[EbookRecord], str]:
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as exc:
            raise ProviderError("Project Gutenberg OPDS 無法解析") from exc
        records: List[EbookRecord] = []
        for index, entry in enumerate(root.findall(f"{self.ATOM}entry")):
            title = (entry.findtext(f"{self.ATOM}title") or "").strip()
            entry_id = (entry.findtext(f"{self.ATOM}id") or "").strip()
            if not title:
                continue
            issued_text = self._find_issued(entry)
            parsed_date = parse_metadata_date(issued_text)
            if not parsed_date:
                continue
            item_start, item_end, _ = parsed_date
            if not ranges_overlap(item_start, item_end, selected_start, selected_end):
                continue
            authors = [
                (author.findtext(f"{self.ATOM}name") or "").strip()
                for author in entry.findall(f"{self.ATOM}author")
            ]
            authors = [author for author in authors if author]
            options: List[DownloadOption] = []
            details_url = ""
            for link in entry.findall(f"{self.ATOM}link"):
                href = urljoin(feed_url, link.attrib.get("href", ""))
                rel = link.attrib.get("rel", "")
                mime = link.attrib.get("type", "")
                if rel == "alternate" and not details_url:
                    details_url = href
                if "acquisition" not in rel:
                    continue
                extension = option_extension(mime, href)
                if not extension:
                    continue
                original = normalize_http_url(href)
                mirror = self._mirror_url(original)
                if is_allowed_download_url(self.key, mirror):
                    options.append(
                        DownloadOption(mirror, extension, mime, "Gutenberg 官方鏡像")
                    )
            options = unique_options(options)
            if not options:
                continue
            id_match = re.search(r"/ebooks/(\d+)", entry_id + " " + details_url)
            source_id = id_match.group(1) if id_match else normalize_key(entry_id)[-30:]
            records.append(
                EbookRecord(
                    source=self.key,
                    source_id=source_id or str(rank_offset + index),
                    title=title,
                    authors=authors,
                    date_text=issued_text,
                    date_start=item_start,
                    date_end=item_end,
                    date_kind="Gutenberg 上架日（非紙本初版日）",
                    license_text="Project Gutenberg：依美國公版狀態提供",
                    language=self._find_language(entry),
                    details_url=details_url or entry_id,
                    downloads=options,
                    rank=rank_offset + index,
                )
            )
        next_url = ""
        for link in root.findall(f"{self.ATOM}link"):
            if link.attrib.get("rel") == "next":
                next_url = urljoin(feed_url, link.attrib.get("href", ""))
                break
        return records, next_url

    def _find_issued(self, entry: ET.Element) -> str:
        for element in entry.iter():
            local_name = element.tag.rsplit("}", 1)[-1].lower()
            if local_name in {"issued", "published"} and element.text:
                return element.text.strip()
        return (entry.findtext(f"{self.ATOM}updated") or "").strip()

    def _find_language(self, entry: ET.Element) -> str:
        for element in entry.iter():
            local_name = element.tag.rsplit("}", 1)[-1].lower()
            if local_name == "language" and element.text:
                return element.text.strip()
        for category in entry.findall(f"{self.ATOM}category"):
            label = category.attrib.get("label", "").lower()
            if label == "language":
                return category.attrib.get("term", "未標示")
        return "未標示"

    @staticmethod
    def _mirror_url(url: str) -> str:
        parsed = urlparse(url)
        if parsed.hostname == "www.gutenberg.org" and parsed.path.startswith(
            "/cache/epub/"
        ):
            return urlunparse(parsed._replace(netloc="gutenberg.pglaf.org"))
        return url


class ChineseWikimediaProvider(Provider):
    site_host = ""
    license_description = ""
    use_wikidata_dates = True

    def search(
        self,
        topic: str,
        selected_start: date,
        selected_end: date,
        limit: int,
        language_code: str,
        client: NetworkClient,
        cancel_event: threading.Event,
    ) -> List[EbookRecord]:
        if language_code not in {"all", "zh"}:
            return []
        search_topic = self._traditional_search_text(topic, client)
        normalized_topic = unicodedata.normalize("NFKC", search_topic).casefold()
        escaped_topic = search_topic.replace("\\", "\\\\").replace('"', '\\"')
        topic_tokens = [
            token
            for token in re.findall(r"\w+", normalized_topic, flags=re.UNICODE)
            if token
        ] or [normalized_topic]
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": f'"{escaped_topic}"',
            "srwhat": "text",
            "srnamespace": "0",
            "srlimit": str(min(max(limit * 2, 20), 50)),
            "srprop": "timestamp|titlesnippet|wordcount|size",
            "format": "json",
            "formatversion": "2",
            "utf8": "1",
        }
        api_base = f"https://{self.site_host}/w/api.php?"
        search_payload = client.get_json(api_base + urlencode(search_params))
        query_data = (
            search_payload.get("query", {}) if isinstance(search_payload, dict) else {}
        )
        search_rows = [
            row
            for row in ensure_list(query_data.get("search"))
            if isinstance(row, dict)
        ]
        title_rows: List[Dict[str, Any]] = []
        for row in search_rows:
            title = str(row.get("title") or "").strip()
            normalized_title = unicodedata.normalize("NFKC", title).casefold()
            title_snippet = str(row.get("titlesnippet") or "").casefold()
            if (
                title
                and "/" not in title
                and (
                    all(token in normalized_title for token in topic_tokens)
                    or "searchmatch" in title_snippet
                )
            ):
                title_rows.append(row)
        page_ids = [str(row.get("pageid")) for row in title_rows if row.get("pageid")]
        if not page_ids:
            return []
        detail_params = {
            "action": "query",
            "pageids": "|".join(page_ids[:50]),
            "prop": "info|pageprops",
            "inprop": "url",
            "redirects": "1",
            "format": "json",
            "formatversion": "2",
        }
        detail_payload = client.get_json(api_base + urlencode(detail_params))
        detail_query = (
            detail_payload.get("query", {}) if isinstance(detail_payload, dict) else {}
        )
        raw_details = detail_query.get("pages", [])
        if isinstance(raw_details, dict):
            detail_pages = list(raw_details.values())
        else:
            detail_pages = [
                page for page in ensure_list(raw_details) if isinstance(page, dict)
            ]
        details_by_id = {
            str(page.get("pageid")): page for page in detail_pages if page.get("pageid")
        }
        pages: List[Dict[str, Any]] = []
        for row in title_rows:
            merged = dict(row)
            merged.update(details_by_id.get(str(row.get("pageid")), {}))
            pages.append(merged)
        wikidata_dates = (
            self._load_wikidata_dates(pages, client)
            if self.use_wikidata_dates
            else {}
        )

        records: List[EbookRecord] = []
        for index, page in enumerate(pages):
            if cancel_event.is_set():
                raise RequestCancelled()
            title = str(page.get("title") or "").strip()
            normalized_title = unicodedata.normalize("NFKC", title).casefold()
            if (
                not title
                or "/" in title
                or re.search(
                    r"\((?:消歧義|消歧义|disambiguation)\)$", normalized_title
                )
                is not None
                or page.get("missing") is True
                or page.get("redirect") is True
                or "disambiguation" in (page.get("pageprops") or {})
            ):
                continue
            wikidata_id = str((page.get("pageprops") or {}).get("wikibase_item") or "")
            date_info = wikidata_dates.get(wikidata_id)
            if date_info:
                date_text, item_start, item_end = date_info
                date_kind = "原作出版／創作日期（Wikidata）"
            else:
                revision_text = str(page.get("timestamp") or "")
                parsed_date = parse_metadata_date(revision_text)
                if not parsed_date:
                    continue
                date_text = revision_text[:10]
                item_start, item_end, _ = parsed_date
                date_kind = "維基頁面最後更新日（非原作出版日）"
            if not ranges_overlap(item_start, item_end, selected_start, selected_end):
                continue
            options = unique_options(self.download_options(title))
            if not options:
                continue
            source_id = str(page.get("pageid") or normalize_key(title)[-40:])
            details_url = str(page.get("fullurl") or "")
            if not details_url:
                details_url = f"https://{self.site_host}/wiki/" + quote(
                    title.replace(" ", "_"), safe=""
                )
            records.append(
                EbookRecord(
                    source=self.key,
                    source_id=source_id,
                    title=title,
                    authors=[],
                    date_text=date_text,
                    date_start=item_start,
                    date_end=item_end,
                    date_kind=date_kind,
                    license_text=self.license_description,
                    language="中文（zh）",
                    details_url=details_url,
                    downloads=options,
                    rank=index,
                )
            )
            if len(records) >= limit:
                break
        return records

    def _traditional_search_text(
        self, topic: str, client: NetworkClient
    ) -> str:
        params = {
            "action": "parse",
            "text": f"<span>{html_lib.escape(topic)}</span>",
            "contentmodel": "wikitext",
            "prop": "text",
            "variant": "zh-hant",
            "disablelimitreport": "1",
            "disableeditsection": "1",
            "format": "json",
            "formatversion": "2",
        }
        try:
            payload = client.get_json(
                f"https://{self.site_host}/w/api.php?" + urlencode(params)
            )
            rendered = str((payload.get("parse") or {}).get("text") or "")
            plain = html_lib.unescape(re.sub(r"<[^>]+>", "", rendered))
            plain = re.sub(r"\s+", " ", plain).strip()
            return plain or topic
        except ProviderError as exc:
            LOGGER.info("Chinese variant conversion unavailable: %s", exc)
            return topic

    def _load_wikidata_dates(
        self, pages: Sequence[Dict[str, Any]], client: NetworkClient
    ) -> Dict[str, Tuple[str, date, date]]:
        item_ids = sorted(
            {
                str((page.get("pageprops") or {}).get("wikibase_item") or "")
                for page in pages
                if (page.get("pageprops") or {}).get("wikibase_item")
            }
        )[:50]
        if not item_ids:
            return {}
        params = {
            "action": "wbgetentities",
            "ids": "|".join(item_ids),
            "props": "claims",
            "format": "json",
        }
        try:
            payload = client.get_json(
                "https://www.wikidata.org/w/api.php?" + urlencode(params)
            )
        except ProviderError as exc:
            LOGGER.info("Wikidata publication dates unavailable: %s", exc)
            return {}
        entities = payload.get("entities", {}) if isinstance(payload, dict) else {}
        result: Dict[str, Tuple[str, date, date]] = {}
        for item_id in item_ids:
            parsed = wikidata_publication_date(entities.get(item_id))
            if parsed:
                result[item_id] = parsed
        return result

    def download_options(self, title: str) -> List[DownloadOption]:
        raise NotImplementedError


class ChineseWikisourceProvider(ChineseWikimediaProvider):
    key = "wikisource_zh"
    label = SOURCE_LABELS[key]
    site_host = "zh.wikisource.org"
    license_description = (
        "中文維基文庫文字依 CC BY-SA 提供；原作權利狀態請見條目"
    )

    def download_options(self, title: str) -> List[DownloadOption]:
        base_params = {
            "lang": "zh",
            "page": title,
            "credits": "true",
        }
        options: List[DownloadOption] = []
        for export_format, extension, mime in (
            ("epub", "epub", "application/epub+zip"),
            ("pdf", "pdf", "application/pdf"),
        ):
            params = dict(base_params)
            params["format"] = export_format
            options.append(
                DownloadOption(
                    "https://ws-export.wmcloud.org/tool/book.php?"
                    + urlencode(params),
                    extension,
                    mime,
                    "Wikimedia WS Export",
                )
            )
        return options


class ChineseWikibooksProvider(ChineseWikimediaProvider):
    key = "wikibooks_zh"
    label = SOURCE_LABELS[key]
    site_host = "zh.wikibooks.org"
    license_description = "中文維基教科書內容依 CC BY-SA 4.0 提供"
    use_wikidata_dates = False

    def download_options(self, title: str) -> List[DownloadOption]:
        encoded_title = quote(title.replace(" ", "_"), safe="")
        return [
            DownloadOption(
                f"https://zh.wikibooks.org/api/rest_v1/page/pdf/{encoded_title}",
                "pdf",
                "application/pdf",
                "Wikimedia PDF 服務（單一書頁）",
            )
        ]


PROVIDERS: Dict[str, Provider] = {
    "oapen": OapenProvider(),
    "openlibrary": OpenLibraryProvider(),
    "gutenberg": GutenbergProvider(),
    "wikisource_zh": ChineseWikisourceProvider(),
    "wikibooks_zh": ChineseWikibooksProvider(),
}


def deduplicate_records(records: Sequence[EbookRecord]) -> List[EbookRecord]:
    seen_source: Set[Tuple[str, str]] = set()
    seen_work: Set[Tuple[str, str, str]] = set()
    result: List[EbookRecord] = []
    for record in records:
        source_key = (record.source, normalize_key(record.source_id))
        author_key = normalize_key(record.authors[0]) if record.authors else ""
        language_key = canonical_language(record.language)
        if author_key:
            work_key = (normalize_key(record.title), author_key, language_key)
        else:
            work_key = (normalize_key(record.title), "", language_key)
        if source_key in seen_source or work_key in seen_work:
            continue
        seen_source.add(source_key)
        seen_work.add(work_key)
        result.append(record)
    return result


def interleave_by_source(
    grouped: Dict[str, List[EbookRecord]], source_order: Sequence[str]
) -> List[EbookRecord]:
    positions = {source: 0 for source in source_order}
    result: List[EbookRecord] = []
    while True:
        added = False
        for source in source_order:
            values = grouped.get(source, [])
            position = positions[source]
            if position < len(values):
                result.append(values[position])
                positions[source] = position + 1
                added = True
        if not added:
            break
    return result


class DestinationAllocator:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir.resolve()
        self.reserved: Set[str] = set()
        self.lock = threading.Lock()

    def allocate(self, basename: str, extension: str, suffix_hint: str = "") -> Path:
        extension = extension.lower().lstrip(".")
        if extension not in ALLOWED_EXTENSIONS:
            raise ProviderError("不支援的副檔名")
        with self.lock:
            available = 235 - len(str(self.output_dir)) - len(extension) - 2
            if available < 24:
                raise ProviderError("下載資料夾路徑過長，請改選較短的路徑")
            stem = safe_filename_component(basename + suffix_hint, available)
            counter = 1
            while True:
                numbered = stem if counter == 1 else f"{stem} ({counter})"
                candidate = self.output_dir / f"{numbered}.{extension}"
                key = os.path.normcase(str(candidate.resolve()))
                if key not in self.reserved:
                    self.reserved.add(key)
                    if not is_within_directory(candidate, self.output_dir):
                        raise ProviderError("下載路徑超出指定資料夾")
                    return candidate
                counter += 1


def ordered_download_options(
    record: EbookRecord, preference_name: str
) -> List[DownloadOption]:
    preference = FORMAT_PREFERENCES.get(
        preference_name, FORMAT_PREFERENCES["EPUB 優先"]
    )
    order = {extension: index for index, extension in enumerate(preference)}
    return sorted(
        record.downloads,
        key=lambda option: order.get(option.extension, len(preference)),
    )


def download_record(
    record: EbookRecord,
    preference_name: str,
    allocator: DestinationAllocator,
    client: NetworkClient,
    cancel_event: threading.Event,
    emit: Any,
) -> DownloadOutcome:
    errors: List[str] = []
    basename = make_book_basename(record)
    destinations: Dict[str, Path] = {}
    invalid_existing: Set[str] = set()
    for option in ordered_download_options(record, preference_name):
        if cancel_event.is_set():
            return DownloadOutcome(record, "cancelled", "已取消")
        try:
            destination = destinations.get(option.extension)
            if destination is None:
                destination = allocator.allocate(basename, option.extension)
                destinations[option.extension] = destination
            if destination.exists() and option.extension not in invalid_existing:
                try:
                    validate_existing_download(destination, option)
                    return DownloadOutcome(
                        record,
                        "existing",
                        "檔案已存在，未重複下載",
                        str(destination),
                        option,
                    )
                except (OSError, ProviderError):
                    invalid_existing.add(option.extension)
                    destination = allocator.allocate(
                        basename, option.extension, " - 重新下載"
                    )
                    destinations[option.extension] = destination

            last_update = [0.0]

            def report_bytes(current: int, total: Optional[int]) -> None:
                now = time.monotonic()
                if now - last_update[0] >= 0.5:
                    last_update[0] = now
                    emit(
                        "book_progress",
                        {
                            "uid": record.uid,
                            "title": record.title,
                            "bytes": current,
                            "total": total,
                        },
                    )

            client.download_to(
                option, destination, report_bytes, source=record.source
            )
            return DownloadOutcome(
                record,
                "success",
                "下載完成",
                str(destination),
                option,
            )
        except RequestCancelled:
            return DownloadOutcome(record, "cancelled", "已取消")
        except Exception as exc:
            errors.append(f"{option.extension.upper()}：{exc}")
            LOGGER.info(
                "Download option failed source=%s id=%s url=%s error=%s",
                record.source,
                record.source_id,
                option.url,
                exc,
            )
    message = "；".join(errors[-3:]) if errors else "沒有可用下載格式"
    return DownloadOutcome(record, "failed", message)


def write_download_report(
    output_dir: Path, outcomes: Sequence[DownloadOutcome]
) -> Optional[Path]:
    if not outcomes:
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"download_report_{timestamp}.csv"
    counter = 2
    while report_path.exists():
        report_path = output_dir / f"download_report_{timestamp}_{counter}.csv"
        counter += 1
    fields = [
        "狀態",
        "來源",
        "來源ID",
        "書名",
        "作者",
        "日期",
        "日期意義",
        "授權或權利說明",
        "語言",
        "格式",
        "儲存路徑",
        "書目網址",
        "下載網址",
        "訊息",
    ]
    status_names = {
        "success": "下載完成",
        "existing": "已存在",
        "failed": "失敗",
        "cancelled": "取消",
    }
    with report_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for outcome in outcomes:
            record = outcome.record
            row = {
                    "狀態": status_names.get(outcome.status, outcome.status),
                    "來源": SOURCE_LABELS.get(record.source, record.source),
                    "來源ID": record.source_id,
                    "書名": record.title,
                    "作者": record.author_text,
                    "日期": record.date_text,
                    "日期意義": record.date_kind,
                    "授權或權利說明": record.license_text,
                    "語言": record.language,
                    "格式": outcome.option.extension.upper() if outcome.option else "",
                    "儲存路徑": outcome.path,
                    "書目網址": record.details_url,
                    "下載網址": outcome.option.url if outcome.option else "",
                    "訊息": outcome.message,
                }
            writer.writerow({key: csv_safe_cell(value) for key, value in row.items()})
    return report_path


class SearchCoordinator:
    def __init__(
        self,
        config: SearchConfig,
        cancel_event: threading.Event,
        event_queue: "queue.Queue[Tuple[str, Any]]",
    ) -> None:
        self.config = config
        self.cancel_event = cancel_event
        self.event_queue = event_queue

    def emit(self, event_type: str, payload: Any = None) -> None:
        self.event_queue.put((event_type, payload))

    def log(self, message: str, level: str = "info") -> None:
        self.emit("log", {"message": message, "level": level})
        getattr(LOGGER, level if level in {"info", "warning", "error"} else "info")(
            message
        )

    def run(self) -> None:
        try:
            self._run()
        except RequestCancelled:
            self.emit(
                "finished",
                {
                    "success": 0,
                    "existing": 0,
                    "failed": 0,
                    "target": self.config.target_count,
                    "cancelled": True,
                    "report": "",
                },
            )
        except Exception as exc:
            LOGGER.exception("Unhandled coordinator error")
            self.emit("fatal", str(exc))

    def _run(self) -> None:
        client = NetworkClient(self.cancel_event)
        self.emit("state", "正在平行搜尋各平台的官方公開介面…")
        per_source_limit = min(max(self.config.target_count * 2, 12), 100)
        grouped: Dict[str, List[EbookRecord]] = {
            source: [] for source in self.config.sources
        }

        def search_one(source_key: str) -> List[EbookRecord]:
            provider = PROVIDERS[source_key]
            self.log(f"開始搜尋：{provider.label}")
            return provider.search(
                self.config.topic,
                self.config.start_date,
                self.config.end_date,
                per_source_limit,
                self.config.language_code,
                client,
                self.cancel_event,
            )

        with ThreadPoolExecutor(max_workers=len(self.config.sources)) as executor:
            futures = {
                executor.submit(search_one, source): source
                for source in self.config.sources
            }
            for future in as_completed(futures):
                source = futures[future]
                if self.cancel_event.is_set():
                    for pending in futures:
                        pending.cancel()
                    raise RequestCancelled()
                try:
                    grouped[source] = [
                        record
                        for record in future.result()
                        if language_matches(record.language, self.config.language_code)
                    ]
                    count = len(grouped[source])
                    self.log(f"{SOURCE_LABELS[source]}：找到 {count} 本符合日期且可下載的書")
                    self.emit("source_done", {"source": source, "count": count})
                except RequestCancelled:
                    raise
                except Exception as exc:
                    grouped[source] = []
                    self.log(f"{SOURCE_LABELS[source]} 搜尋失敗：{exc}", "warning")
                    self.emit(
                        "source_done",
                        {"source": source, "count": 0, "error": str(exc)},
                    )

        candidates = interleave_by_source(grouped, self.config.sources)
        candidates = deduplicate_records(candidates)
        self.log(f"跨平台去重後共有 {len(candidates)} 本候選書")
        if self.cancel_event.is_set():
            raise RequestCancelled()

        allocator = DestinationAllocator(self.config.output_dir)
        outcomes: List[DownloadOutcome] = []
        success_count = 0
        existing_count = 0
        candidate_index = 0
        self.emit("progress", {"value": 0, "maximum": self.config.target_count})
        self.emit("state", "開始並行下載並驗證檔案…")

        while (
            candidate_index < len(candidates)
            and success_count + existing_count < self.config.target_count
            and not self.cancel_event.is_set()
        ):
            remaining = self.config.target_count - success_count - existing_count
            batch_size = min(self.config.workers, remaining)
            batch = candidates[candidate_index : candidate_index + batch_size]
            candidate_index += len(batch)
            if not batch:
                break
            for record in batch:
                self.emit("candidate", record)
            with ThreadPoolExecutor(max_workers=min(self.config.workers, len(batch))) as pool:
                futures = {
                    pool.submit(
                        download_record,
                        record,
                        self.config.format_preference,
                        allocator,
                        client,
                        self.cancel_event,
                        self.emit,
                    ): record
                    for record in batch
                }
                for future in as_completed(futures):
                    outcome = future.result()
                    outcomes.append(outcome)
                    if outcome.status == "success":
                        success_count += 1
                        self.log(f"下載完成：{outcome.record.title}")
                    elif outcome.status == "existing":
                        existing_count += 1
                        self.log(f"已存在：{outcome.record.title}")
                    elif outcome.status == "failed":
                        self.log(
                            f"下載失敗：{outcome.record.title}（{outcome.message}）",
                            "warning",
                        )
                    self.emit("outcome", outcome)
                    self.emit(
                        "progress",
                        {
                            "value": success_count + existing_count,
                            "maximum": self.config.target_count,
                        },
                    )

        if self.cancel_event.is_set():
            self.log("使用者取消工作", "warning")
        report_path: Optional[Path] = None
        try:
            report_path = write_download_report(self.config.output_dir, outcomes)
            if report_path:
                self.log(f"下載報告：{report_path.name}")
        except Exception as exc:
            self.log(f"無法寫入下載報告：{exc}", "warning")
        failed_count = sum(1 for item in outcomes if item.status == "failed")
        self.emit(
            "finished",
            {
                "success": success_count,
                "existing": existing_count,
                "failed": failed_count,
                "target": self.config.target_count,
                "cancelled": self.cancel_event.is_set(),
                "report": str(report_path) if report_path else "",
                "candidate_count": len(candidates),
            },
        )


class DateSelector(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        initial_date: date,
        date_entry_class: Optional[Any] = None,
    ) -> None:
        super().__init__(master)
        self.date_entry_class = date_entry_class
        self.calendar_widget: Optional[Any] = None
        self.year_var = tk.StringVar(value=str(initial_date.year))
        self.month_var = tk.StringVar(value=f"{initial_date.month:02d}")
        self.day_var = tk.StringVar(value=f"{initial_date.day:02d}")
        self.comboboxes: List[ttk.Combobox] = []
        if date_entry_class is not None:
            self.calendar_widget = date_entry_class(
                self,
                width=13,
                date_pattern="yyyy-mm-dd",
                mindate=date(1000, 1, 1),
                maxdate=date(date.today().year + 2, 12, 31),
            )
            self.calendar_widget.set_date(initial_date)
            self.calendar_widget.pack(fill="x")
        else:
            self._build_fallback(initial_date)

    def _build_fallback(self, initial_date: date) -> None:
        years = [str(year) for year in range(1000, date.today().year + 3)]
        year_box = ttk.Combobox(
            self, textvariable=self.year_var, values=years, width=6, state="readonly"
        )
        month_box = ttk.Combobox(
            self,
            textvariable=self.month_var,
            values=[f"{month:02d}" for month in range(1, 13)],
            width=3,
            state="readonly",
        )
        day_box = ttk.Combobox(
            self, textvariable=self.day_var, width=3, state="readonly"
        )
        for index, (widget, suffix) in enumerate(
            ((year_box, "年"), (month_box, "月"), (day_box, "日"))
        ):
            widget.grid(row=0, column=index * 2, sticky="w")
            ttk.Label(self, text=suffix).grid(row=0, column=index * 2 + 1, padx=(2, 5))
        year_box.bind("<<ComboboxSelected>>", self._update_days)
        month_box.bind("<<ComboboxSelected>>", self._update_days)
        self.comboboxes = [year_box, month_box, day_box]
        self._update_days()
        self.day_var.set(f"{initial_date.day:02d}")

    def _update_days(self, _event: Optional[Any] = None) -> None:
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            days = calendar.monthrange(year, month)[1]
        except ValueError:
            days = 31
        current = safe_int(self.day_var.get()) or 1
        if self.comboboxes:
            self.comboboxes[-1].configure(
                values=[f"{day:02d}" for day in range(1, days + 1)]
            )
        self.day_var.set(f"{min(current, days):02d}")

    def get_date(self) -> date:
        if self.calendar_widget is not None:
            value = self.calendar_widget.get_date()
            if isinstance(value, datetime):
                return value.date()
            return value
        return date(
            int(self.year_var.get()),
            int(self.month_var.get()),
            int(self.day_var.get()),
        )


def human_bytes(value: int) -> str:
    number = float(value)
    for unit in ("B", "KB", "MB", "GB"):
        if number < 1024 or unit == "GB":
            return f"{number:.1f} {unit}" if unit != "B" else f"{int(number)} B"
        number /= 1024
    return f"{number:.1f} GB"


class FindEbooksApp:
    def __init__(
        self,
        root: tk.Tk,
        date_entry_class: Optional[Any],
        dependency_status: str,
    ) -> None:
        self.root = root
        self.date_entry_class = date_entry_class
        self.dependency_status = dependency_status
        self.event_queue: "queue.Queue[Tuple[str, Any]]" = queue.Queue()
        self.cancel_event: Optional[threading.Event] = None
        self.worker_thread: Optional[threading.Thread] = None
        self.running = False

        self.topic_var = tk.StringVar()
        self.count_var = tk.IntVar(value=10)
        self.worker_var = tk.IntVar(value=4)
        self.format_var = tk.StringVar(value="EPUB 優先")
        self.language_var = tk.StringVar(value="中文（繁體／簡體）")
        default_output = Path.home() / "Downloads" / "eBooks"
        self.output_var = tk.StringVar(value=str(default_output))
        self.status_var = tk.StringVar(value="請輸入條件後開始搜尋")
        self.source_vars = {
            source: tk.BooleanVar(value=source != "wikibooks_zh")
            for source in SOURCE_ORDER
        }

        self.root.title(f"免費電子書搜尋下載器 v{APP_VERSION}")
        self.root.geometry("1160x790")
        self.root.minsize(900, 650)
        self._configure_style()
        self._build_menu()
        self._build_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(100, self._process_events)
        self._append_log(dependency_status, "info")

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        available = style.theme_names()
        if "vista" in available:
            style.theme_use("vista")
        style.configure("Title.TLabel", font=("Microsoft JhengHei UI", 17, "bold"))
        style.configure("Subtitle.TLabel", foreground="#4b5563")
        style.configure("Accent.TButton", font=("Microsoft JhengHei UI", 10, "bold"))

    def _build_menu(self) -> None:
        menu = tk.Menu(self.root)
        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label="資料來源與日期說明", command=self._show_source_help)
        help_menu.add_command(label="關於", command=self._show_about)
        menu.add_cascade(label="說明", menu=help_menu)
        self.root.configure(menu=menu)

    def _build_widgets(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="免費電子書搜尋下載器", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            container,
            text="只使用官方公開 API／OPDS，不繞過登入、借閱限制或 DRM。",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        form = ttk.LabelFrame(container, text="搜尋與下載條件", padding=10)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)
        form.columnconfigure(5, weight=1)

        ttk.Label(form, text="相關主題：").grid(row=0, column=0, sticky="e", padx=(0, 6))
        self.topic_entry = ttk.Entry(form, textvariable=self.topic_var)
        self.topic_entry.grid(row=0, column=1, columnspan=5, sticky="ew", pady=3)
        self.topic_entry.focus_set()

        ttk.Label(form, text="開始日期：").grid(row=1, column=0, sticky="e", padx=(0, 6))
        self.start_selector = DateSelector(
            form, date(1900, 1, 1), self.date_entry_class
        )
        self.start_selector.grid(row=1, column=1, sticky="w", pady=3)
        ttk.Label(form, text="結束日期：").grid(row=1, column=2, sticky="e", padx=(14, 6))
        self.end_selector = DateSelector(form, date.today(), self.date_entry_class)
        self.end_selector.grid(row=1, column=3, sticky="w", pady=3)
        ttk.Label(form, text="需要本數：").grid(row=1, column=4, sticky="e", padx=(14, 6))
        self.count_spin = ttk.Spinbox(
            form, from_=1, to=50, textvariable=self.count_var, width=7
        )
        self.count_spin.grid(row=1, column=5, sticky="w", pady=3)

        ttk.Label(form, text="下載格式：").grid(row=2, column=0, sticky="e", padx=(0, 6))
        self.format_combo = ttk.Combobox(
            form,
            textvariable=self.format_var,
            values=list(FORMAT_PREFERENCES),
            state="readonly",
            width=15,
        )
        self.format_combo.grid(row=2, column=1, sticky="w", pady=3)
        ttk.Label(form, text="書籍語言：").grid(row=2, column=2, sticky="e", padx=(14, 6))
        self.language_combo = ttk.Combobox(
            form,
            textvariable=self.language_var,
            values=list(LANGUAGE_OPTIONS),
            state="readonly",
            width=18,
        )
        self.language_combo.grid(row=2, column=3, sticky="w", pady=3)
        ttk.Label(form, text="同時下載：").grid(row=2, column=4, sticky="e", padx=(14, 6))
        self.worker_spin = ttk.Spinbox(
            form, from_=1, to=8, textvariable=self.worker_var, width=7
        )
        self.worker_spin.grid(row=2, column=5, sticky="w", pady=3)

        ttk.Label(form, text="下載資料夾：").grid(row=3, column=0, sticky="e", padx=(0, 6))
        self.output_entry = ttk.Entry(form, textvariable=self.output_var)
        self.output_entry.grid(row=3, column=1, columnspan=4, sticky="ew", pady=3)
        ttk.Button(form, text="選擇…", command=self._choose_output).grid(
            row=3, column=5, sticky="w", padx=(6, 0)
        )

        ttk.Label(form, text="搜尋平台：").grid(row=4, column=0, sticky="ne", padx=(0, 6), pady=3)
        source_frame = ttk.Frame(form)
        source_frame.grid(row=4, column=1, columnspan=5, sticky="w", pady=3)
        for index, source in enumerate(SOURCE_ORDER):
            ttk.Checkbutton(
                source_frame,
                text=SOURCE_LABELS[source],
                variable=self.source_vars[source],
            ).grid(
                row=index // 3,
                column=index % 3,
                sticky="w",
                padx=(0, 16),
                pady=2,
            )

        ttk.Label(
            form,
            text=(
                "日期依平台 metadata 判定：OAPEN 為出版日期、Open Library 多為首版年份、"
                "Gutenberg 為電子版上架日；維基來源優先用 Wikidata 出版日，否則用頁面更新日。"
                "只有年份時，會以該年完整區間比對。"
            ),
            foreground="#7c2d12",
            wraplength=950,
        ).grid(row=5, column=0, columnspan=6, sticky="w", pady=(5, 0))

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(10, 7))
        self.start_button = ttk.Button(
            actions,
            text="開始搜尋並下載",
            command=self._start,
            style="Accent.TButton",
        )
        self.start_button.pack(side="left")
        self.cancel_button = ttk.Button(
            actions, text="取消", command=self._cancel, state="disabled"
        )
        self.cancel_button.pack(side="left", padx=7)
        ttk.Button(actions, text="開啟下載資料夾", command=self._open_output).pack(
            side="left"
        )
        ttk.Label(actions, textvariable=self.status_var).pack(side="right", padx=(10, 0))

        self.progress = ttk.Progressbar(container, mode="determinate", maximum=10)
        self.progress.pack(fill="x", pady=(0, 8))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)
        result_frame = ttk.Frame(notebook, padding=4)
        log_frame = ttk.Frame(notebook, padding=4)
        notebook.add(result_frame, text="下載結果")
        notebook.add(log_frame, text="執行記錄")

        columns = (
            "status",
            "source",
            "language",
            "date",
            "format",
            "title",
            "author",
            "file",
        )
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        headings = {
            "status": "狀態",
            "source": "來源",
            "language": "語言",
            "date": "日期",
            "format": "格式",
            "title": "書名",
            "author": "作者",
            "file": "儲存檔案／錯誤",
        }
        widths = {
            "status": 85,
            "source": 175,
            "language": 90,
            "date": 105,
            "format": 65,
            "title": 280,
            "author": 180,
            "file": 300,
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], minwidth=60, stretch=column in {"title", "file"})
        vertical = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        horizontal = ttk.Scrollbar(result_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_frame,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            background="#111827",
            foreground="#e5e7eb",
        )
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.tag_configure("warning", foreground="#fbbf24")
        self.log_text.tag_configure("error", foreground="#f87171")
        self.log_text.tag_configure("info", foreground="#d1d5db")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll.grid(row=0, column=1, sticky="ns")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

    def _choose_output(self) -> None:
        selected = filedialog.askdirectory(
            title="選擇電子書下載資料夾",
            initialdir=self.output_var.get() or str(Path.home()),
        )
        if selected:
            self.output_var.set(selected)

    def _validate_config(self) -> SearchConfig:
        topic = self.topic_var.get().strip()
        if not topic:
            raise ValueError("請輸入相關主題")
        if len(topic) > 200:
            raise ValueError("主題文字請限制在 200 字以內")
        try:
            selected_start = self.start_selector.get_date()
            selected_end = self.end_selector.get_date()
        except (ValueError, tk.TclError) as exc:
            raise ValueError("日期格式不正確") from exc
        if selected_start > selected_end:
            raise ValueError("開始日期不可晚於結束日期")
        try:
            target_count = int(self.count_var.get())
            workers = int(self.worker_var.get())
        except (TypeError, ValueError, tk.TclError) as exc:
            raise ValueError("本數與同時下載數必須是整數") from exc
        if not 1 <= target_count <= 50:
            raise ValueError("需要本數必須介於 1 到 50")
        if not 1 <= workers <= 8:
            raise ValueError("同時下載數必須介於 1 到 8")
        output_text = self.output_var.get().strip()
        if not output_text:
            raise ValueError("請指定下載資料夾")
        output_dir = Path(output_text).expanduser()
        if not output_dir.is_absolute():
            output_dir = (Path.cwd() / output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            with tempfile.NamedTemporaryFile(dir=str(output_dir), prefix=".write_test_", delete=True):
                pass
        except OSError as exc:
            raise ValueError(f"下載資料夾無法寫入：{exc}") from exc
        sources = [source for source, variable in self.source_vars.items() if variable.get()]
        if not sources:
            raise ValueError("請至少選擇一個搜尋平台")
        preference = self.format_var.get()
        if preference not in FORMAT_PREFERENCES:
            raise ValueError("請選擇有效的下載格式")
        language_label = self.language_var.get()
        if language_label not in LANGUAGE_OPTIONS:
            raise ValueError("請選擇有效的書籍語言")
        return SearchConfig(
            topic=topic,
            start_date=selected_start,
            end_date=selected_end,
            target_count=target_count,
            output_dir=output_dir.resolve(),
            workers=workers,
            format_preference=preference,
            language_code=LANGUAGE_OPTIONS[language_label],
            sources=sources,
        )

    def _start(self) -> None:
        if self.running:
            return
        try:
            config = self._validate_config()
        except (ValueError, OSError) as exc:
            messagebox.showerror("輸入錯誤", str(exc), parent=self.root)
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.progress.configure(value=0, maximum=config.target_count)
        self.output_var.set(str(config.output_dir))
        self.cancel_event = threading.Event()
        self.running = True
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.status_var.set("準備搜尋…")
        self._append_log(
            f"任務：主題「{config.topic}」，語言「{self.language_var.get()}」，"
            f"{config.start_date} 至 {config.end_date}，目標 {config.target_count} 本",
            "info",
        )
        coordinator = SearchCoordinator(config, self.cancel_event, self.event_queue)
        self.worker_thread = threading.Thread(
            target=coordinator.run,
            name="SearchCoordinator",
            daemon=True,
        )
        self.worker_thread.start()

    def _cancel(self) -> None:
        if self.running and self.cancel_event is not None:
            self.cancel_event.set()
            self.cancel_button.configure(state="disabled")
            self.status_var.set("正在安全取消…")
            self._append_log("已送出取消要求；目前的網路區塊結束後會停止。", "warning")

    def _process_events(self) -> None:
        try:
            while True:
                event_type, payload = self.event_queue.get_nowait()
                self._handle_event(event_type, payload)
        except queue.Empty:
            pass
        try:
            self.root.after(100, self._process_events)
        except tk.TclError:
            pass

    def _handle_event(self, event_type: str, payload: Any) -> None:
        if event_type == "log":
            self._append_log(payload["message"], payload.get("level", "info"))
        elif event_type == "state":
            self.status_var.set(str(payload))
        elif event_type == "candidate":
            record: EbookRecord = payload
            values = (
                "準備中",
                SOURCE_LABELS.get(record.source, record.source),
                record.language,
                record.date_text,
                "",
                record.title,
                record.author_text,
                "",
            )
            if not self.tree.exists(record.uid):
                self.tree.insert("", "end", iid=record.uid, values=values)
        elif event_type == "book_progress":
            total = payload.get("total")
            current_text = human_bytes(payload.get("bytes", 0))
            total_text = f" / {human_bytes(total)}" if total else ""
            self.status_var.set(
                f"下載中：{payload.get('title', '')}（{current_text}{total_text}）"
            )
        elif event_type == "outcome":
            self._show_outcome(payload)
        elif event_type == "progress":
            self.progress.configure(
                maximum=payload.get("maximum", 1), value=payload.get("value", 0)
            )
        elif event_type == "fatal":
            self.running = False
            self.start_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")
            self.status_var.set("工作發生錯誤")
            self._append_log(str(payload), "error")
            messagebox.showerror("執行錯誤", str(payload), parent=self.root)
        elif event_type == "finished":
            self._finish_ui(payload)

    def _show_outcome(self, outcome: DownloadOutcome) -> None:
        record = outcome.record
        status_names = {
            "success": "完成",
            "existing": "已存在",
            "failed": "失敗",
            "cancelled": "取消",
        }
        values = (
            status_names.get(outcome.status, outcome.status),
            SOURCE_LABELS.get(record.source, record.source),
            record.language,
            record.date_text,
            outcome.option.extension.upper() if outcome.option else "",
            record.title,
            record.author_text,
            outcome.path or outcome.message,
        )
        if self.tree.exists(record.uid):
            self.tree.item(record.uid, values=values)
        else:
            self.tree.insert("", "end", iid=record.uid, values=values)

    def _finish_ui(self, summary: Dict[str, Any]) -> None:
        self.running = False
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        obtained = summary.get("success", 0) + summary.get("existing", 0)
        target = summary.get("target", 0)
        if summary.get("cancelled"):
            self.status_var.set(f"已取消；目前取得 {obtained}／{target} 本")
            return
        self.status_var.set(f"完成：取得 {obtained}／{target} 本")
        lines = [
            f"新下載：{summary.get('success', 0)} 本",
            f"原已存在：{summary.get('existing', 0)} 本",
            f"下載失敗：{summary.get('failed', 0)} 本",
            f"合計取得：{obtained}／{target} 本",
        ]
        if summary.get("report"):
            lines.append(f"報告：{summary['report']}")
        if obtained < target:
            lines.append("符合主題、日期、公開權限且有可驗證檔案的候選書不足。")
            messagebox.showwarning("工作完成但數量不足", "\n".join(lines), parent=self.root)
        else:
            messagebox.showinfo("下載完成", "\n".join(lines), parent=self.root)

    def _append_log(self, message: str, level: str = "info") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n", level)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _open_output(self) -> None:
        try:
            path = Path(self.output_var.get()).expanduser().resolve()
            path.mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            messagebox.showerror("無法開啟資料夾", str(exc), parent=self.root)

    def _show_source_help(self) -> None:
        messagebox.showinfo(
            "資料來源與日期說明",
            (
                "中文維基文庫：透過官方 WS Export 下載含署名資訊的 EPUB／PDF；"
                "優先採 Wikidata 出版日，缺少時使用頁面更新日。\n\n"
                "中文維基教科書頁面：官方 PDF 僅輸出搜尋命中的單一頁面，可能不是完整多章書，"
                "因此預設不勾選。\n\n"
                "OAPEN：開放取用學術書，日期取其出版 metadata。\n\n"
                "Open Library／Internet Archive：只搜尋 ebook_access:public，日期多為作品首版年份；"
                "公開可讀不等於全球無著作權。\n\n"
                "Project Gutenberg：美國公版電子書；日期是 Gutenberg 電子版上架日，不是紙本初版日。\n\n"
                "程式不下載需登入、需借閱、付費、DRM 或加密檔案。使用者仍須確認所在地法規。"
            ),
            parent=self.root,
        )

    def _show_about(self) -> None:
        messagebox.showinfo(
            "關於 Find_eBooks",
            (
                f"Find_eBooks v{APP_VERSION}\n"
                "使用 Python ThreadPoolExecutor 平行處理搜尋與下載。\n"
                "每次下載後會驗證 EPUB／PDF／TXT，並輸出 UTF-8 CSV 報告。"
            ),
            parent=self.root,
        )

    def _on_close(self) -> None:
        if self.running:
            should_close = messagebox.askyesno(
                "工作仍在執行",
                "要取消目前工作並關閉程式嗎？",
                parent=self.root,
            )
            if not should_close:
                return
            if self.cancel_event is not None:
                self.cancel_event.set()
        self.root.destroy()


def _run_bootstrap_command(
    window: tk.Tk, status_var: tk.StringVar, command: List[str], label: str
) -> Tuple[int, str]:
    status_var.set(label)
    window.update_idletasks()
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    with tempfile.TemporaryFile() as capture:
        try:
            process = subprocess.Popen(
                command,
                stdout=capture,
                stderr=subprocess.STDOUT,
                creationflags=creationflags,
            )
        except OSError as exc:
            return 1, str(exc)
        deadline = time.monotonic() + 180
        while process.poll() is None:
            if time.monotonic() >= deadline:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                return 1, "安裝逾時"
            try:
                window.update()
            except tk.TclError:
                process.terminate()
                return 1, "安裝視窗已關閉"
            time.sleep(0.05)
        capture.seek(0)
        output = capture.read().decode("utf-8", errors="replace")
        return int(process.returncode or 0), output


def load_or_install_date_entry() -> Tuple[Optional[Any], str]:
    try:
        module = importlib.import_module("tkcalendar")
        return module.DateEntry, "日期元件 tkcalendar 已就緒。"
    except Exception as exc:
        LOGGER.info("tkcalendar unavailable before bootstrap: %s", exc)

    window = tk.Tk()
    window.title("Find_eBooks 初次設定")
    window.geometry("430x145")
    window.resizable(False, False)
    status_var = tk.StringVar(value="準備安裝日期選擇元件…")
    ttk.Label(
        window,
        text="首次執行設定",
        font=("Microsoft JhengHei UI", 14, "bold"),
    ).pack(anchor="w", padx=18, pady=(16, 5))
    ttk.Label(window, textvariable=status_var, wraplength=390).pack(
        anchor="w", padx=18, pady=(0, 8)
    )
    progress = ttk.Progressbar(window, mode="indeterminate")
    progress.pack(fill="x", padx=18)
    progress.start(12)
    window.update()

    in_virtualenv = getattr(sys, "base_prefix", sys.prefix) != sys.prefix
    install_command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
    ]
    if not in_virtualenv:
        install_command.append("--user")
    install_command.append("tkcalendar>=1.6.1,<2")

    code, output = _run_bootstrap_command(
        window, status_var, install_command, "正在自動安裝 tkcalendar（通常只需一次）…"
    )
    if code != 0 and "No module named pip" in output:
        _run_bootstrap_command(
            window,
            status_var,
            [sys.executable, "-m", "ensurepip", "--upgrade"],
            "正在啟用 Python pip…",
        )
        code, output = _run_bootstrap_command(
            window, status_var, install_command, "重新安裝 tkcalendar…"
        )
    progress.stop()
    try:
        window.destroy()
    except tk.TclError:
        pass

    importlib.invalidate_caches()
    try:
        module = importlib.import_module("tkcalendar")
        return module.DateEntry, "已自動安裝 tkcalendar，日期可使用彈出式月曆。"
    except Exception as exc:
        LOGGER.info("tkcalendar unavailable after bootstrap: %s", exc)
        tail = " ".join(output.strip().splitlines()[-2:])[:250]
        detail = f"（{tail}）" if tail else ""
        return (
            None,
            "tkcalendar 自動安裝失敗，已改用內建年／月／日下拉選單，不影響下載功能。"
            + detail,
        )


def main() -> None:
    if sys.version_info < (3, 9):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Python 版本過舊",
            "Find_eBooks 需要 Python 3.9 或更新版本。",
            parent=root,
        )
        root.destroy()
        return
    date_entry_class, dependency_status = load_or_install_date_entry()
    root = tk.Tk()
    FindEbooksApp(root, date_entry_class, dependency_status)
    root.mainloop()


if __name__ == "__main__":
    main()
