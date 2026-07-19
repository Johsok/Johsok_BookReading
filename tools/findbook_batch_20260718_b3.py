from __future__ import annotations

import findbook_batch_20260716_b13 as batch


FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-18"
WORK_ID = "findbook-20260718-135724-b3"

CANDIDATES = {
    "01_business_startup": (
        (
            "康樂股漲的日股奇妙冒險：體驗食衣住行，布局優質日股!CIIA國際投資分析師的投資筆記",
            "康樂股漲",
            "",
            "https://www.books.com.tw/products/0011051398",
        ),
        (
            "股市小白也能學會 3年賺5,000萬的 MACD趨勢線投資",
            "桂陽",
            "",
            "https://www.books.com.tw/products/0011047020",
        ),
        (
            "蒙格之道：關於投資、閱讀、工作與幸福的普通常識",
            "查理．蒙格 RanRan",
            "",
            "https://www.books.com.tw/products/0010966227",
        ),
        (
            "一年投資5分鐘：打造每月3萬被動收入，免看盤、不選股的最強小資理財法",
            "陳逸朴（小資YP）",
            "",
            "https://www.books.com.tw/products/0010911539",
        ),
        (
            "刷新你的金錢腦【財富自由5階梯實戰祕笈】：你以為的財富自由可能是錯的?扭轉心態與習慣，懂得花錢、聰明投資，中產上班族也能7年滾出3,800萬元",
            "潔米菈．蘇夫蘭 鄭煥昇",
            "",
            "https://www.books.com.tw/products/0011041230",
        ),
        (
            "華爾街操盤手的暴富公式：戒掉選股，靠「耍廢投資」就能讓資產翻倍",
            "大衛．葛芬（David Gaffen） 李璞良",
            "",
            "https://www.books.com.tw/products/0011047003",
        ),
        (
            "【漫畫版】不炒股、不投機，1年賺1億：跟世界富豪學「實體投資法」，從負債3,400萬到上億資產的逆轉故事",
            "戶塚真由子 周若珍 蒼井アオ",
            "",
            "https://www.books.com.tw/products/0011043557",
        ),
        (
            "翻轉月光焦慮的理財必修課：投資，是存給自己的安全感。用ETF搭配科技基金，打造3年獲利100%、資產翻倍的安心財務計畫",
            "詹璇依",
            "",
            "https://www.books.com.tw/products/0011025245",
        ),
        (
            "投資的底層邏輯：高人氣EMBA財富管理課，帶你精準抓對全球趨勢",
            "陳超",
            "",
            "https://www.books.com.tw/products/0011015015",
        ),
        (
            "價值投資翻身筆記：5大穩健理財觀念 × 年化報酬率50%投資心法，30歲前達成買房目標!",
            "Kelvin價值投資",
            "",
            "https://www.books.com.tw/products/0011030913",
        ),
        (
            "我畢業五年，用ETF賺到400萬：每月1,000元就能開始!不用兼差斜槓，兩檔ETF投資組合，年賺20%以上",
            "PG財經筆記",
            "",
            "https://www.books.com.tw/products/0010843448",
        ),
        (
            "工程師勳仔40歲前退休計畫：指數節稅多元收益投資法 低風險避開0050正2盲點",
            "勳仔",
            "",
            "https://www.books.com.tw/products/0011030747",
        ),
        (
            "投機狂潮!查爾斯.麥凱談群眾的幻想與瘋狂：古典金融史×現代投資心理×日常防泡沫判斷，看懂人們如何把希望當成真相",
            "[英]查爾斯．麥凱（Charles Mackay）伊莉莎 編譯",
            "",
            "https://www.books.com.tw/products/0011053442",
        ),
        (
            "散戶交易天才15萬滾10億的最強短線操作攻略：四次實戰投資大賽冠軍的低風險獲利公式，股市震盪也能猛賺不賠",
            "洪仁基 張鑫莉",
            "",
            "https://www.books.com.tw/products/0011021810",
        ),
        (
            "錢進AI人形機器人大時代：從 AI核心技術到供應鏈全解析，掌握投資市場與全球ETF趨勢",
            "蕭毅豪",
            "",
            "https://www.books.com.tw/products/0011037825",
        ),
        (
            "用一本書詳解實戰 MACD交易技術：透過150張圖表， 投資新手學會85%勝率指標，增加賺錢機會",
            "韓雷",
            "",
            "https://www.books.com.tw/products/0011003164",
        ),
        (
            "破框投資，照著做就能富：八大破框武器，不論是低薪、小資或準退休族，都能靠台股、美股、ETF，翻轉人生。",
            "陳詩慧",
            "",
            "https://www.books.com.tw/products/0011020885",
        ),
        (
            "哲哲的ETF投資絕學：「下殺買、上漲賣」，左側交易 讓我從賠500萬到賺1151萬!",
            "郭哲榮",
            "",
            "https://www.books.com.tw/products/0010991863",
        ),
        (
            "如何賺高股息 ETF及科技基金：3年獲利100%的紀律投資術!",
            "詹璇依",
            "",
            "https://www.books.com.tw/products/0010989531",
        ),
        (
            "每月1000元，輕鬆滾出千萬的雞尾酒投資法：6步驟打造資產自動增值系統，通膨時代也能財務自由",
            "米安．薩米Mian Sami 林信帆",
            "",
            "https://www.books.com.tw/products/0011041552",
        ),
    ),
    "02_psychology_growth": (
        (
            "{柳林經典 傾聽內心}柳林風聲+蛤蟆先生去看心理師 雙書附：諮商心理師獨家撰寫「角色問候卡」",
            "羅伯‧狄保德 肯尼斯‧葛拉罕 郭漁 張美惠 Dinner illustration",
            "",
            "https://www.books.com.tw/products/0010944181",
        ),
        (
            "柳林風聲：年度暢銷書《蛤蟆先生去看心理師》故事原型，英國百年經典文學之作",
            "肯尼斯．葛拉罕 郭漁 Dinner illustration",
            "",
            "https://www.books.com.tw/products/0010944079",
        ),
        (
            "【旅行特別版】蛤蟆先生去看心理師(暢銷500萬冊!英國心理諮商經典，附《蛤蟆先生旅遊去萬用卡片》)",
            "羅伯‧狄保德 張美惠 Dinner Illustration",
            "",
            "https://www.books.com.tw/products/0011045831",
        ),
        (
            "【蛤蟆的冒險生活.心理三部曲】柳林風聲+河岸風景+蛤蟆先生去看心理師",
            "姬吉．強森 羅伯．狄保德 肯尼斯．葛拉罕 郭漁 張美惠 林婉婷 Dinner illustration",
            "",
            "https://www.books.com.tw/products/0011021634",
        ),
        (
            "諮商與心理治療(第三版)",
            "Richard S. Sharf 林延叡 羅幼瓊 葉怡寧 馬長齡",
            "",
            "https://www.books.com.tw/products/0011037174",
        ),
        (
            "悲傷輔導與悲傷治療：心理衛生實務工作者手冊(第五版)",
            "J. William Worden 張玉仕 李開敏 林方皓 葛書倫",
            "",
            "https://www.books.com.tw/products/0010867277",
        ),
        (
            "瘦一輩子的本事：心理學權威的10堂知心瘦身課，跳出飲食陷阱，跟減不完的肥說ByeBye",
            "茱蒂絲．貝克 黛布拉．貝克．布西斯 劉佳澐",
            "",
            "https://www.books.com.tw/products/0010981118",
        ),
        (
            "人間遊戲：「PAC模型」⤫ 36種日常心理遊戲，洞悉人的性格與心理狀態，迅速和各種人有效地互動〈人際溝通分析之父艾瑞克.伯恩經典著作〉",
            "艾瑞克．伯恩 林曉欽",
            "",
            "https://www.books.com.tw/products/0010873681",
        ),
        (
            "沙發上的心理治療：圖繪治療師與個案的三階段療程故事，看見改變的發生",
            "菲莉帕．派瑞 陳莉淋 弗洛．派瑞（Flo Perry）",
            "",
            "https://www.books.com.tw/products/0010998148",
        ),
        (
            "每個人都想學的焦慮課【全新修訂版】：用認知行為療法擺脫社交恐懼、黑暗心理、憂慮壓力，學習善待自己(附《焦慮自助練習本》)",
            "亞倫．T．貝克 大衛．A．克拉克 陳莉淋",
            "",
            "https://www.books.com.tw/products/0011026880",
        ),
        (
            "完形諮商與心理治療技術",
            "Phil Joyce & Charlotte Sills 張莉莉",
            "",
            "https://www.books.com.tw/products/0010464102",
        ),
        (
            "有病的其實是我媽，卻要我去諮商：寫給青少年和家長的心理圖文書",
            "大衛・古席翁 穆佐 Geraldine LEE",
            "",
            "https://www.books.com.tw/products/0010864585",
        ),
        (
            "守護我的關係心理學：認識4種溝通類型×49個心理圈套，用英國IAPT 10週關愛課程照顧自己",
            "安潔拉・森 張召儀",
            "",
            "https://www.books.com.tw/products/0010997681",
        ),
        (
            "兒童心理創傷後的遊戲治療：實務工作者應該知道的事：實務工作者應該知道的事",
            "Eliana Gil 陳信昭 陳宏儒 陳碧玲 自然就好心理諮商所",
            "",
            "https://www.books.com.tw/products/0010867874",
        ),
        (
            "諮商與心理治療倫理：準則、研究與新興議題(2020年全新修訂版)",
            "Elizabeth Reynolds Welfel 廖宗慈 楊雅婷 王文秀 蔡欣憓 鍾榕芳 陳俊言",
            "",
            "https://www.books.com.tw/products/0010866823",
        ),
        (
            "EMDR應用於兒童心理治療之藝術 [第二版]",
            "卡洛琳．賽圖 羅比·阿德勒－塔皮亞 余芊慧 朱品潔 楊雅婷 謝馨儀 陳美秀",
            "",
            "https://www.books.com.tw/products/0010954636",
        ),
        (
            "沙游：通往靈性的心理治療取向(2版)",
            "Dora M. Kalff 朱惠英 黃宗堅",
            "",
            "https://www.books.com.tw/products/0010918492",
        ),
        (
            "不和別人比較的自信心理學：卸下重重心防，用愛化解比較心態，與內在的三個自我和解",
            "伊蓮．N．艾倫 蔡心語",
            "",
            "https://www.books.com.tw/products/0010977008",
        ),
        (
            "老人心理諮商與輔導",
            "Morley D. Glicken＝ 周鉦翔 李昆樺 陳佑昇等",
            "",
            "https://www.books.com.tw/products/0010582038",
        ),
        (
            "心理投射技巧分析",
            "Robert C. Burns 梁漢華，黃燦瑛",
            "",
            "https://www.books.com.tw/products/0010037144",
        ),
    ),
    "03_natural_science": (
        (
            "科學實驗王第二部10：生物科技與遺傳學",
            "Story a. 徐月珠 洪鐘賢",
            "",
            "https://www.books.com.tw/products/0011053204",
        ),
        (
            "科學發明王43：電能對決",
            "Gomdori co 許葳 洪鐘賢",
            "",
            "https://www.books.com.tw/products/0011047297",
        ),
        (
            "【實驗王特輯】科學實驗王理科關鍵字2：生物(一)附資優學習單",
            "Story a. 徐月珠 洪鐘賢（Hong-Jong Hyun）",
            "",
            "https://www.books.com.tw/products/0011038117",
        ),
        (
            "哆啦A夢科學任意門27：自由飛翔航空器",
            "漫畫／藤子．F．不二雄 編撰／日本小學館 游韻馨",
            "",
            "https://www.books.com.tw/products/0011040530",
        ),
        (
            "科學發明王42：打掃神器",
            "Gomdori co 許葳 洪鐘賢（홍종현）",
            "",
            "https://www.books.com.tw/products/0011034128",
        ),
        (
            "哆啦A夢科學任意門26：科學入門魔法環",
            "日本小學館 藤子．F．不二雄 黃薇嬪",
            "",
            "https://www.books.com.tw/products/0011027319",
        ),
        (
            "科學實驗王第二部9：氣候危機與碳中和",
            "Story a. 徐月珠 洪鐘賢（Hong-Jong Hyun）",
            "",
            "https://www.books.com.tw/products/0011006299",
        ),
        (
            "【實驗王特輯】科學實驗王理科關鍵字1：地球科學(附資優學習單)",
            "Story a. 徐月珠 洪鐘賢",
            "",
            "https://www.books.com.tw/products/0011023994",
        ),
        (
            "小學生的第一套科學輕百科：哆啦A夢科學任意門3冊(科學入門魔法環+科學記憶吐司+神奇道具大解密)",
            "日本小學館 藤子‧F‧不二雄",
            "",
            "https://www.books.com.tw/products/0011027310",
        ),
        (
            "科學發明王41：多合一功能",
            "Gomdori co 許葳 洪鐘賢(홍종현)",
            "",
            "https://www.books.com.tw/products/0011019584",
        ),
    ),
    "04_healthcare": (
        (
            "陳志金 ICU醫師 重症醫療現場 I+II+III 套書(共3本)：勇敢而發真心話+用生命拚的生命+當個更有溫度的人",
            "陳志金",
            "",
            "https://www.books.com.tw/products/0011032125",
        ),
        (
            "醫療緊缺的時代，醫師最強的助理──AI：病情告知×家屬溝通×罕見病例×研究選題×SCI論文，讓ChatGPT成為醫療現場的實用助手",
            "王偉強，馮曉明，壽松濤",
            "",
            "https://www.books.com.tw/products/0011054460",
        ),
        (
            "臺大醫院減肥班8週燃脂瘦身全書：17位多科醫療專家傳授安全有效營養×運動×心理的健康減重法",
            "臺大醫院健康教育中心與營養師團隊",
            "",
            "https://www.books.com.tw/products/0011025777",
        ),
        (
            "ON CALL隨時待命：佛奇醫師回憶錄，一段改變美國與世界公共醫療的關鍵旅程",
            "安東尼．佛奇醫師 周序諦",
            "",
            "https://www.books.com.tw/products/0011043099",
        ),
        (
            "健康人的小習慣：全球歷時最久地區比較醫療統計 60年追蹤10000人結果大公開",
            "大平哲也 林雅惠",
            "",
            "https://www.books.com.tw/products/0011038616",
        ),
    ),
    "05_food_wellness": (
        (
            "主廚的療癒餐桌：118盤讓細胞開心的料理",
            "羅勻吟",
            "",
            "https://www.books.com.tw/products/0011050972",
        ),
        (
            "食材123!聰明煮好菜：只須1~3樣，用最少的主食材，煮出無需繁複備料的省時料理、美味翻倍的主廚級好料，從此輕鬆上菜!",
            "楊勝凱 蔡萬利",
            "",
            "https://www.books.com.tw/products/0011052210",
        ),
        (
            "Superfood!地瓜不簡單：料理點心七十二變，國民美食好吃good!",
            "拓蔬人料理團隊（施建瑋、蔡長志、曾秀微）",
            "",
            "https://www.books.com.tw/products/0011051510",
        ),
        (
            "冷菜料理：汆燙、涼拌、冰鎮63道清爽夏日料理【附贈真冰涼~書籤小卡2張，用最簡單的步驟做最好吃料理】",
            "蓮池陽子 連雪雅",
            "",
            "https://www.books.com.tw/products/0011052626",
        ),
        (
            "「名店秘製調味料&料理」：跨越法義日中，專業Chef傳授獨家的風味關鍵，帶你深入瞭解星級餐廳色香味的176種秘訣與技巧",
            "加藤順一 國居 優 岩坪 滋 田村亮介 野田雄紀 音羽 元",
            "",
            "https://www.books.com.tw/products/0011046706",
        ),
    ),
    "06_computer_info": (
        (
            "超圖解 Python 程式設計--從入門、網頁應用、YOLO 到生成式 AI 實作",
            "趙英傑",
            "",
            "https://www.books.com.tw/products/0011034569",
        ),
        (
            "深入Linux Kernel程式設計：kernel內部原理、模組開發與同步機制(第二版)",
            "Kaiwan N. Billimoria 廖明沂",
            "",
            "https://www.books.com.tw/products/0011049689",
        ),
        (
            "內行人才知道的程式設計模式面試指南",
            "Alex Xu Shaun Gunawardane 藍子軒",
            "",
            "https://www.books.com.tw/products/0011047246",
        ),
        (
            "Python運算思維: Google Colab x Gemini AI - 「零基礎」x「高效率」學「程式設計」",
            "洪錦魁",
            "",
            "https://www.books.com.tw/products/0011038090",
        ),
        (
            "【中小學生必讀】數位未來百科：快速掌握AI、IoT、元宇宙、資訊安全與程式設計，培養創造力與解決問題的能力!",
            "岡嶋裕史 張嘉芬",
            "",
            "https://www.books.com.tw/products/0011005157",
        ),
    ),
    "07_other": (
        (
            "圖解易讀版中國歷史年表",
            "李光欣 ADee",
            "",
            "https://www.books.com.tw/products/0011040869",
        ),
        (
            "毛澤東時代和後毛澤東時代(1949-2009)：另一種歷史書寫(上、下)",
            "錢理群",
            "",
            "https://www.books.com.tw/products/0011053768",
        ),
        (
            "圖解易讀版臺灣歷史年表",
            "陳映勳 ADee",
            "",
            "https://www.books.com.tw/products/0011040856",
        ),
        (
            "歐美近代史原來很有事(3冊合售)：OSSO~歐美近代史原來很有事+這樣的歷史課我可以+世界是怎麼長成現在的樣子",
            "吳宜蓉",
            "",
            "https://www.books.com.tw/products/0010996285",
        ),
        (
            "一本就懂【歷史的轉換期】：全新手繪人物插畫、地圖，輕鬆跨越2200年歷史長河",
            "歷史的轉換期譯者群 世界の転換期を知る11章編集部",
            "",
            "https://www.books.com.tw/products/0011038365",
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
