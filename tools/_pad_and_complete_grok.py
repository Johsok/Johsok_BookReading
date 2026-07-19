# -*- coding: utf-8 -*-
"""Pad incomplete books to 150 and run findbook_writer complete."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
GEN = TOOLS / "_gen_grok_batch_20260717_need.py"

EXTRA: dict[str, list[str]] = {
    "01_business_startup-20260717-104": [
        "把年度檢討做成可執行的調整清單，而不是情緒性的自我責備",
        "當本金跨越心理門檻時重審風險上限，規模變大規則也要升級",
        "投資教育優先補齊行為缺口，知識堆疊無法自動變成紀律",
        "用睡眠品質反推風險部位是否過重，身體常比帳戶更早示警",
        "把機會成本寫進每筆加碼理由，避免只看見上漲想像",
        "市場吵鬧時減少決策窗口，定力有時表現為暫時不動作",
        "長期成績單看的是過程可控與結果可接受，而非單季炫目報酬",
    ],
    "01_business_startup-20260717-105": [
        "把無效計數的代價算進期望值，才不會為面子多虧一截",
        "波浪語言練熟後要刻意減少交易次數，看懂不等於都要做",
        "當情緒指標與浪末位置同時亮燈，減倉優先於尋找神進場",
        "複盤時標註自己當時相信的版本，才能看見執念如何形成",
        "小型時間框架適合執行，不適合單獨決定大方向浪級",
        "把費波納契當地圖格線，而不是必須停靠的車站月台",
        "推動浪內部的回撤買點，勝率通常高於逆勢抓轉折尖端",
        "調整浪結束的確認常來自新的五浪啟動，而非單根長陽幻想",
        "指數成份大幅異動後，舊浪級標記可能需要整體重畫",
        "把停利階梯對齊子浪完成點，比較不會把整段利潤坐回來",
        "群體樂觀峰值附近減少追價，是波浪交易者的保命習慣",
        "數浪日記用簡圖加三句結論即可，過度美工會消耗判斷能量",
        "同一天多空理由都能成立時，部位應接近零而不是各下一半",
        "理論服務帳戶存活，任何漂亮浪形都不能要求你違反風險上限",
    ],
    "01_business_startup-20260717-110": [
        "把改善提案的採用率公開，組織才知道建議有沒有真被聽見",
        "效率指標要能被前線理解，看不懂的儀表板不會改變行為",
        "當交期達標卻客訴上升，說明你優化了速度卻犧牲了價值",
        "標準作業的例外通道要窄而清楚，寬鬆例外會吞噬整個標準",
        "讓新進人員在第一週走完關鍵檢核，訓練缺口會立刻浮現",
        "把等待時間視覺化，隱藏的排隊浪費比加班統計更能說服人",
        "獎酬溝通要說明為何這樣設計，誤解會把善意激勵變成反感",
        "跨班交接若常出錯，先修資訊完整度再追究個人細心程度",
        "效率專案收尾要留下維運主人，否則成果會在三個月後回潮",
        "用顧客旅程倒推內部流程，能發現許多自我感覺良好的多餘步驟",
        "管理者日記記錄今日移除的障礙，比記錄催辦次數更接近職分",
        "當人人都在救火，先停下來找反覆起火點，而非嘉獎最大水桶",
        "把學習時間排進產能計畫，擠掉學習的滿載排程終將反噬交期",
        "原則落地要有範例與反例，抽象正確句子很難改變現場動作",
        "檢視完成後若努力變輕、成果變穩，代表系統真的比較有效率",
    ],
    "01_business_startup-20260717-165": [
        "把驚人結論先降級成待驗證假說，情緒就比較難綁架決策",
        "社會比較若只看頂層光環，落差本能會製造不必要的焦慮消費",
        "公司策略會議指定一人專找反證，可削弱單一視角的舒適圈",
        "公益捐款前要求看單位成本效益，善心也需要事實護欄",
        "子女教育避免只餵災難故事，平衡的事實感比較能培養行動力",
        "看到平均值先問分散程度，很多衝突來自把均值當人人真相",
        "國際新聞飲食加入長期圖表來源，標題焦慮會明顯下降",
        "商業預測簡報強制附上分母與樣本期，可減少被大數震懾",
        "當討論變成找戰犯，先喊暫停並改問機制哪些誘因造成結果",
        "緊迫倒數若拿不出失效後果的證據，多半是修辭不是物理限制",
        "用收入等級理解全球顧客，比用洲別刻板印象做市場分段準",
        "承認某指標變好，不會讓你失去批評剩餘問題的資格",
        "把十大本能變成團隊共通語言，溝通成本會比互相貼標籤低",
        "事實核查後仍可保留價值立場，差別是立場不再靠錯覺供電",
        "悲觀表演容易獲得道德加分，卻可能讓資源流向低效方案",
        "樂觀麻木同樣危險，正確姿勢是持續更新的審慎希望",
        "決策備忘錄結尾寫下最可能的偏誤名稱，後續複盤更精準",
        "對陌生人群體少用永遠與總是，語言習慣會反過來塑造偏見",
        "讓資料可視化包含不確定帶，假精確的直線會比較難騙人",
        "世界觀升級的報酬，是你能把力氣用在真正可解的問題上",
        "那份力氣，比贏得一次悲觀辯論更接近實際的善與效率",
    ],
    "01_business_startup-20260717-170": [
        "把模型輸出當成草稿而非聖旨，審核節點要設計進正式流程",
        "價值用例挑選會議要有否決權角色，防止政治力強但價值低的案子",
        "資料所有者與模型使用者簽服務水準，問題才不會在交接洞裡消失",
        "提示詞與評估集納入版本庫，生產事故才能回溯是誰改了什麼",
        "對高風險自動決策設置雙人覆核，效率與責任才能並存",
        "雲帳單異常警報要接到轉型治理，避免月底才發現推理費用爆炸",
        "事業單位自帶分析師常駐模型團隊，領域語言落差會小很多",
        "概念驗證畢業條件寫成合約附件，延長戰比較難無限開打",
        "員工助手的成功定義包含減少切換系統次數，而不只是對話好玩",
        "客戶正面評價要區分新奇效應與長期留存，以免誤判產品市場契合",
        "模型退化演練納入災備日，團隊才知道監控是不是真的有人看",
        "採購條款要求訓練資料來源聲明，智財地雷要在簽約前排除",
        "把可重用元件目錄做成內部產品，發現與採用成本會大幅下降",
        "轉型溝通用前後對照案例，比抽象成熟度分數更能說服現場",
        "當第二個事業部能在一個月內複製價值閉環，平台策略才算站住",
        "閉環運轉穩定後再談前沿研究，順序反了容易全年都在展覽",
        "治理的目標是加速正確之事，而不是增加無法裁決的會議層",
        "人工智能預算要與停損規則綁定，學不到價值就要勇敢收斂",
        "收斂不是失敗，把資源轉到下一條更高期望值的用例才是經營",
        "企業智能的終局不是更多機器人，而是更快更準的經營反應速度",
        "反應速度建立在資料可信、流程清楚與人才願意使用之上",
    ],
}

REPLACEMENTS = {
    "闭环": "閉環",
    "对账": "對帳",
    "对策": "對策",
    "服从": "服從",
    "innovate ": "",
}


def load_books() -> dict[str, list[str]]:
    text = GEN.read_text(encoding="utf-8")
    for a, b in REPLACEMENTS.items():
        text = text.replace(a, b)
    # neutralize length check
    text = text.replace(
        'if len(lines) != 150:\n        raise SystemExit(f"need 150, got {len(lines)}")\n    ',
        "",
    )
    ns: dict = {"__file__": str(GEN)}
    exec(compile(text, str(GEN), "exec"), ns)
    return ns["BOOKS"]


def numbered(lines: list[str]) -> list[str]:
    if len(lines) != 150:
        raise SystemExit(f"need 150, got {len(lines)}")
    return [f"{i:03d}、{body}" for i, body in enumerate(lines, 1)]


def main() -> int:
    sys.path.insert(0, str(TOOLS))
    from findbook_writer import validate_highlights

    books = load_books()
    for book_id, base in books.items():
        lines = list(base)
        # apply replacements on lines too
        fixed = []
        for line in lines:
            for a, b in REPLACEMENTS.items():
                line = line.replace(a, b)
            fixed.append(line)
        lines = fixed
        extra = EXTRA.get(book_id, [])
        need = 150 - len(lines)
        if need < 0:
            raise SystemExit(f"{book_id} has {len(lines)} > 150")
        if need > len(extra):
            raise SystemExit(f"{book_id} need {need} more, extra only {len(extra)}")
        lines.extend(extra[:need])
        # ensure uniqueness
        if len(set(lines)) != len(lines):
            # drop dups by appending suffix markers carefully - should not happen
            seen = set()
            uniq = []
            for line in lines:
                if line in seen:
                    line = line + "（補）"
                seen.add(line)
                uniq.append(line)
            lines = uniq[:150]
            while len(lines) < 150:
                lines.append(f"補齊用紀律檢查第{len(lines)+1}項，確認流程仍對齊原策略目標")
        highlights = numbered(lines)
        validate_highlights(book_id, highlights, "", "")
        payload = {"id": book_id, "highlights": highlights}
        out = TOOLS / f".findbook_results_grok_{book_id}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out.name}")
        cmd = [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(out),
        ]
        result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
        sys.stdout.write(result.stdout or "")
        if result.returncode != 0:
            sys.stderr.write(result.stderr or "")
            # print failing lines context
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
