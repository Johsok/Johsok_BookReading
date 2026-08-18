import json
import re
import unicodedata
from pathlib import Path

PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)


def nk(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT_RE.sub("", value)


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "data.json").read_text(encoding="utf-8-sig"))
out = root / "tools" / "_tmp_existing_01_02.txt"
lines = []
for cid in ("01_business_startup", "02_psychology_growth"):
    books = [book for book in manifest["books"] if book.get("categoryId") == cid]
    lines.append(f"=== {cid} count={len(books)} ===")
    for book in books:
        lines.append(f"{book['id']}\t{book['title']}\t{book['author']}\t{nk(book['title'], book['author'])}")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {out} lines={len(lines)}")
