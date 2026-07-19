# -*- coding: utf-8 -*-
"""Fix counts, write results, and complete books 20260717-16..20."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("g", ROOT / "tools" / "_gen_grok_20260717_16_20.py")
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

EXTRA17 = [
    "清算順序決定危機中誰先被清償，結構優先權比口頭承諾更真實",
    "或有請求權把公司想成一組選擇權，股權是對資產的買權",
    "可轉換證券的稀釋日程表，會改變創辦人對融資時點的判斷",
    "員工選擇權的價值依賴波動與期限，帳面費用與真實激勵並不完全相同",
    "債券契約的加速到期條款，讓技術性違約也能瞬間變成流動性危機",
    "交叉違約把一份合約的破口傳染到其他融資，複雜結構提高脆度",
    "利息保障倍數下滑是信用惡化的早期訊號，等評等下調往往已晚",
    "營運槓桿高的公司對營收波動更敏感，固定成本是隱藏的金融風險",
    "季節性融資需求要用承諾額度預先鎖定，否則旺季反而借不到錢",
    "供應商金融與銀行融資互相替代，集中到期日會製造人為緊縮",
    "外匯自然避險優於疊加衍生商品，匹配收支幣別是最便宜的對沖",
    "長期資本預算要壓力測試折現率，樂觀假設是專案過關的常見捷徑",
    "投資後稽核把預估與實際對照，組織才能停止獎勵說故事能力",
]

EXTRA18 = [
    "融資用途表要細到能被追問，模糊的品牌行銷常是紅旗",
    "顧問費與中介費過高會侵蝕進帳資金，條款應預先設上限",
    "橋接輪的高折扣會沉重稀釋，只用在能看得到下一輪的短窗口",
    "內部員工認購若條款優於外部，要能解釋激勵必要性避免治理爭議",
    "共同銷售義務可能迫使創辦人在不理想時點賣股，簽署前要算清楚",
    "智財抵押融資少見但漸增，估值爭議與執行變現能力是關鍵",
    "客戶成功指標若進融資契約，定義模糊會變成無限義務",
    "多產品線同時燒錢時，要勇敢關掉學習價值最低的那條",
    "研發里程碑達成卻不見收入，要分辨是產品問題還是通路問題",
    "政府標案帳期長，得標喜訊若無過橋資金可能變成現金陷阱",
    "硬體認證費用與時間要寫進跑道，實驗室排隊會吃掉整季計畫",
    "專利年費與國際布局分期投入，別在種子期就把現金鎖死在虛榮申請",
    "資料標註與模型訓練成本會隨迭代指數上升，智慧新創尤需單位經濟紀律",
    "開源核心加托管服務的模式，要算清楚支援成本誰在付",
    "社群驅動成長看似低獲客成本，維護社群的人力仍會出現在費用表",
]

EXTRA19 = [
    "訂單到現金流程的每一個卡點都該有主人，跨部門空白最耗現金",
    "預測準確度要納入業務考核，否則財務永遠在為樂觀接單擦屁股",
    "安全庫存參數應隨供應可靠度調整，一刀切天數會懲罰好供應商",
    "模具分攤年限要對齊產品生命，過短會虛增成本、過長會低估風險",
    "客戶指定料件若無法替代，議價權流失要反映在報價與合約條款",
    "出口退稅時點納入現金預測，退得慢等於政府占用你的營運資金",
    "電子支付手續費看似小，薄利多銷模式下足以決定產品生死",
    "加盟金收入若一次認列，後續輔導成本會讓後期現金看起來變差",
    "維修據點拓展要用服務半徑與工單密度計算，情緒拓點最燒錢",
    "管理升級成功後，財務應從記帳角色轉成資源配置的挑戰者",
]

EXTRA20 = [
    "財富炫耀的邊際快樂遞減很快，安全感的邊際價值卻常被忽略",
    "把投資當娛樂的人，通常會為娛樂支付學費而非收取報酬",
    "年度檢視一次資產配置，比每週盯盤更符合長期資本的節奏",
    "失業保險與緊急基金重疊設計，才能避免任一環失效就崩盤",
    "子女教育金要分目標投資，期限越近波動預算應越低",
    "長壽風險意味著你可能需要讓資產工作比預期更久，過早花光最危險",
    "退而不休的兼職收入能降低提領壓力，也維持技能與社交資本",
    "搬到低成本地區是合法套利，但要計算失去網絡的機會成本",
    "醫療通膨常高於一般物價，退休醫療預算用舊假設會嚴重不足",
    "財務計畫的最大風險往往是自己，制度比洞察更能對抗人性",
    "當你不再需要用錢證明價值，金錢才比較可能好好為你工作",
    "市場波動是入場費，想免票入場通常也拿不到長期戲票",
    "把儲蓄自動化後，剩下的精力去改善收入與健康，報酬率往往更高",
    "金錢故事會世代相傳，改變家庭劇本從誠實對話開始",
    "足夠的定義寫下來並定期重讀，欲望膨脹時才有對抗的錨點",
]

NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORB = ("本書", "作者指出", "本章", "這一章")


def extend(base: list[str], extras: list[str], fixes: list[tuple[str, str]]) -> list[str]:
    out = []
    for body in base:
        for old, new in fixes:
            body = body.replace(old, new)
        out.append(body)
    have = set(out)
    for extra in extras:
        if extra not in have:
            out.append(extra)
            have.add(extra)
    return out


def validate(book_id: str, highlights: list[str], title: str, author: str) -> None:
    short_colon = []
    bodies = []
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not line.startswith(expected):
            raise ValueError(f"{book_id} bad number {index}")
        if "｜" in line or "\n" in line or "\r" in line:
            raise ValueError(f"{book_id} banned format {index}")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if len(body) < 12:
            raise ValueError(f"{book_id} short {index}: {body}")
        if any(prefix in body for prefix in FORB):
            raise ValueError(f"{book_id} forbidden {index}")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} step wording {index}")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short_colon.append(index)
        bodies.append(body)
    if len(short_colon) >= 3:
        raise ValueError(f"{book_id} short colon {short_colon[:10]}")
    if len(set(bodies)) != 150:
        raise ValueError(f"{book_id} duplicates")
    starts = Counter(body[:18] for body in bodies)
    if starts.most_common(1)[0][1] >= 4:
        raise ValueError(f"{book_id} repeated starts {starts.most_common(3)}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} repeated {label}")


def write_and_complete(book_id: str, title: str, author: str, bodies: list[str]) -> str:
    if len(bodies) != 150:
        raise ValueError(f"{book_id} count={len(bodies)}")
    lines = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
    validate(book_id, lines, title, author)
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": lines, "source": "cursor-grok-4.5"}
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
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    text = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0 or f"written\t{book_id}" not in text:
        raise RuntimeError(f"{book_id} writer failed:\n{text}")
    return f"{book_id}\tsuccess\t150"


def main() -> None:
    book16 = list(m.BOOK16)
    book17 = extend(m.BOOK17, EXTRA17, [("市場alpha", "市場超額報酬")])
    book18 = extend(m.BOOK18, EXTRA18, [("會增加加管理負擔", "會增加管理負擔")])
    book19 = extend(
        m.BOOK19,
        EXTRA19,
        [("下一次次發生", "下一次發生")],
    )
    book20 = extend(
        m.BOOK20,
        EXTRA20,
        [("市場alpha", "市場超額報酬"), ("追逐IRR", "追逐內部報酬率")],
    )

    jobs = [
        ("01_business_startup-20260717-16", "出乎意料的經濟學", "蒂莫西·泰勒", book16),
        ("01_business_startup-20260717-17", "金融的智慧", "米希爾·德賽", book17),
        ("01_business_startup-20260717-18", "創業金融學", "顧婧、周偉", book18),
        (
            "01_business_startup-20260717-19",
            "中小企業財務：從系統思維到管理升級",
            "楊金芳、鄒函宸、楊燕芳",
            book19,
        ),
        ("01_business_startup-20260717-20", "金錢的藝術", "摩根·豪澤爾", book20),
    ]

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    reports = []
    for book_id, title, author, bodies in jobs:
        if only and book_id not in only and not any(book_id.endswith(item) for item in only):
            continue
        print(f"processing {book_id} count={len(bodies)}", flush=True)
        reports.append(write_and_complete(book_id, title, author, bodies))
        print(reports[-1], flush=True)

    print("---")
    for line in reports:
        print(line)


if __name__ == "__main__":
    main()
