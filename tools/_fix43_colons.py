# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
path = Path("tools/_batch14_bodies_43.json")
bodies = json.loads(path.read_text(encoding="utf-8"))

# Replace problematic short-colon openings with natural prose
replacements = {
    37: "學習止語很重要，不該說的機密、閒話與情緒宣洩，往往比多說更難。",
    66: "職業生涯長跑需要信仰感，要想清楚為何而做，而不只為下一張業績表。",
    79: "工商與人生的修養相通，應減少怨尤、增加承擔、看遠一步。",
    131: "學習止損很關鍵，錯的專案早停比加碼證明自己正確更需要勇氣。",
    143: "把顧客當老師、把員工當夥伴、把對手當鏡子，工商路會走得比較穩。",
}

for idx, text in replacements.items():
    print(idx, "OLD:", bodies[idx - 1])
    bodies[idx - 1] = text
    print(idx, "NEW:", text)

# verify
short = []
for i, b in enumerate(bodies, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", b)
    if m and not m.group(1).endswith(NATURAL):
        short.append((i, m.group(1), b))
print("remaining short-colon", len(short), short)

assert len(bodies) == 150
assert len(set(bodies)) == 150
path.write_text(json.dumps(bodies, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("fixed 43")
