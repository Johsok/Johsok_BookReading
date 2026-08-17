# -*- coding: utf-8 -*-
from pathlib import Path
import zhconv

out = []
for path in [
    "tools/_hl_redo_07_other-20260716-41.py",
    "tools/_hl_redo_07_other-20260716-42.py",
]:
    text = Path(path).read_text(encoding="utf-8")
    start = text.index("BODIES = [")
    end = text.index("\ndef main")
    ns = {}
    exec(text[start:end], ns)
    bodies = ns["BODIES"]
    n = 0
    for i, body in enumerate(bodies, 1):
        trad = zhconv.convert(body, "zh-hant")
        if trad != body:
            diffs = [f"{a}->{b}" for a, b in zip(body, trad) if a != b]
            extra = ""
            if len(trad) != len(body):
                extra = f" len {len(body)}->{len(trad)}"
            out.append(f"{path} {i:03d} {' | '.join(diffs)}{extra}")
            out.append("  " + body)
            n += 1
    out.append(f"{path} simp_diffs={n} count={len(bodies)}")
Path("tools/_zh_check.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok", len(out))
