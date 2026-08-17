# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from findbook_writer import validate_highlights

p = Path(__file__).resolve().parent / "04_healthcare-20260716-16.json"
d = json.loads(p.read_text(encoding="utf-8"))
validate_highlights(d["id"], d["highlights"], "疾病的隱喻 (二手書)", "蘇珊．桑塔格")
assert list(d.keys()) == ["id", "highlights"]
assert d["id"] == "04_healthcare-20260716-16"
assert len(d["highlights"]) == 150
out = Path(__file__).resolve().parent / "_qa16.txt"
out.write_text(
    f"ok count={len(d['highlights'])}\n{d['highlights'][0]}\n{d['highlights'][-1]}\n",
    encoding="utf-8",
)
print("qa_ok")
