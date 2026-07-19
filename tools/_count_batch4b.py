# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("_gen_batch4_highlights.py")
# Load by exec of assignments only
ns = {"__file__": str(path)}
code = path.read_text(encoding="utf-8")
# Strip asserts and main
parts = code.split("assert len(BOOK1)")[0]
exec(parts, ns)
for name in ["BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5"]:
    print(name, len(ns[name]))
