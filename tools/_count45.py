# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("_gen_batch45.py")
spec = importlib.util.spec_from_file_location("gen45", path)
mod = importlib.util.module_from_spec(spec)
# avoid running main
source = path.read_text(encoding="utf-8")
source = source.split("def main")[0]
ns = {"__file__": str(path)}
exec(compile(source, str(path), "exec"), ns)
book = ns["BOOK41"]
print(len(book))
print("LAST:", book[-1])
