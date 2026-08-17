# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

p = Path(__file__).with_name("_hl_273.py")
text = p.read_text(encoding="utf-8")
start = text.index("BODIES = [")
end = text.index("\n]\n", start)
ns: dict = {}
exec(text[start : end + 2], ns)
bodies = ns["BODIES"]
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
fixed = []
for body in bodies:
    body = body.replace(" overlapping ", "疊合")
    body = body.replace("一根 treillis 被當成蛇", "一段籬笆輪廓被當成蛇")
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(NATURAL):
        body = body[: len(match.group(1))] + "，" + body[len(match.group(1)) + 1 :]
    fixed.append(body)
drop = "因此透過幻象看真相，包括承認概念已經是一種合法的、但可修正的簡化。"
if drop in fixed:
    fixed.remove(drop)
elif len(fixed) > 150:
    fixed.pop()
assert len(fixed) == 150, len(fixed)
new_block = "BODIES = [\n" + "\n".join("    " + json.dumps(b, ensure_ascii=False) + "," for b in fixed) + "\n]"
p.write_text(text[:start] + new_block + text[end + 1 :], encoding="utf-8")
print("ok", len(fixed))
