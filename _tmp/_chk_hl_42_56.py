# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

base = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\06_computer_info")
banned = ["｜", "本書", "作者指出", "本章", "這一章", "實作面", "決策面", "復盤面"]
template_tails = [
    "先定義服務責任",
    "要明確規定輸入、輸出和錯誤",
    "宜分離介面與核心功能",
    "需設定逾時與重試",
    "要包含正常、邊界與惡意輸入",
    "應採最小權限和資料最小化",
    "不能只看回應速度",
    "實作前應核對",
    "要保留結構化日誌",
    "建立可演進架構",
    "先定義使用者、用途、輸出格式",
    "先定義任務問題、輸入格式",
]
issues = []
for n in range(42, 57):
    p = base / f"06_computer_info-20260716-{n:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hs = d.get("chatgptHighlights", [])
    bodies = []
    num_ok = True
    ban_hits = []
    tpl_hits = 0
    starts = []
    for i, h in enumerate(hs, 1):
        if not str(h).startswith(f"{i:03d}、"):
            num_ok = False
        body = h.split("、", 1)[1] if "、" in h else h
        bodies.append(body)
        starts.append(body[:6])
        for b in banned:
            if b in h:
                ban_hits.append((i, b))
        for t in template_tails:
            if t in h:
                tpl_hits += 1
    dup = len(bodies) - len(set(bodies))
    start_common = Counter(starts).most_common(3)
    src = d.get("highlightsSource")
    status = d.get("chatgptStatus")
    updated = d.get("updatedAt")
    flag = ""
    if len(hs) != 150 or (not num_ok) or dup or tpl_hits or ban_hits or src != "grok":
        flag = " ISSUE"
        issues.append(n)
    print(
        f"{n:02d} len={len(hs)} status={status} src={src} upd={updated} "
        f"ban={len(ban_hits)} tpl={tpl_hits} dup={dup} num_ok={num_ok} "
        f"starts={start_common}{flag}"
    )
    if ban_hits:
        print("  banned", ban_hits[:8])
print("ISSUES", issues)
