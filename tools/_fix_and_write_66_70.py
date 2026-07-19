# -*- coding: utf-8 -*-
"""Fix highlight counts for 66-70, write results, optionally complete one id."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def load_gen():
    spec = importlib.util.spec_from_file_location("g", TOOLS / "_gen_grok_66_70.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def validate(book_id: str, highlights: list[str], title: str, author: str) -> list[str]:
    if len(highlights) != 150:
        raise ValueError(f"{book_id} count={len(highlights)}")
    if len(set(highlights)) != 150:
        raise ValueError(f"{book_id} duplicates")
    forbidden = ("本書", "作者指出", "本章", "這一章")
    short_colon = []
    for i, body in enumerate(highlights, 1):
        if len(body) < 12:
            raise ValueError(f"{book_id} #{i} short")
        if any(p in body for p in forbidden) or "｜" in body:
            raise ValueError(f"{book_id} #{i} forbidden text")
        if title and title in body:
            raise ValueError(f"{book_id} #{i} title")
        if author and author in body:
            raise ValueError(f"{book_id} #{i} author")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} #{i} step")
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL):
            short_colon.append(i)
    if len(short_colon) >= 3:
        raise ValueError(f"{book_id} short colon {short_colon[:10]}")
    starts = Counter(b[:18] for b in highlights if len(b) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        raise ValueError(f"{book_id} starts {starts.most_common(3)}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in highlights) >= 2:
            raise ValueError(f"{book_id} repeated {label}")
    return [f"{i:03d}、{h}" for i, h in enumerate(highlights, 1)]


def write_results(book_id: str, highlights: list[str], title: str, author: str) -> Path:
    lines = validate(book_id, highlights, title, author)
    path = TOOLS / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": lines}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def complete(book_id: str) -> str:
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(results),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise RuntimeError(out or f"exit {proc.returncode}")
    return out.strip()


FIX_REPLACEMENTS = {
    "關鍵零組合約自主化有戰略價值，但也要算清楚重複投資與規模不經濟": "關鍵零組件自主化有戰略價值，但也要算清楚重複投資與規模不經濟",
    "公會文化決定你學到什麼，長期待在嘲諷成長的圈子會被debuff": "公會文化決定你學到什麼，長期待在嘲諷成長的圈子會被持續削弱",
    "減益來源常是睡眠債與混亂桌面，先清debuff再談輸出": "減益來源常是睡眠債與混亂桌面，先清除負面狀態再談輸出",
    "釣魚小遊戲訓練耐心與機率思維，有些收益本來就 generational": "釣魚小遊戲訓練耐心與機率思維，有些收益本來就要跨很長時間才顯現",
    "快樂疲勞出現時該換地圖，強迫開心會變成新的debuff": "快樂疲勞出現時該換地圖，強迫開心會變成新的負面狀態",
    "翻譯不只語言，也要翻譯職場潛規則與 generational 溝通習慣": "翻譯不只語言，也要翻譯職場潛規則與不同世代的溝通習慣",
    "拒絕也能溫柔，說明限制比假裝答應更保護 reciprocal 信任": "拒絕也能溫柔，說明限制比假裝答應更能保護彼此信任",
    "創意會議禁止過早槍斃点子，先聽完再篩選能提高產量": "創意會議禁止過早槍斃點子，先聽完再篩選能提高產量",
    "為平台寫與為作品集寫要分開帳簿，短影音邏輯不等于長文邏輯": "為平台寫與為作品集寫要分開帳簿，短影音邏輯不等於長文邏輯",
    "書評不是剧透比賽，而是展示你如何與文本搏鬥": "書評不是劇透比賽，而是展示你如何與文本搏鬥",
    "獲獎有助信任，但評審口味不等于目標客群口味": "獲獎有助信任，但評審口味不等於目標客群口味",
}

# Drop corrupted / near-duplicate line in BOOK67
DROP_EXACT = {
    "連擊要求節奏穩定，三天打魚兩天�力",
}

PAD66_DROP_TAIL = 2  # trim extras after fixes

PAD67 = [
    "新手保護機制對應低風險練習場，先在安全區練熟再進高波動戰場",
    "成就分享要選對頻道，對錯的觀眾炫耀只會換來比較與消耗",
    "任務失敗後降低難度不是認輸，而是重新找到可完成的下一階挑戰",
    "把情緒當狀態列顯示，憤怒時禁止重大決策可避免永久傷害",
    "收集材料日與挑戰首領日要分開排，混在同一天容易兩頭不成",
    "語音指令愈短愈好執行，人生口號若太長就無法在壓力下呼叫",
    "側任務獎勵若會拖垮主線血條，寧願放棄華麗裝飾性成就",
    "把睡眠與飲食寫進增益欄，身體數值崩了再強的操作也會失誤",
    "通關慶典後立刻設下一張地圖入口，避免勝利空窗被成癮內容填滿",
    "把比較對象從他人排行榜改成昨天的自己，進步曲線才看得清楚",
]

PAD68 = [
    "傾聽時放下準備反駁的腹稿，大腦一旦寫講稿耳朵就會自動關門",
    "對方重複同一句話通常是核心诉求，別急著換題以為已經聽懂",
    "用時間戳記下關鍵承諾，記憶不可靠時文件就是第二雙耳朵",
    "引導提問避免連續逼問，审讯節奏會讓人立刻換上防禦面具",
    "先處理關係再處理事情，關係裂了再正確的方案也推不動",
    "聽到抱怨背後的標準，才能決定要道歉、要解釋還是要一起改流程",
    "讓沉默者先寫再說，內向成員的洞見常被會議語速剝奪",
    "對錯誤訊息温和校正，當眾羞辱會讓以後沒人願意回報壞消息",
    "傾聽結束要收束下一步，只有共感沒有行動會讓對話停在情緒泡泡",
    "定期關係體檢問最近什麼讓你感到被忽略，維修成本低於重建",
    "把手機朝下是具體尊重，口頭說我在聽卻滑螢幕會被身體拆穿",
    "引導不等于操控，最終選擇權仍要回到對方手上才算成功造局",
]

PAD69 = [
    "寫作日曆比靈感天氣可靠，固定出刊日會訓練大腦準時交稿",
    "選題來自重複出現的讀者問題，市場訊號比關起門空想更準",
    "開頭第一句要交付懸念或利益，讀者沒義務陪你暖身三個段落",
    "中段用小標題切開長坡，視線疲勞會讓再好的論證半途下車",
    "例子要夠近身，遙遠名人故事常輸給讀者明天用得上的小場景",
    "反對意見段能提升可信度，只唱獨角戲的文章像廣告而非思考",
    "結語留下可執行的最小下一步，思想投資要有復利的第一筆入金",
    "素材庫分引言、數據、故事與問題四桶，寫作當下才不會空白焦慮",
    "同一論點用信件、貼文與長文三型改寫，強迫你真正吃透結構",
    "限制字數是創造力道具，三百字挑戰常逼出比長文更利的刀子",
    "大聲朗讀能抓出拗口句，眼睛會自動腦補嘴巴會誠實卡關",
    "寫完靜置再編輯，距離感讓你比較敢刪掉心愛但無用的段落",
    "主題地圖每季重畫一次，避免十年都在重複同一層淺水區",
    "把嫉妒名單變成書單與課綱，情緒能量轉成可累積的能力投資",
    "寫作與金錢帳戶分開看，有些篇章先賺能力稍後再變現",
    "遇到瓶頸允許降載輸出，維持訊號不斷比硬產垃圾更保護品牌",
    "最終複利來自讀者記得並轉述你的一句話，那才是思想真正生息",
]

PAD70 = [
    "接案日與開發日分開排程，整天切換語境會讓兩邊效率一起下滑",
    "報價單用客戶語言寫成果，專業術語堆疊常讓決策者看不懂價值",
    "第一次合作刻意做小而美，信任厚度比首單金額更能決定後續",
    "客戶教育從詢問信開始，回覆品質就是品牌的第一件作品",
    "檔期衝突時給兩個真實選項，假承諾交期會在中期引爆關係",
    "把修改意見分類為錯誤、偏好與新增需求，報價與情緒才分得清",
    "交付當天附使用說明，減少上線後被當成免費客服綁住",
    "年底匯總收入來源結構，過度依賴單一客戶是隱藏的系統風險",
    "技能投資預算固定提撥，接案再忙也要留更新裝備的時間與錢",
    "身體不適就降載接單，硬撐交付出錯的商譽損失通常更貴",
    "家人支持會議定期開，自由工作的波動需要被家戶財務一起看見",
    "把成功案例沉淀成檢查表，下一個專案就能少靠臨場英雄救美",
    "拒絕範圍外要求時給替代方案，界線清楚仍可保持合作溫度",
    "跨月專案每週短同步，沉默太久會讓客戶腦內長出恐懼劇情",
    "收款條件寫進行事曆提醒，靠情緒記得催款會讓現金流隨機化",
    "建立備用通訊管道但不被二十四小時綁架，緊急定義要事先講清",
    "年度漲價信提前預告，突然加價比合理調整更容易失去好人緣",
    "把口碑客戶升級成顧問式長約，穩定顧問費能平滑接案波峰波谷",
    "實驗新服務用限量名額，降低試錯成本也製造可感知的稀缺",
    "失敗專案也寫進作品思考錄，展示學習速度有時比完美更吸客",
    "同行不是只有競爭，轉介溢出需求能讓彼此都吃得更飽",
    "法律與會計年度健檢一次，一人公司最容易在合規細節翻車",
    "幫未來的自己留下營運手冊，生病或休假時事業才不至於停擺",
]

# Fix simplified Chinese that slipped into pads
PAD68 = [s.replace("诉求", "訴求").replace("审讯", "審訊").replace("温和", "溫和").replace("不等于", "不等於") for s in PAD68]
PAD70 = [s.replace("沉淀", "沉澱") for s in PAD70]


def normalize_list(items: list[str], pads: list[str], target: int = 150) -> list[str]:
    out = []
    for h in items:
        if h in DROP_EXACT or "\ufffd" in h:
            continue
        h = FIX_REPLACEMENTS.get(h, h)
        h = (
            h.replace("不等于", "不等於")
            .replace("点子", "點子")
            .replace("剧透", "劇透")
        )
        if h not in out:
            out.append(h)
    for p in pads:
        if len(out) >= target:
            break
        if p not in out:
            out.append(p)
    if len(out) > target:
        out = out[:target]
    if len(out) < target:
        raise ValueError(f"still short {len(out)} need {target}")
    return out


def build_all():
    m = load_gen()
    meta = [
        ("01_business_startup-20260717-66", m.BOOK66, [], "超圖解東亞經濟奇蹟：體制與經濟發展的極限", "黃登興、黃幼宜"),
        ("01_business_startup-20260717-67", m.BOOK67, PAD67, "遊戲思維：人生，就是一場打怪升級的遊戲", "程子"),
        ("01_business_startup-20260717-68", m.BOOK68, PAD68, "造局傾聽術：隨心所欲引導對話與人際關係", "中村淳彥"),
        ("01_business_startup-20260717-69", m.BOOK69, PAD69, "寫作，是最好的自我投資：從注意力到思想複利", "陳立飛"),
        ("01_business_startup-20260717-70", m.BOOK70, PAD70, "原來可以這樣工作一輩子？自由工作者的穩定接案法", "小川真理子"),
    ]
    built = {}
    for book_id, base, pads, title, author in meta:
        highlights = normalize_list(base, pads, 150)
        built[book_id] = (highlights, title, author)
    return built


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    do_complete = "--complete" in sys.argv
    built = build_all()
    ids = [only] if only and only in built else list(built)
    for book_id in ids:
        highlights, title, author = built[book_id]
        path = write_results(book_id, highlights, title, author)
        print(f"prepared\t{book_id}\t{len(highlights)}\t{path.name}")
        if do_complete:
            msg = complete(book_id)
            print(msg)


if __name__ == "__main__":
    main()
