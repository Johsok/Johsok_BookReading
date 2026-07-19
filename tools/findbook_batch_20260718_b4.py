from __future__ import annotations

import findbook_batch_20260716_b13 as batch


FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-18"
WORK_ID = "findbook-20260718-140422-b4"

CANDIDATES = {
    "01_business_startup": (
        ("矽谷創投啟示錄：一場由離經叛道的金融家所發起的瘋狂投資遊戲，如何徹底顛覆你我的生活、工作與娛樂方式", "塞巴斯蒂安‧馬拉比 曹嬿恆 林怡婷", "", "https://www.books.com.tw/products/0010931895"),
        ("頂尖操盤手的美股攻略大全：價值投資╳財報分析╳選股策略，全面解析獲利法則", "紐約居民", "", "https://www.books.com.tw/products/0010960524"),
        ("一本書讀懂匯率： 44個匯率關鍵概念，看懂全球經濟脈動，做對投資理財決策", "盧泳佑 趙慶燁 陳柏蓁", "", "https://www.books.com.tw/products/0011018756"),
        ("非理性效應：行為金融學家專家帶你洞悉人性本能，突破投資盲點", "丹尼爾．克羅斯比 陳重亨", "", "https://www.books.com.tw/products/0010994867"),
        ("通膨時代的投資思維：長銷20年股市經典!法人交易員揭露市場心理與超額報酬原則", "田渕直也", "", "https://www.books.com.tw/products/0011039123"),
        ("正念財務自由計畫：結合禪的智慧與財商素養，從記帳、呼吸到投資，7週輕鬆打造一輩子不為錢煩惱的致富心態", "7美元百萬富翁 呂佩憶", "", "https://www.books.com.tw/products/0011040097"),
        ("投資前最重要的事", "班‧卡爾森 陳儀", "", "https://www.books.com.tw/products/0010782802"),
        ("超級散戶的獲利模式：韓國股票投資大會冠軍的實戰交易法，短中長線都能賺!(二版)", "南錫官 蔡佩君", "", "https://www.books.com.tw/products/0011033554"),
        ("頂尖財務顧問的48堂財商素養課：收支X保險X投資，人生4階段富足全攻略", "洪哲茗 邱茂恒", "", "https://www.books.com.tw/products/0011006201"),
        ("美股投資大週期：從關稅、美債、升降息到AI浪潮，解讀川普2.0時代的致富訊號", "成尚泫 呂昀蔚", "", "https://www.books.com.tw/products/0011031178"),
        ("隱性財富：掌控市場變局的6大事件投資法", "艾席夫．蘇利亞 呂佩憶", "", "https://www.books.com.tw/products/0011013136"),
        ("法拍屋實戰寶典【暢銷萬冊紀念】：法拍教父黃正雄教你投資法拍賺千萬", "黃正雄", "", "https://www.books.com.tw/products/0011012660"),
        ("先鋒榮譽董事長談投資：精煉40年投資智慧，關於儲蓄、複利和人生的致富金律", "傑克‧布倫南 約翰‧沃斯 吳書榆", "", "https://www.books.com.tw/products/0010926129"),
        ("3天搞懂權證買賣(最新增訂版)：1000元就能投資，獲利最多15倍，存款簿多一個0!", "梁亦鴻", "", "https://www.books.com.tw/products/0010840408"),
        ("諸葛亮的買進投資日記：我用程式科學，躺賺存股、期貨、加密貨幣、ETF 的獲利公式!", "JH 諸葛亮", "", "https://www.books.com.tw/products/0011003278"),
        ("小資理財90秒【圖卡小劇場】：一看就懂的新手理財課，學會「儲蓄+保險+投資」，擺脫窮忙、存到第一桶金", "趙柏凱", "", "https://www.books.com.tw/products/0010947196"),
        ("【圖解】地表最簡單的利率教科書：想讀懂財經新聞、掌握經濟趨勢、投資理財不犯錯，你要先學會利率!", "角川總一 方瑜", "", "https://www.books.com.tw/products/0010983719"),
        ("元趨勢投資：找出未來狂漲十倍、百倍的潛力股", "中島聰 林佩瑾", "", "https://www.books.com.tw/products/0011037844"),
        ("技術分析大師的心理操盤術：拆解李佛摩、巴菲特等投資大師的常勝心法，避開買賣決策的情緒陷阱", "馬丁．普林 呂佩憶", "", "https://www.books.com.tw/products/0011031365"),
        ("護城河投資優勢：巴菲特獲利的唯一法則", "派特‧多爾西 黃嘉斌", "", "https://www.books.com.tw/products/0010735443"),
    ),
    "02_psychology_growth": (
        ("逆思維：華頓商學院最具影響力的教授，突破人生盲點的全局思考", "亞當．格蘭特 簡秀如", "", "https://www.books.com.tw/products/0010928118"),
        ("我，刀槍不入：從街頭魯蛇到海豹突擊隊，掌控心智、力抗萬難的奇蹟", "大衛・哥金斯 甘鎮隴", "", "https://www.books.com.tw/products/0010971366"),
        ("隱性潛能：華頓商學院最具影響力教授，突破天賦極限的實證科學【附潛能提升秘訣卡】", "亞當．格蘭特 洪慧芳", "", "https://www.books.com.tw/products/0010995694"),
        ("超速學習：我這樣做，一個月學會素描，一年學會四種語言，完成MIT四年課程", "史考特‧楊 林慈敏", "", "https://www.books.com.tw/products/0010855836"),
        ("打造你要的人生：歐普拉與哈佛教授談「更幸福」的藝術與科學", "亞瑟．布魯克斯 歐普拉．溫弗蕾 鍾玉玨", "", "https://www.books.com.tw/products/0010979654"),
        ("6分鐘日記的魔法：最簡單的書寫，改變你的一生【1書+1日記本】", "多明尼克．斯賓斯特 吳宜蓁", "", "https://www.books.com.tw/products/0010802202"),
        ("換框思維力：把OS轉成SO，不內耗不糾結，重啟人生只需改變視角", "賴婷婷", "", "https://www.books.com.tw/products/0011031674"),
        ("第二座山：當世俗成就不再滿足你，你要如何為生命找到意義?", "大衛．布魯克斯 廖建容", "", "https://www.books.com.tw/products/0010847488"),
        ("來談談那些痛苦的事吧!：商務人士的父親為孩子所寫下的「工作本質」!", "森岡毅 陳亦苓", "", "https://www.books.com.tw/products/0010857636"),
        ("與成功有約最後一堂課：柯維的向上心態", "史蒂芬．柯維 辛希雅．柯維．海勒 顧淑馨", "", "https://www.books.com.tw/products/0010949538"),
        ("生存的12條法則：當代最具影響力的公共知識分子，對混亂生活開出的解方", "喬登．彼得森 何雪綾 劉思潔", "", "https://www.books.com.tw/products/0010820641"),
        ("第3選擇：解決人生所有難題的關鍵思維", "史蒂芬．柯維 姜雪影 蘇偉信", "", "https://www.books.com.tw/products/0010955842"),
        ("越工作越自由：最大的探索，最豐盛的人生(全新探索版)", "Emily Liu", "", "https://www.books.com.tw/products/0010970886"),
        ("挫折逆轉勝：認知×行動×意志，32個聰明應對困境的心理技巧", "萊恩．霍利得 張斐喬", "", "https://www.books.com.tw/products/0010982466"),
        ("調校心態：舉起手，伸開5指，跟自己擊掌，做自己最強的啦啦隊!全球千萬網友實證的轉念習慣", "梅爾．羅賓斯 謝佳真", "", "https://www.books.com.tw/products/0010920162"),
        ("每天寫一張神可貼，九成願望都能實現!【博客來獨家限量贈夢想便利貼】", "坂下仁 林詠純", "", "https://www.books.com.tw/products/0011024725"),
        ("喚醒你心中的大師：偷學48位大師精進的藝術，做個厲害的人", "羅伯．葛林 謝佳真", "", "https://www.books.com.tw/products/0010756524"),
        ("起床後的黃金1小時：揭開64位成功人士培養高效率的祕密時光，從他們的創意晨型活動中，建立屬於自己的高生產力、高抗壓生活習慣", "班傑明．史鮑 麥可・桑德 郭庭瑄", "", "https://www.books.com.tw/products/0010825362"),
        ("成功的原則", "瑞‧達利歐 諶悠文", "", "https://www.books.com.tw/products/0010868559"),
        ("正確努力法：解鎖高效人生的100個關鍵", "野村礼雄 李婉寧", "", "https://www.books.com.tw/products/0011008038"),
    ),
    "03_natural_science": (
        ("爆笑科學王19：煮泡麵要先放麵?還是調味粉?", "辛泰勳 王宥丞 羅承暈", "", "https://www.books.com.tw/products/0011045551"),
        ("普通兄妹怪奇科學家4：我不要打針", "原著 普通兄妹、作者 安致賢 徐小為 柳蘭姬", "", "https://www.books.com.tw/products/0011055551"),
        ("普通兄妹怪奇科學家3：春眠不覺曉", "普通兄妹、安致賢 徐小為 柳蘭姬", "", "https://www.books.com.tw/products/0011046693"),
        ("科學破案王【套書全3冊】：聲音+力+光+電+熱，獨家頭條大公開!(懂點科學就是超級有用!)", "童未 垂垂", "", "https://www.books.com.tw/products/0011048016"),
        ("紅衣亞可：不讀會危險的科學常識書 1 日常生活中的危機!!!", "原著：紅衣亞可；作者：朴鍾恩 施孝臻 李鈴兒", "", "https://www.books.com.tw/products/0011047697"),
        ("普通兄妹怪奇科學家2：明天帶雨傘", "安致賢 普通兄妹 徐小為 柳蘭姬（유난희）", "", "https://www.books.com.tw/products/0011035473"),
        ("普通兄妹怪奇科學家1：味覺大驚奇", "安致賢 普通兄妹 徐小為 柳蘭姬（유난희）", "", "https://www.books.com.tw/products/0011028866"),
        ("酷哆啦的科學課：什麼是人工智慧", "叁川上 介于", "", "https://www.books.com.tw/products/0011048203"),
        ("爆笑科學王18：惡犬隱藏的真相", "辛泰勳 方佳琦 羅承暈", "", "https://www.books.com.tw/products/0011035324"),
        ("酷哆啦的科學課：人工智慧可以做什麼", "叁川上 介于", "", "https://www.books.com.tw/products/0011053346"),
    ),
    "04_healthcare": (
        ("激素平衡瘦身課(限量附贈【14天代謝調整課表】)：啟動代謝重建，瘦得健康持久", "許書華", "", "https://www.books.com.tw/products/0011052396"),
        ("看透醫學謊言，找到代謝真相：逆轉肥胖、高血壓、脂肪肝，讓身體健康長壽的自救指南", "羅伯特．勒夫金 丁亦", "", "https://www.books.com.tw/products/0011053334"),
        ("輕鬆當爸媽，孩子更健康【最新增修版】：超人氣小兒科醫師黃瑽寧教你安心育兒", "黃瑽寧", "", "https://www.books.com.tw/products/0011031212"),
        ("讀懂身體的訊號：基因醫師教你逆轉健康危機", "張家銘", "", "https://www.books.com.tw/products/0011036474"),
        ("科學實證有效的休息100招攻略：用最短時間快速提升專注力、恢復體力和身心健康", "加藤浩晃 陳欣如", "", "https://www.books.com.tw/products/0011050501"),
    ),
    "05_food_wellness": (
        ("1次煮5天便當：營養師親自設計健康又美味的料理", "阿杉(Osugi) 黃詩婷", "", "https://www.books.com.tw/products/0011048024"),
        ("肉の料理科學超圖解【暢銷修訂版】 ：大廚不外傳的雞豬牛羊306個部位烹調密技，從選對肉到出好菜一本搞定!", "朝日新聞出版 鄭睿芝", "", "https://www.books.com.tw/products/0011051573"),
        ("高代謝地中海日常菜：早午餐X便當菜X常備菜，「全球最佳飲食法」75道減醣低卡速簡料理", "謝長鴻（馬可）", "", "https://www.books.com.tw/products/0011024361"),
        ("貝姬的韓式瘦身微波爐食譜：狂瘦35公斤!100道低熱量、高蛋白、高膳食纖維料理", "貝姬（金炫京） 林季妤", "", "https://www.books.com.tw/products/0011050266"),
        ("今天煮什麼?：型男主廚吳秉承的百搭美味方程式，活用15種食材╳6種鍋具小家電，教你又快又省錢，搞定一桌超營養料理!", "吳秉承", "", "https://www.books.com.tw/products/0011028967"),
    ),
    "06_computer_info": (
        ("Python零基礎入門班(第五版)：一次打好程式設計、運算思維與邏輯訓練基本功", "鄧君如 總監製/文淵閣工作室 編著", "", "https://www.books.com.tw/products/0011052006"),
        ("快速精通iOS 26程式設計：從零開始活用Swift與SwiftUI開發技巧", "Simon Ng著 博碩文化 審校 王豪勳 譯", "", "https://www.books.com.tw/products/0011048623"),
        ("Python程式設計的樂趣|範例實作與專題研究的20堂程式設計課 第三版", "Eric Matthes H&C", "", "https://www.books.com.tw/products/0010957410"),
        ("邊玩邊學，使用Scratch學習AI程式設計 第二版", "石原淳也、倉本大資著、阿部和広監修 吳嘉芳", "", "https://www.books.com.tw/products/0011044438"),
        ("機器學習的基礎概論：Python程式設計我也可以成功做到(第1版)", "張任坊 張博一 張紹勳", "", "https://www.books.com.tw/products/0011052258"),
    ),
    "07_other": (
        ("喵的!歷史哪有那麼難(套書1-3)：(限量贈三國豪傑戰鬥閃卡)夏商周到魏晉南北朝", "白茶", "", "https://www.books.com.tw/products/0011037930"),
        ("歷史的瞬間：從宋遼金人物談到三寸金蓮", "陶晉生", "", "https://www.books.com.tw/products/0011051328"),
        ("OKINAWA沖繩二部曲(《砂之劍》+《魂魄 Mabui》，以沖繩視角反映日本二戰後歷史的非虛構漫畫代表作)", "比嘉慂 黃鴻硯", "", "https://www.books.com.tw/products/0011041303"),
        ("軸心文明與現代社會：探索大歷史的結構(平裝)", "金觀濤", "", "https://www.books.com.tw/products/0011052081"),
        ("條條大路：羅馬古道與羅馬之旅的歷史探索", "凱瑟琳．芙萊徹 韓翔中", "", "https://www.books.com.tw/products/0011041780"),
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
