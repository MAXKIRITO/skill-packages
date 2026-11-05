# 多語系作業規範

索引：設定盤點、key 與使用處、訊息語法、UI、腳本契約、驗證與交付。只讀本次類型需要的章節。

## 1. 設定與檢查單位

確認 i18n 工具及版本、來源語系、支援語系、namespace、lazy loading、fallback chain、missing-key 行為與翻譯發布方式。不要假設英文一定是來源語系，也不要假設 locale 都在 repo。

單位為「使用處／namespace＋目標語系＋訊息類型」。局部修正只檢查受影響 keys；語系一致性審查再擴大到指定 locale 集合。明確分開已載入檔案與實際執行時可用語系。

## 2. Key 與使用處

- 靜態字串：從 `t()`、template directive、route meta、驗證與通知封裝找實際 key，確認 namespace prefix 與 key separator。
- 動態 key：找可達值集合，例如狀態 enum、後端 code mapping；無法列舉時標為動態未覆蓋，不報全部缺漏或未使用。
- 別名與包裝：核對翻譯 helper、全域 plugin、server-side rendering 與 lazy module 注入。
- fallback：確認產品要求是否允許某語系 fallback；「來源存在、目標缺少」是結構差異，不一定是執行錯誤。若目標語系要求完整翻譯，仍可列為品質缺漏。
- unused key：需考慮動態值、外部模板、其他 app 與發布版本，不以單次 `rg` 無結果作為刪除理由。

候選表只列 key、語系、使用位置、類別及證據；不要一次貼出整份 locale。

## 3. 訊息語法與翻譯語意

| 類型 | 檢查重點 | 驗證方式 |
| --- | --- | --- |
| 插值 | 參數名稱、必填、型別、escaping | 工具原生解析／格式化，使用代表值 |
| 複數 | 語言規則、zero／one／other 等實際支援 | 對必要數值分支格式化 |
| ICU／巢狀訊息 | select、plural、巢狀語法及 offset | 依工具版本使用 parser，不自製通用 regex |
| linked／rich text | 連結 key、slot、HTML tag、輸出 escaping | 確認 renderer 與框架安全規則 |
| 日期／數字 | locale、timezone、currency、單位 | 對已知輸入比較實際格式 |
| fallback | 無語系、缺 key、載入失敗 | 區分預期 fallback 與錯誤 |

翻譯可因語言需要重排詞序，不以字面順序判錯。參數名稱改動需更新所有語系與使用處；不要為讓比較通過而刪去參數。無法確認的專業詞彙或產品文案需標記人工確認，不假裝完成語言品質驗收。

## 4. 硬編碼與 UI

先識別真正顯示給使用者的文字：標題、按鈕、placeholder、tooltip、toast、驗證錯誤、空狀態、breadcrumb、ARIA label、email／server-rendered template（若在範圍）。

排除或另判斷註解、log、測試 fixture、品牌、裝置識別、協定欄位與使用者輸入。非英文不必然是硬編碼缺陷，英文也可能是待翻譯 UI。

檢查長文字、換行、RTL（專案支援時）、日期／數字與語系切換後反應性。不要以新增 key 取代 UI 可用性驗證；也不要順便改版或大量重排格式。

## 5. JSON 比較腳本契約

`scripts/compare_locales.py` 是唯讀、Python 3、無第三方依賴的結構比較工具。必須提供 `--base` 和至少一個 `--locale`；每個檔案頂層需為 JSON object。

```sh
python3 /path/to/i18n-check/scripts/compare_locales.py --base /project/en.json --locale /project/zh.json --locale /project/ja.json --limit 10
```

輸出：`base`、`limit`、`reports`；每個 report 含 locale、missing、extra、type_mismatches，各組含總數 `count` 與受 limit 限制的 `items`。以總數判斷是否有差異，不把被截斷的 items 當成完整清單。

路徑採 JSON Pointer，`/` 轉 `~1`、`~` 轉 `~0`，保留字面含點 key 與真正巢狀結構的差異。非空容器遞迴比較 leaf；空容器本身為 leaf。JSON number 視為同類，boolean 與 number 不同。

exit 0：所比較的 leaf 路徑與型別一致。exit 1：存在結構差異。exit 2：讀檔、JSON、重複 key、非 object 根或參數錯誤。stderr 提供輸入錯誤；不應把錯誤當成沒有差異。

限制：不解析程式引用、key separator、插值、ICU、翻譯品質或 lazy loading；不支援 YAML／JS。非空 array 與 numeric-key object 若有相同 leaf 可能無法分辨容器差異，需用原生工具補查。只接受明確選定且大小合理的語系檔，不用此工具掃任意未知資料或秘密檔。

腳本會回報檔案位置、key 路徑與型別，不輸出翻譯值；key 本身仍可能含敏感資訊，分享前需檢查。

## 6. 修正與驗證

優先修正實際使用的缺漏／錯誤 key；避免無關的 namespace 重命名、排序與大量翻譯。參數、fallback 與動態 key 的設計要與原生工具一致。

| 變更 | 必要證據 | 視情況增加 |
| --- | --- | --- |
| 新增靜態 key | 使用處與目標語系存在 | 切語系畫面 |
| 插值／plural | 原生 formatter 代表值輸出 | 數值邊界與錯誤輸入 |
| lazy locale | 模組載入與 fallback 行為 | 首次進入／切語系競態 |
| UI 文案替換 | 正確顯示，沒有 raw key | 長文、窄畫面、無障礙 |

locale 比較通過不代表全部文案正確；build 通過不代表動態 key 都可達。測試結果需明示語系、輸入、驗證方式及未覆蓋部分。

## 7. 候選與交付

先查 fallback、動態 namespace、有效發布版本與外部語系，再判缺漏。相同 key 在多處使用可合併一個根因，列出受影響畫面與語系。

交付：範圍／語系 → 問題表（key、位置、類別、證據、影響）→ 修正 → 測試 → 動態或人工待確認事項。未明確要求時不產生整站翻譯報告。

### 案例：目標語系缺 key 但畫面正常

先確認 fallback 是否刻意啟用，再判定為翻譯完整度問題或功能缺陷；不要宣稱畫面會顯示 raw key，除非已觀察或來源規則可證明。

### 案例：`status.${value}` 找不到引用

追 value 的可達集合與外部輸入，列出能確認的 key；無法窮舉時標示缺口，不能批次刪除所有 `status` 翻譯。
