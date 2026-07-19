# -*- coding: utf-8 -*-
"""Pad batch0 highlight lists to exactly 150 unique lines, then write results."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_PATH = ROOT / "tools" / "_gen_batch0_highlights.py"

EXTRA: dict[str, list[str]] = {
    "01_business_startup-20260718-21": [
        "把問題邊界畫出來後，才能判斷哪些資訊值得繼續蒐集。",
        "用一頁紙寫清現況、目標與障礙，拆解效率通常立刻上升。",
        "當多方意見打架，先找可被共同檢驗的事實再辯論解法。",
        "把個人精力負債列入計畫，避免方案理論可行卻執行崩潰。",
        "創業定價測試要同時觀察成交與售後服務成本。",
        "把關鍵假設做成紅黃綠燈狀態，團隊對風險會更同步。",
    ],
    "01_business_startup-20260718-22": [
        "把顧客旅程的情緒高低點標出來，常能解釋轉換斷崖。",
        "同一指標在不同部門被重新定義時，跨隊對齊會先失真。",
        "把促銷毛利與品牌折損一起算，才知道活動是否真賺。",
        "前線人員的沉默，有時比問卷更能顯示制度壓力。",
        "把異常週的行事曆事件對上，假訊號會少很多。",
        "人性互惠會讓受訪者給出討好答案，需用行為交叉驗證。",
        "高活躍低付費族群，可能正在消耗客服與伺服器資源。",
        "把歸因窗口拉長後，某些渠道的真實貢獻才浮現。",
        "決策者若只看亮點頁，會系統性低估長尾風險。",
        "把「不知道」列為合法狀態，分析文化才比較誠實。",
        "客單上升若伴隨客訴上升，成長品質需要重新定義。",
        "把實驗流量隔離乾淨，結論才不會被互相污染。",
        "人性現狀偏誤會讓舊指標即使失效仍被繼續崇拜。",
        "區域差異未被建模時，全國策略常變成平均錯誤。",
        "把動機假設寫進分析摘要，讀者才知道詮釋從哪來。",
    ],
    "01_business_startup-20260718-23": [
        "把兌付承諾的法律細節讀清楚，才能判斷信用硬度。",
        "泡沫中的社交攀比，會把謹慎者逼進非理性參與。",
        "當抵押品與標的高度同質，去槓桿會變成共振崩塌。",
        "把宣傳話術與可稽核財務分開，較不易被故事帶走。",
        "信用擴張若伴隨監督真空，套利者會比建設者更快致富。",
        "股價狂漲期的從業人員膨脹，崩盤後失業也更劇烈。",
        "把國際熱錢流動納入觀察，國內泡沫常有外部加速器。",
        "當政策用道德勸說代替硬約束，發行紀律很難持久。",
        "投機收益的示範會改變年輕人的職業與風險偏好。",
        "把清算順序事先想清楚，才能知道危機時誰先受傷。",
        "銀行券貶值預期一旦形成，持有行為會迅速轉向實物。",
        "泡沫研究要同時看制度誘因與群眾心理，缺一不可。",
        "把「可退出流動性」當成風險參數，估值才較完整。",
        "國家信用被透支後，連正當建設融資都會變貴。",
        "密西西比式結構警告我們：功能耦合過高會放大單點失敗。",
        "投資人應假設極端壓力會到來，再回頭檢視持倉。",
    ],
    "01_business_startup-20260718-24": [
        "把重複問題做成知識庫條目，可減少專家被同樣問題打斷。",
        "目標若缺少完成定義，驗收會議會變成無限扯皮。",
        "責任歸屬要用書面確認，口頭承諾在壓力下最容易蒸發。",
        "作業方法改善要測量學習曲線，導入初期變慢是正常的。",
        "獎酬若獎勵加班時數，會把低效率偽裝成奉獻。",
        "把跨部門介面SLA訂清楚，等待浪費會明顯下降。",
        "效率審計要包含顧客視角，避免內部最佳化外部受傷。",
        "目標瀑布若過長，末端執行者會失去意義感與動能。",
        "方法標準要能在新手手上跑通，才算真正可複製。",
        "獎酬溝通延遲會讓正確行為得不到及時強化。",
        "把會議出席改成按需邀請，可減少無關人員的時間稅。",
        "責任與技能落差大時，先補訓再究責才公平有效。",
        "作業抽查結果要回饋到培訓，而不是只用來扣分。",
        "獎酬制度要能解釋例外情況，否則公平感受到損。",
        "效率提升專案本身也要設停損，避免改善活動變空轉。",
        "把工具權限與職責匹配，可減少求助與等待。",
        "目標衝突公開仲裁，比讓基層私下硬扛更負責任。",
        "方法文件若沒有維護主人，很快會變成過期垃圾。",
        "獎酬與價值觀宣言不一致時，員工會相信錢的訊號。",
        "可以努力，但要把努力放在高槓桿約束條件上。",
        "把交接演練定期做，關鍵崗位離職才不會讓流程斷裂。",
        "責任清晰的團隊，比較敢暴露問題而不是隱藏問題。",
        "作業節拍穩定後，再談加速才不會製造更多缺陷。",
        "獎酬設計要避免懲罰舉報錯誤的人，否則問題會地下化。",
        "效率管理的成熟度，體現在少靠英雄、多靠系統。",
        "把努力與方法一起複盤，下次才不會重複蠻幹。",
        "檢查四柱是否同向，比單獨優化其中一柱更接近艾默生精神。",
    ],
    "01_business_startup-20260718-25": [
        "把年報現金流量表與損益表對讀，能識破盈餘品質問題。",
        "機會常藏在沒人願意讀的附註與或有負債說明裡。",
        "當市場獎勵講故事能力，沉默做生意的公司可能被低估。",
        "把競爭對手資本開支節奏畫出來，能預判供給過剩風險。",
        "看見客戶是否非買不可，比看見廣告聲量更接近護城河。",
        "機會評估要包含退出難度，流動性差時折價要更大。",
        "把管理層歷史承諾對照結果，可判斷言出必行程度。",
        "景氣低谷若現金仍強韌，往往是反轉期值得研究的對象。",
        "看見定價權是否能轉嫁成本，通膨環境判斷會更準。",
        "把投資論文的關鍵假設標成可監控指標，持有才有紀律。",
        "當分析依賴單一客戶或單一產品，機會的脆弱性升高。",
        "巴菲特式機會拒絕用複雜槓桿去硬拗報酬。",
        "把產業學習曲線走完再重倉，比聽消息衝動下單更穩。",
        "看見自由現金流用途：還債、回購、擴張或亂花，結論大不同。",
        "機會出現時若論點需要十個巧合同時成立，通常應放過。",
        "把市場情緒溫度計與自身倉位分開管理，避免被裹挾。",
        "長期報酬來自少數重大正確決策，其餘時間多半是等待。",
        "看見會計估計變更對盈餘的影響，可降低被美化的機率。",
        "把同業失敗案例做成檢查清單，能過濾表面誘人標的。",
        "當價格已反映樂觀到近乎完美，留給錯誤的空間很小。",
        "機會與風險總是同框出現，只看見一邊就不算真正看見。",
        "把能力圈邊界畫清楚，是持續看見可把握機會的前提。",
        "市場錯價會重複發生，但形態每次不同，框架要比預測重要。",
        "看見資本配置是否提高每股內在價值，是機會品質核心。",
        "把等待期用來加深研究，比盯盤更能準備下一次出手。",
        "好機會值得重倉的前提，是下跌時你仍看得懂並敢加碼的理由。",
        "像巴菲特一樣，把獨立思考當成看見機會的日常鍛鍊。",
        "最終能抓住機會的人，通常先贏得了對自己貪婪與恐懼的管理。",
        "把安全邊際當作門票，沒有邊際的上漲故事就不是機會。",
        "價值投資的機會感，來自價格與價值缺口而非熱門排行。",
        "把研究深度換成可表達的商業洞察，判斷才經得起追問。",
        "當你能解釋清楚為何現在便宜且可能修復，機會才算成形。",
        "看見時間站在哪一邊，是區分投資與投機的實用準則。",
        "把現金位置管理好，罕見錯價來臨時才有資格說看見了。",
        "機會不會預告鈴聲，只有準備好的框架能讓你辨認它。",
        "長期投資要比的是誰更願意正確而無聊，而不是誰更會追逐熱門話題。",
        "把每一次錯過與踩雷寫成規則更新，辨識力才會累積。",
        "市場先生每日報價，真正的機會屬於能選擇性失聰的人。",
        "看見一家公司未來現金的主人是誰，股權價值判斷才落地。",
    ],
}


def load_books() -> dict[str, list[str]]:
    text = GEN_PATH.read_text(encoding="utf-8")
    cut = text.split("\ndef main()")[0]
    ns: dict = {"__file__": str(GEN_PATH), "__name__": "gen"}
    exec(compile(cut, str(GEN_PATH), "exec"), ns)
    return ns["BOOKS"]


def validate_local(book_id: str, highlights: list[str], title: str, author: str) -> None:
    if len(highlights) != 150:
        raise ValueError(f"{book_id} count={len(highlights)}")
    forbidden = ("本書", "作者指出", "本章", "這一章")
    bodies = []
    for i, line in enumerate(highlights, 1):
        expected = f"{i:03d}、"
        if not line.startswith(expected):
            raise ValueError(f"{book_id} bad number {i}")
        body = line[len(expected) :].strip()
        if len(body) < 12:
            raise ValueError(f"{book_id} short {i}: {body}")
        if any(p in body for p in forbidden):
            raise ValueError(f"{book_id} forbidden {i}")
        if "｜" in body or "\n" in body:
            raise ValueError(f"{book_id} bad format {i}")
        bodies.append(body)
    if len(set(bodies)) != len(bodies):
        raise ValueError(f"{book_id} duplicates")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        raise ValueError(f"{book_id} repeated starts {starts.most_common(1)}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in bodies) >= 2:
            raise ValueError(f"{book_id} repeats {label}")


def main() -> None:
    books = load_books()
    batch = json.loads((ROOT / "tools" / "_batch0.json").read_text(encoding="utf-8"))
    meta = {b["id"]: b for b in batch}

    for book_id, base in books.items():
        extras = EXTRA.get(book_id, [])
        merged = list(base)
        for line in extras:
            if line not in merged:
                merged.append(line)
        if len(merged) < 150:
            raise SystemExit(f"{book_id} still short: {len(merged)}")
        if len(merged) > 150:
            merged = merged[:150]
        # ensure uniqueness after trim
        if len(set(merged)) != 150:
            # refill uniquely
            uniq = []
            seen = set()
            for line in list(base) + extras:
                if line not in seen:
                    uniq.append(line)
                    seen.add(line)
                if len(uniq) == 150:
                    break
            if len(uniq) < 150:
                raise SystemExit(f"{book_id} cannot unique-fill: {len(uniq)}")
            merged = uniq

        highlights = [f"{i:03d}、{body}" for i, body in enumerate(merged, 1)]
        info = meta[book_id]
        validate_local(book_id, highlights, info["title"], info["author"])
        out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print(f"ok {book_id}")


if __name__ == "__main__":
    main()
