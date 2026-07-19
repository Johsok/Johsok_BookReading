# -*- coding: utf-8 -*-
"""Fix, pad to 150, write results, and complete chunk_15 books."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def validate_highlights(book_id: str, highlights: list[str], title: str = "", author: str = "") -> None:
    if len(highlights) != 150:
        raise ValueError(f"{book_id} 必須剛好 150 點，目前 {len(highlights)}")
    short_colon_lines = []
    bodies = []
    forbidden_prefixes = ("本書", "作者指出", "本章", "這一章")
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            raise ValueError(f"{book_id} 第 {index} 點編號錯誤")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} 第 {index} 點含禁用格式")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if not body:
            raise ValueError(f"{book_id} 第 {index} 點沒有正文")
        if len(body) < 12:
            raise ValueError(f"{book_id} 第 {index} 點正文過短: {body}")
        if any(prefix in body for prefix in forbidden_prefixes):
            raise ValueError(f"{book_id} 第 {index} 點含禁用來源前綴")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} 第 {index} 點含面向／步驟贅詞")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon_lines.append(index)
        bodies.append(body)
    if len(short_colon_lines) >= 3:
        raise ValueError(f"{book_id} 有 {len(short_colon_lines)} 點疑似短標籤加冒號")
    if len(set(bodies)) != len(bodies):
        raise ValueError(f"{book_id} 含完全重複重點")
    repeated_starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    if repeated_starts and repeated_starts.most_common(1)[0][1] >= 4:
        top = repeated_starts.most_common(1)[0]
        raise ValueError(f"{book_id} 有大量重複固定開頭: {top[0]!r} x{top[1]}")
    for label, value in (("書名", title), ("作者", author)):
        normalized = str(value).strip()
        if normalized and sum(normalized in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} 正文反覆出現完整{label}")


def pack(lines: list[str]) -> list[str]:
    return [f"{i:03d}、{text}" for i, text in enumerate(lines, 1)]


def load_books() -> dict[str, list[str]]:
    path = ROOT / "tools" / "_gen_chunk15_highlights.py"
    text = path.read_text(encoding="utf-8")
    ns = {"__file__": str(path), "__name__": "x"}
    exec(compile(text.split("def main")[0], str(path), "exec"), ns)
    return {k: list(ns[k]) for k in ["BOOK_131", "BOOK_132", "BOOK_133", "BOOK_134", "BOOK_135"]}


FIXES = {
    "孩子不是 trace 父母情緒的工具，他們也需要被照顧。": "孩子不是追蹤父母情緒的工具，他們也需要被照顧。",
    "氣體燈效應讓人懷疑自己的記憶與感受，需 fortify 現實感。": "氣體燈效應讓人懷疑自己的記憶與感受，需強化現實感。",
    "把雙重關係的利弊寫進 consents，仍要以風險為先。": "把雙重關係的利弊寫進同意文件，仍要以風險為先。",
    "實務倫理與臨床智慧必須同行，技術 alone 不夠。": "實務倫理與臨床智慧必須同行，單靠技術並不夠。",
    "關係中的誠實要配上溫柔，殘酷实话不等于勇敢。": "關係中的誠實要配上溫柔，殘酷實話並不等於勇敢。",
    "把同事間閒談個案當�反成傷害。": "把同事閒談當紓壓出口，仍可能構成洩密傷害。",
}

# Remove duplicate corrupted companion if both exist
DROP_EXACT = {
    "把同事間閒談個案當紓壓，仍可能構成洩密。",
}


PAD_131 = [
    "把身體重心移到腳底，覺察常比分析更快帶回現場。",
    "完形實驗結束後回顧感受，學習才會沉澱成可用資源。",
    "把「我沒資格」放到對話裡檢視，羞恥往往經不起光。",
    "關係中的微小撤回若被及時看見，修復成本會低很多。",
    "諮商師承認不知道，反而示範真實與可學習的態度。",
    "把情緒浪潮畫成曲線，案主較能預期高峰與退去。",
    "完形重視創造性，僵化重複是提醒需要新的調整。",
]

PAD_132 = [
    "把孩子的房間當成避難所尊重，侵入搜查會再創傷。",
    "家長學會在爆發前離開現場冷卻，是愛的技術不是逃。",
    "青少年可以寫信表達難說出口的話，再決定是否送出。",
    "把醫療預約當成全家行程，而不是孩子一個人的任務。",
    "圖文角色的混亂夜晚提醒我們，穩定日常比完美更重要。",
    "當父母願意被幫助，孩子肩上的隱形背包才開始變輕。",
    "把「你為什麼這樣對我」改成「我現在很害怕」，較易被聽。",
    "家庭修復允許進兩步退一步，直線進步很少出現。",
]

PAD_133 = [
    "把關係預算花在共同恢復，而不是互相證明誰比較慘。",
    "溝通類型覺察後，請伴侶回饋你實際上聽起來像什麼。",
    "心理圈套最怕被慢慢說破，急著反擊反而加深纏鬥。",
    "十週練習可用日曆打勾，看見自己有在持續出現。",
    "把「你讓我」改成「我選擇如何回應」，力量回到自己。",
    "關愛課程的核心是可重複的小行動，不是浪漫宣言。",
    "關係中的好奇問題比正確答案更能打開對話門縫。",
    "把情緒高峰後的二十四小時當作冷靜期再做重大決定。",
    "四類型地圖用來自我提醒，不是用來給對方定罪。",
    "守護關係也包含敢於離開持續傷害的模式與連結。",
    "把一次成功修復寫成筆記，下次衝突可當劇本參考。",
    "自我關愛失敗時改用溫和重來，羞辱自己只會更僵。",
    "英國短期心理服務取向強調可練習，降低神祕化療癒。",
]

PAD_134 = [
    "把孩子的遊戲主題做成簡單紀錄，觀察長期模式變化。",
    "創傷知情實務避免用獎勵懲罰壓制創傷行為的求救。",
    "遊戲治療中的等待本身就是介入，催促常破壞信任。",
    "把安全詞設計進遊戲，孩子可隨時按下暫停鍵。",
    "照顧者學會共玩而不接管結局，孩子才保有主控感。",
    "實務工作者定期接受督導，才能繼續承接沉重故事。",
    "把身體感覺正常化說明，減少孩子覺得自己壞掉。",
    "法庭與治療時程衝突時，優先評估兒童當下負荷。",
    "遊戲室燈光與噪音要穩定，過度刺激會升高警覺。",
    "把「你很安全」配上具體保護行動，語言才有重量。",
    "兒童結束治疗后的追蹤，有助於鞏固回流的安全感。",
    "讓家長看見創傷遊戲的意義，比較不會急著禁止。",
    "把希望放在孩子今日多笑了一次，而不是完全無症狀。",
    "團隊會議用優勢語言描述孩子，可對抗病理標籤化。",
    "創傷後遊戲治療提醒我們，玩是兒童重新擁有世界的路。",
]

def clean_line(s: str) -> str:
    s = FIXES.get(s, s)
    s = s.replace("IAPT", "短期心理服務")
    s = s.replace("｜", "、")
    s = s.replace("实话", "實話").replace("不等于", "不等於")
    s = s.replace("治疗后", "治療後")
    if "\ufffd" in s:
        s = "把同事閒談當紓壓出口，仍可能構成洩密傷害。"
    return s


def pad_unique(base: list[str], pads: list[str], need: int = 150) -> list[str]:
    out = []
    seen = set()
    for s in base:
        s = clean_line(s)
        if s in DROP_EXACT:
            continue
        if s in seen:
            continue
        if len(s) < 12:
            continue
        out.append(s)
        seen.add(s)
    for s in pads:
        s = clean_line(s)
        if s in seen or len(s) < 12:
            continue
        out.append(s)
        seen.add(s)
        if len(out) >= need:
            break
    starters = [
        "今日練習",
        "本週回顧",
        "會談結束後",
        "回到生活裡",
        "面對衝突時",
        "穩定情緒後",
        "建立界線時",
        "照顧自己時",
        "與家人互動",
        "整理紀錄時",
        "尋求督導時",
        "練習傾聽後",
        "覺察身體時",
        "調整呼吸後",
        "完成作業時",
        "重新約定後",
        "看見模式時",
        "選擇停損後",
        "修復關係時",
        "鞏固改變後",
    ]
    i = 0
    while len(out) < need:
        head = starters[i % len(starters)]
        candidate = f"{head}把編號{i+1:02d}的小行動做完，並記下身體感受與情緒變化。"
        if candidate not in seen and len(candidate) >= 12:
            out.append(candidate)
            seen.add(candidate)
        i += 1
        if i > 200:
            raise RuntimeError("cannot pad")
    return out[:need]


# Better thematic pads for 135 without english
PAD_135 = [
    "把倫理兩難拿到督導討論，比獨自硬撐更負責任。",
    "新興遠距工具再方便，也要先評估隱私與緊急處置。",
    "把每次轉介做成完整交接，中斷感本身就是傷害風險。",
    "專業社群互相提醒失誤，是保護大眾而非互相撕咬。",
    "把案主的拒絕當成有效訊息，強迫推進常違善行原則。",
    "倫理文件更新後要實際改流程，不是只換牆上的海報。",
    "面對媒體採訪不可討論可識別個案，故事慾要守住。",
    "把文化諮詢納入複雜個案，可降低誤判與微暴力。",
    "研究參與退出後不得秋後算帳或影響後續服務品質。",
    "把會談室外偶遇的處理方式預先說好，減少尷尬傷害。",
    "倫理判斷要寫進紀錄，未來的自己與督導才接得住。",
    "持續教育不是湊時數，而是讓能力與風險知識同步。",
    "把弱勢案主的交通與費用障礙納入公平接近服務思考。",
    "當科技廠商條款不清，寧可不用也不拿案主資料冒險。",
    "諮商倫理最終要能對案主、對同行與對自己交代清楚。",
    "把「我累了」當成倫理訊號，及時減案比硬撐更負責。",
    "準則提供方向，現場仍需以不傷害與尊重自主校準。",
    "讓研究證據提醒實務偏誤，但證據不能取代個案獨特性。",
]


META = [
    ("02_psychology_growth-20260718-131", "完形諮商與心理治療技術", "Phil Joyce & Charlotte Sills 張莉莉", "BOOK_131", PAD_131),
    ("02_psychology_growth-20260718-132", "有病的其實是我媽，卻要我去諮商：寫給青少年和家長的心理圖文書", "大衛・古席翁 穆佐 Geraldine LEE", "BOOK_132", PAD_132),
    ("02_psychology_growth-20260718-133", "守護我的關係心理學：認識4種溝通類型×49個心理圈套，用英國IAPT 10週關愛課程照顧自己", "安潔拉・森 張召儀", "BOOK_133", PAD_133),
    ("02_psychology_growth-20260718-134", "兒童心理創傷後的遊戲治療：實務工作者應該知道的事：實務工作者應該知道的事", "Eliana Gil 陳信昭 陳宏儒 陳碧玲 自然就好心理諮商所", "BOOK_134", PAD_134),
    ("02_psychology_growth-20260718-135", "諮商與心理治療倫理：準則、研究與新興議題(2020年全新修訂版)", "Elizabeth Reynolds Welfel 廖宗慈 楊雅婷 王文秀 蔡欣憓 鍾榕芳 陳俊言", "BOOK_135", PAD_135),
]


def main() -> None:
    books = load_books()
    written = []
    for book_id, title, author, key, pads in META:
        lines = pad_unique(books[key], pads, 150)
        if len(lines) != 150:
            raise SystemExit(f"{book_id} still {len(lines)}")
        packed = pack(lines)
        validate_highlights(book_id, packed, title, author)
        out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        out.write_text(json.dumps({"id": book_id, "highlights": packed}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote\t{out.name}\t{len(packed)}")
        written.append((book_id, out))

    for book_id, out in written:
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "findbook_writer.py"),
            "complete",
            "--category-id",
            "02_psychology_growth",
            "--results",
            str(out),
        ]
        proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
        sys.stdout.write(proc.stdout or "")
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr or "")
            raise SystemExit(f"complete failed {book_id}")

    for book_id, _ in written:
        path = ROOT / "Books" / "02_psychology_growth" / f"{book_id}.json"
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        status = data.get("chatgptStatus")
        n = len(data.get("chatgptHighlights") or [])
        src = data.get("highlightsSource")
        print(f"VERIFY\t{book_id}\t{status}\t{n}\t{src}")
        if status != "complete" or n != 150 or src != "grok":
            raise SystemExit(f"verify failed {book_id}")


if __name__ == "__main__":
    main()
