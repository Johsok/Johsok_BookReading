# -*- coding: utf-8 -*-
"""Diversify templated openings in Adler results JSON."""
import json
from collections import Counter
from pathlib import Path

p = Path(
    r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools"
    r"\.findbook_results_grok_02_psychology_growth-20260709-07.json"
)
d = json.loads(p.read_text(encoding="utf-8"))
hs = d["highlights"]

replacements = {
    132: "操控他人情緒的衝動升起時，提醒自己那從來不是我的課題範圍",
    133: "害怕不被喜歡時問自己是否正在用討好購買虛假的自由感",
    134: "陷入自卑漩渦時先分辨那是動力還是讓人停滯的藉口說法",
    135: "想稱讚或貶低之際改成看見努力與可能性的溫暖鼓勵話語",
    136: "翻舊帳的時候把目光拉回此刻我可以選擇什麼不同做法路徑",
    137: "嫉妒升起時練習把對方當同伴而非競爭跑道上的敵人對手",
    139: "關係緊繃時先釐清界線再決定要靠近或先退一步喘息一下",
    141: "擁抱自由就得接受不被理解與被拒絕的真實風險與必要代價",
    142: "投入貢獻就會在關係裡逐漸長出踏實而溫暖的歸屬感受來",
    143: "把握此刻行動就不再把人生抵押給遙遠的有一天幻想故事",
}

for i, body in replacements.items():
    assert 25 <= len(body) <= 70, (i, len(body), body)
    hs[i - 1] = f"{i:03d}、{body}"

# validate
assert len(hs) == 150
assert len(set(hs)) == 150
opens3 = [h.split("、", 1)[1][:3] for h in hs]
dups = {k: v for k, v in Counter(opens3).items() if v > 1}
if dups:
    raise SystemExit(f"dup3 {dups}")
for i, h in enumerate(hs, 1):
    assert h.startswith(f"{i:03d}、")
    body = h.split("、", 1)[1]
    assert 25 <= len(body) <= 70, (i, len(body), body)
    for bad in ("本書", "作者指出", "本章", "｜", "面第", "岸見", "古賀"):
        assert bad not in body

d["highlights"] = hs
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lens = [len(h.split("、", 1)[1]) for h in hs]
print(f"OK 150 {p}")
print(f"min={min(lens)} max={max(lens)}")
