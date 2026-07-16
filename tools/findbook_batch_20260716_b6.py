from __future__ import annotations

from pathlib import Path

import findbook_batch_20260716_b5 as previous
import findbook_batch_20260716_b2 as base


batch = previous.batch
batch.BATCH_NAME = "20260716_b6"
batch.WORK_ID = "findbook-20260716-082632-b6"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260716_b6.json"
)
batch.BROWSER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b6.json"
)

LIST_URLS = {
    "01_business_startup": "https://www.books.com.tw/web/sys_nbmidme/books/02",
    "02_psychology_growth": "https://www.books.com.tw/web/sys_nbmidme/books/07",
    "03_natural_science": "https://www.books.com.tw/web/sys_nbmidme/books/06",
    "04_healthcare": "https://www.books.com.tw/web/sys_nbmidme/books/08",
    "05_food_wellness": "https://www.books.com.tw/web/sys_nbmidme/books/09",
    "06_computer_info": "https://www.books.com.tw/web/sys_nbmidme/books/19",
    "07_other": "https://www.books.com.tw/web/sys_nbmidme/books/04",
}


def curated_book(
    category_id: str,
    label: str,
    title: str,
    author: str,
    source: str,
    published: str,
    subjects: tuple[str, ...],
) -> dict:
    url = (
        f"https://www.books.com.tw/products/{source}"
        if source and not source.startswith("http")
        else source or LIST_URLS[category_id]
    )
    row = base.curated_book(
        category_id, label, title, author, url, published or "來源未標示", subjects
    )
    if url == LIST_URLS[category_id]:
        row["sourceName"] = f"博客來中文書新書列表－{label}"
    if not published:
        row["sourceDateNote"] = (
            f"博客來公開新書列表未提供明確出版日期；擷取日期 {batch.TO_DATE}，"
            f"依新書列表收錄狀態列入 {batch.FROM_DATE} 至 {batch.TO_DATE} 的搜尋區間候選。"
        )
    return row


CURATED_BOOKS = (
    curated_book("01_business_startup", "商業理財", "打造永續共好生態圈：來自創業、創新與社會行動者的20則行動觀點", "沈勤譽、詹茹惠", "", "2026-01-22", ("永續創業", "社會創新", "生態圈")),
    curated_book("01_business_startup", "商業理財", "我不是幸運，只是很早學會選擇：30歲前買房、財務自由、身心快樂，平凡女子的富貴體質養成計畫〖限量作者親簽版〗", "冰蹦拉", "", "2026-01-15", ("財務自由", "買房", "人生選擇")),
    curated_book("01_business_startup", "商業理財", "超越機率思考：聰明人為什麼都用計算機做決定?史上最強生活統計決策書", "哈伊姆・夏皮拉", "", "2026-01-14", ("機率", "統計", "決策")),
    curated_book("01_business_startup", "商業理財", "思考致富(全新修訂/註釋/完整權威版)：富裕和動盪時代的完整財富祕密", "拿破崙．希爾、羅斯．康威爾", "", "2026-01-14", ("財富思維", "目標", "行動")),
    curated_book("01_business_startup", "商業理財", "共感的力量：善用體貼為影響力的臺灣式EQ領導學", "近藤弥生子", "", "2026-01-13", ("領導", "共感", "影響力")),
    curated_book("01_business_startup", "商業理財", "讓生活不再空轉的自我管理術：落實六大心法、建構自律系統，輕鬆實現理想人生!", "車純純", "", "2026-01-13", ("自我管理", "自律", "目標實現")),
    curated_book("01_business_startup", "商業理財", "比特幣新手入門：加密貨幣投資教學Step by Step", "呂哲宇（Joey Lu）", "", "2026-01-09", ("比特幣", "加密貨幣", "投資入門")),
    curated_book("01_business_startup", "商業理財", "實用租稅規劃與財富傳承", "廖勇誠", "", "2026-01-09", ("租稅", "財富傳承", "資產規劃")),
    curated_book("01_business_startup", "商業理財", "價值覺醒：股人阿勳的進化思維，破解「便宜不漲」的真相，告別賣飛人生", "股人阿勳", "", "2026-01-08", ("價值投資", "選股", "投資心理")),
    curated_book("01_business_startup", "商業理財", "有錢人不一樣的財富印記2：啟動你的全方位富裕劇本", "金．卡洛斯", "", "2026-01-08", ("財富", "金錢信念", "行動計畫")),
    curated_book("01_business_startup", "商業理財", "圖解透視未來：回顧關鍵轉折，邁向財富自由(第二版)", "錢世傑", "", "2026-01-08", ("趨勢", "財富自由", "資產配置")),
    curated_book("01_business_startup", "商業理財", "主角模式：從「我得這樣」到「我可以選擇」，影響7500萬人的成長祕密", "樊登", "", "2026-01-08", ("選擇", "成長", "行動")),
    curated_book("01_business_startup", "商業理財", "人際關係中的情緒科學：降低誤讀、改善對話、提升連結品質", "吳載昶", "", "2026-01-07", ("情緒", "溝通", "人際關係")),
    curated_book("01_business_startup", "商業理財", "設計你的財務幸福：5個行動，打造不焦慮金錢的未來", "洪哲茗、邱茂恒", "", "2026-01-07", ("財務規劃", "金錢焦慮", "幸福")),
    curated_book("01_business_startup", "商業理財", "巴菲特給股東的投資理財報告", "林郁主編", "", "2026-01-07", ("巴菲特", "投資", "股東信")),
    curated_book("01_business_startup", "商業理財", "5年內打造1億資產的逆襲方程式：普通上班族也能做到，無痛複製4大投資策略，突破薪水牢籠、資產放大100倍!", "kenmo（湘南投資讀書會）", "", "2026-01-07", ("資產成長", "投資策略", "財務自由")),
    curated_book("01_business_startup", "商業理財", "懂一點心理學， 讓說話產生正面效應(熱銷再版)", "張心悅", "", "2026-01-20", ("溝通", "心理學", "說服")),
    curated_book("01_business_startup", "商業理財", "讓人無法拒絕的說服術", "平田貴子", "", "2026-01-17", ("說服", "談判", "溝通")),
    curated_book("01_business_startup", "商業理財", "尋找黑天鵝：加密貨幣時代的散戶生存致富指南", "高培勛、林紘宇", "", "2026-01-16", ("加密貨幣", "風險", "投資")),
    curated_book("01_business_startup", "商業理財", "臺灣邁向淨零未來：碳捕存推動策略與實踐", "吳閔鈺、周彥祺、周芷瑄、尤晴韻、林軒如、許中駿、陳彥豪、陳映蓉、陳柏誼", "", "2026-01-09", ("淨零", "碳捕存", "永續策略")),

    curated_book("02_psychology_growth", "心理勵志", "面對老，我有備而來", "簡靜惠", "0011037765", "2025-11-27", ("老化", "準備", "生命態度")),
    curated_book("02_psychology_growth", "心理勵志", "日日放鬆：100種安頓身心的入口", "胡展誥", "0011037766", "2025-11-27", ("放鬆", "身心安頓", "日常練習")),
    curated_book("02_psychology_growth", "心理勵志", "身體記憶52講(重拾記憶版)", "蔣勳", "0011037772", "2025-11-27", ("身體記憶", "生命經驗", "感受")),
    curated_book("02_psychology_growth", "心理勵志", "卡內基夫人說女人〖暢銷勵志經典〗：全球超過60個國家，2000多所教育機構指定必讀!", "桃樂絲．卡內基", "0011037404", "2025-11-27", ("女性成長", "自信", "人際關係")),
    curated_book("02_psychology_growth", "心理勵志", "如果死期將至：最後的道別不是再見，而是另一個世界見", "四宮敏章", "0011037821", "2025-11-27", ("死亡", "道別", "生命教育")),
    curated_book("02_psychology_growth", "心理勵志", "停止情緒內耗的39個練習：日本人氣心理師破解內耗源頭，教你快速告別自我批判和焦慮", "池田由芽", "0011037577", "2025-11-27", ("情緒內耗", "自我批判", "焦慮")),
    curated_book("02_psychology_growth", "心理勵志", "重新發明自己的工作：不心累、不瞎忙的無限職涯地圖", "林浩賢Terence Lam", "0011037751", "2025-11-27", ("職涯", "工作設計", "自我探索")),
    curated_book("02_psychology_growth", "心理勵志", "松浦彌太郎寫給凌晨五點的你： 不想一個人、不想上班、覺得人生進度落後了……美學大師的微建議，關於生活中那些不美的事", "松浦彌太郎", "0011037150", "2025-11-26", ("生活建議", "孤獨", "自我接納")),
    curated_book("02_psychology_growth", "心理勵志", "你的所有不安，時間一吹就散：99%你擔心的事，放著不管就會消失", "高恩美", "0011037220", "2025-11-26", ("不安", "焦慮", "時間觀")),
    curated_book("02_psychology_growth", "心理勵志", "八十歲，還能跑跳碰：歲月會增心不必老", "葉金川", "0011037257", "2025-11-26", ("熟齡", "活力", "健康心態")),
    curated_book("02_psychology_growth", "心理勵志", "彈性界限：結合腦科學x認知心理學x日常練習，建立心靈防護罩", "金賢", "0011037480", "2025-11-26", ("界限", "腦科學", "心理韌性")),
    curated_book("02_psychology_growth", "心理勵志", "花甲男孩嬉遊記：六個朋友六十年的故事", "劉仲康、方力行、林俊希、蔣炳煜、郭英敏、陳振文", "0011037501", "2025-11-26", ("友情", "熟齡", "人生故事")),
    curated_book("02_psychology_growth", "心理勵志", "讓人生穩定快樂的心理學公式：用「擁有的>期望的」找回生活的平衡與快樂", "劉志軍", "0011037583", "2025-11-26", ("快樂", "期望", "心理平衡")),
    curated_book("02_psychology_growth", "心理勵志", "世界上最溫暖的內向人說明書：一定會是你的最後一本內向人書籍!獻給I人的人生使用說明!", "井上由香里", "0011037216", "2025-11-26", ("內向", "自我理解", "人際相處")),
    curated_book("02_psychology_growth", "心理勵志", "性侵害團體治療", "李靜宜、魏瑋柔", "0011037324", "2025-11-25", ("創傷", "團體治療", "復原")),
    curated_book("02_psychology_growth", "心理勵志", "沒有人等過我：兒少照護者的陪伴與生命紀事", "吳方芳", "0011036890", "2025-11-25", ("兒少照護", "陪伴", "生命紀事")),
    curated_book("02_psychology_growth", "心理勵志", "你不是破碎，而是入口：身心療癒師的身體療癒筆記", "趙耕樂", "0011037256", "2025-11-20", ("身體療癒", "創傷", "自我修復")),
    curated_book("02_psychology_growth", "心理勵志", "想念的日子：給失去摯愛者的告別練習", "坂口幸弘、赤田ちづる", "0011036612", "2025-11-19", ("悲傷", "告別", "失落調適")),
    curated_book("02_psychology_growth", "心理勵志", "心理韌性：重建挫折復原力的132個強效練習大全", "琳達．格拉翰", "0011037178", "2025-11-19", ("心理韌性", "復原力", "練習")),
    curated_book("02_psychology_growth", "心理勵志", "一個人的武林：分享生命分享愛", "劉千瑤", "0011037297", "2025-11-19", ("生命故事", "愛", "自我成長")),

    curated_book("03_natural_science", "自然科學", "臺灣珍鳥重現：古爾德鳥類博物誌臺灣選集", "吳建龍、李政霖、林大利、林文宏、江勻楷、洪廣冀、約翰・古爾德、馮孟婕、黃瀚嶢", "", "2025-12-31", ("臺灣鳥類", "博物誌", "自然史")),
    curated_book("03_natural_science", "自然科學", "升級吧!大腦──激發大腦超能力，破解金魚腦、腦腐陷阱、演算法操控的祕密", "謝伯讓", "", "2025-12-30", ("大腦", "認知", "演算法")),
    curated_book("03_natural_science", "自然科學", "國家地理賞鳥指南", "諾亞．史崔克", "", "2025-12-30", ("賞鳥", "鳥類", "生態觀察")),
    curated_book("03_natural_science", "自然科學", "裸猿大逆襲，瘋狂人類進化史：裸露身體、渴望親密、追求忠誠……身體的每一寸都不是偶然，演化到底設下多少陷阱?", "史鈞", "", "2025-12-17", ("人類演化", "身體", "演化心理")),
    curated_book("03_natural_science", "自然科學", "隱世女畫家的自然手繪集：《金石昆蟲草木狀》花果篇", "（明）文俶", "", "2025-12-25", ("植物", "自然繪圖", "博物學")),
    curated_book("03_natural_science", "自然科學", "隱世女畫家的自然手繪集：《金石昆蟲草木狀》動物篇", "（明）文俶", "", "2025-12-25", ("動物", "自然繪圖", "博物學")),
    curated_book("03_natural_science", "自然科學", "隱世女畫家的自然手繪集：《金石昆蟲草木狀》藥草篇", "（明）文俶", "", "2025-12-25", ("藥草", "自然繪圖", "博物學")),
    curated_book("03_natural_science", "自然科學", "全民防災教本(第1版)", "松井正雄、陳柏蒼", "", "2025-12-25", ("防災", "風險", "應變")),
    curated_book("03_natural_science", "自然科學", "精通物理(第1版)：情境化學習 力學、熱學、流體", "張慧貞", "", "2025-12-25", ("物理", "力學", "熱流學")),
    curated_book("03_natural_science", "自然科學", "紙上草木花實敷：從花果鋪陳的圖像中，看見明代植物知識的悄然流轉", "張鈁", "", "2025-12-24", ("植物知識", "圖像", "科學史")),

    curated_book("04_healthcare", "醫療保健", "藥師沒告訴你的50件事：你不可不知的居家用藥常識", "洪正憲", "0011041009", "2026-01-05", ("用藥安全", "藥物迷思", "健康常識")),
    curated_book("04_healthcare", "醫療保健", "原來都是濕氣惹的禍：讓中醫師帶你透過日常飲食調理、經絡穴位按摩、健康生活律動，從裡到外、按部就班徹底解決濕氣引起的身體病痛", "李志剛 醫師", "0011041148", "2026-01-01", ("中醫", "濕氣", "生活調理")),
    curated_book("04_healthcare", "醫療保健", "嬰幼兒常見疾病照護全書 ：從症狀觀察、正確處置到就醫指南，寫給所有新手爸媽的0～6歲安心速查圖解手冊", "野村さちい", "0011044911", "2026-02-10", ("兒科", "疾病照護", "就醫判斷")),
    curated_book("04_healthcare", "醫療保健", "追尋失落的漢醫｜暢銷增訂版｜經脈血壓計世界專利發明人、中西醫師郭育誠博士，引你窺見千年前漢醫AI系統，實現隔空把脈，診斷於千里之外", "郭育誠", "0011041575", "2026-01-10", ("漢醫", "脈診", "中西醫整合")),
    curated_book("04_healthcare", "醫療保健", "動力取向精神醫學：臨床應用與實務 [第五版] *根據DSM-5最新改版", "葛林‧嘉寶醫師", "0011039848", "2025-12-18", ("精神醫學", "心理治療", "DSM-5")),

    curated_book("05_food_wellness", "飲食養生", "正韓湯鍋〖博客來獨家親簽版〗 ：五星韓廚的道地韓湯！從湯頭風味到烹調技巧，49道職人級湯品的美味哲學", "孫榮KaiSon", "0011041953", "2026-01-15", ("韓國料理", "湯鍋", "湯底")),
    curated_book("05_food_wellness", "飲食養生", "圖繪泰國料理", "卡洛琳．趙", "0011043121", "2026-01-28", ("泰國料理", "飲食文化", "食譜")),
    curated_book("05_food_wellness", "飲食養生", "無添加高湯粉：一粉入魂，簡單好吃的日式家常菜", "藍筱儀 Angel", "0011035294", "2025-11-07", ("高湯", "無添加", "家常菜")),
    curated_book("05_food_wellness", "飲食養生", "親愛的，今天蛋想怎麼吃？：〖愛妻廚房必備〗有蛋就有88種靈感，雞牛豬魚蝦也來湊湊熱鬧", "貝蒂做便當", "0011040629", "2025-12-31", ("蛋料理", "家常菜", "食譜")),
    curated_book("05_food_wellness", "飲食養生", "從麵團到吐司: 完整烘焙指南", "黃鈺翔", "0011041317", "2026-01-15", ("麵包", "吐司", "烘焙")),

    curated_book("06_computer_info", "電腦資訊", "Canva零基礎入門：圖文設計、影音動畫、簡報編輯、行銷素材、AI應用快速上手 (暢銷回饋版)", "鄭苑鳳", "", "2025-12-31", ("Canva", "視覺設計", "AI應用")),
    curated_book("06_computer_info", "電腦資訊", "ChatGPT X SEO行銷超強工作術：高效活用AI工具，穩定提升網站能見度(第三版)", "吳燦銘、胡昭民", "", "2025-12-30", ("ChatGPT", "SEO", "網路行銷")),
    curated_book("06_computer_info", "電腦資訊", "網路行銷的14堂關鍵必修課：ChatGPT 5•UI/UX•行動支付•駭客•廣告•SEO•直播•Google Gemini•AI多媒體(第三版)", "胡昭民", "", "2025-12-30", ("網路行銷", "AI", "SEO")),
    curated_book("06_computer_info", "電腦資訊", "Vibe Coding 提示詞全攻略! 從概念到業界實戰：提示工程 / 程式碼維護 / Cursor / ChatGPT Codex / Lovable", "卓昌憲 Penguin Cho 著", "", "2025-12-29", ("Vibe Coding", "提示工程", "AI開發")),
    curated_book("06_computer_info", "電腦資訊", "商務人士一定要懂的ChatGPT活用術", "國本知里", "", "2025-12-29", ("ChatGPT", "商務應用", "生產力")),

    curated_book("07_other", "其他", "埃及", "墨刻編輯部、翁紫曦", "", "2026-01-22", ("埃及", "古文明", "文化旅行")),
    curated_book("07_other", "其他", "尋貓啟事", "崔瑩", "", "2026-01-20", ("貓", "歷史", "文化")),
    curated_book("07_other", "其他", "中國大陸經改的政經分析", "戴東清", "", "2026-01-20", ("中國研究", "政治經濟", "經濟改革")),
    curated_book("07_other", "其他", "台灣光復那些年--重現1945前後的胎動與新生", "汪毅夫", "", "2026-01-20", ("臺灣史", "1945", "歷史記憶")),
    curated_book("07_other", "其他", "馬祖祕密地圖：發掘世界級的寶藏", "榮芳杰、彭若涵", "", "2026-01-20", ("馬祖", "地方文化", "地圖")),
)


def prepare_curated_candidates(refresh: bool) -> list[dict]:
    manifest = batch.findbook_writer.read_json(batch.ROOT / "data.json")
    used_keys = {
        batch.findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
        if book.get("workId") != batch.WORK_ID
    }
    rows = [
        row for row in CURATED_BOOKS
        if batch.findbook_writer.normalized_key(row["title"], row["author"]) not in used_keys
    ]
    expected = {spec.category_id: spec.quota for spec in batch.CATEGORIES}
    actual = {
        category_id: sum(row["categoryId"] == category_id for row in rows)
        for category_id in expected
    }
    keys = {
        batch.findbook_writer.normalized_key(row["title"], row["author"])
        for row in rows
    }
    if actual != expected or len(keys) != len(rows):
        raise RuntimeError(f"策展候選需補書：counts={actual} unique={len(keys)}/{len(rows)}")
    batch.findbook_writer.write_json_atomic(batch.MASTER_CANDIDATES, rows)
    return rows


batch.prepare_candidates = prepare_curated_candidates


if __name__ == "__main__":
    batch.main()
