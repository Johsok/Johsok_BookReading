import ast
from pathlib import Path
import re

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
mod = ast.parse(Path("tools/_gen_pg_181_185.py").read_text(encoding="utf-8"))
out = Path("tools/_hl_prefix_check.txt")
lines = []
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id.startswith("BOOK"):
                vals = ast.literal_eval(node.value)
                lines.append(f"==== {t.id} {len(vals)}")
                short = []
                for i, b in enumerate(vals, 1):
                    m = re.match(r"^([^：:]{1,12})[：:]", b)
                    if m and not m.group(1).endswith(NATURAL):
                        short.append(f"{i:03d} {m.group(1)}|{b[:24]}")
                lines.append(f"short_colon {len(short)}")
                lines.extend(short)
                # forbidden
                for i, b in enumerate(vals, 1):
                    for p in ("本書", "作者指出", "本章", "這一章"):
                        if p in b:
                            lines.append(f"forbidden {i} {p}")
                    if "｜" in b:
                        lines.append(f"bar {i}")
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
