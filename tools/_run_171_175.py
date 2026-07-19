# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("g", ROOT / "tools" / "_gen_171_175.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

extra172 = [
    "現場回饋迴路愈短，模型與流程改進的複利愈明顯。",
    "把停機分鐘數貨幣化，轉型預算攻防會立刻具體起來。",
    "跨廠最佳實務庫要含失敗案例，避免只傳播成功幻燈片。",
    "資料契約比資料湖口號更能約束上下游責任。",
    "營運儀表要區分診斷指標與結果指標，避免指標自嗨。",
    "新技術導入窗口應避開旺季峰值，降低學習成本外部化。",
    "供應商鎖定風險要每年重估，特別是核心排程引擎。",
]

extra173 = [
    "貧窮家庭的時間稅很高，排隊與奔波本身就消耗謀生能量。",
    "夜間安全與照明影響女性勞動參與，基礎設施也是性別政策。",
    "學校餐食可同時改善營養與到課率，設計要防浪費與汙名。",
    "技能認證若不被雇主承認，訓練投入會變成沉沒成本。",
    "地方語言教材能降低學習門檻，尤其對第一代就學者。",
    "微型企業記帳工具可提高貸款可審核性，也能自我管理現金。",
    "災害後重建若忽略租戶與無產權者，不平等會被災難放大。",
    "青年失業造成疤痕效應，早期職缺品質影響一生軌跡。",
    "社會信任高的社區，公共方案執行成本往往較低。",
]

extra174 = [
    "比較靜態分析先固定其他條件，再觀察單一變數衝擊。",
    "一般均衡提醒，一處管制的效果會透過相對價格傳到他處。",
    "跨期選擇把利率視為今日與明日消費的相對價格。",
    "實質利率下降通常鼓勵投資，但也需看風險溢酬變化。",
    "潛在產出估計不完美，政策過度反應可能放大波動。",
    "規則型政策減少任意性，但碰上新衝擊仍需判斷空間。",
    "預期理論強調，政策可信度本身就是一種穩定工具。",
    "開放經濟乘數通常小於封閉經濟，因需求會漏到進口。",
    "貿易條件惡化等於實質收入下降，即使出口量表面成長。",
    "人力資本外溢使教育具公共性，但衡量外溢並不容易。",
    "制度經濟學把誘因與約束寫進成長故事，而不只堆資本。",
]

extra175 = [
    "演算法推薦若優化停留時長，公共議題討論可能被娛樂化。",
    "職場生產力工具會留下操作軌跡，監控界線要先談妥。",
    "合成數據可補訓練缺口，但若複製舊偏差只會加速偏誤。",
    "模型卡與資料卡讓採購方能比較風險，而不只看演示。",
    "公共計算資源若分配不公，會複製原有研究不平等。",
    "小型語言模型加領域微調，有時比巨型通用模型更可控。",
    "自動化客服的隱藏成本是升級無門時的憤怒外溢到社群。",
    "當系統能影響選舉或信用，治理強度應接近關鍵基礎設施。",
    "技術失業恐懼常高估短期、低估中期任務重組的複雜度。",
    "把增益部分導向廣基服務，能降低社會對自動化的敵意。",
]

b171 = g.B171[:150]
b172 = g.B172 + extra172
b173 = g.B173 + extra173
b174 = [
    s.replace("花费", "花費")
    .replace("边际效用", "邊際效應")
    .replace("承担", "承擔")
    .replace("滞胀", "滯脹")
    .replace("工资", "工資")
    for s in (g.B174 + extra174)
]
# Fix mistaken 邊際效應 -> 邊際效應 is wrong; should be 边际效用 -> 边际效用 in TW is 效用
b174 = [s.replace("邊際效應", "边际效用") for s in b174]
b174 = [s.replace("边际效用", "边际效用") for s in b174]
# Ensure traditional: 效用 is same; 邊際效用
b174 = [s.replace("边际效用", "边际效用") for s in b174]
# Direct fix
b174 = []
for s in g.B174 + extra174:
    s = s.replace("花费", "花費").replace("承担", "承擔").replace("滞胀", "滯脹").replace("工资", "工資")
    s = s.replace("边际效用", "边际效用")
    if "边际效用" in s:
        s = s.replace("边际效用", "边际效用")
    # original may have simplified 边际
    s = s.replace("边际效用递减", "边际效用遞減")
    s = s.replace("边际效用", "边际效用")
    b174.append(s)

# Clean approach for B174 traditional fixes
fixed = []
for s in g.B174 + extra174:
    s = (
        s.replace("花费", "花費")
        .replace("承担", "承擔")
        .replace("滞胀", "滯脹")
        .replace("工资", "工資")
        .replace("边际效用遞減", "边际效用遞減")
        .replace("边际效用", "边际效用")
        .replace("边际", "邊際")
        .replace("效用递减", "效用遞減")
    )
    # If still has 边际效用 as mixed, normalize
    s = s.replace("边际效用", "边际效用")
    fixed.append(s)
b174 = fixed
# Final normalize known phrase
b174 = [s.replace("边际效用", "边际效用").replace("邊際效应", "边际效用") for s in b174]
b174 = [s.replace("边际效用", "边际效用") for s in b174]

# Explicit: replace any remaining simplified forms
def to_tw(s: str) -> str:
    return (
        s.replace("花费", "花費")
        .replace("承担", "承擔")
        .replace("滞胀", "滯脹")
        .replace("工资", "工資")
        .replace("边际", "邊際")
        .replace("递减", "遞減")
    )


b174 = [to_tw(s) for s in (g.B174 + extra174)]
b175 = g.B175 + extra175

pairs = [
    (
        "01_business_startup-20260717-171",
        b171,
        "金融投機史【25周年長銷典藏版】：綜觀三百年九大投機狂潮，從泡沫中洞悉人性的貪婪與恐懼",
        "愛德華．錢思樂",
    ),
    (
        "01_business_startup-20260717-172",
        b172,
        "AI融合策略：矽谷工業巨頭如何擁抱人工智慧、即時數據，華麗轉型成為未來智慧工業",
        "維傑．高文達拉簡",
    ),
    (
        "01_business_startup-20260717-173",
        b173,
        "窮人的經濟學：如何終結貧窮？",
        "阿比吉特．班納吉",
    ),
    (
        "01_business_startup-20260717-174",
        b174,
        "零基礎也不怕，史丹佛給你最好懂的經濟學：個體經濟篇＋總體經濟篇套書",
        "提摩太．泰勒",
    ),
    (
        "01_business_startup-20260717-175",
        b175,
        "一個經濟學家的AI觀點：未來，剝削我們的是演算法，還是掌握演算法的「人」？",
        "羅傑．布特爾",
    ),
]

for book_id, bodies, title, author in pairs:
    print(f"=== {book_id} count={len(bodies)} unique={len(set(bodies))} ===")
    if len(bodies) != 150:
        raise SystemExit(f"{book_id} bad count {len(bodies)}")
    if len(set(bodies)) != 150:
        raise SystemExit(f"{book_id} duplicates")
    g.write_and_complete(book_id, bodies, title, author)

print("ALL_DONE")
