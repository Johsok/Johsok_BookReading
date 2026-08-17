# -*- coding: utf-8 -*-
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import zhconv

TOOLS = Path(__file__).resolve().parent
out = []


def show(path: Path) -> None:
    spec = spec_from_file_location(path.stem, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    out.append(f"== {path.name} n={len(mod.BODIES)}")
    for i, b in enumerate(mod.BODIES, 1):
        trad = zhconv.convert(b, "zh-hant")
        if trad != b:
            pairs = []
            for a, c in zip(b, trad):
                if a != c:
                    pairs.append(f"{a}->{c}")
            extra = ""
            if len(trad) != len(b):
                extra = f" len {len(b)}->{len(trad)}"
            out.append(f"{i:03d} " + " ".join(pairs) + extra)
            out.append("  " + b)
            out.append("  " + trad)


show(TOOLS / "_hl_redo_07_other-20260716-53.py")
show(TOOLS / "_hl_redo_07_other-20260716-54.py")
(TOOLS / "_tmp_zhconv_53_54_out.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", len(out), "lines")
