# -*- coding: utf-8 -*-
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

specs = [
    ("07_other-20260716-57", "共同知識：揭開人類群體合作的邏輯，剖析經濟、政治與日常生活的隱藏規則", "史迪芬．平克"),
    ("07_other-20260716-58", "一顆豆腐心，寫下了花園傳奇：從醫護送養到生命教育，初衷不改二十年", "花園／Rose（晴夜）"),
]
root = Path(__file__).resolve().parent
for book_id, title, author in specs:
    path = root / f".findbook_results_grok_{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    hl = validate_highlights(book_id, data["highlights"], title, author)
    bodies = [re.sub(r"^\d{3}、", "", x) for x in hl]
    print(book_id, "count", len(hl), "id", data["id"])
    print("001", hl[0])
    print("150", hl[-1])
    print("starts", sum(b.startswith(("共同知識", "浪浪", "愛心")) for b in bodies))
    print("names", {t: sum(t in b for b in bodies) for t in ("平克", "花園", "Rose", "晴夜")})
