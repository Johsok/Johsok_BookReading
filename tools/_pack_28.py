import json, re
from pathlib import Path
from collections import Counter
BOOK_ID = "01_business_startup-20260724-28"
TITLE = "AI發展下的人類新生態：就業衝擊、倫理困境、環境壓力、資本運作"
AUTHOR = "李國祥"
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
raw = Path(r"tools/_bodies_28.txt").read_text(encoding="utf-8").splitlines()
bodies = [ln.strip() for ln in raw if ln.strip()]
fixed = []
for b in bodies:
    b = b.replace("合規 Mor 通過", "合規通過").replace("出让", "讓")
    m = re.match(r"^([^：:]{1,12})[：:](.*)$", b)
    if m and not m.group(1).endswith(NATURAL):
        b = m.group(1) + "，" + m.group(2)
    fixed.append(b)
print(len(fixed), len(set(fixed)))
assert len(fixed) == 150 and len(set(fixed)) == 150
short = [i for i,b in enumerate(fixed,1) if (m:=re.match(r"^([^：:]{1,12})[：:]", b)) and not m.group(1).endswith(NATURAL)]
assert len(short) < 3, short
starts = Counter(b[:18] for b in fixed)
assert starts.most_common(1)[0][1] < 4
assert sum(TITLE in b for b in fixed) < 2 and sum(AUTHOR in b for b in fixed) < 2
hl = [f"{i:03d}、{b}" for i,b in enumerate(fixed,1)]
Path(f"tools/.findbook_results_grok_{BOOK_ID}.json").write_text(json.dumps({"id": BOOK_ID, "highlights": hl}, ensure_ascii=False, indent=2), encoding="utf-8")
print("written results")
