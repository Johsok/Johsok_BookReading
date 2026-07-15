from __future__ import annotations

import findbook_batch_20260715_b2 as batch


BOOKS = {
    "01_business_startup": (
        "商業理財",
        30,
        (
            ("The Student Leadership Challenge", "James M. Kouzes、Barry Z. Posner", "OL1974738W", 2000, ("學生領導", "團隊", "影響力")),
            ("Rich Dad, Poor Dad for Teens", "Robert T. Kiyosaki、Sharon L. Lechter", "OL2010893W", 2004, ("青少年理財", "資產", "財務教育")),
            ("The Art of Persuasion", "Bob Burg", "OL22367098W", 2011, ("說服", "溝通", "銷售")),
            ("Project", "Helgi Thor Ingason、Haukur Ingi Jonasson", "OL25754672W", 2018, ("專案管理", "執行", "組織")),
            ("Think Big and Kick Ass in Business and Life", "Donald Trump、Bill Zanker", "OL2720608W", 2007, ("創業", "談判", "企圖心")),
            ("Eurasian Business Perspectives", "Mehmet Huseyin Bilgin、Hakan Danis、Ender Demir、Ahmet Faruk Aysan", "OL20820046W", 2017, ("歐亞商業", "經濟", "管理")),
            ("Contemporary Selling", "Mark W. Johnston", "OL16727213W", 2013, ("銷售", "顧客關係", "成交")),
            ("Advances in National Brand and Private Label Marketing", "Francisco J. Martínez-López、Juan Carlos Gázquez-Abad、Els Gijsbrecht", "OL20775747W", 2015, ("自有品牌", "零售", "行銷")),
            ("Marketing", "Roger A. Kerin、Eric N. Berkowitz、Steven W. Hartley、William Rudelius", "OL17744763W", 2002, ("行銷管理", "市場", "顧客價值")),
            ("Leadership in Health Care", "Jill Barr、Lesley L. Dowding", "OL9454258W", 2008, ("醫療領導", "組織", "變革")),
            ("Ethical Leadership and Decision Making in Education", "Joan Poliner Shapiro、Jacqueline Anne Stefkovich", "OL20900619W", 2000, ("倫理領導", "決策", "教育管理")),
            ("Entrepreneurship, Innovation and Regional Development", "Jay Mitra", "OL4071686W", 2008, ("創業", "創新", "區域發展")),
            ("Inspired Entrepreneurs", "Beth Caldwell、Debra Dion Krischke、Danielle Cuomo", "OL39679993W", 2010, ("女性創業", "企業家", "實務案例")),
            ("The Dynamics of Managing Diversity", "Gill Kirton、Anne-Marie Greene", "OL8477902W", 2000, ("多元管理", "人力資源", "組織文化")),
            ("The New Retirementality", "Mitch Anthony", "OL5827037W", 2001, ("退休規劃", "理財", "生活設計")),
            ("How to Win Campaigns", "Chris Rose", "OL7974716W", 2005, ("倡議", "行銷活動", "傳播")),
            ("Review of Marketing Research", "Naresh K. Malhotra", "OL25724460W", 2004, ("行銷研究", "消費者", "市場分析")),
            ("Strategic Marketing", "Tony Proctor", "OL1962170W", 2000, ("策略行銷", "定位", "競爭")),
            ("Social Media Marketing All-in-One for Dummies", "Jan Zimmerman", "OL20056309W", 2010, ("社群行銷", "內容", "數位策略")),
            ("Destination Marketing", "Steven Pike", "OL21281286W", 2012, ("目的地行銷", "觀光", "品牌")),
            ("Sponsorship in Marketing", "T. Bettina Cornwell", "OL19992774W", 2014, ("贊助行銷", "品牌", "效益衡量")),
            ("Basic Marketing Research", "Naresh K. Malhotra", "OL1959083W", 2001, ("市場研究", "資料分析", "顧客洞察")),
            ("Management", "Annie McKee", "OL20412530W", 2010, ("管理", "組織", "領導")),
            ("The New Psychology of Leadership", "S. Alexander Haslam", "OL16995812W", 2010, ("領導心理", "群體認同", "影響力")),
            ("Snapshots of Great Leadership", "Jon P. Howell", "OL16521674W", 2012, ("領導案例", "組織", "管理")),
            ("Entrepreneurship Marketing", "Sonny Nwankwo、Ayantunji Gbadamosi", "OL20749628W", 2010, ("創業行銷", "新創", "市場開發")),
            ("Responsible Leadership", "Thomas Maak、Nicola M. Pless", "OL25201859W", 2005, ("責任領導", "企業倫理", "利害關係人")),
            ("New Venture Management", "Donald F. Kuratko、Jeffrey Hornsby", "OL2761717W", 2008, ("新創管理", "成長", "營運")),
            ("Understanding Social Entrepreneurship", "Jill Kickul、Thomas S. Lyons", "OL20749665W", 2012, ("社會創業", "影響力", "商業模式")),
            ("Tribal Leadership", "David Logan、John King、Halee Fischer-Wright", "OL11659147W", 2007, ("組織文化", "領導", "團隊")),
        ),
    ),
    "02_psychology_growth": (
        "心理勵志",
        30,
        (
            ("The Children Who Lived", "Kathryn A. Markell", "OL12921155W", 2008, ("兒童韌性", "創傷", "復原")),
            ("Group and Team Coaching", "Christine Thornton", "OL20925062W", 2010, ("團隊教練", "群體動力", "成長")),
            ("Overcoming Objectification", "Ann J. Cahill", "OL15489348W", 2011, ("身體意象", "自我認同", "性別心理")),
            ("Employee Engagement Through Effective Performance Management", "Edward M. Mone", "OL8936327W", 2010, ("投入感", "動機", "回饋")),
            ("Handbook of Coaching Psychology", "Stephen Palmer、Alison Whybrow", "OL21330566W", 2014, ("教練心理", "行為改變", "目標")),
            ("Handbook of Self-Help Therapies", "Patti Lou Watkins、George A. Clum", "OL18205061W", 2007, ("自助治療", "心理介入", "實證方法")),
            ("Tip-of-the-Tongue States", "Bennett L. Schwartz", "OL8447532W", 2001, ("記憶", "認知", "語言心理")),
            ("African American Grief", "Paul C. Rosenblatt", "OL2918063W", 2005, ("哀傷", "文化", "支持")),
            ("The Right Words at the Right Time, Vol. 2", "Marlo Thomas", "OL281481W", 2006, ("鼓勵", "人生轉折", "溝通")),
            ("Anxiety & Depression Workbook for Dummies", "Charles H. Elliott、Laura L. Smith、Elaine Iljon Foreman", "OL15181635W", 2005, ("焦慮", "憂鬱", "自助練習")),
            ("Everyday SEL in High School", "Carla Tantillo Philibert", "OL21313001W", 2017, ("社會情緒學習", "青少年", "情緒調節")),
            ("Positive Psychology in Practice", "P. Alex Linley、Stephen Joseph", "OL18206819W", 2004, ("正向心理", "實務", "優勢")),
            ("Becoming Your Own Emotional Support System", "Linda L. Simmons", "OL5839082W", 2006, ("情緒支持", "自我照顧", "韌性")),
            ("Helping Grieving People When Tears Are Not Enough", "J. Shep Jeffreys", "OL3535056W", 2004, ("哀傷輔導", "失落", "陪伴")),
            ("Peak Performance Every Time", "Simon Hartley", "OL16002767W", 2012, ("高峰表現", "心理訓練", "專注")),
            ("Applied Positive Psychology", "Stewart I. Donaldson、Jeanne Nakamura、Mihaly Csikszentmihalyi", "OL16162280W", 2011, ("正向心理", "心流", "介入")),
            ("Let Her Fly", "Ziauddin Yousafzai", "OL19761941W", 2018, ("家庭支持", "女性成長", "勇氣")),
            ("The Theory and Treatment of Depression", "Jozef Corveleyn、Sidney J. Blatt", "OL19167181W", 2005, ("憂鬱", "心理治療", "人格")),
            ("How to Organize Yourself", "John Caunt", "OL20473689W", 2013, ("自我管理", "整理", "時間")),
            ("Exposure Treatments for Anxiety Disorders", "Johan Rosqvist", "OL8105166W", 2005, ("暴露治療", "焦慮", "認知行為")),
            ("Existential and Spiritual Issues in Death Attitudes", "Adrian Tomer、Grafton Eliason、Paul T. P. Wong", "OL18397916W", 2007, ("死亡態度", "存在心理", "靈性")),
            ("The Heart of the Soul", "Gary Zukav", "OL788825W", 2001, ("情緒覺察", "內在成長", "關係")),
            ("Daily Inspiration from the Monk Who Sold His Ferrari", "Robin S. Sharma", "OL16513166W", 2007, ("每日反思", "習慣", "人生智慧")),
            ("A Toolkit of Motivational Skills", "Catherine Fuller", "OL11810093W", 2008, ("動機", "助人技巧", "行為改變")),
            ("Fish!", "Stephen C. Lundin、Harry Paul、John Christensen", "OL13245065W", 2000, ("工作態度", "熱情", "團隊")),
            ("Advances in Contemplative Psychotherapy", "Joseph John Loizzo、Miles Neale、Emily J. Wolf", "OL21300693W", 2017, ("沉思心理治療", "正念", "療癒")),
            ("Emotionally Intelligent Leadership for Students", "Marcy Levy Shankman、Scott J. Allen", "OL16504581W", 2010, ("情緒智能", "學生領導", "自我覺察")),
            ("Linking Emotional Intelligence and Performance at Work", "Fabio Sala、Vanessa Urch Druskat、Gerald Mount", "OL18982884W", 2005, ("情緒智能", "工作表現", "團隊")),
            ("Lift", "Ryan W. Quinn", "OL13766657W", 2009, ("正向影響", "領導自己", "心理狀態")),
            ("Creativity Across Domains", "James C. Kaufman、John Baer", "OL19167838W", 2004, ("創造力", "認知", "跨領域")),
        ),
    ),
    "03_natural_science": (
        "自然科學",
        10,
        (
            ("How I Rescued My Brain", "David Roland", "OL21800574W", 2014, ("腦科學", "復健", "神經可塑性")),
            ("The Common Thread", "John Sulston、Georgina Ferry", "OL9351395W", 2002, ("基因體", "科學史", "生物學")),
            ("Knocking on Heaven's Door", "Lisa Randall", "OL16342081W", 2011, ("粒子物理", "宇宙", "實驗")),
            ("Surfing Scientist", "Ruben Meerman", "OL21013246W", 2007, ("科學實驗", "生活科普", "探索")),
            ("When Least Is Best", "Paul J. Nahin", "OL1907385W", 2003, ("數學", "極值", "科學問題")),
            ("How Mathematicians Think", "William Byers", "OL8328732W", 2006, ("數學思考", "創造力", "證明")),
            ("Why Icebergs Float", "Andrew Morris", "OL20931942W", 2016, ("物理", "日常現象", "科普")),
            ("Atoms Under the Floorboards", "Chris Woodford", "OL17092875W", 2015, ("物理", "材料", "生活科學")),
            ("Bird Populations", "Ian Newton", "OL17489279W", 2013, ("鳥類學", "族群生態", "保育")),
            ("Einstein", "Walter Isaacson", "OL4288870W", 2007, ("愛因斯坦", "物理史", "科學傳記")),
        ),
    ),
    "04_healthcare": (
        "醫療保健",
        2,
        (
            ("Mountains Beyond Mountains", "Tracy Kidder", "OL98216W", 2003, ("全球醫療", "公共衛生", "醫師故事")),
            ("When the Body Says No", "Gabor Maté", "OL8299076W", 2003, ("壓力", "身心健康", "慢性病")),
        ),
    ),
    "05_food_wellness": (
        "飲食養生",
        2,
        (
            ("Glucose Revolution", "Jessie Inchauspé", "OL26599673W", 2022, ("血糖", "飲食順序", "代謝")),
            ("French Women Don't Get Fat", "Mireille Guiliano", "OL5840799W", 2004, ("飲食文化", "份量", "生活習慣")),
        ),
    ),
    "06_computer_info": (
        "電腦資訊",
        2,
        (
            ("Python for Data Analysis", "Wes McKinney", "OL17422847W", 2012, ("Python", "pandas", "資料分析")),
            ("Head First Java", "Kathy Sierra、Bert Bates", "OL5756124W", 2003, ("Java", "物件導向", "程式設計")),
        ),
    ),
    "07_other": (
        "其他",
        2,
        (
            ("Born a Crime", "Trevor Noah", "OL17824318W", 2016, ("回憶錄", "南非", "種族文化")),
            ("Hillbilly Elegy", "J. D. Vance", "OL17357665W", 2016, ("美國社會", "階級", "回憶錄")),
        ),
    ),
}


batch.BOOKS = BOOKS
batch.BATCH_NAME = "b3"


if __name__ == "__main__":
    batch.main()
