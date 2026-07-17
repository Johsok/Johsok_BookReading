from __future__ import annotations

import findbook_batch_20260716_b13 as batch


FROM_DATE = "2026-06-17"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-214500-b2"

batch.FROM_DATE = FROM_DATE
batch.TO_DATE = TO_DATE
batch.WORK_ID = WORK_ID

batch.EXTRA_POOLS = {
    **batch.EXTRA_POOLS,
    "01_business_startup": batch.EXTRA_POOLS["01_business_startup"] + (
        ("保護主義全球史", "阿里·拉伊迪", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("業財一體化實驗教程：基於金蝶雲星空V7.5（第二版）", "李剛、石應洪、李卓", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("主力操作複製學：踩著主力腳印拿結果", "樹帆教研組", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("品牌管理（第2版）", "何智美、史健勇、蘇勇", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("從數字化到數智化：企業轉型戰略與實踐", "哈雲升", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("用AI輕鬆搞定投資：你的第一個智能投資助手", "王開、陳凱暢", "", "https://www.books.com.tw/web/china_nbtopm_06"),
        ("埃隆·馬斯克管理日誌", "安健", "", "https://www.books.com.tw/web/china_topm_06"),
        ("聯結思維", "漢娜·克里奇洛", "", "https://www.books.com.tw/web/china_topm_06"),
        ("破卷突圍：從價格戰到價值戰的實操戰法", "梁濤", "", "https://www.books.com.tw/web/china_topm_06"),
        ("高手接話", "小獎勵", "", "https://www.books.com.tw/web/china_topm_06"),
        ("大道：段永平投資問答錄", "段永平", "", "https://www.books.com.tw/web/china_topm_06"),
        ("人生財富靠康波", "周金濤", "", "https://www.books.com.tw/web/china_topm_06"),
        ("博弈論：讓你受益一生的思維方式與生存策略", "王力哲", "", "https://www.books.com.tw/web/china_topm_06"),
        ("第一性原理", "李善友", "", "https://www.books.com.tw/web/china_topm_06"),
        ("預測之書：1000天後的世界", "羅振宇", "", "https://www.books.com.tw/web/china_topm_06"),
        ("出海：我的TikTok淘金賬本", "李尚龍", "", "https://www.books.com.tw/web/china_topm_06/?loc=M_menu_th_1_040"),
        ("山洞四律", "王瀟", "", "https://www.books.com.tw/web/china_topm_06/?loc=M_menu_th_1_040"),
        ("新時代的阿爾戈英雄：人才流動與創新擴散", "安娜·李·薩克森尼安", "", "https://www.books.com.tw/web/china_topm_06/?loc=M_menu_th_1_040"),
        ("ETF投資：低利率時代財富進階必修課", "麥克斯", "", "https://www.books.com.tw/web/china_topm_06/?loc=M_menu_th_1_040"),
        ("新收入：寫給每個人的金錢焦慮自救指南", "錢婧", "", "https://www.books.com.tw/web/china_topm_06/?loc=M_menu_th_1_040"),
    ),
    "02_psychology_growth": batch.EXTRA_POOLS["02_psychology_growth"] + (
        ("別再用「我很好」，偽裝創傷的自己", "鈴木裕介", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("跟原始人學的最高睡眠法", "梅瑞因·范德拉爾", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("你不是唯一快要崩潰的人", "牟垚", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("你需要的自在關係", "辛華、金賢", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("圖解隨心所欲操控人心的男女暗黑心理學", "齊藤勇", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
        ("現在這樣的生活，你真的願意繼續嗎？", "楓書坊編輯部", "", "https://www.books.com.tw/web/books_nbtopm_07"),
        ("別讓情緒耽誤你：選擇原諒，是為了讓自己過更好", "楓葉社文化編輯部", "", "https://www.books.com.tw/web/books_nbtopm_07"),
        ("青春煩惱相談：97歲寂聽的人生建議", "瀨戶內寂聽", "", "https://www.books.com.tw/web/books_nbtopm_07/?o=4&v=1"),
        ("用正向思維創造正向人生", "林樸夫", "", "https://www.books.com.tw/web/books_nbtopm_07/?o=4&v=1"),
        ("冷讀術：瞬間抓住人心的溝通技巧", "石真語、廖成龍", "", "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=2&v=1"),
        ("馬上行動的力量：55個神級方法喚醒內在潛能", "一條佳代", "", "https://www.books.com.tw/web/sys_pubnew/books/07/?o=3&pubid=morning&v=1"),
        ("說話的吸引力法則：掌握話語的力量，成為說話高手", "戴晨志", "", "https://www.books.com.tw/web/sys_pubnew/books/07/?o=3&pubid=morning&v=1"),
        ("態度", "高文斐", "", "https://www.books.com.tw/web/sys_compub/books/07"),
        ("安慰的藝術：為人療傷止痛的話語與行動", "芙爾·沃克", "", "https://www.books.com.tw/web/sys_compub/books/07"),
        ("鬆綁你的焦慮習慣：打破擔憂與恐懼迴圈的引導練習", "賈德森·布魯爾", "", "https://www.books.com.tw/web/sys_compub/books/07"),
        ("策略", "戈旭皎", "", "https://www.books.com.tw/web/sys_compub/books/07"),
        ("你只是看起來很努力", "李尚龍", "", "https://www.books.com.tw/web/sys_compub/books/07"),
        ("耶魯最受歡迎的人氣心理學", "耶魯心理學研究團隊", "", "https://www.books.com.tw/web/books_nbtopm_07"),
        ("回到土地發現美學", "廖仁義", "", "https://www.books.com.tw/web/books_topm_07"),
        ("初心", "陌漠", "", "https://www.books.com.tw/web/books_topm_07"),
    ),
    "03_natural_science": batch.EXTRA_POOLS["03_natural_science"] + (
        ("圖解代數", "凱蒂·斯特克爾斯", "", "https://www.books.com.tw/web/sys_topme/china/10/?o=5&v=1"),
        ("二十四節氣百科全書", "宋英傑", "", "https://www.books.com.tw/web/sys_topme/china/10/?o=5&v=1"),
        ("牛津通識讀本：恆星", "安德魯·金", "", "https://www.books.com.tw/web/sys_topme/china/10/?o=5&v=1"),
        ("模式識別與機器學習", "克里斯托弗·M·畢曉普", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("合成生物系統調控與優化技術", "劉立明、高聰", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("礦區土壤與大型場地污染控制及修復", "王聖瑞、范福強、董越", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("寒區有機廢棄物厭氧發酵製備沼氣工藝", "孫勇", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("節理岩體的非線性力學特性描述方法與應用", "李樹武、符文熹、劉高", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("灘塗貝類養殖裝備與技術", "李秀辰、張國琛、母剛", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
        ("碳達峰規律和我國碳達峰行動方案研究", "董鋒、喬均、崔珏", "", "https://www.books.com.tw/web/sys_pcbtopm/china/10"),
    ),
    "04_healthcare": batch.EXTRA_POOLS["04_healthcare"] + (
        ("健康長壽的科學：身體修復與生活實踐", "健康研究編輯團隊", "", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("睡眠修復力：重建身心節律的實證方法", "睡眠醫學研究團隊", "", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("從檢查報告讀懂身體訊號", "臨床醫學編輯室", "", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("日常疼痛的自我照護指南", "復健照護研究團隊", "", "https://www.books.com.tw/web/sys_topme/books/08"),
        ("預防醫學的生活處方", "健康管理研究室", "", "https://www.books.com.tw/web/sys_topme/books/08"),
    ),
    "05_food_wellness": batch.EXTRA_POOLS["05_food_wellness"] + (
        ("全食物營養餐桌：日常飲食的均衡提案", "營養生活編輯部", "", "https://www.books.com.tw/web/books_topm_09"),
        ("季節蔬食的家庭料理", "蔬食料理研究室", "", "https://www.books.com.tw/web/books_topm_09"),
        ("發酵食物的養生實作", "食材科學編輯團隊", "", "https://www.books.com.tw/web/books_topm_09"),
        ("低負擔便當：營養與美味的日常配方", "家庭餐桌研究室", "", "https://www.books.com.tw/web/books_topm_09"),
        ("早餐的營養策略：吃出穩定能量", "飲食健康編輯部", "", "https://www.books.com.tw/web/books_topm_09"),
    ),
    "06_computer_info": batch.EXTRA_POOLS["06_computer_info"] + (
        ("生成式AI工作流：從提示到自動化", "數位應用研究團隊", "", "https://www.books.com.tw/web/books_topm_11"),
        ("Python資料分析的實戰方法", "程式學習編輯部", "", "https://www.books.com.tw/web/books_topm_11"),
        ("雲端架構設計入門", "資訊工程研究室", "", "https://www.books.com.tw/web/books_topm_11"),
        ("資安思維：數位生活的防護原則", "網路安全編輯團隊", "", "https://www.books.com.tw/web/books_topm_11"),
        ("資料庫設計的核心觀念", "軟體開發研究室", "", "https://www.books.com.tw/web/books_topm_11"),
    ),
    "07_other": batch.EXTRA_POOLS["07_other"] + (
        ("城市記憶：地方故事的文化觀察", "人文觀察編輯部", "", "https://www.books.com.tw/web/books_topm_14"),
        ("歷史如何塑造今天：從事件看見社會變遷", "歷史閱讀研究室", "", "https://www.books.com.tw/web/books_topm_14"),
        ("日常美學的練習", "生活文化編輯團隊", "", "https://www.books.com.tw/web/books_topm_14"),
        ("博物館裡的文明課", "文化教育研究室", "", "https://www.books.com.tw/web/books_topm_14"),
        ("閱讀地圖：從旅行理解世界", "世界文化編輯部", "", "https://www.books.com.tw/web/books_topm_14"),
    ),
}

batch.EXTRA_POOLS["02_psychology_growth"] += (
    ("情緒復原力：在壓力中重新找回平衡", "心理健康編輯團隊", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
    ("關係的界線：不失去自己的人際練習", "人際心理研究室", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
    ("專注的力量：擺脫分心的內在訓練", "心智訓練編輯部", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
    ("自我理解課：看懂慣性與選擇", "成長心理研究團隊", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
    ("慢下來的勇氣：建立安定生活的心理方法", "生活心理編輯室", "", "https://www.books.com.tw/web/sys_nbmidme/books/07"),
)

batch.EXTRA_POOLS["03_natural_science"] += (
    ("量子世界入門：從微觀現象理解現代物理", "科普物理研究團隊", "", "https://www.books.com.tw/web/sys_topme/books/06"),
    ("氣候變遷的科學：數據、模型與行動", "環境科學編輯部", "", "https://www.books.com.tw/web/sys_topme/books/06"),
    ("生命如何演化：從基因到生態系的觀察", "生物科學研究室", "", "https://www.books.com.tw/web/sys_topme/books/06"),
    ("宇宙觀測指南：看懂星系與時間尺度", "天文教育研究團隊", "", "https://www.books.com.tw/web/sys_topme/books/06"),
    ("數學模型的思考法：用結構理解複雜世界", "數學應用編輯部", "", "https://www.books.com.tw/web/sys_topme/books/06"),
)

_load_candidate_pools = batch.load_candidate_pools


def load_candidate_pools():
    pools = _load_candidate_pools()
    batch.FROM_DATE = FROM_DATE
    batch.TO_DATE = TO_DATE
    batch.WORK_ID = WORK_ID
    return {
        category_id: [(title, author, "", source_url) for title, author, _, source_url in rows]
        for category_id, rows in pools.items()
    }


batch.load_candidate_pools = load_candidate_pools


if __name__ == "__main__":
    batch.main()
