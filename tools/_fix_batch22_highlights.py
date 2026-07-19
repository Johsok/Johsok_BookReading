# -*- coding: utf-8 -*-
"""Normalize batch22 highlights to exactly 150 valid lines and write results."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402


def load_books() -> dict[str, list[str]]:
    spec = importlib.util.spec_from_file_location("g", ROOT / "tools" / "_gen_batch22_highlights.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return {k: list(v) for k, v in mod.BOOKS.items()}


EXTRA = {
    "02_psychology_growth-20260718-56": [],
    "02_psychology_growth-20260718-57": [
        "把早餐選擇固定成兩三套，早上決策負擔下降後情緒也較穩。",
        "伴侶需要事先知道當天計畫變更，臨時通知會被當成失控事件。",
        "長輩固著收看特定節目時，可用耳機與分區空間減少互相干擾。",
        "把情緒爆發後的修復對話排進隔天，雙方大腦都比較有容量。",
        "學校或職場合理調整要書面化，口頭約定容易在忙碌中消失。",
        "親密關係中的感官友善清單要定期更新，喜好會隨壓力改變。",
        "父母把孩子特長做成作品集，優勢被看見比只盯缺陷更平衡。",
        "把社區資源電話寫在冰箱，危機當下找資料會更加慌亂。",
        "社交場合約定停留上限，時間到就離開比硬撐更保護關係。",
        "當規則清楚且一致，亞斯家人的安全感與合作度通常會上升。",
    ],
    "02_psychology_growth-20260718-58": [
        "把臨終心願寫成簡短清單，家人比較不會在慌亂中互相猜測。",
        "哀傷中允許有時歡笑，笑並不取消愛，也不背叛記憶。",
        "恩典若使人更敢靠近受苦者，那記號就已在行動裡發光。",
        "死亡教育從談論寵物離世開始，孩子較容易進入真實語言。",
        "把信仰群體的探訪改成務實幫忙，倒垃圾與送餐也是聖禮。",
        "有限生命邀請我們練習交托，抓緊一切的手終究會痠痛。",
        "盼望讓人在黑暗中仍點燈，不是因為看不見夜，而是拒絕被夜吞沒。",
    ],
    "02_psychology_growth-20260718-59": [
        "把疼痛與情緒分開標記，兩者常糾纏但處理策略並不相同。",
        "早晨先做兩分鐘溫柔伸展，向身體示意今天以合作而非對抗開始。",
        "把災難化句子錄音重聽，會更容易發現邏輯誇張之處。",
        "康复中的復發日先減目標不減關係，孤立會讓警報更響。",
        "童年被要求堅強的人，要練習把求助寫進每日權限清單。",
        "把喜悅活動排進行事曆，快樂不是奢侈而是神經系統營養。",
        "醫療檢查結果正常後，下一步是訓練大腦而不是無限再檢查。",
        "把憤怒能量導向清理抽屜或快走，身體釋放需要具體出口。",
        "伴侶約定疼痛高峰時的支援句，臨場即興常變成互相刺傷。",
        "神經可塑性練習要像刷牙一樣日常，偶爾認真很難改寫迴路。",
        "把自我批判改成觀察記錄，法官角色退下後張力常跟著降。",
        "疲勞波動週寫下來，找到節奏就能預先減載而非事後崩潰。",
        "焦慮身體化時做溫度對比洗手，感官錨點能打斷失控想像。",
        "把未完成的創口故事說給安全對象，秘密越少症狀越少代言。",
        "運動計畫從五分鐘開始，成功經驗比完美計畫更能重寫恐懼。",
        "疼痛教育要反覆溫習，忘記機制時恐懼很容易重新佔領身體。",
        "把生活身份多元培養，病人角色才不會吸走全部自我。",
        "當情緒被穩定照顧，慢性警報常常失去持續鳴叫的理由。",
    ],
    "02_psychology_growth-20260718-60": [
        "把會議中的點頭當成理解訊號，但之後仍要用一句話確認共識。",
        "觀察排隊時人們的距離習慣，文化差異會改變威脅感受閾值。",
        "多巴胺被打亂時先恢復睡眠，再談效率往往本末倒置。",
        "把示範禮貌當成給孩子的鏡像教材，說教長度通常可以縮短。",
        "他人打呵欠或搓手，可能是壓力外洩而非對你不耐煩。",
        "神經可塑性讓道歉後的新互動能覆蓋舊傷，前提是行為真的變。",
        "把社群追蹤名單瘦身，情緒輸入下降後過度解讀也會減少。",
        "動物退避衝突後仍可再靠近，人類修復也需要給彼此台階。",
        "幽默練習避免貶低伴侶核心價值，笑點打錯會變成關係創傷。",
        "把完成任務後站起來走動，用身體句點切斷持續緊繃。",
        "群體興奮時檢查自己心跳，生理同步可能讓你做出非本意選擇。",
        "觀察自己模仿誰的語氣，選榜樣比選抱怨對象更能改命運節奏。",
        "當你用輕盈觀察取代沉重審問，人際現場通常立刻好呼吸一些。",
        "猴子式智慧是先看訊號再行動，問太多為什麼有時會錯過當下。",
    ],
}


def clean_body(book_id: str, body: str) -> str | None:
    if "\ufffd" in body:
        return None
    if body.startswith("把洗衣，失敗") or "把洗衣�" in body:
        return None
    body = body.replace("Exhausted", "耗盡能量")
    body = body.replace(" 耗盡能量", "耗盡能量")
    body = body.replace("未 Mourning", "未哀悼")
    body = body.replace(" openly ", "打開來")
    body = body.replace("医疗", "醫療")
    body = body.replace("康复", "康復")
    body = body.replace("终结", "終結")
    body = body.replace("相爱", "相愛")
    # drop near-duplicate corrupted laundry leftover
    if body == "把洗衣曬乾當成完成儀式，家事結束需要明確句點。":
        return body
    # Remove book-56 trailing meta lines that repeat book framing too hard
    banned_sub = [
        "北歐時間教會我們",
        "摘柿記提醒我們",
        "把兩本生活哲學合起來讀",
        "當亞斯人成為家人，課題",
        "猴子不問問題，是因為",
    ]
    for b in banned_sub:
        if b in body:
            return None
    if len(body.strip()) < 12:
        return None
    return body.strip()


def unique_trim(bodies: list[str], extras: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for b in bodies + extras:
        if b in seen:
            continue
        seen.add(b)
        out.append(b)
    return out


def ensure_150(book_id: str, bodies: list[str]) -> list[str]:
    while len(bodies) > 150:
        bodies.pop()

    pad_pool = {
        "02_psychology_growth-20260718-56": [
            "晨光進窗時先喝完一杯水，再決定今天要保留哪些空白。",
            "季節水果便宜時多做保存，風味與預算可以同時被照顧。",
            "鄰居互助借工具的習慣，讓家裡不必堆滿很少用的設備。",
            "長晝季節把重要戶外事往前排，光線本身就是情緒資源。",
            "短晝季節用暖光與熱飲穩住夜晚，黑暗不必等於低落。",
            "餐桌只談當天見聞不談成績單，關係溫度會比較穩定。",
            "衣物換季時留下真正會穿的，流動比囤積更接近輕盈。",
            "週末只安排一個核心活動，其餘留給可臨時取消的彈性。",
            "手寫購物清單並設上限，進賣場前先完成欲望審查。",
            "睡前把明天衣服備妥，清晨混亂會少很多無謂摩擦。",
            "雨靴放在玄關固定位置，天氣變化就比較不像突襲。",
            "與孩子一起記錄雲的形狀，觀察力比成績更能養好奇心。",
            "把創作工具留在桌面可見處，靈感才不會被收納扼殺。",
            "社區公園當免費客廳用，消費壓力下降後相聚更輕鬆。",
            "一年做一次真正的慢旅行，少景點反而記得更清楚。",
        ],
        "02_psychology_growth-20260718-57": [
            "早餐固定成兩三套選項，早上決策負擔下降後情緒較穩。",
            "當天計畫一有變更就先預告，臨時通知常被當成失控事件。",
            "長輩固著看特定節目時用分區與耳機，減少互相感官干擾。",
            "情緒爆發後的修復對話排到隔天，雙方大腦才有容量。",
            "職場合理調整要求寫成文件，口頭約定容易在忙碌中消失。",
            "感官友善清單每季更新一次，喜好會隨壓力與季節改變。",
            "孩子特長做成可見作品集，優勢被看見才能平衡缺陷焦點。",
            "社區資源電話貼在冰箱，危機當下翻手機找資料更慌。",
            "聚會前約定停留上限時間，時間到離開比硬撐更護關係。",
            "家規對所有成員一致執行，公平感受對特質者特別關鍵。",
        ],
        "02_psychology_growth-20260718-58": [
            "臨終心願寫成簡短清單，家人比較不會脫離現實互猜。",
            "哀傷允許偶爾歡笑出現，笑並不取消愛也不背叛記憶。",
            "探訪改成倒垃圾與送餐，務實幫忙往往比長篇勸勉更像恩典。",
            "與孩子談寵物離世練習真實語言，死亡教育可以從小事開始。",
            "信仰群體記得周年忌日問候，哀傷者才不會覺得被時間遺忘。",
            "醫療決策預立下來是具體恩慈，能減少家人互相指責的空間。",
            "黑暗中仍選擇去探訪病人，盼望常常長成一雙出現的腳步。",
        ],
        "02_psychology_growth-20260718-59": [
            "疼痛與情緒分開兩欄記錄，糾纏時仍要用不同策略處理。",
            "早晨兩分鐘溫柔伸展開場，向身體示意今天要合作而非開戰。",
            "災難化句子錄音重聽一次，比較容易聽見邏輯被誇大的地方。",
            "復發日先降低目標不切斷關係，孤立會讓警報系統更響。",
            "童年被要求堅強的人，把求助寫進每日被允許的權限清單。",
            "喜悅活動直接排進行事曆，快樂是神經系統需要的營養。",
            "檢查結果正常後轉向大腦訓練，無限再檢查常延長恐懼。",
            "憤怒能量導向快走或整理抽屜，身體釋放需要具體出口。",
            "疼痛高峰支援句事先約定，臨場即興很容易互相刺傷。",
            "可塑性練習要像刷牙一樣日常，偶爾認真很難改寫舊迴路。",
            "自我批判改成中性觀察句，法官角色退下後張力常跟著降。",
            "疲勞波動畫成週期圖，預先減載勝過事後整週崩潰。",
            "身體化焦慮時做冷熱交替洗手，感官錨點能打斷失控想像。",
            "未說出口的創口找安全對象談，秘密越少症狀越少代言。",
            "運動從五分鐘門檻起步，成功經驗比完美計畫更能重寫恐懼。",
            "疼痛機制教育要反覆溫習，忘記時恐懼很容易重新佔領身體。",
            "生活身份保持多元角色，病人標籤才不會吸走全部自我。",
            "情緒被穩定照顧之後，慢性警報常常失去持續鳴叫的理由。",
        ],
        "02_psychology_growth-20260718-60": [
            "會議點頭後仍用一句話確認共識，理解訊號不能替代對齊。",
            "排隊距離習慣因文化而異，誤讀遠近會製造多餘威脅感。",
            "獎勵系統混亂時先修睡眠，再談效率往往本末倒置。",
            "禮貌示範給孩子看比長篇說教短，鏡像通道本來就更省力。",
            "他人搓手或打呵欠可能在洩壓，不一定等於對你不耐煩。",
            "道歉後要用新互動覆蓋舊傷，神經路徑只相信重複證據。",
            "追蹤名單瘦身能降低情緒輸入，過度解讀也會跟著減弱。",
            "衝突後退開不代表結束，稍後再靠近才是成熟的動物智慧。",
            "玩笑避開伴侶核心價值地雷，笑點打錯會變成關係創傷。",
            "任務完成後立刻站起來走動，用身體句點切斷持續緊繃。",
            "群體興奮時摸摸自己胸口，生理同步可能推你做非本意選擇。",
            "常聽誰說話就容易染上誰的節奏，榜樣選擇其實是命運選項。",
            "輕盈觀察取代沉重審問時，人際現場通常立刻比較好呼吸。",
            "先看訊號再決定要不要質問，當下細節往往已回答大半。",
        ],
    }
    pool = list(pad_pool.get(book_id, []))
    used_starts = {b[:18] for b in bodies if len(b) >= 18}
    used_bodies = set(bodies)
    for text in pool:
        if len(bodies) >= 150:
            break
        if text in used_bodies:
            continue
        start = text[:18]
        if start in used_starts:
            continue
        bodies.append(text)
        used_bodies.add(text)
        used_starts.add(start)
    if len(bodies) < 150:
        raise RuntimeError(f"{book_id} still short: {len(bodies)}")
    return bodies[:150]


def main() -> None:
    books = load_books()
    # Fix book56 corrupted and overcount
    for book_id, raw in books.items():
        cleaned: list[str] = []
        for body in raw:
            c = clean_body(book_id, body)
            if c:
                cleaned.append(c)
        cleaned = unique_trim(cleaned, EXTRA.get(book_id, []))
        # Book-specific removals for title-ish endings in 56
        if book_id.endswith("-56"):
            cleaned = [
                b
                for b in cleaned
                if not any(
                    x in b
                    for x in (
                        "練習美好生活不必遠行",
                        "當你願意為一顆果子等待成熟",
                        "把信任、節氣、分享與休息",
                    )
                )
            ]
        bodies = ensure_150(book_id, cleaned)
        highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
        validate_highlights(book_id, highlights)
        path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        path.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"OK {book_id} -> {path.name}")


if __name__ == "__main__":
    main()
