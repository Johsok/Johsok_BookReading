# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

p = Path(__file__).with_name("_batch47_bodies.py")
spec = importlib.util.spec_from_file_location("b", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for name in ["H21", "H22", "H23", "H24", "H25"]:
    H = getattr(m, name)
    for i, b in enumerate(H, 1):
        if re.search(r"[A-Za-z]{3,}", b):
            print(f"{name}:{i}:ENG:{b}")
        if re.search(r"[复护证样坛们为这说时国长经]", b):
            # weak check; print candidates with common simplified
            for ch in "复护证坛们长经":
                if ch in b and ch not in "經驗經絡經歷已經長期長者經常經營":
                    pass
        for bad in ("复评", "护肝", "电击", "辨证", "thrush", "entrapment", "比较", "何时", "当做", "内部", "生长", "减少", "为体"):
            if bad in b:
                print(f"{name}:{i}:BAD:{bad}:{b}")
