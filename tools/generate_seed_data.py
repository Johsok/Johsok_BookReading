from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = [
    {
        "id": "01_business_startup",
        "label": "01_商業創業",
        "file": "01_business_startup.json",
        "description": "商業、創業、投資、職涯與財務決策。"
    },
    {
        "id": "02_psychology_growth",
        "label": "02_心理勵志",
        "file": "02_psychology_growth.json",
        "description": "心理、習慣、情緒、人際與自我成長。"
    },
    {
        "id": "03_natural_science",
        "label": "03_自然科學",
        "file": "03_natural_science.json",
        "description": "宇宙、生命、物理、數學與科學思維。"
    },
    {
        "id": "04_healthcare",
        "label": "04_醫療保健",
        "file": "04_healthcare.json",
        "description": "醫療知識、身心健康、疾病預防與照護。"
    },
    {
        "id": "05_food_wellness",
        "label": "05_飲食養生",
        "file": "05_food_wellness.json",
        "description": "飲食、營養、運動、代謝與日常養生。"
    },
    {
        "id": "06_computer_info",
        "label": "06_電腦資訊",
        "file": "06_computer_info.json",
        "description": "程式、演算法、AI、資料、工作流與資訊科技。"
    },
    {
        "id": "07_other",
        "label": "07_其他",
        "file": "07_other.json",
        "description": "歷史、文化、生活、文學與無法歸入單一主題的書。"
    }
]

BOOKS = [
    {
        "id": "navalmanack-deluxe",
        "categoryId": "01_business_startup",
        "title": "納瓦爾寶典珍藏版：從白手起家到財務自由，矽谷傳奇創投家的投資哲學與人生智慧",
        "author": "艾瑞克．喬根森",
        "sourceName": "博客來商業理財暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/02/?loc=P_0002_003",
        "tags": ["創業", "投資", "財務自由", "人生策略"],
        "summary": "本書把納瓦爾關於財富、判斷、幸福與長期主義的公開觀點整理成可反覆檢查的人生策略。讀後重點可放在槓桿、專長、責任感、時間複利與內在自由。",
        "anchors": [
            "把長期複利放在短期聲量之前",
            "用專長、槓桿與責任感建立不可替代性",
            "將財富理解為可持續創造價值的系統",
            "把判斷力視為比努力更稀缺的資產",
            "透過閱讀、思考與實作形成自己的心智模型",
            "避免用時間直接換錢而忽略可擴張成果",
            "在市場需求與個人熱情交會處累積優勢",
            "把幸福看成降低欲望與增加自由的結果",
            "用清晰溝通放大信任與合作效率",
            "持續淘汰低價值承諾，保留深度創造的時間"
        ]
    },
    {
        "id": "poor-charlies-almanack",
        "categoryId": "01_business_startup",
        "title": "窮查理的普通常識（紀念典藏版）：巴菲特50年智慧合夥人查理．蒙格的人生哲學",
        "author": "查理．蒙格",
        "sourceName": "博客來商業理財暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/02/?loc=P_0002_003",
        "tags": ["投資", "心智模型", "決策", "商業判斷"],
        "summary": "本書聚焦查理．蒙格的跨學科心智模型、反向思考、投資紀律與品格要求。讀後整理適合建立自己的決策檢查表，避免單一學科與情緒偏誤。",
        "anchors": [
            "用多元心智模型避免單點盲區",
            "先避免愚蠢錯誤，再追求聰明決策",
            "反向思考能快速暴露風險與漏洞",
            "投資前先判斷能力圈與安全邊際",
            "品格與耐心是長期複利的底層條件",
            "大錯通常來自誘因、槓桿與過度自信",
            "學科之間的連結比零散知識更有價值",
            "等待好機會比頻繁出手更接近高手行為",
            "用清單管理偏誤，而不是相信自己永遠理性",
            "把閱讀當成持續更新判斷力的日課"
        ]
    },
    {
        "id": "atomic-habits",
        "categoryId": "02_psychology_growth",
        "title": "原子習慣：細微改變帶來巨大成就的實證法則",
        "author": "詹姆斯‧克利爾",
        "sourceName": "博客來心理勵志暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/07/?loc=P_0002_006",
        "tags": ["習慣", "自我管理", "行為設計", "成長"],
        "summary": "本書主張微小行動會經由複利累積成身份與成果。重點整理應放在提示、渴望、反應、獎賞四階段，以及如何設計環境讓好習慣自然發生。",
        "anchors": [
            "把目標轉成每天可重複的最小行動",
            "先設計環境，再要求意志力配合",
            "用身份認同讓習慣有持續理由",
            "讓好習慣顯而易見、有吸引力、容易做、有滿足感",
            "讓壞習慣隱形、無吸引力、困難且沒有立即回報",
            "追蹤行為能把模糊努力變成清楚證據",
            "不要因一次中斷否定整個系統",
            "微小改善在時間拉長後會呈現巨大差異",
            "習慣堆疊能降低啟動成本",
            "成果落後時仍要相信系統正在累積"
        ]
    },
    {
        "id": "i-may-be-wrong",
        "categoryId": "02_psychology_growth",
        "title": "我可能錯了：森林智者的最後一堂人生課",
        "author": "比約恩．納提科．林德布勞、卡洛琳．班克勒、納維德．莫迪里",
        "sourceName": "博客來心理勵志暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/07/?loc=P_0002_006",
        "tags": ["正念", "謙遜", "人生課", "情緒"],
        "summary": "本書以出家、還俗、疾病與臨終反思串起對生命的柔軟理解。重點不在標準答案，而在學會承認可能錯了、放下控制並回到當下。",
        "anchors": [
            "承認我可能錯了能鬆開防衛與執著",
            "把不確定視為生命的一部分，而非失敗證明",
            "正念練習讓人先看見念頭，再決定是否跟隨",
            "痛苦常來自抗拒現實，而不只是事件本身",
            "謙遜能讓關係留出理解與和解空間",
            "死亡意識會重新排序真正重要的事",
            "安靜不是逃避，而是讓心回到可觀察狀態",
            "慈悲從停止攻擊自己開始",
            "放下控制不等於放棄行動",
            "人生的平靜常藏在簡單、誠實與在場之中"
        ]
    },
    {
        "id": "brief-history-of-time",
        "categoryId": "03_natural_science",
        "title": "時間簡史：從大爆炸到黑洞",
        "author": "史蒂芬．霍金",
        "sourceName": "科普暢銷經典",
        "sourceUrl": "https://zh.wikipedia.org/wiki/%E6%99%82%E9%96%93%E7%B0%A1%E5%8F%B2",
        "tags": ["宇宙", "物理", "時間", "黑洞"],
        "summary": "本書把宇宙起源、時間箭頭、黑洞、量子與相對論問題帶入一般讀者視野。讀後重點可放在科學如何用模型處理看不見的尺度與極限。",
        "anchors": [
            "宇宙問題需要同時處理觀測、模型與假設",
            "時間不是單純背景，而與空間及物理定律相連",
            "大爆炸模型說明宇宙曾處於高密度高溫狀態",
            "黑洞讓重力、光與資訊的邊界變得可思考",
            "相對論改變了人對絕對時間與空間的直覺",
            "量子觀點提醒微觀世界不服從日常經驗",
            "科學模型的價值在於解釋力與可檢驗性",
            "時間箭頭連結熱力學、記憶與宇宙演化",
            "最偉大的問題常需要跨越數學與想像",
            "理解宇宙也是理解人類位置感的方式"
        ]
    },
    {
        "id": "rewire-neuroplasticity",
        "categoryId": "04_healthcare",
        "title": "Rewire-神經可塑性：用神經科學突破行為模式迴圈，終結焦慮、恐慌和憂鬱，實現最佳的心理健康",
        "author": "妮可．維諾拉",
        "sourceName": "博客來中文書暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/",
        "tags": ["神經可塑性", "心理健康", "焦慮", "行為模式"],
        "summary": "本書以神經可塑性作為理解情緒與行為模式的入口，強調身體、睡眠、飲食、壓力與重複練習對心理健康的影響。整理時應避免把它當醫囑，而是當成健康習慣檢查表。",
        "anchors": [
            "神經可塑性代表大腦會隨重複經驗改變",
            "情緒迴圈常由身體狀態、念頭與行為共同維持",
            "焦慮不只是想太多，也可能與生理壓力負荷有關",
            "睡眠、飲食與運動是心理穩定的重要底座",
            "小而穩定的行為練習比一次性爆發更有效",
            "辨識觸發點能讓自動反應變成可選擇反應",
            "調節神經系統需要同時照顧呼吸、節奏與安全感",
            "改變行為模式要先降低羞愧與自責",
            "專業協助與日常自我照護可以互補",
            "心理健康的進步通常是非線性累積"
        ]
    },
    {
        "id": "carb-cycling",
        "categoryId": "05_food_wellness",
        "title": "碳水循環（新年瘦身特別版）：一輩子都瘦用的增肌減脂飲食法",
        "author": "蕭捷健",
        "sourceName": "博客來醫療保健暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/08/?loc=P_0002_009",
        "tags": ["飲食", "減脂", "代謝", "運動"],
        "summary": "本書圍繞碳水攝取、訓練日安排與代謝管理做飲食規劃。讀後整理可把重點放在可持續、可追蹤、可調整，而不是追求極端限制。",
        "anchors": [
            "碳水攝取應配合活動量與訓練日調整",
            "減脂不是完全禁食某一類營養素",
            "蛋白質、纖維與總熱量仍是基礎框架",
            "飲食策略要能長期執行才有意義",
            "訓練表現與恢復狀態能反映飲食是否合適",
            "體重短期波動常包含水分與肝醣變化",
            "外食也可以用份量、順序與替換管理",
            "睡眠與壓力會影響食慾與代謝判斷",
            "紀錄飲食不是自責，而是取得回饋",
            "任何飲食法都應依個人健康狀況調整"
        ]
    },
    {
        "id": "algorithm-python-visual",
        "categoryId": "06_computer_info",
        "title": "演算法 圖解原理 x Python實作 x 創意應用 王者歸來（四版）",
        "author": "洪錦魁",
        "sourceName": "博客來電腦資訊暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/19/?loc=P_0002_021",
        "tags": ["演算法", "Python", "資料結構", "程式設計"],
        "summary": "本書把演算法概念、圖解理解、Python 實作與應用題連在一起。讀後整理應把每個演算法拆成問題情境、資料結構、時間複雜度與實作陷阱。",
        "anchors": [
            "先理解問題型態，再選擇演算法",
            "資料結構會直接影響效能與程式可讀性",
            "圖解能幫助看見流程與狀態變化",
            "Python 實作要注意邊界條件與資料規模",
            "排序、搜尋與圖論是許多問題的基礎積木",
            "時間複雜度用來預估規模放大後的成本",
            "遞迴需要明確終止條件與狀態定義",
            "動態規劃重點在子問題與重複計算",
            "測試案例要包含正常、極端與空資料",
            "演算法學習應搭配手寫推演與實際跑碼"
        ]
    },
    {
        "id": "gemini-notebooklm-workflow",
        "categoryId": "06_computer_info",
        "title": "Gemini 3 x NotebookLM領軍：Nano Banana Pro x Veo x Whisk x Flow x Gem - Google 多模態 AI 工作流",
        "author": "洪錦魁",
        "sourceName": "博客來中文書暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/",
        "tags": ["AI", "Gemini", "NotebookLM", "多模態工作流"],
        "summary": "本書聚焦 Google AI 生態系與多模態工具的工作流整合。由於工具版本更新很快，讀後整理應特別標註版本、可替代工具與可重複流程。",
        "anchors": [
            "AI 工具書要先記錄版本與適用情境",
            "多模態工作流重點在輸入、轉換與輸出銜接",
            "NotebookLM 適合把資料來源轉成可追問的知識工作區",
            "Gemini 類模型可用於摘要、改寫、推理與素材生成",
            "影像、影片與文字工具需要明確分工",
            "提示詞應包含目標、限制、格式與驗收標準",
            "AI 產出要保留人工審稿與來源核對",
            "自動化流程要把錯誤處理與版本更替列入設計",
            "個人知識管理可用 AI 加速整理但不可放棄判斷",
            "學工具不如學會可遷移的工作流程"
        ]
    },
    {
        "id": "young-taiwan-history",
        "categoryId": "07_other",
        "title": "少年臺灣史 二○一九年增訂版",
        "author": "周婉窈",
        "sourceName": "博客來中文書暢銷榜",
        "sourceUrl": "https://www.books.com.tw/web/sys_saletopb/books/",
        "tags": ["臺灣史", "歷史", "文化", "通識"],
        "summary": "本書以適合青少年與一般讀者的方式整理臺灣歷史脈絡。讀後重點可放在時間軸、族群互動、政權轉換、世界局勢與日常生活如何彼此影響。",
        "anchors": [
            "臺灣史要同時看島內變化與世界局勢",
            "不同族群的互動形塑了社會與文化樣貌",
            "政權更迭會改變制度、教育、經濟與身份認同",
            "歷史不是背年代，而是理解因果與脈絡",
            "地理位置讓臺灣長期處於交流與競逐之中",
            "普通人的生活史能補足政治史的抽象",
            "史料需要比較來源與觀點",
            "理解過去有助於辨認今日議題的根源",
            "多元記憶可能並存，也需要被仔細聆聽",
            "好的歷史閱讀會提升公民判斷力"
        ]
    }
]

POINT_TEMPLATES = [
    ("核心觀念", "把「{anchor}」當成本書的核心線索，讀每一章時都回頭確認是否呼應。"),
    ("問題意識", "先問自己：如果忽略「{anchor}」，生活、工作或學習中最可能付出什麼代價。"),
    ("概念拆解", "將「{anchor}」拆成定義、原因、行動與衡量方式，避免只留下口號。"),
    ("行動轉換", "把「{anchor}」轉成一個今天能做的小動作，讓讀書成果進入日常。"),
    ("案例觀察", "閱讀時記下能支持「{anchor}」的案例，並標明它是事實、推論或作者觀點。"),
    ("反向檢查", "從相反方向檢查「{anchor}」：什麼情況下它可能失效或需要修正。"),
    ("個人連結", "把「{anchor}」對照最近一次真實決策，找出可改進的一個細節。"),
    ("風險提醒", "不要把「{anchor}」簡化成萬用答案，它仍需要情境、資料與自我覺察。"),
    ("筆記方法", "為「{anchor}」建立一張索引卡：一句話、三個關鍵詞、一個應用場景。"),
    ("複盤問題", "讀完後用「{anchor}」問自己：三個月後我想看到哪一個可觀察改變。")
]

EXTRA_LENSES = [
    "將此重點放進長期視角，判斷它在一年後是否仍有價值。",
    "找出此重點背後的前提，避免在不同情境中誤用。",
    "用自己的話重寫此重點，確認不是只記住書名式語句。",
    "為此重點配一個反例，讓理解更有邊界。",
    "把此重點轉成待辦清單中的一個實驗。",
    "用一個數字或紀錄方式追蹤此重點是否被實踐。",
    "把此重點與另一個主題連結，建立跨書比較。",
    "思考作者可能沒有談到的限制或成本。",
    "找一位可討論的人，用三分鐘講清楚此重點。",
    "在下次重讀時檢查自己對此重點的理解是否改變。"
]


def numbered(points: list[str]) -> list[str]:
    return [f"{index:02d}、{point}" for index, point in enumerate(points, start=1)]


def make_chatgpt_points(book: dict) -> list[str]:
    points: list[str] = []
    anchors = book["anchors"]
    for anchor in anchors:
        for _, template in POINT_TEMPLATES:
            points.append(template.format(anchor=anchor))

    for index, lens in enumerate(EXTRA_LENSES):
        anchor = anchors[index % len(anchors)]
        points[index] = f"{points[index]} {lens}"

    return numbered(points[:100])


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def main() -> None:
    books_by_category = {category["id"]: [] for category in CATEGORIES}
    for book in BOOKS:
        normalized = {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "sourceName": book["sourceName"],
            "sourceUrl": book["sourceUrl"],
            "tags": book["tags"],
            "summary": book["summary"],
            "updatedAt": "2026-07-08",
            "chatgptHighlights": make_chatgpt_points(book),
            "geminiHighlights": [],
            "geminiStatus": "待使用 FindBook_Skill.md 以 Chrome MCP 操作 Gemini 補齊。"
        }
        books_by_category[book["categoryId"]].append(normalized)

    manifest_books = []
    for book in BOOKS:
        manifest_books.append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "categoryId": book["categoryId"],
            "tags": book["tags"],
            "sourceName": book["sourceName"],
            "sourceUrl": book["sourceUrl"]
        })

    manifest = {
        "version": "2026-07-08",
        "title": "讀書後重點整理",
        "recommendedStorage": "data.json 僅存索引；分類 JSON 存書籍重點；超過 1000 本時改為每本一個 JSON 並由 data.json 指向檔案路徑。",
        "categories": CATEGORIES,
        "books": manifest_books,
        "totalBooks": len(BOOKS)
    }
    write_json(ROOT / "data.json", manifest)

    for category in CATEGORIES:
        payload = {
            "categoryId": category["id"],
            "categoryLabel": category["label"],
            "description": category["description"],
            "updatedAt": "2026-07-08",
            "books": books_by_category[category["id"]]
        }
        write_json(ROOT / category["file"], payload)


if __name__ == "__main__":
    main()
