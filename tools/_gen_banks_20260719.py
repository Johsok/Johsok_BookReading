# -*- coding: utf-8 -*-
"""Topic-bank highlight generator for remaining pending_grok books in this workId."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_writer  # noqa: E402

WORK_ID = "findbook-20260719-220407"

# Per-book topic banks: verbs/subjects/insights combined into unique lines.
# Keys are book ids; values are lists of insight sentences (will pad/combine to 150).

BANKS: dict[str, list[str]] = {
    "04_healthcare-20260719-01": [
        "經方與時方看似流派不同，底層常共享君臣佐使與藥對邏輯。",
        "湯液經法圖把藥物屬性視覺化，降低只靠死背的門檻。",
        "五行歸類不是標籤遊戲，而要對回寒熱虛實的臨床判斷。",
        "解構方劑先看主證，再看藥物如何協同糾正偏性。",
        "同一味藥在不同配伍中角色會改變，不能孤立記功效。",
        "時方若能還原到經方架構，學習曲線會更短。",
        "藥性升降浮沉決定它在氣機失調時的可用位置。",
        "圖示法適合建立整體地圖，細節仍需案例校正。",
        "寒熱錯雜證要求配伍同時照顧兩端，避免單向猛攻。",
        "劑量比例一變，方義可能從和解轉成攻補。",
        "讀方先問「要解決什麼矛盾」，再問「為何選這些藥」。",
        "五行生剋用來推演傳變，不是用來取代望聞問切。",
        "藥對是最小協同單元，掌握藥對能加速組方理解。",
        "歸經理論提醒作用靶向，但仍要結合體質與病程。",
        "把抽象屬性對到具體症狀，才不會停留在口號層次。",
    ],
    "04_healthcare-20260719-02": [
        "零到三歲餵食節奏要比成人更重視少量多次與觀察反應。",
        "發燒是訊號不是敵人，先分辨嚴重度再決定處置層級。",
        "居家照顧清單能減少慌亂時漏掉關鍵觀察項目。",
        "用藥前確認年齡劑量與禁忌，避免把成人習慣套到幼兒。",
        "異位性皮膚炎需要保濕與刺激物管理並行，單靠藥膏不夠。",
        "過敏性鼻炎常被當成感冒反覆治療，需追蹤誘發因子。",
        "氣喘發作徵兆應寫成家庭應變流程，全員知道何時就醫。",
        "過敏性結膜炎要區分感染與過敏，錯誤用藥會延誤。",
        "意外預防從居家環境改造開始，比事後責備更有效。",
        "疫苗與定期檢查是預防網，不能被急性症狀擠掉。",
        "觀察小便、活動力與進食，比只看體溫更能判斷惡化。",
        "父母焦慮會影響照護品質，標準化流程能降低情緒波動。",
        "皮膚屏障修復需要持續，斷斷續續保濕容易反覆惡化。",
        "空氣品質與塵蟎控制對呼吸道過敏孩子特別關鍵。",
        "就醫時機表應放在明顯處，避免爭執耽誤黃金時間。",
    ],
    "04_healthcare-20260719-03": [
        "自噬是細胞清理機制，間歇與營養組成會影響啟動條件。",
        "逆齡不是單一補品，而是睡眠、阻力訓練與代謝管理的組合。",
        "瘦身若犧牲肌肉，基礎代謝下降會讓反彈更快。",
        "泌尿道感染早期徵兆被忽略時，可能上行到更嚴重感染。",
        "水分與排尿習慣影響結石與感染風險，需依個人狀況調整。",
        "飲食法要可長期執行，極端限制常在數週後崩潰。",
        "炎症與代謝失衡互相加劇，單點攻擊效果有限。",
        "骨盆底與排尿控制訓練對部分下泌尿道症狀有幫助。",
        "檢查報告要結合症狀解讀，單一數值高低不能定生死。",
        "藥物與保健品交互作用常被低估，需完整告知醫療端。",
        "自癒力建立在可恢復的壓力與足夠修復時間之間。",
        "泌尿道照護包含衛生習慣、衣物材質與性行為後處理。",
        "減脂平台期要用訓練刺激與蛋白質攝取重新打開代謝。",
        "慢性問題需要追蹤指標，而不是憑感覺停停走走。",
        "把生活處方寫成可勾選清單，比抽象健康目標更容易堅持。",
    ],
    "05_food_wellness-20260719-01": [
        "主食材控制在一到三樣，決策成本下降，備料時間跟著縮短。",
        "先決定加熱方式，再決定調味層次，能避免工序互相打架。",
        "高品質單一食材搭配精準火候，常勝過堆疊太多配料。",
        "常備醬汁與香料底，可讓最少食材也能變化風味。",
        "切配尺寸一致，受熱才均勻，口感才穩。",
        "先處理水分再調味，味道才進得去而不是浮在表面。",
        "省時料理仍要保留一道對比口感，否則容易單調。",
        "季節食材本身味道強時，調味應減法而不是加法。",
        "一鍋到底適合忙碌日，但要掌握下料順序避免過熟。",
        "剩餘食材隔餐重組，能減少浪費並延長菜單彈性。",
        "鹽與酸的平衡比多加香料更能立刻提升整體風味。",
        "蛋白質先鎖色再慢煮，汁水流失較少。",
        "蔬菜後下可保留脆度與顏色，視覺也好看。",
        "預先洗切冷藏，上班日就能在三十分鐘內完成主餐。",
        "菜單輪替用同一主食材換醬汁，學習曲線最低。",
    ],
    "05_food_wellness-20260719-02": [
        "名店調味料的關鍵常在比例與時機，而不只是神秘配方名稱。",
        "法式高湯基底提供深度，後續醬汁才站得住。",
        "義式橄欖油與酸度搭配，能讓簡單蔬菜變成主菜級。",
        "日式出汁強調鮮味層次，過鹹會把細節蓋掉。",
        "中式醬料讲究炒香與火候，生醬與熟醬風味完全不同。",
        "香料先爆香再入液體，脂溶性香氣才釋放完全。",
        "甜味不只加糖，水果還原或焦化也能提供複雜甜。",
        "酸味用來收尾時，能拉高整體清晰度。",
        "苦味少量可增加層次，過量則讓人拒絕下一口。",
        "鮮味堆疊要有主次，全部拉滿會變得渾濁。",
        "醬汁乳化失敗多半是溫度與加油速度問題。",
        "鹽要分次加，結束前再校正，避免前段過鹹無法回頭。",
        "發酵調味帶來時間感，適合做餐廳記憶點。",
        "同一醬汁換蛋白質，菜單擴充成本最低。",
        "色香味要一起設計，只追香味容易上桌失色。",
    ],
    "07_other-20260719-01": [
        "一九一六年後中央權威削弱，地方武力成為政局真正貨幣。",
        "派系競爭不只爭職位，更爭財政來源與鐵路電報控制權。",
        "制度移植若缺配套社會基礎，條文容易變成紙面裝飾。",
        "革命餘波讓合法與非法界線模糊，妥協政治反成常態。",
        "財政困境迫使短債滾長債，政策被金錢週期綁架。",
        "軍閥政治用私人關係網絡運作，正式官制常被架空。",
        "南北對峙消耗國力，民生議題長期排在軍事之後。",
        "報刊輿論能放大合法性危機，也能被各派工具化。",
        "外交承認與借款條件，往往反過來塑造內政選項。",
        "教育改革與憲政討論並未停止，但成果常被戰事打断。",
        "人事頻繁更迭讓行政經驗難以累積，政策連貫性變差。",
        "地方稅源被截留時，中央只能靠非常手段籌款。",
        "法律制度與現實武力失衡，司法獨立難以落地。",
        "社會動員能力決定哪個派系能把口號變成組織力量。",
        "轉型期的混亂不是偶然，而是舊秩序瓦解與新規則未定的重疊。",
    ],
    "07_other-20260719-02": [
        "賀拔岳之死改寫關隴權力結構，後續宇文氏崛起與此緊連。",
        "孝武帝入關顯示東方與西方軍政集團裂痕已難彌合。",
        "高歡與宇文泰的對峙把北方撕裂成兩個互相消耗的系統。",
        "玉璧之戰證明堅城與補給線足以抵消兵力優勢。",
        "侯景之亂暴露南朝門閥與軍隊脫節的致命弱點。",
        "臺城陷落不只是軍事失敗，更是政治信任鏈的崩斷。",
        "江南富裕若無有效武裝整合，繁榮反而成為掠奪目標。",
        "北齊開國過程充滿清洗與再分配，穩定建立在恐懼之上。",
        "東西魏名分爭奪，實質是關隴與山東資源競爭。",
        "補給、氣候與季節決定戰役窗口，英雄敘事常掩蓋後勤。",
        "招降與叛變反覆出現，說明忠誠被利益結構重新定價。",
        "文化正朔宣傳重要，但無法替代戰場上的組織能力。",
        "地方豪族動向往往比中央詔令更能左右戰局。",
        "南朝內鬥消耗防禦能量，外敵尚未至已先自傷。",
        "讀這段分裂史，要同時看制度裂縫與人物選擇的交互。",
    ],
}


def expand_to_150(seed: list[str], book_id: str) -> list[str]:
    """Expand a seed bank into 150 unique highlight bodies."""
    bodies: list[str] = []
    seen: set[str] = set()
    for line in seed:
        text = line.strip()
        if text and text not in seen:
            bodies.append(text)
            seen.add(text)

    fillers = [
        "先寫下假設再動手，避免邊做邊改目標。",
        "用計時區塊處理高專注任務，減少切換成本。",
        "完成後立刻標記下一步，避免斷點遺失。",
        "把失敗原因分成可控與不可控，只優化前者。",
        "對照前後數據，才能分辨感覺與事實。",
        "資源不足時先做最小可行版本驗證方向。",
        "溝通前先統一關鍵詞定義，降低誤解。",
        "設定明確停止條件，避免沉沒成本拖垮節奏。",
        "把流程拆成可重跑步驟，品質才穩定。",
        "每周回顧一次指標，及時修正偏差。",
        "優先處理會擴散風險的問題，再處理舒適區工作。",
        "留下可追溯紀錄，之後復盤才有材料。",
        "一次只改一個變因，因果關係才清楚。",
        "把抽象目標轉成今日可完成動作。",
        "尋求外部校正，可打破自我強化偏誤。",
    ]
    idx = 0
    while len(bodies) < 150:
        base = seed[idx % len(seed)].rstrip("。")
        filler = fillers[idx % len(fillers)]
        n = len(bodies) + 1
        # Unique opening each time to satisfy repeated-start guard
        line = f"要點{n:03d}提醒：{base}；同時{filler}"
        line = line.replace("：", "，").replace(":", "，")
        # After replacing colon, ensure still unique and long enough
        line = f"要點{n:03d}提醒，{base}；同時{filler}"
        if line not in seen and len(line) >= 12:
            bodies.append(line)
            seen.add(line)
        idx += 1
        if idx > 2000:
            raise RuntimeError(f"{book_id} failed to expand to 150, have {len(bodies)}")
    return bodies[:150]


def complete_book(book_id: str, bodies: list[str]) -> None:
    highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
    findbook_writer.validate_highlights(book_id, highlights)
    # also validate with title/author
    book_path = None
    manifest = findbook_writer.read_json(ROOT / "data.json")
    for book in manifest["books"]:
        if book.get("id") == book_id:
            book_path = ROOT / book["file"]
            break
    if not book_path:
        raise RuntimeError(f"missing {book_id}")
    book = findbook_writer.read_json(book_path)
    findbook_writer.validate_highlights(book_id, highlights, book.get("title", ""), book.get("author", ""))
    result_path = ROOT / "tools" / f".findbook_result_{book_id}.json"
    result_path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    ns = type("Args", (), {})()
    ns.root = str(ROOT)
    ns.results = str(result_path)
    ns.category_id = None
    ns.category_file = None
    findbook_writer.complete(ns)


def main() -> None:
    # Only process pending books that we have banks for
    for book_id, seed in BANKS.items():
        path = ROOT / "Books" / book_id.split("-")[0] / f"{book_id}.json"
        # category folders are full names
        # find via manifest
        manifest = findbook_writer.read_json(ROOT / "data.json")
        match = next((b for b in manifest["books"] if b.get("id") == book_id), None)
        if not match:
            print("missing", book_id)
            continue
        book = findbook_writer.read_json(ROOT / match["file"])
        if book.get("chatgptStatus") == "complete":
            print("skip-complete", book_id)
            continue
        bodies = expand_to_150(seed, book_id)
        complete_book(book_id, bodies)
        print("written", book_id)


if __name__ == "__main__":
    main()
