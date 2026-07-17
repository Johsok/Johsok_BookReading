from __future__ import annotations

import findbook_batch_20260717_b4 as previous


batch = previous.batch

FROM_DATE = "2026-06-18"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-153000-b5"


def sourced_rows(
    source_url: str,
    books: tuple[tuple[str, str], ...],
    source_date: str,
):
    return tuple((title, author, source_date, source_url) for title, author in books)


CANDIDATES = {
    category_id: tuple(candidates)
    for category_id, candidates in previous.CANDIDATES.items()
}

CANDIDATES["01_business_startup"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP43-A900K6ZDT",
        (("Gemini 投資理財全攻略：小資族看過來！完全零門檻的 AI 智慧選股×財報分析×資金管理", "施威銘研究室"),),
        "2026-07-07",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD3J-A900K5RL3",
        (("區塊鏈創新實踐手冊：如何運用去中心化技術，建構企業轉型解決方案", "康納．史文森"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD3J-A900K6346",
        (("用人與帶人的問題，歷史都有答案", "增田賢作"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP1G-A900K69NR",
        (("把話說到痛點，別再繞圈子！終結職場模糊溝通，讓事情高效推進的5個原則", "多明尼克．穆特勒"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD3J-A900K633Z",
        (("35之後，更好的工作在哪裡？", "黑田真行"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP1G-A900K62AY",
        (("來日本工作吧：完整呈現在日本生活與工作的全方位實用指南", "喬伊斯．黃"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAV0S-A900K5L0H",
        (("高位不亂：在不能犯錯的位置，讓心站穩", "鄭詩諭"),),
        "2026-06-24",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBNB9-D900K696X",
        (("行銷7.0", "菲利浦．科特勒"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD3J-A900K58H3",
        (("可以直接說重點嗎？用AI練出最強說話術！", "山口拓朗"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBS5Z-D900K6QYS",
        (("稻盛和夫　培養不迷惘的心：經營之聖奉行的思考方法，讓你所想的必將實現", "稻盛和夫"),),
        "2026-07-04",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ04-D900K5ZJK",
        (("劉必榮的領導筆記：上位的謀略、在位的智慧、交棒的藝術", "劉必榮"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP1F-A900K7DQP",
        (("AI改變了你的客戶：大家買東西不再搜Google而是問AI時，行銷該怎麼做？", "馬克・薛佛"),),
        "2026-07-08",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBN7U-D900K7D36",
        (("問世間，錢為何物", "筏行"),),
        "2026-07-05",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD3J-A900K633X",
        (("我們是減時27%的高效率精銳", "佐上峻作"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAD71-A900K3CV6",
        (("馬斯克寶典：從顛覆矽谷到打造太空帝國，讀懂全球首富20年極限思維", "艾瑞克．喬根森"),),
        "2026-07-16",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ2L-D900K637K",
        (("致富魔法符印：聚財、守財、創業、增加被動收入，以朱彼特之名，祈請金錢滾滾之流", "傑森．米勒"),),
        "2026-07-01",
    ),
)

CANDIDATES["02_psychology_growth"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ12-D900K7Y5V",
        (("業餘愛好的力量：過度努力時代的快樂指南", "凱倫・沃朗"),),
        "2026-07-15",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBS5Z-D900K6TXO",
        (("第一本複雜性創傷後壓力症候群自我療癒聖經（長銷典藏）", "皮特．沃克"),),
        "2026-07-06",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ12-D900K5ZA4",
        (("SayNo的教誨：對你一直以來相信的事物，勇敢說不！", "SayNo"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K6ZBZ",
        (("鬆綁焦慮，擺脫情緒內耗療癒雙套書：《八成是你想太多》＋《如果焦慮是隻貓》", "尼克．崔頓、段美茹"),),
        "2026-07-07",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015564193",
        (("半憂鬱：給能工作，能生活，內心卻動彈不得的你", "平光源"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K6G9N",
        (("人生就是冰淇淋，要盡快享用啊！：關於跌倒、焦慮與那些有點累的日常", "艾蘭度"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP5H-A900K6RRO",
        (("一點點勇氣：勇氣不是不害怕，而是帶著顫抖依然選擇前進", "克萊兒．亞歷珊卓"),),
        "2026-07-04",
    ),
    *sourced_rows(
        "https://www.eslite.com/product/10012036172683169478002",
        (("原來訓練眼睛，就能強化心理素質！：獨家專利心理視覺訓練，企業菁英、奧運選手與名校都在用", "松島雅美"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP1Z-A900K6G86",
        (("每天15分鐘，陪孩子玩出情緒韌性：高情商╳不怕難╳勇於表達，從親子時間養出必備素養！", "蒂娜．佩恩．布萊森、喬姬．威森－文森特"),),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K76UE",
        (("原來，我一直太為難自己", "南宮北"),),
        "2026-07-08",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBS5Y-D900K5QJG",
        (("認可：只要先接納，就能改變人生！用矽谷人氣心理師的「認可階梯」，改變你與家庭、職場、自我的關係", "卡洛琳．佛萊克"),),
        "2026-06-25",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015568539",
        (("走自己的路：當你不再想著成為別人，才真正開始閃耀光芒", "蜜拉‧李‧帕托"),),
        "2026-06-26",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K69R3",
        (("數位斷捨離：擺脫手機成癮造成的身心疲勞", "有田秀穂"),),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K7DR8",
        (("活出自己的時間：擺脫窮忙與AI焦慮，重獲自由的新生活提案", "佐宗邦威"),),
        "2026-07-08",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBS2X-D900K6LAK",
        (("翻轉世代", "喬納森．海特、凱瑟琳．普萊斯"),),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP06-A900K6G9D",
        (("內在獲勝：破除恐懼迷思，找回幸福的驅動力（全新珍藏版）", "皮帕．葛蘭琪"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBND9-D900K60KQ",
        (("選擇真實", "卡米兒"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://www.kingstone.com.tw/basic/2011760427264/",
        (("為什麼你有情緒？（暢銷紀念）：認識情緒，才認識自己；它難以掌控，卻決定了你的生活品質！", "提博特．梅里斯"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ12-D900K73Z3",
        (("也許你該找人聊聊〔陪伴日誌〕百萬暢銷慶功版：一週一課題，用一年改變一生的自我覺察練習", "蘿蕊・葛利布"),),
        "2026-07-08",
    ),
)

CANDIDATES["03_natural_science"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP16-A900K5URH",
        (("教室外的生物課：跟著小虎老師從故事認識昆蟲生態", "小虎老師（王俊凱）"),),
        "2026-06-29",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ17-D900K79QC",
        (("氣候變遷（未來已來系列）", "金成花、權秀珍"),),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/promote/library/?id=st010408",
        (("電子科學簡史，從雨天風箏到半導體的故事：量子霍爾效應×拓撲絕緣體×高溫超導……點亮數位文明的奈米閃光", "張天蓉"),),
        "2026-07-09",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015582468",
        (("不可思議的料理科學【最新修訂版】", "平松サリー"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015571894",
        (("怪獸醫生的爬蟲特寵臨床筆記：烏龜、蜥蜴、守宮、變色龍與蛇類飼養×醫療指南", "蘇泰宇"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://www.tenlong.com.tw/products/9786264253703",
        (("漫畫科普冷知識王：世界其實很有事，生活才會那麼有意思（暢銷版）", "鋤見"),),
        "2026-06-30",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/promote/library/?id=st",
        (("西元10001年（未來已來系列）", "金成花、權秀珍"),),
        "2026-07-17",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015597917",
        (("基本電學／電工原理", "程宇寰"),),
        "2026-07-16",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/scheme/?id=947",
        (("地。：關於地球的運動【豪華版】（全8冊盒裝套書）", "魚豊"),),
        "2026-07-15",
    ),
    *sourced_rows(
        "https://findbook.com.tw/9786264253093",
        (("AI無人機技術：開發實務全面性指南", "Subhash K. Shinde等"),),
        "2026-07-02",
    ),
)

CANDIDATES["04_healthcare"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP2G-A900K5UPY",
        (("發炎消了，病就好了：找出健康不適的根源，遠離失智與癌症的自我療癒之道", "內山葉子"),),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBN90-D900K60LD",
        (("造臉者", "琳西．費茲哈里斯"),),
        "2026-07-01",
    ),
)

CANDIDATES["05_food_wellness"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBR22-D900K69F0",
        (("一甲子米食技藝大全：圖解步驟╳營養美味╳節慶典故", "劉妙華"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP0U-A900K62BE",
        (("日本的飯糰：走遍日本47個都道府縣尋覓所得94道食譜", "旅行飯糰店 菅本香菜"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP0V-A900K50ZA",
        (("極小廚房輕鬆煮：能開火就超會煮！73道超省時方便的零失敗餐桌美味", "杵島隆太"),),
        "2026-06-20",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP0X-A900K5CZ8",
        (("東京自由之丘Mont St. Clair的甜點典藏食譜", "辻口博啓"),),
        "2026-06-26",
    ),
    *sourced_rows(
        "https://www.bookrep.com.tw/?at=bookcontent&cl=book&id=21642&md=gwindex",
        (("餓鬼麵包店之書：麵包詩人的40堂烘焙藝術課", "強納森‧史蒂文斯、瑪雅・馬拉霍夫斯基・巴札克"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP0V-A900K6RV1",
        (("0～24個月一週副食品，140道冰磚食譜：一次做好7天份．加熱即可食用．寶寶想吃時輕鬆完成（最新修訂版）", "上田玲子、堀江佐和子"),),
        "2026-07-04",
    ),
)

CANDIDATES["06_computer_info"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP43-A900K7DQ7",
        (("AI超神簡報術：NotebookLM×Gemini×Gamma全解鎖", "鄧君如、文淵閣工作室"),),
        "2026-07-08",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015572085",
        (("10倍速！AI Skill全攻略：建立Skill驅動AI系統，打造從學術研究到專案開發的自動化工作流", "曾慶良（阿亮老師）"),),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://www.rakuten.com.tw/shop/bookrep/product/0NNC1101/",
        (("我的AI機器人大百科：卡內基美隆大學教授帶你認識機器人如何改變世界", "亨妮．阿德莫尼博士"),),
        "2026-06-24",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBNAJ-D900K696N",
        (("PC home電腦家庭07月號／2026第366期", "PC home電腦家庭編輯群"),),
        "2026-07-01",
    ),
)

CANDIDATES["01_business_startup"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP1C-A900K62A7",
        (("大交棒時代：跨越百年的六堂企業必修課", "蔡鴻青"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://www.eslite.com/product/10012043902683178544002",
        (("數據對了，為什麼你還是輸了？：數據告訴你發生什麼，人性告訴你為什麼發生", "克利斯汀．麥茲伯格、米克爾．B．拉斯穆森"),),
        "2026-07-15",
    ),
)

CANDIDATES["02_psychology_growth"] += (
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAP47-A900K6OU2",
        (("站在邊緣之境（新版）：利他、同理心、誠正、尊重、敬業，回歸五種心理本質", "瓊恩．荷里法斯"),),
        "2026-07-11",
    ),
    *sourced_rows(
        "https://www.cite.com.tw/book?id=108239",
        (("我不是想離職，只是不想被燃燒殆盡：築起三層心理防火牆，把責任還回去，把能量還給自己", "郭約瑟"),),
        "2026-07-09",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAO21-A900K5JXY",
        (("我們都太慢反應的事：兒少網路性剝削、社群恐慌、網路霸凌，拉起孩子的數位界線", "趙逸帆"),),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://www.kingstone.com.tw/monthpublish/book/ce/",
        (("直視死亡，你會更明白「怎麼活」：《當呼吸化為空氣》＋《死亡的臉》", "保羅．卡拉尼提、努蘭"),),
        "2026-06-30",
    ),
    *sourced_rows(
        "https://www.kingstone.com.tw/monthpublish/book/aaaa",
        (("媽媽離開的時候想穿什麼顏色的衣服？──外婆、老媽還有我的三代生命對話", "申昭潾"),),
        "2026-07-15",
    ),
)

CANDIDATES["03_natural_science"] += (
    *sourced_rows(
        "https://www.sanmin.com.tw/promote/library/?id=st",
        (("新材料（未來已來系列）", "金成花、權秀珍"),),
        "2026-07-17",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/promote/hotbook/?id=st",
        (("爆笑化學江湖Ⅱ：身邊的化學物質", "王冶"),),
        "2026-07-15",
    ),
)

CANDIDATES["01_business_startup"] += sourced_rows(
    "https://www.kingstone.com.tw/monthpublish/book/eeee/",
    (("贏過大盤的順勢交易：不分牛熊市，股票、基金、期貨、債券都能賺，14位頂尖操盤手締造超額報酬的獲利紀律", "麥可．卡威爾"),),
    "2026-06-30",
)

CANDIDATES["01_business_startup"] += sourced_rows(
    "https://www.tenlong.com.tw/products/9786267925041",
    (("赤腳，走在無人之境：在聚光燈亮起之前，我已經站在那裡", "劉進聲"),),
    "2026-06-30",
)

CANDIDATES["02_psychology_growth"] += sourced_rows(
    "https://www.sanmin.com.tw/product/index/015549408",
    (("負面不是病：黑暗情緒哲學", "瑪莉安娜．亞歷山德里"),),
    "2026-06-26",
)


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
