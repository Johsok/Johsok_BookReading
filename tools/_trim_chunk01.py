# -*- coding: utf-8 -*-
import ast
import pathlib

REPLACES = {
    "口号": "口號",
    "危险": "危險",
    "不等于": "不等於",
    "撑不久": "撐不久",
    "自以为": "自以為",
    "Exhaust": "筋疲力盡",
}


def trim(path: str, n: int = 150) -> None:
    p = pathlib.Path(path)
    t = p.read_text(encoding="utf-8")
    start = t.index("BODIES = [")
    end = t.index("\n\nassert len")
    bodies = ast.literal_eval(t[start + len("BODIES = ") : end])
    fixed = []
    for b in bodies:
        for a, c in REPLACES.items():
            b = b.replace(a, c)
        fixed.append(b)
    bodies = fixed[:n]
    lines = ["BODIES = ["]
    for b in bodies:
        lines.append(f'    "{b}",')
    lines.append("]")
    new = t[:start] + "\n".join(lines) + t[end:]
    p.write_text(new, encoding="utf-8")
    print(path, "now", len(bodies))


trim("tools/_gen_chunk01_b64.py")
trim("tools/_gen_chunk01_b65.py")
