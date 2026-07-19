# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).with_name("_gen_186_190.py")
text = path.read_text(encoding="utf-8")
repls = {
    "'局部最優是飛輪的慢性病'": "'局部最優化會慢慢侵蝕整圈飛輪的動量'",
    "'減法是加速的一部分'": "'勇敢做減法，往往比硬推更能真正加速'",
    "'清晰本身可以很美'": "'清晰的層級與節奏本身就可以構成美感'",
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f"missing: {old}")
    text = text.replace(old, new)
    print("fixed", old)
path.write_text(text, encoding="utf-8")
