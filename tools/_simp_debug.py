# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location("g", Path(__file__).with_name("_gen_91_95.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
out = []
for book in g.BOOKS:
    bodies = [b.strip() for b in book["bodies"] if b.strip()]
    for i, body in enumerate(bodies, 1):
        hit = [ch for ch in body if ch in g.SIMP]
        if hit:
            out.append(f"{book['id']}\t{i}\t{''.join(hit)}\t{body}")
            break
Path(__file__).with_name("_simp_hits.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
