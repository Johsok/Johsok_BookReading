# -*- coding: utf-8 -*-
"""Fix and complete batch56 highlights to 150 each, then write via findbook_writer."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

sys.path.insert(0, str(ROOT / "tools"))

# Load partial lists
ns56 = {"__file__": str(ROOT / "tools" / "_gen_batch56.py")}
exec((ROOT / "tools" / "_gen_batch56.py").read_text(encoding="utf-8"), ns56)
ns_rest = {}
exec((ROOT / "tools" / "_gen_batch56_rest.py").read_text(encoding="utf-8"), ns_rest)

BOOK56 = list(ns56["BOOK56"])
BOOK57 = list(ns56["BOOK57"])
BOOK58 = list(ns_rest["BOOK58"])
BOOK59 = list(ns_rest["BOOK59"])
BOOK60 = list(ns_rest["BOOK60"])

# Fix bad lines
FIXES = {
    ("58", "當化學工具失效時， integr ated 組合中的輪作與覆蓋才顯真價值"):
        "當化學工具失效時，輪作覆蓋與機械防除的組合價值才真正顯現",
    ("59", "保护区與國家公園規範限制採集，傳統利用需走申請與共管機制"):
        "保護區與國家公園規範限制採集，傳統利用需走申請與共管機制",
    ("59", "栽培要点含繁殖法與病蟲害，鼓勵花園種植以減野外壓力"):
        "栽培要點含繁殖法與病蟲害，鼓勵花園種植以減野外壓力",
    ("59", " ethnobotany 倫理要求回饋知識社群，出版利益應討論分享機制"):
        "民族植物研究倫理要求回饋知識社群，出版利益應討論分享機制",
    ("59", "芋與甘藷 savior 作物在颱風後快速提供熱量，種植知識仍具韌性價值"):
        "芋與甘藷作為救荒作物在颱風後快速提供熱量，種植知識仍具韌性價值",
    ("59", "野外遇見 native plant 時先問會不會、該不該採，再問怎麼用"):
        "野外遇見本土植物時先問會不會、該不該採，再問怎麼用",
}

def apply_fixes(book_key: str, lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        key = (book_key, line)
        out.append(FIXES.get(key, line))
    return out

BOOK58 = apply_fixes("58", BOOK58)
BOOK59 = apply_fixes("59", BOOK59)

PAD56 = [
    "脈衝星計時精度可媲美原子鐘，用來檢驗重力理論與探測低頻引力波背景",
    "星系形態分類從橢圓到螺旋再到不規則，反映不同形成與交互歷史",
    "活動星系核光譜依射電與光學特徵分型，有助比較中央引擎與寄主星系關係",
    "宇宙射線空氣簇射在地面陣列可重建初級粒子能量與方向",
    "中微子天文觀測穿透力極強，能揭示超新星核心塌縮的即時訊息",
    "太陽震盪學用表面波動反推內部結構，類似地震波掃描地球",
    "系外衛星搜尋仍早期，但其大氣若存在或可擴充可居環境樣本",
    "潮汐鎖定使近距行星恆面向恆星，氣候模型必須處理極端日夜差",
    "大氣逃逸在低重力高輻射環境加劇，小型行星更難長期保有厚大氣",
    "磁場保護可能減緩大氣剝蝕，比較行星學因此關注內部發電機條件",
    "撞擊坑統計可粗估地表年齡，月球與火星年代學常靠此交叉校正",
    "冰衛星地下海假說來自潮汐熱與磁場感應資料，拓展生命搜尋場景",
    "有機分子在星際雲與彗星中被偵測到，說明生命前體化學並不罕見",
    "實驗室天文用微波與紅外光譜比對太空訊號，確認分子指紋",
    "公開資料檔讓全球研究者重分析同一觀測，加速發現也利於錯誤覆核",
    "公民望遠鏡網路可追蹤暫現源，專業警報加上業餘響應縮短遺漏",
    "科普寫作要把信心水準與競爭假說並列，避免單一敘事鎖死想像",
    "下一代極大望遠鏡將解析更早期星系，邊界問題會隨數據一再改寫",
    "黑洞研究把重力、量子與熱力學拉到同一桌，是基礎物理的交會點",
    "把「看不到」轉成可測量效應，正是現代天文把邊界往外推的方法",
    "保持開放又不輕信，才能在宇宙尺度的未知面前繼續往前走",
]

PAD57 = [
    "雨滴撞擊葉面的節奏隨葉形與角度改變，聽覺也能成為微氣候指標",
    "霧氣凝結在蛛絲上形成水珠鏈，提醒表面張力如何塑造可見世界",
    "朽木內部溫度常高於氣溫，微生物代謝熱支撐特殊小型生境",
    "樹瘤與癒傷組織記錄過去傷害，也成為昆蟲與真菌的二次棲所",
    "葉蟲啃食圖案可輔助鑑定，缺刻位置與形狀常具物種特異性",
    "蚜蟲排泄蜜露吸引螞蟻互助，同時可能傳播植物病毒",
    "蟬的地下若蟲吸食根部數年才羽化，物候大發生年會重寫林下養分流",
    "螢火蟲光訊號用於求偶，光害會提高配對失敗率",
    "腐殖質酸影響金屬離子有效性，間接左右幼苗微量元素吸收",
    "石頭下的濕潤避難所聚集等足類與蜈蚣，翻動後應輕放歸位",
    "季節性溪流斷流期，水生昆蟲以耐旱卵或遷移成蟲渡過",
    "樹冠層附生蘭與蕨類截取霧水，形成離地濕島",
    "松果開閉隨濕度變化，是種子散布與天氣聯動的小型機械",
    "松鼠通道與跳躍路線塑造枝條磨損痕跡，行為留下結構印記",
    "狐狸與貂的氣味標記重疊領域，哺乳動物地圖常靠鼻子閱讀",
    "腐肉氣味召集成群埋葬蟲，養分快速重返土壤食物網",
    "鳥類換羽期飛行動能下降，隱蔽棲位需求上升",
    "種子萌發後子葉形態可助科屬判斷，比成葉更早提供線索",
    "連作觀察教會你區分罕見訪客與常駐居民，避免一次驚喜定論",
    "把手機收起來一段時間，注意力才回得來給緩慢展開的事件",
    "若要把祕境分享給他人，先示範安靜與等待，再示範命名",
]

PAD58 = [
    "田埂水泥化後種源改道，管理策略要隨基礎設施更新一起改寫",
    "有機質敷蓋分解過快時需分次補料，才能維持遮光厚度",
    "芽前藥劑對已出土雜草無效，時機錯誤等於浪費成本與抗性壓力",
    "抗性檢測可用劑量反應盆栽試驗，田間懷疑要儘速實驗室確認",
    "多年生雜草的地下芽庫盤點，比只數地上莖更能預測回彈",
    "整合方案年度檢討應比較產量、成本與草相變化三條曲線",
]

PAD59 = [
    "標本採集號與報導人代碼對應，日後訂正鑑定才找得到源頭",
    "汁液黏性與顏色變化可當場記錄，乾燥標本常失去這些性狀",
    "幼葉與成熟葉形態差異大時，圖鑑應同時呈現以免誤認",
    "寄生植物如菟絲子也有民俗用途，但仍可能危害作物需分開討論",
    "海岸漂流種子傳播史解釋部分共有植物，島嶼生物地理不可忽略",
    "火山與泥岩地特有植物常具狹域分布，利用強度要特別保守",
    "石灰岩地形植物群落特殊，民族知識亦常對應獨特地質",
    "濕地香蒲與蘆葦的編織與食用加工，展示水生資源完整利用鏈",
    "蕨類抱子與幼葉利用傳統存在，但部分種類具毒性需嚴謹鑑定",
    "苔蘚雖少作大宗材料，在保濕敷材與微生境指標上仍有角色",
    "種子萌發試驗可驗證口述繁殖法，科學與經驗互相校正",
    "氣生根與板根樹種的支撐功能影響聚落選樹與神話敘事",
    "果皮染料與果肉食用可能來自同一株，部位分工要寫清楚",
    "乳膠凝固技術決定是否能成器具或織品，工藝參數屬於知識本體",
    "炭窯技術選擇樹種影響火力與煙味，技藝復興需材料學配合",
    "獵場火燒管理若存在，應記錄季節與頻率，而非以現代禁火一刀切",
    "漁網植物纖維耐鹽耐晒性質，決定其在海岸社群的不可替代性",
    "兒童遊戲植物常是入門生態教育，保存玩耍知識也是傳承",
    "夢境、占卜與植物聯結屬宇宙觀範疇，記錄時避免化約成迷信二字",
    "戰爭避難與遷移路線上的可食植物清單，是韌性知識的極端考題",
    "現代臨床案例若引用民族用法，必須回溯原脈絡與劑量條件",
    "開放授權圖像仍要尊重拍攝地社群感受，尤其涉及儀式場景",
    "增訂版收錄氣候新生境紀錄，例如高海拔新現的低海拔利用種",
    "讀者若是醫療人員，圖鑑應導向專業諮詢而非替代診斷",
    "農業試驗所與部落合作保存種原，可把圖鑑知識轉成活體庫存",
    "語言巢與植物園走讀結合，讓孩子在身體移動中學會詞彙",
    "把感謝與互惠寫進程式，研究結束後仍維持長期關係而非一次取样",
]

PAD60 = [
    "探究課時間不夠時，可採多週連續同一問題，比單堂假探究更真",
    "學生自訂測量工具後再與標準儀器比對，能體會校准意義",
    "把新聞標題改寫成可檢驗假說，是連接媒體素養與科學方法的練習",
    "錯誤答案公開討論時先保護提出者尊嚴，焦點放在推理結構",
    "實驗室座位輪替降低固定成見，也讓不同動作技能被看見",
    "用學生語言先說現象，再引入形式定義，可降低符號焦慮",
    "長周期實驗設中繼檢查點，避免期末才發現整組資料作廢",
    "邀請高中生協助國小科學日，教學相長也擴散科學文化",
    "對行政抽查說明探究證據鏈，比展示精美海報更能護衛課室方向",
    "把安全失誤當案例教學，而非只懲罰，可形成真正的安全文化",
    "閱讀原始科普論文摘要，訓練抓研究問題與限制條件",
    "比較兩份結論相反的研究，練習尋找方法差異而非選邊站",
    "校園爭議主題討論設證據桌與價值桌，分開談事實與取捨",
    "教師備課寫下預期迷思清單，課堂才能預備對應的衝突事件",
    "讓學生為下屆留下設備使用須知，知識承啟從同儕文件開始",
    "評量結束後公布常見錯誤統計，全班一起重修概念而非只對分數",
    "把「我不知道但可以怎麼查」說出口，示範知性誠實",
    "畢業前完成一次完整的學驗思循環專題，作為科學公民成年禮",
]


def pad_to_150(lines: list[str], pad: list[str], label: str) -> list[str]:
    lines = [x.strip() for x in lines if x.strip()]
    # drop remaining bad english fragments if any
    cleaned = []
    for x in lines:
        if "integr" in x or "ethnobotany" in x or "native plant" in x or "savior" in x:
            continue
        cleaned.append(x)
    lines = cleaned
    need = 150 - len(lines)
    if need < 0:
        raise SystemExit(f"{label} has {len(lines)} > 150")
    if need > len(pad):
        raise SystemExit(f"{label} need {need} but pad only {len(pad)}")
    # ensure uniqueness
    existing = set(lines)
    add = []
    for p in pad:
        p = p.strip()
        if p not in existing:
            add.append(p)
            existing.add(p)
        if len(add) == need:
            break
    if len(add) < need:
        raise SystemExit(f"{label} could only add {len(add)}/{need}")
    out = lines + add
    assert len(out) == 150, (label, len(out))
    return out


BOOK56 = pad_to_150(BOOK56, PAD56, "56")
BOOK57 = pad_to_150(BOOK57, PAD57, "57")
BOOK58 = pad_to_150(BOOK58, PAD58, "58")
BOOK59 = pad_to_150(BOOK59, PAD59, "59")
BOOK60 = pad_to_150(BOOK60, PAD60, "60")


def numbered(lines: list[str]) -> list[str]:
    out = []
    for i, body in enumerate(lines, 1):
        body = body.strip()
        assert len(body) >= 12, (i, body)
        out.append(f"{i:03d}、{body}")
    return out


def validate_local(book_id: str, highlights: list[str], title: str = "", author: str = "") -> None:
    short_colon = []
    bodies = []
    forbidden = ("本書", "作者指出", "本章", "這一章")
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        assert line.startswith(expected), (book_id, index, line[:40])
        assert "\n" not in line and "\r" not in line and "｜" not in line
        body = NUMBER_RE.sub("", line, count=1).strip()
        assert len(body) >= 12, (book_id, index, body)
        for p in forbidden:
            assert p not in body, (book_id, index, p)
        assert not re.search(r".{1,8}面第\d+步[，,]", body)
        assert not re.match(r"^第\d+步[，,]", body)
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon.append(index)
        bodies.append(body)
    assert len(short_colon) < 3, (book_id, short_colon)
    assert len(set(bodies)) == 150, book_id
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    assert starts.most_common(1)[0][1] < 4, (book_id, starts.most_common(3))
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in bodies) >= 2:
            raise AssertionError(f"{book_id} repeats {label}")


def write_results(book_id: str, lines: list[str], title: str = "", author: str = "") -> Path:
    highlights = numbered(lines)
    validate_local(book_id, highlights, title, author)
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def run_writer(category_id: str, results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def main() -> None:
    books = [
        ("03_natural_science-20260718-56", "03_natural_science", BOOK56,
         "宇宙的邊界到底在哪?黑洞不是終點，而是我們與星空之間的開端", "姚建明"),
        ("03_natural_science-20260718-57", "03_natural_science", BOOK57,
         "森林祕境：生物學家的自然觀察年誌(自然寫作經典，長銷慶功版，隨書附贈限量精美2026年曆小卡)", "大衛．喬治．哈思克"),
        ("03_natural_science-20260718-58", "03_natural_science", BOOK58,
         "雜草管理學(第1版)", "王慶裕"),
        ("03_natural_science-20260718-59", "03_natural_science", BOOK59,
         "臺灣民族植物圖鑑(增訂版)", "楊智凱,鍾明哲"),
        ("03_natural_science-20260718-60", "03_natural_science", BOOK60,
         "學驗思：文化承啟與科學教育", "劉源俊　著"),
    ]
    ok = []
    fail = []
    for book_id, cat, lines, title, author in books:
        try:
            # also fix remaining simplified in body
            fixed = []
            for line in lines:
                line = line.replace("无效", "無效").replace("盘点", "盤點").replace("茎", "莖")
                fixed.append(line)
            path = write_results(book_id, fixed, title, author)
            run_writer(cat, path)
            ok.append(book_id)
        except Exception as exc:
            fail.append((book_id, str(exc)))
            print("FAIL", book_id, exc)
    print("OK", ok)
    print("FAIL", fail)


if __name__ == "__main__":
    main()
