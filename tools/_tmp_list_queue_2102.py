# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ids = [
    "01_business_startup-20260818-13",
    "01_business_startup-20260818-14",
    "01_business_startup-20260818-15",
    "01_business_startup-20260818-16",
    "01_business_startup-20260818-17",
    "02_psychology_growth-20260818-13",
    "02_psychology_growth-20260818-14",
    "02_psychology_growth-20260818-15",
    "02_psychology_growth-20260818-16",
    "02_psychology_growth-20260818-17",
    "03_natural_science-20260818-03",
    "03_natural_science-20260818-04",
    "03_natural_science-20260818-05",
    "03_natural_science-20260818-06",
    "03_natural_science-20260818-07",
]
rows = []
for book_id in ids:
    category = "_".join(book_id.split("-")[:3]) if book_id.startswith("03") else "_".join(book_id.split("-")[:2])
    # 01_business_startup, 02_psychology_growth, 03_natural_science
    if book_id.startswith("01_"):
        category = "01_business_startup"
    elif book_id.startswith("02_"):
        category = "02_psychology_growth"
    else:
        category = "03_natural_science"
    path = root / "Books" / category / f"{book_id}.json"
    book = json.loads(path.read_text(encoding="utf-8"))
    rows.append(
        {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "categoryId": book["categoryId"],
            "file": f"Books/{category}/{book_id}.json",
            "status": book.get("chatgptStatus"),
        }
    )
out = root / "tools" / ".findbook_queue_20260818_2102.json"
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"queued={len(rows)}")
