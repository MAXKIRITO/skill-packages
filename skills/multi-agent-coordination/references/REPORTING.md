# 多 Agent 協同交付與報告規範

本文件提供多 Agent 任務從規劃、跨端對齊、對抗討論到最終交付的可裁剪範本與表格結構。

---

## 1. 多 Agent 任務規劃表 (Dispatch Plan)

在啟動多 Agent 前，主調度者應建立並記錄最小化派發計畫：

| 角色名稱 | 指派 Worker / ID | 所屬拓撲 | 職責與專注範圍 | 工作區模式 | 交付產物格式 |
| --- | --- | --- | --- | --- | --- |
| Doc-Reader-Auth | worker-1 | 海量文件平行分讀 | 研讀認證授權相關 RFC 與規格 | `inherit` | 權限實體與攔截規則表 |
| Frontend-Analyst | worker-2 | 跨專案隔離探勘 | 盤點前端 API 呼叫與狀態映射 | `inherit` | 請求定義與 Fallback 矩陣 |
| Challenger | worker-3 | 需求研擬與對抗審查 | 對提案架構發動邊界破壞測試 | `inherit` | 反例清單與安全性質疑 |

---

## 2. 跨專案邊界對齊矩陣 (Boundary Alignment Matrix)

適用於「拓撲二：跨專案／多 Repo 隔離探勘」之產物整合：

| 介面／行為 | 調用方 (Client) 實作與預期 | 服務端 (Server) 實作與現況 | 狀態 | 具體不相容點與證據 | 建議修正方向 |
| --- | --- | --- | --- | --- | --- |
| `POST /api/v1/order` | 發送 camelCase `userId`，期待 200 回傳 `orderId` | 驗證 snake_case `user_id`，未提供時回傳 400 | 不相容 | Client: `file:///src/api.ts#L45`<br>Server: `file:///handler.go#L88` | Client 統一序列化格式或 Server 增加 alias 支援 |
| `GET /api/v1/status` | 預設超時 2s，重試 3 次 | 內部依賴外部慢服務，平均延遲 2.5s | 潛在超時 | Client: `file:///http.ts#L12`<br>Server: `file:///service.py#L30` | 延長 Client 超時或 Server 端改為非同步輪詢機制 |

- **狀態標記**：`相容 (ALIGNED)`、`不相容 (MISMATCHED)`、`待驗證 (UNVERIFIED)`、`阻礙 (BLOCKED)`。

---

## 3. 對抗審查與共識收斂紀錄 (Convergence Log)

適用於「拓撲三：需求研擬與對抗審查」之討論過程追蹤：

| 議題／設計點 | Proposer 初始主張 | Challenger 提出的質疑與反例 | Verifier 查驗實情（代碼／測試依據） | 最終收斂結論 | 決策層級 |
| --- | --- | --- | --- | --- | --- |
| 即時推播機制 | 採用 Server-Sent Events (SSE) 傳送通知 | 斷線後重連未帶 Last-Event-ID，可能遺失訊息 | 現有閘道器對長連線預設 60s 斷開 (`file:///nginx.conf#L40`) | 採用 SSE 並在客戶端補齊本地緩衝與重試序號 | 共識 (Consensus) |
| 跨租戶快取隔離 | 以 `tenantId:key` 為 Redis 快取鍵 | 多租戶併發更新時可能產生快取擊穿 | Redis 叢集目前未配置記憶體上限與淘汰政策 | 快取寫入需加分散式鎖，但成本上升 | 權衡 (Trade-off，待決策) |

- **決策層級**：
  - `共識 (Consensus)`：經程式碼驗證，雙方達成一致並修正規格。
  - `權衡 (Trade-off)`：存在客觀技術衝突，列入使用者抉擇清單。
  - `駁回 (Rejected)`：質疑已被實測反駁，維持原設計。

---

## 4. 最終整合報告範本 (Synthesis Report Template)

任務完成後，主調度者交付給使用者之整合總結：

```markdown
# 多 Agent 協同任務交付報告：[任務名稱]

## 1. 任務範疇與調度總結
- **執行拓撲**：[平行分讀 / 跨專案探勘 / 對抗審查]
- **調度規模**：共啟動 [N] 位專職 Agent，已全部正常終止並完成生命週期回收。
- **目標範圍**：[涵蓋之檔案、Repo 或需求議題]

## 2. 核心發現與收斂產物
- **結論 1**：[精確描述，附帶跨 Agent 核對之證據路徑與行號]
- **結論 2**：...

## 3. 跨端/對抗爭端決策表
| 爭議點 | 核心衝突 | 推薦方案 | 備選方案與代價 | 依據程式碼/規範 |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

## 4. 資源回收核驗
- [x] 所有子 Agent / Swarm Worker 已全部 Kill 或回報完畢。
- [x] 暫存分支或工作區已完成整理／合併。
- [x] 無殘留之背景進程。

## 5. 待使用者裁定之開放問題 (Open Decisions)
1. [需人類決策者拍板的業務優先級或架構取捨]
```
