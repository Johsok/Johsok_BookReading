# -*- coding: utf-8 -*-
"""Accept remaining unique classics from later ranks of 讀冊 yearly lists."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402

FROM_DATE = "1986-09-15"
TO_DATE = "2024-09-15"
OUT = ROOT / "tools/.findbook_candidates_findbook-20260915-1211.json"
payload = json.loads(OUT.read_text(encoding="utf-8"))
existing = s.load_existing_keys(ROOT)
seen = {cat: set() for cat in payload}
for cat, items in payload.items():
    for item in items:
        seen[cat].add(s.normalized_key(item["title"], item["author"]))


def need(cat: str) -> int:
    return 6 - len(payload.get(cat, []))


def take(cat: str, title: str, author: str, prod_id: str, published: str, source_name: str) -> bool:
    if need(cat) <= 0:
        return False
    raw = {
        "title": title,
        "author": author,
        "sourceUrl": f"https://www.taaze.tw/products/{prod_id}.html",
        "published": published,
        "sourceSite": "讀冊",
        "sourceName": source_name,
    }
    key = s._accept_item(raw, existing, seen[cat], FROM_DATE, TO_DATE, cat)
    if not key:
        return False
    seen[cat].add(key)
    payload.setdefault(cat, []).append(s.to_candidate(raw, cat, FROM_DATE, TO_DATE))
    print("+", cat, title[:42])
    return True


PSY = "02_psychology_growth"
BIZ = "01_business_startup"
PSY_SRC = "讀冊－心理勵志2013暢銷百大"
BIZ_SRC = "讀冊－商業2011暢銷百大"

rows = [
    (PSY, "《深夜加油站遇見蘇格拉底》【全新修訂版】", "丹．米爾曼", "11100979479", "2022-04-08", PSY_SRC),
    (PSY, "心靈女戰士：快樂女人覺醒六法", "央金拉姆", "11100644093", "2013-01-31", PSY_SRC),
    (PSY, "焦慮是戒得掉的：不再自己嚇自己的四個練習", "塔瑪．強斯基", "11100638536", "2012-12-15", PSY_SRC),
    (PSY, "做自己，還是做罐頭？勇敢挺自己的第一堂課", "黃士鈞（哈克）", "11100636591", "2012-11-30", PSY_SRC),
    (PSY, "不為小事抓狂的50個練習：大腦決定你的「度量」，增加「腦容量」，脾氣一定會變好", "西多昌規", "11100640831", "2013-01-03", PSY_SRC),
    (PSY, "穿越夢境，遇見最真實的自己", "王榮義", "11100635250", "2012-11-05", PSY_SRC),
    (PSY, "松浦彌太郎的100個基本", "松浦彌太郎", "11100779966", "2016-04-11", PSY_SRC),
    (PSY, "不生氣的技術（暢銷紀念版）", "嶋津良智", "11100835966", "2018-01-20", PSY_SRC),
    (PSY, "搜尋你內心的關鍵字：Google最熱門的自我成長課程！幫助你創造健康、快樂、成功的人生，在工作、生活上脫胎換骨！", "陳一鳴", "11100655800", "2013-05-27", PSY_SRC),
    (PSY, "毒型人物：毀掉你美好人生的13種人際毒害", "貝納鐸‧史達馬提亞斯", "11100662432", "2013-07-25", PSY_SRC),
    (PSY, "心靈能量：藏在身體裡的大智慧", "大衛．霍金斯", "11100615372", "2012-06-25", PSY_SRC),
    (PSY, "說話，其實也能套公式：一開口就能說到重點，百分百提升好感、達成目標", "李飛彤、廖翊君", "11100636594", "2012-11-30", PSY_SRC),
    (PSY, "回家：與父母的關係，決定你與幸福的距離", "賴佩霞、郭貞伶", "11100898721", "2020-01-20", PSY_SRC),
    (PSY, "30堂帶來幸福的思辨課：多想一點，發現更有深度的自己", "琳達．艾爾德、理察．保羅", "11101000216", "2023-01-07", PSY_SRC),
    (PSY, "和好：療癒你的內在小孩（三版）", "一行禪師", "11100897952", "2020-01-22", PSY_SRC),
    (PSY, "傾聽，不可思議的力量：學會諮商師的聽話術，你和別人都受益", "東山紈久", "11100647545", "2013-02-26", PSY_SRC),
    (PSY, "魅力學：無往不利的自我經營術（新版）", "奧麗薇亞．福克斯．卡本尼", "11100833730", "2017-12-12", PSY_SRC),
    (PSY, "法國女人寫給女人的３０天愛自己計劃", "奧莉薇亞‧圖佳", "11100618459", "2012-07-04", PSY_SRC),
    (PSY, "最後14堂星期二的課（20週年紀念版）", "米奇‧艾爾邦", "11100848737", "2018-06-27", PSY_SRC),
    (PSY, "空出位子給幸福！逆轉人生的空間診斷術：你的房間，就是你的人生", "埃克索榮．貝比斯", "11100639694", "2012-12-12", PSY_SRC),
    (PSY, "The Power力量", "朗達‧拜恩", "11100513133", "2011-03-29", PSY_SRC),
    (PSY, "擁抱不完美：認回自己的故事療癒之旅", "周志建", "11100665273", "2013-08-01", PSY_SRC),
    (PSY, "失落的幸福經典－影響千萬人的生命法則", "佛羅倫絲‧辛", "11100202907", "2010-02-25", PSY_SRC),
    (PSY, "在天堂遇見的五個人", "米奇．艾爾邦", "11100177891", "2004-11-01", PSY_SRC),
    (PSY, "一個人的療癒（暢銷45年經典版）：真正的放下，是你不介意再度提起", "約翰．詹姆斯、羅素．傅里曼", "11100969414", "2021-12-01", PSY_SRC),
    (PSY, "比打工度假更重要的11件事：出國前先給自己這份人生問卷", "褚士瑩", "11100665247", "2013-07-29", PSY_SRC),
    (PSY, "這樣學習改變了我（勵志版）", "齋藤孝", "11100924950", "2020-12-12", PSY_SRC),
    (PSY, "丟掉50個壞習慣，懶熊也能訂做成功新生活！【暢銷五週年版】", "美崎榮一郎", "11100806098", "2017-02-05", PSY_SRC),
    (PSY, "故事的療癒力量：敘事、隱喻、自由書寫", "周志建", "11100628573", "2012-09-10", PSY_SRC),
    (BIZ, "15分鐘聊出好交情：66個開場、提問、接話的超級說話術", "野口 敏", "11100433512", "2011-01-25", BIZ_SRC),
    (BIZ, "影響力：讓人乖乖聽話的說服術（全新增訂版）", "羅勃特．席爾迪尼", "11100981634", "2022-05-06", BIZ_SRC),
    (BIZ, "找到你的工作好感覺：松浦彌太郎の舒服工作術", "松浦彌太郎", "11100571649", "2011-07-21", BIZ_SRC),
    (BIZ, "世界地圖就是你的財富版圖：掌握國際觀，獲利更可觀", "劉必榮、林志昊", "11100564779", "2011-05-31", BIZ_SRC),
    (BIZ, "魔球：逆境中致勝的智慧（經典新版）", "麥可．路易士", "11100717788", "2014-09-05", BIZ_SRC),
    (BIZ, "擁抱初衷", "嚴心鏞", "11100248464", "2010-10-26", BIZ_SRC),
    (BIZ, "20幾歲，就定位（2）：邁向成功的人際關係法則", "水湄", "11100252614", "2010-11-29", BIZ_SRC),
    (BIZ, "勇往直前：我如何拯救星巴克", "霍華．舒茲、瓊安．戈登", "11100563079", "2011-04-26", BIZ_SRC),
    (BIZ, "這樣思考，人生就不一樣早知道該多好的", "外山滋比古", "11100209998", "2009-10-29", BIZ_SRC),
    (BIZ, "賈伯斯憑什麼領導世界：我在蘋果的近身觀察與體悟", "杰伊．艾略特、威廉．賽蒙", "11100576698", "2011-08-25", BIZ_SRC),
    (BIZ, "筆記女王的手帳活用術：全彩圖解 工作、生活、理財、時間管理一本通", "筆記女王Ada", "11100203160", "2010-01-13", BIZ_SRC),
    (BIZ, "大家來看賈伯斯：向蘋果的表演大師學簡報", "卡曼．蓋洛", "11100199956", "2010-03-03", BIZ_SRC),
    (BIZ, "創意CEO：行銷、廣告、媒體、設計的創意管理", "馬里奧．普瑞肯", "11100563298", "2011-04-28", BIZ_SRC),
    (BIZ, "成功者的筆記本都記些什麼？", "美崎榮一郎", "11100249285", "2010-11-30", BIZ_SRC),
    (BIZ, "卡內基成功學經典：人性的弱點（典藏精裝版）", "戴爾‧卡內基", "11100638586", "2012-11-30", BIZ_SRC),
    (BIZ, "民國100年大泡沫：財富即將重分配，央行沒告訴你的真相", "王伯達", "11100243255", "2010-09-24", BIZ_SRC),
    (BIZ, "美元圈套：全球經濟大逆轉，如何創富與避險", "王伯達", "11100568292", "2011-06-30", BIZ_SRC),
    (BIZ, "這些事等老闆來教，學費很貴！－ 35歲前一定要養成的10種工作習慣", "重茂　達", "11100228970", "2010-06-29", BIZ_SRC),
]

for row in rows:
    take(*row)

print("COUNTS", {c: len(v) for c, v in payload.items()})
for cat in [BIZ, PSY, "03_natural_science", "04_healthcare"]:
    print("---", cat, len(payload[cat]))
    for item in payload[cat]:
        print(" ", item["title"][:36], "|", item["author"][:18])
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
