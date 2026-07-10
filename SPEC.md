# 讀書後重點整理 SPEC

## 目標

建立可部署到 GitHub Pages 的靜態網頁，用下拉式單選 UI 切換風格、背景、主題與書名，並以單欄版面顯示每本書由 Codex 產生的讀後重點整理。另提供 `modifyData.html`，讓使用者可以修改、排序各主題 JSON 的書籍並在本機儲存。

## 檔案

- `index.html`：主頁面與書籍資料載入邏輯。
- `theme.js`：至少 10 種書籍整理版面風格。
- `bg.js`：動態背景下拉選單與背景樣式。
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

## index.html UI

1. 上方控制區有 4 個下拉式單選 UI：風格、背景、主題、書名。
2. 風格、背景、主題控制會依目前文字自動縮到可顯示內容的最小寬度。
3. 搜尋輸入框位在主題右側，可用書名或作者關鍵字跨主題搜尋。
4. 書名下拉選單每頁最多顯示 50 筆，上一頁、頁碼、下一頁整合在書名控制內。
5. 搜尋結果也遵守每頁 50 筆規則。
6. 主題切換後，只載入該主題 JSON，並更新書名下拉選單。
7. 書名切換後，以單欄版面直接顯示作者與 Codex 重點整理，不顯示來源切換或點數按鈕。
8. 風格與背景選擇會寫入 `localStorage`。
9. 首頁直接進入書籍內容，不顯示大型標題與統計區。
10. 書籍資訊位於重點整理上方，桌面與行動版都維持單欄。
11. 每個重點優先顯示為一列；內容換行時，正文與上一行正文起點對齊。
12. 頁面保留進度列，方便閱讀新版 200 個重點。

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
    { "id": "01_business_startup", "label": "01_商業創業", "file": "01_business_startup.json" }
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
      "chatgptHighlights": ["001、...", "...", "200、..."],
      "chatgptStatus": "complete"
    }
  ]
}
```

`chatgptHighlights` 為既有相容欄位；實際內容由 Codex 產生。

## 初始內容

既有書籍可保留舊版 100 個重點；之後透過 `FindBook_Skill.md` 新增或重做的書籍，每本由 Codex 產生 200 個重點。

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
4. 新增或重做的 Codex 重點必須剛好 200 點，並通過 `001、` 至 `200、` 的逐行驗證。
5. 1000 本以上建議改成每本一檔，而不是每個分類一大檔。
