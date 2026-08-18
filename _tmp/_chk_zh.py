# -*- coding: utf-8 -*-
import ast
import collections
import re
from pathlib import Path

src = Path(__file__).with_name("_gen_book41_42.py").read_text(encoding="utf-8")
tree = ast.parse(src)
lists = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ("BOOK41", "BOOK42"):
            lists[node.targets[0].id] = ast.literal_eval(node.value)

simp_map = "后发会体里国对与从于产众点当么这为来时样说过还没开关见让条龙车门儿"
# too crude. check common simplified
simp = re.compile(r"[后发会体国对与从于产众点当这为来时说过还没开关见让条车门干发]")

cjk = re.compile(r"[\u4e00-\u9fff]")
for name, arr in lists.items():
    print("----", name)
    starts = collections.Counter("".join(cjk.findall(s)[:2]) for s in arr)
    print("top2", starts.most_common(15))
    starts4 = collections.Counter("".join(cjk.findall(s)[:4]) for s in arr)
    print("top4>=3", [(k, v) for k, v in starts4.items() if v >= 3])
    for i, s in enumerate(arr, 1):
        if "：" in s or ":" in s or "｜" in s or "|" in s:
            print("colon", i, s)
        for w in ("本書", "作者", "本章", "金成花", "權秀珍", "平松", "氣候變遷", "未來已來", "不可思議"):
            if w in s:
                print("word", w, i, s)
        if re.search(r"[A-Za-z]", s):
            print("latin", i, s)
        # common simplified
        for ch in "后发会体国对与从于产这为来时说还开关见车门":
            if ch in s and ch not in "開會體國對與從於產這為來時說還開關見車門":
                pass
        bad = []
        repl = {
            "后": "後", "发": "發", "会": "會", "体": "體", "国": "國", "对": "對",
            "与": "與", "从": "從", "于": "於", "产": "產", "这": "這", "为": "為",
            "来": "來", "时": "時", "说": "說", "还": "還", "开": "開", "关": "關",
            "见": "見", "车": "車", "门": "門", "个": "個", "们": "們", "过": "過",
            "让": "讓", "种": "種", "无": "無", "电": "電", "气": "氣",
        }
        for a, b in repl.items():
            if a in s:
                bad.append(a)
        if bad:
            print("simp?", i, bad, s)
