# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\verify_23_24.txt")
parts = []
for name in ["07_other-20260717-23.json", "07_other-20260717-24.json"]:
    p = root / name
    raw = p.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    hs = data["chatgptHighlights"]
    bodies = [x.split("、", 1)[1] for x in hs]
    numbered = all(x.startswith(f"{i:03d}、") for i, x in enumerate(hs, 1))
    parts.append(name)
    parts.append(
        "count=%s unique=%s numbered=%s bom=%s end_nl=%s"
        % (
            len(hs),
            len(set(bodies)),
            numbered,
            raw.startswith(b"\xef\xbb\xbf"),
            raw.endswith(b"\n"),
        )
    )
    parts.append("status=%s source=%s" % (data["chatgptStatus"], data["highlightsSource"]))
    parts.append("captured=%s updated=%s" % (data["highlightsCapturedAt"], data["updatedAt"]))
    parts.append("keys=%s" % list(data.keys()))
    parts.append("title=%s author=%s workId=%s" % (data["title"], data["author"], data.get("workId")))
    parts.append("FIRST " + hs[0])
    parts.append("LAST " + hs[-1])
    parts.append("")
out.write_text("\n".join(parts), encoding="utf-8")
