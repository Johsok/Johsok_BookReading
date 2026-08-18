# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).with_name("_write_hl_57_58.py")
text = p.read_text(encoding="utf-8")
marker = "何首烏塊根有異常維管束雲紋"
idx = text.find(marker)
if idx < 0:
    raise SystemExit("marker not found")
head = text[:idx]

rest = r'''何首烏塊根橫切可見雲紋，藤本葉心形，把直立灌木根畫上去會生活型全錯。",
    "夜交藤是同一植物的莖，與塊根不同器官，畫面若只有葉，就沒有標明用哪一段。",
    "地黃葉基生皺縮，花筒狀，根肥厚，鮮時與蒸製後的顏色差無法從一張鮮株圖讀出。",
    "玄參莖方形、根乾後內部色深，只畫紫花穗會跟別的玄參科混。",
    "牡丹皮取根皮，畫面若只給牡丹花，就停在觀賞層而不是藥用層。",
    "麥冬葉叢生線形，塊根紡錘狀成串，只畫葉叢會以為是禾草。",
    "天冬的葉狀枝成刺，塊根成串，把寬葉百合根套上去會科錯。",
    "玉竹根莖有環節，黃精根莖更粗壯，兩者平行脈葉極像，花序位置才比較能拆。",
    "石斛莖節明顯，氣生根附樹，畫成地生蘭會棲地錯。",
    "遠志葉小互生，根皮與木心可分離，只畫小紫花就沒有根的筒狀資訊。",
    "酸棗枝有刺、核果紅熟，入藥常取種仁，把果肉當主體是部位顛倒。",
    "五味子藤本、漿果成穗，葉緣有腺齒，把直立木本漿果畫上去會屬錯。",
    "枸杞枝常有刺、漿果橙紅，根皮另作地骨皮，同一株兩種器官不能畫成同一塊。",
    "山藥是地下塊莖，地上零餘子是珠芽，只畫藤葉會漏掉兩個可採收部位。",
    "茯苓是菌核，依附松根，畫成普通塊根植物會界級全錯。",
    "靈芝菌蓋有漆樣光澤與輪紋，把葉子畫到菌蓋上就把真菌當種子植物。",
    "桔梗花冠鐘狀五裂，根長圓柱，沙參類近緣要靠花與葉毛才能分開。",
    "南沙參與北沙參連科都可能不同，只畫一把白根綠葉會讓對照表失效。",
    "貝母鱗莖由肥厚鱗葉組成，地上葉序隨種而異，把洋蔥圓球套上去會科錯。",
    "半夏塊莖球形，葉形隨年齡從心形到三出，只畫成株三出葉會漏掉幼期。",
    "天南星佛焰苞與肉穗花序是科徵，塊莖毒性不能從綠色掌狀葉讀出。",
    "細辛花貼地鐘狀，葉心形，把大型馬兜鈴花套上去會屬級錯。",
    "麻黃莖綠色具節，葉退化成鞘，把普通草葉畫上去就不是這屬。",
    "蒼耳瘦果包在鉤刺總苞裡，這套傳播構造比黃花更重要。",
    "辛夷是木蘭科花蕾，必須畫出苞片與未開花蕾，盛開花不是同一採收狀態。",
    "澤瀉葉基生，塊莖球形，花序分枝輪生，畫成慈姑箭形葉會近緣混淆。",
    "豬苓是菌核，表面凹凸，畫成光滑薯類就界錯。",
    "金錢草葉對生圓形，與廣金錢草的豆科三出葉在圖上必須分開，同名不能同形。",
    "海金沙入藥常取孢子，必須畫孢子囊穗，只畫營養葉會漏掉真正採收物。",
    "石韋葉背有孢子囊群，若把孢子囊畫成蟲卵，鑑定會跨界。",
    "瞿麥萼筒長、花瓣先端齒裂，萹蓄節間有白色托葉鞘，兩種在圖上結構不同。",
    "木通果實肉質漿果成串，與馬兜鈴藤的花形必須分開畫，否則毒與非毒會被同名綁在一起。",
    "板藍根是菘藍的根，大青葉是葉，同一物種兩器官，畫面要標出用的是哪一層。",
    "青黛是加工產物，圖只能畫植物原料，不能畫出粉末色素。",
    "女貞葉革質對生、核果黑藍，旱蓮草是草本菊科，兩種在形態上毫無相似。",
    "菟絲子無綠葉，全株寄生纏繞，畫成有真葉的藤本就生態全錯。",
    "覆盆子聚合核果與皮刺是薔薇科線索，把無刺漿果灌木套上去會科錯。",
    "澤蘭是菊科頭狀花序，佩蘭常被混稱，頭狀花序與唇形花不能畫成同一株。",
    "前胡繖形花序與複葉裂片要把白花前胡與紫花前胡分開，單色渲染做不到。",
    "款冬花先葉開放，採收常在花期，畫成葉花同株盛開會物候錯。",
    "紫菀根有須，頭狀花序舌狀花紫，把黃花旋覆花的根套上去會種錯。",
    "百部塊根成紡錘串，葉輪生或對生隨種而異，把單條直根畫上去會部位簡化過度。",
    "苦杏仁與甜杏仁在圖上幾乎同形，含氰苷與否讀不出來。",
    "採收根類常在秋冬地上部枯萎後，畫面若滿是盛花，就不是典型採根當下。",
    "葉類藥常在花前或盛葉期採，把殘花敗葉當葉藥標準株會物候相反。",
    "花類藥要標開綻程度，花蕾、初開與全開不是同一張鑑定圖能混用。",
    "果類藥要標成熟度，青果與熟果的皺紋、宿萼與種子數都會變。",
    "皮類藥要畫喬木或灌木的皮孔與韌皮層，草本莖皮代替不了。",
    "全草入藥必須包含花果與根的相對比例，只截一段嫩梢會讓近緣種無法核對。",
    "近緣種混淆往往發生在花未開、果未結的營養期，所以缺花果的圖風險最高。",
    "本草條目常沿用舊名，圖上的葉序若與現行分類衝突，應以形態為準去回查異名。",
    "轉繪會把甲地植物的花安到乙地植物的根上，形成文獻裡不存在的嵌合體。",
    "工筆設色追求好看時，會把有毒乳汁畫成透明無物，警戒資訊就被美學刪除。",
    "繪圖是給形態核對用的輔助，不能替代藥典、鑑定與臨床決策。",
    "把古方煎煮法寫進讀圖筆記，容易把觀察記錄誤當成可執行的現代醫療建議。",
    "科學讀圖先問這是哪個器官、哪個物候、哪一類近緣風險，而不是先問能治什麼。",
]

BANNED = (
    "金石昆蟲草木狀",
    "動物篇",
    "藥草篇",
    "文俶",
    "本書",
    "作者",
    "第1章",
    "第一章",
    "本章",
    "第2章",
    "第二章",
)


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    seen = set()
    out = []
    for i, t in enumerate(items, 1):
        t = t.strip()
        if t.startswith(f"{i:03d}、"):
            key = t.split("、", 1)[1]
            body = t
        else:
            key = t
            body = f"{i:03d}、{t}"
        if key in seen:
            raise SystemExit(f"duplicate {i}: {key[:40]}")
        seen.add(key)
        if len(key) < 12:
            raise SystemExit(f"short {i}: {key}")
        if "：" in key or ":" in key:
            raise SystemExit(f"colon {i}: {key}")
        for b in BANNED:
            if b in key:
                raise SystemExit(f"banned {b} in {i}")
        out.append(body)
    prefixes = {}
    for i, s in enumerate(out, 1):
        prefixes.setdefault(s[4:22], []).append(i)
    bad = {k: v for k, v in prefixes.items() if len(v) >= 4}
    if bad:
        raise SystemExit(f"same prefix x4+: {bad}")
    return out


def patch(filename, items, summary):
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    data["summary"] = summary
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(data['chatgptHighlights'])} summary={data['summary']}")


def main():
    jobs = [
        (
            "03_natural_science-20260716-57.json",
            ITEMS_57,
            "整理草蟲魚鳥走獸的形態比例、鱗羽斑紋、停棲姿態與配景關係，並標出標本、轉繪與學名對照的觀察限度。",
        ),
        (
            "03_natural_science-20260716-58.json",
            ITEMS_58,
            "整理藥用植物根莖葉花果如何入畫，區分形態鑑定、物候、毒性與本草記載，並避免把古方當成現代處方。",
        ),
    ]
    for fn, items, summary in jobs:
        patch(fn, items, summary)


if __name__ == "__main__":
    main()
'''

p.write_text(head + rest, encoding="utf-8")
print("patched", p, "chars", p.stat().st_size)
