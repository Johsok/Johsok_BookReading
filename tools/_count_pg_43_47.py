# -*- coding: utf-8 -*-
from pathlib import Path

text = Path(__file__).with_name("_gen_pg_43_47.py").read_text(encoding="utf-8")
ns = {"__file__": str(Path(__file__).with_name("_gen_pg_43_47.py"))}
# Execute only the list definitions by skipping imports that need ROOT
start = text.find("B43 = [")
end = text.find("\nBOOKS =")
exec(text[start:end], ns)
for name in ["B43", "B44", "B45", "B46", "B47"]:
    print(name, len(ns[name]))
