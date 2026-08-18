from pathlib import Path
from collections import Counter

p = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_08.txt")
raw = p.read_bytes()
text = raw.decode("utf-8")
lines = text.splitlines()
keys = ["優格", "泡菜", "味噌", "麴", "納豆", "康普", "酸種", "醋", "鹽度", "霉", "甘酒", "福菜", "豆腐乳"]
hits = {k: sum(k in s for s in lines) for k in keys}
forb = ["本書", "作者指出", "本章", "這一章", "｜", "：", ":"]
iss = [(i, f) for i, s in enumerate(lines, 1) for f in forb if f in s]
c2 = Counter(s[:2] for s in lines)
d2 = [k for k, v in c2.items() if v > 1]
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_hl08_chk.txt")
out.write_text(
    "\n".join(
        [
            f"count={len(lines)}",
            f"unique={len(set(lines))}",
            f"open2={len(c2)} dups={d2}",
            f"bom={raw[:3] == bytes((0xEF, 0xBB, 0xBF))}",
            f"nl={text.endswith(chr(10))}",
            f"issues={iss}",
            f"hits={hits}",
        ]
    ),
    encoding="utf-8",
)
print(out.read_text(encoding="utf-8"))
