from __future__ import annotations

import findbook_batch_20260716_b13 as batch


FROM_DATE = "2026-06-19"
TO_DATE = "2026-07-18"
WORK_ID = "findbook-20260718-121027"

CANDIDATES = {
    "01_business_startup": (
        (
            "AI時代的一人創業 x 人生整理：從外在創業經營，到內在心靈覺醒的自我實現【獨家套書】",
            "洪儒明 MING HUNG,流川美加",
            "2026-07-01",
            "https://www.books.com.tw/products/0011056445",
        ),
        (
            "史蒂文.巴列特著作限量套書《快樂性感的百萬富翁》+ 《執行長日記【耀黑燙金版】》",
            "史蒂文．巴列特 Steven Bartlett",
            "2026-06-26",
            "https://www.books.com.tw/products/0011055057",
        ),
        (
            "在雲之上的帕蘭提爾：改變戰爭與世界的AI祕密力量Palantir",
            "林冠群",
            "2026-06-24",
            "https://www.books.com.tw/products/0011055370",
        ),
        (
            "比特幣 風雲再起",
            "Zac W、Dave C",
            "2026-06-20",
            "https://www.books.com.tw/products/0011055757",
        ),
        (
            "加密貨幣投資聖經：從開戶、選幣、DeFi 到風險管理的全方位指南",
            "Zac W、Dave C",
            "2026-06-20",
            "https://www.books.com.tw/products/0011055758",
        ),
        (
            "選擇權操作全攻略 實戰演練-單式部位、價差策略與期貨避險應用",
            "Dave C、吳西蒙、Amber",
            "2026-06-20",
            "https://www.books.com.tw/products/0011055759",
        ),
        (
            "AI一人公司：OpenClaw龍蝦兵團養成記",
            "曾任偉，秋葉，秦陽",
            "",
            "https://www.books.com.tw/products/CN18097253",
        ),
        (
            "AI一人公司：128種商業模式與盈利實操",
            "胡華成，雷鳴，徐捷",
            "",
            "https://www.books.com.tw/products/CN18097887",
        ),
        (
            "零基礎學MACD指標：背離技術分析、波段交易技巧與短線操盤實戰",
            "馭龍識黑馬",
            "",
            "https://www.books.com.tw/products/CN18098950",
        ),
        (
            "大數據財務分析：基於新道DBE Cloud",
            "鍾愛軍，黃楠，李愛琴",
            "",
            "https://www.books.com.tw/products/CN18102185",
        ),
        (
            "Stata計量經濟學與實證研究應用",
            "張甜",
            "",
            "https://www.books.com.tw/products/CN18102513",
        ),
        (
            "降本增效實戰：美的“3+4”卓越運營體系",
            "陳凱歌著",
            "",
            "https://www.books.com.tw/products/CN18104881",
        ),
        (
            "金融GPT：人工智能與全球經濟安全",
            "（美）詹姆斯·里卡茲",
            "",
            "https://www.books.com.tw/products/CN18105538",
        ),
        (
            "OpenClaw時代的OPC：一人公司從0到1方法論",
            "寒樹，秋葉，易洋，吳迪，劉海峰",
            "",
            "https://www.books.com.tw/products/CN18112320",
        ),
        (
            "銀行轉型2035：邁向智能體銀行的範式躍遷",
            "何大勇,孫中東,譚彥",
            "",
            "https://www.books.com.tw/products/CN18098388",
        ),
        (
            "中國近代對外貿易管理制度史研究(1840-1949)",
            "張國義",
            "",
            "https://www.books.com.tw/products/CN18114954",
        ),
        (
            "AI時代創新法則：AI RaaS模式重新定義企業",
            "劉燕,彭志強",
            "",
            "https://www.books.com.tw/products/CN18096176",
        ),
        (
            "證券暨期貨月刊(44卷7期115/07)",
            "金融監督管理委員會證期局",
            "2026-07-16",
            "https://www.books.com.tw/products/0011058266",
        ),
        (
            "農業部農業金融署114年年報",
            "農業部農業金融署",
            "2026-07-01",
            "https://www.books.com.tw/products/0011056955",
        ),
        (
            "組織發展與變革(12版)：(Cummings/Organization Development & Change 12e)",
            "陳以亨",
            "2026-06-25",
            "https://www.books.com.tw/products/0011057056",
        ),
    ),
    "02_psychology_growth": (
        (
            "健康社交說明書：人際連結的藝術與科學，哈佛社會學家用「5-3-1法則」打開人生快樂關鍵【鸚鵡螺圖書獎金獎】",
            "卡斯利˙基蘭",
            "2026-07-18",
            "https://www.books.com.tw/products/0011055740",
        ),
        (
            "TPI天賦人格卡帶給我的指引(附202張TPI天賦人格卡+指引手冊+典藏牌卡盒)",
            "天賦人格研究院,玩轉牌卡機構",
            "2026-07-17",
            "https://www.books.com.tw/products/0011057722",
        ),
        (
            "意識如何湧現?：從神經科學到精神分析，探索心靈的隱藏泉源",
            "馬克．索姆斯 (Mark Solms)",
            "2026-07-15",
            "https://www.books.com.tw/products/0011057438",
        ),
        (
            "【宇宙就想對你好】系列：你想要的一切，宇宙早已為你預備+宇宙安排的一切，都是通往豐盛人生的祕密(套書共二冊)",
            "克里斯．普倫提斯（Chris Prentiss）",
            "2026-07-08",
            "https://www.books.com.tw/products/0011056470",
        ),
        (
            "做自己的珍珠：把你的不一樣，磨成耀眼的光",
            "凱凱 Kaikai Chou",
            "2026-06-26",
            "https://www.books.com.tw/products/0011054740",
        ),
        (
            "「想太多」只會偷走快樂：跳脫情緒鏈的思維陷阱!折磨你的從來不是事情本身，而是失控的內心戲",
            "理察．卡爾森博士（Ph.D. Richard Carlson）",
            "2026-06-26",
            "https://www.books.com.tw/products/0011054799",
        ),
        (
            "心靈化學：「吸引力法則之父」最核心的思想精隨",
            "查爾斯‧哈奈爾(Charles F. Haanel)",
            "2026-06-25",
            "https://www.books.com.tw/products/0011054229",
        ),
        (
            "心靈天氣圖：146則陪你理解情緒與人生的溫柔提醒",
            "河合隼雄",
            "2026-06-25",
            "https://www.books.com.tw/products/0011053587",
        ),
        (
            "讓孩子的「強項」發光：運用5大氣質診斷與35個實踐方法，發掘孩子的天賦優勢，培養提問力、內驅力與共感",
            "船津徹",
            "2026-06-26",
            "https://www.books.com.tw/products/0011054750",
        ),
        (
            "新哲人(07)：敢於脆弱的勇氣",
            "澳大利亞新哲人編輯部",
            "",
            "https://www.books.com.tw/products/CN18105081",
        ),
        (
            "數位時代的情緒療癒：在過載的情緒疲勞中練習排毒，得到真正的休息",
            "潔西卡‧豪爾Jessica Howard",
            "2026-06-24",
            "https://www.books.com.tw/products/0011055186",
        ),
        (
            "OH卡讀心術(新版)",
            "曹春燕",
            "2026-07-01",
            "https://www.books.com.tw/products/0011052995",
        ),
        (
            "你不睡，貓都知道",
            "Juno주노",
            "2026-07-14",
            "https://www.books.com.tw/products/0011056683",
        ),
        (
            "我沒有成為很厲害的大人",
            "5m",
            "2026-07-07",
            "https://www.books.com.tw/products/0011055362",
        ),
        (
            "意志薄弱狗：把煩惱交給明天的自己",
            "San-X株式會社",
            "2026-07-04",
            "https://www.books.com.tw/products/0011055741",
        ),
        (
            "迷航狐狸夢：快樂不迷航—一位父親給孩子的五則睡後小寓言&六堂快樂智商課(雙書封.雙向閱讀)",
            "葉向林Noah",
            "2026-06-30",
            "https://www.books.com.tw/products/0011054642",
        ),
        (
            "SEL解憂小學堂3：我真的不想開學!",
            "鄒敦怜",
            "2026-07-10",
            "https://www.books.com.tw/products/0011055549",
        ),
        (
            "SEL解憂小學堂4：我才沒有愛生氣!",
            "鄒敦怜",
            "2026-07-10",
            "https://www.books.com.tw/products/0011055550",
        ),
        (
            "一點點勇氣【SEL情緒素養繪本|害怕|陪伴|自我認同】勇氣不是不害怕，而是帶著顫抖依然選擇前進",
            "克萊兒．亞歷珊卓",
            "2026-07-04",
            "https://www.books.com.tw/products/0011055732",
        ),
        (
            "一點點尊重【SEL情緒素養繪本|人際|界線|自我認同】尊重不需要委屈求全，是我有權利說不，而你願意聽見",
            "克萊兒．亞歷珊卓",
            "2026-07-04",
            "https://www.books.com.tw/products/0011055733",
        ),
    ),
    "03_natural_science": (
        (
            "邊看漫畫邊解謎!144題算術大挑戰",
            "橫山明日希",
            "2026-07-17",
            "https://www.books.com.tw/products/0011056686",
        ),
        (
            "妙醫Why博士4",
            "林季融,許雅筑",
            "2026-07-15",
            "https://www.books.com.tw/products/0011055778",
        ),
        (
            "妙醫Why博士3",
            "林季融,許雅筑",
            "2026-07-15",
            "https://www.books.com.tw/products/0011055779",
        ),
        (
            "漫畫大英百科【生物地科20】：氣候異常",
            "BomBom Story",
            "2026-07-10",
            "https://www.books.com.tw/products/0011055552",
        ),
        (
            "昆蟲大競賽",
            "Macmillan Children’s Books",
            "2026-07-05",
            "https://www.books.com.tw/products/0011054770",
        ),
        (
            "無人機空拍應用於路段交通衝突分析(2/2)–路側交通衝突[115綠]",
            "溫基信、王宏生、高郁承、陳濬得、黃家耀、胡守任、蘇志文、黃明正、喻世祥、黃耀緯",
            "2026-07-01",
            "https://www.books.com.tw/products/0011057478",
        ),
        (
            "橋梁檢測輔助工具精進之研究(2/2)-建立橋梁多時期劣化比對技術[115橘]",
            "饒見有、林昭宏、劉光晏、李志清、李易唐、賴威伸、胡智超",
            "2026-07-01",
            "https://www.books.com.tw/products/0011057473",
        ),
        (
            "Microelectronics: Circuit Analysis and Design 5/e/ Neamen 微電子學：電路分析與設計導讀本",
            "Donald A. Neamen,Phyllis R. Nelson原著; 曾宗亮導讀",
            "2026-06-22",
            "https://www.books.com.tw/products/0011056433",
        ),
        (
            "COMSOL百識通",
            "吳細秀，侯慧，羅義新",
            "",
            "https://www.books.com.tw/products/CN18105054",
        ),
        (
            "對手與權威：古代希臘與古代中國的科學和思想",
            "（英）G·E·R.勞埃德",
            "",
            "https://www.books.com.tw/products/CN18110946",
        ),
    ),
    "04_healthcare": (
        (
            "為0~3歲嬰幼兒健康把關，餵食×發燒×意外預防×用藥×居家照顧×異位性皮膚炎×過敏性鼻炎×氣喘×過敏性結膜炎 套書(共2本)",
            "江伯倫,蘇一宇",
            "2026-07-16",
            "https://www.books.com.tw/products/0011056693",
        ),
        (
            "本草備要點評本(POD)",
            "【清】汪昂原著,蒲團子 點評,蒲曉博 參訂",
            "2026-06-26",
            "https://www.books.com.tw/products/0011054563",
        ),
        (
            "每一次敲響，都是為了讓你遇見更好的自己",
            "楊裕仲(Leo)",
            "2026-06-20",
            "https://www.books.com.tw/products/0011054523",
        ),
        (
            "AI賦能醫療",
            "（意）丹尼爾·卡利喬雷（DANIELE CALIGIORE）",
            "",
            "https://www.books.com.tw/products/CN18112876",
        ),
        (
            "中國接骨學(CO)的臨床實踐與智能接骨術(IO)的探索",
            "成永忠，溫建民，陳偉（主編）",
            "",
            "https://www.books.com.tw/products/CN18102713",
        ),
    ),
    "05_food_wellness": (
        (
            "超萌人氣造型餐X夢幻便當：步驟全圖解X料理輕鬆配X圖稿照著做，讓孩子忍不住就吃光光的可愛食譜110+【隨書附造型圖稿】",
            "Kana,陳琪",
            "2026-07-18",
            "https://www.books.com.tw/products/0011056923",
        ),
        (
            "南青山「UN GRAIN」的燒菓子：一口精緻小巧的極上風味",
            "UN GRAIN",
            "2026-07-10",
            "https://www.books.com.tw/products/0011056799",
        ),
        (
            "大廚不外傳の黃金比例調醬祕訣801：熱銷上萬冊，增量升級版!主廚們的私藏調味公式，讓家常料理升等餐廳美味",
            "學研編輯部",
            "2026-06-25",
            "https://www.books.com.tw/products/0011053735",
        ),
        (
            "5分鐘味噌湯療(暢銷改版)：簡單╳省時╳對症~用114道料多味美的味噌湯喝出每日健康",
            "大友育美",
            "2026-06-25",
            "https://www.books.com.tw/products/0011054697",
        ),
        (
            "風土品酒學：失傳200年的地感品鑑技藝復興",
            "邱奕翔",
            "2026-06-23",
            "https://www.books.com.tw/products/0011054304",
        ),
    ),
    "06_computer_info": (
        (
            "SDD實戰：規範驅動開發之道",
            "黃佳",
            "",
            "https://www.books.com.tw/products/CN18114772",
        ),
        (
            "數據結構教程(微課視頻·題庫·AI賦能版)(第7版)(附練習冊)",
            "李春葆（主編）",
            "",
            "https://www.books.com.tw/products/CN18113857",
        ),
        (
            "Windows安全內幕：身份驗證、授權與審計(AAA)核心技術詳解",
            "（英）詹姆斯·福肖",
            "",
            "https://www.books.com.tw/products/CN18114812",
        ),
        (
            "AIGC賦能AutoCAD輔助設計",
            "徐穎，周黎黎，韓雪（主編）",
            "",
            "https://www.books.com.tw/products/CN18097563",
        ),
        (
            "LLaMA+ChatGLM大模型實戰",
            "薛棟",
            "",
            "https://www.books.com.tw/products/CN18097685",
        ),
    ),
    "07_other": (
        (
            "圖解世界5大神話：從日本、印度、中東、希臘到北歐，65個主題解讀東西方神祇與傳說、信仰與世界觀",
            "中村圭志",
            "2026-07-15",
            "https://www.books.com.tw/products/0011056857",
        ),
        (
            "新「聞」時代--海上報刊與晚清文人的知識重構(1853-1889)",
            "黃龍彬",
            "2026-07-15",
            "https://www.books.com.tw/products/0011057434",
        ),
        (
            "VTuber學：虛擬角色/真實靈魂，全面解析席捲網路世代的文化現象",
            "吉川慧,山野弘樹,岡本健",
            "2026-07-09",
            "https://www.books.com.tw/products/0011055746",
        ),
        (
            "殺人魔名冊【暢銷紀念版】：全球150名極惡連環殺手檔案",
            "傑克˙羅斯伍德（Jack Rosewood）、蕾貝卡．洛 (Rebecca Lo)",
            "2026-07-08",
            "https://www.books.com.tw/products/0011056466",
        ),
        (
            "大不列顛小心機：搞定英國人的25條金律",
            "讀者太太Mrs Reader",
            "2026-07-07",
            "https://www.books.com.tw/products/0011055368",
        ),
    ),
}


def load_candidate_pools():
    batch.FROM_DATE = FROM_DATE
    batch.TO_DATE = TO_DATE
    batch.WORK_ID = WORK_ID
    return CANDIDATES


batch.FROM_DATE = FROM_DATE
batch.TO_DATE = TO_DATE
batch.WORK_ID = WORK_ID
batch.EXTRA_POOLS = CANDIDATES
batch.load_candidate_pools = load_candidate_pools


if __name__ == "__main__":
    batch.main()
