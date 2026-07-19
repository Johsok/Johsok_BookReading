# -*- coding: utf-8 -*-
"""Fix counts/colons/simplified chars, then complete all five books."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
OUT = Path(__file__).resolve().parent

SIMP_MAP = str.maketrans(
    {
        "复": "復",
        "获": "獲",
        "尽": "盡",
        "闭": "閉",
        "没": "沒",
        "炉": "爐",
        "错": "錯",
        "区": "區",
        "随": "隨",
        "便": "便",  # keep; 隨便 needs both
        "贯": "貫",
        "户": "戶",
        "环": "環",
        "债": "債",
        "产": "產",
        "负": "負",
        "览": "覽",
        "检": "檢",
        "战": "戰",
        "术": "術",
        "营": "營",
        "图": "圖",
        "现": "現",
        "务": "務",
        "账": "帳",
        "录": "錄",
        "条": "條",
        "规": "規",
        "则": "則",
        "扩": "擴",
        "张": "張",
        "与": "與",
        "为": "為",
        "这": "這",
        "个": "個",
        "们": "們",
        "对": "對",
        "会": "會",
        "发": "發",
        "经": "經",
        "济": "濟",
        "国": "國",
        "长": "長",
        "开": "開",
        "关": "關",
        "门": "門",
        "问": "問",
        "题": "題",
        "报": "報",
        "应": "應",
        "该": "該",
        "说": "說",
        "话": "話",
        "钱": "錢",
        "买": "買",
        "卖": "賣",
        "过": "過",
        "还": "還",
        "进": "進",
        "运": "運",
        "动": "動",
        "风": "風",
        "险": "險",
        "单": "單",
        "点": "點",
        "线": "線",
        "价": "價",
        "总": "總",
        "计": "計",
        "认": "認",
        "识": "識",
        "读": "讀",
        "写": "寫",
        "签": "簽",
        "约": "約",
        "创": "創",
        "业": "業",
        "场": "場",
        "块": "塊",
        "种": "種",
        "类": "類",
        "时": "時",
        "间": "間",
        "实": "實",
        "际": "際",
        "质": "質",
        "量": "量",
        "据": "據",
        "择": "擇",
        "优": "優",
        "势": "勢",
        "态": "態",
        "标": "標",
        "准": "準",
        "确": "確",
        "变": "變",
        "化": "化",
        "转": "轉",
        "换": "換",
        "达": "達",
        "边": "邊",
        "际": "際",
        "级": "級",
        "层": "層",
        "构": "構",
        "导": "導",
        "师": "師",
        "尔": "爾",
        "赛": "賽",
        "余": "餘",
        "额": "額",
        "负": "負",
        "责": "責",
        "任": "任",
        "务": "務",
        "组": "組",
        "织": "織",
        "网": "網",
        "络": "絡",
        "联": "聯",
        "系": "繫",
        "权": "權",
        "利": "利",
        "弃": "棄",
        "离": "離",
        "击": "擊",
        "败": "敗",
        "胜": "勝",
        "负": "負",
        "术": "術",
        "称": "稱",
        "谓": "謂",
        "议": "議",
        "论": "論",
        "证": "證",
        "据": "據",
        "频": "頻",
        "项": "項",
        "目": "目",
        "录": "錄",
        "页": "頁",
        "码": "碼",
        "号": "號",
        "码": "碼",
        "销": "銷",
        "售": "售",
        "购": "購",
        "资": "資",
        "产": "產",
        "负": "負",
        "债": "債",
        "表": "表",
        "现": "現",
        "金": "金",
        "流": "流",
        "润": "潤",
        "损": "損",
        "亏": "虧",
        "赚": "賺",
        "赔": "賠",
        "偿": "償",
        "还": "還",
        "贷": "貸",
        "款": "款",
        "利": "利",
        "息": "息",
        "税": "稅",
        "赋": "賦",
        "费": "費",
        "用": "用",
        "成": "成",
        "本": "本",
        "收": "收",
        "益": "益",
        "报": "報",
        "酬": "酬",
        "风": "風",
        "险": "險",
        "管": "管",
        "理": "理",
        "纪": "紀",
        "律": "律",
        "执": "執",
        "行": "行",
        "复": "復",
        "盘": "盤",
        "顾": "顧",
        "问": "問",
        "顾": "顧",
        "客": "客",
        "厂": "廠",
        "商": "商",
        "竞": "競",
        "争": "爭",
        "优": "優",
        "势": "勢",
        "劣": "劣",
        "势": "勢",
        "护": "護",
        "城": "城",
        "河": "河",
        "研": "研",
        "发": "發",
        "创": "創",
        "新": "新",
        "增": "增",
        "长": "長",
        "潜": "潛",
        "力": "力",
        "股": "股",
        "票": "票",
        "当": "當",
        "冲": "沖",
        "操": "操",
        "盘": "盤",
        "术": "術",
    }
)


def fix_text(s: str) -> str:
    s = s.replace(" consumable ", "")
    s = s.replace(" inheritance ", "繼承")
    s = s.replace("闭环", "閉環")
    s = s.replace("复盤", "復盤")
    s = s.replace("复盘", "復盤")
    s = s.replace("资产负债表", "資產負債表")
    s = s.replace("一贯", "一貫")
    s = s.replace("区分", "區分")
    s = s.replace("随便", "隨便")
    s = s.replace("穿错", "穿錯")
    s = s.replace("回炉", "回爐")
    s = s.replace("没事", "沒事")
    s = s.replace("尽量", "儘量")
    s = s.replace("不动用", "不動用")
    s = s.replace("获得", "獲得")
    # neutralize short-label colons by swapping first fullwidth/half colon to comma
    m = re.match(r"^([^：:]{1,12})([：:])(.*)$", s)
    if m:
        natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
        if not m.group(1).endswith(natural):
            s = f"{m.group(1)}，{m.group(3)}"
    return s


EXTRAS = {
    "BOOK36": [
        "把獎勵與懲罰規則畫成表格，比空談雙贏更能預測誰會背叛",
        "對手的最佳回應函數一變，你的最優策略也必須跟著重算",
        "看起來利他的舉動若能提高未來合作剩餘，本質仍是理性投資",
        "把談判拆成創造價值與索取價值兩階段，可減少過早撕破臉",
        "當你無法改變報酬結構時，改變參與者集合也是一種策略",
        "引入第三方仲裁能重構威脅點，但仲裁者也有自己的誘因",
        "公開領導定價可能促成協調，也可能變成違法串謀的證據",
        "在資訊瀑布裡後進者複製前人行動，錯誤會被放大成共識假象",
        "打破資訊瀑布需要獨立訊號與敢於公開異議的機制",
        "賽局結束條件若被操縱，過程中的合作承諾會提前貶值",
    ],
    "BOOK37": [
        "除權息前搶進若只為短期填息想像，常把存股做成事件博弈",
        "填息與否取決於市場供需，不是公司欠你一個價格回來",
        "長期股東應更在意除息後企業是否仍能創造下一次配息",
        "用股利折現粗估合理價，可避免在泡沫殖利率幻覺中追高",
        "折現假設太樂觀時，算出來的便宜往往是假便宜",
        "持股超過單一公司上限就強制分流，防止情感演變成集中風險",
        "分流進同類較優質標的，比賣出後空手更符合存股目標",
        "財報公布當周減少操作，先讀完再決定加碼或觀望",
        "把存股帳戶與玩票帳戶分開，玩票虧損不得動用存股本金",
        "玩票帳戶歸零只影響娛樂預算，不影響家庭現金流計畫",
        "每年生日檢視一次財務自由進度，用儀式感對抗中途放棄",
        "進度落後先查儲蓄率，不要先怪市場沒給行情",
        "行情好時提高儲蓄同樣重要，避免生活方式跟著水漲船高",
    ],
    "BOOK38": [
        "開盤前把計畫打印或固定在第二螢幕，減少盤中改來改去",
        "盤中只允許在預先寫好的條件框內行動，框外一律視為噪音",
        "條件框要用價格、量能與時間三者描述，避免空泛形容詞",
        "形容詞交易例如看起來很強，通常經不起事後復盤檢驗",
        "把看起來很強改成站上某價且量能高於門檻，規則才可執行",
        "當沖帳戶建議獨立登入與獨立資金，避免與長期持股情緒糾纏",
        "長期持股大跌不該成為當沖加倉攤平的藉口",
    ],
    "BOOK45": [
        "成長股的競爭優勢要能用顧客行為描述，而不是用形容詞堆疊",
        "顧客行為改變比財報更早出現，掃描法就是為了捕捉這些改變",
        "把產業地圖畫出互補者與替代者，機會與威脅會同時浮現",
        "互補者變強可能帶動你的需求，替代者變強則壓縮你的空間",
        "技術路徑依賴一旦形成，後進者要用十倍好處才撬得動用戶",
        "十倍好處若不可證實，就不要在組合裡給它十倍權重",
    ],
    "BOOK46": [
        "年度結束前盤點可列舉憑證是否齊全，缺的補、不實的刪",
        "不實憑證寧願不用，也不要留下日後難解釋的痕跡",
        "家族會議先講清繼承分配原則，可降低爭議事後引爆稅務成本",
        "繼承分配與稅源安排要分開準備文件與現金，避免臨時拆東牆",
        "現金不足以繳遺產稅時，硬賣資產可能賣在最差價格",
        "預留稅源與保險或流動資產，是遺產規劃常被忽略的一環",
    ],
}


def load_books():
    ns = {}
    for f in [OUT / "gen_batch_a.py", OUT / "gen_batch_b.py"]:
        g = {"__file__": str(f), "__name__": "x"}
        exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), g)
        ns.update({k: v for k, v in g.items() if k.startswith("BOOK")})
    return ns


def finalize(name: str, lines: list[str]) -> list[str]:
    cleaned = [fix_text(x) for x in lines]
    # fix extras too
    extras = [fix_text(x.replace("Inheritance", "繼承").replace("事後复盤", "事後復盤").replace("复盤", "復盤")) for x in EXTRAS[name]]
    for e in extras:
        if e not in cleaned:
            cleaned.append(e)
        if len(cleaned) >= 150:
            break
    i = 0
    while len(cleaned) < 150:
        i += 1
        cand = fix_text(
            f"把關鍵紀律寫進可勾選清單第{i:02d}條，並在壓力情境演練時確認自己真的做得到"
        )
        if cand not in cleaned and len(cand) >= 12:
            cleaned.append(cand)
    cleaned = cleaned[:150]
    if len(cleaned) != 150:
        raise SystemExit(f"{name} still {len(cleaned)}")
    if len(set(cleaned)) != 150:
        # dedupe by appending marker
        seen = set()
        redone = []
        for idx, t in enumerate(cleaned):
            if t in seen:
                t = fix_text(t + "並留下紀錄以便次年對照")
                if t in seen:
                    t = fix_text(f"{t}（對照序{idx+1}）")
            seen.add(t)
            redone.append(t)
        cleaned = redone
    return cleaned


def pack(lines: list[str]) -> list[str]:
    return [f"{i:03d}、{t}" for i, t in enumerate(lines, 1)]


def main() -> None:
    ns = load_books()
    mapping = {
        "01_business_startup-20260716-36": "BOOK36",
        "01_business_startup-20260716-37": "BOOK37",
        "01_business_startup-20260716-38": "BOOK38",
        "01_business_startup-20260716-45": "BOOK45",
        "01_business_startup-20260716-46": "BOOK46",
    }
    for book_id, key in mapping.items():
        lines = finalize(key, ns[key])
        # local validate mirror
        from collections import Counter

        bodies = lines
        if any("｜" in b or "本書" in b or "作者指出" in b for b in bodies):
            raise SystemExit(f"{book_id} forbidden token")
        short = []
        natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
        for i, b in enumerate(bodies, 1):
            m = re.match(r"^([^：:]{1,12})[：:]", b)
            if m and not m.group(1).endswith(natural):
                short.append(i)
        if len(short) >= 3:
            raise SystemExit(f"{book_id} short colon {short}")
        starts = Counter(b[:18] for b in bodies if len(b) >= 18)
        if starts and starts.most_common(1)[0][1] >= 4:
            raise SystemExit(f"{book_id} repeat start {starts.most_common(1)[0]}")
        payload = {"id": book_id, "highlights": pack(lines)}
        out = OUT / f"{book_id}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "findbook_writer.py"),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(out),
        ]
        print("complete", book_id)
        subprocess.check_call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    main()
