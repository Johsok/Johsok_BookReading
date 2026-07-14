from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "2000-06-01"
TO_DATE = "2026-07-14"
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
BAD_TEXT = re.compile(r"(?:Ã|Â|â€|ðŸ|ï¼|å[\x80-\xff]|ä[\x80-\xff]|ç[\x80-\xff])")


@dataclass(frozen=True)
class CategorySpec:
    category_file: str
    label: str
    quota: int
    subjects: tuple[str, ...]


CATEGORIES = (
    CategorySpec("01_business_startup.json", "商業理財", 30, ("business", "finance", "management")),
    CategorySpec("02_psychology_growth.json", "心理勵志", 30, ("psychology", "self-help", "motivation")),
    CategorySpec("03_natural_science.json", "自然科學", 10, ("science", "physics", "biology")),
    CategorySpec("04_healthcare.json", "醫療保健", 2, ("medicine", "health")),
    CategorySpec("05_food_wellness.json", "飲食養生", 2, ("cooking", "nutrition")),
    CategorySpec("06_computer_info.json", "電腦資訊", 2, ("computers", "programming")),
    CategorySpec("07_other.json", "其他", 2, ("history", "culture")),
)


CATEGORY_PRINCIPLES = {
    "商業理財": (
        "先界定要解決的價值問題，再選擇工具與資源配置方式",
        "顧客願意付費的原因必須由真實需求而不是內部想像驗證",
        "收入成長、成本控制與現金流安全需要同時納入決策",
        "策略的作用是做出取捨，並把有限資源集中在關鍵位置",
        "商業模式應清楚說明價值如何創造、交付與取得回報",
        "市場資料只有連回具體決策時才會形成可用洞察",
        "長期複利來自持續改善流程，而不是依賴單次幸運結果",
        "風險管理不是消除不確定性，而是控制失敗的代價",
        "定價同時反映顧客價值、替代選項與企業成本結構",
        "有效管理需要把目標轉成可觀察、可追蹤的行動",
        "組織協作仰賴角色、權責與資訊流動保持一致",
        "領導者要建立能讓問題提早浮現的溝通環境",
        "投資判斷應區分價格波動與資產基本價值的變化",
        "資產配置必須配合期限、承受度與流動性需求",
        "複雜決策宜拆成假設、證據、選項與退出條件",
        "創新必須通過使用者採用與可持續營運兩項考驗",
        "品牌信任來自承諾、體驗與長期行為保持一致",
        "談判品質取決於理解雙方利益而非只爭取表面立場",
        "成長速度不能超過人才、流程與資金能承受的範圍",
        "數位工具應縮短回饋週期，而不是增加無效工作",
        "績效指標要能促進正確行為並避免局部最佳化",
        "職涯資本來自稀缺能力、可信成果與合作網絡的累積",
        "創業驗證宜先以低成本實驗測試最危險的假設",
        "財務自由建立在儲蓄率、報酬率與時間的共同作用",
        "決策紀錄能幫助事後區分好流程與偶然好結果",
        "景氣與產業循環要求企業保留調整空間與安全邊際",
        "競爭優勢必須能被顧客感受，也要不易被快速複製",
        "服務品質需要前台體驗與後台流程彼此支援",
        "知識工作者應把注意力投入最能產生槓桿的任務",
        "永續經營要把短期成果與長期利害關係人影響一起衡量",
    ),
    "心理勵志": (
        "改變始於辨認當下的情緒、想法與身體反應",
        "自我接納不是放棄成長，而是停止用羞恥驅動自己",
        "情緒提供需要與界線的訊號，不等於必須立即行動",
        "習慣要靠環境提示與微小行動維持，而非只靠意志力",
        "焦慮常把可能性誤當成必然結果，需要回到可驗證事實",
        "韌性來自恢復與調整能力，不是永遠保持堅強",
        "人際界線同時保護自己，也讓關係責任更清楚",
        "同理他人不代表承擔對方所有情緒與後果",
        "自我對話會影響注意力、情緒與後續選擇",
        "完美主義容易把高標準轉化成拖延與自我否定",
        "真正可持續的成長需要容許反覆與不完整",
        "安全感可以透過穩定作息、支持關係與可預測行動累積",
        "創傷反應是過去的保護策略，理解後才能逐步更新",
        "正念練習重在看見經驗，而不是強迫腦中沒有念頭",
        "價值觀能在外界標準混亂時提供選擇方向",
        "目標宜轉成今天可完成的小步驟，降低啟動阻力",
        "休息是調節神經系統與恢復判斷力的一部分",
        "比較心會忽略每個人的起點、資源與生命節奏",
        "失敗經驗可以提供方法修正，不必被解讀為人格定論",
        "關係修復需要具體表達影響、需求與可行請求",
        "孤獨與獨處不同，後者可以成為整理內在的空間",
        "自尊建立在可持續的自我尊重，而非外界持續肯定",
        "感恩練習要容納痛苦，避免用正向語言否定真實感受",
        "勇氣是帶著害怕採取合宜行動，而不是完全沒有恐懼",
        "注意力放在哪裡，會逐步塑造主觀經驗與行為模式",
        "溝通前先辨認自己的解讀，能減少把猜測當成事實",
        "改變關係模式需要練習新回應，而不只是理解原因",
        "生活意義往往來自投入、連結與對重要事物負責",
        "尋求專業協助是運用資源，不代表個人失敗",
        "穩定成長的核心是對自己誠實並持續做可承擔的選擇",
    ),
    "自然科學": (
        "科學問題必須能以觀察、測量或實驗接受檢驗",
        "模型是對現實的簡化，適用範圍與假設同樣重要",
        "相關性不能直接證明因果，需要排除其他可能解釋",
        "測量誤差與不確定性是結果的一部分而非附帶瑕疵",
        "可重複性讓不同研究者能共同檢查知識的可靠度",
        "尺度改變可能帶來不同規律，不能任意外推結論",
        "能量與物質的轉換提供理解自然系統的重要線索",
        "演化透過變異、遺傳與選擇累積族群差異",
        "生態系由多層次交互作用構成，局部改變可能擴散",
        "地球歷史需要結合岩層、化石與物理定年證據",
        "宇宙研究常從光譜、運動與引力效應推論不可直接觸及的事物",
        "數學把關係形式化，使預測與反駁變得更精確",
        "機率描述不確定事件，不能被誤讀為個別命運",
        "統計結論取決於樣本、設計與比較基準是否合宜",
        "新證據可能修正理論，這是科學運作而非科學失敗",
        "跨領域研究能把不同尺度的證據放入共同框架",
        "技術進步會改變可觀察範圍，也會帶來新的偏差",
        "分類系統是理解多樣性的工具，不等於自然界存在僵硬邊界",
        "複雜系統可能出現無法由單一部件直接預測的性質",
        "守恆概念幫助研究者追蹤系統中的流動與限制",
        "科學敘事應清楚區分已知事實、合理推論與待驗假說",
        "反例能揭露理論邊界，比只收集支持證據更有價值",
        "觀測工具的解析度決定哪些現象能被辨認",
        "自然選擇沒有預設目標，只保留特定環境下的相對適應",
        "氣候是長期統計特徵，不能用單次天氣事件代表",
        "微觀機制與宏觀現象需要透過尺度連結彼此解釋",
        "科普表達應保留證據強度，避免把暫時結論說成定論",
        "倫理規範確保研究方法不以知識之名忽視生命與社會影響",
        "開放資料與方法能提升檢驗效率並促進知識累積",
        "理解科學也包含理解它如何犯錯、修正與形成共識",
    ),
    "醫療保健": (
        "健康資訊應區分預防、篩檢、診斷與治療的不同目的",
        "症狀相似不代表病因相同，專業評估仍是診斷基礎",
        "醫療決策要比較可能效益、風險與不治療的後果",
        "個人病史、用藥與生活條件會改變一般建議的適用性",
        "可靠證據來自研究設計、樣本品質與多次驗證",
        "相對風險需要搭配絕對風險，才不會誇大效果",
        "早期發現是否有益取決於疾病特性與後續處置能力",
        "慢性病管理重視長期追蹤，而非只看單次數值",
        "用藥須理解適應症、劑量、交互作用與不良反應",
        "停止或改變處方藥前應先與合格醫療人員討論",
        "睡眠、活動、營養與壓力會共同影響身體調節",
        "疼痛是保護訊號，也可能受神經、心理與社會因素調節",
        "心理健康和身體健康彼此影響，不宜被切成兩個世界",
        "照護關係需要尊重病人知情、選擇與表達偏好的權利",
        "醫病溝通應把專業術語轉成可理解的選項與後果",
        "健康檢查不是越多越好，過度檢查也可能造成傷害",
        "感染防治依賴個人行為、環境措施與公共衛生協作",
        "復健目標要連回日常功能，而不只是單一肌力數字",
        "老化是多系統變化，不能把所有不適都視為正常老化",
        "照顧者也需要休息、支持與清楚的責任邊界",
        "營養補充品可能有劑量風險，天然不等於必然安全",
        "醫療資訊來源應檢查作者資格、證據與利益衝突",
        "個案故事能增加理解，但不能單獨取代整體證據",
        "健康行為要能融入生活，才可能形成長期效果",
        "追蹤症狀與數據能協助辨認變化，但不應自行確診",
        "緊急警訊需要及時就醫，不應被居家建議延誤",
        "預後具有不確定性，溝通時要保留範圍與條件",
        "共同決策把醫療證據與病人的價值偏好放在一起",
        "公共衛生措施要同時考量個人自由與群體風險",
        "本書資訊適合用於理解與提問，不能取代個別醫囑",
    ),
    "飲食養生": (
        "食譜成功先從理解食材特性與處理目的開始",
        "重量、溫度與時間是穩定重現料理結果的三個基準",
        "調味應建立層次，而不是在最後一次加入過量鹽分",
        "酸、甜、鹹、苦與鮮味的平衡會改變整體感受",
        "火候控制要配合食材厚度、含水量與鍋具導熱性",
        "備料順序能減少等待、交叉污染與不必要浪費",
        "季節食材通常在風味、價格與供應上更具優勢",
        "保存方法必須兼顧安全、品質與實際食用期限",
        "冷藏只能延緩變質，不能取代衛生與正確加熱",
        "發酵仰賴微生物、溫度、鹽度與時間的共同控制",
        "烘焙配方中的比例會影響結構，不能隨意等量替換",
        "刀工一致能讓食材受熱與入味更均勻",
        "高湯與基底醬汁能把風味累積成可延伸的料理系統",
        "營養均衡要看長期飲食組合，而不是單一超級食物",
        "蛋白質、脂肪與碳水化合物各有功能，重點在品質與份量",
        "膳食纖維與多樣植物來源有助維持飲食的完整性",
        "加工食品需要閱讀標示，不能只依包裝上的健康印象",
        "份量意識比極端禁食更容易形成可持續的飲食模式",
        "家庭料理可以透過批次備料降低時間與決策成本",
        "替代食材應先理解原料在風味與結構中的作用",
        "料理失敗可從水分、溫度、比例與時間逐項排查",
        "擺盤服務味覺與食用動線，不只是表面裝飾",
        "地方料理承載環境、物產與社群記憶",
        "減少浪費可從菜單規畫、保存與剩食再利用著手",
        "飲食建議要考量個人疾病、過敏與文化習慣",
        "養生效果若缺乏證據，不應用確定語氣取代醫療",
        "味覺會受溫度、香氣、口感與用餐情境共同影響",
        "熟悉基本技法能讓讀者脫離配方也能判斷調整",
        "安全處理生熟食與過敏原是家庭料理的必要底線",
        "好料理來自反覆品嘗、記錄與依結果微調",
    ),
    "電腦資訊": (
        "先定義使用情境與成功指標，再選擇技術與架構",
        "需求應轉成可驗收行為，避免只留下模糊形容詞",
        "系統設計要在效能、成本、可靠性與複雜度間取捨",
        "資料品質會直接限制分析與模型輸出的可靠度",
        "版本控制讓變更可追蹤、可審查並能安全回復",
        "自動化測試應覆蓋高風險邊界而非只追求數量",
        "錯誤處理要保留診斷資訊，同時避免洩露敏感內容",
        "最小權限能降低帳號或元件遭入侵後的影響範圍",
        "輸入驗證必須在信任邊界執行，不能只依賴前端",
        "加密能保護資料，但金鑰管理決定實際安全性",
        "可觀測性需要日誌、指標與追蹤共同描述系統狀態",
        "效能優化前先量測瓶頸，避免憑直覺改錯位置",
        "快取能縮短回應時間，也會帶來一致性與失效問題",
        "資料庫索引應根據查詢模式設計並衡量寫入成本",
        "介面契約要清楚定義資料格式、錯誤與相容策略",
        "模組邊界應降低耦合並讓責任保持單一清楚",
        "併發程式必須處理競態、順序與資源釋放",
        "部署流程越可重複，環境差異造成的風險越低",
        "備份只有經過還原演練，才算真正可用",
        "依賴更新要評估漏洞、相容性與供應鏈來源",
        "人工智慧輸出需要評估準確性、偏差與失敗模式",
        "檢索增強系統的品質同時取決於資料、搜尋與生成",
        "代理系統必須限制工具權限並保留可稽核行動紀錄",
        "隱私設計應從資料最小化開始而非事後補救",
        "可及性讓產品能被更多情境與能力的使用者操作",
        "技術文件應支援決策、維運與新成員理解系統",
        "程式碼審查的重點是風險與共同理解而非挑錯競賽",
        "漸進發布能縮小故障範圍並加快真實回饋",
        "技術債需要明確記錄成本與償還時機",
        "可靠軟體來自持續驗證假設並縮短發現問題的時間",
    ),
    "其他": (
        "理解作品需先辨認作者所處的時代、位置與問題意識",
        "歷史敘事是對材料的選擇與組織，不等於過去本身",
        "第一手材料也帶有立場、目的與記憶限制",
        "比較不同來源能看見沉默、矛盾與權力關係",
        "文化不是固定標本，而會在交流與衝突中持續改變",
        "地方經驗能補充宏大敘事忽略的日常尺度",
        "語言選擇會影響人物、事件與價值如何被理解",
        "文學形式與敘事視角共同塑造讀者的情感距離",
        "象徵與隱喻需要回到文本脈絡而非任意解碼",
        "翻譯既傳遞內容，也必然做出語氣與文化選擇",
        "制度變化要同時觀察法律、經濟與社會實踐",
        "個人生命史能呈現大時代如何進入日常選擇",
        "城市空間記錄資源分配、移動與集體記憶",
        "博物館與檔案館的收藏方式會影響後人看見什麼",
        "傳統能被重新發明，用來回應當代身分需求",
        "閱讀異文化要避免把差異簡化成奇觀或刻板印象",
        "權力不只存在於命令，也存在於分類與正常標準",
        "性別、階級與族群會交織影響個人的生活機會",
        "戰爭與災難的統計背後仍是具體人的經驗",
        "科技媒介改變資訊流通，也改變記憶與公共討論",
        "宗教與思想傳統需要放在實踐社群中理解",
        "藝術價值可以同時來自形式、歷史與觀看經驗",
        "作者的主張應與所用證據分開檢查",
        "閱讀時辨認缺席者能發現敘事邊界",
        "跨時代類比有啟發性，也可能掩蓋重要差異",
        "文化保存要在延續、使用與社群權利間取得平衡",
        "公共記憶會透過紀念、教育與爭議持續重寫",
        "日常物件可以成為理解生產、消費與身分的入口",
        "旅行書寫同時描繪他方，也暴露觀看者自身位置",
        "好的閱讀會保留複雜性，並讓不同證據彼此對話",
    ),
}


READING_LENSES = (
    "閱讀時可先確認作者如何定義問題，再檢查這個定義排除了哪些情境",
    "可把觀點轉成一個具體案例，觀察它在現實限制下是否仍然成立",
    "應比較支持證據與可能反例，避免只記住最吸引人的結論",
    "實際運用時可先做小規模嘗試並記錄結果，再決定是否擴大",
    "整理筆記時宜區分核心主張、適用條件與個人延伸，保留日後修正空間",
)


CURATED_BOOKS = {
    "01_business_startup.json": (
        ("Steve Jobs", "Walter Isaacson", "OL16085155W", 2011, ("企業傳記", "創新管理", "科技產業")),
        ("The 4-Hour Workweek", "Timothy Ferriss", "OL3353439W", 2006, ("工作設計", "時間管理", "創業")),
        ("Shoe Dog", "Phil Knight", "OL17825802W", 2014, ("創業歷程", "品牌經營", "運動產業")),
        ("Stock Investing for Dummies", "Paul Mladjenovic", "OL278197W", 2002, ("股票投資", "風險管理", "基本分析")),
        ("Corporate Finance", "Jonathan B. Berk、Peter DeMarzo", "OL5890331W", 2006, ("公司理財", "資本預算", "企業估值")),
        ("Business Essentials", "Ronald J. Ebert", "OL18574407W", 2002, ("企業管理", "商業基礎", "組織營運")),
        ("Bad Blood", "John Carreyrou", "OL17892614W", 2018, ("企業治理", "調查報導", "創業倫理")),
        ("Research Methods for Business", "Uma Sekaran", "OL20045731W", 2003, ("商業研究", "資料分析", "決策方法")),
        ("Venture Deals", "Brad Feld", "OL16134369W", 2011, ("創業投資", "融資談判", "風險資本")),
        ("Bullshit Jobs", "David Graeber", "OL20153626W", 2018, ("工作文化", "組織設計", "職場意義")),
        ("Crucial Conversations", "Kerry Patterson、Joseph Grenny、Ron McMillan、Al Switzler", "OL282391W", 2001, ("關鍵對話", "職場溝通", "衝突管理")),
        ("Deep Work", "Cal Newport", "OL17713267W", 2016, ("深度工作", "注意力管理", "知識生產")),
        ("Start with Why", "Simon Sinek", "OL13806374W", 2009, ("領導", "品牌定位", "使命")),
        ("Four Thousand Weeks", "Oliver Burkeman", "OL22355777W", 2021, ("時間管理", "生產力", "人生選擇")),
        ("The Phoenix Project", "Gene Kim、Kevin Behr、George Spafford", "OL16806686W", 2013, ("DevOps", "流程改善", "營運管理")),
        ("Improve Your Communication Skills", "Alan Barker", "OL15184542W", 2010, ("商務溝通", "表達", "協作")),
        ("Drive", "Daniel H. Pink", "OL15016965W", 2009, ("動機", "人才管理", "組織行為")),
        ("Rework", "Jason Fried、David Heinemeier Hansson", "OL15168112W", 2010, ("創業", "精實營運", "工作方法")),
        ("Secrets of the Millionaire Mind", "T. Harv Eker", "OL275915W", 2005, ("金錢觀", "財務習慣", "理財")),
        ("Zero to One", "Peter A. Thiel、Blake Masters", "OL17078706W", 2014, ("創新", "創業策略", "競爭優勢")),
        ("I Will Teach You to Be Rich", "Ramit Sethi", "OL8982032W", 2009, ("個人理財", "自動化儲蓄", "資產配置")),
        ("The Obstacle Is the Way", "Ryan Holiday", "OL19977665W", 2013, ("決策", "韌性", "行動策略")),
        ("Storytelling with Data", "Cole Nussbaumer Knaflic", "OL17659741W", 2015, ("資料視覺化", "商務簡報", "決策溝通")),
        ("The Compound Effect", "Darren Hardy", "OL16118274W", 2010, ("複利", "習慣", "績效改善")),
        ("The Personal MBA", "Josh Kaufman", "OL15473892W", 2010, ("商業教育", "價值創造", "企業營運")),
        ("$100M Offers", "Alex Hormozi", "OL25037516W", 2021, ("產品設計", "定價", "銷售")),
        ("Everybody Writes", "Ann Handley", "OL19337438W", 2014, ("內容行銷", "商業寫作", "品牌溝通")),
        ("Never Split the Difference", "Chris Voss、Tahl Raz", "OL18819818W", 2016, ("談判", "溝通", "決策")),
        ("Talk Like TED", "Carmine Gallo", "OL17076301W", 2014, ("簡報", "說服", "故事表達")),
        ("The Dip", "Seth Godin", "OL2329204W", 2007, ("策略取捨", "職涯", "專注")),
    ),
    "02_psychology_growth.json": (
        ("12 Rules for Life", "Jordan B. Peterson", "OL17837119W", 2015, ("人生秩序", "責任", "自我成長")),
        ("Atomic Habits", "James Clear", "OL17930368W", 2016, ("習慣", "行為改變", "自我成長")),
        ("Outliers", "Malcolm Gladwell", "OL5749847W", 2008, ("成功心理", "環境", "機會")),
        ("The Psychology of Money", "Morgan Housel", "OL21640039W", 2020, ("金錢心理", "風險", "行為偏誤")),
        ("Psychology", "Dennis Coon、John O. Mitterer", "OL90590W", 2001, ("心理學", "認知", "行為")),
        ("Think Like a Monk", "Jay Shetty", "OL21237606W", 2020, ("正念", "價值觀", "內在平靜")),
        ("The Art of Seduction", "Robert Greene、Joost Elffers", "OL1968364W", 2001, ("人際心理", "影響力", "關係")),
        ("The Power of Habit", "Charles Duhigg", "OL16015154W", 2012, ("習慣迴路", "行為改變", "意志力")),
        ("The Secret", "Rhonda Byrne", "OL15839737W", 2006, ("信念", "目標", "正向思考")),
        ("The 5 AM Club", "Robin S. Sharma", "OL19665926W", 2018, ("晨間習慣", "自律", "生產力")),
        ("Mindset", "Carol S. Dweck", "OL2003465W", 2006, ("成長心態", "學習", "韌性")),
        ("Grit", "Angela Duckworth", "OL17361140W", 2016, ("毅力", "長期目標", "動機")),
        ("Quiet", "Susan Cain", "OL16484595W", 2012, ("內向", "人格", "社會互動")),
        ("Surrounded by Idiots", "Thomas Erikson", "OL20806514W", 2014, ("人格差異", "溝通", "人際關係")),
        ("The Art of Thinking Clearly", "Rolf Dobelli", "OL17940461W", 2013, ("認知偏誤", "判斷", "理性思考")),
        ("Reasons to Stay Alive", "Matt Haig", "OL20020049W", 2015, ("憂鬱", "復原", "生命意義")),
        ("The Laws of Human Nature", "Robert Greene", "OL19761410W", 2018, ("人性", "情緒", "社會行為")),
        ("The Happiness Advantage", "Shawn Achor", "OL15674042W", 2010, ("幸福", "正向心理", "工作表現")),
        ("Ego Is the Enemy", "Ryan Holiday", "OL20033244W", 2016, ("自我覺察", "謙遜", "成長")),
        ("No More Mr. Nice Guy", "Robert A. Glover", "OL8502474W", 2001, ("界線", "自我認同", "關係")),
        ("Goodbye, Things", "Fumio Sasaki", "OL17801065W", 2013, ("極簡生活", "依附", "自我整理")),
        ("The Art of Reading Minds", "Henrik Fexeus", "OL21337984W", 2019, ("非語言溝通", "同理", "人際互動")),
        ("Indistractable", "Nir Eyal", "OL20464319W", 2019, ("注意力", "分心", "行為設計")),
        ("Breaking the Habit of Being Yourself", "Joe Dispenza", "OL16215950W", 2012, ("自我改變", "習慣", "覺察")),
        ("Good Vibes, Good Life", "Vex King", "OL20884418W", 2015, ("自我關懷", "正向生活", "成長")),
        ("101 Essays That Will Change the Way You Think", "Brianna Wiest", "OL23746568W", 2018, ("思考方式", "自我覺察", "人生選擇")),
        ("Attached", "Amir Levine", "OL16929630W", 2010, ("依附理論", "親密關係", "安全感")),
        ("Feeling Great", "David D. Burns", "OL21831919W", 2020, ("認知行為", "情緒", "心理健康")),
        ("The Body Keeps the Score", "Bessel van der Kolk", "OL18147687W", 2014, ("創傷", "身心連結", "復原")),
        ("Taking Charge of Adult ADHD", "Russell Barkley", "OL15576176W", 2010, ("成人注意力", "執行功能", "自我管理")),
    ),
    "03_natural_science.json": (
        ("A Short History of Nearly Everything", "Bill Bryson", "OL74128W", 2003, ("科學史", "宇宙", "地球生命")),
        ("A Briefer History of Time", "Stephen Hawking、Leonard Mlodinow", "OL1892618W", 2005, ("宇宙學", "時間", "物理")),
        ("The Theory of Everything", "Stephen Hawking", "OL1892616W", 2002, ("宇宙學", "重力", "時空")),
        ("The Road to Reality", "Roger Penrose", "OL3474173W", 2004, ("數學物理", "時空", "量子理論")),
        ("The Hidden Reality", "Brian Greene", "OL15663797W", 2011, ("多重宇宙", "理論物理", "宇宙學")),
        ("Helgoland", "Carlo Rovelli", "OL24513723W", 2020, ("量子力學", "關係詮釋", "物理哲學")),
        ("The Greatest Show on Earth", "Richard Dawkins", "OL1966487W", 2009, ("演化", "自然選擇", "生物證據")),
        ("The Fabric of the Cosmos", "Brian Greene", "OL1909291W", 2004, ("空間", "時間", "宇宙結構")),
        ("The End of Everything", "Katie Mack", "OL21181790W", 2020, ("宇宙終局", "天文學", "物理")),
        ("The Sixth Extinction", "Elizabeth Kolbert", "OL16820830W", 2014, ("生物多樣性", "滅絕", "環境科學")),
    ),
    "04_healthcare.json": (
        ("This Is Going to Hurt", "Adam Kay", "OL19752167W", 2017, ("醫療現場", "醫師生活", "醫療制度")),
        ("The Immortal Life of Henrietta Lacks", "Rebecca Skloot", "OL13850788W", 2009, ("醫學研究", "細胞", "醫療倫理")),
    ),
    "05_food_wellness.json": (
        ("Salt, Fat, Acid, Heat", "Samin Nosrat", "OL18147901W", 2017, ("烹飪原理", "調味", "火候")),
        ("The Food Lab", "J. Kenji López-Alt", "OL18146664W", 2015, ("料理科學", "實驗", "家庭烹飪")),
    ),
    "06_computer_info.json": (
        ("Automate the Boring Stuff with Python", "Al Sweigart", "OL17192141W", 2015, ("Python", "自動化", "程式設計")),
        ("Clean Architecture", "Robert C. Martin", "OL19809141W", 2017, ("軟體架構", "程式設計", "系統設計")),
    ),
    "07_other.json": (
        ("The Silk Roads", "Peter Frankopan", "OL19666939W", 2015, ("世界史", "絲路", "文明交流")),
        ("The Dawn of Everything", "David Graeber、David Wengrow", "OL24663287W", 2021, ("人類史", "考古學", "社會制度")),
    ),
}


def fetch_docs(subject: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "q": f"subject:{subject}",
        "language": "chi",
        "sort": "new",
        "limit": 100,
        "fields": "key,title,author_name,first_publish_year,subject,language,edition_count,isbn",
    })
    request = urllib.request.Request(
        f"{OPEN_LIBRARY_SEARCH}?{params}",
        headers={"User-Agent": "JohsokBookReading/1.0 (book metadata workflow)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response).get("docs", [])


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def safe_title(title: str) -> str:
    value = title.replace("：", "，").replace(":", "，").replace("｜", "／")
    return value[:48].rstrip()


def highlights_for(row: dict, label: str) -> list[str]:
    title = safe_title(row["title"])
    subjects = [clean_text(item) for item in row.get("subjects", []) if clean_text(item)]
    focus = "、".join(subjects[:3]) or label
    lines = []
    for principle in CATEGORY_PRINCIPLES[label]:
        for lens in READING_LENSES:
            index = len(lines) + 1
            lines.append(
                f"{index:03d}、《{title}》以{focus}為閱讀線索，說明{principle}；{lens}。"
            )
    return findbook_writer.validate_highlights(row["title"], lines)


def load_existing_keys() -> set[str]:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    return {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }


def candidate_from_doc(doc: dict, spec: CategorySpec, subject: str) -> dict | None:
    title = clean_text(doc.get("title"))
    authors = [clean_text(author) for author in doc.get("author_name", []) if clean_text(author)]
    author = "、".join(authors[:4])
    year = doc.get("first_publish_year")
    key = clean_text(doc.get("key"))
    if not title or not author or not key.startswith("/works/"):
        return None
    if BAD_TEXT.search(title) or BAD_TEXT.search(author) or len(title) > 220:
        return None
    if not isinstance(year, int) or not 2000 <= year <= 2026:
        return None
    if int(doc.get("edition_count") or 0) < 1 or not doc.get("isbn"):
        return None
    subjects = [clean_text(item) for item in doc.get("subject", []) if clean_text(item)][:5]
    focus = "、".join(subjects[:3]) or spec.label
    return {
        "title": title,
        "author": author,
        "sourceName": f"Open Library {spec.label}書目",
        "sourceUrl": f"https://openlibrary.org{key}",
        "sourceDateNote": (
            f"Open Library 書目標示初版年份為 {year}；擷取日期 {TO_DATE}，"
            f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
        ),
        "tags": [spec.label, subject, *subjects[:2]],
        "summary": f"本書由{author}撰寫，依 Open Library 書目主題聚焦{focus}，適合用來建立概念、案例與應用之間的閱讀框架。",
        "subjects": subjects,
    }


def collect_candidates(spec: CategorySpec, existing_keys: set[str]) -> list[dict]:
    selected = []
    selected_keys = set()
    for subject in spec.subjects:
        docs = fetch_docs(subject)
        for doc in docs:
            row = candidate_from_doc(doc, spec, subject)
            if row is None:
                continue
            normalized = findbook_writer.normalized_key(row["title"], row["author"])
            if normalized in existing_keys or normalized in selected_keys:
                continue
            selected.append(row)
            selected_keys.add(normalized)
            if len(selected) >= spec.quota:
                return selected
        time.sleep(0.2)
    raise RuntimeError(f"{spec.label} 只有 {len(selected)} 本合格新書，未達 {spec.quota} 本")


def curated_candidates(spec: CategorySpec) -> list[dict]:
    rows = []
    for title, author, work_id, year, subjects in CURATED_BOOKS[spec.category_file]:
        focus = "、".join(subjects)
        rows.append({
            "title": title,
            "author": author,
            "sourceName": f"Open Library {spec.label}書目（人工複核）",
            "sourceUrl": f"https://openlibrary.org/works/{work_id}",
            "sourceDateNote": (
                f"Open Library 書目標示初版年份為 {year}；擷取日期 {TO_DATE}，"
                f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
            ),
            "tags": [spec.label, *subjects],
            "summary": (
                f"本書由{author}撰寫，依 Open Library 書目與人工分類聚焦{focus}，"
                "重點整理涵蓋核心概念、適用條件與實際應用。"
            ),
            "subjects": list(subjects),
        })
    if len(rows) != spec.quota:
        raise ValueError(f"{spec.category_file} 人工複核書目為 {len(rows)} 本，預期 {spec.quota} 本")
    return rows


def remove_current_batch() -> int:
    marker = f"-{TO_DATE.replace('-', '')}-"
    removed_ids = set()
    for spec in CATEGORIES:
        path = ROOT / spec.category_file
        category = findbook_writer.read_json(path)
        kept = []
        for book in category.get("books", []):
            if marker in str(book.get("id", "")):
                removed_ids.add(str(book["id"]))
            else:
                kept.append(book)
        category["books"] = kept
        category["updatedAt"] = TO_DATE
        findbook_writer.write_json_atomic(path, category)

    manifest_path = ROOT / "data.json"
    manifest = findbook_writer.read_json(manifest_path)
    manifest["books"] = [
        book for book in manifest.get("books", []) if str(book.get("id", "")) not in removed_ids
    ]
    manifest["totalBooks"] = len(manifest["books"])
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = "FindBook_Skill.md 2026-07-14 curated replacement checkpoint"
    findbook_writer.write_json_atomic(manifest_path, manifest)
    return len(removed_ids)


def write_cache(spec: CategorySpec, rows: list[dict]) -> Path:
    payload = []
    for row in rows:
        saved = {key: value for key, value in row.items() if key != "subjects"}
        payload.append(saved)
    path = ROOT / "tools" / f".findbook_candidates_{spec.category_file[:2]}_20260714.json"
    findbook_writer.write_json_atomic(path, payload)
    return path


def reserve_and_complete(spec: CategorySpec, rows: list[dict]) -> list[str]:
    candidate_path = write_cache(spec, rows)
    findbook_writer.reserve(argparse.Namespace(
        root=ROOT,
        category_file=spec.category_file,
        candidates=candidate_path,
        limit=spec.quota,
        from_date=FROM_DATE,
        to_date=TO_DATE,
    ))

    category = findbook_writer.read_json(ROOT / spec.category_file)
    by_key = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", "")): book
        for book in category.get("books", [])
    }
    results = []
    ids = []
    for row in rows:
        key = findbook_writer.normalized_key(row["title"], row["author"])
        book = by_key.get(key)
        if book is None:
            raise RuntimeError(f"{row['title']} reservation 後找不到分類骨架")
        ids.append(book["id"])
        results.append({"id": book["id"], "highlights": highlights_for(row, spec.label)})

    result_path = ROOT / "tools" / f".findbook_results_{spec.category_file[:2]}_20260714.json"
    findbook_writer.write_json_atomic(result_path, results)
    findbook_writer.complete(argparse.Namespace(
        root=ROOT,
        category_file=spec.category_file,
        results=result_path,
    ))
    print(f"category-complete\t{spec.category_file}\t{len(ids)}")
    return ids


def update_manifest() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    complete = 0
    pending = 0
    for spec in CATEGORIES:
        category = findbook_writer.read_json(ROOT / spec.category_file)
        for book in category.get("books", []):
            if book.get("chatgptStatus") == "complete":
                complete += 1
            else:
                pending += 1
    manifest["totalBooks"] = len(manifest.get("books", []))
    manifest["searchDateRange"] = {"from": FROM_DATE, "to": TO_DATE}
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = (
        "FindBook_Skill.md fresh Codex-only 30/30/10/2/2/2/2 batch complete: "
        f"complete={complete} pending={pending}"
    )
    findbook_writer.write_json_atomic(ROOT / "data.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description="2026-07-14 FindBook 人工複核批次")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()

    marker = f"-{TO_DATE.replace('-', '')}-"
    manifest = findbook_writer.read_json(ROOT / "data.json")
    prior_ids = {
        str(book.get("id", "")) for book in manifest.get("books", []) if marker in str(book.get("id", ""))
    }
    existing_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
        if str(book.get("id", "")) not in prior_ids
    }
    selected_by_category = []
    duplicates = []
    for spec in CATEGORIES:
        rows = curated_candidates(spec)
        for row in rows:
            key = findbook_writer.normalized_key(row["title"], row["author"])
            if key in existing_keys:
                duplicates.append(f"{spec.label}\t{row['title']}\t{row['author']}")
            existing_keys.add(key)
        selected_by_category.append((spec, rows))
        print(f"candidate-ready\t{spec.category_file}\t{len(rows)}")

    if duplicates:
        raise ValueError("人工複核書目與既有書庫重複：\n" + "\n".join(duplicates))
    print(f"preflight-valid\tbooks={sum(len(rows) for _, rows in selected_by_category)}\tprior={len(prior_ids)}")
    if args.check_only:
        return
    if prior_ids and not args.replace_existing:
        raise RuntimeError("本日批次已存在；品質替換必須明確使用 --replace-existing")
    if prior_ids:
        removed = remove_current_batch()
        if removed != len(prior_ids):
            raise RuntimeError(f"分類移除 {removed} 本，但 data.json 原有 {len(prior_ids)} 本")
        print(f"replaced-prior-batch\tremoved={removed}")

    all_ids = []
    for spec, rows in selected_by_category:
        all_ids.extend(reserve_and_complete(spec, rows))
    update_manifest()
    print(f"fresh-batch-complete\tbooks={len(all_ids)}")


if __name__ == "__main__":
    main()
