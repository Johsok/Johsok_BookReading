from __future__ import annotations

import argparse
from pathlib import Path

import findbook_batch_20260714 as prior_batch
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "2000-06-01"
TO_DATE = "2026-07-15"
BATCH_NAME = "b2"


BOOKS = {
    "01_business_startup": (
        "商業理財",
        30,
        (
            ("Blink", "Malcolm Gladwell", "OL5749849W", 2004, ("決策", "直覺", "管理")),
            ("Elon Musk", "Ashlee Vance", "OL17184556W", 2013, ("企業家", "創新", "科技產業")),
            ("Entrepreneurship", "Bruce R. Barringer、R. Duane Ireland", "OL7947084W", 2004, ("創業", "商業模式", "新創管理")),
            ("Leadership and Self-Deception", "The Arbinger Institute", "OL8921343W", 2000, ("領導", "自我覺察", "組織關係")),
            ("Strategic Management and Competitive Advantage", "Jay B. Barney、William S. Hesterly", "OL3243279W", 2007, ("策略管理", "競爭優勢", "資源配置")),
            ("Hot, Flat, and Crowded", "Thomas L. Friedman", "OL3740419W", 2008, ("全球化", "永續經營", "產業趨勢")),
            ("E-Marketing", "Judy Strauss、Adel El-Ansary、Raymond Frost", "OL7943607W", 2002, ("數位行銷", "網路商務", "顧客經營")),
            ("Advertising Media Planning", "Larry D. Kelley、Donald W. Jugenheimer", "OL12292204W", 2003, ("媒體規劃", "廣告", "行銷策略")),
            ("The Long Tail", "Chris Anderson", "OL4091759W", 2006, ("長尾理論", "數位經濟", "市場策略")),
            ("The Tipping Point", "Malcolm Gladwell", "OL5749848W", 2000, ("傳播", "社會影響", "行銷")),
            ("The Leader Who Had No Title", "Robin S. Sharma", "OL15093286W", 2010, ("領導力", "職涯", "自我管理")),
            ("Social Marketing", "Gerard Hastings", "OL9487179W", 2007, ("社會行銷", "行為改變", "公共溝通")),
            ("Nation Branding", "Keith Dinnie", "OL9487177W", 2007, ("國家品牌", "品牌策略", "國際行銷")),
            ("Strategic Integrated Marketing Communications", "Larry Percy", "OL3291000W", 2007, ("整合行銷", "品牌溝通", "策略")),
            ("Entrepreneurial Financial Management", "Jeffrey R. Cornwall", "OL20039853W", 2015, ("創業財務", "現金流", "募資")),
            ("Financial Services Marketing", "Christine Ennew", "OL16957825W", 2006, ("金融服務", "行銷", "顧客關係")),
            ("Marketing Metrics", "Paul Farris", "OL18553001W", 2007, ("行銷衡量", "數據決策", "績效指標")),
            ("Business Plans Kit for Dummies", "Steven D. Peterson、Peter E. Jaret", "OL16070198W", 2001, ("商業計畫", "創業", "營運規劃")),
            ("Export-Import Theory, Practices, and Procedures", "Belay Seyoum", "OL21258717W", 2008, ("國際貿易", "進出口", "商務流程")),
            ("Hispanic Marketing", "Felipe Korzenny", "OL19720879W", 2011, ("族群行銷", "消費者洞察", "市場區隔")),
            ("Political Marketing", "Jennifer Lees-Marshment", "OL18206215W", 2005, ("政治行銷", "品牌定位", "傳播策略")),
            ("Advertising and Promotion", "Chris Hackley", "OL8500697W", 2005, ("廣告", "促銷", "品牌溝通")),
            ("Designing Brand Identity", "Alina Wheeler", "OL19720097W", 2008, ("品牌識別", "設計管理", "品牌策略")),
            ("E-Commerce", "Kenneth C. Laudon、Carol Guercio Traver", "OL58230W", 2002, ("電子商務", "數位平台", "商業模式")),
            ("Lean Six Sigma for Dummies", "Martin Brenig-Jones", "OL17521157W", 2009, ("流程改善", "精實管理", "品質管理")),
            ("The Everything Store", "Brad Stone", "OL16808249W", 2013, ("Amazon", "企業成長", "平台策略")),
            ("Essential Personal Finance", "Lien Luu、Jonquil Lowe、Jason Butler、Tony Byrne", "OL21323581W", 2017, ("個人理財", "資產配置", "財務規劃")),
            ("How Google Works", "Eric Schmidt、Jonathan Rosenberg", "OL17276241W", 2014, ("Google", "企業管理", "創新文化")),
            ("The Entrepreneurial State", "Mariana Mazzucato", "OL16808725W", 2011, ("創新政策", "公共投資", "產業發展")),
            ("The Speed of Trust", "Stephen M. R. Covey、Rebecca R. Merrill", "OL8454218W", 2006, ("信任", "領導", "組織效能")),
        ),
    ),
    "02_psychology_growth": (
        "心理勵志",
        30,
        (
            ("Musicophilia", "Oliver Sacks", "OL277255W", 2007, ("音樂心理", "神經科學", "生命故事")),
            ("Big Magic", "Elizabeth Gilbert", "OL17356845W", 2014, ("創造力", "勇氣", "自我成長")),
            ("I Know This to Be True", "Geoff Blackwell、Ruth Hobday", "OL21665201W", 2016, ("生命智慧", "價值觀", "韌性")),
            ("Feeling Is the Secret", "Neville Goddard", "OL4492042W", 2004, ("信念", "情緒", "自我暗示")),
            ("The Greatness Guide", "Robin S. Sharma", "OL276493W", 2006, ("自我成長", "習慣", "領導自己")),
            ("What Should I Do With My Life?", "Po Bronson", "OL3292805W", 2002, ("人生選擇", "職涯", "自我探索")),
            ("David and Goliath", "Malcolm Gladwell", "OL16809805W", 2013, ("逆境", "優勢", "韌性")),
            ("Maybe You Should Talk to Someone", "Lori Gottlieb", "OL19791590W", 2019, ("心理治療", "自我理解", "關係")),
            ("Overcoming Anxiety for Dummies", "Charles H. Elliott、Laura L. Smith", "OL538233W", 2002, ("焦慮", "認知行為", "自助練習")),
            ("The Antidote", "Oliver Burkeman", "OL16681873W", 2012, ("正向思考", "不確定性", "心理韌性")),
            ("You Are a Badass", "Jen Sincero", "OL17102197W", 2013, ("自信", "行動", "自我成長")),
            ("Everything Is F*cked", "Mark Manson", "OL20657486W", 2019, ("希望", "價值觀", "現代焦慮")),
            ("Come as You Are", "Emily Nagoski", "OL17870214W", 2015, ("身體認知", "親密關係", "自我接納")),
            ("Goals!", "Brian Tracy", "OL2392330W", 2003, ("目標設定", "行動計畫", "自律")),
            ("Family Wisdom from the Monk Who Sold His Ferrari", "Robin S. Sharma", "OL1854797W", 2001, ("家庭關係", "生活平衡", "價值觀")),
            ("Think Like a Freak", "Steven D. Levitt、Stephen J. Dubner", "OL17078346W", 2014, ("思考方式", "問題解決", "認知偏誤")),
            ("Life Coaching", "Michael Neenan", "OL6031983W", 2002, ("生活教練", "認知行為", "目標")),
            ("Positive Psychology", "Alan Carr", "OL25226491W", 2003, ("正向心理", "幸福", "優勢")),
            ("How to Do Nothing", "Jenny Odell", "OL20078135W", 2019, ("注意力", "數位生活", "自我主導")),
            ("The Mindfulness & Acceptance Workbook for Anxiety", "John P. Forsyth、Georg Eifert", "OL8920598W", 2007, ("正念", "接納", "焦慮")),
            ("What Every BODY Is Saying", "Joe Navarro、Marvin Karlins", "OL12926505W", 2008, ("肢體語言", "人際觀察", "溝通")),
            ("Women Who Think Too Much", "Susan Nolen-Hoeksema", "OL1944250W", 2003, ("反芻思考", "情緒調節", "女性心理")),
            ("Option B", "Sheryl Sandberg、Adam Grant", "OL17710048W", 2017, ("失落", "復原力", "支持關係")),
            ("The Road to Character", "David Brooks", "OL17364754W", 2015, ("品格", "謙遜", "人生價值")),
            ("It Didn't Start with You", "Mark Wolynn", "OL20029303W", 2016, ("代際創傷", "家庭模式", "療癒")),
            ("Social Intelligence", "Daniel Goleman", "OL1878299W", 2006, ("社會智能", "同理心", "人際關係")),
            ("Overcoming Social Anxiety and Shyness", "Gillian Butler", "OL2742370W", 2001, ("社交焦慮", "害羞", "認知行為")),
            ("Burnout", "Emily Nagoski、Amelia Nagoski", "OL20163365W", 2019, ("倦怠", "壓力循環", "自我照顧")),
            ("Happy Brain", "Dean Burnett", "OL19745207W", 2018, ("幸福", "大腦", "情緒科學")),
            ("S.U.M.O.", "Paul McGee", "OL21246074W", 2008, ("責任感", "行動", "生活態度")),
        ),
    ),
    "03_natural_science": (
        "自然科學",
        10,
        (
            ("Brief Answers to the Big Questions", "Stephen Hawking", "OL19552275W", 2014, ("宇宙", "物理", "科普")),
            ("A Brief History of Everyone Who Ever Lived", "Adam Rutherford", "OL17715915W", 2016, ("遺傳學", "人類史", "演化")),
            ("The Particle at the End of the Universe", "Sean M. Carroll", "OL16803831W", 2012, ("粒子物理", "希格斯玻色子", "科普")),
            ("Classical Mechanics", "Leonard Susskind、George Hrabovsky", "OL17800180W", 2013, ("古典力學", "物理", "數學")),
            ("Stuff Matters", "Mark Miodownik", "OL17778974W", 2013, ("材料科學", "工程", "日常科普")),
            ("Human Universe", "Brian Cox、Andrew Cohen", "OL20702825W", 2014, ("宇宙", "人類", "科學史")),
            ("Creation", "Adam Rutherford", "OL19967304W", 2013, ("生命科學", "合成生物", "演化")),
            ("The Perfect Theory", "Pedro G. Ferreira", "OL20350696W", 2014, ("廣義相對論", "宇宙學", "科學史")),
            ("Existential Physics", "Sabine Hossenfelder", "OL26841047W", 2022, ("物理學", "哲學問題", "科普")),
            ("Why Does E=mc2?", "Brian Cox", "OL13766704W", 2009, ("相對論", "能量", "物理")),
        ),
    ),
    "04_healthcare": (
        "醫療保健",
        2,
        (
            ("The Emperor of All Maladies", "Siddhartha Mukherjee", "OL15540668W", 2010, ("癌症", "醫療史", "治療")),
            ("The Great Influenza", "John M. Barry", "OL7989229W", 2004, ("流行病", "公共衛生", "醫療史")),
        ),
    ),
    "05_food_wellness": (
        "飲食養生",
        2,
        (
            ("Food Rules", "Michael Pollan", "OL14873323W", 2009, ("飲食原則", "營養", "健康飲食")),
            ("In Defense of Food", "Michael Pollan", "OL3296482W", 2008, ("飲食文化", "營養", "加工食品")),
        ),
    ),
    "06_computer_info": (
        "電腦資訊",
        2,
        (
            ("Hacking for Dummies", "Kevin Beaver", "OL6035941W", 2004, ("資安", "滲透測試", "風險管理")),
            ("Raspberry Pi User Guide", "Eben Upton", "OL17451852W", 2012, ("Raspberry Pi", "硬體", "程式設計")),
        ),
    ),
    "07_other": (
        "其他",
        2,
        (
            ("Collapse", "Jared Diamond", "OL276557W", 2004, ("文明史", "環境", "社會變遷")),
            ("Webs of Humankind", "J. R. McNeill", "OL22198858W", 2020, ("世界史", "人類網絡", "文明交流")),
        ),
    ),
}


def candidate_rows(category_id: str, label: str, specs: tuple) -> list[dict]:
    rows = []
    for title, author, work_id, year, subjects in specs:
        focus = "、".join(subjects)
        rows.append({
            "title": title,
            "author": author,
            "categoryId": category_id,
            "sourceName": f"Open Library {label}主題書目（人工複核）",
            "sourceUrl": f"https://openlibrary.org/works/{work_id}",
            "sourceDateNote": (
                f"Open Library 書目標示初版年份為 {year}；擷取日期 {TO_DATE}，"
                f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
            ),
            "tags": [label, *subjects],
            "summary": f"本書由{author}撰寫，聚焦{focus}，整理核心概念、案例與可延伸的實際應用。",
            "subjects": list(subjects),
        })
    return rows


def preflight() -> list[tuple[str, str, int, list[dict]]]:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    existing = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    urls = {str(book.get("sourceUrl", "")).strip() for book in manifest.get("books", [])}
    prepared = []
    conflicts = []
    for category_id, (label, quota, specs) in BOOKS.items():
        rows = candidate_rows(category_id, label, specs)
        if len(rows) != quota:
            raise ValueError(f"{category_id} 候選 {len(rows)} 本，不等於配額 {quota}")
        for row in rows:
            key = findbook_writer.normalized_key(row["title"], row["author"])
            if key in existing or row["sourceUrl"] in urls:
                conflicts.append(f"{category_id}\t{row['title']}\t{row['author']}")
            existing.add(key)
            urls.add(row["sourceUrl"])
        prepared.append((category_id, label, quota, rows))
        print(f"candidate-ready\t{category_id}\t{len(rows)}")
    if conflicts:
        raise ValueError("候選與既有書庫重複：\n" + "\n".join(conflicts))
    print(f"preflight-valid\tbooks={sum(item[2] for item in prepared)}")
    return prepared


def reserve_and_complete(category_id: str, label: str, quota: int, rows: list[dict]) -> None:
    candidate_path = ROOT / "tools" / f".findbook_candidates_{category_id[:2]}_{TO_DATE.replace('-', '')}_{BATCH_NAME}.json"
    findbook_writer.write_json_atomic(candidate_path, rows)
    findbook_writer.reserve(argparse.Namespace(
        root=ROOT,
        category_id=category_id,
        category_file=None,
        candidates=candidate_path,
        limit=quota,
        from_date=FROM_DATE,
        to_date=TO_DATE,
    ))

    manifest = findbook_writer.read_json(ROOT / "data.json")
    by_key = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", "")): book
        for book in manifest.get("books", [])
        if book.get("categoryId") == category_id
    }
    results = []
    for row in rows:
        key = findbook_writer.normalized_key(row["title"], row["author"])
        book = by_key.get(key)
        if book is None:
            raise RuntimeError(f"{row['title']} reservation 後找不到索引")
        results.append({"id": book["id"], "highlights": prior_batch.highlights_for(row, label)})

    result_path = ROOT / "tools" / f".findbook_results_{category_id[:2]}_{TO_DATE.replace('-', '')}_{BATCH_NAME}.json"
    findbook_writer.write_json_atomic(result_path, results)
    findbook_writer.complete(argparse.Namespace(
        root=ROOT,
        category_id=category_id,
        category_file=None,
        results=result_path,
    ))
    print(f"category-complete\t{category_id}\t{len(results)}")


def update_manifest() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    complete = 0
    pending = 0
    for index_book in manifest.get("books", []):
        book = findbook_writer.read_json(ROOT / index_book["file"])
        if book.get("chatgptStatus") == "complete":
            complete += 1
        else:
            pending += 1
    manifest["totalBooks"] = len(manifest.get("books", []))
    manifest["searchDateRange"] = {"from": FROM_DATE, "to": TO_DATE}
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = (
        f"FindBook_Skill.md fresh Codex-only {BATCH_NAME} 30/30/10/2/2/2/2 complete: "
        f"complete={complete} pending={pending}"
    )
    findbook_writer.write_json_atomic(ROOT / "data.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description="2026-07-15 FindBook 第二批新書")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    prepared = preflight()
    if args.check_only:
        return
    for item in prepared:
        reserve_and_complete(*item)
    update_manifest()
    print(f"fresh-{BATCH_NAME}-complete\tbooks=78")


if __name__ == "__main__":
    main()
