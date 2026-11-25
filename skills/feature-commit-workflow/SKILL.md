---
name: feature-commit-workflow
description: 在 Git repository 實作一項或多項功能、要求代理建立 commit，或需要避免把整批變更塞進單一 commit 時使用。依可獨立審查的功能單位建立本機 commit、統一 commit 訊息，並將所有 push 保留給人為操作；純審查、唯讀分析或非 Git 工作不適用。
---

# 依功能提交 Git Commit

## 核心規則

- 啟用本 skill 且任務包含已授權的實作時，把建立本機 commit 視為交付流程的一部分；不因此擴張功能、檔案或環境的授權範圍。
- 每完成一個可獨立理解、驗證及審查的功能單位，就建立一個本機 commit，再開始下一個功能單位。
- 不把多項已可分離的功能累積到最後一次提交，也不為增加 commit 數量而按檔案或任意行數拆分。
- 建立測試腳本前先判斷它是專案正式測試或僅供本機驗證；本機專用腳本不得放進可推送的專案內容。
- Agent 永遠不得執行 push。任何會上傳 commit、建立或更新遠端 ref 的命令、工具或 API 都由人為操作。

## 功能單位

一個 commit 只包含一個清楚的目的，例如新增一項行為、修正一個根因或完成一個可獨立成立的重構。該行為所必需且應由專案長期維護的測試、文件、型別、設定或 migration 應與功能放在同一 commit，不要機械式拆開。

若前置重構本身可獨立驗證且不改變行為，可先提交 `refactor`，再提交功能。若多項變更必須一起存在才不會破壞建置、契約或資料相容性，視為同一功能單位，並在交付時說明原因。

## 測試腳本的存放判斷

建立或修改測試腳本前先分類：

- **專案正式測試**：驗證應長期保留的行為或回歸情境，能供其他開發者或 CI 重複執行，且不依賴個人路徑、帳號或機器狀態。放進專案既有測試結構，與所屬功能一起 commit。
- **本機驗證腳本**：只用於一次性診斷、探索或手動驗證，含本機路徑／個人環境假設／臨時資料，或不打算由專案維護。預設放在 repository 外的系統暫存目錄或個人工作區，不得先放進專案再期待提交時記得排除。

若無法確定是否值得長期維護，先當作本機驗證腳本放在 repository 外；若它實際上是在保護重要回歸行為，應整理成不依賴本機狀態的正式測試，而不是永久隱藏。

只有工具限制使腳本必須位於 worktree 時，才可使用專案既有且明確供本機使用的 ignored 目錄。建立後用 `git check-ignore -v <path>` 確認忽略規則生效；不得僅為隱藏一次性腳本而修改共享的 `.gitignore`。若沒有合適的既有區域，改用 repository 外的位置或向使用者確認，不自行新增可推送的本機腳本目錄。

提交前以 `git status --short --untracked-files=all` 及 staged diff 複核。本機驗證腳本不得是 tracked 或 staged；若誤加到 staging，先 unstage 並移到 repository 外。既有已追蹤的本機腳本不因本規則自動刪除，應排除於本次 commit 並回報使用者處理。

## 提交流程

1. 開工前檢查目前 branch、`git status`、近期 commit 慣例與既有未提交變更。把任務劃分為預計的功能單位；實作中可依新證據調整。
2. 保留使用者及其他工作的既有變更。不得把無關變更納入 commit；若同一檔案的變更無法安全分離，停止該次提交並向使用者確認。
3. 一次只實作一個功能單位，先按上方規則分類測試腳本，再完成相應的測試或最低限度驗證。不得提交已知會破壞建置或主要行為的中間狀態。
4. 只 stage 該功能涉及的明確路徑或 hunk；避免 `git add .`、`git add -A` 等可能夾帶其他變更的廣域操作。
5. 提交前檢查 staged 檔案與 staged diff，確認內容完整、沒有憑證或無關修改，再依下方格式建立 commit。
6. commit 成功後才進入下一個功能單位。沒有實際變更時不得建立 empty commit。
7. 最後列出本次建立的 commit hash 與主旨、各功能的驗證結果、剩餘未提交變更，以及仍保留的 repository 外本機驗證腳本位置，並明確註記「未 push」。

若 hook 或檢查失敗，先修正同一功能再重試，不得自行使用 `--no-verify`。若因環境限制無法執行檢查，可在沒有已知損壞的前提下提交，但必須明列未驗證項目。不得為了完成流程而改寫使用者的 Git 設定、跳過簽章要求，或修改不屬於本任務的既有 commit。

## Commit 訊息

格式採 Conventional Commits：

```text
<type>(<scope>): <summary>

<optional body>

<optional footer>
```

- `type` 使用 `feat`、`fix`、`refactor`、`test`、`docs`、`perf`、`build`、`ci`、`style`、`chore` 或 `revert`；優先選能表達使用者可感知目的的類型。
- `scope` 使用穩定的模組、領域或套件名稱；沒有明確 scope 時省略括號，不填 `misc`。
- `summary` 用祈使語氣描述完成的結果，遵循 repository 既有語言；主旨不超過 72 個字元、不加句號，避免 `update`、`changes`、`misc fixes` 等空泛文字。
- 行為原因、重要取捨或非顯而易見的影響放在 body，不把檔案清單當成說明。
- 不相容變更使用 `!` 並在 footer 寫 `BREAKING CHANGE: ...`；議題關聯可用 `Refs: #123` 或 repository 既有格式。

範例：

```text
feat(auth): add passkey sign-in
fix(chart): preserve zero-value samples
refactor(mqtt): isolate payload decoding
docs(commits): define feature commit policy
```

## Push 邊界

不得執行 `git push`、force push、`git send-pack`、會隱含 push 的 PR 發布流程，或任何等效遠端寫入。即使使用者在後續要求 push，也要說明此 skill 規定 push 只能由人為執行，並交付目前 branch、待推送 commit 與供人確認後手動執行的普通 push 指令；不得預設建議 force push。
