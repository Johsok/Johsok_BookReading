# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "gen", Path(__file__).with_name("_gen_pg_196_200.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in ("B196", "B197", "B198", "B199", "B200"):
    bodies = getattr(mod, name)
    print(name, len(bodies), "unique", len(set(bodies)))
