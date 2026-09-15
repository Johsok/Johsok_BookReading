# -*- coding: utf-8 -*-
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_highlights import write_highlights, extract_highlights

payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
root = Path(__file__).resolve().parents[1]
for book_id, text in payload.items():
    if isinstance(text, list):
        h = extract_highlights("\n".join(str(item) for item in text))
    else:
        h = extract_highlights(text)
    if len(h) != 150:
        raise SystemExit(f'{book_id} count={len(h)}')
    print(json.dumps(write_highlights(root, book_id, h), ensure_ascii=False))
