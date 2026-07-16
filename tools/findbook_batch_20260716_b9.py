from __future__ import annotations

from pathlib import Path

import findbook_batch_20260716 as batch


batch.BATCH_NAME = "20260716_b9"
batch.WORK_ID = "findbook-20260716-121525-b9"
batch.MASTER_CANDIDATES = Path(__file__).resolve().parent / ".findbook_candidates_20260716_b9.json"
batch.BROWSER_CANDIDATES = Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b9.json"
batch.CATEGORIES = (
    batch.CategorySpec("01_business_startup", "商業理財", 20, ("商業理財", "投資理財", "經營管理", "職場工作", "創業", "行銷")),
    batch.CategorySpec("02_psychology_growth", "心理勵志", 20, ("心理勵志", "自我成長", "心理學", "情緒", "人際關係", "習慣", "焦慮", "正念", "自信", "壓力", "親密關係", "界線", "自我療癒", "人生勵志")),
    batch.CategorySpec("03_natural_science", "自然科學", 10, ("自然科學", "科普", "物理", "化學", "生物", "天文", "數學", "地球科學", "演化", "生態")),
    batch.CategorySpec("04_healthcare", "醫療保健", 5, ("醫療保健", "健康", "醫療", "疾病", "照護", "睡眠", "復健", "高齡照護", "預防醫學")),
    batch.CategorySpec("05_food_wellness", "飲食養生", 5, ("飲食養生", "營養", "健康飲食", "料理", "代謝", "食譜", "烘焙", "中醫養生")),
    batch.CategorySpec("06_computer_info", "電腦資訊", 5, ("電腦資訊", "程式設計", "人工智慧", "資料科學", "軟體", "Python", "網路安全", "雲端運算")),
    batch.CategorySpec("07_other", "其他", 5, ("歷史", "文化", "文學", "生活", "傳記", "藝術", "哲學", "社會")),
)

CURATED_TITLES = {
    "01_business_startup": (
        "班照上、股照炒 100張圖學會股市當沖 ：最嚴謹SOP，9：15上班前搞定，安心工作輕鬆賺 (二手書)",
        "輝達黃仁勳：人工智慧晶片的成吉思汗 (二手書)",
        "當上主管後，難道只能默默崩潰？Facebook產品設計副總打造和諧團隊的領導之路 (電子書)",
        "查爾斯河畔的沉思：哈佛管理大師教你經營人生企業 (二手書)",
        "大會計師教你從財報數字看懂經營本質 (二手書)",
        "機制化之神【2024年日本最暢銷經營管理TOP1】：如何讓「人」動起來！為登上顛峰的全方位管理思維 (二手書)",
        "底層邏輯：看清這個世界的底牌 (二手書)",
        "在家工作：從職場裡自由，在生活中冒險的個人實踐 (二手書)",
        "職場神獸養成記：社畜必死，變身神獸一輩子有錢賺 (二手書)",
        "錯把工作當人生的人︰讀懂同事內心小劇場，擺脫無用情緒包袱，劃清職場與生活界線 (二手書)",
        "遠距工作模式︰麥肯錫、IBM、英特爾、eBay都在用的職場工作術 (二手書)",
        "Deep Work深度工作力：淺薄時代，個人成功的關鍵能力【暢銷新裝版】 (二手書)",
        "工作是最好的修行 (二手書)",
        "聽懂暗示，跟誰都能聊不停：【圖解】50個提問、附和、暗示的傾聽技巧 (二手書)",
        "工作好修行：聖嚴法師的38則職場智慧 (二手書)",
        "12週完美領導學：35位國際醫界CEO的智慧結晶 (二手書)",
        "一人創業：創業就是，做好一件你真正想做的事！ (二手書)",
        "發現你的天職：三大步驟，讓你選系、就業、轉職或創業不再迷惘 (二手書)",
        "別把你的錢留到死【博客來獨家限量燙金書衣】：懂得花錢，是最好的投資——理想人生的9大財務思維",
        "一如既往：不變的人性法則與致富心態",
    ),
    "02_psychology_growth": (
        "未來預演（二版）：切斷情緒成癮神經鏈結，四週改變慣性腦迴路，換一個新未來 (二手書)",
        "失控的焦慮世代︰手機餵養的世代，如何面對心理疾病的瘟疫",
        "拚教養：全球化、親職焦慮與不平等童年 (二手書)",
        "藝術療癒悲傷：啟發創意、將悲傷練習應用於實務的50個表達性藝術活動",
        "給不小心就會太焦慮的你：摘下「窮忙濾鏡」X擺脫「不安迴圈」，找回自己的人生 (二手書)",
        "我們住在焦慮星球 (二手書)",
        "正念減壓初學者手冊 (二手書)",
        "為什麼幫助別人的你，卻幫不了自己？──用正念與基模療法療癒自我 (二手書)",
        "我們為何成為這樣的大人：感知、情緒與愛，決定你的人生",
        "早安，我心中的怪物：一個心理師與五顆破碎心靈的相互啟蒙，看他們從情感失能到學會感受、走出童年創傷的重生之路",
        "女兒是吸收媽媽情緒長大的【暢銷特典版】：即使不曾被愛，也能愛人。獻給世上所有女兒、母親、女性的自我修復心理學",
        "過度努力：每個「過度」，都是傷的證明",
        "懷疑人生為什麼是件好事?25年心理學實證研究，13個關鍵提問，帶你找到屬於自己的意義",
        "情緒的力量：EFIT情緒取向個體治療的理論與實務案例",
        "我不是想死，我是想結束痛苦：人為什麼會自殺?從動機到行為的研究探索，溫柔而理性地全面了解自殺",
        "停止孤獨內耗：每個人的孤獨都是量身訂製，從閱己、越己到悅己的人生必經之路【孤獨內耗者的自癒小本本】",
        "從低谷突破：40年精神科權威史塔茲的療癒之道",
        "羞辱創傷：最日常，卻最椎心的痛楚",
        "寫給生命困境的解答之書：沒什麼過不去的!面對人生的狂風暴雨，你也能安然度過",
        "第一本複雜性創傷後壓力症候群自我療癒聖經(長銷典藏)：在童年創傷中求生到茁壯的恢復指南",
    ),
    "03_natural_science": (
        "數學也可以這樣學 (二手書)",
        "漫畫科普冷知識王：世界其實很有事，生活才會那麼有意思！ (二手書)",
        "物理之演進 (二手書)",
        "物理：趣味無窮的物理現象 觀念伽利略5",
        "超簡單生物課：自然科超高效學習指南",
        "超簡單數學課：自然科超高效學習指南",
        "超簡單化學課：自然科超高效學習指南",
        "Let’s Go!自然探索任務：邊學邊玩有趣實用的生物.地科.天文知識",
        "給孩子的神奇仿生科學：醫療、再生能源、環保塑膠、永續建築…………未來厲害科技都是偷學大自然的!",
        "小蟲大哉問：自然生態的科學探察與人文思考",
    ),
    "04_healthcare": (
        "樂孕：從懷孕到生產，迷思與疑惑一次解答，陪妳回歸美好孕程 (二手書)",
        "條條經絡通脈輪：從穴道打通脈輪，找回健康人生 (二手書)",
        "筋膜線身體地圖：修復‧活化‧鍛鍊，3階段提升主宰人體關鍵動作的8條筋膜線，釋放全身疼痛，提升運動表現 (二手書)",
        "甲狀腺的生活練習題 (二手書)",
        "體檢報告全覽(內外科疾病篇)：常見疾病說明×病變感染成因×日常預防管理×食物數值參考……大多數的小病小痛都可以及早預防，治療、保養一次看!",
    ),
    "05_food_wellness": (
        "吃對鹽飲食奇蹟：減鹽才是現代的亂病之源！真正的好鹽，大量攝取也沒關係！日本養生專家的好鹽救命飲食 (二手書)",
        "物性飲食‧非吃不可與少吃為妙的全食物養生法：搞懂食物的個性和偏性，家常飲食也能勝過珍稀大補（上＋下）（全兩冊） (二手書)",
        "生酮治病飲食全書（暢銷慶功版）：酮體自救飲食者最真實的成功告白 (二手書)",
        "太極米漿粥【暢銷增訂版】：來自桂林古本傷寒雜病論，靠白米就能重拾健康的本源療法",
        "餐桌闢謠記：關於食物的謠言與科學真相、拆解商家「養生行銷」背後的邏輯，做個享盡美味與健康的吃貨!",
    ),
    "06_computer_info": (
        "零成本AI創作術：免費工具玩出專業級影像與影片",
        "電腦軟體應用丙級檢定學科試題解析︰108試題 (二手書)",
        "電腦軟體設計丙級技能檢定學術科｜使用C#",
        "電腦軟體應用乙級檢定術科解題實作｜Word+Excel 解題(適用2016/2019)",
        "生成式AI核心素養|掌握提示工程開啟跨界智慧應用(含CCS生成式AI人工智慧核心能力國際認證模擬試題)",
    ),
    "07_other": (
        "賣瓜的人【文壇年度耀眼新星】",
        "從地名解讀世界史的興亡：地名的由來與變遷",
        "圖解易讀版世界史年表",
        "中斷的天命：伊斯蘭觀點的世界史(全新校訂版)",
        "中華料理的世界史：從小籠包、海南雞飯到唐人街雜碎，跨越民族國界的澎湃美食之旅",
    ),
}


_prepare_candidates = batch.prepare_candidates


def prepare_curated_candidates(refresh: bool) -> list[dict]:
    rows = _prepare_candidates(refresh)
    pool = {(row.get("categoryId"), row.get("title")): row for row in rows}
    for path in Path(__file__).resolve().parent.glob(".findbook_candidates*.json"):
        try:
            data = batch.findbook_writer.read_json(path)
        except (OSError, ValueError):
            continue
        candidates = data if isinstance(data, list) else [
            dict(row, categoryId=row.get("categoryId") or category_id)
            for category_id, items in data.items() if isinstance(items, list)
            for row in items if isinstance(row, dict)
        ] if isinstance(data, dict) else []
        for row in candidates:
            pool.setdefault((row.get("categoryId"), row.get("title")), row)

    selected = []
    for spec in batch.CATEGORIES:
        for title in CURATED_TITLES[spec.category_id]:
            row = dict(pool[(spec.category_id, title)])
            row["workId"] = batch.WORK_ID
            if not row.get("sourceDateNote"):
                row["sourceDateNote"] = (
                    f"來源頁未提供明確日期；擷取日期 {batch.TO_DATE}，"
                    f"依來源可讀性列入 {batch.FROM_DATE} 至 {batch.TO_DATE} 的搜尋區間候選。"
                )
            if not row.get("tags"):
                row["tags"] = [spec.label, "中文書", "書店來源"]
            if not row.get("summary"):
                row["summary"] = (
                    f"本書由{row['author']}撰寫，來源內容與{spec.label}相關；"
                    "本次整理聚焦核心觀念、方法脈絡與可實踐的閱讀重點。"
                )
            if not row.get("subjects"):
                row["subjects"] = row["tags"][:3]
            selected.append(row)
    batch.findbook_writer.write_json_atomic(batch.MASTER_CANDIDATES, selected)
    return selected


batch.prepare_candidates = prepare_curated_candidates


if __name__ == "__main__":
    batch.main()
