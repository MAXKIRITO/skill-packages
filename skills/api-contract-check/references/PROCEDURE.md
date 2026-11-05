# API 契約作業規範

索引：範圍、契約矩陣、追蹤、候選驗證、修正與測試、交付案例。按 endpoint 或契約面選讀。

## 1. 範圍與單位

檢查單位是「method＋正規化 route＋版本＋使用方＋受影響契約面」。同 URL 的 GET／POST、不同 API 版本或權限角色，不自動視為相同單位。

從指定 diff、報錯請求或功能切入，記錄所屬 repo、變更前基準（若有）、目前未提交差異與明確排除範圍。不需要為一個欄位審查所有 endpoint。

最低輸入為 endpoint／相關檔案／可定位的症狀之一。缺少實際 payload 時先以程式碼確認形狀；只有該資料會改變判斷時才向使用者索取已去識別範例。

## 2. 契約矩陣

每個受影響面只記錄必要欄位，沒有適用情境標為不適用並說明原因。

| 面向 | 必查內容 | 易誤判情況 |
| --- | --- | --- |
| 傳輸與路由 | method、prefix、版本、content type、redirect、encoding | client 拼接及 proxy rewrite 後才是實際 URL |
| 輸入 | path/query/body/header、型別、必填、預設、null／省略、unknown fields | HTML form 與 JSON 的數字／布林序列化不同 |
| 識別與範圍 | auth context、tenant、parent resource、scope | 傳入 PlatformId 不代表已做授權 |
| 輸出 | status、envelope、欄位、nullable、單位、日期、精度 | middleware 可能再包裝 handler 回傳值 |
| 集合 | 分頁 token、limit、排序、filter、total、空結果 | 排序鍵不唯一可造成翻頁重複／遺漏 |
| 錯誤 | status、machine code、可顯示訊息、欄位錯誤、request ID | client 可能捕捉並轉換錯誤 |
| 生命週期 | retry、timeout、取消、idempotency、並行、非同步狀態 | client timeout 不代表後端沒完成寫入 |
| 發布與版本 | 舊使用方、generated clients、schema、SDK | 移除欄位與新增必填常需協調部署 |

特殊介面才展開檔案上傳、binary、stream、SSE、GraphQL 或 WebSocket 語意；不要把 HTTP JSON 的規則套用所有協定。

## 3. 追蹤與證據

從 client wrapper／route 定義確認實際入口，再追必要 middleware、validation、service、serializer 與 consumer mapping。只在需要判斷資料型別或 persistence 時讀 schema／model。

建立小型欄位對照：

| 路徑／欄位 | 呼叫端送出或期待 | 服務端接受或回傳 | 中介轉換 | 證據位置 |
| --- | --- | --- | --- | --- |
| body.limit | number／省略 | integer／預設 50 | JSON serializer | 路徑與符號 |

OpenAPI、型別與舊報告是線索，不直接證明執行契約。若 spec 與程式不同，指出哪一份由部署／測試證據支持。無執行證據就限制在目前來源可見行為。

搜尋真正使用方，不把同名字串當成使用證據。檢查 interceptor、adapter、fallback、alias 及 feature flag 是否已補償差異；同時確認補償有否破壞其他使用方。

## 4. 候選問題驗證

每個候選至少包含：觸發條件、來源→轉換→使用方、預期與實際差異、受影響操作、最小修正。

驗證時主動嘗試推翻：

- 是否是未啟用版本、未使用檔案或測試 fixture？
- 型別 coercion、client transformation 或 response middleware 是否使兩側實際相容？
- 欄位是否刻意 nullable、optional，或以 fallback 保持相容？
- 所宣稱的錯誤是否真的會出現在該 auth／tenant／feature flag 條件下？

原始碼直接證明的確定差異可以標示為靜態確認，但不得宣稱已重現網路請求。需要部署設定／第三方實際回傳才能判斷時，保留具體未確認事項。

合併同一根因的多個症狀，列出受影響使用方；不同 endpoint 的獨立 validation 缺陷不為方便而合併。影響依已建立的結果描述，不將契約差異自動提升為安全漏洞。

## 5. 修正與測試

先決定維持舊版相容或協調更新；使用者未要求 breaking change 時，優先最小相容方案。必要時分階段新增欄位／alias、遷移 client，再移除舊契約；不得永久掩蓋所有無效輸入。

| 變更 | 最小驗證 | 視影響增加 |
| --- | --- | --- |
| 欄位名稱／envelope | handler 到 client mapping 的代表案例 | 舊 client 相容性、generated client |
| 必填／型別 | 正常、缺漏、null、錯誤型別 | coercion、unknown fields |
| 分頁／排序 | 空集、單頁、跨頁邊界 | 同排序值、token 過期 |
| 權限／範圍 | 允許及拒絕、不同資源歸屬 | 多 tenant／parent-child 組合 |
| 重試／寫入 | 一次成功、失敗後重試 | timeout 後已完成、重複提交 |

依專案 scripts 找最小驗證；測試應覆蓋可觀察行為，不能只測新 helper 的相同實作。型別檢查、build、schema validation 各自只能支持其覆蓋層級。

實際請求前確認目標、auth、是否有寫入副作用及已授權的請求量。使用測試身份與去識別資料；不列印 header secrets 或真實個資。遇到服務不可用時交付靜態結果及精確的待驗證請求條件。

## 6. 完成與交付

完成條件：範圍中的契約面已確認或列出缺口；候選已查過反證；修改後驗證與相容性結論一致。未讀取的 endpoint 不得標成已檢查。

需要報告時使用：範圍與版本 → 契約差異表 → 根因與影響 → 修正／遷移 → 實際驗證 → 未確認事項。一般小修正用相同資訊的簡短摘要即可，不預設寫報告檔。

### 案例：client 期待 `items`，handler 回傳陣列

先檢查 response middleware 是否包裝為 `items`，再核對 client unwrap。沒有此轉換才成立為契約不一致；不能看到 handler 回傳陣列就立刻修改所有 client。

### 案例：新增必填 tenant ID

列出舊使用方、身份 context 的推導規則與部署順序。若 server 已能從授權 session 唯一決定範圍，查清設計後再決定是否需要新增欄位，不能把前端補值等同於授權修正。
