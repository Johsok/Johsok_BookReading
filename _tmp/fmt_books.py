# -*- coding: utf-8 -*-
from pathlib import Path
from importlib.machinery import SourceFileLoader

BOOKS = SourceFileLoader("o", str(Path(__file__).with_name("BOOKS_b05_b06_b07_out.py"))).load_module().BOOKS
lines = ["# -*- coding: utf-8 -*-", "BOOKS = {"]
for k in ("b05", "b06", "b07"):
    lines.append(f'    "{k}": [')
    for s in BOOKS[k]:
        lines.append("        " + repr(s) + ",")
    lines.append("    ],")
lines.append("}")
Path(__file__).with_name("BOOKS_b05_b06_b07_fmt.py").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("ok")
