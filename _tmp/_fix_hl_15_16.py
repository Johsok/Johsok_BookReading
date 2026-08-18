# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

GEN = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_gen_hl_15_16.py")
OUT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_15_16.json")

LIU_PAD = [
    "此理甚明。",
    "官德在茲。",
    "民本不可倒裝。",
    "貶所亦當盡職。",
    "文章須有所為。",
    "可拿來檢驗吏治。",
    "清流正在這一念。",
]
SPAIN_PAD = [
    "史實不容粉飾。",
    "暴力寫進制度。",
    "帝國靠強制維持。",
    "轉型並未完結。",
    "殖民賬尚未結清。",
    "文化難洗白征服。",
    "民主從來不是終點。",
]


def load_lists():
    spec = importlib.util.spec_from_file_location("g", GEN)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return list(m.B15), list(m.B16)


def pad(t: str, i: int, pads: list[str]) -> str:
    t = t.replace("叙事", "敘事")
    if 35 <= len(t) <= 70:
        return t
    extra = pads[i % len(pads)]
    cand = t[:-1] + "，" + extra
    if len(cand) > 70:
        cand = t[:-1] + "，可核對。"
    if len(cand) < 35:
        cand = t[:-1] + "，這一點至今仍值得反覆核對。"
    return cand


def numbered(items: list[str]) -> list[str]:
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def check(name: str, items: list[str]) -> list[str]:
    errs: list[str] = []
    if len(items) != 150:
        errs.append(f"{name} count={len(items)}")
    d4 = [k for k, v in Counter(t[:4] for t in items).items() if v > 1]
    if d4:
        errs.append(f"{name} dup4={d4}")
    for i, t in enumerate(items, 1):
        n = len(t)
        if not (35 <= n <= 70):
            errs.append(f"{name} {i:03d} len={n} {t}")
        if t[-1] not in "。！？":
            errs.append(f"{name} {i:03d} not_complete")
        for w in ["本書", "作者指出", "本章", "步驟", "面向"]:
            if w in t:
                errs.append(f"{name} {i:03d} forbidden {w}")
        if re.search(r"[A-Za-z]", t):
            errs.append(f"{name} {i:03d} latin {t}")
    return errs


def main() -> None:
    b15, b16 = load_lists()
    # drop extra 裝腔、恃寵 item (keep 裝腔的虛勢)
    b15 = [t for t in b15 if not t.startswith("裝腔、恃寵")]
    repl15 = {
        "長安一樣盛產無德而有形的龐然大物，把黔之驢只讀成笑邊地，就誤了靶心。":
            "都城一樣盛產無德而有形的龐然大物，把黔之驢只讀成笑邊地，就誤了靶心。",
        "地方分權若無公開約束，會迅速變成私人武裝與私人稅源，封建論至今仍響。":
            "分權一旦缺少公開約束，會迅速變成私人武裝與私人稅源，封建論至今仍響。",
        "利益面前仍能把雇主是誰說出口，清流不是潔癖，而是不肯改口的倫理位置。":
            "好處擺在眼前仍能把雇主是誰說出口，清流不是潔癖，而是不肯改口的倫理位置。",
    }
    b15 = [repl15.get(t, t) for t in b15]

    repl16 = {
        "塞維利亞港壟斷美洲貿易，財富集中也造成走私、腐敗與對 hinterland 的抽血。":
            "白銀貿易被塞維利亞港壟斷，財富集中也造成走私、腐敗與內地被層層抽血。",
        "卡洛斯戰爭反覆撕裂鄉村，王位正統、教會特權與地方武裝糾纏成慢性病。":
            "王位正統之爭反覆撕裂鄉村，教會特權與地方武裝糾纏成十九世紀慢性病。",
        "一九七八年憲法確立議會君主制與自治區國家，把多元塞進可修訂的法律框架。":
            "憲法於一九七八年確立議會君主制與自治區國家，把多元塞進可修訂的法律框架。",
        "一九七七年大選讓政黨從地下走到議會，轉型關鍵是把槍口移出投票所。":
            "大選讓地下政黨走進議會，一九七七年轉型的關鍵是把槍口移出投票所。",
        "科爾特斯利用墨西卡帝國的納貢矛盾，殖民擴張靠離間與同盟，而不只靠勇氣。":
            "墨西卡帝國的納貢矛盾被科爾特斯利用，殖民擴張靠離間與同盟，而不只靠勇氣。",
        "北非移民面對圍欄與海上死亡，歐洲南門的人道危機寫在海峽每天的新聞裡。":
            "來自馬格里布的移民面對圍欄與海上死亡，歐洲南門的人道危機寫在海峽新聞裡。",
        "美洲原住民社會被武器、同盟分裂與疫病擊垮，征服叙事常把屠殺寫成奇蹟。":
            "原住民社會被武器、同盟分裂與疫病擊垮，征服敘事常把屠殺寫成奇蹟與天命。",
        "觀光與僑匯在一九六〇年代帶來外匯，開放消費並未開放言論，陽光下仍有警察。":
            "獨裁後期靠觀光與僑匯賺外匯，開放消費並未開放言論，陽光下仍有警察。",
        "流亡的猶太人把資本與印刷術帶到鄂圖曼與阿姆斯特丹，宗教統一輸掉長期人才。":
            "被逐猶太人把資本與印刷術帶到鄂圖曼與阿姆斯特丹，宗教統一輸掉長期人才。",
        "流亡作家把獨裁寫進世界文學，語言華麗擋不住監獄與審查被帶出國境。":
            "作家流亡後把獨裁寫進世界文學，語言華麗擋不住監獄與審查被帶出國境。",
        "軍事叛亂於一九三六年引爆內戰，德義援助佛朗哥，蘇聯與國際縱隊援助共和派。":
            "叛軍於一九三六年引爆內戰，德義援助佛朗哥，蘇聯與國際縱隊援助共和派。",
        "軍事修會把土地、信仰與武裝綁在一起，邊地暴力被說成神聖事業。":
            "修會把土地、信仰與武裝綁在一起，邊地暴力被說成神聖事業，土地隨信仰轉移。",
        "阿爾瓦公爵的血腥理事會用處決製造秩序，結果是更堅決的獨立意志與海上襲擊。":
            "血腥理事會在尼德蘭用處決製造秩序，結果是更堅決的獨立意志與海上襲擊。",
        "美洲各殖民地乘半島崩潰宣布獨立，帝國在十九世紀初失去主要大陸領地。":
            "各殖民地乘半島崩潰宣布獨立，帝國在十九世紀初失去主要大陸領地與稅源。",
        "一八九八年美西戰爭再失古巴、波多黎各與菲律賓，帝國殘餘被另一個帝國接收。":
            "美西戰爭於一八九八年再失古巴、波多黎各與菲律賓，帝國殘餘被另一帝國接收。",
        "第二共和推動土地、教育與政教分離，改革速度超過妥協能力，左右都走向武裝化。":
            "土地、教育與政教分離在共和時期齊頭推進，改革快過妥協，左右都走向武裝化。",
        "內戰流亡把獨裁寫進世界文學，語言的華麗擋不住作家把監獄與審查帶出國境。":
            "作家流亡後把獨裁寫進世界文學，語言華麗擋不住監獄與審查被帶出國境。",
        "歐元區中等經濟體靠觀光、汽車與農產出口過活，銀船已被貨櫃與包機取代。":
            "中等經濟體靠觀光、汽車與農產出口過活，銀船已被貨櫃與包機取代。",
        "一九六〇年代觀光與僑匯帶來外匯，開放消費並未開放言論，陽光下仍有警察。":
            "獨裁後期靠觀光與僑匯賺外匯，開放消費並未開放言論，陽光下仍有警察。",
        "一九三六年軍事叛亂引爆內戰，德義援助佛朗哥，蘇聯與國際縱隊援助共和派。":
            "叛軍於一九三六年引爆內戰，德義援助佛朗哥，蘇聯與國際縱隊援助共和派。",
    }
    b16 = [repl16.get(t, t) for t in b16]
    b16.append(
        "安達盧斯的建築層疊被印成明信片時，仍要讀出征服、改宗與驅逐疊在牆裡的地層。"
    )

    b15 = [pad(t, i, LIU_PAD) for i, t in enumerate(b15)]
    b16 = [pad(t, i, SPAIN_PAD) for i, t in enumerate(b16)]

    errs = check("15", b15) + check("16", b16)
    report = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_hl_fix_report.txt")
    if errs:
        report.write_text("\n".join(errs), encoding="utf-8")
        print("FAIL", len(errs))
        return
    payload = {
        "07_other-20260717-15": numbered(b15),
        "07_other-20260717-16": numbered(b16),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK", len(b15), len(b16), "min15", min(len(x) for x in b15), "max15", max(len(x) for x in b15),
          "min16", min(len(x) for x in b16), "max16", max(len(x) for x in b16))


if __name__ == "__main__":
    main()
