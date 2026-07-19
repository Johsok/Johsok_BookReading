# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("_gen_grok_151_to_154.py")
spec = importlib.util.spec_from_file_location("gen151", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for book_id, title, author, bodies in mod.BOOKS:
    print(book_id, len(bodies))
