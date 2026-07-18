from __future__ import annotations

import findbook_batch_20260716_b13 as batch


FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-18"
WORK_ID = "findbook-20260718-122056-b2"

CANDIDATES = {
    "01_business_startup": (
        (
            "拆商：解決人生99%難題的底層思維，專為上班族、創業者與追求自我成長者打造的問題解決實戰指南",
            "王奕迪",
            "",
            "https://www.books.com.tw/products/0011055537",
        ),
        (
            "數據對了，為什麼你還是輸了？：【數據告訴你發生什麼，人性告訴你為什麼發生】看懂數字背後的動機、偏誤與選擇，破解最棘手的商業難題",
            "克利斯汀．麥茲伯格,米克爾．拉斯穆森",
            "",
            "https://www.books.com.tw/products/0011056589",
        ),
        (
            "金融泡沫的底層邏輯，約翰．勞與密西西比狂熱：發行準備金×銀行券流通，對股票的期望大於價值，信用從交易工具變成投機燃料",
            "[英]約翰．勞（John Law）著,伊莉莎編譯",
            "",
            "https://www.books.com.tw/products/0011056753",
        ),
        (
            "可以努力，但別太用力！艾默生的效率管理十二原則：檢查目標、責任、作業方法與獎酬制度，拆解現代職場常見的低效率來源，讓好成果不再只靠盲目努力",
            "[美]哈林頓．艾默生（Harrington Emerson）著,伊莉莎編譯",
            "",
            "https://www.books.com.tw/products/0011056754",
        ),
        ("像巴菲特一樣看見機會", "管唯中編著", "", "https://www.books.com.tw/products/0011055770"),
        ("把別人的NO，變成你的YES", "林郁／主編", "", "https://www.books.com.tw/products/0011055814"),
        (
            "致富不是暴富的幻想！華勒斯．華特斯談財富科學：金錢信念×行動秩序×價值創造，從羞愧、匱乏與焦慮中找回人生選擇權",
            "[美]華勒斯．華特斯（Wallace Wattles）著,伊莉莎編譯",
            "",
            "https://www.books.com.tw/products/0011055684",
        ),
        (
            "GDP成長肥到誰？李嘉圖帶你讀懂房價、薪資、稅負與全球貿易的成本轉嫁：從生活成本到薪資報酬，從企業獲利到全球貿易，揭開經濟成長背後的利益流向",
            "[英]大衛．李嘉圖（David Ricardo）著,伊莉莎編譯",
            "",
            "https://www.books.com.tw/products/0011055685",
        ),
        (
            "縱橫：《戰國策》教我的人生逆襲術(限量親簽版)",
            "胡川安",
            "",
            "https://www.books.com.tw/products/0011055270",
        ),
        (
            "別把你的錢留到死【博客來獨家限量燙金書衣】：懂得花錢，是最好的投資——理想人生的9大財務思維",
            "比爾‧柏金斯",
            "",
            "https://www.books.com.tw/products/0011054749",
        ),
        ("洛克菲勒自傳 2版", "洛克菲勒", "", "https://www.books.com.tw/products/0011055255"),
        ("世界是不平衡的-無所不在的80/20", "帕雷托", "", "https://www.books.com.tw/products/0011055257"),
        (
            "讓努力變值錢，巴納姆的二十條致富法則：能力圈×市場位置×信用累積，避開越勤奮越窮困的收入陷阱",
            "[美]P. T. 巴納姆（P. T. Barnum）著,伊莉莎編譯",
            "",
            "https://www.books.com.tw/products/0011055070",
        ),
        (
            "人生的五種財富【實作練習本】：打造屬於你的夢想人生，時間、社會、心理、身體、金錢財富，全方位升級",
            "薩希．布魯姆",
            "",
            "https://www.books.com.tw/products/0011054285",
        ),
        (
            "從新主管到頂尖主管 實戰版：全球頂尖商學院必讀轉職聖經，九十天完美因應轉職、升遷、空降與接班挑戰",
            "麥克．瓦金斯",
            "",
            "https://www.books.com.tw/products/0011054318",
        ),
        (
            "上流老人退休寶典：從容瀟灑過晚年的十二堂課",
            "葉美麗,吳俊德",
            "",
            "https://www.books.com.tw/products/0011054308",
        ),
        (
            "理財關鍵100：學校不會教，簡單易學，為自己開創複利人生！",
            "葉怡成",
            "",
            "https://www.books.com.tw/products/0011054371",
        ),
        (
            "人生的五種財富【實踐套書】（《人生的五種財富》+《人生的五種財富【實作練習本】》共兩冊）",
            "薩希．布魯姆",
            "",
            "https://www.books.com.tw/products/0011054314",
        ),
        (
            "思考致富：全球3億人瘋傳的財富翻倍公式",
            "拿破崙．希爾",
            "",
            "https://www.books.com.tw/products/0011054508",
        ),
        (
            "人腦與AI腦的新協作革命：從分析師到創造者的工作模式根本改變",
            "陳永隆,曾憲鈺,蔡承佳",
            "",
            "https://www.books.com.tw/products/0011053646",
        ),
    ),
    "02_psychology_growth": (
        (
            "黑色情緒【限量附贈讀懂我的心．情緒貼紙乙張】：我會陪著你，釐清隱藏在內心的70種真實感受",
            "Seolleda 崔敏正",
            "",
            "https://www.books.com.tw/products/0011056861",
        ),
        (
            "不內傷、不吃虧，難搞魔人應對二部曲【對付難搞魔人的不內傷心理學＋對付難搞魔人的不吃虧回話術】",
            "齊藤勇,司拓也",
            "",
            "https://www.books.com.tw/products/0011056585",
        ),
        (
            "想死不如健身！改變一生的超科學理由：破除99％肌力訓練迷思找到堅持健身的意義，用肌肉治癒人生的最強動力手冊【暢銷紀念版】",
            "泰史特龍,久保孝史",
            "",
            "https://www.books.com.tw/products/0011055925",
        ),
        ("風月同天（上下冊不分售）", "慈濟人文志業中心", "", "https://www.books.com.tw/products/0011055824"),
        (
            "縫隙之歌（獨家作者祝福簽繪版）：在放逐與解放間漂泊，活在邊緣之存在的質問",
            "洪承喜（홍칼리）",
            "",
            "https://www.books.com.tw/products/0011055278",
        ),
        (
            "豐富人生：一位醫生筆記及體驗分享",
            "黎炳民",
            "",
            "https://www.books.com.tw/products/0011056432",
        ),
        (
            "如何用話語救活老公：即使有時候你只想掐死他",
            "安・威爾森,戴夫・威爾森",
            "",
            "https://www.books.com.tw/products/0011055822",
        ),
        (
            "當你過了45歲：健康、職涯、財務、法律，必須按齡知道的事",
            "康哲偉",
            "",
            "https://www.books.com.tw/products/0011055376",
        ),
        (
            "直視死亡，你會更明白「怎麼活」：《當呼吸化為空氣》＋《死亡的臉》",
            "保羅．卡拉尼提,許爾文．努蘭",
            "",
            "https://www.books.com.tw/products/0011054643",
        ),
        (
            "再難過，也終會度過：總有那些迷惘、不知所措的時刻──給不知不覺成為大人的你（限量作者親簽版）",
            "吳若權",
            "",
            "https://www.books.com.tw/products/0011055306",
        ),
        (
            "在落地之處開花【暢銷300萬冊，日本勵志經典】：無論在何種境遇，你都能閃耀發光（新修版）",
            "渡邊和子",
            "",
            "https://www.books.com.tw/products/0011054747",
        ),
        (
            "家人使用說明書【暢銷新修版】：腦科學專家寫給總是被家人一秒惹怒的你",
            "黑川伊保子",
            "",
            "https://www.books.com.tw/products/0011054744",
        ),
        (
            "退休後的孤獨入門：重建不受公司定義的人生意義",
            "河合薰",
            "",
            "https://www.books.com.tw/products/0011054654",
        ),
        (
            "做自己的珍珠【作者親簽＋限量版珍煮丹╳珍奶小姐「珍珠奶茶」兌換珍藏卡】：把你的不一樣，磨成耀眼的光",
            "凱凱 Kaikai Chou",
            "",
            "https://www.books.com.tw/products/0011054751",
        ),
        (
            "覺悟的力量：超譯安倍晉三精神教父「吉田松陰」的人生格言",
            "池田貴將",
            "",
            "https://www.books.com.tw/products/0011054656",
        ),
        (
            "重縫人生：從罹患腦瘤、市場一坪小攤到國際伸展台，她為人生重新打版，將生命的傷口縫成了美麗的翅膀。",
            "夏筱琴",
            "",
            "https://www.books.com.tw/products/0011054743",
        ),
        ("最初的你，早已足夠", "李瑜 Yu Lee", "", "https://www.books.com.tw/products/0011054203"),
        ("我的父母竟然成了老害", "西野みや子", "", "https://www.books.com.tw/products/0011054783"),
        (
            "【誰在讓你失控？】駕馭多巴胺，打造最強大腦行動力：不靠意志力！用行為科學找回專注與自控",
            "安納斯塔西雅．赫羅尼斯",
            "",
            "https://www.books.com.tw/products/0011055141",
        ),
        (
            "我想了解身心科：身心科醫生寫給全家人，認識疾病、看診、治療、用藥的實用指南",
            "莊節一",
            "",
            "https://www.books.com.tw/products/0011055013",
        ),
    ),
    "03_natural_science": (
        ("超好懂圖解遺傳10堂課", "瑪麗安‧泰勒", "", "https://www.books.com.tw/products/0011056914"),
        (
            "全知睿寶＆輝寶視角1【首刷限量贈品「你好，我是睿寶」證件卡】：睿智又閃耀的出生日記，愛寶樂園官方授權！",
            "宋永寬,柳汀勳─攝影",
            "",
            "https://www.books.com.tw/products/0011055465",
        ),
        (
            "全知睿寶＆輝寶視角2【首刷限量贈品「你好，我是輝寶」證件卡】：睿智又閃耀的成長冒險，愛寶樂園官方授權！",
            "宋永寬,柳汀勳─攝影",
            "",
            "https://www.books.com.tw/products/0011055466",
        ),
        (
            "寶家族雙胞胎成長全紀錄套書【博客來獨家甜夢版】：《全知睿寶＆輝寶視角1》+《全知睿寶＆輝寶視角2》+博客來獨家寫真拼貼小卡",
            "宋永寬,柳汀勳─攝影",
            "",
            "https://www.books.com.tw/products/0011055467",
        ),
        (
            "寶家族雙胞胎成長全紀錄套書【首刷限量搗蛋版】：《全知睿寶＆輝寶視角1》+《全知睿寶＆輝寶視角2》+首刷限定寫真拼貼小卡",
            "宋永寬,柳汀勳─攝影",
            "",
            "https://www.books.com.tw/products/0011055468",
        ),
        (
            "儲能產業政策與典型專案案例解析",
            "岳芬,陳海生,劉為等編著",
            "",
            "https://www.books.com.tw/products/0011053980",
        ),
        (
            "哎呦！我的身體：我與我身體之間的那些事",
            "阿克塞爾・哈克",
            "",
            "https://www.books.com.tw/products/0011053088",
        ),
        (
            "機智人類的自然生活公約：從城市到山川海洋，不可不知的法律規則",
            "一日一種",
            "",
            "https://www.books.com.tw/products/0011052413",
        ),
        (
            "我家狗狗是天生偵探（限量特典：神鼻偵探養成卡）：10週嗅聞遊戲，解放毛孩的鼻子天賦",
            "雷雷",
            "",
            "https://www.books.com.tw/products/0011052532",
        ),
        (
            "多巴胺聖經：為什麼生活越刺激反而越空虛？自律神經失控了！三階段重設大腦快樂系統",
            "安澈雨안철우",
            "",
            "https://www.books.com.tw/products/0011052863",
        ),
    ),
    "04_healthcare": (
        (
            "先看見人，再談看不見的病：台灣精神醫療照護現場的思辨，從「機構全控」面向「公民賦權」的社區實踐，體悟標籤下的真實生命",
            "鄭淦元",
            "",
            "https://www.books.com.tw/products/0011054841",
        ),
        (
            "過敏、肥胖或憂鬱？其實是腸道菌在抗議！日本醫學教授公開最新腸道菌研究，教你養出不生病的好菌體質",
            "內藤裕二,小林弘幸,中島淳",
            "",
            "https://www.books.com.tw/products/0011056916",
        ),
        (
            "戰勝癌症：從恐懼到希望，科學與生活的雙重智慧",
            "Kevin Chen 著",
            "",
            "https://www.books.com.tw/products/0011055548",
        ),
        (
            "中醫藥食療手冊4：食養日常 高尿酸與痛風的中醫藥防治指南",
            "區靖彤主編",
            "",
            "https://www.books.com.tw/products/0011056430",
        ),
        (
            "她所在的山谷：豐盛、富足，鄉村醫師的生命餽贈",
            "波莉・莫蘭",
            "",
            "https://www.books.com.tw/products/0011055439",
        ),
    ),
    "05_food_wellness": (
        (
            "好好吃飯，一鍋就好：微微蔡的66道驚艷又簡單的原味料理【博客來獨家贈品版】",
            "微微蔡",
            "",
            "https://www.books.com.tw/products/0011056355",
        ),
        (
            "歡迎入座：12位主廚的極致餐桌，台灣精緻餐飲黃金10年：Welcome to the Table: Taiwan’s Golden Decade of Fine Dining",
            "高琹雯",
            "",
            "https://www.books.com.tw/products/0011051131",
        ),
        (
            "復刻台日老麵包：活用液種、中種、燙種 揉出最柔軟的經典滋味",
            "史惠麟,徐銓蔚",
            "",
            "https://www.books.com.tw/products/0011053302",
        ),
        (
            "高蛋白低碳水減重料理：0失敗0壓力，狂瘦22kg不復胖的87道美味瘦身食譜",
            "Mini 朴祉禹",
            "",
            "https://www.books.com.tw/products/0011055187",
        ),
        (
            "解酒料理：喝得像失去國家的人的隔天早晨",
            "蜜柑",
            "",
            "https://www.books.com.tw/products/0011054839",
        ),
    ),
    "06_computer_info": (
        (
            "全民版AI識讀：原理、應用、幻覺與誤區（作者親簽版）",
            "彭明輝",
            "",
            "https://www.books.com.tw/products/0011056700",
        ),
        (
            "一本搞定Open Claw：不會寫程式的人，怎麼讓AI幫你把事情做完？",
            "邱閔渝（Marc）",
            "",
            "https://www.books.com.tw/products/0011056669",
        ),
        (
            "室內製圖解剖：平面圖｜空間邏輯×圖面判斷×配置實務",
            "留美幸",
            "",
            "https://www.books.com.tw/products/0011055649",
        ),
        (
            "OpenClaw超級龍蝦煉金術：活用Skills×Channels打造自動化的高效AI助理",
            "劉滄碩",
            "",
            "https://www.books.com.tw/products/0011055592",
        ),
        (
            "ERP企業資源規劃實務｜AI智慧應用",
            "林文恭,中華企業資源規劃(ERP)學會",
            "",
            "https://www.books.com.tw/products/0011055010",
        ),
    ),
    "07_other": (
        (
            "台灣的李登輝時代：意外國度的重塑【限量作家親簽版】",
            "林孝庭",
            "",
            "https://www.books.com.tw/products/0011057570",
        ),
        (
            "嘉義被看見了：從土地到天空的閃耀",
            "許喻理",
            "",
            "https://www.books.com.tw/products/0011055629",
        ),
        (
            "被出賣的台灣：經典譯校版",
            "葛超智",
            "",
            "https://www.books.com.tw/products/0011056293",
        ),
        (
            "第二性（法文直譯繁體中文全譯本，三冊全新校訂版【唯一收錄萬言譯序】）",
            "西蒙．德．波娃",
            "",
            "https://www.books.com.tw/products/0011056117",
        ),
        (
            "在看板對面，聽見人生：方念華",
            "方念華",
            "",
            "https://www.books.com.tw/products/0011056991",
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
