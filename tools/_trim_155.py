# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

p = Path(__file__).with_name("_gen_155.py")
text = p.read_text(encoding="utf-8")
m = re.search(r"HIGHLIGHTS = \[(.*?)\]\n", text, re.S)
assert m
items = re.findall(r'"([^"]+)"', m.group(1))
print("count", len(items))
remove = {
    "匿名捐贈減少虛榮動機，卻也可能削弱示範效應",
    "家庭分工也可看成合作結構，公平感影響長期穩定",
    "育兒投入常有外部性，政策補貼能改變家庭決策",
}
kept = [h for h in items if h not in remove]
print("kept", len(kept))
assert len(kept) == 150, len(kept)
assert len(set(kept)) == 150
assert Counter(h[:18] for h in kept).most_common(1)[0][1] < 4
new_list = "HIGHLIGHTS = [\n" + ",\n".join(f'    "{h}"' for h in kept) + ",\n]\n"
text2 = re.sub(r"HIGHLIGHTS = \[.*?\]\n", new_list, text, count=1, flags=re.S)
p.write_text(text2, encoding="utf-8")
print("updated")
