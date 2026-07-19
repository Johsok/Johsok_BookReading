# -*- coding: utf-8 -*-
"""Pad chunk10 highlight lists to 150 and fix simplified chars."""
from __future__ import annotations

import ast
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent / "_gen_chunk10_highlights.py"

EXTRA = {
    "H106": [
        "把一天中最安穩的時刻標註下來，那就是你最適合練習的窗口。",
        "若坐著時腳麻到受不了，改成跪坐或椅坐，覺知仍然成立。",
        "練習結束對自己說一句謝謝，感謝願意停下的那份勇氣。",
    ],
    "H107": [
        "把哀傷日記鎖起來也可以，隱私是你給傷口的繃帶。",
        "有些歌暫時不要聽，等心比較穩再讓旋律回來。",
        "搬家後第一個夜晚特別空，開盞暖燈能降低陌生感。",
        "收到對方以前的信件時，允許停工十分鐘好好讀完。",
        "把「我要堅強」改成「我要誠實」，誠實比較扛得久。",
        "朋友邀約若你能量不夠，改約短聚比勉強長局更好。",
        "季節轉換時舊痛易醒，提前安排溫和行程當作防波堤。",
        "若突然很想大掃除，慢一點做，激進整理也會激起情緒。",
        "你仍配得上被安慰，即使你覺得自己早該好了。",
    ],
    "H108": [
        "把討好當成舊軟體，更新前先備份你真正在意的價值。",
        "價值清單貼在手機備忘，臨場猶豫時打開看一眼。",
        "一眼就夠提醒：你不是來贏人緣競賽的。",
        "人緣競賽的獎盃常常是透支後的空殼稱讚。",
        "空殼稱讚退回，換真實回饋，成長反而加快。",
        "加快成長不靠更乖，靠更清楚的自我定位。",
        "定位清楚後，該靠近與該疏遠的人會自動分列。",
        "分列完成，日子少了很多隱形表演。",
        "少表演後你會更累也更醒，醒是好的副作用。",
        "副作用退去，留下的是可呼吸的人際距離。",
        "距離不是冷漠，是讓善意可以自願流動。",
        "自願的善意比較香，強迫的乖巧比較苦。",
        "苦味出現就檢查：我是否又在用討好換短暫安全。",
        "檢查完做一次小修正，勇氣就是這樣疊起來的。",
    ],
    "H109": [
        "把衣櫃顏色減到三主色，搭配決策會瞬間變輕。",
        "郵件一天只回兩次，即時回覆成癮會吃掉深度時間。",
        "深度時間留給創作或思考，簡單感常從這裡回來。",
        "回來後別急著塞滿，留白要像存錢一樣被保護。",
        "保護留白的句子可以是：這段我已有安排。",
        "安排可以是發呆，發呆也是合法行程。",
        "合法行程被質疑時，不必過度證明休息的正當性。",
        "正當性來自你可持續運作，而非他人點頭。",
        "他人點頭是加分，自體許可才是基礎建設。",
        "基礎建設好了，突發麻煩比較推不倒你。",
        "推不倒的感覺，會讓煩惱自動失去誇大戲服。",
        "戲服脫下，問題回到原始尺寸就好處理。",
        "好處理的關鍵是一次只碰一層，不貪心全拆。",
        "全拆容易再複雜化，微調哲學就是反其道。",
        "反其道而行幾週後，你會懷念以前為何把自己逼那麼緊。",
        "懷念過後微笑就好，然後繼續用小步把日子調準。",
        "調準不是一次完成，是一生可更新的練習。",
    ],
    "H110": [
        "把夢想生活的月費算出來，目標才從霧變成可射擊靶。",
        "靶心清楚後，每日行動用靠近或偏離來快速校正。",
        "校正時允許慢月，慢月不是失敗而是節奏的一部分。",
        "節奏穩定的人比較能撐過市場與情緒的雙重波動。",
        "波動來時重讀覺察日記，看自己又掉進哪條舊信念。",
        "舊信念被點名後威力下降，新選擇空間就出現。",
        "空間出現就放入一個小實驗，讓轉富保持在移動中。",
    ],
}


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    repls = {
        "写成": "寫成",
        "迈出": "邁出",
        "抽屉": "抽屜",
        "降温": "降溫",
        "难收的话": "難收的話",
        "兑现": "兌現",
        "含义": "含義",
        "复盘": "復盤",
        "说清你解决谁的什么痛": "說清你解決誰的什麼痛",
        "不要紧": "不要緊",
        "连环崩盤": "連環崩盤",
    }
    for a, b in repls.items():
        text = text.replace(a, b)

    for name, extras in EXTRA.items():
        # insert extras before the closing of each list: find `]\n\n# ---` or similar after name
        pattern = rf"({name}\s*=\s*\[)(.*?)(\n\])"
        m = re.search(pattern, text, flags=re.S)
        if not m:
            raise SystemExit(f"cannot find {name}")
        body = m.group(2)
        # count existing
        existing = ast.literal_eval("[" + body + "]")
        need = 150 - len(existing)
        if need < 0:
            raise SystemExit(f"{name} already {len(existing)}")
        add = extras[:need]
        if len(add) < need:
            raise SystemExit(f"{name} need {need} extras have {len(add)}")
        insert = "".join(f'\n    "{line}",' for line in add)
        # insert before closing ]
        text = text[: m.end(2)] + insert + text[m.end(2) :]

    SRC.write_text(text, encoding="utf-8")

    # verify
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.startswith("H"):
                    if isinstance(node.value, ast.List):
                        print(t.id, len(node.value.elts))


if __name__ == "__main__":
    main()
