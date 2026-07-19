# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

q = json.loads(Path("tools/.findbook_grok_queue_findbook-20260719-220407.json").read_text(encoding="utf-8"))
print("total", len(q))
print(dict(Counter(b["categoryId"] for b in q)))
for i, b in enumerate(q):
    print(f"{i:02d}\t{b['id']}\t{b['title']}")
