# -*- coding: utf-8 -*-
from pathlib import Path
from collections import Counter

src = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_08.txt")
dst = src
lines = src.read_text(encoding="utf-8").splitlines()

# Drop second duplicate-openings and extra lines to reach 150.
# 1-based indices to drop
drop = {
    9, 13, 14, 15, 16, 20, 27, 32, 36, 41, 42, 43, 48, 50, 51, 54, 58, 61, 64, 65,
    68, 69, 72, 74, 75, 81, 82, 84, 88, 102, 104, 106, 108, 110, 113,
    122, 124, 125, 127, 128, 129, 133, 134, 136, 137, 138, 139, 141,
    145, 146, 147, 149, 150, 152, 154, 155, 156, 158, 159, 160, 161, 162, 163,
    166, 168, 169, 172, 173, 174, 177, 178, 179, 180, 181, 183, 184, 185,
    186, 187, 188, 189, 191, 192, 193, 194, 201, 203, 204,
}

kept = [s for i, s in enumerate(lines, 1) if i not in drop]
used = {s[:2] for s in kept}
for i, s in enumerate(lines, 1):
    if i in drop and s[:2] not in used:
        kept.append(s)
        used.add(s[:2])
    if len(kept) >= 150:
        kept = kept[:150]
        break
if len(kept) < 150:
    raise SystemExit(f"only {len(kept)}")

# Fix simplified / wording
fixed = []
for s in kept:
    s = s.replace("加强", "加強")
    s = s.replace("腌菜", "醃菜")
    s = s.replace("自制", "自製")
    s = s.replace("蜂產肉毒芽孢可能存在蜂蜜康普茶", "蜂蜜康普茶可能含肉毒芽孢")
    fixed.append(s)

# Unique openings
c2 = Counter(s[:2] for s in fixed)
if any(v > 1 for v in c2.values()):
    dups = [k for k, v in c2.items() if v > 1]
    # retarget remaining dups
    seen = set()
    new = []
    alts = {
        "葉菜": "台菜含水量高於韓菜時搓鹽可較短但瀝水一定要徹底",
        "隔夜": "靜置隔夜可降低余氯仍要蓋好防塵",
        "酒精": "噴霧酒精後要揮發乾再接觸菌種殘酒會干擾發酵",
    }
    for s in fixed:
        o = s[:2]
        if o in seen:
            if o in alts:
                s = alts[o]
            else:
                raise SystemExit(f"unresolved dup {o} {s}")
        seen.add(s[:2])
        new.append(s)
    fixed = new

# If still not 150, trim or error
n = len(fixed)
rep = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_hl08_chk.txt")
c2 = Counter(s[:2] for s in fixed)
dups = [k for k, v in c2.items() if v > 1]
forb = ["本書", "作者指出", "本章", "這一章", "｜", "：", ":", "第一步", "第二步"]
iss = []
for i, s in enumerate(fixed, 1):
    for f in forb:
        if f in s:
            iss.append(f"{i}:{f}")
    if "第" in s and "步" in s:
        iss.append(f"{i}:步")

if n != 150 or dups or iss:
    extra = [s[:2] for s in fixed]
    rep.write_text(
        f"count={n}\ndups={dups}\nissues={iss}\n" + "\n".join(f"{i:03}|{s[:2]}|{s}" for i, s in enumerate(fixed, 1)),
        encoding="utf-8",
    )
else:
    dst.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    text = dst.read_text(encoding="utf-8")
    lines2 = text.splitlines()
    rep.write_text(
        f"OK count={len(lines2)} unique={len(set(lines2))} unique_open2={len(set(s[:2] for s in lines2))} nl={text.endswith(chr(10))}",
        encoding="utf-8",
    )

print("done", n, "dups", dups, "iss", iss)
