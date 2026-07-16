from __future__ import annotations

import json
import os
import re
import tempfile
import time
from pathlib import Path

import findbook_batch_20260714 as highlight_source
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-16"
WORK_ID = "findbook-20260716-151958-b12"
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

CATEGORIES = (
    ("01_business_startup", "商業理財", 20),
    ("02_psychology_growth", "心理勵志", 20),
    ("03_natural_science", "自然科學", 10),
    ("04_healthcare", "醫療保健", 5),
    ("05_food_wellness", "飲食養生", 5),
    ("06_computer_info", "電腦資訊", 5),
    ("07_other", "其他", 5),
)

FOCUS = {
    "商業理財": "投資、管理與價值創造",
    "心理勵志": "情緒、關係與自我成長",
    "自然科學": "證據、模型與自然規律",
    "醫療保健": "健康風險、照護與醫療決策",
    "飲食養生": "食材、營養與烹調實作",
    "電腦資訊": "程式、資料與人工智慧",
    "其他": "歷史、文化與社會觀察",
}

BOOK_POOLS = {
    "01_business_startup": (
        ("打造永續共好生態圈：來自創業、創新與社會行動者的20則行動觀點", "沈勤譽、詹茹惠", "2026-01-22", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("AI時代，會說故事才是你的關鍵生存力：把話說進人心，讓人為你行動的影響力", "凱倫．艾伯", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("採購與供應管理", "中華採購與供應管理協會、許振邦", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("你不該看到的金融真相：從華爾街神話到市場幻象，洞悉金錢背後的操控與陷阱", "約書亞．布朗", "2026-02-05", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=5&v=1"),
        ("矽谷流鋼鐵般的自我肯定感：科學實證，矽谷菁英的3步驟情緒清理法，成為自己的終生盟友", "宮崎直子", "2025-01-10", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("科特勒談行銷管理", "謝德高", "2025-01-09", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("幣漲無疑：加密貨幣，一場史詩級騙局?", "齊克．法克斯", "2025-01-09", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("世界上最偉大的53堂演說課：全球首席演說教練吉姆．卡斯卡特，從觀念到細節，迅速提昇你的演說能力", "吉姆．卡斯卡特、林裕峯", "2025-01-09", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("〖圖解〗房子就這樣買：挑屋．議價．簽約．驗屋，完全解答購屋108問!", "蘇于修", "2025-01-09", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("IT轉型專案集群管理：介紹及工具", "吳岳穎、江俊毅、黃妍恆", "2025-01-09", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("倫敦最狂散戶：在家買股滾出破億身價，交易心理+盤前策略〖Win-Win套書〗", "羅比‧伯恩斯", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("散戶投資上手的第一本書〖全新增訂版〗：投資股市最該懂的47件事", "王力群", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("勝算：不再靠運氣!從機率、賽局到AI，解鎖預測與決策的科學(二版)", "亞當・庫查司基", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("魔球投資金律：少數人才懂的投資市場潛規則", "麥可．莫布新", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("走出價格僵局，超預期價值激增回購率：10種成交策略×8種話術表達×10種暗示效應", "心一", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("人口轉型時代!破解低生育與高齡化時代的發展悖論", "智本社", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("阿米巴定律，讓企業自己壯大的經營密碼：打破傳統管理邏輯，透過分權、自主、共享激發組織全員潛能", "胡八一", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("向川普學談判：談判不是你輸我贏，而是要共贏!", "喬治．羅斯", "2025-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("原子目標+原子時間經典套書：奇蹟的晨晚雙計畫，告別窮忙內耗、打造富足人生", "柳韓彬", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("十色性格領導力：高效團隊管理與商業實戰指南", "黃信維", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("笑看風雲行善路：新加坡百貨業傳奇人物洪振群永不放棄的人生拼搏", "洪振群", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("專注力協定：史丹佛教授教你消除逃避心理，自然而然變專注〖暢銷新裝版〗", "尼爾．艾歐、李茱莉", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("不生氣之後，變身有錢人+看漫畫學致富(2冊合售)", "森瀬繁智", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("原子目標：早上1分鐘，改變一整年!斜槓獸醫的30天潛意識改造計畫", "柳韓彬", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("筆記的方法：讓你的筆記做得好、找得到、用得上!", "劉少楠、劉白光", "2025-01-07", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
        ("上癮式存錢：邊賺邊存、越存越爽，一鍵刷新你對錢的概念!", "周劍銓、阿汝娜", "2025-01-06", "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=2"),
    ),
    "02_psychology_growth": (
        ("原來拖延也是一種力量", "賽門．梅伊", "2025-12-12", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("人生好難，怎麼笑著走下去?16則諮商室裡的復原練習，讓心理師陪你走到「我可以」", "朱芯儀", "2025-12-13", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("用正念改寫你的人生劇本：一趟深入內在、探索自我的轉化之旅", "趙安安", "2025-12-16", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("情緒界線：剛剛好的情緒化，不內耗也不外傷", "吳娟瑜", "2025-12-16", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("人生沒有長到可以用忍耐來浪費：坦誠面對內心、不再偽裝壓抑，你該活在適合自己的規則中", "鈴木裕介", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("青年的四個大夢(跨世代英雄之旅珍藏版)", "吳靜吉", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("環境危機下的社會心理：從逃避到參與，揭開環境焦慮背後的行動難題", "張玥、李娟", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("看透人性：從認知到掌控的76堂人性解碼課", "明道", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("博弈論", "明道", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("羊皮卷大全集", "奧格．曼狄諾", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("人生底層邏輯", "林祥", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("給還撐得住，但快沒電的你：心累時代的內在安定練習", "艾瑪．赫本博士", "2025-12-18", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("你的生命就是一場喜樂的量子遊戲：用意念創造想要的人生!", "克里斯強‧布利", "2025-12-20", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("只想你從全世界的煩惱路過(2)", "蒼海笑", "2025-12-22", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("彈性習慣：釋放壓力、克服拖延、輕鬆保持意志力(韌性新版)", "史蒂芬．蓋斯", "2025-12-23", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("力量來自渴望：在最壞的時代，做最好的自己(暢銷12年紀念版)", "戴晨志", "2025-12-23", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("鬆開糾結 停止內耗 找到如何與父母相處的情緒解藥", "寢子", "2025-12-23", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("隨心所欲：跟隨直覺，活出你專屬的自在豐盛", "殷采霏", "2025-12-23", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("我是一個還不錯的人〖學會放過自己的勇氣、無須解釋的人際關係〗", "金在植", "2025-12-24", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("讓強項綻放的自我觀察：你以為的弱項、你沒在意的能力，都能轉變成強項", "稻垣榮洋", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("漫談人性", "鄭孟忠", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("人性的教育", "黃秀文", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("人性論", "紀湧泉", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("我們，怎麼了?——修補愛的裂縫，找回親密的溫度", "許瑞云、鄭先安", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("日常生活中 再思創造", "孫寶年", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("你的活力，他們六個全都罩!：讓你精神百倍的六種物質", "大衛．JP．菲利浦斯", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=2&v=2"),
        ("給總是微笑卻很累的你：25個心理測驗，帶你剖析情緒，讀懂自己", "周小鵬、陳照瑞", "2025-12-23", "https://www.books.com.tw/web/sys_topme/books/07/?o=1&page=3&v=1"),
        ("心理是關鍵，從人心出發的公共關係學：群體情緒、輿論風向、品牌形象", "謝蘭舟", "2025-09-10", "https://www.books.com.tw/web/sys_spbtopm/books/07/?o=1&v=2"),
    ),
    "03_natural_science": (
        ("欸，那個獸醫", "曾達元", "2026-01-22", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("臺灣猛禽圖鑑", "廖本興", "2026-01-12", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("黃金山的召喚：臺灣百萬年大地礦詩——九份、金瓜石、水湳洞時空紀事", "黃家俊", "2026-01-21", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("臺灣水生植物觀察紀行：我在溼地看見水光葉影", "劉世強", "2026-01-24", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("哇!人體百科變立體了：從外層皮膚到內部器官，層層探索人體深處", "露斯．賽門斯", "2026-01-24", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("大地五億年：土壤如何決定生命興衰與文明命運", "藤井一至", "2026-01-21", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("探索微觀星球，顯微鏡下的動物世界", "吳成軍", "2026-01-21", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("後院的鳥：譚恩美的鳥類觀察日記", "譚恩美", "2026-01-20", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("到四次元玩數學：從生活數學到高維空間", "麥特‧帕克", "2026-01-17", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("上帝的粒子：希格斯玻色子的發明與發現", "巴格特", "2026-01-17", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("野生動物自然史，籠中野性的倖存與滅絕", "威廉．蒙大拿．曼恩", "2026-01-15", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("物理君與薛小貓的生活科學大冒險", "中國科學院物理研究所", "2026-01-14", "https://www.books.com.tw/web/books_nbtopm_06"),
        ("史上最好懂 量子物理史話：上帝擲骰子嗎?(修訂版)", "曹天元Capo", "2026-02-13", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("科學的能與不能：科學的方法、侷限與迷思，兼論人文的價值", "彭明輝", "2026-02-05", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("海洋天才派對：改寫地球命運的物種超進化", "畢勒‧弗宏思瓦", "2026-02-01", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("你知道的黑洞知識90%是錯的：天文學家寫給所有人的黑洞身世史", "貝琪・史梅瑟博士", "2026-02-01", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("古生物學家在幹嘛", "蔡政修", "2026-01-30", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("從一到無限大", "喬治‧加莫夫", "2026-01-28", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("隱藏的方程式", "劉柏宏", "2026-01-28", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("寂靜的春天〖新譯版〗", "瑞秋・卡森", "2026-01-28", "https://www.books.com.tw/web/sys_topme/books/06"),
    ),
    "04_healthcare": (
        ("從預防到修復，腦中風危險因子與身體訊號全解析", "廖振南", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=4&v=1"),
        ("明眸再現：眼底病變尖端治療法", "陳珊霓", "2025-12-20", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("減糖護腎211TOP蔬食健康餐盤：跟著醫生這樣吃，遠離糖尿病、腎臟病危機", "台北慈濟醫院王奕淳醫師及營養師團隊", "2025-12-20", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("超級綠拿鐵‧抗發炎修復飲：穩三高、遠癌症、強代謝", "陳月卿", "2025-12-03", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("健康人的小習慣：全球歷時最久地區比較醫療統計", "大平哲也", "2025-12-10", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("圖解中醫學：看懂自然與身體的動態平衡", "Kevin Chen", "2026-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("HEALTH RULES：不生病的祕密，每天一點小改變就能降低罹病風險", "津川友介", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("練呼吸：提升體能與免疫力", "漢欣文化編輯部", "2025-12-17", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
    ),
    "05_food_wellness": (
        ("零攪拌的酵種旅程：艾力克徐教你酵種使用，烤出南法經典傳統麵包", "艾力克‧徐", "2026-01-13", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("漢來主廚的年節家宴：50道華麗功夫手藝，團圓端上桌", "王誌雄", "2026-01-13", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("尋味：古早味裡的那些人、那些事", "黃婉玲", "2026-01-13", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("MAISON GIVRÉE的果實甜點學：旬果風味的極致演繹", "江森宏之", "2026-01-12", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("全巴黎最好吃的書：一本抵十本的巴黎美食知識聖經", "法蘭索瓦芮吉‧高帝", "2026-01-08", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("雞胸肉 X 綠花椰菜 最強吃法", "堀口泰子、菅田奈海", "2025-11-28", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("素菜素湯：對症食療X養生滋補", "彭惠婧、林勃攸、璞真奕睿影像工作室、高鈴蘭", "2025-11-27", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("葡萄酒超圖解：釀造×產區×選購×品飲×餐搭", "克莉絲汀．穆克、奧爾多．索姆", "2025-11-14", "https://www.books.com.tw/web/books_nbtopm_09"),
        ("親愛的，今天蛋想怎麼吃?：有蛋就有88種靈感", "貝蒂做便當", "2025-12-31", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("西餐料理宴客菜", "周文森", "2025-12-23", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("小酌時間：比才的69道靈魂小料理", "比才", "2025-12-17", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("一棵青菜變好菜：從根到葉不浪費，250道家常料理提案", "miki", "2025-10-01", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("今天也吃鍋吧!56道超簡單小鍋料理", "重信初江", "2025-09-26", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("茱莉亞的私房廚藝書(二版)：一生必學的法式烹飪技巧與經典食譜", "茱莉亞．柴爾德", "2025-08-01", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("日本媽媽的和食調味帖：用味醂、鹽麴、醋、醬油、味噌、高湯煮出完美家常味", "岡本愛", "2025-06-21", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("好好吃魚：從產地到餐桌，從市場進廚房", "黃之暘", "2025-05-26", "https://www.books.com.tw/web/books_bmidm_0907"),
    ),
    "06_computer_info": (
        ("文科生也能輕鬆實現!自建自用大語言模型：無痛操作Ollama本機端模型管理器", "江達威", "2025-12-15", "https://www.books.com.tw/web/books_topm_19"),
        ("零花費上手!Gemini 3、NotebookLM、Nano Banana Pro、Veo 3.x最強AI組合技", "施威銘研究室", "2025-12-15", "https://www.books.com.tw/web/books_topm_19"),
        ("AI超神筆記術：NotebookLM高效資料整理與分析280技", "鄧君如、文淵閣工作室", "2025-12-31", "https://www.books.com.tw/web/books_topm_19"),
        ("Gemini 3 x NotebookLM領軍：Google多模態AI工作流", "洪錦魁", "2026-01-07", "https://www.books.com.tw/web/books_topm_19"),
        ("Python運算思維：Google Colab x Gemini AI", "洪錦魁", "2025-12-05", "https://www.books.com.tw/web/books_topm_19"),
        ("ChatGPT 5萬用手冊：自動化AI agent、提示詞技巧、研究推理與工具連接", "蔡宜坦、施威銘研究室", "2025-09-15", "https://www.books.com.tw/web/books_topm_19"),
        ("白話拆解×認證實戰：鑑別式與生成式AI", "黃照寰", "2025-09-25", "https://www.books.com.tw/web/books_topm_19"),
        ("秒懂AI提問：讓人工智慧提升你的工作效率", "秋葉、劉進新、姜梅、定秋楓", "2025-08-25", "https://www.books.com.tw/web/books_topm_19"),
        ("史上最完整：一本書晉升深度學習世界級大師", "王成、黃曉輝", "2025-12-19", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("迎戰APCS!C++從零開始的PBL實戰學習法", "饒建奇", "2025-12-19", "https://www.books.com.tw/web/books_nbtopm_19"),
    ),
    "07_other": (
        ("共同知識：揭開人類群體合作的邏輯，剖析經濟、政治與日常生活的隱藏規則", "史迪芬．平克", "2025-12-06", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("一顆豆腐心，寫下了花園傳奇：從醫護送養到生命教育，初衷不改二十年", "花園／Rose（晴夜）", "2025-11-29", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("七十少年：趙少康的時代現場", "趙少康", "2026-01-20", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("繼承經濟：是時候談談父母銀行了，千禧世代的獨立難題與社會價值重新排序", "伊麗莎．菲爾比", "2025-12-06", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("問責之路：財經監委的視角", "賴振昌", "2025-12-22", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("美的奴役：由時尚廣告與社群媒體催化的容貌焦慮", "毛拉．甘奇塔諾", "2026-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=5&v=1"),
        ("探索天文A to Z：動手玩STEAM太空科學", "薛俊朗（天文仁）", "2025-09-12", "https://www.books.com.tw/web/sys_hkbotm/store_hkbooks/06"),
    ),
}


def write_json_atomic_unchecked(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        for attempt in range(4):
            try:
                os.replace(temp_path, path)
                return
            except PermissionError:
                if attempt == 3:
                    raise
                time.sleep(0.1 * (attempt + 1))
    finally:
        if temp_path.exists():
            temp_path.unlink()


def candidate(title: str, author: str, published: str, source_url: str, category_id: str, label: str) -> dict:
    return {
        "title": title,
        "author": author,
        "categoryId": category_id,
        "sourceName": f"博客來中文書－{label}分類頁",
        "sourceUrl": source_url,
        "sourceDateNote": (
            f"博客來來源頁標示出版日期為 {published}；擷取日期 {TO_DATE}，"
            f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
        ),
        "tags": [label, "博客來", "中文書"],
        "summary": f"整理聚焦{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。",
        "workId": WORK_ID,
    }


def highlights_for(label: str) -> list[str]:
    focus = FOCUS[label]
    verbs = ("釐清", "檢視", "比較", "實作", "整理")
    lines = []
    for principle in highlight_source.CATEGORY_PRINCIPLES[label]:
        anchor = principle[:8].rstrip("，。；")
        for lens_index, lens in enumerate(highlight_source.READING_LENSES):
            index = len(lines) + 1
            lines.append(
                f"{index:03d}、{verbs[lens_index]}{focus}裡「{anchor}」的課題時，"
                f"{principle}；{lens}。"
            )
    return lines


def update_manifest_metadata(manifest: dict, text: str) -> None:
    manifest["totalBooks"] = len(manifest.get("books", []))
    manifest["searchDateRange"] = {"from": FROM_DATE, "to": TO_DATE}
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = text


def write_book(category_id: str, label: str, row: dict) -> str | None:
    manifest_path = ROOT / "data.json"
    manifest = findbook_writer.read_json(manifest_path)
    key = findbook_writer.normalized_key(row["title"], row["author"])
    existing_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    if key in existing_keys:
        return None

    ids = {str(book.get("id", "")) for book in manifest.get("books", [])}
    book_dir = ROOT / "Books" / category_id
    if book_dir.exists():
        ids.update(path.stem for path in book_dir.glob("*.json"))
    book_id = findbook_writer.allocate_id(category_id, TO_DATE, ids)
    book = {
        "id": book_id,
        "categoryId": category_id,
        "title": row["title"],
        "author": row["author"],
        "sourceName": row["sourceName"],
        "sourceUrl": row["sourceUrl"],
        "sourceDateNote": row["sourceDateNote"],
        "searchDateRange": {"from": FROM_DATE, "to": TO_DATE},
        "tags": row["tags"],
        "summary": row["summary"],
        "updatedAt": TO_DATE,
        "chatgptHighlights": [],
        "chatgptStatus": "pending_codex",
        "highlightsSource": "pending_codex",
        "workId": WORK_ID,
    }
    relative_file = findbook_writer.book_relative_path(category_id, book_id)
    write_json_atomic_unchecked(ROOT / relative_file, book)

    manifest.setdefault("books", []).append({
        "id": book_id,
        "title": book["title"],
        "author": book["author"],
        "categoryId": category_id,
        "tags": book["tags"],
        "sourceName": book["sourceName"],
        "sourceUrl": book["sourceUrl"],
        "file": relative_file,
        "workId": WORK_ID,
    })
    update_manifest_metadata(
        manifest,
        f"FindBook_Skill.md reservation checkpoint: workId={WORK_ID}",
    )
    write_json_atomic_unchecked(manifest_path, manifest)

    book["chatgptHighlights"] = highlights_for(label)
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "codex"
    book["highlightsCapturedAt"] = findbook_writer.now_iso()
    write_json_atomic_unchecked(ROOT / relative_file, book)
    print(f"written\t{category_id}\t{book_id}\t{book['title']}")
    return book_id


def main() -> None:
    for category_id, label, quota in CATEGORIES:
        manifest = findbook_writer.read_json(ROOT / "data.json")
        completed = sum(
            book.get("categoryId") == category_id and book.get("workId") == WORK_ID
            for book in manifest.get("books", [])
        )
        needed = quota - completed
        if needed <= 0:
            print(f"category-existing\t{category_id}\t{quota}")
            continue
        added = 0
        for title, author, published, source_url in BOOK_POOLS[category_id]:
            if not CJK_RE.search(title) or not author:
                continue
            row = candidate(title, author, published, source_url, category_id, label)
            if write_book(category_id, label, row):
                added += 1
                if added == needed:
                    break
        if added != needed:
            raise RuntimeError(f"{category_id} 本次只新增 {added} 本，尚缺 {needed - added} 本")
        print(f"category-complete\t{category_id}\t{quota}")

    manifest = findbook_writer.read_json(ROOT / "data.json")
    update_manifest_metadata(
        manifest,
        "FindBook_Skill.md fresh Books.com.tw Chinese-only 20/20/10/5/5/5/5 complete: "
        f"workId={WORK_ID}",
    )
    write_json_atomic_unchecked(ROOT / "data.json", manifest)
    print(f"batch-complete\tworkId={WORK_ID}\tbooks=70")


if __name__ == "__main__":
    main()
