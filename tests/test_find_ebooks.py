# -*- coding: utf-8 -*-
"""Find_eBooks 的離線單元測試。"""

from __future__ import annotations

import gzip
import importlib.machinery
import importlib.util
import sys
import tempfile
import threading
import types
import unittest
from datetime import date
from pathlib import Path
from unittest import mock
import zipfile


MODULE_PATH = Path(__file__).resolve().parents[1] / "Find_eBooks.pyw"
MODULE_NAME = "find_ebooks_under_test"


def load_find_ebooks_module():
    """以 SourceFileLoader 載入 .pyw，且避免建立正式日誌檔。"""
    loader = importlib.machinery.SourceFileLoader(MODULE_NAME, str(MODULE_PATH))
    spec = importlib.util.spec_from_loader(MODULE_NAME, loader)
    if spec is None:
        raise RuntimeError("無法建立 Find_eBooks.pyw 的 module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    tkinter_stub = types.ModuleType("tkinter")
    filedialog_stub = types.ModuleType("tkinter.filedialog")
    messagebox_stub = types.ModuleType("tkinter.messagebox")
    ttk_stub = types.ModuleType("tkinter.ttk")

    class StubFrame:
        pass

    ttk_stub.Frame = StubFrame
    tkinter_stub.filedialog = filedialog_stub
    tkinter_stub.messagebox = messagebox_stub
    tkinter_stub.ttk = ttk_stub
    tkinter_modules = {
        "tkinter": tkinter_stub,
        "tkinter.filedialog": filedialog_stub,
        "tkinter.messagebox": messagebox_stub,
        "tkinter.ttk": ttk_stub,
    }
    with mock.patch.dict(sys.modules, tkinter_modules), mock.patch(
        "logging.handlers.RotatingFileHandler", side_effect=OSError("test logger disabled")
    ):
        loader.exec_module(module)
    return module


ebooks = load_find_ebooks_module()


def make_record(
    source: str,
    source_id: str,
    title: str,
    author: str = "作者",
    language: str = "zh",
):
    return ebooks.EbookRecord(
        source=source,
        source_id=source_id,
        title=title,
        authors=[author] if author else [],
        date_text="2020",
        date_start=date(2020, 1, 1),
        date_end=date(2020, 12, 31),
        date_kind="測試日期",
        license_text="測試授權",
        language=language,
        details_url="https://example.test/book",
        downloads=[ebooks.DownloadOption("https://example.test/book.epub", "epub")],
    )


class DateHelpersTests(unittest.TestCase):
    def test_parse_metadata_date_supports_year_month_and_day(self):
        self.assertEqual(
            ebooks.parse_metadata_date("出版於 2020"),
            (date(2020, 1, 1), date(2020, 12, 31), "year"),
        )
        self.assertEqual(
            ebooks.parse_metadata_date("2024-02"),
            (date(2024, 2, 1), date(2024, 2, 29), "month"),
        )
        self.assertEqual(
            ebooks.parse_metadata_date("2023-07-09T12:00:00Z"),
            (date(2023, 7, 9), date(2023, 7, 9), "day"),
        )

    def test_parse_metadata_date_rejects_missing_or_invalid_dates(self):
        for value in (None, "", "沒有日期", "0000", "2023-02-29", "2020-13-01"):
            with self.subTest(value=value):
                self.assertIsNone(ebooks.parse_metadata_date(value))

    def test_ranges_overlap_is_inclusive(self):
        self.assertTrue(
            ebooks.ranges_overlap(
                date(2020, 1, 1),
                date(2020, 12, 31),
                date(2020, 12, 31),
                date(2021, 1, 1),
            )
        )
        self.assertFalse(
            ebooks.ranges_overlap(
                date(2019, 1, 1),
                date(2019, 12, 31),
                date(2020, 1, 1),
                date(2020, 12, 31),
            )
        )


class FilenameAndFormatTests(unittest.TestCase):
    def test_safe_filename_removes_unsafe_characters_and_reserved_names(self):
        cleaned = ebooks.safe_filename_component('  書名<>:"/\\|?*\x00  . ')
        self.assertEqual(cleaned, "書名_")
        self.assertNotRegex(cleaned, r'[<>:"/\\|?*]')
        self.assertEqual(ebooks.safe_filename_component("CON"), "_CON")
        self.assertEqual(ebooks.safe_filename_component(" . \x00 "), "未命名電子書")
        self.assertEqual(ebooks.safe_filename_component("abcdefgh", 5), "abcde")

    def test_option_extension_recognizes_supported_formats(self):
        cases = (
            ("application/epub+zip; charset=binary", "download", "epub"),
            ("", "BOOK.EPUB?download=1", "epub"),
            ("application/pdf", "download", "pdf"),
            ("", "https://example.test/book.PDF", "pdf"),
            ("text/plain; charset=utf-8", "download", "txt"),
            ("", "book.txt.utf-8", "txt"),
            ("text/html", "index.html", None),
        )
        for mime, name, expected in cases:
            with self.subTest(mime=mime, name=name):
                self.assertEqual(ebooks.option_extension(mime, name), expected)

    def test_csv_cells_neutralize_spreadsheet_formulas(self):
        self.assertEqual(ebooks.csv_safe_cell("=HYPERLINK(\"x\")"), "'=HYPERLINK(\"x\")")
        self.assertEqual(ebooks.csv_safe_cell("  +SUM(1,2)"), "'  +SUM(1,2)")
        self.assertEqual(ebooks.csv_safe_cell("一般書名"), "一般書名")

    def test_download_urls_are_limited_to_provider_domains(self):
        self.assertTrue(
            ebooks.is_allowed_download_url(
                "openlibrary", "https://ia801.us.archive.org/file.epub"
            )
        )
        self.assertTrue(
            ebooks.is_allowed_download_url(
                "gutenberg", "https://gutenberg.pglaf.org/cache/book.epub"
            )
        )
        self.assertFalse(
            ebooks.is_allowed_download_url(
                "gutenberg", "https://www.gutenberg.org/cache/book.epub"
            )
        )
        self.assertTrue(
            ebooks.is_allowed_download_url(
                "wikisource_zh", "https://ws-export.wmcloud.org/tool/book.php"
            )
        )
        self.assertTrue(
            ebooks.is_allowed_download_url(
                "wikibooks_zh", "https://upload.wikimedia.org/generated.pdf"
            )
        )
        self.assertFalse(
            ebooks.is_allowed_download_url(
                "wikisource_zh", "https://ws-export.wmcloud.org.evil.example/book"
            )
        )
        self.assertFalse(
            ebooks.is_allowed_download_url(
                "oapen", "https://malicious.example/book.pdf"
            )
        )

    def test_language_aliases_support_chinese_and_multilingual_metadata(self):
        self.assertTrue(ebooks.language_matches("zh-Hant", "zh"))
        self.assertTrue(ebooks.language_matches("eng; chi", "zh"))
        self.assertTrue(ebooks.language_matches("eng; chi", "en"))
        self.assertFalse(ebooks.language_matches("eng", "zh"))
        self.assertEqual(ebooks.canonical_language("Chinese"), "zh")


class RecordOrderingTests(unittest.TestCase):
    def test_deduplicate_records_uses_source_id_and_cross_source_work_key(self):
        first = make_record("gutenberg", "1", "同一本書", "王小明", "zh")
        duplicate_source_id = make_record("gutenberg", "1", "另一標題", "另一作者", "en")
        duplicate_work = make_record("oapen", "xyz", "同一本書", "王小明", "ZH")
        unique = make_record("oapen", "abc", "獨立作品", "李小華", "zh")

        self.assertEqual(
            ebooks.deduplicate_records(
                [first, duplicate_source_id, duplicate_work, unique]
            ),
            [first, unique],
        )

    def test_interleave_by_source_round_robins_in_requested_order(self):
        g1 = make_record("gutenberg", "g1", "G1")
        g2 = make_record("gutenberg", "g2", "G2")
        o1 = make_record("oapen", "o1", "O1")
        l1 = make_record("openlibrary", "l1", "L1")
        l2 = make_record("openlibrary", "l2", "L2")
        l3 = make_record("openlibrary", "l3", "L3")

        actual = ebooks.interleave_by_source(
            {
                "gutenberg": [g1, g2],
                "oapen": [o1],
                "openlibrary": [l1, l2, l3],
            },
            ["oapen", "gutenberg", "openlibrary"],
        )
        self.assertEqual(actual, [o1, g1, l1, g2, l2, l3])

    def test_authorless_same_chinese_title_deduplicates_across_sources(self):
        first = make_record("wikisource_zh", "1", "論語", "", "zh")
        second = make_record("openlibrary", "2", "論語", "", "chi")
        self.assertEqual(ebooks.deduplicate_records([first, second]), [first])


class ProviderParserTests(unittest.TestCase):
    def test_chinese_wikisource_search_and_export_options(self):
        client = mock.Mock()
        client.get_json.side_effect = [
            {"parse": {"text": "<div><p><span>三國演義</span></p></div>"}},
            {
                "query": {
                    "search": [
                        {
                            "pageid": 7223,
                            "title": "三國演義",
                            "timestamp": "2026-05-20T11:48:30Z",
                        },
                        {
                            "pageid": 7224,
                            "title": "三國演義/第一回",
                            "timestamp": "2026-05-20T11:48:30Z",
                        },
                        {
                            "pageid": 7225,
                            "title": "三國演義 (消歧義)",
                            "timestamp": "2024-03-15T10:00:00Z",
                        },
                    ]
                }
            },
            {
                "query": {
                    "pages": [
                        {
                            "pageid": 7223,
                            "title": "三國演義",
                            "fullurl": "https://zh.wikisource.org/wiki/三國演義",
                            "pageprops": {"wikibase_item": "Q70806"},
                        },
                        {
                            "pageid": 7225,
                            "title": "三國演義 (消歧義)",
                            "fullurl": "https://zh.wikisource.org/wiki/三國演義_(消歧義)",
                            "pageprops": {},
                        }
                    ]
                }
            },
            {
                "entities": {
                    "Q70806": {
                        "claims": {
                            "P577": [
                                {
                                    "mainsnak": {
                                        "datavalue": {
                                            "value": {
                                                "time": "+1350-00-00T00:00:00Z",
                                                "precision": 7,
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            },
        ]
        records = ebooks.ChineseWikisourceProvider().search(
            "三国演义",
            date(1300, 1, 1),
            date(1400, 12, 31),
            5,
            "zh",
            client,
            threading.Event(),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.title, "三國演義")
        self.assertEqual(record.language, "中文（zh）")
        self.assertEqual(record.date_text, "約 1301–1400")
        self.assertIn("Wikidata", record.date_kind)
        self.assertEqual(
            [item.extension for item in record.downloads],
            ["epub", "pdf"],
        )
        self.assertTrue(
            record.downloads[0].url.startswith(
                "https://ws-export.wmcloud.org/tool/book.php?"
            )
        )
        self.assertIn("format=epub", record.downloads[0].url)
        self.assertIn("credits=true", record.downloads[0].url)

    def test_chinese_wikibooks_uses_revision_date_and_excludes_subpages(self):
        client = mock.Mock()
        client.get_json.side_effect = [
            {"parse": {"text": "<div><p><span>Python</span></p></div>"}},
            {
                "query": {
                    "search": [
                        {
                            "pageid": 101,
                            "title": "Python",
                            "timestamp": "2025-03-04T10:00:00Z",
                        },
                        {
                            "pageid": 102,
                            "title": "Python/語法",
                            "timestamp": "2025-03-03T10:00:00Z",
                        },
                    ]
                }
            },
            {
                "query": {
                    "pages": [
                        {
                            "pageid": 101,
                            "title": "Python",
                            "fullurl": "https://zh.wikibooks.org/wiki/Python",
                            "pageprops": {"wikibase_item": "Q28865"},
                        }
                    ]
                }
            },
        ]
        records = ebooks.ChineseWikibooksProvider().search(
            "Python",
            date(2025, 1, 1),
            date(2025, 12, 31),
            5,
            "zh",
            client,
            threading.Event(),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.title, "Python")
        self.assertEqual(record.date_text, "2025-03-04")
        self.assertIn("頁面最後更新日", record.date_kind)
        self.assertEqual(record.downloads[0].extension, "pdf")
        self.assertIn("/api/rest_v1/page/pdf/Python", record.downloads[0].url)
        self.assertEqual(client.get_json.call_count, 3)

    def test_chinese_wikimedia_sources_skip_non_chinese_filter(self):
        client = mock.Mock()
        records = ebooks.ChineseWikisourceProvider().search(
            "三國演義",
            date(1900, 1, 1),
            date(2026, 12, 31),
            5,
            "en",
            client,
            threading.Event(),
        )
        self.assertEqual(records, [])
        client.get_json.assert_not_called()

    def test_gutenberg_catalog_search_filters_topic_issued_date_and_builds_mirrors(self):
        catalog = """Text#,Type,Issued,Title,Language,Authors,Subjects,LoCC,Bookshelves
101,Text,2020-06-01,Python Data Handbook,en,Ada Author,Programming; Data,QA76,Computing
102,Text,2019-12-31,Python Data Before Range,en,Old Author,Programming; Data,QA76,Computing
103,Text,2020-07-01,Gardening Handbook,en,Green Author,Gardens,SB,Home
104,Sound,2020-08-01,Python Data Audio,en,Voice Author,Programming; Data,QA76,Computing
"""
        provider = ebooks.GutenbergProvider()
        client = mock.Mock()

        with mock.patch.object(
            provider,
            "_load_catalog",
            return_value=gzip.compress(catalog.encode("utf-8")),
        ) as load_catalog:
            records = provider.search(
                "Python Data",
                date(2020, 1, 1),
                date(2020, 12, 31),
                5,
                "all",
                client,
                threading.Event(),
            )

        load_catalog.assert_called_once_with(client)
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.source_id, "101")
        self.assertEqual(record.title, "Python Data Handbook")
        self.assertEqual(record.date_text, "2020-06-01")
        self.assertEqual(record.date_start, date(2020, 6, 1))
        self.assertEqual(record.date_end, date(2020, 6, 1))
        self.assertEqual(record.downloads[0].label, "Gutenberg 官方鏡像")
        self.assertEqual(
            record.downloads[0].url,
            "https://gutenberg.pglaf.org/cache/epub/101/pg101-images.epub",
        )
        self.assertEqual(
            [option.url for option in record.downloads],
            [
                "https://gutenberg.pglaf.org/cache/epub/101/pg101-images.epub",
                "https://gutenberg.pglaf.org/cache/epub/101/pg101.epub",
                "https://gutenberg.pglaf.org/cache/epub/101/pg101.txt",
            ],
        )

    def test_gutenberg_chinese_filter_excludes_same_topic_in_english(self):
        catalog = """Text#,Type,Issued,Title,Language,Authors,Subjects,LoCC,Bookshelves
201,Text,2020-01-01,歷史入門,zh,中文作者,歷史,DS,History
202,Text,2020-01-02,歷史概論,en,English Author,歷史,DS,History
"""
        provider = ebooks.GutenbergProvider()
        client = mock.Mock()
        with mock.patch.object(
            provider,
            "_load_catalog",
            return_value=gzip.compress(catalog.encode("utf-8")),
        ):
            records = provider.search(
                "歷史",
                date(2019, 1, 1),
                date(2021, 12, 31),
                5,
                "zh",
                client,
                threading.Event(),
            )
        self.assertEqual([record.source_id for record in records], ["201"])

    def test_open_library_search_requests_and_keeps_chinese_multilingual_book(self):
        client = mock.Mock()
        client.get_json.side_effect = [
            {
                "docs": [
                    {
                        "key": "/works/OLZH1W",
                        "title": "雙語書",
                        "author_name": ["作者"],
                        "first_publish_year": 2020,
                        "ia": ["zh-public-id"],
                        "ebook_access": "public",
                        "language": ["eng", "chi"],
                        "public_scan_b": True,
                    }
                ]
            },
            {
                "metadata": {"title": "雙語書"},
                "files": [
                    {"name": "book.epub", "format": "EPUB", "size": "40"}
                ],
            },
        ]
        records = ebooks.OpenLibraryProvider().search(
            "雙語",
            date(2019, 1, 1),
            date(2021, 12, 31),
            5,
            "zh",
            client,
            threading.Event(),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].language, "eng; chi")
        search_url = client.get_json.call_args_list[0].args[0]
        self.assertIn("language%3Achi", search_url)

    def test_gutenberg_opds_feed_parsing(self):
        xml_data = b"""<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom"
              xmlns:dcterms="http://purl.org/dc/terms/">
          <link rel="next" href="?page=2" />
          <entry>
            <title>Offline Gutenberg Book</title>
            <id>https://www.gutenberg.org/ebooks/123</id>
            <updated>2020-06-02T00:00:00Z</updated>
            <dcterms:issued>2020-06-01</dcterms:issued>
            <dcterms:language>en</dcterms:language>
            <author><name>Ada Author</name></author>
            <link rel="alternate" href="/ebooks/123" type="text/html" />
            <link rel="http://opds-spec.org/acquisition"
                  href="http://www.gutenberg.org/cache/epub/123/pg123.epub"
                  type="application/epub+zip" />
          </entry>
          <entry>
            <title>Outside Selected Range</title>
            <id>https://www.gutenberg.org/ebooks/999</id>
            <dcterms:issued>1999-01-01</dcterms:issued>
            <link rel="http://opds-spec.org/acquisition"
                  href="https://www.gutenberg.org/files/999/999.txt"
                  type="text/plain" />
          </entry>
        </feed>"""
        provider = ebooks.GutenbergProvider()

        records, next_url = provider._parse_feed(
            xml_data,
            "https://www.gutenberg.org/ebooks/search.opds/?query=offline",
            date(2020, 1, 1),
            date(2020, 12, 31),
        )

        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.source_id, "123")
        self.assertEqual(record.title, "Offline Gutenberg Book")
        self.assertEqual(record.authors, ["Ada Author"])
        self.assertEqual(record.language, "en")
        self.assertEqual([option.extension for option in record.downloads], ["epub"])
        self.assertEqual(record.downloads[0].url, "https://gutenberg.pglaf.org/cache/epub/123/pg123.epub")
        self.assertEqual(
            next_url,
            "https://www.gutenberg.org/ebooks/search.opds/?page=2",
        )

    def test_oapen_item_parsing(self):
        item = {
            "name": "Fallback title",
            "handle": "20.500.12657/777",
            "metadata": [
                {"key": "dc.title", "value": "Open Academic Book"},
                {"key": "dc.contributor.author", "value": "Grace Scholar"},
                {"key": "dc.date.issued", "value": "2021-03"},
                {"key": "dc.type", "value": "book"},
                {"key": "dc.language", "value": "en"},
                {"key": "dc.rights", "value": "CC BY 4.0"},
            ],
            "bitstreams": [
                {
                    "bundleName": "ORIGINAL",
                    "name": "academic.pdf",
                    "mimeType": "application/pdf",
                    "retrieveLink": "/server/api/core/bitstreams/777/content",
                    "sizeBytes": "12345",
                },
                {
                    "bundleName": "THUMBNAIL",
                    "name": "cover.pdf",
                    "mimeType": "application/pdf",
                    "retrieveLink": "/cover.pdf",
                },
            ],
        }
        provider = ebooks.OapenProvider()

        record = provider._parse_item(
            item, date(2021, 1, 1), date(2021, 12, 31), rank=4
        )

        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.source_id, "777")
        self.assertEqual(record.title, "Open Academic Book")
        self.assertEqual(record.authors, ["Grace Scholar"])
        self.assertEqual(record.date_start, date(2021, 3, 1))
        self.assertEqual(record.date_end, date(2021, 3, 31))
        self.assertEqual(record.license_text, "CC BY 4.0")
        self.assertEqual(len(record.downloads), 1)
        self.assertEqual(record.downloads[0].extension, "pdf")
        self.assertEqual(record.downloads[0].expected_size, 12345)
        self.assertEqual(
            record.downloads[0].url,
            "https://library.oapen.org/server/api/core/bitstreams/777/content",
        )

        chapter = dict(item)
        chapter["metadata"] = list(item["metadata"]) + [
            {"key": "dc.type", "value": "book chapter"}
        ]
        self.assertIsNone(
            provider._parse_item(
                chapter, date(2021, 1, 1), date(2021, 12, 31), rank=5
            )
        )

    def test_open_library_internet_archive_candidate_parsing(self):
        client = mock.Mock()
        client.get_json.return_value = {
            "metadata": {
                "title": "Metadata fallback",
                "creator": "Fallback Author",
                "licenseurl": "https://creativecommons.org/publicdomain/mark/1.0/",
                "rights": "Public domain",
            },
            "files": [
                {
                    "name": "book.epub",
                    "format": "EPUB",
                    "size": "42",
                    "md5": "abc123",
                },
                {"name": "book.pdf", "format": "Text PDF", "size": "84"},
                {"name": "book_djvu.txt", "format": "DjVuTXT", "size": "21"},
                {"name": "book_encrypted.epub", "format": "EPUB", "size": "12"},
                {"name": "private.pdf", "format": "Text PDF", "private": True},
                {"name": "wrong.epub", "format": "Unknown", "size": "10"},
                {
                    "name": "huge.pdf",
                    "format": "Text PDF",
                    "size": str(ebooks.MAX_DOWNLOAD_BYTES + 1),
                },
            ],
        }
        doc = {
            "key": "/works/OL123W",
            "title": "Public Domain Work",
            "author_name": ["Open Author"],
            "first_publish_year": 1925,
            "language": ["eng"],
        }
        provider = ebooks.OpenLibraryProvider()

        record = provider._resolve_candidate(
            2,
            doc,
            "archive item/1",
            date(1920, 1, 1),
            date(1930, 12, 31),
            client,
        )

        client.get_json.assert_called_once_with(
            "https://archive.org/metadata/archive%20item%2F1"
        )
        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.source_id, "archive item/1")
        self.assertEqual(record.title, "Public Domain Work")
        self.assertEqual(record.authors, ["Open Author"])
        self.assertEqual(record.rank, 2)
        self.assertEqual(
            [option.extension for option in record.downloads],
            ["epub", "pdf", "txt"],
        )
        self.assertEqual(record.downloads[0].expected_md5, "abc123")
        self.assertEqual(
            record.downloads[0].url,
            "https://archive.org/download/archive%20item%2F1/book.epub",
        )
        self.assertIn("Internet Archive 不保證版權狀態", record.license_text)
        self.assertIn("Public domain", record.license_text)

    def test_open_library_rejects_restricted_candidate(self):
        payloads = (
            {
                "metadata": {"access-restricted-item": "true"},
                "files": [{"name": "book.pdf", "format": "Text PDF"}],
            },
            {
                "metadata": {},
                "nodownload": True,
                "files": [{"name": "book.pdf", "format": "Text PDF"}],
            },
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                client = mock.Mock()
                client.get_json.return_value = payload
                record = ebooks.OpenLibraryProvider()._resolve_candidate(
                    0,
                    {"title": "Restricted", "first_publish_year": 2000},
                    "restricted-id",
                    date(1999, 1, 1),
                    date(2001, 12, 31),
                    client,
                )
                self.assertIsNone(record)

    def test_open_library_tries_later_public_ia_edition(self):
        client = mock.Mock()
        client.get_json.side_effect = [
            {
                "metadata": {"access-restricted-item": "true"},
                "files": [],
            },
            {
                "metadata": {"title": "Public copy"},
                "files": [
                    {"name": "public.epub", "format": "EPUB", "size": "50"}
                ],
            },
        ]
        record = ebooks.OpenLibraryProvider()._resolve_candidate(
            0,
            {"title": "Work", "first_publish_year": 2000},
            ["restricted-id", "public-id"],
            date(1999, 1, 1),
            date(2001, 12, 31),
            client,
        )
        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.source_id, "public-id")
        self.assertEqual(len(record.downloads), 1)


class DownloadValidationTests(unittest.TestCase):
    def test_validate_download_accepts_valid_pdf_epub_and_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf = root / "valid.pdf"
            pdf.write_bytes(b"%PDF-1.7\nminimal test payload")

            epub = root / "valid.epub"
            with zipfile.ZipFile(epub, "w") as archive:
                archive.writestr("mimetype", "application/epub+zip")
                archive.writestr("META-INF/container.xml", "<container />")

            text = root / "valid.txt"
            text.write_text("這是純文字電子書。", encoding="utf-8")

            for path, extension in ((pdf, "pdf"), (epub, "epub"), (text, "txt")):
                with self.subTest(extension=extension):
                    ebooks.validate_download(path, extension)

    def test_validate_download_rejects_mismatched_or_unsafe_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            invalid_pdf = root / "invalid.pdf"
            invalid_pdf.write_bytes(b"not a PDF")

            invalid_epub = root / "invalid.epub"
            with zipfile.ZipFile(invalid_epub, "w") as archive:
                archive.writestr("mimetype", "application/epub+zip")

            html_text = root / "html.txt"
            html_text.write_text("<!doctype html><html></html>", encoding="utf-8")

            binary_text = root / "binary.txt"
            binary_text.write_bytes(b"\x00" * 100)

            empty_text = root / "empty.txt"
            empty_text.write_bytes(b"")

            for path, extension in (
                (invalid_pdf, "pdf"),
                (invalid_epub, "epub"),
                (html_text, "txt"),
                (binary_text, "txt"),
                (empty_text, "txt"),
            ):
                with self.subTest(path=path.name):
                    with self.assertRaises(ebooks.ProviderError):
                        ebooks.validate_download(path, extension)


if __name__ == "__main__":
    unittest.main()
