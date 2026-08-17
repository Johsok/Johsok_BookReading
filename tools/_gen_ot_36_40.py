# -*- coding: utf-8 -*-
"""Rewrite 150 highlights for 07_other-20260716-36..40, one book at a time."""
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
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from _pts_37 import POINTS as POINTS_37  # noqa: E402
from _pts_38 import POINTS as POINTS_38  # noqa: E402
from _pts_39 import POINTS as POINTS_39  # noqa: E402
from _pts_40 import POINTS as POINTS_40  # noqa: E402
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
        if "\n" in line or "\r" in line or "｜" in line or "*" in line or "`" in line:
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
        raise ValueError(f"{book_id} repeated starts {repeated.most_common(8)}")
    for label, value in (("title", title), ("author", author)):
        normalized = value.strip()
        if normalized and sum(normalized in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} repeats {label}")
    shortish = [i for i, b in enumerate(bodies, 1) if len(b) < 25]
    longish = [i for i, b in enumerate(bodies, 1) if len(b) > 52]
    if shortish:
        print(f"warn short {book_id} {shortish[:8]} n={len(shortish)}")
    if longish:
        print(f"warn long {book_id} {longish[:8]} n={len(longish)}")


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
        json.dumps({"id": book["id"], "highlights": highlights}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(WRITER),
        "complete",
        "--category-id",
        "07_other",
        "--results",
        str(out),
    ]
    subprocess.check_call(cmd, cwd=str(ROOT))


BOOKS = [
    {
        "id": "07_other-20260716-36",
        "title": "臺灣史：臺灣共產黨",
        "author": "戚嘉林",
        "points": [
            "日治左翼不是外來標籤，而是糖廠工時、佃租與臨檢堆出的組織實驗",
            "共產國際把殖民地寫進世界時間表，臺灣被看成日本帝國的海外弱點",
            "上海法租界的創黨會議，說明島內革命儀式常在帝國縫隙完成",
            "林木順出任首任書記，早期領導多從留日與上海網絡抽調",
            "建黨文獻同時寫反日帝、土地革命與民族獨立，三線日後互相拉扯",
            "獨立訴求指向臺灣共和國式蘇維埃，不宜直接套戰後政黨語彙",
            "謝雪紅以女工與農運經驗進入核心，人事檔不該只剩男性姓名",
            "翁澤生長駐上海莫斯科窗口，把島內報告改寫成國際可讀敘事",
            "林日高負責島內聯絡，合法身分與地下任務重疊而被檔案放大",
            "潘欽信參與路線草稿，後來在檢舉潮中變成內部檢討的箭靶",
            "蔡孝乾走過文協、台共到戰後中共系統，履歷本身就是史觀戰場",
            "莊春火屬創黨成員，供述讓組織圖譜被殖民警察重新繪製",
            "洪朝宗早逝與退出提醒，小黨核心極易被逮捕與疾病雙重掏空",
            "蘇新從文化青年轉入左翼出版，文字工作在非法狀態等於暴露地址",
            "楊克煌長期同行謝雪紅，回憶與檔案之間常見自我辯護縫隙",
            "文化協會先走講習報刊的合法啟蒙，左右分裂才把部分人推向地下",
            "連溫卿代表文協左派，主張階級路線卻未必等於擁有台共黨籍",
            "蔣渭水偏民族與社會民主，和共產國際階段論不是同一張地圖",
            "民眾黨嘗試議會請願與合法組黨，被總督府當成可監視的公開容器",
            "農民組合把二林竹林爭議做成佃農網絡，簡吉成為農運符號",
            "糖業資本主義把土地與工時量化，宣傳才找得到具體仇敵",
            "機械工會與印刷工人提供城市據點，工廠紀律也被拿去練習密會",
            "留日學生在東京接觸日共週邊，返臺後成為翻譯理論的中間人",
            "民族支部體制迫使台共向日共報告，島內緊急仍要等東京回文",
            "中共提供訓練與刊物管道，一九二八年法理上級仍是日共系統",
            "土地口號碰到漢人業主結構，原住民土地問題並未被同一化",
            "反封建與反殖民綁在一起，民族資本家既是統戰對象又是鬥爭目標",
            "婦女部與讀書會吸收女工，性別壓迫寫進階級敘事卻常被邊緣",
            "青年部用夜學同鄉會掩護，學校宿舍成為警察重點巡邏區",
            "油印傳單發行量其實很小，卻足以構成治安罪名與搜索令",
            "口號可簡成打倒總督府，細節爭論卻卡在土地、民族與階段",
            "創黨當年秋季即有成員落網，成立與破獲幾乎前後腳",
            "特高警察專責思想案件，常把出席名單做成叛亂證據鏈",
            "保甲連坐讓鄰里監視比密探便宜，農村支部特別容易被舉報",
            "巡查常以違警與治安維持法辦案，不必等到公開衝突才出手",
            "一九三一年大檢舉幾乎端掉中央，台共作為組織實體實質瓦解",
            "改組會議被起訴書寫成陰謀高峰，現場其實是路線辯論",
            "轉向政策誘導公開悔過，獄中聲明成為再動員的對照文本",
            "刑求痕跡寫在判決與回憶之間，史家要交叉而非只信單方",
            "獄中互相指控，失敗常被解釋成奸細，而不是情報不對稱",
            "密探滲入農組與讀書會，信任在地下狀態裡變成致命弱點",
            "日共國內同步遭大檢舉，上級一斷民族支部立刻失去補給",
            "第三期極左要求暴露鬥爭，使原本就薄的組織更易被點名",
            "人民陣線尚未在島內落地，台共已先在檢舉潮中被掏空",
            "民族獨立條款被中共史觀後來改寫成中國革命邊區支線",
            "國民黨敘事把台共寫成亂黨，省略總督府社會立法失敗脈絡",
            "戰後獨立論述有時回收民族口號，卻抽掉當時的土地革命核心",
            "三套史觀並列閱讀，看誰被刪掉：女工、佃農，還是國際電報",
            "警察檔案保存完整，被害者聲音往往只能從審訊記錄反讀",
            "莫斯科訓令用階段論套殖民地，和地方租佃習慣經常錯位",
            "日共中央視臺灣為帝國破綻，島內同志則先要活過保甲與工頭",
            "上海—東京—臺北的書信延遲，使決策永遠慢過警察行動",
            "國際派強調世界革命時間表，本土派先問今晚農組還開不開得成",
            "階級民族雙重任務讓宣傳左右為難，打地主怕失農戶，打日帝怕失工友",
            "臺灣話傳單與日文理論並列，翻譯本身就是權力關係",
            "讀書會討論剩餘價值，窗外已是巡查木屐聲，理論現場極度不對稱",
            "農組請願與減租若被視為合法，地下黨就失去唯一群眾出口",
            "總督府允許極有限結社，為的是把不滿導入可登記名冊",
            "文協分裂後經費與報刊對倒，左翼失去公開講臺只剩夜聚",
            "知識青年鄙視議會請願太溫和，工人又嫌密會太危險",
            "女性交通員被寫成配角，實際常是跨庄送信的關鍵節點",
            "家庭反對入黨多出於連坐恐懼，不是抽象的反共理論",
            "糖廠季節工流動快，支部名冊還沒抄完人就換港口",
            "礦工與茶工被宣傳點名，真正能穩定開會的仍是少數固定戶",
            "城市知識分子與農村幹部互相看不慣，這裂縫後來被檢舉利用",
            "共產國際遠東局要數字，島內只能呈報誇張的群眾人數",
            "虛報黨員讓莫斯科高興，也讓特高更容易按名單抓人",
            "經費靠僑匯與日共殘餘接濟，一斷炊印刷機就停擺",
            "暗號與化名在小島上很容易被口音與同鄉關係拆穿",
            "地圖上的支部圓點是事後起訴書畫的，當時多半是流動的兩三個人",
            "合法報刊被停發的那天，激進與否不再是辯論而是生存選擇",
            "總督府統計社會運動次數，數字上升就被拿來證明高壓有理",
            "思想犯罪名把讀書等同預備叛亂，知識本身被刑事化",
            "保釋與交保條件要求脫離組織，法律把悔過做成出口",
            "家族連坐讓父母成為義務告密者，倫理被國家徵用",
            "學校開除左傾學生，教育體系替警察完成第一層過濾",
            "寺廟與宗親會有時提供場地，傳統組織並非天然反左",
            "基督教青年會與工友夜學交叉，信仰空間也被監視",
            "無政府主義者早於馬克思派出現，後來在路線鬥爭中被邊緣",
            "民族主義青年拒絕階級鬥爭，兩造爭奪同一批讀者",
            "中國大陸北伐敘事傳入島內，有人以為國民革命可取代共產國際",
            "對岸黨派變化極快，島內資訊卻靠延遲的報紙與口傳",
            "把臺共寫成中共預備隊，會抹掉它曾隸屬日共的制度事實",
            "把臺共寫成純獨立運動，會抹掉土地與工會條款的重量",
            "把臺共寫成失敗笑話，會忽略殖民警察動員了整套保甲國家",
            "判決書裡的陰謀辭彙要當修辭看，還原成會議紀錄才讀得動",
            "回憶錄多寫於戰後冷戰，敘事者已預知誰勝誰負",
            "日文原檔與漢譯之間常有語氣升降，翻譯會重判罪責",
            "女性供述被書記改寫成軟弱或淫亂，性別偏見進入司法文本",
            "原住民地區幾乎未進入台共組織圖，所謂全島革命是沿海幻覺",
            "客家庄與福佬庄的租佃習慣不同，統一口號在地方會走樣",
            "港市碼頭工人接觸世界航線，國際主義在此比農村更有實感",
            "走私與地下經濟有時資助刊物，道德純潔的革命史常省略這筆",
            "疾病、失業與酒後失言造成的破獲，不比英雄叛徒故事少",
            "一九三〇年前後世界蕭條打擊糖價，農運高漲與黨組織脆弱同步",
            "檢舉名單按職業排列，可見警察先摧毀能連外的職業節點",
            "律師辯護空間極窄，思想案件幾乎注定以組織罪收場",
            "公開審判被當成教化劇場，旁聽席也是再恐嚇的教室",
            "出獄者被盯梢，舊同志不敢往來，社會死亡長過刑期",
            "轉向者書寫悔過文換工作，那份文字成為再就業證書",
            "拒絕轉向者長期關押，身體耗損本身就是消滅政策",
            "臺共瓦解後農組殘餘改打游擊式減租，已失去中央指揮",
            "殘存個人轉入文化出版，把未完成的政治改寫成雜誌語氣",
            "戰後有人銜接中共對臺工作，那是另一套上級與另一場失敗",
            "光復敘事若從一九四五起筆，會把日治左翼變成無根插曲",
            "二二八前後個別前黨人再現身，不能倒推成台共仍存在",
            "冷戰檔案解禁後才能核對莫斯科電文，早年只能靠口供",
            "史家爭辯黨員人數，重點不在虛實而在為何必須虛報",
            "領導巡迴靠夜行與親戚屋，地理尺度很小卻被寫成全島起義",
            "港口檢查行李搜印刷品，物質流通與思想流通被同一關卡攔截",
            "日文馬列譯本比漢譯更流通，理論語言本身已經殖民化",
            "漢字刊物必須躲詞彙審查，只好用文藝欄夾帶社會分析",
            "歌謠與演劇被視為煽動工具，娛樂場所也畫進治安地圖",
            "工友喪事被當成集會，警察開始盯葬禮出席名單",
            "減租成功的村子未必入黨，實利與意識形態常常分開走",
            "地主民團與警察合作，農村暴力不對稱遠大於宣傳對打",
            "左翼內部肅奸會議在證據貧乏時最傷自己，猜疑加速瓦解",
            "國際路線一年一變，島內還在消化上一年的小冊子",
            "把失敗只怪個人變節，會放過殖民國家的制度性監控能力",
            "把失敗只怪理論錯誤，會放過小島人口密度對秘密活動的限制",
            "閱讀起訴書要標出時間差，何日開會、何日被捕，常短過一週",
            "對照日共黨史年表，才能看見上級崩潰如何傳導到民族支部",
            "對照中共六大前後爭論，才能看見土地與民族問題的進口版本",
            "人物晚年選擇極度分歧，用結局倒算初心最容易誣陷",
            "女工夜班與育兒負擔被理論忽略，組織時間表其實性別化",
            "識字率限制文件傳達，口頭宣傳比綱領更決定地方理解",
            "總督府社會事業課同時辦救濟，懷柔與檢舉是一體兩面",
            "統計「不良份子」人數上升，媒體配合把左翼描成治安病",
            "知識界事後切割，只承認文協啟蒙、不承認地下組織曾共享讀者",
            "家族口述常強調被迫，檔案卻記自願出席，兩種羞恥要並讀",
            "地圖作業把支部畫在行政區，實際活動沿糖鐵與溪流走",
            "密碼本與會員證在博物展示裡像傳奇，當時多半是薄紙與鉛筆",
            "國際主義承諾救援，破獲當夜沒有任何外部武力可來",
            "所謂世界革命在島上縮成躲避保甲的夜路，尺度差本身是悲劇",
            "後來黨國用台共陰影擴大整肅，日治組織史被工具化",
            "對岸教科書把先烈譜系拉直，刪掉日共上級與獨立條款",
            "本土教材若只講反抗日本，也會刪掉內部路線鬥爭的殘酷",
            "朝鮮共產黨規模與武裝條件不同，不能用同一失敗公式套臺灣",
            "越南東遊與共產網絡另有法屬脈絡，僅共有被帝國統治的結構位置",
            "作為政治史來讀，重點是國家監控如何擊敗跨國意識形態機器",
            "作為社會史來讀，重點是佃農女工學生為何短暫共用同一套詞彙",
            "作為思想史來讀，重點是民族自決與階級解放如何在同一綱領打架",
            "作為檔案史來讀，重點是勝利者的警察文書為何成為主要史料",
            "人名要連著組織職務看，孤立英雄傳會把結構寫成性格",
            "組織圖要連著破獲日期看，靜態系統圖是檢方事後的美化",
            "意識形態要連著印刷條件看，沒有紙張就沒有所謂正確路線",
            "國際關係要連著航線與簽證看，同志情誼過不了港口檢查",
            "後續零星左翼活動是餘波，不是同一黨中央的地下延續",
            "把這段歷史讀成行動手冊，會錯過它其實是一部監控成功史",
            "把這段歷史讀成純粹悲劇，會錯過當事人曾認真計算過勝算",
        ],
    },
    {
        "id": "07_other-20260716-37",
        "title": "香港已死？",
        "author": "張燦輝",
        "points": POINTS_37,
    },
    {
        "id": "07_other-20260716-38",
        "title": "重返牡丹社：牡丹事件筆記、牡丹頭顱筆記",
        "author": "陳耀昌",
        "points": POINTS_38,
    },
    {
        "id": "07_other-20260716-39",
        "title": "全球氣候治理的危與機：兼論香港的挑戰",
        "author": "何偉歡、羅金義",
        "points": POINTS_39,
    },
    {
        "id": "07_other-20260716-40",
        "title": "夕陽西下幾時回——給年老明慧的二十封信",
        "author": "張燦輝",
        "points": POINTS_40,
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
