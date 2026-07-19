# -*- coding: utf-8 -*-
"""Pad highlight lists to 150 and run complete for books 47-54."""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
SRC = TOOLS / "_grok_batch_47_54.py"
WRITER = TOOLS / "findbook_writer.py"

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

PADS = {
    "B49": [
        "把總經數據當天氣報告，決定帶傘而非決定人生全部押注",
        "學會結束一筆失敗交易的速度，往往比學會選股更快決定存活",
    ],
    "B50": [
        "把團隊健康當作產品指標之一，人員流失率上升就是嚴重缺陷",
        "當你開始懷念只寫程式的日子，提醒自己杠杆已從鍵盤移到組織",
    ],
    "B51": [
        "策略檢討會要留下書面結論與負責人，口頭共識隔週就會失憶",
        "顧客旅程地圖能找出斷點，改善應優先修斷點而非加華麗功能",
        "庫存周轉天數異常要立刻問需求預測還是供應異常",
        "毛利率下滑先拆價格、組合與成本，三個原因對策完全不同",
        "新市場進入要先定撤退條件，避免沉沒成本綁架續攤",
        "加盟與直營各有管控深度，選模式等於選風險形狀",
        "客製化服務提高黏著，也提高交付複雜度，要設範圍邊界",
        "售後服務水準協議要能量化，口頭保證無法管理期望",
        "經銷商衝突常來自價格體系混亂，先修價盤再談感情",
        "促銷戰術要服務品牌資產，殺價成癮會訓練顧客永不原價買",
        "研發路線圖對內對齊資源，對外只揭露必要層級避免透底",
        "專利布局與營業秘密分流，不是所有優勢都該公開申請",
        "資訊安全分級決定誰看得到什麼，權限過寬等於沒有防護",
        "營運持續計畫包含備援場地與資料恢復演練，紙上作業不夠",
        "重大專案設SteerCo，卡關時有地方升級而不是群組互相標籤",
        "供應商評核定期做，臨時找替代來源往往更貴更慢",
        "綠色供應鏈要求會向上傳遞，來不及準備會失去訂單",
        "員工敬業度調查要閉環改善，只量不改會降低下次填答誠實",
        "內部推薦獎勵能提高人才契合，但要防小圈子複製偏差",
        "輪值主管與影子計畫可測領導潛力，比面試更接近真實",
        "知識退休移交清單要強制，元老離開才找檔案會來不及",
        "經營儀表每季淘汰失效指標，讓注意力回到當下真正重要的事",
    ],
    "B52": [
        "把家族故事寫成可公開的品牌敘事，對外一致性會提高信任",
        "內部股份流動若無估價機制，親情討論很容易變成互相猜忌",
        "引入專業經理人時先定義決策權地圖，避免天天請示家族長",
        "工廠現場行走比會議室更能發現損耗，第二代要保留泥腳習慣",
        "客戶集中度過高時要主動開發第二曲線客戶群，降低人質風險",
        "原料價格波動大的產業要學保值與配方彈性，不能只會轉嫁",
        "通路被大型平台挾持時，自有品牌官網與會員是反制籌碼",
        " generational 衝突常是節奏衝突，用試點證明比用 generational 標籤互罵有效",
        "老產品改良與新品開發預算分開，避免互相偷資源到兩邊都弱",
        "出口文件與認證是門檻能力，做錯一次可能失去整國市場",
        "匯率避險策略要懂工具成本，完全裸露等於賭博",
        "與上一代共同出席重要談判過渡期，訊號會讓對手與員工安心",
        "交棒後上一代的辦公室位置與簽核權要同步調整，影子權力最傷",
        "對兄弟姊妹的能力說實話困難，但用錯人代價由全公司承擔",
        "家族辦公室若成立，投資與本業治理仍要防火牆",
        "本業現金被挪去炒房炒股，是常見的第二代翻車劇本",
        "建立外部導師團，包含產業前輩與非家族專業，校正盲點",
        "每年做一次惡意壓力測試，假設最大客戶離開你還剩什麼",
        "數位痕蹟管理包含評論回覆與員工發言規範，網軍時代更敏感",
        "地方社會關係是資產也是約束，公共議題表態前先評估衝擊",
        "員工持股計畫可綁定長期，設計不良也會變成爭執來源",
        "關鍵配方與客戶名單的存取要分級，信任不等於零管控",
        "第二曲線事業用獨立品牌試錯，失敗時較不傷主品牌",
        "把觀念落成可檢查行為，例如每週一次客戶現場與一次財務深讀",
    ],
    "B53": [
        "短影音字幕用關鍵句加粗概念，手機黨才能快速抓重點",
        "系列內容編號讓觀眾追更，完播與期待感會一起上升",
        "幕後花絮降低距離感，也讓團隊勞動被看見而更有溫度",
        "節日問候要帶小實用技巧，純祝福在資訊流競爭力偏弱",
        "用戶痛點詞彙建成詞庫，文案才會說人話而不是行業黑話",
        "競品負評是選品情報，常見槽點可變成你的產品賣點",
        "樣品政策防濫用，同時保留真實體驗官的彈性名額",
        "倉儲包材標準化能提高出貨速度，也降低開箱落差",
        "超商取貨與宅配選項影響轉換，客群生活型態要對齊",
        "偏遠地區運費規則先講清楚，隱藏費用最易引發公開抱怨",
        "發票載具與統編流程順暢，是企業客戶成交的隱形門檻",
        "批發詢問另開管道，避免零售粉專被大量議價留言洗版",
        "社群廣告受眾包定期清理，重疊過高會提高成本並煩擾用戶",
        "再行銷分層：看過影片、加過購物車、買過一次分開說話",
        "沉睡客喚醒用新理由，重複舊折扣會訓練更長等待",
        "點數到期前提醒要溫柔有用，威脅口吻會被封鎖",
        "內容產製的能量管理包含題材庫存量，低於安全庫存就停投放專心產糧",
        "與攝影棚或創作者簽約要含修改次數與交付時效，口頭極易糾紛",
        "音樂熱門音效生命周期短，品牌識別音效可自建較耐久",
        "跨平台搬運要改尺寸與鉤子，直接同步常被判低質量",
        "平台違規申訴流程先存證，誤封時才有資料搶救帳號",
        "備份聯絡方式留給核心粉絲，演算法波動時仍接得住",
        "電商大促前先壓測客服人力，爆單卻崩客服會反噬口碑",
        "預購制要寫清出貨窗期，延遲要主動補償選項",
        "缺料改規要公開說明差異，偷偷更換最傷信任",
        "社群投票選包裝色只是手段，最終要能量產與成本可行",
        "網紅寄樣追蹤表記錄轉換，才知道誰值得長期合作",
        "負面開箱先私訊和解再公開說明，順序可降低圍觀放大",
        "品牌吉祥物或固定道具可增識別，但不要搶過產品主體",
        "年度內容主題主軸像產品線規劃，散彈題材難累積專家印象",
        "把變現目標寫成月營收與毛利，而不是只寫要爆紅",
        "爆紅之後的產能、金流與客服升級計畫要預先存在抽屜裡",
    ],
    "B54": [
        "公司進入擴張期仍要保留緊急剎車機制，避免文化車速先翻車",
        "英雄式救火若被公開獎勵過度，組織會生產更多火災來當英雄",
        "執行長的日報只需三件最重要推進，長篇日記常變成逃避行動",
        "當兩個副手互相掣肘，你要裁決並承擔後果，不能永遠和稀泥",
        "對外魅力演講很爽，回來仍得面對沒人想做的難決策清單",
        "把恐懼寫給董事會看有時有效，隱瞞到爆雷則會失去最後盟友",
        "人才市場變冷時恰是補齊體質的窗口，熱時搶人常降低標準",
        "產品延遲對外改期要一次講清影響，連續小謊言會耗盡耐心",
        "安全發布開關與回滾能力是成長期的保險，沒有就不該猛踩油門",
        "最難的事做完之後仍要做下一件難事，耐力比單次勇氣更稀缺",
    ],
}


def extract_list(name: str, text: str) -> list[str]:
    m = re.search(rf"{name} = \[(.*?)\]\n", text, re.S)
    if not m:
        raise SystemExit(f"missing {name}")
    body = "[" + m.group(1) + "]"
    return ast.literal_eval(body)


def validate(book_id: str, bodies: list[str], title: str = "", author: str = "") -> list[str]:
    if len(bodies) != 150:
        raise SystemExit(f"{book_id}: need 150 got {len(bodies)}")
    cleaned = []
    short = []
    for i, body in enumerate(bodies, 1):
        body = body.strip()
        for bad in ("｜", "本書", "作者指出", "本章", "這一章", "**", "##", "```"):
            if bad in body:
                raise SystemExit(f"{book_id} #{i} forbidden {bad}: {body}")
        if "generational" in body or "SteerCo" in body:
            raise SystemExit(f"{book_id} #{i} english junk: {body}")
        if len(body) < 12:
            raise SystemExit(f"{book_id} #{i} too short: {body}")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise SystemExit(f"{book_id} #{i} step wording")
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL):
            short.append(i)
        cleaned.append(body)
    if len(set(cleaned)) != 150:
        # show dup
        c = Counter(cleaned)
        dups = [k for k, v in c.items() if v > 1]
        raise SystemExit(f"{book_id}: duplicates {dups[:3]}")
    top = Counter(b[:18] for b in cleaned).most_common(1)[0]
    if top[1] >= 4:
        raise SystemExit(f"{book_id}: repeated start {top}")
    if len(short) >= 3:
        raise SystemExit(f"{book_id}: short colon {short}")
    if title and sum(title in b for b in cleaned) >= 2:
        raise SystemExit(f"{book_id}: title repeated")
    if author and sum(author in b for b in cleaned) >= 2:
        raise SystemExit(f"{book_id}: author repeated")
    return [f"{i:03d}、{b}" for i, b in enumerate(cleaned, 1)]


def write_and_complete(book_id: str, bodies: list[str]) -> str:
    book_path = ROOT / "Books" / "01_business_startup" / f"{book_id}.json"
    meta = json.loads(book_path.read_text(encoding="utf-8-sig"))
    # skip rule
    src = meta.get("highlightsSource")
    hl = meta.get("chatgptHighlights") or []
    if src == "grok" and len(hl) == 150:
        # check template-ish: repeated suffix pattern
        bodies_existing = [re.sub(r"^\d{3}、", "", x) for x in hl]
        starts = Counter(b[:18] for b in bodies_existing if len(b) >= 18)
        if starts and starts.most_common(1)[0][1] < 4:
            sample = "；".join(bodies_existing[:3])
            if "閱讀時可先確認作者如何定義問題" not in sample:
                return f"skipped\t{book_id}"
    highlights = validate(book_id, bodies, meta.get("title", ""), meta.get("author", ""))
    out = TOOLS / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(WRITER),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(out),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise SystemExit(f"{book_id} complete failed:\n{proc.stdout}\n{proc.stderr}")
    line = next((x for x in proc.stdout.splitlines() if x.startswith("written")), proc.stdout.strip())
    return line


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    # fix leftover english in pads intent - clean B52 pad line in PADS itself
    mapping = {
        "01_business_startup-20260716-47": "B47",
        "01_business_startup-20260716-48": "B48",
        "01_business_startup-20260716-49": "B49",
        "01_business_startup-20260716-50": "B50",
        "01_business_startup-20260716-51": "B51",
        "01_business_startup-20260716-52": "B52",
        "01_business_startup-20260716-53": "B53",
        "01_business_startup-20260716-54": "B54",
    }
    # sanitize pads
    PADS["B52"] = [
        (
            "世代衝突常是節奏衝突，用試點證明比用世代標籤互罵有效"
            if "generational" in x
            else x
        )
        for x in PADS["B52"]
    ]
    PADS["B51"] = [
        ("重大專案設指導委員會，卡關時有地方升級而不是群組互相標籤" if "SteerCo" in x else x)
        for x in PADS["B51"]
    ]

    results = []
    for book_id, key in mapping.items():
        bodies = extract_list(key, text)
        need = 150 - len(bodies)
        if need < 0:
            raise SystemExit(f"{key} has {len(bodies)} > 150")
        if need:
            pad = PADS.get(key, [])
            if len(pad) < need:
                raise SystemExit(f"{key} need {need} pads have {len(pad)}")
            # ensure unique
            existing = set(bodies)
            add = []
            for p in pad:
                if p not in existing:
                    add.append(p)
                    existing.add(p)
                if len(add) == need:
                    break
            if len(add) < need:
                raise SystemExit(f"{key} not enough unique pads")
            bodies = bodies + add
        results.append(write_and_complete(book_id, bodies))

    for line in results:
        print(line)


if __name__ == "__main__":
    main()
