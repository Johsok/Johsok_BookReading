# 讀書後重點整理 SPEC

## 目標

建立可部署到 GitHub Pages 的靜態網頁，用下拉式單選 UI 切換風格、背景、主題與書名，並以 15 種響應式版面顯示每本書由 Codex 產生的讀後重點整理。另提供 `modifyData.html`，讓使用者可以修改、排序各主題 JSON 的書籍並在本機儲存。

## 檔案

- `index.html`：主頁面與書籍資料載入邏輯。
- `theme.js`：15 種具有不同資訊結構的書籍整理版面風格。
- `bg.js`：20 種背景（含無背景）與背景下拉選單；背景 01–10 使用 Canvas 逐幀動畫。
- `modifyData.html`：JSON 編輯器，可讀取、驗證、格式化、儲存或下載資料。
- `data.json`：全站索引，只存主題、書籍基本資料與分類 JSON 路徑。
- `01_business_startup.json`：商業創業書籍重點。
- `02_psychology_growth.json`：心理勵志書籍重點。
- `03_natural_science.json`：自然科學書籍重點。
- `04_healthcare.json`：醫療保健書籍重點。
- `05_food_wellness.json`：飲食養生書籍重點。
- `06_computer_info.json`：電腦資訊書籍重點。
- `07_other.json`：其他書籍重點。
- `FindBook_Skill.md`：下次找新書與整理重點的 SOP。
- `Find_eBooks.pyw`：獨立的免費電子書搜尋與下載工具，不修改網站書籍 JSON。

## Find_eBooks.pyw

1. 提供 Windows Tkinter GUI，可輸入主題、開始／結束日期、需要本數與下載資料夾；日期優先使用月曆選單，無法安裝日期元件時改用內建年／月／日下拉選單。
2. 只使用官方公開介面搜尋 OAPEN、Open Library／Internet Archive、Project Gutenberg、中文維基文庫與中文維基教科書，不繞過登入、借閱限制或 DRM。
3. 日期意義依來源標示：OAPEN 為出版日期、Open Library 為作品首版年、Gutenberg 為電子版上架日、維基來源優先採 Wikidata 原作日期；只有年份時以整年區間比對。
4. 搜尋平台可平行處理；下載使用 `ThreadPoolExecutor`，同時下載數可由使用者選擇，並另以每站限流、重試及 `Retry-After` 保護來源服務。
5. Python 3.9 以上即可執行；首次啟動會嘗試自動安裝 `tkcalendar`，安裝失敗不影響核心功能。
6. 下載僅接受 EPUB、PDF、TXT，使用官方網域白名單、500 MB 上限、`.part` 暫存、格式／大小／MD5 驗證及原子替換，最後輸出 UTF-8 CSV 報告。

## index.html UI

1. 上方控制區有 4 個下拉式單選 UI：風格、背景、主題、書名。
2. 風格、背景、主題控制會依目前文字自動縮到可顯示內容的最小寬度。
3. 搜尋輸入框位在主題右側，可用書名或作者關鍵字跨主題搜尋。
4. 書名下拉選單每頁最多顯示 50 筆，上一頁、頁碼、下一頁整合在書名控制內。
5. 搜尋結果也遵守每頁 50 筆規則。
6. 主題切換後，只載入該主題 JSON，並更新書名下拉選單。
7. 書名切換後，15 種風格在桌面寬度大於 920px 時，都將書名與作者資訊顯示於左側 330px 欄，並在捲動時維持螢幕垂直置中；寬度小於或等於 920px 時統一改為單欄，不顯示來源切換或點數按鈕。
8. 風格與背景選擇會寫入 `localStorage`。
9. 首頁直接進入書籍內容，不顯示大型標題與統計區。
10. 15 種風格必須以配色、書籤造型、字體、重點卡片排列或閱讀節奏形成可辨識差異，不得只有單一顏色差異；桌面版書籍資訊位置不作為風格差異，統一使用左側 330px 欄與螢幕垂直置中。
11. 每個重點優先顯示為一列；內容換行時，正文與上一行正文起點對齊。
12. 頁面保留進度列，方便閱讀新版 150 個重點。
13. 背景選單的 01–10 必須使用 Canvas 逐幀繪製動態特效，畫面需持續有可見運動（可含游標互動），不得退化為靜態圖片或靜態 CSS；切換至其他背景時須停止前一個動畫，且事件監聽只能初始化一次，不得重複綁定。

## modifyData.html UI

1. 可選擇 `data.json` 或 7 個主題 JSON。
2. 可從網站檔案讀取 JSON。
3. 可選擇本機 JSON 檔並取得瀏覽器授權後覆蓋儲存。
4. 可格式化與驗證 JSON。
5. 若瀏覽器不支援本機覆蓋儲存，改用下載 JSON。
6. 左側列出目前 JSON 的書籍，點擊後跳到對應書籍區段。
7. 可依書名、作者或 ID 以升冪／降冪排序 `books` 陣列，排序後的順序會同步寫回編輯器並可儲存或下載。

## 資料格式

`data.json` 只作索引：

```json
{
  "categories": [
    { "id": "01_business_startup", "label": "01_商業理財", "file": "01_business_startup.json" }
  ],
  "books": [
    { "id": "book-id", "title": "書名", "author": "作者", "categoryId": "01_business_startup" }
  ]
}
```

分類 JSON 存實際重點：

```json
{
  "categoryId": "01_business_startup",
  "books": [
    {
      "id": "book-id",
      "title": "書名",
      "author": "作者",
      "chatgptHighlights": ["001、...", "...", "150、..."],
      "chatgptStatus": "complete"
    }
  ]
}
```

`chatgptHighlights` 為既有相容欄位；實際內容由 Codex 產生。

## 初始內容

既有書籍可保留舊版 100 或 200 個重點；之後透過 `FindBook_Skill.md` 新增或重做的書籍，每本由 Codex 產生 150 個重點。

## GitHub Pages 效能建議

目前需求指定 7 個分類 JSON，因此先採「索引 + 分類 JSON」架構。若成長到約 1000 本，最佳做法是改成：

- `data.json` 只存書籍索引與每本書的 JSON 路徑。
- 每本書獨立成 `books/{category}/{book-id}.json`。
- 首頁只載入 `data.json`，選書後才載入單本 JSON。
- 可另外產生 `search-index.json` 存書名、作者、標籤，不存 100 個重點。

這樣 GitHub Pages 載入會更快，也比較不會因單一大 JSON 造成手機卡頓。

## 改善建議

1. 7 個主題其實是 7 類，不是 6 類；規格統一稱為 7 大主題。
2. 每本書只歸一類，但可用 tags 做交叉搜尋。
3. 新書資料來源應保留網址、擷取日期、榜單名稱、搜尋日期區間與來源日期說明。
4. 新增或重做的 Codex 重點必須剛好 150 點，並通過 `001、` 至 `150、` 的逐行驗證。
5. 1000 本以上建議改成每本一檔，而不是每個分類一大檔。
