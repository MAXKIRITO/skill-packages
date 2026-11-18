# 多 Agent 拓撲架構與協同協定

本文件定義三種核心協同拓撲的具體角色分工、通訊協定、派工簡報範例與收斂標準。

---

## 拓撲一：海量文件平行分讀與萃取 (Parallel Fan-Out & Reduce)

### 1.1 適用情境
- 需研讀跨數十個章節的技術規範書（RFC / PRD / 架構手冊）。
- 跨數個獨立技術棧之長篇官方文件（如雲原生部署指南、複雜權限框架規格）。
- 需自海量分散日誌或變更紀錄中比對特定歷史事件。

### 1.2 角色矩陣與資料流

```
                    [Coordinator (主調度者)]
                               |
         +---------------------+---------------------+
         | (分派 Slice A)      | (分派 Slice B)      | (分派 Slice C)
         v                     v                     v
   [Worker 1: 規格分析]  [Worker 2: 架構分析]  [Worker 3: 邊界/錯誤分析]
   (docs/spec-a/*.md)    (docs/spec-b/*.md)    (docs/spec-c/*.md)
         |                     |                     |
         +---------------------+---------------------+
                               |
                       (回傳結構化萃取結果)
                               v
                     [Coordinator 整合去重]
```

### 1.3 執行步序
1. **目錄劃分（Partitioning）**：主調度者先通讀目錄索引或檔案清單，依「領域內聚、領域間解耦」原則，將文件切分成 2–3 個獨立集合。
2. **派發專職 Worker**：為每個集合啟動一個子 Agent，設定 `Workspace: 'inherit'`（唯讀）。
3. **結構化萃取（Extraction）**：Worker 僅回答限定維度，輸出統一 Markdown 表格或 JSON。
4. **主調度者彙整（Reduce）**：核對交叉引用，消除重複條目，彙整為單一完整知識索引。

### 1.4 派工簡報 (Briefing) 範例

```markdown
@role: Spec-Analyst-Storage
@workspace: inherit
@objective: 分析儲存子系統規格，萃取所有資料模型實體與持久化約束。
@scope: docs/specs/storage/**/*.md
@evidence_standard: 每個實體欄位必須標註文件檔名與精確章節/行號。
@output_format:
- 實體名稱與用途
- 關鍵欄位清單 (欄位名稱 / 型別 / 必填 / 約束條件)
- 來源段落連結
@stop_condition: 讀完指定範圍內所有儲存規格即停止回報，不分析 API 或網路模組。
```

---

## 拓撲二：跨專案／多 Repo 隔離探勘 (Cross-Project Specialists)

### 1.1 適用情境
- 前端專案與後端 API 專案聯合分析，排查跨端資料欄位與生命週期不相符。
- 客戶端 SDK 與微服務後端對接，追蹤呼叫協議與錯誤重試。
- 舊系統（Legacy Repo）向新系統（New Repo）遷移時之功能與資料流比對。

### 1.2 角色矩陣與隔離邊界

```
+------------------------------------------------------------------+
|                     Integration Coordinator                      |
|                     (負責契約邊界對齊與仲裁)                     |
+------------------------------------------------------------------+
          ^                                              ^
          | (出口定義: 呼叫/參數/預期)                   | (入口定義: 路由/驗證/回傳)
          |                                              |
+------------------------+                    +------------------------+
|  Worker A: Client 端   |                    |  Worker B: Server 端   |
|  (限定於 frontend/)    |                    |  (限定於 backend/)     |
|  Workspace: share 或   |                    |  Workspace: share 或   |
|  指定路徑白名單        |                    |  指定路徑白名單        |
+------------------------+                    +------------------------+
```

### 1.3 執行步序
1. **劃定專案邊界**：明確區分 Project A 與 Project B 的根目錄。若需修改或測試，指派各自獨立的 workspace。
2. **單邊追蹤**：
   - Worker A 只追蹤客戶端請求組裝、攔截器（Interceptor）、預期結構與錯誤 Fallback。
   - Worker B 只追蹤服務端路由中介軟體（Middleware）、權限校驗、序列化與異常回應。
3. **邊界核對（Interface Matching）**：主調度者接收兩端報告，對比 URL、HTTP Method、Header、Payload 欄位命名、Null 值處理與狀態碼。
4. **輸出相容性差異**：產出《跨專案契約相容性檢驗表》。

### 1.4 派工簡報 (Briefing) 範例

```markdown
@role: Backend-Contract-Auditor
@workspace: inherit
@objective: 盤點訂單支付完成後的 Webhook 發送行為與資料契約。
@scope: /Users/axm/project/backend/services/payment/**/*.go
@evidence_standard: 記錄具體 handler 函數、發送 payload 結構體定義行號。
@output_format:
- Webhook 觸發條件
- 目標 URL 構造邏輯
- 實際發送之 JSON 欄位（精確標明大小寫、型別與可能為 null 之欄位）
- 失敗重試策略
@stop_condition: 完成 payment webhook 相關追蹤即停止，不得讀取 frontend 程式碼。
```

---

## 拓撲三：需求研擬與對抗審查 (Adversarial Debate & Requirement Elicitation)

### 1.1 適用情境
- 需求不明確、架構改動影響巨大，需在編寫程式前探討並鎖定邊界。
- 評估多種技術架構方案之優缺點（如 Polling vs WebSocket vs SSE）。
- 對重大功能規格書進行「紅藍軍對抗審查」，提前挖掘安全、並行與恢復死角。

### 1.2 角色劃分

| 角色 | 職責 | 行為準則 |
| --- | --- | --- |
| **Proposer (提案方)** | 擬定需求規格書草案、系統資料流與實作藍圖 | 主動提供具體架構決策與理由，不給含糊其詞的描述 |
| **Challenger (對抗質疑方)** | 扮演 Devil's Advocate，主動挑戰設計缺陷 | 針對並發衝突、網絡失敗、授權穿透、邊界狀態提出反例 |
| **Verifier (事實錨定方)** | 依據當前專案實際程式碼與環境進行驗證 | 用實際程式碼、已有依賴、歷史 Bug 或基準測試裁決爭端 |

### 1.3 協同協定與三階段收斂

```
[階段 1: 初步提案]
Proposer 產出需求草案與關鍵假設 (Draft Spec)
       |
       v
[階段 2: 對抗質疑與事實檢驗 (限 1~2 輪)]
Challenger 提出反例清單與邊界缺陷 (Challenges)
       |
       +---> Verifier 查驗現有程式碼/工具能力，提供事實支持或反證
       |
Proposer 修正草案，或記錄不可抗之架構權衡 (Trade-offs)
       |
       v
[階段 3: 共識收斂與交接]
主調度者彙整確定需求清單，列出未決邊界由使用者裁定
```

### 1.4 辯論互動約束（嚴防文字遊戲）
- **禁止空泛肯定**：嚴禁「我非常同意你的看法」、「你的建議很有深度」等無意義客套話；直接陳述「同意點與依據」或「反對點與反證」。
- **反駁必須有情境**：Challenger 的質疑必須以「如果發生情境 X，且條件 Y 滿足，該架構將導致 Z 失敗」的形式提出。
- **終止閾值**：若連續兩輪對同一爭端各持己見且無新代碼證據出現，立即終止爭辯，記錄為「開放性設計權衡（Architectural Trade-off）」，列入交付報告由使用者拍板。
