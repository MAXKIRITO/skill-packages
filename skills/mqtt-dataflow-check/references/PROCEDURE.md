# MQTT 資料流作業規範

索引：環境與追蹤、連線、訊息、consumer、儲存與呈現、主動測試、交付。按中斷環節讀取。

## 1. 環境與追蹤單位

確認 broker 環境與 protocol、裝置或測試身份、topic、觀察時間、預期 consumer 與資料出口。輸入不足先讀設定鍵及程式入口，不輸出密碼、私鑰、token 或完整真實 payload。

檢查單位是「publisher 身份＋topic／filter＋payload 類型＋consumer＋結果」。相同 topic 在不同租戶、broker 或 consumer group 的行為不自動共用證據。

被動診斷優先使用既有 log、設定與來源。主動測試另記錄訊息 ID、唯一 client ID、授權 topic、數量、頻率、timeout、清理方式及停止條件。

## 2. 連線與訂閱

| 階段 | 檢查內容 | 能證明什麼 |
| --- | --- | --- |
| 傳輸 | DNS、port、TCP／WebSocket、TLS、CA、SNI | 能否到達 broker，不能證明授權成功 |
| 登入 | protocol version、client ID、credential、CONNACK | session 建立結果，不能證明可讀寫 topic |
| 訂閱 | filter、ACL、SUBACK、QoS、session state | 訂閱授權及建立情況 |
| 發布 | topic、ACL、QoS、publish／ack | broker 層接收狀況，不能證明入庫 |
| 重連 | keepalive、session expiry、clean start、backoff | 斷線後訂閱與重送是否符合設計 |

MQTT 3.1.1 與 5 的 session、reason code 及屬性依實際 client／broker 版本確認。不要以 disable TLS verification 當修復；先找信任鏈或 endpoint 問題。

共享 client ID 可能踢掉既有連線。讀取 broker 管理 API 或修改 ACL 也可能有權限與副作用，不因可取得憑證就擴大範圍。

## 3. Topic 與訊息

核對大小寫、斜線、空層級、wildcard、shared subscription 及租戶／裝置路徑。一般訂閱 filter 與 broker ACL 語法不必然相同，要查實際設定。

Payload 檢查編碼、schema version、必要欄位、sensor mapping、資料型別、單位、device time／received time、大小上限及拒絕策略。

若協定本身沒有 correlation ID，不擅自新增未知欄位。可在專用測試裝置使用已支援的唯一識別或已知點值，配合時間窗口追蹤；標明無法唯一關聯的限制。

QoS 不是資料庫層 exactly-once 保證。retained 可能在新訂閱時回放；DUP 與應用重試、重送或 reconnect 都需要與 consumer 去重策略一起判斷。

## 4. Consumer 與持久化

追訂閱啟動 → dispatch → parse → validation → device/sensor resolve → queue／batch → DB commit → snapshot 更新。只看成功 log 不能證明 transaction 已提交。

- consumer 是否使用正確環境、訂閱 filter 與 schema？
- parse／validation 失敗是否有可識別證據，還是吞例外？
- queue 是否積壓、重試、dead-letter，batch 何時 flush？
- 去重鍵是否涵蓋裝置與事件，而非錯誤地跨裝置去重？
- 歷史表允許 late events 嗎？snapshot 比較哪個時間、同 timestamp 如何決勝？
- retry 前後是否可能部分寫入或重複 side effect？
- 多 consumer 是否共用 group，訊息是否預期只被其中一個處理？

確認資料真正寫入的表／時序來源、tenant 邊界、retention 與查詢路徑。不得為證明 consumer 正常就直接插 DB，這會繞過待測流程。

## 5. API 與 UI

追查 API 讀 historical 還是 snapshot、filter、cache、授權、time window，再看 WebSocket、polling 與 UI state。以相同裝置、點值與時間窗口串接證據；不同來源的最新值不能只按畫面順序推論。

可以用分段表：

| 階段 | 預期 | 已見證據 | 判斷 | 下一個必要檢查 |
| --- | --- | --- | --- | --- |
| broker | 接收測試 publish | ack／log | 只確認 broker 層 | consumer 收取 |
| consumer | resolve 裝置並提交 | 目前未見 | 未確認 | 指定 correlation 的 log |

## 6. 主動測試與停止

只在任務已授權的測試環境／topic 上執行。使用專用身份、唯一 client ID、少量訊息、明確 deadline、`retain=false`；不廣域訂閱 `#`、不發正式控制指令、不清 retained、不改 ACL。

執行既有 e2e／load 腳本前先讀副作用。帳號註冊、email verification、直接插 DB、歷史回填、刪除 fixture 及大量發布，都要符合本次授權，不能當成唯讀檢查。

驗證結果的層級：broker ack → consumer 接收 → schema 接受 → commit → API 查到 → UI 顯示，各段需各自證據。前一段成功不能代替下一段。

測試可按問題選擇：正常事件、無效裝置、重複、同 timestamp、晚到歷史事件、重連與 consumer retry。不在共享環境刻意造成過載或中斷。看到非預期副作用、身份衝突或已達訊息上限即停止並回報，不自動加量重試。

清理僅處理本次建立且可識別的 fixture；刪除 DB 或 retained message 是額外副作用，需符合原測試方案。無法安全清理時明確交代剩餘資料，不猜測後批次刪除。

## 7. 候選驗證與交付

查反證：是不是 retained 舊訊息、其他 consumer 正常處理、snapshot 刻意不接受晚到資料、API cache 尚未過期、UI 時間範圍不含該事件？

同根因可合併 broker／API／UI 症狀，但列出每段缺口。交付環境與追蹤條件、最後成功階段、第一個未成立階段、證據、最小修正、實際測試與未覆蓋環節。

### 案例：有 PUBACK 但圖表沒點

不要重送大量訊息；先用唯一識別確認 consumer parse／validation、commit 與 API time filter。PUBACK 不能支持「入庫已成功」。

### 案例：晚到資料有入歷史表但最新值沒變

先查 snapshot 的時間比較規則。若晚到資料不覆寫最新值正是設計，應判斷流程正常，而不是強迫更新 snapshot。
