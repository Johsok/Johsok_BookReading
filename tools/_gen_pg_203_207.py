# -*- coding: utf-8 -*-
"""Rewrite 150 book-specific highlights for 20260716-203..207."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
WRITER = TOOLS / "findbook_writer.py"
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORB = ("本書", "作者指出", "本章", "這一章")


def validate(book_id: str, highlights: list[str], title: str, author: str) -> None:
    """Raise ValueError if highlights violate findbook_writer rules."""
    if len(highlights) != 150:
        raise ValueError(f"{book_id} count={len(highlights)}")
    short_colon = []
    bodies = []
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not line.startswith(expected):
            raise ValueError(f"{book_id} bad number {index}")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} forbidden format {index}")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if len(body) < 12:
            raise ValueError(f"{book_id} too short {index}: {body}")
        if any(p in body for p in FORB):
            raise ValueError(f"{book_id} forbidden prefix {index}")
        if re.search(r"第\d+章", body):
            raise ValueError(f"{book_id} chapter wording {index}")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} step wording {index}")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short_colon.append(index)
        bodies.append(body)
    if len(short_colon) >= 3:
        raise ValueError(f"{book_id} short colon {short_colon}")
    if len(set(bodies)) != len(bodies):
        raise ValueError(f"{book_id} duplicate bodies")
    repeated = Counter(body[:18] for body in bodies if len(body) >= 18)
    if repeated and repeated.most_common(1)[0][1] >= 4:
        raise ValueError(f"{book_id} repeated starts {repeated.most_common(5)}")
    for label, value in (("title", title), ("author", author)):
        normalized = value.strip()
        if normalized and sum(normalized in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} repeats {label}")


def pack(points: list[str]) -> list[str]:
    """Number 150 highlight bodies."""
    if len(points) != 150:
        raise ValueError(f"need 150 got {len(points)}")
    return [f"{i:03d}、{text}" for i, text in enumerate(points, 1)]


def write_and_complete(book: dict) -> None:
    """Validate, write results JSON, and run findbook_writer complete."""
    highlights = pack(book["points"])
    validate(book["id"], highlights, book["title"], book["author"])
    out = TOOLS / f".findbook_results_grok_{book['id']}.json"
    out.write_text(
        json.dumps({"id": book["id"], "highlights": highlights}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(WRITER),
        "complete",
        "--category-id",
        "02_psychology_growth",
        "--results",
        str(out),
    ]
    subprocess.check_call(cmd, cwd=str(ROOT))


BOOKS = [
    {
        "id": "02_psychology_growth-20260716-203",
        "title": "格局",
        "author": "喬潔",
        "points": [
            "爭兩百元車資前先算這場吵會不會輸掉下季合作",
            "升遷被跳過先畫三年能力帳，不把今日面子當成終局",
            "會議搶功先補紀錄釘事實，當場撕破臉常把全局賠掉",
            "家族被比較年薪時，改問自己三年後要扛哪種責任",
            "部屬對外出事先擋責難，對內再拆流程，氣量用在護場",
            "客戶少下單先看產業週期，一季數字不夠給人格定罪",
            "讓利時記的是信任庫存，不是當下現金流出",
            "公開講我決策錯在哪，比找代罪者更能撐住團隊",
            "分紅少一塊就翻臉，等於告訴所有人你只看得見眼前",
            "對手贏了先學他多看了哪一層，酸言會把視野縮回井底",
            "加班爭功勞前先問這份成果三年後還值不值得署名",
            "被插隊先選要不要開口，選完就別把整晚拿去重播仇恨",
            "預算被砍先重排優先序，哭窮不能當策略",
            "朋友借錢先看關係與償還路徑，義氣不是無限額度",
            "新聞裡的名人翻車，先查制度漏洞，少拿來證明自己比較清高",
            "使命感應寫成可交付的一件事，例如本季帶一名新人獨立上線",
            "只為自己爭座位時，房間會愈坐愈小，改問誰還缺一把椅子",
            "擔當不是把錯全攬，是把可修的那截扛走並給期限",
            "活得大氣的檢驗是虧一次還能跟對方吃下一頓飯",
            "觀照全局先列出受影響的五類人，漏掉任何一類都是局部思維",
            "認知範圍窄時，先去站一天前線，再發表後勤評論",
            "層級要進階，先停止用昨天的成功解釋今天的例外",
            "為一時得失計較時，把時間軸拉到十二個月再重估火氣",
            "能成大事的人先把不可逆後果標紅，可逆的小虧允許試",
            "放開胸懷不是沒底線，是底線以外的閒氣不收集",
            "來到世上不能只為自己，本週做一件不署名的補位",
            "思維決定出路時，先寫出你正在用的假設，假設錯了路就錯",
            "進階級別看你肯不肯把功勞分出去仍把責任留在自己桌上",
            "產業領袖的裂變往往從少計較一筆小帳開始，不是從口號開始",
            "有使命的人開會先問這決策對十年後的組織還站不站得住",
            "不同人看見的範圍不同，先請基層用三句話描述同一事件",
            "覺得自己委屈時，把對手的限制條件也寫上，畫面才完整",
            "被當眾否定先穩呼吸，再決定要澄清事實還是護住合作",
            "資源分配表就是優先序，口頭說重視人才卻砍培訓就拆穿了",
            "合作先找共同利益帶，純輸贏會把棋盤下到死局",
            "寬容要配界線，否則氣量會被讀成可欺",
            "重大決策同時寫個人、團隊、社會三欄後果再簽字",
            "面對批評先把有效資訊與人身攻擊分成兩欄，只回第一欄",
            "過往成功最容易變成盲點，每季問一句哪條舊經驗已過期",
            "尊重小事與基層經驗，高處視角才有校正點",
            "成就分享與利益回饋要定期發生，一次宴請換不來長久信任",
            "守信看的是準時交付與一致標準，不是年會上的感性演講",
            "情緒容量不夠時先睡飽再做判斷，飢餓的人最容易變小氣"
            "真正的自信容得下不同意見，會議留兩分鐘給最安靜的人",
            "理解他人位置不等於放棄原則，原則寫成不可讓的三條",
            "長期視角能降低短期綁架，投資與做人同一套時間尺",
            "局部事件背後常有系統，客訴先查流程再查個人態度",
            "影響力來自修補而不是追兇，修補要有日期與驗收",
            "把一年後的自己當成第三者，問他今天這場爭執還重不重要",
            "團隊出錯時公開扛、私下教，順序反了會讓人只學會甩鍋",
            "看見別人走捷徑先問代價落在誰身上，再決定要不要學",
            "小氣的人把所有關係都做成即時結算，大氣的人允許延遲平衡",
            "被比較時改比貢獻半徑，不比頭銜字數",
            "拒絕一件事時說明你在保護哪一個更大的承諾",
            "接受一件虧時說明你在投資哪一段關係，虧要有名字",
            "對敵手保持好奇，恨意會把資訊通道關掉",
            "決策前問這選擇會不會讓自己變得更狹窄",
            "把掌聲當警報，掌聲最大處往往是認知最滿、最該補課的地方",
            "幫助對手完成他的目標，有時比擊敗他更能擴大盤面",
            "家族企業爭權時先寫共同生存條件，再談誰當家",
            "社群上被酸先停二十四小時，鍵盤氣量幾乎都偏小",
            "升官後第一週去最被忽略的崗位坐半天，視野才接得上地氣",
            "談判留下讓對方面子的句子，贏盡當下常輸掉下一次進門",
            "把不可逆的傷害從可逆的摩擦裡分開，只有前者值得動用全部怒氣",
            "成功後主動讓出舞台一角，層級才不會停在個人英雄",
            "失敗後先保護學習資料，不要連同自尊一起燒毀",
            "聽到風向變了先重繪地圖，用地圖辯論不如用新偵察",
            "錢不夠時先保信任與關鍵人才，砍展示型開支",
            "時間不夠時先保不可逆的窗口，例如證照與季節性訂單",
            "面子夠用就好，把多餘面子兌換成可檢驗的成果",
            "別人誇你氣量大時，回一句我這季實際讓出了哪塊利益"
            "遇到制度不公先連署可改的條款，抱怨若無提案就只是排氣",
            "對新人解釋規則時連同例外一起講，小氣的組織最喜歡藏規則",
            "自己得利的方案要主動揭露利益，隱瞞會把胸襟寫成投機",
            "跨部門衝突用共同客戶當裁判，不用職級當武器",
            "把仇恨做成燃料前先問這燃料會不會燒到自己的未來同盟",
            "看見不公平先問自己有無權限改，有就改、沒有就記錄並上報",
            "退休規劃若只算自己，照顧鏈一斷就露出狹窄",
            "捐助選可追蹤的項目，善心也要經得起全局檢視",
            "演講少講我多講我們欠誰，聽眾才聽得出層次",
            "被挖角時比較的是責任半徑，不只是薪資跳級",
            "對媒體回應先核對會不會傷害沉默的第三人",
            "內部競爭設公開規則，陰招會把整個組織的氣量往下拉",
            "把年度目標寫成對誰有益，寫不出對象就只是自我膨脹",
            "承認未知比裝懂更能打開下一步，裝懂是最小的那種自負",
            "請教對手一句你怎麼看這風險，比再寫十頁自衛稿有用",
            "會議結束問誰被這決定傷到，傷到的人要有補償路徑",
            "把歷史恩怨寫在紙上再折起來，討論只准用本季事實",
            "看見短線暴利先問誰在為你的速度付代價",
            "培養接班人等於把事業從個人命運升級成系統",
            "對批評者邀請他指出一個可改的點，關閉大門才是真的小",
            "自己的舒適若建立在別人長期加班，那舒適就是狹窄的證據",
            "旅行時去看與自己無關的行業，認知範圍才會被硬拉開",
            "讀書選會讓你不舒服的作者，舒服的書通常只在原井裡打轉",
            "交朋友跨出同溫層一位，年度只加一位也算擴張",
            "處理遺產先寫共同記憶與照顧義務，再談坪數",
            "政治話題在飯桌上先約定不升級人身攻擊，人身一出盤面就碎",
            "發現自己在蒐集別人的把柄，立刻停手，把柄思維會把人做小",
            "獎勵說真話的人，即使話難聽，氣量要有制度承載",
            "把勝利定義成局面變好，而不是對手看起來更慘",
            "遇到兩難用十年尺，十年後仍痛的才是真問題",
            "對自己的嫉妒點名，嫉妒常指出你不肯承認的缺口",
            "公開場合把功勞還給實際做事的人，私德會變成組織文化",
            "犯錯罰款自己出，別用部門預算替個人面子買單",
            "聽到我們一向都這樣，把一向拿出來曬太陽，慣例最會縮小思考",
            "新市場先派自己去住一週，遙控評論最容易變井蛙",
            "危機公關先保護受害者，再保護品牌，順序反了就是小算盤",
            "股價波動時對員工講現金跑道，對股東講假設，兩套謊言最傷層級",
            "把競爭對手的優點寫進內部教材，忌妒就無法佔領黑板",
            "年終只獎個人英雄，隔年就沒人願意補位，獎項也在塑造氣量",
            "請假制度要讓照顧者活得下去，否則組織只獎勵無負擔的人",
            "對外承諾前先問最弱的供應商做不做得到，全局含供應鏈",
            "自己的孩子犯錯，先當公民再當父母，私心會把公共判斷做歪",
            "看到弱勢被嘲，當場把話題轉回事情本身，沉默也是一種站隊",
            "權力變大時把決策權下放到能看見現場的人，集權常是恐懼",
            "寫遺囑或授權書等於承認自己不是宇宙中心，這是成熟的尺度",
            "對前東家保持敬意，把人做絕會讓下一個圈子提前關門",
            "投資失敗先分清是機率、是貪婪、還是資訊不足，三種教訓不同",
            "把每天的抱怨改寫成一條可提案的改進，排氣要升級成工程",
            "宴會上把話題讓給新來的人，主持場面也是一種層級",
            "發現自己在用道德高地壓人，立刻改成具體請求，高地最狹窄",
            "對科學未知保持謙虛，確定口吻用在可驗證處",
            "城市規劃式思考，問十年後的擁擠會落在誰家門口",
            "自己得勢時留下反對者的座位，將來你也需要那張椅子",
            "把國家、公司、家庭的利益衝突寫清楚，混為一談會做出糊決策",
            "慈善活動若要拍照才肯做，先把鏡頭拿掉再決定還做不做",
            "對清潔人員道謝並記住名字，層級從對待無權者的方式開始量",
            "被誤會時先澄清事實，不必要求對方瞬間喜歡你",
            "把敵人這個詞從工作郵件刪掉，改成競爭條件，語言會塑形胸襟",
            "年度回顧問我讓誰變得更有能力，而不是我贏了幾場",
            "面對世代差異先請對方示範他的工具，少用我們那年代壓人",
            "國際合作先學對方的禁忌與節日，無知會被讀成傲慢",
            "把機密與閒話分開，傳閒話的人看似熱鬧，其實在縮小信用圈",
            "自己的藝術品味不必當別人的功課，審美獨裁也是一種小",
            "遇到歷史爭議先讀兩種史觀，再決定要不要發言",
            "公司裁員時親自面談被影響的人，數字背後要有臉",
            "把成功歸因寫成運氣加系統加團隊，單寫我努力會把人做小",
            "對身體邊界說不，保護自己才能長期承擔更大的事",
            "看見短影音審判，先查來源與時間線，再決定要不要轉發",
            "把遺產稅、照顧班表、備用金寫進家庭會議，親情也需要全局表",
            "對自己的特權列清單，列得出來才有機會主動讓出一部分",
            "最後用一件不求回報的事結束本週，練習不只為自己活",
            "胸襟要靠重複的讓利與護場來長，不是靠一句我很大器",
            "簽約前把最壞情況寫給對方看，藏條款只是最小的精明",
            "對退休同事保持請教，不讀舊地圖會把學費再繳一次",
            "發現自己在記仇名單加名字，改成只記一條可談判條件",
            "社區會議先聽最受影響的住戶，再談美觀與房價",
            "年度旅費撥一部分去陌生城市住三天，認知範圍要出門買",
            "標案落敗去問評審缺哪一層資訊，不問就只剩下怨氣",
            "家庭爭執停在事情本身，不把對方父母一併拖進戰場",
            "看見公共資源被拿去圖私，先留下紀錄再決定要不要舉報",
            "自己的日程每週留一格給不產生個人績效的公共事",
        ],
    },
]


def main() -> int:
    """Write books in order; pass start index via argv."""
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start + 1
    for book in BOOKS[start:end]:
        write_and_complete(book)
        print(f"done\t{book['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

