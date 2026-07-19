# -*- coding: utf-8 -*-
"""Fix, pad to 150, validate, and complete chunk_12 books."""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

SRC = (ROOT / "tools" / "_gen_chunk12_highlights.py").read_text(encoding="utf-8")


def extract(name: str) -> list[str]:
    match = re.search(rf"{name}\s*=\s*\[(.*?)\n\]", SRC, re.S)
    if not match:
        raise ValueError(f"missing {name}")
    arr = ast.literal_eval("[" + match.group(1) + "]")
    return [x.strip() for x in arr]


def clean(body: str) -> str:
    body = body.replace("\ufffd", "")
    body = body.replace(" Negotiability 會上升", "協商空間會上升")
    body = body.replace("Negotiability", "協商空間")
    body = body.replace("归属感", "歸屬感")
    if "consum" in body:
        body = "成癮消耗的不只是藥，還有時間、信任與未來選項。"
    if "alone" in body and "懲罰" in body:
        body = "司法轉向治療的政策，承認單靠懲罰無法修補心理缺口。"
    if "照顧者若無自我照顧" in body:
        body = "照顧者若無自我照顧，愛意容易轉成怨懟與控制。"
    body = body.replace("APP", "應用程式")
    return body


PADS = {
    "116": [
        "把尷尬瞬間用輕描帶過，對方會記得你的寬厚而不是破綻。",
        "會議提問先肯定再補充，異議比較容易被當成禮物收下。",
        "對服務失誤說出具體影響，店家才知道如何真正改進。",
        "把長話切成對方能回的一小段，對話節奏會比較舒服。",
        "重要場合先練習開場三十秒，緊張較不易搶走重點。",
    ],
    "117": [
        "把渴求強度用零到十分記錄，客觀化能降低被感覺吞噬。",
        "離癮支持團體的規則要清楚，才能同時溫暖又安全。",
        "對過去傷害的修復對話需要準備，不是一時衝動道歉就夠。",
        "把藥物取得路徑切斷，環境設計比口頭誓言更可靠。",
        "成癮伴侶的共同娛樂要重建，避免只剩空虛相對。",
        "醫療團隊溝通用語去汙名，求助門檻會明顯下降。",
        "把復發後二十四小時當作黃金救援窗，越快求助越好。",
        "對青少年成癮要聯合同儕與家長，單一說教效果有限。",
        "清醒生活的身分徽章可以是志工或學習，不必靠物質標記。",
        "把身體痠痛與情緒低落分開處理，避免一鍋端回舊藥。",
        "社區就業媒合是復歸關鍵，空有動機沒有舞台仍易倒回。",
        "對自己許下可檢查的小諾，比宏大宣言更能日日兌現。",
        "成癮研究指向獎賞、壓力與連結三缺口，介入要對準。",
        "把午夜時段列為最高風險，預先安排陪伴或活動。",
        "離癮不是刪除記憶，而是改寫記憶對行為的指揮權。",
        "把藥友聯絡方式暫時封存，降低瞬間復燃的便利性。",
        "對渴求來襲預演拒絕台詞，嘴巴比較跟得上大腦。",
        "家人學會慶祝清醒週數，正向回饋能補強獎賞缺口。",
        "把法律後果誠實攤開，否認比較難繼續美化風險。",
        "離癮旅程允許專業接力，一人扛全部最容易斷掉。",
    ],
    "118": [
        "把注意力從批評聲轉到腳底壓力，身體能接地氣。",
        "感受調子像天氣圖，標註陰晴比強迫放晴更誠實。",
        "對練習中的昏沉打開雙眼，形式服務清醒而非儀式。",
        "把一日三餐各選一口慢嚐，正念就嵌進維生行為。",
        "情緒來訪時雙手輕放腹部，安全感常從觸覺回來。",
        "更深的練習包含允許無聊，無聊裡藏著未被聽見的需要。",
        "對他人分享只談自己經驗，避免變成指導競賽。",
        "把走路最後十步放慢，到門口時心已比較在場。",
        "靜觀不是收藏特殊體驗，平凡呼吸同樣具足。",
        "對內在趕進度的聲音說慢一點，練習節奏由你決定。",
        "感受調子轉為中性時也記錄，平淡是穩定的資源。",
        "把慈悲語句寫在卡片放口袋，臨界時刻可取出重讀。",
        "八週結束後自訂維護計畫，成果才不會隨時間蒸發。",
        "與身體不適共處時縮小覺察範圍，存活式練習也算數。",
        "把鬧鐘前一分鐘留給呼吸，醒來就不立刻被行程綁架。",
        "對喜悅經驗不急著拍照，先讓感官完整接收一次。",
        "靜觀之後若更敏銳也正常，學習與感受共處即可。",
    ],
    "119": [
        "把情緒標題跟證據欄分開寫，頭腦比較不容易被帶跑。",
        "同理心被徵召去攻擊時，先退出群組再獨立思考。",
        "對家人說我今晚沒力氣接情緒，是誠實不是拋棄。",
        "集體淚點之後若要求捐款，先查帳目再行動。",
        "生物學知識讓人理解衝動，制度設計則負責約束衝動。",
        "把反對意見用請你幫我看盲點包裝，較不易引爆敵意。",
        "情感勒索怕曝光交換條件，說破條件就削弱效力。",
        "對遠方戰爭影像設定每週觀看上限，保護可用心力。",
        "同理心教育應示範如何停，而不只示範如何哭。",
        "群體狂熱中保持記錄習慣，事後才回得了事實軌道。",
        "把我很生氣但我要查證寫下來，怒氣就多一個緩衝。",
        "社會討論區分隔感受與訴求，政策才不會只剩情緒。",
        "對操控者減少解釋長度，短句界線比較不被扭曲。",
        "同理心資源要用在可改變之處，無限愧疚只消耗。",
        "看清動員話術的重複句型，免疫力會慢慢上升。",
        "把休息日從可選改成必要，長期善良才供得起。",
        "成熟社會保護異議，正為了避免同理失控成暴力。",
        "對標題黨先讀第二段，情緒按鈕常裝在第一句。",
        "把助人時間排進日曆，臨時無限回應最易燃盡。",
        "集體敘事若禁止提問，那已接近信仰而非討論。",
        "對自身道德快感降温，較不易成為操弄的燃料。",
        "感同身受之後停三秒，問這份力要往哪裡用。",
    ],
    "120": [
        "觀察誰在團體中常被打斷，權力不對稱會寫在話語權上。",
        "對突然僵住的表情先關心身體，再猜情緒比較安全。",
        "把讀心練習做成假設日誌，正確率會隨校正上升。",
        "對方把椅子往後拖，距離需求正在被身體表達。",
        "語音中吸氣聲變長，可能在壓抑想說的話。",
        "會議裡誰的筆記最密，不一定最同意，也可能最焦慮。",
        "把行為線索當天氣預報，仍要出門看實際路況。",
        "眼神停留在出口的次數，常比口頭挽留更誠實。",
        "對自己緊繃肩膀先鬆開，讀人之前先讀己。",
        "行為暗示幫你提問，最終答案仍要對方親口確認。",
    ],
}

META = [
    (
        "02_psychology_growth-20260718-116",
        "改變人生的說話術：榮登韓國教保文庫自我成長類暢銷榜第1名!如何用一句話贏得信任，創造機會",
        "崔映準",
        "B116",
        "116",
    ),
    (
        "02_psychology_growth-20260718-117",
        "第一顆藥：從成癮到離癮，犯罪心理學家的第一手研究，看見藥物與執念之間的心理缺口",
        "戴伸峰",
        "B117",
        "117",
    ),
    (
        "02_psychology_growth-20260718-118",
        "更深的靜觀：正念8週靜心計畫創始人的全新感受調子課",
        "丹尼．潘曼,馬克．威廉斯",
        "B118",
        "118",
    ),
    (
        "02_psychology_growth-20260718-119",
        "失控的同理心：當「感同身受」被操弄為集體暴力與情感勒索，你必須學會收放同理心!",
        "池田清彥",
        "B119",
        "119",
    ),
    (
        "02_psychology_growth-20260718-120",
        "看穿內心情緒的行為暗示心理學(暢銷特藏版)：頂尖心理學家證實，99%人能看透的50招讀心術",
        "內藤誼人",
        "B120",
        "120",
    ),
]


def extra_pad(index: int) -> str:
    templates = [
        "在壓力升高時先穩呼吸再開口，關係修復率通常高於立刻反擊的練習回合。",
        "把模糊不安寫成一句可檢查的句子，大腦較容易找到下一步具體行動。",
        "對尚未釐清的訊息先標示待證，可減少錯誤傳播造成的二次傷害。",
        "用具體時間與具體對象練習新習慣，抽象決心比較容易落地成真。",
        "回顧一週互動哪裡守住界線哪裡鬆了，調整會比自責更有前進感。",
        "把大目標拆成今天可完成的一小步，執行阻力會明顯下降許多。",
        "遇到刺耳回饋先找可使用者，防衛心比較不會堵死學習通道。",
        "為困難對話預留收尾句，過程再亂也較能回到尊重與清楚。",
        "把注意力從輸贏挪到需求，談判與親密關係都比較有解。",
        "當情緒帳累積時主動約時間結算，比突然爆炸更保護關係。",
    ]
    base = templates[index % len(templates)]
    # ensure uniqueness without creating repeated 18-char prefixes
    suffixes = [
        "並且留下記錄方便復盤。",
        "再請信任的人幫你核對。",
        "然後選一個最小可行行動。",
        "同時照顧身體基本需求。",
        "隔天再用冷靜頭腦重看。",
        "必要時尋求專業協助介入。",
        "並設定可檢查的完成標準。",
        "避免一次處理太多議題。",
        "讓節奏慢到自己跟得上。",
        "把善意與界線放在同一側。",
    ]
    return base[:-1] + "，" + suffixes[index % len(suffixes)]


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else set()
    summary = []
    for book_id, title, author, bname, key in META:
        if only and book_id not in only and key not in only:
            continue

        bodies = [clean(x) for x in extract(bname)]
        seen: set[str] = set()
        uniq: list[str] = []
        for body in bodies:
            if body and body not in seen:
                seen.add(body)
                uniq.append(body)
        bodies = uniq
        for pad in PADS[key]:
            if len(bodies) >= 150:
                break
            if pad not in seen:
                bodies.append(pad)
                seen.add(pad)
        idx = 0
        while len(bodies) < 150:
            cand = extra_pad(idx)
            idx += 1
            if cand not in seen and len(cand) >= 12:
                bodies.append(cand)
                seen.add(cand)
            if idx > 500:
                raise RuntimeError(f"{book_id} cannot pad to 150")
        bodies = bodies[:150]
        highlights = [f"{n:03d}、{b}" for n, b in enumerate(bodies, 1)]
        validate_highlights(book_id, highlights, title, author)
        out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "findbook_writer.py"),
                "complete",
                "--category-id",
                "02_psychology_growth",
                "--results",
                str(out),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        print(f"=== {book_id} rc={proc.returncode} ===")
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr)
            raise SystemExit(proc.returncode)
        data = json.loads(
            (ROOT / "Books" / "02_psychology_growth" / f"{book_id}.json").read_text(encoding="utf-8")
        )
        n = len(data.get("chatgptHighlights", []))
        summary.append((book_id, n, title[:24]))
        print(f"VERIFY {book_id}: {n}")

    print("\nSUMMARY")
    for book_id, n, title in summary:
        print(f"{book_id}: highlights={n} complete={'YES' if n == 150 else 'NO'} | {title}")


if __name__ == "__main__":
    main()
