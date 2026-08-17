# -*- coding: utf-8 -*-
"""Fix colons in gen_27 and rewrite results."""
from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

src = Path("tools/_gen_27.py")
text = src.read_text(encoding="utf-8")
mod = ast.parse(text)
bodies = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for tg in node.targets:
            if isinstance(tg, ast.Name) and tg.id == "BODIES":
                bodies = list(ast.literal_eval(node.value))

natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
fixed = []
for b in bodies:
    m = re.match(r"^([^：:]{1,12})[：:](.*)$", b)
    if m and not m.group(1).endswith(natural):
        b = m.group(1) + "，" + m.group(2).lstrip()
    # also split mid-sentence short labels carefully already handled
    fixed.append(b)

# manual known fixes if still colon-tagged
replacements = {
    "攝影般的記憶片段提醒：情緒也有色溫與層次。": "攝影般的記憶片段提醒情緒也有色溫與層次。",
    "回到舊島才明白：逃離不是消失，共處才是功課。": "回到舊島才明白逃離不是消失，共處才是功課。",
    "自我照顧清單可以很具體：喝水、睡覺、拒絕加班情緒勞動。": "自我照顧清單可以很具體，包括喝水睡覺與拒絕情緒加班。",
    "失衡時身體會抗議：失眠、暴食、無緣由的怒。": "失衡時身體會抗議，出現失眠暴食或無緣由的怒。",
    "堅強的重新定義是：我會求助、會休息、會哭。": "堅強的重新定義是我會求助、會休息、也會哭。",
    "重建信任從對自己誠實開始：我到底想要什麼。": "重建信任從對自己誠實開始，先問我到底想要什麼。",
    "過度懂事的警訊是：還沒收斂就先道歉、先承擔。": "過度懂事的警訊是還沒收斂就先道歉、先承擔。",
    "先道歉前先問：這真的是我的錯，還是習慣性攬責。": "先道歉前先問這真的是我的錯，還是習慣性攬責。",
    "對自己溫柔的句子可以很短：你已經很努力了。": "對自己溫柔的句子可以很短，例如你已經很努力了。",
}
fixed = [replacements.get(b, b) for b in fixed]

# re-check short colon
sc = []
for i, b in enumerate(fixed, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", b)
    if m and not m.group(1).endswith(natural):
        sc.append((i, b))
print("short_colon", sc)
print("count", len(fixed), "unique", len(set(fixed)))
starts = Counter(b[:18] for b in fixed)
print("top starts", starts.most_common(3))

book_id = "02_psychology_growth-20260724-27"
highlights = [f"{i:03d}、{b}" for i, b in enumerate(fixed, 1)]
out = Path(f"tools/.findbook_results_grok_{book_id}.json")
out.write_text(
    json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print("wrote", out)
