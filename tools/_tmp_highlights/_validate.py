import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from findbook_writer import validate_highlights, read_json

root = Path(__file__).resolve().parents[2]
tmp = Path(__file__).resolve().parent
ids = [
    "03_natural_science-20260709-01",
    "03_natural_science-20260709-02",
    "03_natural_science-20260709-03",
    "03_natural_science-20260709-04",
    "03_natural_science-20260709-05",
    "03_natural_science-20260709-06",
    "03_natural_science-20260709-07",
    "03_natural_science-20260709-08",
    "03_natural_science-20260710-09",
    "03_natural_science-20260710-10",
    "03_natural_science-20260710-11",
]
for book_id in ids:
    result = read_json(tmp / f"{book_id}.json")
    book = read_json(root / "Books" / "03_natural_science" / f"{book_id}.json")
    highlights = result.get("highlights")
    count = len(highlights) if isinstance(highlights, list) else "NA"
    try:
        validate_highlights(
            book_id,
            highlights,
            book.get("title", ""),
            book.get("author", ""),
        )
        print(f"OK\t{book_id}\t{count}")
    except Exception as e:
        print(f"FAIL\t{book_id}\t{count}\t{e}")
