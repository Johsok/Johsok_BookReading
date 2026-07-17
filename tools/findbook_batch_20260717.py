from __future__ import annotations

import findbook_batch_20260716_b13 as batch


TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-212000"

batch.TO_DATE = TO_DATE
batch.WORK_ID = WORK_ID

batch.EXTRA_POOLS = {
    **batch.EXTRA_POOLS,
    "01_business_startup": batch.EXTRA_POOLS["01_business_startup"] + (
        ("公司理財（第6版）（上下冊）", "喬納森·伯克、彼得·德馬佐", "2025-10-01", "https://www.books.com.tw/products/CN17912402"),
        ("公司金融", "方芳、王欣陽", "2025-04-01", "https://www.books.com.tw/products/CN17874639"),
        ("銀行經營邏輯", "歐陽衛民", "2025-03-01", "https://www.books.com.tw/products/CN17885640"),
        ("AI賦能財務：寫給CFO的AI使用手冊", "武魁", "2025-09-29", "https://www.books.com.tw/products/CN17899357"),
        ("錢經：商聖范蠡的財富智慧", "孔方", "2025-01-01", "https://www.books.com.tw/products/CN17906053"),
        ("銀行簡史", "理查德·希爾德雷思", "2025-01-01", "https://www.books.com.tw/products/CN13597261"),
        ("通往幸福的理財課", "肖剛", "2025-03-01", "https://www.books.com.tw/products/CN13967337"),
        ("財報掘金（第2版）", "張新民", "2025-02-01", "https://www.books.com.tw/products/CN14161428"),
        ("把脈：全球巨變與中國經濟", "高柏", "2025-06-01", "https://www.books.com.tw/products/CN17901149"),
        ("證券市場分析（第3版）（微課版）", "張本照", "2025-04-01", "https://www.books.com.tw/products/CN17865439"),
        ("出乎意料的經濟學", "蒂莫西·泰勒", "2025-06-01", "https://www.books.com.tw/products/CN17868923"),
        ("金融的智慧", "米希爾·德賽", "2025-06-01", "https://www.books.com.tw/products/CN17853637"),
        ("創業金融學", "顧婧、周偉", "2025-09-01", "https://www.books.com.tw/products/CN17933816"),
        ("中小企業財務：從系統思維到管理升級", "楊金芳、鄒函宸、楊燕芳", "2025-08-01", "https://www.books.com.tw/products/CN17889980"),
        ("金錢的藝術", "摩根·豪澤爾", "2025-10-01", "https://www.books.com.tw/products/CN17903312"),
        ("數理金融學", "馬克·H.A.戴維斯", "2025-07-01", "https://www.books.com.tw/products/CN17891572"),
        ("金融科技力2025年版", "台灣金融研訓院編輯委員會", "2025-08-01", "https://www.books.com.tw/web/sys_bbotm/books/020808/?f=N&o=1&v=2"),
        ("企業經營模式創新理論與個案", "薄榮薇、顧志遠", "2025-09-25", "https://www.books.com.tw/web/books_bmidm_0202"),
        ("財富掠奪者：私募股權投資基金如何欺詐全球市井小民的錢", "約書亞‧羅斯納、葛雷琴‧摩根森", "2025-09-02", "https://www.books.com.tw/web/books_bmidm_0208"),
        ("負債資本論，用「債權思維」驅動資產成長：全球視野下的財務槓桿與現金流管理", "遠略智庫", "2025-07-09", "https://www.books.com.tw/web/sys_bbotm/books/020902"),
    ),
    "02_psychology_growth": batch.EXTRA_POOLS["02_psychology_growth"] + (
        ("榮格心理學入門：自我重生的人生旅程", "山根久美子", "2025-02-05", "https://www.books.com.tw/products/0011011968"),
        ("文心化智：傳統文化與心理科學的交融碰撞", "王軼楠", "2025-10-01", "https://www.books.com.tw/products/CN17996132"),
        ("正在成為大人的我們，就算迷惘也沒關係：關於成長路上的每一個難題，心理學給你的21個解答", "潔瑪•史貝格", "2025-08-09", "https://www.books.com.tw/products/0011028325"),
        ("心理韌性：重建挫折復原力的132個強效練習大全", "琳達．格拉翰", "2025-11-19", "https://www.books.com.tw/products/0011037178"),
    ),
    "03_natural_science": batch.EXTRA_POOLS["03_natural_science"] + (
        ("DK生物學百科", "DK出版社", "2025-10-01", "https://www.books.com.tw/products/CN17910925"),
        ("大衛·麥考利科普繪本·這不簡單呀！（全3冊）", "大衛·麥考利", "2025-05-01", "https://www.books.com.tw/products/CN17868064"),
        ("一直在場：為何科學界不能沒有女性", "雅典娜·唐納德", "2025-11-01", "https://www.books.com.tw/web/sys_natopm/china/10/?cus_id=3078&loc=P_0001_010"),
        ("白話微積分(5版)", "卓永鴻", "2025-07-25", "https://www.books.com.tw/web/sys_topme/books/06/?o=5&v=1"),
        ("數學分析圖鑑：圖解x實例，從微積分到向量分析，一本搞定！", "藏本貴文", "2025-09-03", "https://www.books.com.tw/web/sys_topme/books/06/?o=5&v=1"),
    ),
    "05_food_wellness": batch.EXTRA_POOLS["05_food_wellness"] + (
        ("史上最強1000種全食物營養完整圖鑑：探索110種食材，1000個OK和NG組合，全營養聖經！", "康鑑文化編輯部", "2025-10-01", "https://www.books.com.tw/products/0011033604"),
        ("傳家健康菜：潘懷宗博士的三代養生食譜＋長壽要訣，讓你健康多活40年", "潘懷宗、游謦榕", "2020-02-18", "https://www.books.com.tw/products/0010848851"),
        ("自製養生豆漿大全（全新修訂版）", "李寧", "2019-11-01", "https://www.books.com.tw/products/0010838103"),
        ("養生粥膳：會說話的食譜書", "陳志田", "2015-09-09", "https://www.books.com.tw/products/0010688956"),
    ),
}

_load_candidate_pools = batch.load_candidate_pools


def load_candidate_pools():
    pools = _load_candidate_pools()
    batch.TO_DATE = TO_DATE
    batch.WORK_ID = WORK_ID
    return pools


batch.load_candidate_pools = load_candidate_pools


if __name__ == "__main__":
    batch.main()
