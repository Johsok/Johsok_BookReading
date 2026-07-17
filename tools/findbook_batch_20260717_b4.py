from __future__ import annotations

import findbook_batch_20260717_b3 as previous


batch = previous.batch

FROM_DATE = "2026-06-18"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-140500-b4"


def sourced_rows(
    source_url: str,
    books: tuple[tuple[str, str], ...],
    source_date: str = "",
):
    return tuple((title, author, source_date, source_url) for title, author in books)


CANDIDATES = {
    category_id: tuple(candidates)
    for category_id, candidates in previous.CANDIDATES.items()
}

CANDIDATES["01_business_startup"] += sourced_rows(
    "https://www.books.com.tw/web/books_nbtopm_02",
    (
        ("駕馭機運的長贏思維：成功只是倖存者偏差？從健康、投資到事業，讓每一個風險變好運的決策指南", "史畢羅斯．馬克里達奇、羅賓．霍格思、阿尼爾．加巴"),
        ("如何讓AI幫你代筆寫出你想要的銷魂文案：教你正確下指令，讓企劃案、簡報、履歷、論文、寫作一秒完成！", "秋葉、劉進新、賈凝墨、萬靜"),
        ("直覺鍛鍊：腦科學家教你強化直覺判斷，打造高效率、低失誤的理想人生", "喬爾．皮爾森"),
        ("化解職場內傷：獻給在工作、生活、績效與人際壓力中疲憊掙扎的主管與上班族", "勅使川原真衣"),
        ("求職面試快易通：HR專家教你飛越雷區，展現優勢，理想工作不是夢", "孫裕盟"),
        ("獨角獸，炒作與泡沫：新科技熱門話題，是真商機還是假訊號？", "傑佛瑞．方克"),
        ("圖解邊畫邊解決的視覺化溝通術", "尼古拉．葛羅"),
        ("圖卡創意法則，觸發全方位創新思考", "張燕玲、郭蓋、范一葉"),
        ("知識變現！超效率閱讀", "丁玥"),
        ("不確定時代的投資關鍵", "丹尼爾．拉斯穆森"),
        ("秒懂行為經濟學", "阿部誠"),
        ("換框思維力", "賴婷婷"),
    ),
)

CANDIDATES["02_psychology_growth"] += sourced_rows(
    "https://www.books.com.tw/web/books_nbtopm_07",
    (
        ("每天早上起床，都被夢想照亮：改變內在的40堂正向晨間課", "李貞慧"),
        ("品味空虛：精神科北山醫師教你正視生活中的空白和情緒", "北山修"),
        ("不完美的我們：給努力過頭卻永遠都覺得不夠好的你", "尹葉瑟"),
        ("重塑潛意識，改寫人生腳本", "梯谷幸司"),
    ),
)

CANDIDATES["03_natural_science"] += (
    *sourced_rows(
        "https://findbook.com.tw/9786267507377",
        (
            ("小小觀察家的自然博物館：收藏自然界繽紛的形態與色彩，看見地球萬物的奧妙", "班．霍爾"),
        ),
        "2026-07-15",
    ),
    *sourced_rows(
        "https://www.sanmin.com.tw/product/index/015571482",
        (
            ("小學生的STEM科學研究室：工程篇", "克里斯．奧克斯雷德"),
        ),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ17-D900K79QF",
        (
            ("奈米機器人（未來已來系列）", "金成花、權秀珍"),
        ),
        "2026-07-03",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP0V-A900K62BZ",
        (
            ("起司的科學【最新修訂版】", "齋藤忠夫"),
        ),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBS3I-D900K797F",
        (
            ("口感科學：透視剖析食物質地，揭開舌尖美味的背後奧祕（特別收錄──50道無國界全方位料理）", "歐雷．莫西森、克拉夫斯．史帝貝克"),
        ),
        "2026-07-06",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP5I-A900K69O2",
        (
            ("莫非大冒險1：日常的魔咒（SEL社會情緒學習）", "嚴淑女"),
        ),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBP5L-A900K6G7K",
        (
            ("我的未來探索圖鑑：出發吧！從感興趣的事物，找到自己的方向", "宮野公樹"),
        ),
        "2026-07-01",
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJAH0H-A900K633N",
        (
            ("生生世世量子糾纏：從宇宙運轉科學探討量子世界", "許心華、謝昊霓"),
        ),
        "2026-07-02",
    ),
    *sourced_rows(
        "https://www.books.com.tw/web/books_nbtopm_06",
        (
            ("探索微觀星球，顯微鏡下的動物世界：外骨骼×翅與鱗×血管系統……透過顯微鏡觀察，建立動物身體結構與生理功能的整體認知", "吳成軍"),
        ),
    ),
)

CANDIDATES["04_healthcare"] += sourced_rows(
    "https://www.books.com.tw/web/books_nbtopm_08",
    (
        ("抗氧化物的奇蹟：常保年輕、健康與活力", "萊斯特．派克、卡羅．科曼"),
        ("50+人生問題解決對策", "横手彰太"),
        ("修復筋膜、強化穩定度MELT神經力量訓練全書", "蘇．希茲曼"),
        ("給大腦的13堂全方位照護課", "克萊拉・朵蘭"),
        ("胃癌術後營養照護全書", "林明燦、吳經閔、賴聖如"),
    ),
)

CANDIDATES["06_computer_info"] += (
    *sourced_rows(
        "https://www.books.com.tw/web/books_nbtopm_19",
        (
            ("邊玩邊學，使用Scratch學習AI程式設計 第二版", "石原淳也、倉本大資、阿部和広"),
        ),
    ),
    *sourced_rows(
        "https://24h.pchome.com.tw/books/prod/DJBQ2Q-D900K84CT",
        (
            ("全民版AI識讀：原理、應用、幻覺與誤區", "黃國珍"),
        ),
        "2026-07-16",
    ),
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
