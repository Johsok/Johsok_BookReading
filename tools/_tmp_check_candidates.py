# -*- coding: utf-8 -*-
"""Match candidate titles against existing data.json keys."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def title_key(title: str) -> str:
    value = unicodedata.normalize("NFKC", title).casefold()
    return PUNCT.sub("", value)


CANDIDATES = {
    "01_business_startup": [
        ("花錢的藝術：打造富足人生的金錢心理學", "摩根．豪瑟", "2026-07-27"),
        ("高薪賽道：選擇比努力重要！走對路徑的職場換軌與談薪心法", "抹布（Moboo）", "2026-07-31"),
        ("你不是不夠好，只是站錯了位置：找到對的定位，不再耗損、不必硬撐，活出真正自我成就的人生", "陳世明", "2026-08-08"),
        ("致富思維——不是你不夠努力，而是一直用錯方法在賺錢；生命不能重來，但思維可以重新彩排！", "董耀慶（Max）、周君樺（Ginger）", "2026-08-06"),
        ("微實驗：透過微小的嘗試，探索人生的無限可能", "安蘿爾．勒坎弗", "2026-08-07"),
        ("才賦自由：打造選擇權，實踐屬於你的成就樣貌", "黃瑞仁", "2026-08-01"),
        ("財富護城河：立足台股、接軌美股，打造散戶穿越牛熊的全球財富系統", "施雅棠", "2026-07-28"),
        ("大怒神來了：川普關稅風暴與台灣的地緣經濟時刻", "洪財隆", "2026-07-29"),
        ("你的人生需要新收入！：25堂揭露財富和人生真相的商業洞察課，用51分的勇氣，專心快樂發展自己！", "錢婧", "2026-08-12"),
        ("走出金錢焦慮：理解現實真相，真正消除不安", "田內學", "2026-08-01"),
    ],
    "02_psychology_growth": [
        ("留白：少即是富，活出成熟大人的餘裕", "橫田真由子", "2026-08-18"),
        ("我們都有小憂鬱：作者親身實測!利用療鬱象限圖的33種情緒解方，找回失去的快樂與活力", "Hossy", "2026-08-18"),
        ("菇蛙小姐的不用力生活練習1+2【套書】", "梅貝兒．伊奎", "2026-08-17"),
        ("創作之路：通往更高創造力的靈性道路", "茱莉亞．卡麥隆", "2026-08-15"),
        ("戀愛課金：不管付出多大代價，永遠不要對愛失去信心", "洪培芸", "2026-08-14"),
        ("我在生命終點站上班：真正需要被安放的，其實是留下來的人", "丸編（王威）", "2026-08-13"),
        ("你的人生，可以活在答案之外：韓國百萬學子信賴的「讀書之神」寫給迷惘世代──如何用學習打造人生選擇權", "姜聲泰", "2026-08-12"),
        ("自我批評也是愛，但不是我們要的愛：一步一步克服自我懷疑，接納你就是你的美好和信心", "戴蒙．札哈里斯", "2026-08-12"),
        ("心流WORKBOOK【實踐本‧附練習步驟】：一套可訓練的高效專注系統", "韋因", "2026-08-12"),
        ("男人的四個原型：暢銷30年經典，榮格學派帶你剖析男性心理", "羅伯特・摩爾、道格拉斯・吉列特", "2026-08-12"),
        ("覺察之道：任何時候都能回到當下、降伏煩惱的8個修心練習", "藍獅子", "2026-08-12"),
        ("恐懼，是最好的教練：一位奧運冠軍關於失敗、改變、未知與重生的心理鍛鍊", "維多利亞・彭德爾頓", "2026-08-10"),
        ("讓自己休息的練習：拋開效率崇拜，東大急診名醫寫給焦慮世代的心靈指南", "矢作直樹", "2026-08-07"),
        ("惡意是怎麼形成的?：從霸凌、劈腿到仇恨言論，歷時15年、全球超過250萬筆研究數據，心理學家教你揪出身邊有問題的人!", "班雅明‧E‧席比", "2026-08-06"),
        ("大人系女子不必完美，也能活得閃閃發亮：125個告別內耗的微練習，找回「做自己」的底氣", "中島輝", "2026-08-05"),
    ],
    "03_natural_science": [
        ("困境使用說明書：關於失敗與擁抱未知，科學教我們的事", "卡蜜拉．彭", "2026-07-28"),
        ("藝數摺學2：20堂用指尖探索幾何規律的藝數美學課，從對稱全等到比例相似，動手體驗數學之用與藝術之美", "李政憲", "2026-08-06"),
        ("數學女孩：黎曼猜想", "結城浩", "2026-08-05"),
        ("別讓意識型態害了你：如何讓大腦靈活思考", "莉奧．茲米格羅德", "2026-07-29"),
        ("文明的原點：天文地理如何塑造人類歷史", "達奈爾", "2026-07-23"),
        ("看魚：台灣第一本河溪魚類水下踏查實錄", "周銘泰、李政霖", "2026-08-03"),
        ("氣候如何影響你的大腦？：減損認知、增加暴力傾向、引發創傷……高溫與動盪的氣候怎樣改寫我們的心智和大腦？", "克萊頓．艾登", "2026-07-30"),
        ("哺乳類王朝：從恐龍陰影下竄出的邊緣生物，如何接手稱霸地球？", "史提夫．布魯薩特", "2026-08-08"),
        ("蝴蝶誌：一部關於人類迷戀、收藏狂熱與蝴蝶生存的自然史", "蘿賽", "2026-08-08"),
        ("有一種田野報告叫植物獵人", "洪信介", "2026-07-30"),
    ],
}


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing_keys = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    existing_titles = {title_key(str(book.get("title", ""))) for book in manifest.get("books", [])}
    lines = []
    for category_id, items in CANDIDATES.items():
        lines.append(f"## {category_id}")
        new_count = 0
        for title, author, published in items:
            key = normalized_key(title, author)
            tkey = title_key(title)
            # also check prefix of title (before colon) against existing titles
            short = title.split("：")[0].split(":")[0]
            short_hit = any(title_key(short) in existing for existing in existing_titles)
            status = "NEW"
            if key in existing_keys or tkey in existing_titles or short_hit:
                status = "DUP"
            else:
                new_count += 1
            lines.append(f"{status}\t{published}\t{title}\t{author}")
        lines.append(f"new={new_count}")
        lines.append("")
    (ROOT / "tools" / ".candidate_check_20260818_2102.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
