# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("_gen_chunk20_highlights.py")
spec = importlib.util.spec_from_file_location("g", p)
m = importlib.util.module_from_spec(spec)
# avoid running main
src = p.read_text(encoding="utf-8")
src = src.replace('if __name__ == "__main__":\n    main()\n', "")
ns = {"__name__": "g", "__file__": str(p)}
exec(compile(src, str(p), "exec"), ns)
for k, v in ns["BOOKS"].items():
    print(k[-3:], len(v))
