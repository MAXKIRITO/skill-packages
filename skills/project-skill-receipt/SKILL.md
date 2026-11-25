---
name: project-skill-receipt
description: 回報本次實際讀取的專案 skill 數量與路徑。適用專案規則要求固定開頭，或使用者想確認 AI 有讀到哪些專案 skills 時。
---

# 專案 Skill 回報

每次任務開始時讀取本指引，按任務選讀並套用相關的專案 skills。最終回覆第一行必須以固定字串 `【專案 Skill 回報】` 開頭，接著在同一行用一句話寫出實際讀取的數量與各 `SKILL.md` 的專案相對路徑。路徑用 `、` 分隔，正文從下一段開始。

以本次任務實際取得完整內容的專案 `SKILL.md` 為準，每個檔案只計一次。本 skill 位於專案內且已讀取時也計入。僅從目錄、搜尋結果或技能清單看到的項目，以及專案外的全域 skills 與參考文件，不列入。只讀任務需要的 skills，並如實回報。

`【專案 Skill 回報】已讀取 2 個專案 skill，位於 skills/project-skill-receipt/SKILL.md、skills/i18n-check/SKILL.md。`

若沒有實際讀取任何專案 skill，使用 `【專案 Skill 回報】已讀取 0 個專案 skill。`
