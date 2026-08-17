# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parent
main = (root / "_build_hl_0610.py").read_text(encoding="utf-8")
rest = (root / "_hl_b09b10_snippet.py").read_text(encoding="utf-8")
footer = r'''

BOOKS = [
    ("02_psychology_growth-20260717-06", "情結", "河合隼雄", B06),
    ("02_psychology_growth-20260717-07", "生活中的心理學智慧", "韋志中", B07),
    ("02_psychology_growth-20260717-08", "偶爾出格：療愈自己的39種方式", "觀心實驗室", B08),
    ("02_psychology_growth-20260717-09", "心流與積極心理學", "米哈里·契克森米哈伊", B09),
    ("02_psychology_growth-20260717-10", "輕釋壓", "詹妮弗·L.泰茲", B10),
]


def main() -> None:
    out_dir = ROOT / "tools"
    for book_id, title, author, bodies in BOOKS:
        if len(bodies) != 150:
            raise SystemExit(f"{book_id} has {len(bodies)} lines")
        highlights = numbered(bodies)
        validate_highlights(book_id, highlights, title, author)
        path = out_dir / f".findbook_results_grok_{book_id}.json"
        path.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("ok", book_id)


if __name__ == "__main__":
    main()
'''
(root / "_build_hl_0610.py").write_text(main.rstrip() + "\n\n" + rest + footer, encoding="utf-8")
print("merged")
