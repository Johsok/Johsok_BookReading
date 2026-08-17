import json
from pathlib import Path

a = json.loads(Path("Books/02_psychology_growth/02_psychology_growth-20260716-147.json").read_text(encoding="utf-8-sig"))
b = json.loads(Path("tools/.findbook_results_grok_02_psychology_growth-20260716-226.json").read_text(encoding="utf-8"))
old = [x.split("、", 1)[1] for x in a["chatgptHighlights"]]
new = [x.split("、", 1)[1] for x in b["highlights"]]
old_set = set(old)
print("exact", sum(x in old_set for x in new))
# 20-char substring overlap
hits = []
for n in new:
    for o in old:
        if len(n) >= 16 and n[:16] in o:
            hits.append((n[:20], o[:20]))
            break
print("prefix16_in_147", len(hits))
for h in hits[:10]:
    print(h)
