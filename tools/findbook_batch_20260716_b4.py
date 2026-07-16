from __future__ import annotations

import time
import urllib.error
from pathlib import Path

import findbook_batch_20260716_b3 as previous


batch = previous.batch
batch.BATCH_NAME = "20260716_b4"
batch.WORK_ID = "findbook-20260716-074811-b4"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260716_b4.json"
)
batch.BROWSER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b4.json"
)

EXTRA_QUERIES = {
    "01_business_startup": ("企業財務", "領導", "品牌經營", "工作效率"),
    "02_psychology_growth": ("自我接納", "正念", "心理諮商", "親密關係", "內向", "拖延", "韌性"),
    "03_natural_science": ("化學", "地球科學", "演化", "生態"),
    "04_healthcare": ("健康檢查", "復健", "高齡照護"),
    "05_food_wellness": ("食譜", "營養學", "飲食保健"),
    "06_computer_info": ("網路安全", "資料庫", "演算法", "生成式AI"),
    "07_other": ("世界史", "臺灣史", "藝術", "哲學", "社會學", "旅行"),
}


def curated_book(
    category_id: str,
    label: str,
    title: str,
    author: str,
    item: str,
    published: str,
    subjects: tuple[str, ...],
) -> dict:
    row = previous.prior.curated_book(
        category_id, label, title, author,
        f"https://www.books.com.tw/products/{item}", published or "來源未標示",
        subjects,
    )
    if not published:
        row["sourceDateNote"] = (
            f"博客來公開列表未提供明確出版日期；擷取日期 {batch.TO_DATE}，"
            f"依來源可讀性列入 {batch.FROM_DATE} 至 {batch.TO_DATE} 的搜尋區間候選。"
        )
    return row


INITIAL_CURATED_BOOKS = (
    curated_book("01_business_startup", "商業理財", "強績效策略，從願景到成果的新管理趨勢：談薪資待遇、企業認可、目標成就……結合核心理論，「八大工具表」全面提升企業績效管理！", "楊文浩", "0011014546", "2025-02-19", ("績效管理", "組織策略", "人才培育")),
    curated_book("01_business_startup", "商業理財", "扁平化管理，從繁雜到高效的管理蛻變：化繁為簡、專注關鍵，以最少資源創造最大價值", "張毅、西武", "0011014548", "2025-02-19", ("扁平化", "管理效率", "資源配置")),
    curated_book("01_business_startup", "商業理財", "阿米巴激勵體系！全面剖析稻盛和夫經營哲學：薪酬×獎金×股權全解析，從哲學理念到管理技術的全面進化", "胡八一", "0011014551", "2025-02-19", ("阿米巴經營", "激勵制度", "薪酬管理")),
    curated_book("01_business_startup", "商業理財", "追求卓越：長銷40年，管理超級大師畢德士扛鼎之作，巴菲特盛讚的企業管理經典", "湯姆．畢德士、羅勃．華特曼", "0011015943", "2025-02-07", ("企業管理", "卓越組織", "管理經典")),
    curated_book("01_business_startup", "商業理財", "祕書親信該有的參謀思維：成為辦公室的拆彈專家，上司倚仗的智囊心腹，解鎖升遷限制的職場破框思考", "荒川詔四", "0011012911", "2025-02-07", ("職場溝通", "參謀思維", "問題解決")),
    curated_book("01_business_startup", "商業理財", "當部屬無法依指令做事：很努力卻沒照你說的執行、重複同樣的錯、忘東忘西、把建議當惡意、被客戶牽著走……一步驟消除主管帶人困擾。", "榎本博明", "0011012156", "2025-02-04", ("主管帶人", "團隊溝通", "執行管理")),
    curated_book("01_business_startup", "商業理財", "我創業，我獨角 no.10：精實創業全紀錄，商業模式全攻略", "羅芷羚", "0011012324", "2025-02-01", ("精實創業", "商業模式", "創業案例")),
    curated_book("01_business_startup", "商業理財", "我創業，我獨角 no.11：精實創業全紀錄，商業模式全攻略", "羅芷羚", "0011012326", "2025-02-01", ("精實創業", "商業模式", "品牌案例")),
    curated_book("01_business_startup", "商業理財", "我創業，我獨角 no.12：精實創業全紀錄，商業模式全攻略", "羅芷羚", "0011012328", "2025-02-01", ("精實創業", "商業模式", "經營實務")),
    curated_book("01_business_startup", "商業理財", "超圖解高績效主管養成術：關鍵69堂課", "戴國良", "0011011985", "2025-01-28", ("主管能力", "高績效", "管理實務")),
    curated_book("01_business_startup", "商業理財", "臺灣創業型大學之發展：理論與個案", "吳慈榕、張元杰、蔡林彤飛", "0011013553", "2025-01-23", ("創業教育", "大學治理", "個案研究")),
    curated_book("01_business_startup", "商業理財", "布局九略：你永遠玩不過一個讀通布局九略的人，無局不可布，無局不能成，九大方略讓你布局致勝", "東篱子", "0011011405", "2025-01-22", ("策略思考", "局勢判斷", "決策")),
    curated_book("01_business_startup", "商業理財", "顛覆與重構，管理者的新商業思維", "邢國英", "0011011922", "2025-01-22", ("商業創新", "管理思維", "市場變革")),
    curated_book("01_business_startup", "商業理財", "客戶資本：以兩岸專家觀點看中國企業以客戶為中心的增長策略", "王賽、鍾思騏", "0011012498", "2025-01-22", ("客戶價值", "增長策略", "商業模式")),
    curated_book("01_business_startup", "商業理財", "企業創新與使命：36位創業家企業創新與使命", "台企會菁英群", "0011012320", "2025-01-21", ("企業創新", "創業家", "社會責任")),
    curated_book("01_business_startup", "商業理財", "點亮品牌之光（5）企業家、職人專訪", "優報導youReport", "0011012325", "2025-01-21", ("品牌經營", "企業家", "職人精神")),
    curated_book("01_business_startup", "商業理財", "亞馬遜領導力：亞馬遜14條最強管理與領導原則", "約翰．羅斯曼", "0011010975", "2025-01-20", ("領導力", "亞馬遜", "組織原則")),
    curated_book("01_business_startup", "商業理財", "〖倍速講義〗杜拉克×卡內基商業小學堂", "藤屋伸二", "0011010566", "2025-01-17", ("杜拉克", "卡內基", "商業管理")),
    curated_book("01_business_startup", "商業理財", "杜拉克談高效能的5個習慣（暢銷新裝版）", "彼得．杜拉克", "0011011026", "2025-01-17", ("高效能", "時間管理", "管理思想")),
    curated_book("01_business_startup", "商業理財", "高效領導力：杜拉克的52週教練課", "約瑟夫．馬齊里洛", "0011011567", "2025-01-16", ("領導力", "教練", "杜拉克")),

    curated_book("02_psychology_growth", "心理勵志", "度冬：在人生的寒冷時刻，停止消耗自己，沉靜修復內在", "凱瑟琳．梅", "0011037886", "2025-12-03", ("心理修復", "韌性", "自我照顧")),
    curated_book("02_psychology_growth", "心理勵志", "不完美，才自由：學會與自己和解，從人生谷底到CEO的幸福逆襲心法，遇見就是歡喜，逆境是成長的養分！", "貝姬Becky（宋可欣）", "0011037909", "2025-12-03", ("自我和解", "逆境成長", "幸福")),
    curated_book("02_psychology_growth", "心理勵志", "走出黑森林—自我轉變的旅程：你所經歷的困境讓你成為你自己", "陳海賢", "0011037928", "2025-12-03", ("自我轉變", "心理諮商", "困境")),
    curated_book("02_psychology_growth", "心理勵志", "「思路清楚」需要的是勇氣，不是智慧", "林郁／主編", "0011037997", "2025-12-03", ("勇氣", "自我覺察", "思考")),
    curated_book("02_psychology_growth", "心理勵志", "往好的地方看，你就會變得更好", "林郁／主編", "0011037998", "2025-12-03", ("正向心理", "情緒調節", "成長")),
    curated_book("02_psychology_growth", "心理勵志", "從負債2000萬到逆轉現實每一天：56個解鎖困境、終結內耗的強運心法，回應宇宙法則，活出天命，自然內外富裕！", "小池浩", "0011038696", "2025-12-03", ("內耗", "信念", "行動")),
    curated_book("02_psychology_growth", "心理勵志", "我媽已經三天沒打我了：喵！大膽點，貓咪哪有不出錯的呢！", "老楊的貓頭鷹", "0011037910", "2025-12-03", ("自我接納", "幽默", "療癒")),
    curated_book("02_psychology_growth", "心理勵志", "寫給離開與留下之人的．刺蝟日記：當愛超越生命的邊界，我們終將學會告別，一場從臨終到重生的真實旅程", "莎拉．桑兹", "0011037892", "2025-12-03", ("告別", "悲傷療癒", "生命教育")),
    curated_book("02_psychology_growth", "心理勵志", "在黑暗的日子裡，陪伴是最溫暖的曙光：大熊貓與小小龍的相伴旅程", "詹姆斯．諾柏瑞", "0011037305", "2025-12-02", ("陪伴", "希望", "關係")),
    curated_book("02_psychology_growth", "心理勵志", "1分鐘奇蹟日記：年收百萬、體態改變、不敢想的事全發生了", "三宅裕之", "0011037840", "2025-12-01", ("書寫練習", "習慣", "自我效能")),
    curated_book("02_psychology_growth", "心理勵志", "人若不開悟，無論怎麼活都痛苦", "張善通", "0011039047", "2025-12-01", ("覺察", "痛苦", "自我探索")),
    curated_book("02_psychology_growth", "心理勵志", "勇敢告別的人，生活會獎勵一場新的開始", "Peter Su", "0011037485", "2025-11-30", ("告別", "重建", "希望")),
    curated_book("02_psychology_growth", "心理勵志", "主人（精裝燙金全新彩圖版）：你的外面沒有別人，但你不是獨自一個人", "心玲", "0011037429", "2025-11-29", ("內在力量", "關係", "自我成長")),
    curated_book("02_psychology_growth", "心理勵志", "老公，我要出門約會了！：一位妻子走入開放式婚姻，學習誠實、溝通及重新定義愛的探險之旅", "茉莉．羅登．溫特", "0011037437", "2025-11-29", ("親密關係", "誠實溝通", "界線")),
    curated_book("02_psychology_growth", "心理勵志", "銀髮川柳9：原來我的手機，忘在冰箱裡", "POPLAR社、日本公益社團法人全國自費老人之家協會", "0011036440", "2025-11-28", ("熟齡生活", "幽默", "生命態度")),
    curated_book("02_psychology_growth", "心理勵志", "刪掉容易，忘掉很難", "林思齊", "0011041796", "2026-01-20", ("失落", "情緒整理", "關係療癒")),
    curated_book("02_psychology_growth", "心理勵志", "中年之路：穿越幽暗，迎向完整的內在鍊金之旅", "詹姆斯．霍利斯", "0010990110", "2024-06-05", ("中年心理", "榮格心理學", "個體化")),
    curated_book("02_psychology_growth", "心理勵志", "自卑與超越：生命對你意味著什麼（全新修訂二版）", "阿爾弗雷德‧阿德勒", "0011028766", "2025-08-13", ("阿德勒", "自卑", "社會興趣")),
    curated_book("02_psychology_growth", "心理勵志", "哇賽！心理學：48個超實用建議，讓你從此告別卡卡人生", "蔡宇哲", "0010779792", "2018-03-01", ("心理學", "生活應用", "行為")),
    curated_book("02_psychology_growth", "心理勵志", "明明沒病，一看到老公就不舒服：妳的「丈夫在家壓力症候群」該化解了", "和田秀樹", "0011029194", "2025-08-27", ("伴侶關係", "壓力", "熟齡心理")),

    curated_book("03_natural_science", "自然科學", "蘋果才沒有砸在牛頓頭上！：長久以來被誤解的科學故事大解密", "安托萬‧侯盧─賈西亞", "0011019926", "", ("科學史", "科學迷思", "物理")),
    curated_book("03_natural_science", "自然科學", "命定：沒有自由意志的科學", "羅伯．薩波斯基", "0011006605", "2024-12-04", ("神經科學", "自由意志", "行為生物學")),
    curated_book("03_natural_science", "自然科學", "情緒跟你以為的不一樣（暢銷改版）──科學證據揭露喜怒哀樂如何生成", "麗莎．費德曼．巴瑞特", "0011019049", "2025-04-26", ("情緒科學", "神經科學", "大腦")),
    curated_book("03_natural_science", "自然科學", "人類存在的意義：一個生物學家對生命的思索", "愛德華．威爾森", "0011018237", "2025-04-14", ("演化生物學", "人類", "生命")),
    curated_book("03_natural_science", "自然科學", "人類文明：生物機制如何塑造世界史", "達奈爾", "0010990283", "2024-05-30", ("生物學", "文明", "演化")),
    curated_book("03_natural_science", "自然科學", "為何龍蝦不會變老，水母會逆齡，人類卻無法？：24個自然界中青春、衰老與生命期限的科學奧祕", "尼可拉斯•潘柏格", "0011009096", "2025-01-02", ("老化", "動物學", "生命科學")),
    curated_book("03_natural_science", "自然科學", "如果這樣，會怎樣？（10週年增訂版）：胡思亂想的搞怪趣問，正經認真的科學妙答", "蘭德爾．門羅", "0011036314", "2025-11-24", ("科學推理", "物理", "思想實驗")),
    curated_book("03_natural_science", "自然科學", "如果這樣，會怎樣？2：千奇百怪的問題 嚴肅精確的回答", "蘭德爾．門羅", "0010953383", "2023-03-31", ("科學推理", "估算", "思想實驗")),
    curated_book("03_natural_science", "自然科學", "德國一流大學教你數學家的22個思考工具", "克里斯昂．赫塞", "0011010499", "2025-01-13", ("數學", "思考工具", "解題")),
    curated_book("03_natural_science", "自然科學", "寫給懶人的神奇化學書：既長知識又省時省力的生活祕笈", "李光烈", "0011006530", "2024-12-01", ("化學", "生活科學", "清潔原理")),

    curated_book("04_healthcare", "醫療保健", "好眼力：台大眼科名醫楊中美教你正確認識及防護眼睛疾病", "楊中美、黃靜宜", "0011017241", "", ("眼科", "視力保健", "疾病預防")),
    curated_book("04_healthcare", "醫療保健", "更年期完全聖經：更年不是老化而是身體系統升級，從前期到後期都能接住妳的身心照護指南", "瑪莉‧克萊爾‧哈弗", "0011025577", "2025-07-09", ("更年期", "婦女健康", "實證照護")),
    curated_book("04_healthcare", "醫療保健", "39~63歲‧圖解更年期全書：婦科權威&美容師親身經驗，從荷爾蒙帶你輕鬆了解症狀／療法／舒緩／調理／美容", "対馬瑠璃子、吉川千明", "0010940661", "2022-12-08", ("更年期", "荷爾蒙", "女性保健")),
    curated_book("04_healthcare", "醫療保健", "別怕荷爾蒙，妳抗衰防病的關鍵：全面解析更年期症狀、心血管健康、失智症、骨質疏鬆、心理健康、乳癌迷思", "吳佳鴻", "0011015074", "2025-03-11", ("荷爾蒙", "心血管", "婦女健康")),
    curated_book("04_healthcare", "醫療保健", "一輩子的好視力：只有眼科醫生才知道，保持好視力的50個習慣", "平松類", "0010978340", "2024-01-16", ("眼科", "視力", "日常保健")),

    curated_book("05_food_wellness", "飲食養生", "林姓主婦的晚餐餐桌提案：4種生活情境 Ｘ 8組餐桌提案＝32套美味一桌菜", "林姓主婦", "0011011986", "2025-02-07", ("家庭料理", "餐桌規劃", "食譜")),
    curated_book("05_food_wellness", "飲食養生", "四季戚風蛋糕專門書：柔軟綿密蛋糕 X 四季更迭花草，結合戚風蛋糕與鮮奶油裝飾，探索四季獨特風味", "呂昇達、Daisy", "0011010184", "2025-01-15", ("烘焙", "戚風蛋糕", "季節食材")),
    curated_book("05_food_wellness", "飲食養生", "10分鐘快速登場 義大利麵的多重饗宴", "PastaWorks Takashi", "0011008829", "2025-01-15", ("義大利麵", "快速料理", "食譜")),
    curated_book("05_food_wellness", "飲食養生", "蔬食料理聖經（上）：葉菜、花菜、蔥蒜、嫩莖、玉米與番薯篇", "尼克．夏馬", "0011017026", "", ("蔬食", "食材", "料理技法")),
    curated_book("05_food_wellness", "飲食養生", "如何品飲咖啡：19個練習，開拓感官技巧，品嘗每杯咖啡的全貌", "潔西卡‧伊斯托", "0011016775", "", ("咖啡", "感官訓練", "品飲")),

    curated_book("06_computer_info", "電腦資訊", "Gemini x NotebookLM 領軍：Nano Banana x Imagen x Veo x Gem x Gemini Live - Google 多模態 AI 工作流", "洪錦魁", "0011034764", "2025-10-17", ("Gemini", "NotebookLM", "AI工作流")),
    curated_book("06_computer_info", "電腦資訊", "Clean Code：Python 寫乾淨程式碼 - 告別技術債，不再為爛程式加班收爛攤", "洪錦魁", "0011033500", "2025-10-09", ("Python", "Clean Code", "技術債")),
    curated_book("06_computer_info", "電腦資訊", "最強 AI 組合技！NotebookLM / Gemini / Nano Banana / Veo 3 〖影音生成進化版〗", "施威銘研究室", "0011034258", "2025-10-17", ("生成式AI", "影音生成", "NotebookLM")),
    curated_book("06_computer_info", "電腦資訊", "AI超神應用術：Google Gemini × Gemini Live × Nano Banana × Veo × Flow × NotebookLM全解鎖", "鄧君如、文淵閣工作室", "0011035186", "2025-10-30", ("Google AI", "多模態", "生產力")),
    curated_book("06_computer_info", "電腦資訊", "高效能Python程式設計 第三版：寫給人類的高性能編程法", "Micha Gorelick、Ian Ozsvald", "0011039382", "", ("Python", "效能優化", "程式設計")),

    curated_book("07_other", "其他", "流量國度：從人氣變現到掌握影響力，網紅如何造就自媒體盛世", "泰勒・羅倫茲", "0011015256", "", ("網路文化", "自媒體", "社會史")),
    curated_book("07_other", "其他", "電玩的本質：遊走於真實規則與虛構世界的藝術", "賈斯柏．朱爾", "0011012759", "", ("遊戲研究", "文化", "藝術")),
    curated_book("07_other", "其他", "寫作的靈現：AI時代寫手的修煉與想像力", "楊憲宏", "0011007167", "", ("寫作", "想像力", "AI時代")),
    curated_book("07_other", "其他", "串流音樂為何能精準推薦「你可能喜歡」：從演算機制、音樂經濟到文化現象，前Spotify資料鍊金師全剖析", "葛倫．麥當諾", "0011007009", "", ("音樂文化", "演算法", "串流經濟")),
    curated_book("07_other", "其他", "數位自我：從出生到登出人生，科技如何影響人格發展？", "艾蓮・卡斯凱特", "0011000853", "", ("數位文化", "人格發展", "科技社會")),
)


REPLACED_TITLES = {
    "顛覆與重構，管理者的新商業思維",
    "度冬：在人生的寒冷時刻，停止消耗自己，沉靜修復內在",
    "不完美，才自由：學會與自己和解，從人生谷底到CEO的幸福逆襲心法，遇見就是歡喜，逆境是成長的養分！",
    "走出黑森林—自我轉變的旅程：你所經歷的困境讓你成為你自己",
    "「思路清楚」需要的是勇氣，不是智慧",
    "往好的地方看，你就會變得更好",
    "寫給離開與留下之人的．刺蝟日記：當愛超越生命的邊界，我們終將學會告別，一場從臨終到重生的真實旅程",
    "在黑暗的日子裡，陪伴是最溫暖的曙光：大熊貓與小小龍的相伴旅程",
    "1分鐘奇蹟日記：年收百萬、體態改變、不敢想的事全發生了",
    "人若不開悟，無論怎麼活都痛苦",
    "勇敢告別的人，生活會獎勵一場新的開始",
    "主人（精裝燙金全新彩圖版）：你的外面沒有別人，但你不是獨自一個人",
    "老公，我要出門約會了！：一位妻子走入開放式婚姻，學習誠實、溝通及重新定義愛的探險之旅",
    "中年之路：穿越幽暗，迎向完整的內在鍊金之旅",
    "命定：沒有自由意志的科學",
    "情緒跟你以為的不一樣（暢銷改版）──科學證據揭露喜怒哀樂如何生成",
    "人類存在的意義：一個生物學家對生命的思索",
    "為何龍蝦不會變老，水母會逆齡，人類卻無法？：24個自然界中青春、衰老與生命期限的科學奧祕",
}

REPLACEMENT_BOOKS = (
    curated_book("01_business_startup", "商業理財", "不敗的智慧：孫子兵法讓你當個好人也不會輸！", "長尾一洋", "0011010488", "2025-01-13", ("孫子兵法", "商業策略", "決策")),

    curated_book("02_psychology_growth", "心理勵志", "成為自己的貴人：不內耗、不強求，順應變化的49個人生提醒", "阿飛", "0011040701", "2025-12-29", ("自我支持", "人生選擇", "心理韌性")),
    curated_book("02_psychology_growth", "心理勵志", "攻心操控說服術（暢銷新版）：從「眼神表情」與「姿勢」看穿內心想法，活用「暗示與問話五技術」，無論誰都甘心聽你的", "葛瑞格利‧哈特萊、瑪莉安‧卡琳屈", "0011040095", "2025-12-26", ("說服", "肢體語言", "人際互動")),
    curated_book("02_psychology_growth", "心理勵志", "亨利識人術：用八種臉型洞悉人性的奧秘", "周亨利", "0011043380", "2025-12-26", ("識人", "人性洞察", "自我修養")),
    curated_book("02_psychology_growth", "心理勵志", "不過度努力，不為難自己的減法哲學：捨去不必要的執著，只做擅長的事，更容易成功的41個轉念練習", "伊庭正康", "0011040094", "2025-12-26", ("減法思維", "自我接納", "壓力調節")),
    curated_book("02_psychology_growth", "心理勵志", "用指尖聊出好關係：從職場溝通到日常互動，網聊時代的好感對話術", "瑪那熊（陳家維）", "0011040126", "2025-12-25", ("網路溝通", "人際關係", "情緒辨識")),
    curated_book("02_psychology_growth", "心理勵志", "生活賽局學，日常選擇中的心理與策略：囚徒困境×納許均衡×重複博弈……打破零和思維、看懂人性陷阱，用心理學找出你的最優解", "崔英勝", "0011034358", "2025-10-15", ("賽局理論", "心理策略", "生活選擇")),
    curated_book("02_psychology_growth", "心理勵志", "讓聲音被聽見：小金老師的20堂打動人心說話課", "張金蘭", "0011032877", "2025-10-03", ("口語表達", "自信", "溝通")),
    curated_book("02_psychology_growth", "心理勵志", "逆轉不和諧人際關係，從此難受、痛苦全數終結！", "松村亞里", "0011032808", "2025-10-01", ("人際關係", "正向心理", "衝突修復")),
    curated_book("02_psychology_growth", "心理勵志", "玩的就是心計：一本書講透人際交往中的心理博弈學！有心計，懂套路，牢牢掌控人生的主動權", "路天章", "0011032888", "2025-09-30", ("心理博弈", "人際策略", "自我保護")),
    curated_book("02_psychology_growth", "心理勵志", "對你親切，不代表我好欺負：學會精準表達，讓心意不被誤解的31個提案", "鄭文正", "0011032778", "2025-09-27", ("界線", "精準表達", "自我主張")),
    curated_book("02_psychology_growth", "心理勵志", "WIN-WIN！美國人的雙贏溝通法：「說真話也不傷人」的聰明人際學！", "小林音子", "0011021207", "2025-05-26", ("雙贏溝通", "尊重", "共感")),
    curated_book("02_psychology_growth", "心理勵志", "關係免疫力：人際排毒、建立強連結與非暴力溝通的哈佛心理學課（長銷新版）", "梅樂妮．喬伊", "0011020337", "2025-05-20", ("關係韌性", "非暴力溝通", "安全感")),
    curated_book("02_psychology_growth", "心理勵志", "看人要準，防人要快：FBI資深顧問教你一眼認出危險人物，避開身邊的隱形炸彈", "大衛．李柏曼", "0011020250", "2025-05-15", ("識人", "風險訊號", "自我保護")),

    curated_book("03_natural_science", "自然科學", "五感之外的世界：認識動物神奇的感知系統，探見人類感官無法觸及的大自然", "艾德．楊", "0010963862", "2023-08-10", ("動物感官", "演化", "生物學")),
    curated_book("03_natural_science", "自然科學", "21世紀狩獵採集者的生存指南：讓演化生物學為你的人生效力", "希瑟•赫因、布萊特•韋恩斯坦", "0010982889", "2024-03-06", ("演化生物學", "現代生活", "人類行為")),
    curated_book("03_natural_science", "自然科學", "如何蓋一座大教堂？：學習工程師「解決問題的思維」！從重大歷史工程到日常小物，一窺創新與發明背後的故事", "比爾．漢馬克", "0011035210", "2025-11-06", ("工程學", "試錯", "發明史")),
    curated_book("03_natural_science", "自然科學", "熱帶雨林：多樣、美麗而稀少的熱帶生命", "約瑟夫‧萊希霍夫", "0011030686", "2025-10-13", ("熱帶雨林", "生物多樣性", "自然保育")),
)

CURATED_BOOKS = tuple(
    row for row in INITIAL_CURATED_BOOKS if row["title"] not in REPLACED_TITLES
) + REPLACEMENT_BOOKS


def prepare_curated_candidates(refresh: bool) -> list[dict]:
    manifest = batch.findbook_writer.read_json(batch.ROOT / "data.json")
    used_keys = {
        batch.findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    used_urls = {str(book.get("sourceUrl", "")).strip() for book in manifest.get("books", [])}
    rows = [
        row for row in CURATED_BOOKS
        if batch.findbook_writer.normalized_key(row["title"], row["author"]) not in used_keys
        and row["sourceUrl"] not in used_urls
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


def fetch_with_retry(keyword: str) -> str:
    for attempt in range(2):
        try:
            return batch.fetch_search(keyword)
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 1:
                raise
            time.sleep(3)
    raise RuntimeError(f"無法取得搜尋結果：{keyword}")


def prepare_checkpointed_candidates(refresh: bool) -> list[dict]:
    if batch.MASTER_CANDIDATES.exists() and not refresh:
        rows = batch.findbook_writer.read_json(batch.MASTER_CANDIDATES)
        if isinstance(rows, list) and len(rows) == sum(spec.quota for spec in batch.CATEGORIES):
            return rows

    manifest = batch.findbook_writer.read_json(batch.ROOT / "data.json")
    used_keys = {
        batch.findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    used_urls = {str(book.get("sourceUrl", "")).strip() for book in manifest.get("books", [])}
    selected_all: list[dict] = []
    selected_keys: set[str] = set()
    selected_urls: set[str] = set()

    for spec in batch.CATEGORIES:
        checkpoint = Path(__file__).resolve().parent / f".findbook_search_{spec.category_id[:2]}_20260716_b4.json"
        selected: list[dict] = []
        if checkpoint.exists() and not refresh:
            cached = batch.findbook_writer.read_json(checkpoint)
            if isinstance(cached, list):
                for row in cached:
                    key = batch.findbook_writer.normalized_key(row.get("title", ""), row.get("author", ""))
                    url = str(row.get("sourceUrl", "")).strip()
                    if key not in used_keys and key not in selected_keys and url not in used_urls and url not in selected_urls:
                        selected.append(row)
                        selected_keys.add(key)
                        selected_urls.add(url)

        queries = spec.queries + EXTRA_QUERIES.get(spec.category_id, ())
        for keyword in queries:
            if len(selected) >= spec.quota:
                break
            try:
                page = fetch_with_retry(keyword)
            except urllib.error.HTTPError as error:
                print(f"source-limited\t{spec.category_id}\t{keyword}\tHTTP {error.code}")
                continue
            for row in batch.parse_items(page, spec, keyword):
                title = row.get("title", "")
                if any(marker in title for marker in ("套書", "全套", "全兩冊")):
                    continue
                key = batch.findbook_writer.normalized_key(title, row.get("author", ""))
                url = str(row.get("sourceUrl", "")).strip()
                if key in used_keys or key in selected_keys or url in used_urls or url in selected_urls:
                    continue
                row.pop("_published", None)
                selected.append(row)
                selected_keys.add(key)
                selected_urls.add(url)
                if len(selected) >= spec.quota:
                    break
            if spec.category_id == "07_other" and len(selected) < spec.quota:
                for url in batch.product_links(page):
                    if url in used_urls or url in selected_urls:
                        continue
                    try:
                        row = batch.fetch_product_candidate(url, spec, keyword)
                    except Exception:
                        continue
                    if row is None:
                        continue
                    key = batch.findbook_writer.normalized_key(row["title"], row["author"])
                    if key in used_keys or key in selected_keys:
                        continue
                    selected.append(row)
                    selected_keys.add(key)
                    selected_urls.add(url)
                    if len(selected) >= spec.quota:
                        break
            batch.findbook_writer.write_json_atomic(checkpoint, selected)
            print(f"checkpoint\t{spec.category_id}\t{keyword}\tselected={len(selected)}")
            time.sleep(0.4)
        if len(selected) != spec.quota:
            raise RuntimeError(f"{spec.category_id} 只有 {len(selected)} 本中文新候選，未達 {spec.quota} 本")
        selected_all.extend(selected)

    batch.findbook_writer.write_json_atomic(batch.MASTER_CANDIDATES, selected_all)
    return selected_all


batch.prepare_candidates = prepare_curated_candidates


if __name__ == "__main__":
    batch.main()
