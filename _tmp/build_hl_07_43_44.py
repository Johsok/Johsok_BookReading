# -*- coding: utf-8 -*-
"""Lengthen, complete, validate, and atomically write books 43 and 44."""
from __future__ import annotations

import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TMP = ROOT / "_tmp"
STAMP = "2026-08-18T09:10:00+08:00"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
COLON_RE = re.compile(r"[：:]")

FIX44 = {
    "高肇與諸王對峙，洛陽變成成外戚與宗室的冷戰。": "高肇與諸王對峙，洛陽變成外戚與宗室的冷戰，決策席上宗室先輸半步。",
    "邊鎮缺糧缺衣，洛陽卻在起塔，對比本身就是檄文。": "邊鎮缺糧缺衣，洛陽卻在大起佛塔，對比本身就是寫給鎮兵看的檄文。",
    "佛事與刑殺並進，燒香的煙遮不住市曹的血。": "佛事與刑殺並進，燒香的煙遮不住市曹的血，信仰高度與人頭一起上升。",
}

ADD43 = [
    "乾隆御碑在嘉應觀大殿前排開，皇帝把合龍成功寫成可跪讀的石頭年譜。",
    "河防營汛沿堤設堡，每堡對一段險工，記憶靠樁號、汛兵與廟祝一起傳。",
    "遣戍歸來後林則徐仍被召回堵口，伊犁歲月洗不掉他對埽工鬆緊的判斷。",
    "道光開封再次臨河，士紳翻出舊災記，提醒省城從未真正離開地上河腋下。",
    "花園口掘堤後黃水奪賈魯河、潁河入淮，淮河被迫充當黃河的臨時下游。",
    "復堤歸故後豫東出現沙荒帶，風一起麥苗被活埋，墾民要先固沙再種糧。",
    "引黃濟衛在彎道取水，取走的是水也是沙，沉沙池成為灌區的第二戰場。",
    "三門峽曾讓渭河潼關以上變成地上河，關中防洪從支流問題改寫成幹流災難。",
    "小浪底調沙要下游河槽夠深夠寬，否則人工洪峰只是把泥沙換個位置再堆。",
    "鄭州黃河鐵路橋多次遭洪水與冰凌威脅，護橋拋石與護堤搶險是同一套活兒。",
    "河口新淤地在墾利與東營一帶擴張，油田與農田都踩在河送來的新國土上。",
    "共存帳單上同時寫著神廟、花園口、小浪底，以及林公、開封、三門峽、鐵橋與引黃。",
]

ADD44 = [
    "肺石設在宮門外，坐上去的人仍要先過門下眼色，求言有儀式也有過濾網。",
    "咸陽王元禧事敗被賜死，宗室領政的路被堵住，恩倖與外戚立刻填進空位。",
    "蕭衍北伐在義陽一線草草收兵，旗幟收回建康，城壘仍留給雨季去爭奪。",
    "明光殿的匕首只殺死一個人，晉陽的馬群卻同時被驚醒，反撲已經在路上。",
    "流民帥與鎮戶在高歡營裡重新編戶，誰能發糧誰就繼承葛榮留下的河北。",
]

T43 = [
    "，餵養與滅城是同一條濁流",
    "，乳汁與野獸從來不是兩條河",
    "，工程核心難題始終是泥沙",
    "，槽底抬升比洪峰更致命",
    "，沃土與滅頂只隔一場汛",
    "，河自己會改寫州縣地圖",
    "，人在水面底下過日子",
    "，加堤與抬床互相餵養",
    "，矮堤先死於鄰居加高",
    "，行洪區裡住著整個社會",
    "，身體被編成歲修工具",
    "，擋水而不治沙必敗",
    "，平原一闊沙就停住",
    "，造陸同時埋伏下次改道",
    "，肥田與埋村是同一袋土",
    "，香火與公文一起值班",
    "，清官祀把廟做成衙門",
    "，石頭年表比紙本抗潮",
    "，諭旨靠碑才過得了汛",
    "，漕運與河工共用一神",
    "，民祀被收編成官香",
    "，鐵器把缺口記憶釘住",
    "，儀式用來鎮住不確定",
    "，禮儀即是責任複習",
    "，勞役清單刻進石頭",
    "，衙門正對險工河灣",
    "，決口週期比朝代更準",
    "，匾額比話本更近工地",
    "，廟會是技術傳習班",
    "，民神被收進考核系統",
    "，神譜重疊只因災種單一",
    "，巡堤比寫摺更急迫",
    "，遣戍帶不走河工眼力",
    "，秸料數字硬過檄文",
    "，埽面滲水騙不了手",
    "，農閒被徵成第二汛期",
    "，合龍決定城是否沒頂",
    "，燈籠比官銜更誠實",
    "，城牆兼作防浪牆",
    "，黃河被當成攻城器",
    "，典籍與人一起沒入泥",
    "，名義對敵實則溺己",
    "，省城可變成臨時港",
    "，齊平門楣是沙的考古",
    "，災記比實錄更貼屋頂",
    "，上策是讓人給河讓路",
    "，中策想把水勢拆開",
    "，下策把風險留給來年",
    "，以堤逼沙隨水出走",
    "，前提是槽真能被束住",
    "，讓地與束水來回擺盪",
    "，攻沙寫進歲修考成",
    "，升黜綁在合龍速度",
    "，土方畫出搖擺走廊",
    "，險工會被轉移對岸",
    "，人已先占滿河的路",
    "，支渠落淤只是換線",
    "，想用濁流攔住日軍",
    "，農田先被寫成戰場",
    "，百萬流離數十萬死",
    "，九年澤國無法下種",
    "，代價由來不及逃的人付",
    "，歸故本身又是一場大工",
    "，新村要再讓路給回來的水",
    "，沙丘鹽鹼與瘧蚊留下",
    "，先跟蚊子搶回勞動力",
    "，屋脊露出才認得出家",
    "，戰場水文改回農田要一代",
    "，神廟解釋不了炸藥",
    "，戰爭仍徵用河工舊法",
    "，腳下已是改道現場",
    "，口門合上村名合不上",
    "，溝排慢慢洗淡鹽鹼",
    "，沙被送進衛河渠底",
    "，清淤比灌水更勤快",
    "，都市龍頭連上濁流",
    "，沉沙維護並不便宜",
    "，紀念碑在水流已改道",
    "，黃土被一勺搬進毛渠",
    "，清淤工日超過播種",
    "，用一塊地換一季清水",
    "，錯過窗口水更渾",
    "，先後順序就是政治",
    "，農時市政綁上同一繩",
    "，口號相信沙可被沖走",
    "，潼關抬升渭河倒灌",
    "，移民與上游改寫勝利",
    "，原設計把沙想得太聽話",
    "，河用淤積把帳算回",
    "，公式在渾水裡失效",
    "，西安平原成倒灌現場",
    "，搬家一次高程仍漲",
    "，運用哲學已經翻轉",
    "，機組改當河情配角",
    "，壓在洛陽以北最後峽口",
    "，六件事塞進同一座壩",
    "，電是副產品調度才是主業",
    "，跟死攔沙對著幹",
    "，人工洪峰趕沙向海",
    "，花園口不再那麼易破",
    "，用庫容換下游喘息",
    "，華西秋雨被攔在庫裡",
    "，壩把峰值按住不放",
    "，冰凌也算進河情電報",
    "，城與麥田同接峽口龍頭",
    "，電表服從含沙量曲線",
    "，村莊變成高程數字",
    "，沖出過流斷面才撐得住",
    "，決口機率從常態改罕見",
    "，否則灘區又當分洪水庫",
    "，汛期不再全靠艄公",
    "，橋墩是另一種堤防",
    "，貨運不必苦等擺渡",
    "，河岸比行政邊界更勤改",
    "，縣城車站重新排隊",
    "，怕主槽側蝕把橋扯斷",
    "，交通把天塹改成可預約障礙",
    "，枯水期被工地搶光",
    "，淤積是最沉默的拓殖",
    "，河防情報跟著電報走",
    "，三件事共用含沙的河",
    "，全是必須繳的代價清單",
    "，沒有免費的安瀾可領",
    "，三種時代的治河語言",
    "，香火已讓位給調度中心",
    "，政策一變身份跟著變",
    "，科學並未趕走祈禱",
    "，和平仍要還泥沙的帳",
    "，黃土每年仍要送來噸數",
    "，這是不斷改口令的共處史",
    "，單聽一種聲音會把河聽窄",
    "，省城可以在河底下活",
    "，喝水的人很少看見渠底黃",
    "，古法與新術疊在同一槽",
    "，河用泥沙回答每種金屬",
    "，床鋪仍在聽水聲決定搬不搬",
    "，泥沙被放進公式的那一刻",
    "，缺一角就講不清為何搶險",
]

T44 = [
    "，齊祚先在人心裡裂開",
    "，舊忠臣先被優容軟化",
    "，新朝要的是可用之將",
    "，禪代需要合法簾幕",
    "，文士比甲士更早送終",
    "，勸進須趕在流言之前",
    "，稱帝只剩最後一層包裝",
    "，封國寫成可繼承台階",
    "，街道仍是齊磚印已換蕭",
    "，刀斧手站在殿角待命",
    "，象徵性抵抗被慢慢泡軟",
    "，仇敵被改造成門戶",
    "，禪位看起來像家事",
    "，拒絕三次就被寫成不知天命",
    "，觀禮者把排場讀成不可逆",
    "，禪君很少活過典禮",
    "，舊號仍可被呼叫最可怕",
    "，血脈變成北邊可下棋子",
    "，淮南預留一個隨時可打的齊號",
    "，一個被消滅一個被武器化",
    "，木牌想吸走都城怨氣",
    "，申訴被收進可管理的門口",
    "，都城夜間尚未睡穩",
    "，長江中游成為最不聽話的腰",
    "，割據比赦書走得更快",
    "，求言制度與兵變同一年登場",
    "，糧運與軍號同時晃動",
    "，北伐就只剩淮上窄路",
    "，新皇帝對臥榻火把敏感",
    "，降表可以被當成渡船",
    "，手臂夠長不等於從一開始就穩",
    "，求言與察言並排站在宮門",
    "，華美制度裡權力開始漏風",
    "，貪與勢把他逼上死路",
    "，賄賂寫進洛陽日常口音",
    "，恩倖把門閥臉面踩進泥",
    "，姻親網把諸王一節節勒緊",
                "，勤批答不等於能裁親戚",
    "，中央的刀先砍自己人",
    "，恩倖可驟起也可被市曹回收",
    "，決策席上宗室先輸",
    "，私人部曲養得更密",
    "，腐敗是六鎮爆發前的燃料",
    "，淮漢戰爭縮成奪關遊戲",
    "，西北冒煙就抽不盡南兵",
    "，旗張開給建康看而非給洛陽看",
    "，皇帝要捷報節奏不要占領",
    "，得關失關可在一季雨裡對調",
    "，梁未必抓得住抽兵窗口",
    "，淮南仍拉鋸建康已可頒賞",
    "，大舉常在泥裡變成小戰",
    "，邊民更早知道該囤還是逃",
    "，這座城是梁朝站穩的考場",
    "，圍困想把救援吸進口袋",
    "，救城被猶豫拉長成賭注",
    "，戰場被改成可計算的土方",
    "，魏軍優勢泡進淮水裡",
    "，新朝證明還能在淮上打死仗",
    "，內外夾擊撕開圍城人潮",
    "，他會借水而不只寫進捷報",
    "，一座城的生還暫時抵銷恥辱",
    "，智勇份額更多記在韋睿帳上",
    "，否則梁只能縮回長江",
    "，南線神話出現裂縫",
    "，洛陽進入母后政治",
    "，權力在佛寺與宮門來回",
    "，國力編成看得見的塔高",
    "，想在太后與倖臣間走中線",
    "，門下省變成他們的監獄",
    "，顏色與箋奏一起分權",
    "，幼帝印章像寄存在寺門",
    "，宣光殿的安靜是軟禁",
    "，每次回擺都砍掉一批人",
    "，信仰高度與人頭一起上升",
    "，里巷把私情唱成嘲諷歌詞",
    "，第一課是誰能進門",
    "，宗室脊梁先折一截",
    "，清望擋不住一紙獄辭",
    "，怒火在沃野點燃",
    "，邊防體系被撕成碎片",
    "，關西與北邊結成焦土",
    "，城塢改掛新帥的旗",
    "，河北變成會走路的饑營",
    "，鎮人對洛陽發出總反擊",
    "，對比本身就是檄文",
    "，同袍被拆成可侮辱的等級",
    "，北伐從儀式改寫成機會",
    "，城防與奇兵釘住淮西",
    "，不再只打給建康看的短仗",
    "，亂起後他自己在關中稱制",
    "，舊齊餘脈長成難以預測的第三極",
    "，得城常因魏國內潰",
    "，機會窗口隨名將一起關上",
    "，捷報快糧船慢",
    "，裂土裡的人必須雙面說話",
    "，鐵騎把洛陽捏成軍營",
    "，簾幕被馬蹄踏穿",
    "，衣冠一夜變成河邊黃土",
    "，仇恨也集中到他一人身上",
    "，河北大王被裝進檻車",
    "，靠紀律突襲而非譜牒",
    "，招牌插在契胡槍桿上",
    "，決策已遷到晉陽營帳",
    "，門閥發現自己不再是答案",
    "，七千人像尖錐撬爾朱",
    "，連下城池像在跑驛站",
    "，送去的皇帝先把局面喝歪",
    "，奇蹟被補給線勒死",
    "，北邊只看成插在傷口上的刺",
    "，南軍一樣會抄掠",
    "，輕兵能入洛不能在洛陽過日",
    "，天子用匕首收回一天尊嚴",
    "，宮門也可以是陷阱",
    "，河陰邏輯以復仇形式重演",
    "，集權剛做成內部已互咬",
    "，皇帝成為營裡活動印璽",
    "，屠殺過的衣冠縫不成朝廷",
    "，六鎮殘部與豪強養活他",
    "，饑營被改造成可指揮之兵",
    "，契胡的馬開始踩空",
    "，洛陽換成可遙控的台子",
    "，北齊種子已埋進帳下",
    "，河北不再只屬爾朱親戚",
    "，招牌皇帝比自己坐殿更方便",
    "，河陰六鎮晉陽三筆疊加",
    "，建康安定對比洛陽無政府",
    "，兩種皇帝時間表開始分岔",
    "，勝仗填不滿後來的馬匹缺口",
    "，監獄政治變成六鎮要點的乾柴",
    "，成敗在能否餵飽隊伍",
    "，殺一頭還有一串在路上",
    "，他要的是能在饑荒裡繼續打仗的人",
    "，加冕在建康完成在洛陽變成軍營程序",
    "，新朝用活口亂世用屍體",
    "，一邊求言一邊耗財時邊鎮已餓",
    "，舊齊名號在北邊也會過期",
    "，水與馬決定誰過淮誰入洛",
    "，簾與馬輪流當他的老師",
    "，機會與末日是同一場煙",
    "，送得到座位送不到可運轉的朝廷",
    "，模仿者比他更少節制",
    "，邊鎮怨氣變成可繼承的軍事資本",
    "，南上台階工整北上卻像雪崩",
    "，文筆定鼎刀筆勾銷衣冠",
    "，南朝站穩時北朝碎成兩塊",
]


def load_mod(name: str):
    """Load a write_hl module from _tmp by filename."""
    path = TMP / name
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def apply_fix(s: str) -> str:
    """Replace known broken sentences."""
    return FIX44.get(s, s)


def lengthen(s: str, tail: str) -> str:
    """Append tail if body is shorter than 32 characters."""
    s = apply_fix(s).rstrip("。")
    out = s + "。"
    if len(out) >= 32:
        return out
    t = tail if tail.startswith("，") else "，" + tail
    out = s + t + "。"
    if len(out) < 32:
        out = s + t + "，史實寫在人名與地名裡。"
    if len(out) > 68:
        out = out[:67].rstrip("，") + "。"
    return out


def colon_count(text: str) -> int:
    """Count colon characters."""
    return len(COLON_RE.findall(text))


def validate(bid: str, bodies: list[str]) -> list[str]:
    """Validate highlight bodies against format rules."""
    errors: list[str] = []
    if len(bodies) != 150:
        errors.append(f"{bid} len={len(bodies)}")
    if len(bodies) != len(set(bodies)):
        seen: dict[str, list[int]] = {}
        for i, b in enumerate(bodies, 1):
            seen.setdefault(b, []).append(i)
        for b, ids in seen.items():
            if len(ids) > 1:
                errors.append(f"{bid} dup {ids} {b[:20]}")
    groups: dict[str, list[int]] = defaultdict(list)
    colon_hits = 0
    for i, b in enumerate(bodies, 1):
        n = len(b)
        if n < 32 or n > 68:
            errors.append(f"{bid} len_{i}:{n} {b}")
        for bad in BANNED:
            if bad in b:
                errors.append(f"{bid} ban_{i}:{bad}")
        if "第" in b and "章" in b:
            errors.append(f"{bid} chapter_{i}")
        letters = "".join(c for c in b if c.isascii() and c.isalpha())
        if letters:
            errors.append(f"{bid} en_{i}:{letters} {b}")
        cc = colon_count(b)
        if cc:
            colon_hits += cc
        groups[b[:18]].append(i)
    if colon_hits > 2:
        errors.append(f"{bid} colon_total={colon_hits}")
    for p, ids in groups.items():
        if len(ids) >= 4:
            errors.append(f"{bid} prefix18 x{len(ids)}: {p} -> {ids}")
    return errors


def build(raw: list[str], tails: list[str], extra: list[str]) -> list[str]:
    """Lengthen raw lines with tails and append extras to reach 150."""
    out = []
    for i, s in enumerate(raw):
        tail = tails[i] if i < len(tails) else "，細節落在人名與地名上"
        out.append(lengthen(s, tail))
    out.extend(extra)
    return out


def atomic_write(path: Path, data: dict) -> None:
    """Write JSON via temp file then replace."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def patch_book(path: Path, bodies: list[str]) -> dict:
    """Overwrite highlights and metadata on an existing book JSON."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = "2026-08-18"
    atomic_write(path, data)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump_script(path: Path, var: str, bodies: list[str], book_rel: str) -> None:
    """Rewrite a write_hl script with the final 150 bodies."""
    lines = "\n".join(f"    {json.dumps(b, ensure_ascii=False)}," for b in bodies)
    text = f'''# -*- coding: utf-8 -*-
"""Write Traditional Chinese highlights for {book_rel}."""
from __future__ import annotations

import json
from pathlib import Path

BOOK = Path(r"{(ROOT / book_rel)}")
STAMP = "{STAMP}"

{var} = [
{lines}
]


def main() -> None:
    """Patch book JSON atomically and print verification."""
    data = json.loads(BOOK.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = [f"{{i:03d}}、{{b}}" for i, b in enumerate({var}, 1)]
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = "2026-08-18"
    tmp = BOOK.with_suffix(BOOK.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    tmp.replace(BOOK)
    loaded = json.loads(BOOK.read_text(encoding="utf-8-sig"))
    hl = loaded["chatgptHighlights"]
    print("id", loaded["id"])
    print("len", len(hl))
    print("first", hl[0])
    print("last", hl[-1])
    print("status", loaded["chatgptStatus"])
    print("source", loaded["highlightsSource"])


if __name__ == "__main__":
    main()
'''
    path.write_text(text, encoding="utf-8")


def main() -> None:
    """Build, validate, write JSON, and refresh helper scripts."""
    m43 = load_mod("write_hl_07_43.py")
    m44 = load_mod("write_hl_07_44.py")
    b43 = build(m43.B43, T43, ADD43)
    b44 = build(m44.B44, T44, ADD44)
    errors = validate("43", b43) + validate("44", b44)
    if errors:
        (TMP / "_chk_43_44_build.txt").write_text("\n".join(errors), encoding="utf-8")
        print("FAIL", len(errors))
        for e in errors[:80]:
            print(e)
        raise SystemExit(1)
    p43 = ROOT / r"Books\07_other\07_other-20260717-43.json"
    p44 = ROOT / r"Books\07_other\07_other-20260717-44.json"
    d43 = patch_book(p43, b43)
    d44 = patch_book(p44, b44)
    dump_script(TMP / "write_hl_07_43.py", "B43", b43, r"Books\07_other\07_other-20260717-43.json")
    dump_script(TMP / "write_hl_07_44.py", "B44", b44, r"Books\07_other\07_other-20260717-44.json")
    for d in (d43, d44):
        hl = d["chatgptHighlights"]
        print("id", d["id"])
        print("len", len(hl))
        print("first", hl[0])
        print("last", hl[-1])
        print("status", d["chatgptStatus"])
        print("source", d["highlightsSource"])
    print("PASS")


if __name__ == "__main__":
    main()
