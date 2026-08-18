# -*- coding: utf-8 -*-
"""Strip mismatched pads and re-extend with book-themed endings."""
from importlib.machinery import SourceFileLoader
from pathlib import Path

src = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_b08_b09_b10.py")
fix = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_fix_hl_b08_10.py")
ns = {}
exec(fix.read_text(encoding="utf-8").split("def apply_repl")[0] + "\n", ns)
PADS = sorted(ns["PADS"], key=len, reverse=True)

m = SourceFileLoader("hl", str(src)).load_module()


def strip_pads(s):
    changed = True
    while changed:
        changed = False
        for p in PADS:
            if s.endswith(p) and len(s) > len(p) + 12:
                s = s[: -len(p)]
                changed = True
                break
    return s


P08 = """
，較合四時食補節奏
，並對照性味與禁忌
，選購時先認產季
，烹調保留清補之氣
，忌口比多吃更要緊
，新鮮度決定藥性強弱
，合體質才算食療
，逆季催熟效力常偏弱
，少油少醬才顯本味
，綠葉宜快炒少燜爛
，清湯連皮要洗淨泥砂
，黑色入腎仍防燥熱
，白色潤肺切忌過甜助痰
，紅色夏補也要防濕熱
，春發之氣忌怒忌鬱
，夏神明要清勿昏憒
，秋燥先護呼吸道
，冬寒先護腰膝足心
，穴位只輔助時令飲食
，二十六方隨節氣改料
，蔬果百科先讀禁忌欄
，肉類海鮮先分寒熱
，雜糧堅果忌高溫久炒
，市場摸重量防灌水
，隔夜湯撇油只熱一次
，兒童少用成人補法
，長者改粉入粥較安全
，血糖者把甜味另外算
，痛風者避開高普林部位
，過敏者先排除發物
""".strip().splitlines()

P09 = """
，才算把胃氣養住
，順食比貴藥更要緊
，中庸就是不走極端
，空胃進補最傷黏膜
，熱食細嚼才化得動
，寒熱要靠烹調來扳回
，連皮整物才不丟藥位
，別人的補可能是你的毒
，正餐仍在補品之前
，節氣菜只當配菜也夠
，廚房常備即日常藥房
，粥是養胃的基本功
，冰飲最容易把脾陽關掉
，睡前酸果最容易反流
，怒後先停食再喝熱粥
，七分飽留給晚間運化
，回鍋一次即盡勿反覆
，消積只對有積的人
，陰血不足時當歸也空轉
，陽藥沒有陰食會燒津
，孩童控糖重氣不重甜
，長者要能吞能化
，發燒先留胃氣抗病
，旅行先溫胃再嘗異味
，螢幕拿開迷走才啟動
，腰帶鬆了胃才降得下
，二便與腹感用來校對
，能香能化才是成功
，醃碟點胃不可當主菜
，酒冰放在熱湯之後
""".strip().splitlines()

P10 = """
，此乃該派宇宙論說法
，讀時勿當成臨床醫令
，重點在潔氣不在補劑
，固體被看成渣滓負擔
，揮發性氣體才被稱為養分
，加熱被指控驅散生命氣
，果食只是回走的過渡
，空氣被寫成真正燃料
，蛋白質神話在此被駁
，細胞據稱可自組氮氫
，十五日翻轉只是其宣稱
，每週兩日被當成節奏
，高地潔氣被理想化
，雨水被指定為飲品
，血液被比喻成液態氣
，退化階梯以肉食為終站
，復食過快被說更危險
，密閉污濁被視為退化源
，煙草酒精被列為破氣
，化驗單被看成固體尺子
，神志清明才是其指標
，樹上現摘被寫成保氣
，用火熟食被當成墮落
，搬家換氣勝過吞礦片
，實踐仍看呼吸是否加深
，社交餐桌最容易破功
，排毒語言不可覆蓋惡化
，宇宙物質被說成氣態礦
，皮膚與肺都被要求呼吸
，長壽例證當該派敘事看
""".strip().splitlines()

P08 = [x.strip() for x in P08 if x.strip()]
P09 = [x.strip() for x in P09 if x.strip()]
P10 = [x.strip() for x in P10 if x.strip()]


def extend(s, pads, i):
    if 28 <= len(s) <= 55:
        return s, i
    if len(s) > 55:
        return s[:55], i
    t = s
    guard = 0
    while len(t) < 28 and guard < 8:
        extra = pads[i % len(pads)]
        i += 1
        if extra in t:
            extra = pads[i % len(pads)]
            i += 1
        if len(t) + len(extra) <= 55:
            t += extra
        else:
            t += extra[: 55 - len(t)]
        guard += 1
    if len(t) > 55:
        t = t[:55]
    if len(t) < 28:
        raise RuntimeError(len(t), t)
    return t, i


out = {}
for key, pads in (("b08", P08), ("b09", P09), ("b10", P10)):
    i = 0
    xs = []
    for s in m.BOOKS[key]:
        t, i = extend(strip_pads(s), pads, i)
        xs.append(t)
    out[key] = xs

lines = ["# -*- coding: utf-8 -*-", "BOOKS = {"]
for k, xs in out.items():
    lines.append(f"{k!r}: [")
    for s in xs:
        lines.append(f"    {s!r},")
    lines.append("],")
lines.append("}")
src.write_text("\n".join(lines) + "\n", encoding="utf-8")
print({k: (len(v), min(map(len, v)), max(map(len, v))) for k, v in out.items()})
