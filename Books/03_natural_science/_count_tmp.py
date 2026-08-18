# -*- coding: utf-8 -*-
import pathlib, re
p = pathlib.Path("_write_hl_135_137.py")
text = p.read_text(encoding="utf-8")
# extract first items list only
m = re.search(r'"items": \[(.*?)\]\s*,\s*\}', text, re.S)
# simpler exec
ns = {}
try:
    exec(compile(text, "x", "exec"), ns)
    print("exec ok", list(ns.get("BOOKS", {})))
except Exception as e:
    print("exec fail", type(e), e)
    # count quoted lines in items
lines = text.splitlines()
items = [ln for ln in lines if ln.strip().startswith('"') and ln.strip().endswith('",') or ln.strip().endswith('"')]
print("quoted-ish", len(items))
