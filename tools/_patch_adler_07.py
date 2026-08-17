# -*- coding: utf-8 -*-
"""Patch short highlight bodies then regenerate results JSON."""
import importlib.util
import pathlib
from collections import Counter

path = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools\_gen_adler_07.py")
spec = importlib.util.spec_from_file_location("g", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fixes = {
    67: "水平關係要求你放下我比較懂那種高高在上的優越姿態態度",
    87: "活在如果當時的假設裡，會偷走你對現在的寶貴注意力焦點",
    95: "尊重意味著承認對方有權用自己的方式處理自己整段人生",
    100: "拒絕並不等於傷害，長期偽裝同意才真正腐蝕彼此間信任",
    105: "屬於某個地方需要先願意為那裡做一點實際而可見的小事",
    109: "把價值綁在成績上，情緒就會隨分數劇烈起伏難以安穩下來",
    110: "價值若來自我對誰有幫助，就較不受單一評價左右來回搖擺",
    113: "把力氣從證明自己受害轉向選擇下一步，人生就會開始轉向",
    114: "勇氣與不安可以並存，帶著發抖的手仍然把該做的事情做出去",
    119: "歸屬共同體要求勇氣：既獨立又敢對世界真正敞開自己胸懷",
    121: "對手不是別人，而是昨日那個比較猶豫不決的自己內心聲音",
    122: "焦點從別人怎麼看我轉到我現在能貢獻什麼這一點上面去",
    127: "強大不是壓過別人，而是能承擔自己做出的每一個真實選擇",
    134: "每當陷入自卑漩渦先分辨那是動力還是讓人停滯的藉口說法",
    136: "每當翻舊帳時把目光拉回此刻我可以選擇什麼不同做法路徑",
    137: "每當嫉妒升起練習把對方當同伴而非競爭跑道上的敵人對手",
    138: "想證明自己比較優越時檢查背後是否藏著未消化的自卑情緒",
    139: "每當關係緊繃先釐清界線再決定要靠近或先退一步喘息一下",
    141: "選擇自由就得接受不被理解與被拒絕的真實風險與必要代價",
    142: "選擇貢獻就會在關係裡逐漸長出踏實而溫暖的歸屬感受來",
    143: "選擇此刻行動就不再把人生抵押給遙遠的有一天幻想故事",
    145: "哲人反覆強調世界其實簡單，難的是願意鼓起勇氣好好去過",
    146: "更新生活方式像更換過時的地圖之後重新出發上路向前行",
    147: "終極人際課題是敢不敢以真實的自己與人真誠相遇並相待",
}

text = path.read_text(encoding="utf-8")
bodies = list(m.BODIES)
for i, nb in fixes.items():
    old = bodies[i - 1]
    old_lit = '"' + old + '"'
    new_lit = '"' + nb + '"'
    if old_lit not in text:
        raise SystemExit(f"missing {i}: {old}")
    text = text.replace(old_lit, new_lit, 1)
    bodies[i - 1] = nb

path.write_text(text, encoding="utf-8")

assert len(bodies) == 150
dups = {k: v for k, v in Counter(b[:3] for b in bodies).items() if v > 1}
if dups:
    raise SystemExit(dups)
for i, b in enumerate(bodies, 1):
    if not (25 <= len(b) <= 70):
        raise SystemExit((i, len(b), b))

print("patched ok")
