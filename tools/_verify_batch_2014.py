# -*- coding: utf-8 -*-
from pathlib import Path
from findbook_writer import read_json

ROOT = Path(__file__).resolve().parents[1]
IDS = [
    "01_business_startup-20260818-08",
    "01_business_startup-20260818-09",
    "01_business_startup-20260818-10",
    "01_business_startup-20260818-11",
    "01_business_startup-20260818-12",
    "02_psychology_growth-20260818-08",
    "02_psychology_growth-20260818-09",
    "02_psychology_growth-20260818-10",
    "02_psychology_growth-20260818-11",
    "02_psychology_growth-20260818-12",
]


def main() -> None:
    manifest = read_json(ROOT / "data.json")
    books = manifest.get("books", [])
    print(f"totalBooks={manifest.get('totalBooks')} len={len(books)}")
    assert manifest.get("totalBooks") == len(books)
    ids = [book.get("id") for book in books]
    files = [book.get("file") for book in books]
    assert len(ids) == len(set(ids))
    assert len(files) == len(set(files))
    missing = [path for path in files if not (ROOT / path).exists()]
    assert not missing, missing[:5]
    extras = []
    for path in ROOT.glob("Books/**/*.json"):
        relative = path.relative_to(ROOT).as_posix()
        if path.name.startswith("_"):
            extras.append(relative)
            continue
        if relative not in files:
            extras.append(relative)
    for book_id in IDS:
        matches = [book for book in books if book.get("id") == book_id]
        assert len(matches) == 1
        index_book = matches[0]
        expected = f"Books/{index_book['categoryId']}/{book_id}.json"
        assert index_book.get("file") == expected
        book = read_json(ROOT / expected)
        for field in ("id", "categoryId", "title", "author"):
            assert index_book.get(field) == book.get(field), (book_id, field)
        highlights = book.get("chatgptHighlights") or []
        assert book.get("chatgptStatus") == "complete"
        assert book.get("highlightsSource") == "grok"
        assert book.get("workId") == "findbook-20260818-2014"
        assert len(highlights) == 150
        assert highlights[0].startswith("001、")
        assert highlights[-1].startswith("150、")
        print(f"ok\t{book_id}")
    print(f"underscore-or-unindexed={len(extras)}")
    for item in extras[:12]:
        print(f"extra\t{item}")
    print("batch-index-ok")


if __name__ == "__main__":
    main()
