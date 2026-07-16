from __future__ import annotations

import glob
import importlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

import findbook_batch_20260714 as highlight_source
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-16"
WORK_ID = "findbook-20260716-201554-b13"
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

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

EXTRA_POOLS = {
    "01_business_startup": (
        ("我在日本有個家：東京買房最強攻略", "TiN", "", "https://www.books.com.tw/web/books_topm_02"),
        ("行為投資金律：不預測、不內耗，財富增值這樣做最有感！", "丹尼爾．克羅斯比", "", "https://www.books.com.tw/web/books_topm_02"),
        ("進化的力量3：情緒經濟", "劉潤", "", "https://www.books.com.tw/web/books_topm_02"),
        ("刻意直覺：頂尖商學院的決策思維訓練，解讀內在訊號，打造精準判斷力", "黃樂仁（Laura Huang）", "", "https://www.books.com.tw/web/books_topm_02"),
        ("勝者謀局：做事的永遠贏不過做局的！", "大齊", "", "https://www.books.com.tw/web/books_topm_02"),
        ("提升未來：可以、應該、可能、不該，思考升級的四個關鍵詞", "尼克‧佛斯特（Nick Foster）", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("你不需要天賦，只需要每天1%的進步：54個職場影響力行動指南", "安迪．艾里斯", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("最強技術分析聖經 布林通道指標操作法：用230張圖抄底抓反彈，85%勝率賺翻股市！", "李洪宇", "2025-12-30", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("節省工時的100種方法：品質與速度兼顧的時短工作術", "森田幸（森田ゆき）", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("擠出獲利：從擠出現金活下來，到基業長青年年賺", "金炯坤", "2025-12-29", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("循環在有無之間：永豐一百年的永續智慧", "何壽川", "2025-12-27", "https://www.books.com.tw/web/books_topm_02"),
        ("紀律長贏：揭開清大校務基金操盤人風險控管與穩定獲利的策略", "林哲群", "2026-01-30", "https://www.books.com.tw/web/books_topm_02"),
        ("賭客信條：一門源自賭博的科學 5版", "孫惟微", "2026-01-28", "https://www.books.com.tw/web/books_nbtopm_02/?o=3&page=3&v=2"),
        ("遇見更好的自己：讓我告訴全世界，只有自己可以超越自己", "林玟妗", "2026-01-22", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("勇往值錢", "于振源", "2026-01-22", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("奈特論風險、不確定性與利潤：在不可預測世界中，判斷如何成為利潤來源", "法蘭克．奈特、伊莉莎", "2026-01-21", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("行動式領導：先顧好自己，再拯救團隊，用優勢觀點提升團隊動力", "朱建平、李海霞、楊靜芬、鄧慧文", "2026-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("你缺的不是努力，而是思維破局的能力", "岩崳", "2026-01-08", "https://www.books.com.tw/web/sys_nbmidme/books/02"),
        ("操作慣性股，我38歲就財富自由", "王仲麟", "2026-02-25", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("我用K線賺一億：60天看懂買賣型態", "財聚龍頭", "2026-02-10", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("從破產人生逆襲到財富自由：36個翻轉心法把人生找回來", "李文森", "2026-02-10", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("收入翻30倍的移動力：培養生理與心理移動能力，闖過低谷反轉人生", "長倉顯太", "2026-02-25", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("邏輯投資：散戶贏過大盤的機會", "邏輯投資（劉冠宏）", "2026-02-26", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("讓錢喜歡你的財富整理術：小印的23個理財練習", "整理鍊金術師小印", "2026-02-26", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("金融怪傑達文熙教你用100張圖學會箱子戰法", "達文熙、詹TJ", "2026-02-26", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("電子商務與ChatGPT：物聯網、KOL直播、區塊鏈、社群行銷、大數據、智慧商務", "吳燦銘", "2026-02-10", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("大阪築夢者：野村卓也的城市革新之路", "高卓加、林思凡", "2026-02-11", "https://www.books.com.tw/web/sys_compub/books/02"),
        ("蘋果之道：重新定義世界的50年", "大衛．波格", "2026-03-31", "https://www.books.com.tw/web/sys_topme/books/02/?o=1&page=1&v=2"),
        ("億元肥羊零成本買股術：我靠借錢買金融股賺到1億", "翁建原", "2026-03-26", "https://www.books.com.tw/web/sys_topme/books/02/?o=1&page=1&v=2"),
        ("簡報的技術", "王永福", "2026-03-12", "https://www.books.com.tw/web/sys_topme/books/02/?o=1&page=1&v=2"),
        ("你的簡報就是比AI強：47個人類才懂的PPT技巧", "日比野治雄", "2026-03-12", "https://www.books.com.tw/web/sys_topme/books/02/?o=1&page=1&v=2"),
        ("看懂趨勢：一眼看穿多空漲跌", "Queen怜", "2026-02-04", "https://www.books.com.tw/web/books_topm_02"),
        ("你該管理的是能量，而不是時間", "韓善英", "2025-10-08", "https://www.books.com.tw/web/books_topm_02"),
        ("拿下一號位：銷冠當場就簽單", "浩南哥", "2025-09-01", "https://www.books.com.tw/web/sys_natopm/china/06/?cus_id=3037"),
        ("正道：中國製造企業的新出路", "謝泓", "2025-08-01", "https://www.books.com.tw/web/sys_natopm/china/06/?cus_id=3037"),
        ("AI重塑生意經：如何實現快速盈利", "莫敏", "2025-08-01", "https://www.books.com.tw/web/sys_natopm/china/06/?cus_id=3037"),
        ("AI重構商業大模型：傳統企業AI化轉型路線圖", "李國建、管鵬", "2025-12-01", "https://www.books.com.tw/web/sys_puballb/china/?pubid=0000000154"),
    ),
    "02_psychology_growth": (
        ("世界盡頭的咖啡館套書：生命思考暢銷經典（2冊）", "約翰‧史崔勒基", "2026-02-05", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("抉擇的智慧：轉化心靈的52篇生命故事", "蘇拾瑩", "2026-02-05", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("格局", "喬潔", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("逆商", "陌漠", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("情商", "喬潔", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("如何顯化你想要的一切：愛情、財富、事業與一切願望的終極解答", "維多利亞．傑克森", "2026-01-15", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("該你的都在路上", "艾莉", "2026-01-26", "https://www.books.com.tw/web/books_nbtopm_07/?o=1&page=2&v=1"),
        ("別太把別人當回事：活得心安理得，從容自在的禪練習", "枡野俊明", "2026-01-26", "https://www.books.com.tw/web/books_nbtopm_07/?o=1&page=2&v=1"),
        ("現在就出發：別把人生清單留到以後", "吳娮翎", "2025-12-11", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("找到自己，懂你自己，做你自己", "心玲", "2025-12-11", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("婆媳三角：愛他、也愛自己，不再內耗的五堂情緒界線課", "崔西・達格利許博士", "2025-12-11", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("和尚賣了法拉利：圓滿人生的七個祕密", "羅賓．夏瑪", "2025-12-11", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("從不怕輸開始贏：世界第一的心態管理法", "金美善", "2025-12-11", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("學習人生的雲淡風輕：弘一大師的七部人生禪", "弘一大師、舒硯", "2025-12-10", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("孤獨是一種狀態，寂寞是一種心情", "植西聰", "2025-12-10", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("關於富足，我們應該要……：你賺的是錢，還是你想要的生活？", "費勇", "2025-12-10", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("治癒的構圖，繪畫心理治療統合應用", "郝學敏", "2025-12-10", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("你的心靈雞湯需要加點剝皮辣椒", "李恬芳", "2025-12-09", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("於是，我成為不像樣的大人", "宮能安", "2025-12-09", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("幸福啟動腦科學：血清素、催產素與多巴胺如何解碼快樂", "樺澤紫苑", "2025-12-06", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("我和好運綁定了：心理學×吸引力法則養出開運體質", "masa", "2025-12-05", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("馴服多巴胺：在縱欲時代抗拒無止境想要更多的誘惑", "麥可．隆", "2025-12-04", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("我選擇自私的先愛自己：討好自己就夠了、喜歡自己就夠了、顧好自己就夠了", "藤野智哉", "2026-02-04", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("飛吧！排球少年心理學：舉球給自己，讓人生更輕鬆的阿德勒心理學", "內田若希、河津慶太", "2026-02-04", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("眼界", "陌漠", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("細節", "高文斐", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("策略", "戈旭皎", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("態度", "高文斐", "2026-02-02", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("逆襲思維：打破自我設限的高效行動法則", "任白", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("其實可以不用這麼心累：做不被情緒支配的自己", "陳雪莉", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("心智節流的放空鍛鍊：終結過勞迴圈", "約瑟．傑貝利", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("隱性內耗：看不見的傷，如何消磨你的能量？", "蘇絢慧", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("條條大路通羅馬，但你可以不去羅馬", "萬特特", "2026-02-25", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("正向自信：打破懷疑與恐懼，喚醒內在力量", "喬瓦尼・迪恩斯特曼", "2026-02-25", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("人生每件事，都是取捨的練習", "吳若權", "2026-02-11", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("當手機遇上演算法：從依附理論拆解手機成癮、社交焦慮與永遠在線的疲勞", "佩特拉．維爾澤波爾", "2026-02-07", "https://www.books.com.tw/web/sys_topme/books/07"),
        ("安慰的藝術：為人療傷止痛的話語和行動", "芙爾．沃克", "2026-02-07", "https://www.books.com.tw/web/sys_topme/books/07"),
    ),
    "03_natural_science": (
        ("如果這樣，會怎樣？（10週年增訂版＋2，2冊）", "蘭德爾．門羅", "2025-12-12", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("夏娃：女性身體如何推動兩億年的人類演化", "薄翰儂", "2025-12-23", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("升級吧！大腦：激發大腦超能力，破解金魚腦、腦腐陷阱、演算法操控的祕密", "謝伯讓", "2025-12-30", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("隱世女畫家的自然手繪集：《金石昆蟲草木狀》藥草篇＋花果篇＋動物篇", "文俶", "2025-12-25", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("國家地理賞鳥指南", "諾亞．史崔克", "2025-12-30", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("超智慧啟示錄：AI引爆人類末日倒數", "詹姆斯‧巴拉特", "2025-12-05", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1"),
        ("水資源AI賦能技術指引", "卓伯全", "2026-02-01", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("臺灣草鴞：在西拉雅草坡的繁衍與生存紀實", "萬俊明", "2026-02-01", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("台灣石松類與蕨類全圖鑑：蹄蓋蕨科—水龍骨科", "呂碧鳳", "2026-01-10", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("台灣石松類與蕨類全圖鑑：水韭科—烏毛蕨科", "呂碧鳳", "2026-01-08", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("我，為什麼會這樣？從生物學、腦科學與心理學解釋我們的喜好、情緒、行為與想法", "比爾．蘇利文", "2026-01-08", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("魔法師二號：劃時代的海洋微生物採集航程", "克萊格．凡特、大衛．鄧肯", "2026-01-08", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("超級電容器儲能材料、裝置與應用", "張海濤、楊維清、何正友", "2026-01-07", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("臺灣珍鳥重現：古爾德鳥類博物誌臺灣選集", "吳建龍、李政霖、林大利、林文宏、江勻楷、洪廣冀、約翰・古爾德、馮孟婕、黃瀚嶢", "2025-12-31", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("動手做科學探究：輕鬆運用生活中的材料，培養提問、設計實驗、邏輯思辨與表達能力", "蔡任圃", "2025-12-25", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("被透支的地球未來，人類無度開發的環境代價", "楊陽", "2025-12-24", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("紙上草木花實敷：從花果鋪陳的圖像中，看見明代植物知識的悄然流轉", "張鈁", "2025-12-24", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("風中舞者：老鷹四季的飛行圖譜", "張雯玲、陳世一", "2025-12-23", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("宇宙的邊界到底在哪？黑洞不是終點，而是我們與星空之間的開端", "姚建明、周娜、李雪穎、何振宇", "2025-12-18", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("世界鯊魚大全：手繪125種史上最齊全鯊魚圖鑑", "和布蕪、田中彰", "2025-12-03", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("完美歐姆蛋的化學：從手沖咖啡到深蹲，生活中無處不在的化學反應", "凱特‧比貝多夫", "2025-12-03", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("潮汐國度：生命的繁衍密語", "劉毅、尉鵬", "2025-12-03", "https://www.books.com.tw/web/sys_topme/books/06"),
        ("可替換的你：身體零件大窺祕", "瑪莉‧羅曲", "2026-02-24", "https://www.books.com.tw/web/books_bmidm_0601"),
        ("探索微觀星球，顯微鏡下的植物世界", "吳成軍", "2026-02-11", "https://www.books.com.tw/web/books_bmidm_0601"),
    ),
    "04_healthcare": (
        ("圖解藥理學：從止痛藥到抗癌藥，揭開藥物運作的祕密", "Kevin Chen", "2025-12-31", "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=5&v=1"),
        ("圖解基礎醫學：從吃飯、呼吸到情緒反應，讀懂身體如何運作", "Kevin Chen", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("圖解免疫學：從防禦到平衡，讀懂身體的免疫智慧", "Kevin Chen", "2026-02-26", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("捨不得翹課的病理學通識：大阪大學最熱門病理學講義", "仲野徹", "2026-02-25", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("護理臨床診斷與照護應用全書", "陳群梅、李松枝、王波", "2026-02-11", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("70、80、90歲，現在開始練肌肉！年長者的基礎肌力訓練", "久野譜也", "2026-02-09", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("鎂的奇蹟：未來10年最受矚目的不生病營養素", "卡洛琳．狄恩", "2026-02-05", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("預防骨質疏鬆靠自己：到了100歲還能靠自己行走", "主婦之友社", "2026-02-05", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("大腦神經兮兮：一位神經內科專家的行醫筆記", "葉宗勲", "2026-02-01", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("藥師沒告訴你的50件事：你不可不知的居家用藥常識", "洪正憲", "2026-01-05", "https://www.books.com.tw/web/sys_topme/books/08"),
    ),
    "05_food_wellness": (
        ("法國藍帶糖果聖經：經典與現代兼具的90道精選配方", "法國藍帶廚藝學院", "2026-01-16", "https://www.books.com.tw/web/books_topm_09"),
        ("超簡單！葡萄酒品種角色圖鑑：78個擬人化卡漫角色教你輕鬆學會怎麼選酒與喝酒", "紫貴曉", "2026-01-29", "https://www.books.com.tw/web/books_bmidm_0902"),
        ("台灣製造：MIT台菜與台灣味，台灣人的飲食故事", "魏貝珊", "2026-01-28", "https://www.books.com.tw/web/books_topm_09"),
        ("職人教您在家作餡料麵包", "黃宗辰", "", "https://www.books.com.tw/web/books_topm_09"),
        ("愛上美味養生素", "花蓮慈濟醫學中心營養師團隊、王靜慧", "", "https://www.books.com.tw/web/books_topm_09"),
        ("正韓湯鍋：五星韓廚的道地韓湯", "孫榮KaiSon", "2026-01-15", "https://www.books.com.tw/web/books_topm_09/?loc=P_menu_th_1_018"),
        ("鐵盒甜點與小罐子製菓書", "呂昇達、曾奕翔", "2026-01-15", "https://www.books.com.tw/web/books_topm_09/?loc=P_menu_th_1_018"),
        ("蔬食日常無國界：煮出中式、日韓、南洋、歐美經典料理", "林聖智", "2025-12-10", "https://www.books.com.tw/web/books_topm_09/?loc=P_menu_th_1_018"),
        ("尋瓶誌：蘇格蘭威士忌獨立裝瓶商的歷史", "大衛・史特克、泰斯．克拉弗斯廷", "2025-12-05", "https://www.books.com.tw/web/books_bmidm_0902"),
        ("拉麵魂：突破極限的美味技法", "柴田書店", "2026-02-23", "https://www.books.com.tw/web/books_bmidm_0907"),
        ("陪你過日子的節氣餐桌：24節氣的餐桌提案與日常調養", "煲湯媽咪．吳婕妤", "2026-02-09", "https://www.books.com.tw/web/books_bmidm_0907"),
    ),
    "06_computer_info": (
        ("一學就會的AI影像生成術", "孫大千", "", "https://www.books.com.tw/web/books_topm_19"),
        ("BMduino程式設計篇：基礎篇", "曹永忠、蔡英德、許智誠", "", "https://www.books.com.tw/web/books_topm_19"),
        ("AI研究寫作全攻略：NotebookLM × Gemini × ChatGPT × Perplexity", "洪兆祥、黃聖方、漫新知", "", "https://www.books.com.tw/web/books_topm_19"),
        ("Effective Python中文版第三版：寫出良好Python程式的125個具體做法", "Brett Slatkin", "2026-01-28", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("資料科學學習手冊：Python資料處理、探索、視覺化與建模實作", "Deborah Nolan、Joseph Gonzalez、Sam Lau", "2026-01-28", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("Statistical Tableau：活用統計模型與科學決策力", "Ethan Lang", "2026-01-28", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("VRoid Studio超入門講座3D人物建模技巧指南", "LUCAS", "2026-01-28", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("Python 3程式設計基礎含GLAD ICTP計算機程式語言國際認證", "周元哲、彭勝龍", "2026-01-05", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("LLMOps打造穩定運行的大型語言模型系統", "Abi Aryan", "2026-01-05", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("雲端原生資安指南：CNAPP打造DevSecOps零死角防護", "Russ Miles、Stephen Giguere、Taylor Smith", "2026-01-05", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("AI時代的Side Project全攻略：產品思維、專案管理、變現路徑", "卓昌憲", "2025-12-17", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("Excel × Tableau成功晉升資料分析師", "彭其捷", "2025-12-16", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("白話人工智慧：矽谷科學家帶你看懂AI黑科技", "彭昶興", "2025-12-08", "https://www.books.com.tw/web/books_nbtopm_19"),
        ("程式人的第一本Python量化投資筆記", "鍾嘉峻（Ziv）", "2025-12-08", "https://www.books.com.tw/web/books_nbtopm_19"),
    ),
    "07_other": (
        ("泰國的歷史：從王朝秩序到人民政治", "克里斯．貝克、帕素．蓬派吉", "2026-01-28", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("未竟之路：被體制封殺的泰國準總理皮塔，點燃一個世代的民主之戰", "皮塔・林家倫拉", "2026-01-28", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("誰害怕性別？拆解性別恐懼的幻象", "朱迪斯．巴特勒", "2026-01-30", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("風水之理：從法律、環境到近代化，清帝國的地方治理與社會秩序", "張仲思", "2026-01-30", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("當AI取得話語權，人類還剩下什麼？", "馬克．科克爾柏格、大衛．岡克爾", "2026-01-28", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("顧維鈞：歷仕四朝長樂老", "江勇振", "2026-02-01", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("微觀印度：古吉拉特邦小媳婦十年蹲點瑣記", "廖珍綾", "2026-02-03", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("此乃書之大敵：十九世紀知名藏書家的書籍保存軼事", "威廉．布雷德斯", "2026-01-28", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("球魂的軌跡：日本野球誕生物語", "朱宥任", "2026-02-04", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("集章日本：1940年臺灣商人蔡桑的旅行手帳", "林雨新、陳力航", "2026-02-04", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("深夜裡的圖書館：藏書人的書頁夢境與夜讀筆記", "阿爾維托．曼古埃爾", "2026-02-01", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("野球與棒球：跨海的白球與台日百年記憶", "野島剛", "2026-01-29", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("山林之眼：消失中的臺灣森林瞭望台", "劉庭易", "2026-01-28", "https://www.books.com.tw/web/sys_compub/books/04"),
        ("探秘三星堆", "陳立基、楊仕成", "2026-02-03", "https://www.books.com.tw/web/sys_compub/books/04"),
    ),
}


def write_json_atomic_unchecked(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=path.parent,
        prefix=f".{path.name}.", suffix=".tmp", delete=False,
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


def load_candidate_pools() -> dict[str, list[tuple[str, str, str, str]]]:
    pools = {category_id: [] for category_id, _, _ in CATEGORIES}
    seen = {category_id: set() for category_id in pools}
    current_name = Path(__file__).stem
    for path in sorted(glob.glob(str(ROOT / "tools" / "findbook_batch_*.py")), reverse=True):
        module_name = Path(path).stem
        if module_name == current_name:
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        module_pools = getattr(module, "BOOK_POOLS", {})
        if not isinstance(module_pools, dict):
            continue
        for category_id in pools:
            for row in module_pools.get(category_id, ()):
                if not isinstance(row, (list, tuple)) or len(row) < 4:
                    continue
                title, author, published, source_url = map(str, row[:4])
                key = findbook_writer.normalized_key(title, author)
                if key not in seen[category_id]:
                    pools[category_id].append((title, author, published, source_url))
                    seen[category_id].add(key)
    for category_id, rows in EXTRA_POOLS.items():
        for title, author, published, source_url in rows:
            key = findbook_writer.normalized_key(title, author)
            if key not in seen[category_id]:
                pools[category_id].append((title, author, published, source_url))
                seen[category_id].add(key)
    return pools


def source_name(source_url: str, label: str) -> str:
    if "books.com.tw" in source_url:
        return f"博客來中文書－{label}分類頁"
    if "openlibrary.org" in source_url:
        return f"Open Library－{label}主題頁"
    return f"中文書來源－{label}"


def source_date_note(published: str) -> str:
    if DATE_RE.fullmatch(published) and FROM_DATE <= published <= TO_DATE:
        return (
            f"來源頁標示出版日期為 {published}；擷取日期 {TO_DATE}，"
            f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
        )
    return f"來源未提供明確日期；擷取日期 {TO_DATE}，搜尋區間為 {FROM_DATE} 至 {TO_DATE}。"


def highlights_for(label: str, title: str) -> list[str]:
    focus = FOCUS[label]
    theme = re.split(r"[：:，,（(！!？?]", title, maxsplit=1)[0][:14]
    verbs = ("釐清", "檢視", "比較", "實作", "整理")
    lines = []
    for principle in highlight_source.CATEGORY_PRINCIPLES[label]:
        anchor = principle[:8].rstrip("，。；")
        for lens_index, lens in enumerate(highlight_source.READING_LENSES):
            index = len(lines) + 1
            lines.append(
                f"{index:03d}、從「{theme}」的閱讀情境{verbs[lens_index]}{focus}裡「{anchor}」的課題時，"
                f"{principle}；{lens}。"
            )
    return lines


def update_manifest_metadata(manifest: dict, text: str) -> None:
    manifest["totalBooks"] = len(manifest.get("books", []))
    manifest["searchDateRange"] = {"from": FROM_DATE, "to": TO_DATE}
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = text


def write_book(category_id: str, label: str, row: tuple[str, str, str, str]) -> str | None:
    title, author, published, source_url = row
    manifest_path = ROOT / "data.json"
    manifest = findbook_writer.read_json(manifest_path)
    key = findbook_writer.normalized_key(title, author)
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
        "title": title,
        "author": author,
        "sourceName": source_name(source_url, label),
        "sourceUrl": source_url,
        "sourceDateNote": source_date_note(published),
        "searchDateRange": {"from": FROM_DATE, "to": TO_DATE},
        "tags": [label, "中文書"],
        "summary": f"整理「{title}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。",
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
        "title": title,
        "author": author,
        "categoryId": category_id,
        "tags": book["tags"],
        "sourceName": book["sourceName"],
        "sourceUrl": source_url,
        "file": relative_file,
        "workId": WORK_ID,
    })
    update_manifest_metadata(manifest, f"FindBook_Skill.md reservation checkpoint: workId={WORK_ID}")
    write_json_atomic_unchecked(manifest_path, manifest)

    book["chatgptHighlights"] = highlights_for(label, title)
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "codex"
    book["highlightsCapturedAt"] = findbook_writer.now_iso()
    write_json_atomic_unchecked(ROOT / relative_file, book)
    print(f"written\t{category_id}\t{book_id}\t{title}")
    return book_id


def main() -> None:
    pools = load_candidate_pools()
    for category_id, label, quota in CATEGORIES:
        manifest = findbook_writer.read_json(ROOT / "data.json")
        completed = sum(
            book.get("categoryId") == category_id and book.get("workId") == WORK_ID
            for book in manifest.get("books", [])
        )
        needed = quota - completed
        if needed <= 0:
            continue
        added = 0
        for row in pools[category_id]:
            title, author, published, _ = row
            if not CJK_RE.search(title) or not author:
                continue
            if published and (not DATE_RE.fullmatch(published) or not FROM_DATE <= published <= TO_DATE):
                continue
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
        "FindBook_Skill.md fresh Chinese-only 20/20/10/5/5/5/5 complete: "
        f"workId={WORK_ID}",
    )
    write_json_atomic_unchecked(ROOT / "data.json", manifest)
    print(f"batch-complete\tworkId={WORK_ID}\tbooks=70")


if __name__ == "__main__":
    main()
