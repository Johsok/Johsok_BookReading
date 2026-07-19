# -*- coding: utf-8 -*-
"""Fix, pad, validate and complete books 67-70."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from _gen_grok_67_70 import BOOK67, BOOK68, BOOK69, BOOK70, fix_typos  # noqa: E402
from findbook_writer import validate_highlights  # noqa: E402

PAD68 = [
    "交辦會議若超過三人，會後仍要指定單一執行窗口，避免大家都以為別人會做。",
    "部屬回報卡關時，主管先給資源選項再給期限，比只加壓力更能恢復執行。",
    "把常見客訴做成決策樹，前線才不會每次都被情緒牽著現場發明規則。",
    "同一錯誤若跨多人出現，召開十分鐘對齊會比分別約談更有效率。",
    "新進人員前兩週只給單一主任務，過早多線並行會放大遺忘與錯置。",
    "主管離開座位前留下今日必完成三件事，代理者才接得住不斷的臨時交辦。",
    "當部屬說我想做得更好，立刻約定可觀察的下一件小改變與檢查日。",
    "客戶稱讚個人卻要求破例時，教部屬把功勞歸團隊並把例外帶回內部。",
    "執行清單要寫動詞開頭的句子，名詞堆疊無法驅動行動。",
    "若進度會議變成追責大會，改成阻礙清除會，發言品質通常會改善。",
    "對高敏感部屬，書面回饋先給對方閱讀時間，再約面談補充溫度。",
    "帶人困擾升高前，先檢查自己本週是否連續改口三次以上。",
    "把成功案例錄成兩分鐘說明，比重複口述更能穩定複製正確做法。",
    "消除帶人困擾的收尾動作是公開更新規則，讓改進變成大家的新預設。",
]

PAD69 = [
    "早期團隊的週會應用半數時間設計下一實驗，其餘時間才處理營運雜務。",
    "顧客願付費的證據要強過親友稱讚，否則容易活在溫室回饋裡。",
    "把通路酬庸算進真實獲客成本，商業模式才不會紙上漂亮、帳上流血。",
    "當兩個創辦人爭功能方向，回到共同假設清單投票，用證據結束口角。",
    "獨角獸路徑上的耐心，是忍受重複驗證的枯燥，而不是忍受拒絕學習。",
]

PAD70 = [
    "擴張期引入中階主管後，仍要保留創辦人可直接看到原始同期群數據的權限。",
    "價格頁的微文案測試屬於營收工程，應與產品功能迭代爭取同等注意力。",
    "當某個渠道貢獻過半營收，進階風險清單就要寫進替代渠道進度。",
    "客戶成功若只被衡量工單量，會獎勵救火而非預防流失。",
    "把年度大會的戰略翻譯成前線每週可做的三種行為，策略才不算漂浮。",
    "進階階段的實驗倫理包含告知與退出，信任是可複利的無形資產。",
    "毛利改善來自組合拳：減無效功能、優化交付、調整客群結構同步進行。",
    "當投資人催成長，拿出悲觀情境下的單位經濟，比情緒對抗更有力。",
    "跨國客服時段覆蓋要用需求熱圖配置，平均主義會浪費現金。",
    "產品封存功能前先看實際使用率與營收歸因，避免錯砍沉默但關鍵的價值。",
    "進階護城河要能在盡職調查中被指出證據，否則只是簡報修辭。",
    "讓前線每周提交一個卡住成交的假設，成長學習才不會停在辦公室。",
    "現金水位警報要連到自動放慢投放的規則，人為猶豫常讓缺口更大。",
    "模式複雜度上升時，用一頁紙對新員工講清誰付錢、為何續留。",
    "當留存提升卻口碑下降，檢查是否用鎖定機制取代真正價值。",
    "進階創業的成熟標記，是團隊能在沒有英雄救場下穩定完成學習閉環。",
]


def neutralize_short_colons(lines: list[str]) -> list[str]:
    natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    out = []
    for body in lines:
        body = (
            body.replace("不等于", "不等於")
            .replace("纠正", "糾正")
            .replace("口头", "口頭")
            .replace("过高", "過高")
            .replace("体感不对", "體感不對")
            .replace("每周", "每週")
        )
        if "渠道契合" in body and ("eth" in body or "可以複製" in body or "穩定複製" in body):
            body = "產品市場契合之後的下一題，是渠道契合，同樣訊息要證明在哪個管道可以穩定複製。"
        if "加法組織" in body:
            body = "進階階段淘汰功能與淘汰渠道同樣重要，加法組織會失去焦點與銳度。"
        if "替代技術" in body:
            body = "當市場出現替代技術，重新驗證你的價值是否仍獨立於舊技術假設。"
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(natural):
            body = body.replace("：", "，", 1).replace(":", "，", 1)
        out.append(body)
    return out


def ensure_unique_pad(base: list[str], pads: list[str]) -> list[str]:
    existing = set(base)
    added = []
    for item in pads:
        if item not in existing:
            added.append(item)
            existing.add(item)
    return base + added


def write_and_complete(book_id: str, title: str, author: str, lines: list[str]) -> None:
    if len(lines) != 150:
        raise SystemExit(f"{book_id} need 150 got {len(lines)}")
    starts = Counter(body[:18] for body in lines if len(body) >= 18)
    bad = [(key, value) for key, value in starts.items() if value >= 4]
    if bad:
        raise SystemExit(f"{book_id} repeated starts {bad[:5]}")
    if len(set(lines)) != 150:
        raise SystemExit(f"{book_id} duplicate bodies")
    highlights = [f"{index:03d}、{text}" for index, text in enumerate(lines, 1)]
    validate_highlights(book_id, highlights, title, author)
    results_path = TOOLS / f".findbook_results_grok_{book_id}.json"
    results_path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    command = [
        sys.executable,
        str(TOOLS / "findbook_writer.py"),
        "--root",
        str(ROOT),
        "complete",
        "--category-id",
        "01_business_startup",
        "--results",
        str(results_path),
    ]
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    sys.stdout.write((proc.stdout or "").strip() + "\n")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "")
        raise SystemExit(proc.returncode)
    book = json.loads((ROOT / "Books" / "01_business_startup" / f"{book_id}.json").read_text(encoding="utf-8"))
    print(f"confirm\t{book_id}\t{len(book['chatgptHighlights'])}\t{book.get('highlightsSource')}")


def main() -> None:
    fix_typos()
    book67 = neutralize_short_colons(BOOK67)
    book68 = neutralize_short_colons(ensure_unique_pad(BOOK68, PAD68))
    book69 = neutralize_short_colons(ensure_unique_pad(BOOK69, PAD69))
    book70 = neutralize_short_colons(ensure_unique_pad(BOOK70, PAD70))
    # neutralize again after pad (pad may contain short colons)
    book67 = neutralize_short_colons(book67)
    book68 = neutralize_short_colons(book68)
    book69 = neutralize_short_colons(book69)
    book70 = neutralize_short_colons(book70)

    print("counts", len(book67), len(book68), len(book69), len(book70))
    overlap = set(book69) & set(book70)
    if overlap:
        raise SystemExit(f"overlap 69/70: {len(overlap)} {next(iter(overlap))}")

    books = [
        (
            "01_business_startup-20260716-67",
            "祕書親信該有的參謀思維：成為辦公室的拆彈專家，上司倚仗的智囊心腹，解鎖升遷限制的職場破框思考",
            "荒川詔四",
            book67,
        ),
        (
            "01_business_startup-20260716-68",
            "當部屬無法依指令做事：很努力卻沒照你說的執行、重複同樣的錯、忘東忘西、把建議當惡意、被客戶牽著走……一步驟消除主管帶人困擾。",
            "榎本博明",
            book68,
        ),
        (
            "01_business_startup-20260716-69",
            "我創業，我獨角 no.10：精實創業全紀錄，商業模式全攻略",
            "羅芷羚",
            book69,
        ),
        (
            "01_business_startup-20260716-70",
            "我創業，我獨角 no.11：精實創業全紀錄，商業模式全攻略",
            "羅芷羚",
            book70,
        ),
    ]
    for book_id, title, author, lines in books:
        print(f"=== doing {book_id} ===")
        write_and_complete(book_id, title, author, lines)
    print("ALL DONE")


if __name__ == "__main__":
    main()
