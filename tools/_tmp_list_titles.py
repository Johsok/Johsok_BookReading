# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = [
    "01_business_startup-20160830-36",
    "01_business_startup-20160830-38",
    "01_business_startup-20160830-39",
    "03_natural_science-20160830-40",
    "04_healthcare-20160830-40",
]


def main() -> None:
    for book_id in IDS:
        category = book_id.rsplit("-", 2)[0]
        path = ROOT / "Books" / category / f"{book_id}.json"
        book = json.loads(path.read_text(encoding="utf-8"))
        highlights = book["chatgptHighlights"]
        last = highlights[149]
        print(book_id, len(highlights), book["chatgptStatus"])
        print("  150", last)
        print("  dirty", last.endswith("}") or last.endswith('"') or "\\u" in last)

    book_path = ROOT / "Books/06_computer_info/06_computer_info-20260716-01.json"
    book = json.loads(book_path.read_text(encoding="utf-8"))
    print("06 file", book.get("categoryId"), book.get("id"))
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    for item in manifest["books"]:
        if item.get("id") == "06_computer_info-20260716-01":
            print("06 idx", item.get("categoryId"))
            break
    print("total", manifest.get("totalBooks"), len(manifest["books"]))


if __name__ == "__main__":
    main()
