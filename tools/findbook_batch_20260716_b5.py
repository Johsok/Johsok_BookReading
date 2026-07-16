from __future__ import annotations

from pathlib import Path

import findbook_batch_20260716_b4 as previous
import findbook_batch_20260716_b2 as base


batch = previous.batch
batch.BATCH_NAME = "20260716_b5"
batch.WORK_ID = "findbook-20260716-081252-b5"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260716_b5.json"
)
batch.BROWSER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_books_20260716_b5.json"
)

LIST_URLS = {
    "01_business_startup": "https://www.books.com.tw/web/sys_nbmidme/books/02",
    "02_psychology_growth": "https://www.books.com.tw/web/sys_nbmidme/books/07",
    "03_natural_science": "https://www.books.com.tw/web/sys_nbmidme/books/19",
    "04_healthcare": "https://www.books.com.tw/web/sys_nbmidme/books/08",
    "05_food_wellness": "https://www.books.com.tw/web/sys_nbmidme/books/17",
    "06_computer_info": "https://www.books.com.tw/web/sys_nbmidme/books/18",
    "07_other": "https://www.books.com.tw/web/sys_nbmidme/books/03",
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
    curated_book("01_business_startup", "商業理財", "遇見更好的自己：讓我告訴全世界，只有自己可以超越自己", "林玟妗", "0011042444", "2026-01-22", ("職涯探索", "自我超越", "行動選擇")),
    curated_book("01_business_startup", "商業理財", "所有問題，都是一場賽局：贏家邏輯──洞悉高勝算決策，操縱與雙贏的策略思考〖暢銷紀念版〗", "川西諭", "0011042389", "2026-01-21", ("賽局理論", "決策", "策略思考")),
    curated_book("01_business_startup", "商業理財", "奈特論風險、不確定性與利潤：在不可預測世界中，判斷如何成為利潤來源", "法蘭克．奈特、伊莉莎", "", "2026-01-21", ("風險", "不確定性", "利潤")),
    curated_book("01_business_startup", "商業理財", "提升未來：可以、應該、可能、不該，思考升級的四個關鍵詞", "尼克‧佛斯特", "", "2025-12-31", ("未來思考", "決策", "判斷")),
    curated_book("01_business_startup", "商業理財", "你不需要天賦，只需要每天1%的進步：54個職場影響力行動指南", "安迪．艾里斯", "", "2025-12-31", ("職場成長", "影響力", "持續進步")),
    curated_book("01_business_startup", "商業理財", "AI時代，會說故事才是你的關鍵生存力：把話說進人心，讓人為你行動的影響力", "凱倫．艾伯", "", "2025-12-31", ("故事力", "溝通", "AI時代")),
    curated_book("01_business_startup", "商業理財", "採購與供應管理", "中華採購與供應管理協會、許振邦", "", "2025-12-31", ("採購", "供應鏈", "管理")),
    curated_book("01_business_startup", "商業理財", "最強技術分析聖經 布林通道指標操作法：用230張圖抄底抓反彈，85%勝率賺翻股市!", "李洪宇", "", "2025-12-30", ("技術分析", "布林通道", "投資")),
    curated_book("01_business_startup", "商業理財", "AI會取代人類智慧嗎?：人工智慧與人類智慧的雙重謎團", "丹尼爾．安德勒", "", "2025-12-30", ("人工智慧", "人類智慧", "科技趨勢")),
    curated_book("01_business_startup", "商業理財", "智慧型投資人：價值投資權威著作(75週年紀念.全新譯本)", "傑森．茲威格、班傑明．葛拉漢", "", "2025-12-30", ("價值投資", "風險管理", "投資紀律")),
    curated_book("01_business_startup", "商業理財", "業務之神的極限成交：為什麼那個業務員可以快速、輕鬆賣出一億元商品?", "瀧本真也", "", "2025-12-29", ("銷售", "成交", "客戶溝通")),
    curated_book("01_business_startup", "商業理財", "節省工時的100種方法：我在巴克萊銀行、AIG、安聯等外商主管身邊學會，品質與速度兼顧的時短工作術，不用拚命就有高績效。", "森田幸（森田ゆき）", "", "2025-12-29", ("工作效率", "時間管理", "高績效")),
    curated_book("01_business_startup", "商業理財", "擠出獲利：20年來，為無數大老闆與CEO一對一授課的經營教練，從擠出現金活下來，到基業長青年年賺", "金炯坤", "", "2025-12-29", ("獲利", "現金流", "企業經營")),
    curated_book("01_business_startup", "商業理財", "大腦配速的心流工作術：AI時代從A到A+的高效法則，讓大腦在對的狀態做對的事", "米圖．斯托羅尼", "", "2025-11-14", ("心流", "腦力管理", "工作效率")),
    curated_book("01_business_startup", "商業理財", "股市豐神榜：一本變神通，從零開始學贏家投資法則", "許豐祿", "", "2025-11-13", ("股票投資", "投資法則", "風險")),
    curated_book("01_business_startup", "商業理財", "從此擺脫加班人生!化繁為簡的30分鐘工作法", "瀧川徹", "", "2025-11-11", ("工作效率", "簡化", "時間管理")),
    curated_book("01_business_startup", "商業理財", "商道", "楊志勇", "", "2025-11-06", ("商業思維", "經營", "管理")),
    curated_book("01_business_startup", "商業理財", "我一生中聽過的最好建議：人生沒有標準答案，在做任何決定前，先留意別人怎麼說，你可以活出自己的版本。", "黛娜．佩里諾", "", "2026-01-20", ("決策", "人生建議", "職涯選擇")),
    curated_book("01_business_startup", "商業理財", "有願就有力，勇敢築夢：喬山從零到世界第一品牌成功奮鬥傳奇", "羅崑泉、陳雅莉", "", "2026-01-17", ("品牌", "創業", "企業成長")),
    curated_book("01_business_startup", "商業理財", "爸媽，我想和你談談錢：關於父母老後的財務與遺囑安排，那些最難開口的金錢對話這樣談", "卡麥隆．赫德斯頓", "", "2026-01-21", ("家庭財務", "退休", "遺囑規劃")),

    curated_book("02_psychology_growth", "心理勵志", "712件可寫的事", "舊金山寫作社", "0011038022", "2025-11-28", ("創意", "書寫練習", "自我探索")),
    curated_book("02_psychology_growth", "心理勵志", "從不怕輸開始贏：世界第一的心態管理法，金牌選手致勝的「無懼失敗」韌性練習", "金美善", "0011038920", "2025-12-11", ("心態管理", "韌性", "失敗學習")),
    curated_book("02_psychology_growth", "心理勵志", "學習人生的雲淡風輕：弘一大師的七部人生禪(三版)", "弘一大師、舒硯", "0011038617", "2025-12-10", ("修心", "人生態度", "安定")),
    curated_book("02_psychology_growth", "心理勵志", "孤獨是一種狀態，寂寞是一種心情", "植西聰", "0011038656", "2025-12-10", ("孤獨", "自處", "情緒理解")),
    curated_book("02_psychology_growth", "心理勵志", "不老青春", "Ｗ．Ｒ．史班斯、鮑伯．達頓", "0011039007", "2025-12-10", ("活力", "熟齡成長", "生命態度")),
    curated_book("02_psychology_growth", "心理勵志", "關於富足，我們應該要……：你賺的是錢，還是你想要的生活?", "費勇", "0011039195", "2025-12-10", ("富足", "生活選擇", "價值觀")),
    curated_book("02_psychology_growth", "心理勵志", "偶然間來到江南站小吃店(隨書贈 勇敢面對生活書籤)", "尹昣善", "0011038648", "2025-12-10", ("療癒", "勇氣", "生活故事")),
    curated_book("02_psychology_growth", "心理勵志", "做自己的太陽，去看你想看的星星和月亮+一個人，你也要活得晴空萬里︰陽光幸福套組", "角子", "0011038869", "2025-12-08", ("自我支持", "幸福", "釋懷")),
    curated_book("02_psychology_growth", "心理勵志", "大人的半日禪：弘一大師的修心筆記", "慈心", "0011038782", "2025-12-04", ("修心", "書寫", "安頓")),
    curated_book("02_psychology_growth", "心理勵志", "爆發式成長", "木沐", "0011038035", "2025-12-04", ("自我提升", "認知", "成長")),
    curated_book("02_psychology_growth", "心理勵志", "心書", "諸葛亮", "0011038034", "2025-12-04", ("識人", "心智", "處世")),
    curated_book("02_psychology_growth", "心理勵志", "做自己的太陽，去看你想看的星星和月亮：幸福路上，50個對自己的訴說、和解與釋懷", "角子", "0011037943", "2025-12-01", ("和解", "釋懷", "幸福")),
    curated_book("02_psychology_growth", "心理勵志", "因為你們，我們相信光：創造抗癌力，設計你的運動菜單", "財團法人台灣癌症基金會", "0011037996", "2025-12-01", ("希望", "抗癌", "生命韌性")),
    curated_book("02_psychology_growth", "心理勵志", "了解自我心理學 漫畫圖解版(全新修訂版)", "Yuuki Yuu", "0011038226", "2025-12-01", ("自我心理學", "心理知識", "自我理解")),
    curated_book("02_psychology_growth", "心理勵志", "跨越脊病，生命前行：脊髓傷友與醫療團隊攜手重建的生命記事", "李政道、傑米、Sam Chang、阿翰等、吳立萍", "0011037669", "2025-11-29", ("生命重建", "支持", "韌性")),
    curated_book("02_psychology_growth", "心理勵志", "奇蹟的起點：透過量子法則，改寫人生", "田畑誠", "0011037304", "2025-11-28", ("信念", "人生改變", "潛意識")),
    curated_book("02_psychology_growth", "心理勵志", "想你時，終於可以笑著流淚：從理解他人、世界到理解自己，關於愛與告別的生死課", "郭憲鴻（小冬瓜）", "0011037403", "2025-11-28", ("告別", "悲傷療癒", "生命教育")),
    curated_book("02_psychology_growth", "心理勵志", "這一生所為何來：麥可．喬丹的人生導師，傳奇教練喬治．瑞夫林的永恆智慧", "喬治．瑞夫林、萊恩．霍利得", "0011037418", "2025-11-28", ("人生智慧", "導師", "使命")),
    curated_book("02_psychology_growth", "心理勵志", "我是不是想太多?關於「隱性高敏感族」", "時田HISAKO", "0011037496", "2025-11-28", ("高敏感", "自我接納", "情緒")),
    curated_book("02_psychology_growth", "心理勵志", "把天聊死，不如把愛聊活：看懂伴侶關係賽局，開展有效溝通的活局對話", "大心診所、王家齊", "0011037393", "2025-11-27", ("伴侶關係", "溝通", "情感界線")),

    curated_book("03_natural_science", "自然科學", "黃金山的召喚：臺灣百萬年大地礦詩——九份、金瓜石、水湳洞時空紀事｜島嶼東北角的礦物熱帶雨林", "黃家俊", "", "", ("礦物", "地質", "臺灣自然史")),
    curated_book("03_natural_science", "自然科學", "超圖解電力電路入門：從電路的性質、分析測量到應用範圍，一本全面學習!", "二宮崇", "0011030333", "", ("電力", "電路", "測量")),
    curated_book("03_natural_science", "自然科學", "流淌臺灣之心：濁水溪空拍誌", "蔡嘉陽", "0011029193", "", ("河川", "地理", "環境")),
    curated_book("03_natural_science", "自然科學", "基礎建設全圖解：秒懂STEM!160張精緻彩圖、50組關鍵詞，掌握超厲害人造設施的運作原理", "格雷迪．希爾豪斯", "0011024588", "", ("STEM", "工程", "基礎建設")),
    curated_book("03_natural_science", "自然科學", "欲望植物園", "麥可‧波倫", "0011023679", "", ("植物", "演化", "人類文化")),
    curated_book("03_natural_science", "自然科學", "海洋博物誌3｜離岸珊瑚礁｜：航向外洋的壯闊湛藍!墾丁、台東、蘭嶼、綠島、龜山島、澎湖南方四島，936種熱帶珊瑚礁生物辨識百科", "李承錄、趙健舜", "0011025773", "", ("海洋", "珊瑚礁", "生物辨識")),
    curated_book("03_natural_science", "自然科學", "邏輯解謎：150+謎題、4週大腦訓練，讓頭腦越玩越靈光!", "葛瑞斯‧摩爾博士", "0011027612", "", ("邏輯", "謎題", "認知訓練")),
    curated_book("03_natural_science", "自然科學", "AI好學圖鑑：全面快速入門", "DK出版社編輯群", "0011029575", "", ("人工智慧", "科技科普", "圖鑑")),
    curated_book("03_natural_science", "自然科學", "向星而生：人類突破極限、飛向太空的故事", "提姆・皮克", "", "2025-12-10", ("太空", "航太", "科學探索")),
    curated_book("03_natural_science", "自然科學", "臺灣猛禽圖鑑", "廖本興", "", "", ("猛禽", "鳥類", "生態")),

    curated_book("04_healthcare", "醫療保健", "明眸再現 眼底病變尖端治療法", "陳珊霓", "0011039732", "2025-12-20", ("眼底病變", "視網膜", "治療")),
    curated_book("04_healthcare", "醫療保健", "糖尿病圖解全攻略，掌握數據背後的潛在風險：早期預防×低碳飲食×運動治療×病後監測，整合臨床經驗與生活指導，實踐可持續的健康管理", "戴霞", "0011038923", "2025-12-11", ("糖尿病", "預防", "健康管理")),
    curated_book("04_healthcare", "醫療保健", "大腦神經兮兮：一位神經內科專家的行醫筆記", "葉宗勲", "0011044284", "2026-02-01", ("神經科", "大腦", "疾病辨識")),
    curated_book("04_healthcare", "醫療保健", "老人健康促進（三版）", "陳雪芬、黃雅文、許維中、姜逸群、張宏哲、陳嫣芬、黃曉令、黃惠瑩、黃純德、林志學、林文元、魏大森、王靜枝、彭晴憶", "0011045504", "2026-02-08", ("健康老化", "高齡照護", "健康促進")),
    curated_book("04_healthcare", "醫療保健", "大腦需要的幸福食物：有效對抗焦慮、健忘、失眠、提升記憶力與性慾，哈佛醫生親身實證的最強食物。", "烏瑪．納多（Uma Naidoo）", "0011042099", "2026-01-27", ("營養精神醫學", "大腦健康", "飲食")),

    curated_book("05_food_wellness", "飲食養生", "世界茶香點心：6大茶文化╳30款經典茶類╳56道甜點飲品，居家製作、創業配方通通有〖附QRCODE影片〗", "宋淑娟（Jane）", "", "2025-12-27", ("茶文化", "點心", "飲品")),
    curated_book("05_food_wellness", "飲食養生", "西餐料理宴客菜", "周文森", "", "2025-12-23", ("西餐", "宴客", "烹飪")),
    curated_book("05_food_wellness", "飲食養生", "金牌團隊不藏私的中式點心全工法：96款經典麵食 米食 甜點，從自家享用到營業接單都適用!", "開平青年發展基金會", "", "2025-12-11", ("中式點心", "麵食", "米食")),
    curated_book("05_food_wellness", "飲食養生", "幸福素食餐桌：營養師團隊為全家人量身打造70道健康蔬食!", "台北慈濟醫院總務室營養組", "0011042448", "2026-01-22", ("素食", "營養", "家庭料理")),
    curated_book("05_food_wellness", "飲食養生", "全肉料理：125道高蛋白質食譜，找到原型食物的最佳飲食搭配", "艾許萊．萬霍頓、貝絲．利普頓", "", "2025-12-08", ("高蛋白", "原型食物", "肉料理")),

    curated_book("06_computer_info", "電腦資訊", "知道你的下一筆訂單 - 使用LLM", "梁志遠、韓曉晨", "0011039440", "2025-12-19", ("LLM", "資料分析", "預測")),
    curated_book("06_computer_info", "電腦資訊", "深入淺出Python 第三版", "Paul Barry", "0011039495", "2025-12-19", ("Python", "程式設計", "實作")),
    curated_book("06_computer_info", "電腦資訊", "精通JavaScript 第四版", "Marijn Haverbeke", "0011039496", "2025-12-19", ("JavaScript", "程式設計", "Web")),
    curated_book("06_computer_info", "電腦資訊", "內行人才知道的生成式 AI系統設計面試指南", "Ali Aminian、Hao Sheng", "0011039497", "2025-12-19", ("生成式AI", "系統設計", "面試")),
    curated_book("06_computer_info", "電腦資訊", "史上最完整 - 一本書晉升深度學習世界級大師", "王成、黃曉輝", "0011039543", "2025-12-19", ("深度學習", "神經網路", "AI")),

    curated_book("07_other", "其他", "暗網惡帝：直擊全球最大器官交易、毒品走私、軍火買賣帝國絲路偵查全紀錄", "尼克・比爾頓", "0011017144", "", ("暗網", "犯罪調查", "全球化")),
    curated_book("07_other", "其他", "你玩遊戲，還是遊戲玩你?：一場無法登出的遊戲，公司、政府和學校如何利用遊戲來控制我們所有人", "安瑞恩．韓", "0010985100", "", ("遊戲化", "社會控制", "科技文化")),
    curated_book("07_other", "其他", "AI底層真相：如何避免數位滲透的陰影", "穆吉亞", "0011004062", "", ("AI倫理", "數位社會", "科技風險")),
    curated_book("07_other", "其他", "再玩個一關就好了：關不掉遊戲不是你的錯，那些潛藏在電玩之中的心理學效應", "傑米．麥迪根", "0011000984", "", ("電玩", "心理學", "行為設計")),
    curated_book("07_other", "其他", "電玩哲學", "朱家安", "0011001592", "", ("哲學", "電玩文化", "思辨")),
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
