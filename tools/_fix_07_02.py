# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).with_name("_bodies_07_other-20260719-02.txt")
text = p.read_text(encoding="utf-8")
text = text.replace("稳住", "穩住").replace("叠在", "疊在").replace("反复", "反覆")
lines = [x.strip() for x in text.splitlines() if x.strip()]
extra = [
    "每一次城破與受禪，都在重估武人與士族之間的契約內容。",
    "契約若只能靠恐嚇維持，下一次背叛只是時間問題。",
    "江南物資網絡被打斷後，奢侈消費文化也失去物質基礎。",
    "失去物質基礎的繁華敘事，很難再支撐舊有的政治自信。",
    "北周後來能吞齊，部分原因正是更早完成組織與紀律改造。",
    "改造需要時間，而對手內鬥恰好把時間送給了對方。",
    "把兵劫當成結構警訊而非傳奇故事，讀史才有現實意義。",
    "關中雖貧，卻因壓力集中而更快形成高效戰爭體制。",
    "河北雖富，卻因利益分散而更難形成穩定政治中心。",
    "富與強若不能轉成制度，最後仍會在內耗中流失。",
    "南朝水鄉地形可遲滯騎兵，卻無法取代清楚的指揮鏈。",
    "指揮鏈斷裂時，再險的長江也只是地理風景。",
    "北齊名將不少，卻常在宮廷恐懼中無法發揮全力。",
    "將領寒心之後，戰場猶豫比兵器短缺更致命。",
]
seen = set(lines)
for e in extra:
    if len(lines) >= 150:
        break
    if e not in seen:
        lines.append(e)
        seen.add(e)
if len(lines) != 150:
    raise SystemExit(f"count={len(lines)}")
p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("ok", len(lines))
