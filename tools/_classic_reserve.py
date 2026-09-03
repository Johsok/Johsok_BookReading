# -*- coding: utf-8 -*-
"""One-shot: parse Taaze list JSON, reserve 5 classic books per first 4 categories."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import findbook_scraper as scraper
import findbook_writer as writer

ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "1986-09-03"
TO_DATE = "2024-09-03"
WORK_ID = "findbook-20260903-1119"
LIMIT = 5
OUT = ROOT / "tools" / ".findbook_candidates_findbook-20260903-1119.json"
AGENT_TOOLS = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading\agent-tools"
)

LIST_FILES = {
    "01_business_startup": [
        ("讀冊－商業2011暢銷百大", "20548342-7f20-4155-84fb-90c27e7d9c80.txt"),
        ("讀冊－商業2013暢銷百大", "e668bb08-47e4-4b54-9fe2-9e9a69eaee03.txt"),
    ],
    "02_psychology_growth": [
        ("讀冊－心理勵志2013暢銷百大", "28b1f890-0e6e-4467-bd9e-8a7b7613108d.txt"),
        ("讀冊－心理勵志2013暢銷百大", "cdf2bf6d-a2e0-440e-9214-a50bd44e3ea9.txt"),
    ],
    "03_natural_science": [
        ("讀冊－科學2013暢銷百大", "89d901e5-7506-432e-92c9-fc09581258bb.txt"),
    ],
    "04_healthcare": [
        ("讀冊－醫學保健2013暢銷百大", "aa318626-3121-4f6a-8998-414aa6975728.txt"),
        ("讀冊－醫學保健2013暢銷百大", "aca6db52-0d77-43a2-9379-88ae309290e6.txt"),
    ],
}

# 61–80 歷年榜（列表 JSON，非詳情頁）
EXTRA = {
    "01_business_startup": [
        {
            "title": "態度決定一切",
            "author": "阿爾伯特‧哈伯德",
            "prodId": "11100071501",
            "published": "2005-01-12",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "失落的致富經典",
            "author": "華勒思‧華特斯",
            "prodId": "11100019364",
            "published": "2008-01-25",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "師父：那些我在課堂外學會的本事(專訪20週年紀念版)",
            "author": "諾姆．布羅斯基、鮑．柏林罕",
            "prodId": "11100774185",
            "published": "2016-02-02",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "先問，為什麼？：顛覆慣性思考的黃金圈理論，啟動你的感召領導力（新增訂版）",
            "author": "賽門．西奈克",
            "prodId": "11100985250",
            "published": "2018-05-23",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "不懂帶人，你就做到死又留不住人！：行為科學教你量身打造團隊的SOP使用手冊",
            "author": "石田淳",
            "prodId": "11100900813",
            "published": "2020-02-28",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "不當行為：行為經濟學之父教你更聰明的思考、理財、看世界",
            "author": "理查‧塞勒",
            "prodId": "11100783429",
            "published": "2016-06-01",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "富爸爸商學院：銷售致富的財商教育",
            "author": "羅勃特．T．清崎",
            "prodId": "11100913527",
            "published": "2020-07-29",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "貨幣戰爭：誰掌握了貨幣，誰就能主宰這個世界【暢銷新裝版】",
            "author": "宋鴻兵 編著",
            "prodId": "11100905784",
            "published": "2020-04-29",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "思考的技術",
            "author": "大前研一",
            "prodId": "11100743770",
            "published": "2015-06-12",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "超速學習：我這樣做，一個月學會素描，一年學會四種語言，完成MIT四年課程",
            "author": "史考特．楊",
            "prodId": "11100905884",
            "published": "2020-05-01",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "美安賣什麼？：從零售到電商 揭開千億帝國的驚人祕密",
            "author": "今周刊",
            "prodId": "11100829105",
            "published": "2017-11-02",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "康乃爾最經典的思考邏輯課（暢銷典藏版）：避開六大謬誤，資訊時代必備的理性判斷工具",
            "author": "湯瑪斯．吉洛維奇",
            "prodId": "11100969760",
            "published": "2021-12-01",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "下班後的黃金8小時",
            "author": "羅伯‧帕格利瑞尼",
            "prodId": "11100479747",
            "published": "2011-03-04",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "Deep Work深度工作力：淺薄時代，個人成功的關鍵能力【暢銷新裝版】",
            "author": "卡爾．紐波特",
            "prodId": "11100967753",
            "published": "2021-11-09",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "無限賽局：翻轉思維框架，突破勝負盲點，贏得你想要的未來",
            "author": "賽門．西奈克",
            "prodId": "11101020319",
            "published": "2020-12-30",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "發現我的天賦（修訂版）：打開34個天賦的禮物",
            "author": "馬克斯‧巴金漢、唐納‧克里夫頓",
            "prodId": "11100774411",
            "published": "2016-01-28",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
        {
            "title": "跟誰都能聊不停─這樣說話，讓你到處受歡迎",
            "author": "金井英之",
            "prodId": "11100226632",
            "published": "2010-05-25",
            "sourceName": "讀冊－商業歷年累計暢銷百大",
        },
    ],
    "02_psychology_growth": [
        {
            "title": "不要在該奮鬥時選擇安逸",
            "author": "老楊的貓頭鷹",
            "prodId": "11101036842",
            "published": "2024-05-15",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "卡內基溝通與人際關係（2015年新版）",
            "author": "戴爾‧卡內基",
            "prodId": "11100734348",
            "published": "2015-01-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "逆思維：華頓商學院最具影響力的教授，突破人生盲點的全局思考",
            "author": "亞當．格蘭特",
            "prodId": "11100985594",
            "published": "2022-07-04",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "心態致勝（2023版）：全新成功心理學",
            "author": "卡蘿．杜維克",
            "prodId": "11101019441",
            "published": "2023-08-28",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "遇見未知的自己【恩佐全彩插圖典藏版】：張德芬經典代表作「身心靈三部曲」喚醒篇",
            "author": "張德芬",
            "prodId": "11100896545",
            "published": "2020-01-06",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "過度努力：每個「過度」，都是傷的證明",
            "author": "周慕姿",
            "prodId": "11100930682",
            "published": "2021-03-05",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "愛：即使世界不斷讓你失望，也要繼續相信愛",
            "author": "Peter Su",
            "prodId": "11100734827",
            "published": "2015-02-06",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "阿德勒心理學講義",
            "author": "阿德勒",
            "prodId": "11100745352",
            "published": "2015-05-08",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "讓上司挺你、朋友懂你，跟誰都能聊不停的「回話技術」：談判、責罵、提案、請託，40個讓人欲罷不能、拍手叫好的「臨場說話術」",
            "author": "福田健",
            "prodId": "11100720741",
            "published": "2014-10-23",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "做自己與別人生命中的天使",
            "author": "嚴長壽",
            "prodId": "11100257426",
            "published": "2008-05-15",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "思考致富聖經 愛藏版",
            "author": "拿破崙．希爾",
            "prodId": "11101007979",
            "published": "2023-05-03",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "好好說話：粉絲破千萬！最強說話團隊教你新鮮有趣的話術精進技巧",
            "author": "馬東出品",
            "prodId": "11100820713",
            "published": "2017-08-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "Good Luck：當幸運來敲門（全新插圖．30萬冊暢銷典藏版）",
            "author": "亞歷士‧羅維拉 & 費南多‧德里亞斯迪貝斯",
            "prodId": "11100815397",
            "published": "2017-06-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "受傷的孩子和壞掉的大人",
            "author": "陳志恆",
            "prodId": "11100831459",
            "published": "2017-12-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "別對每件事都有反應：淡泊一點也無妨， 活出快意人生的99個禪練習！",
            "author": "枡野俊明",
            "prodId": "11101000410",
            "published": "2023-01-03",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "吸引力法則：心想事成的黃金三步驟",
            "author": "麥可J‧羅西爾",
            "prodId": "11100019361",
            "published": "2007-10-31",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "輕鬆駕馭意志力（暢銷10年紀念新版）：史丹佛大學最受歡迎的心理素質課",
            "author": "凱莉．麥高尼格",
            "prodId": "11100958729",
            "published": "2021-10-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "卡內基 人性的弱點",
            "author": "戴爾．卡內基",
            "prodId": "11100926539",
            "published": "2020-12-30",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "一個新世界：喚醒內在的力量",
            "author": "艾克哈特‧托勒",
            "prodId": "11100019840",
            "published": "2008-07-25",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "誰搬走了我的乳酪？ 【全新翻譯．全新插圖．精裝典藏版】",
            "author": "史賓賽．強森博士",
            "prodId": "11100589495",
            "published": "2011-12-26",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "禮物",
            "author": "史賓賽．強森博士",
            "prodId": "11100190940",
            "published": "2005-01-31",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "異數：超凡與平凡的界線在哪裡？（暢銷慶功版）",
            "author": "麥爾坎．葛拉威爾",
            "prodId": "11100913882",
            "published": "2020-08-12",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "拖延心理學：為什麼我總是愛拖延？是與生俱來的壞習慣，還是身不由己？（暢銷35週年增修新版）",
            "author": "珍‧博克、萊諾拉‧袁",
            "prodId": "11100814407",
            "published": "2017-05-11",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "接受不完美的勇氣：阿德勒100句人生革命",
            "author": "小倉廣",
            "prodId": "11100734977",
            "published": "2015-02-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "不抱怨的世界（全新增修版）",
            "author": "威爾．鮑溫",
            "prodId": "11100649451",
            "published": "2013-03-15",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "情緒勒索（全球暢銷20年經典）：遇到利用恐懼、責任與罪惡感控制你的人，該怎麼辦？",
            "author": "蘇珊．佛沃（Susan Forward, Ph.D.）、唐娜．費瑟（Donna Frazier）",
            "prodId": "11100823762",
            "published": "2017-09-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "為自己出征（燙金珍藏版）",
            "author": "羅伯．費雪",
            "prodId": "11100823760",
            "published": "2017-09-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "峰與谷─超越逆境、享受順境的人生禮物",
            "author": "史賓賽‧強森",
            "prodId": "11100190941",
            "published": "2009-11-30",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "再給我一天",
            "author": "米奇．艾爾邦",
            "prodId": "11100122294",
            "published": "2007-03-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
        {
            "title": "你想活出怎樣的人生？【品格形塑經典，宮崎駿為它復出，親自改編電影】",
            "author": "吉野源三郎",
            "prodId": "11100858844",
            "published": "2018-11-01",
            "sourceName": "讀冊－心理勵志歷年累計暢銷百大",
        },
    ],
    "03_natural_science": [
        {
            "title": "看不見的雨林–福爾摩沙雨林植物誌：漂洋來台的雨林植物，如何扎根台灣，建構你我的歷史文明、生活日常",
            "author": "胖胖樹 王瑞閔",
            "prodId": "11100840285",
            "published": "2018-03-15",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "元素生活完全版：非典型118個化學元素圖鑑，徹底解構你的生活",
            "author": "寄藤文平",
            "prodId": "11100884414",
            "published": "2019-08-28",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "自然老師沒教的事（1）：100堂都會自然課（2019新版）",
            "author": "張慧芬、黃一峰",
            "prodId": "11100878190",
            "published": "2019-05-28",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "大腦的秘密檔案（增訂版）",
            "author": "Rita Carter",
            "prodId": "11100527976",
            "published": "2011-04-01",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "這才是數學：從不知道到想知道的探索之旅",
            "author": "保羅．拉克哈特",
            "prodId": "11100739811",
            "published": "2015-03-13",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "飛機的構造與飛行原理（全彩修訂版）",
            "author": "中村寬治",
            "prodId": "11101030191",
            "published": "2024-02-06",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "量子力學與混沌理論的人生十二堂課",
            "author": "林文欣",
            "prodId": "11100906461",
            "published": "2020-05-12",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "大腦當家（最新增訂版）：12個讓大腦靈活的守則，工作學習都輕鬆有效率",
            "author": "約翰‧麥迪納",
            "prodId": "11100804877",
            "published": "2017-01-20",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "數學天方夜譚：撒米爾的奇幻之旅（經典復刻版）",
            "author": "馬爾巴坦",
            "prodId": "11100651701",
            "published": "2013-04-14",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "為什麼公車一次來三班？：從自然的奧妙原理到日常的不思議定律，探索生活中隱藏的81個數學謎題",
            "author": "羅勃．伊士威、傑瑞米‧溫德漢",
            "prodId": "11100938712",
            "published": "2021-07-03",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "第七感：啟動認知自我與感知他人的幸福連結",
            "author": "丹尼爾．席格",
            "prodId": "11100863635",
            "published": "2018-12-19",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "3.3秒的呼吸奧祕：失傳吐納技法與最新科學研究的絕妙旅程",
            "author": "詹姆斯．奈斯特",
            "prodId": "11100955105",
            "published": "2021-08-28",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "非實用野鳥圖鑑：600種鳥類變身搞笑全紀錄（十週年台灣特有版）",
            "author": "富士鷹茄子",
            "prodId": "11100900717",
            "published": "2020-02-26",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "觀念生物1-4套書（全新修訂版）",
            "author": "尼達姆、霍格蘭、麥克佛森、竇德生",
            "prodId": "11100818667",
            "published": "2017-06-30",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "欲望分子多巴胺：帶來墮落與貪婪、同時激發創意和衝動的賀爾蒙，如何支配人類的情緒、行為及命運",
            "author": "丹尼爾．利伯曼、麥可．隆",
            "prodId": "11100999694",
            "published": "2023-01-05",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "細胞的靈性療癒【典藏增訂版】：生物化學博士教你的細胞轉化修練！",
            "author": "桑德拉‧巴雷特",
            "prodId": "11100783017",
            "published": "2016-06-01",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
        {
            "title": "大腦解密手冊：誰在做決策、現實是什麼、為何沒有人是孤島、科技將如何改變大腦的未來",
            "author": "伊葛門",
            "prodId": "11100802999",
            "published": "2016-12-27",
            "sourceName": "讀冊－科學歷年累計暢銷百大",
        },
    ],
    "04_healthcare": [
        {
            "title": "醫療靈媒：慢性與難解疾病背後的祕密，以及健康的終極之道",
            "author": "安東尼．威廉",
            "prodId": "11100791438",
            "published": "2016-09-01",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "耳鳴，是救命的警鈴：耳鳴不需要根治，也不必恐慌，剛剛好的耳鳴，是你最忠實的健康守護者！台灣耳科權威教你不吃藥破解耳鳴的迷思！",
            "author": "賴仁淙醫師",
            "prodId": "11100779712",
            "published": "2016-04-11",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "呼吸，為了療癒：全新的呼吸科學與醫學，透過清醒的呼吸，徹底轉化身心",
            "author": "楊定一、馬奕安（Jan Martel）(協力)、陳夢怡(協力)",
            "prodId": "11101007727",
            "published": "2023-04-26",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "時時刻刻微養生：陳月卿30年養生全精華，打造身心全方位自癒地圖（元氣新書封．暢銷健康版）",
            "author": "陳月卿",
            "prodId": "11101021850",
            "published": "2023-11-10",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "也許你該找人聊聊：一個諮商心理師與她的心理師，以及我們的生活（二版）",
            "author": "蘿莉・葛利布（Lori Gottlieb）",
            "prodId": "11101015037",
            "published": "2023-08-02",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "瑜珈解剖書：解開瑜珈與人體的奧秘【增修三版】",
            "author": "雷思利．卡米諾夫、艾美．馬修斯",
            "prodId": "11101015026",
            "published": "2023-08-02",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "為什麼要睡覺？：睡出健康與學習力、夢出創意的新科學（2023年新版）",
            "author": "沃克",
            "prodId": "11101011682",
            "published": "2023-05-26",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "醫生哪有這麼萌：Nikumon的實習生活全紀錄",
            "author": "Nikumon",
            "prodId": "11100744800",
            "published": "2015-04-29",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "伸展聖經：40週年全新增修版",
            "author": "包柏．安德森",
            "prodId": "11100975149",
            "published": "2022-01-24",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "醫行天下（上）：尋醫求道",
            "author": "蕭宏慈",
            "prodId": "11100158393",
            "published": "2010-01-28",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "人體解剖全書（第三版）",
            "author": "安德魯．貝爾",
            "prodId": "11100956359",
            "published": "2021-09-03",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "1000萬人都說有效的輕鬆戒菸法",
            "author": "亞倫．卡爾",
            "prodId": "11100461459",
            "published": "2011-03-03",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "百病起於寒（暢銷經典版）",
            "author": "進藤義晴、進藤幸惠",
            "prodId": "11100942919",
            "published": "2021-08-18",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "全食物密碼",
            "author": "陳月卿",
            "prodId": "11100133188",
            "published": "2005-01-01",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "求醫不如求己（增訂版）",
            "author": "中里巴人",
            "prodId": "11100137636",
            "published": "2009-12-22",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "救命聖經．葛森療法（暢銷紀念版）：史上第一個成功的癌症療法，見證奇蹟80年",
            "author": "夏綠蒂．葛森、莫頓．沃克",
            "prodId": "11101013521",
            "published": "2023-07-27",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "57健康同學會：破除關鍵57健康迷思！",
            "author": "潘懷宗、隋安德、張雅芳、東森財經新聞台",
            "prodId": "11100649808",
            "published": "2013-03-30",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
        {
            "title": "奇蹟",
            "author": "吉爾．泰勒",
            "prodId": "11100925457",
            "published": "2020-12-10",
            "sourceName": "讀冊－醫學保健歷年累計暢銷百大",
        },
    ],
}


def extract_json_object(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no json object")
    return json.loads(text[start : end + 1])


def rows_from_payload(payload: dict, source_name: str) -> list[dict]:
    items = []
    for row in payload.get("result1") or []:
        title = str(row.get("titleMain") or "").strip()
        author = str(row.get("author") or "").strip(" /|,，、")
        prod_id = str(row.get("prodId") or "").strip()
        published = str(row.get("publishDate") or "").strip()[:10]
        if not title or not scraper.has_han(title) or not author or not prod_id:
            continue
        items.append(
            {
                "title": title,
                "author": author,
                "prodId": prod_id,
                "published": published,
                "sourceName": source_name,
            }
        )
    return items


def to_item(row: dict) -> dict:
    return {
        "title": row["title"],
        "author": row["author"],
        "sourceUrl": f"https://www.taaze.tw/products/{row['prodId']}.html",
        "published": row.get("published") or "",
        "sourceSite": "讀冊",
        "sourceName": row["sourceName"],
    }


def collect_category(category_id: str, existing: set[str]) -> list[dict]:
    pool: list[dict] = []
    pool.extend(EXTRA.get(category_id, []))
    for source_name, filename in LIST_FILES.get(category_id, []):
        path = AGENT_TOOLS / filename
        payload = extract_json_object(path.read_text(encoding="utf-8"))
        pool.extend(rows_from_payload(payload, source_name))
    seen: set[str] = set()
    found: list[dict] = []
    for row in pool:
        item = to_item(row)
        key = scraper._accept_item(item, existing, seen, FROM_DATE, TO_DATE, category_id)
        if not key:
            continue
        seen.add(key)
        candidate = scraper.to_candidate(item, category_id, FROM_DATE, TO_DATE)
        if "經典" not in candidate["tags"]:
            candidate["tags"].append("經典")
        candidate["workId"] = WORK_ID
        found.append(candidate)
        if len(found) >= LIMIT + 1:
            break
    return found


def main() -> int:
    existing = scraper.load_existing_keys(ROOT)
    payload = {}
    for category_id in (
        "01_business_startup",
        "02_psychology_growth",
        "03_natural_science",
        "04_healthcare",
    ):
        rows = collect_category(category_id, existing)
        payload[category_id] = rows
        print(f"{category_id} candidates={len(rows)}")
        for row in rows:
            print(" ", row["title"][:40], "/", row["author"][:16], "/", row.get("published", ""))

    missing = [cid for cid, rows in payload.items() if len(rows) < LIMIT]
    if missing:
        raise SystemExit("缺額：" + ",".join(missing))

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    committed = []
    for category_id, candidates in payload.items():
        count = 0
        for candidate in candidates:
            if count >= LIMIT:
                break
            result = writer.reserve_one(ROOT, category_id, candidate, FROM_DATE, TO_DATE)
            print(result.get("status"), result.get("id") or result.get("reason"), result.get("title", "")[:28])
            if result.get("status") == "committed":
                count += 1
                committed.append(result)
                existing.add(scraper.normalized_key(result["title"], result["author"]))
        if count != LIMIT:
            raise SystemExit(f"{category_id} only {count}")
    print("COMMITTED", len(committed))
    for row in committed:
        print(f"{row['id']}\t{row['title']}\t{row['author']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
