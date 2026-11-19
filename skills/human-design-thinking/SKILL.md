---
name: human-design-thinking
description: 當需要從零發想介面或產品架構、重塑使用者體驗流程、規劃感知配色與字階空間系統，或進行多視角設計決策時使用。基於人本設計方法論（雙鑽石模型、設計思考五階段、內容優先、格式塔視覺認知、Laws of UX、60-30-10 OKLCH 語意配色、8pt/4pt 空間系統、W3C 三層 Token 架構與 8 狀態互動矩陣）。支援單 Agent 三重認知視角或多 Agent「三方頭腦互搏」協同（Lead 總監、Designer 設計師、Critic 審查員），透過對抗性審查與邊界質疑挖掘盲點，收斂出兼具美學秩序與工程可執行性的完整設計規格藍圖（Design Spec）。
---

# 人本設計思考與多 Agent 頭腦互搏 (Human-Centered Design Thinking & Adversarial Co-Design)

AI 生成介面之所以常顯得平庸、千篇一律或缺乏靈魂，核心癥結在於 AI 往往**直接從前端實作語法（如 CSS / Tailwind utility classes）反推畫面**，跳過了人類設計師在動手切版前所進行的**同理洞察、問題定義、內容優先規劃、視覺層級構建與邊界狀態推演**。

本 skill 將人類頂級設計師的隱性經驗（Tacit Knowledge）與認知科學轉譯為可執行的架構規範。它專注於**「上游設計思考與系統化架構」**——決定為什麼這樣排版、色彩語意如何分佈、空間節奏如何呼吸、元件如何因應極端狀態；產出的規格藍圖可無縫銜接下游的實作與工藝驗證流程（如 `frontend-anti-slop`）。

---

## 1. 運作模式與協同機制

本 skill 支援兩種運作架構，無論環境是否支援子 Agent，皆能維持「三重視角頭腦互搏」的高審美與嚴謹度：

| 模式 | 觸發條件 | 執行架構 | 產出目標 |
| :--- | :--- | :--- | :--- |
| **多 Agent 三方互搏 (Multi-Agent Triad)** | 環境支援子 Agent / Swarm，或使用者指定「多開 agent 討論／頭腦互搏」時 | 調度三位專職 Worker：<br>1. **Lead**（設計總監 / 流程主導與裁決）<br>2. **Designer**（設計架構師 / 方案發想與系統化推演）<br>3. **Critic**（審查質疑員 / 易用性與邊界狀態挑戰） | 經過 2~3 輪交鋒質疑與事實抗辯後，由 Lead 收斂之《人本設計決策架構書 (Design Spec)》 |
| **單 Agent 三重認知沙盒 (Single-Agent Cognitive Sandbox)** | 單一上下文、快速諮詢或無子 Agent 權限時（預設） | 主 Agent 在思考與輸出中依序切換三重角色人格：<br>`[🎯 Lead 總監定調]` → `[🎨 Designer 方案推演]` → `[🔍 Critic 邊界反駁]` → `[⚖️ Lead 仲裁收斂]` | 在單一上下文內完整模擬設計攻防，杜絕未經深思的默認模版輸出 |
| **設計規範校驗 (Design Audit)** | 使用者提供既有設計草案、PRD 或設計 Token 要求檢驗時 | 直接由 **Critic** 與 **Lead** 介入，依據 40+ 項設計審查指標（Rubric）與驗證腳本執行靜態合規與狀態完整度掃描 | 產出缺失清單、對比度修正建議與補全之 8 狀態矩陣 |

---

## 2. 三方角色職責矩陣（頭腦互搏核心）

多 Agent 或三重認知架構中，必須嚴格維持以下三位角色的專業邊界與對抗張力，嚴禁互相客套或無原則妥協：

```
+-----------------------------------------------------------------------+
|                    👑 Lead (設計總監 / 協調與裁決者)                    |
|  - 定義核心問題與受眾任務 (雙鑽石第 1 鑽)                                 |
|  - 掌控討論進程與輪次上限 (限 2~3 輪)                                     |
|  - 評估 Trade-offs 並裁決爭端，輸出最終可交付之 Design Spec               |
+-----------------------------------------------------------------------+
          |                                                   ^
          | (指派設計任務與約束)                                 | (匯報抗辯成果與最終提案)
          v                                                   |
+-----------------------------------+       質疑與攻防       +-----------------------------------+
|    🎨 Designer (設計架構師)        | <-------------------> |     🔍 Critic (審查質疑員)        |
| - 提出具體設計方案與版面構想        |   (針對邊界/易用性/   | - 扮演 Devil's Advocate           |
| - 建立 60-30-10 OKLCH 配色系統    |    狀態完整度互搏)    | - 挑戰空泛假設與文字溢出危機       |
| - 推導模組化字階與 8pt 空間網格    |                       | - 查驗 Laws of UX 與格式塔偏離    |
| - 定義元件解剖學插槽與視覺隱喻     |                       | - 揪出遺漏之互動狀態與 a11y 違規   |
+-----------------------------------+                       +-----------------------------------+
```

### 角色責任詳解
1. **👑 Lead (設計總監 / 流程主導與裁決者)**
   - **職責**：破除模糊需求，鎖定真實使用者角色、核心任務與內容約束（Content-First）。引導發散與收斂節奏。
   - **行為準則**：不直接跳入具體排版細節；當 Designer 與 Critic 各持己見時，依據使用者利益、認知成本與實作複雜度進行仲裁，產出最終定案。
2. **🎨 Designer (設計架構師 / 方案發想與系統化推演)**
   - **職責**：將抽象任務具象化為清晰的視覺架構。提出 60-30-10 預算配比、OKLCH 語意色票、Modular Scale 字階、8pt 留白節奏與元件解剖插槽。
   - **行為準則**：每個設計決策必須能回答「為什麼這樣設計」（以認知科學為背書）；面對 Critic 質疑時，以原則或改進方案回應，不得以「這只是示意」搪塞。
3. **🔍 Critic (審查質疑員 / 易用性挑戰與防盲點)**
   - **職責**：扮演嚴苛的產品審查員與無障礙衛士。抓出「理想狀態幻覺」——如超長標題折行、網路延遲白屏、缺少 Focus Ring、純靠顏色傳達狀態等。
   - **行為準則**：質疑必須具體具象，格式為「若情境 X 發生，當前設計 Y 將導致使用者 Z 困難，違反了原則 W」；拒絕泛泛而談的讚美。

---

## 3. 按需讀取參考文獻（知識底座）

設計決策推演時，依據涉及領域按需查閱 `references/` 目錄：

- **流程與認知科學基礎**：讀 [METHODOLOGY.md](references/METHODOLOGY.md)。
  - 雙鑽石發散收斂模型（Double Diamond）與設計思考五步驟。
  - 內容優先（Content-First）實踐與真實微文案。
  - 格式塔心理學五大原則（接近性、相似性、共同區域、主體背景、閉合連續）之 UI 映射。
  - Don Norman 符標（Signifier）與可供性（Affordance）；Laws of UX 認知負荷定律。
- **系統化美學與視覺度量**：讀 [SYSTEM_AESTHETICS.md](references/SYSTEM_AESTHETICS.md)。
  - 60-30-10 色彩比例紀律與視覺焦點預算。
  - OKLCH 感知均勻色彩模型與 Tonal Palette 色階演算法。
  - Material Design 3 語意色彩角色矩陣（Surface, Primary, Secondary, Outline, Error）。
  - Tonal Elevation（色調明度階層）取代高斯模糊重陰影。
  - 模組化字級比例（Modular Type Scale）與 45~75 字元最佳閱讀欄寬。
  - 8pt/4pt 空間網格與微留白（Micro: 4~16px） vs 宏留白（Macro: 48~120px+）。
- **元件解剖與互動狀態矩陣**：讀 [COMPONENTS_AND_TOKENS.md](references/COMPONENTS_AND_TOKENS.md)。
  - W3C DTCG 2025.10 三層 Token 架構（Primitive → Semantic → Component）。
  - 元件結構解剖學插槽（Container, Leading, Label, Supporting, Trailing）。
  - **必備 8 大互動狀態矩陣**：Default, Hover, Focus-Visible, Active, Disabled, Loading, Error, Empty。
- **多 Agent 頭腦互搏協定**：讀 [TRIAD_CO_DESIGN.md](references/TRIAD_CO_DESIGN.md)。
  - Lead, Designer, Critic 專屬派工簡報（Briefing）範本。
  - 對抗交鋒三階段協定與攻防語法標準。
  - 爭端未決時之 Trade-off 矩陣與防死循環機制（硬限制 2~3 輪）。
- **設計批判評審清單 (Rubric)**：讀 [CRITIQUE_RUBRIC.md](references/CRITIQUE_RUBRIC.md)。
  - 40+ 項覆蓋流程、認知、色彩、字階、空間與狀態之結構化審查指標。
- **規格書範本**：讀 [DESIGN_SPEC_TEMPLATE.md](references/DESIGN_SPEC_TEMPLATE.md)。
  - 標準可執行之 Markdown 交付模板。

---

## 4. 人本設計五階段標準流程 (The 5-Phase Procedure)

任何設計任務均嚴格遵循以下五個階段推進，拒絕跳過前置階段直接生代碼：

```
[Phase 1: 同理探索] ---> [Phase 2: 定義聚焦] ---> [Phase 3: 方案推演] ---> [Phase 4: 頭腦互搏] ---> [Phase 5: 交付定案]
 (Discover & Empathize)   (Define & Framing)     (Ideate & System)    (Adversarial Critique)   (Deliver Spec)
      (Lead 主導)             (Lead 確立)           (Designer 提案)         (Critic 攻防)           (Lead 收斂)
```

### Phase 1: 同理探索與內容鎖定 (Discover & Empathize)
1. **拒絕虛擬假字**：明確定義真實內容（Content-First），包括最長標題預期、數值極限、多語系長度倍率（如德文或日文可能膨脹 30%~50%）。
2. **鎖定使用者與情境**：定義核心 Persona、操作設備、環境光線（是否需高對比或深色模式）與情緒基調。

### Phase 2: 問題定義與任務路徑 (Define & Framing)
1. **確立核心任務（Core User Task）**：列出使用者在該畫面中最必須完成的 1~2 件核心行動。
2. **HMW 視角陳述**：以「How Might We（我們如何能...）」定義問題，劃定本次設計邊界，明確排除無關功能。

### Phase 3: 方案發想與系統化美學推演 (Ideate & Systematize)
Designer 依據人本設計原則產出具體的系統架構方案：
1. **60-30-10 感知色彩系統**：
   - 60% 畫布底層（Surface / Neutral），提供寧靜閱讀空間。
   - 30% 輔助結構（Surface Container / Secondary），建立卡片或側欄層級。
   - 10% 聚焦強調（Primary CTA / Accent），嚴格控制視覺重量。
   - 色彩採用 OKLCH 空間定義，確保深淺色與各語意色之感知亮度一致。
2. **模組化字階與排版尺度**：
   - 選定比例（如 Major Third `1.25` 或 Perfect Fourth `1.333`）。
   - 標題與內文維持顯著字級差（≥ 2.5x），減少對純粗體之依賴。
3. **8pt/4pt 空間系統**：
   - 宏留白（Macro: 48~96px+）明顯大於微留白（Micro: 4~16px），利用格式塔接近性自然分群。
4. **元件插槽與三層 Token 映射**：
   - 定義 Semantic Tokens（如 `color.surface.default`, `color.action.primary`）。

### Phase 4: 多視角頭腦互搏與對抗質疑 (Adversarial Critique)
Critic 展開對抗性審查（限 1~2 輪交鋒）：
1. **格式塔與層級審查**：是否有不必要的邊框隔斷了關聯？視覺焦點是否分散？
2. **Laws of UX 檢驗**：選項是否過多（Hick's Law）？主按鈕命中區與間距是否足夠（Fitts's Law）？資訊是否過載（Miller's Law）？
3. **互動心理與符標**：可點擊元素是否有足夠 Affordance/Signifier？是否像純裝飾？
4. **8 大狀態地毯式抽檢**：Default, Hover, Focus-Visible, Active, Disabled, Loading, Error, Empty 缺一不可。
5. **極端狀況壓力測試**：文案超長如何截斷？網路中斷如何重試？空資料時如何引導？
- **對抗規則**：Designer 必須針對 Critic 的有效質疑提出實質修正；若雙方對權衡有爭議，標記為 Trade-off 提交 Lead。

### Phase 5: 決策裁決、合約鎖定與交付 (Deliver & Contract Lock)
Lead 介入收斂，產出《設計決策架構書 (Design Spec)》，包含：
- 使用者情境與核心任務
- 60-30-10 OKLCH 語意 Token 表
- 模組化字階與 8pt 空間尺度表
- 關鍵元件解剖圖與 8 狀態定義
- 頭腦互搏攻防記錄與權衡裁定

---

## 5. 核心設計鐵律（Design Axioms）

在進行任何推演或審查時，堅決恪守以下原則：

1. **空間優先於線條（Whitespace over Borders）**：利用格式塔接近性與色調底塊（Common Region）分群，嚴禁「框中有框、到處畫 1px 灰色分割線」。
2. **宏留白必須壓倒微留白（Macro >> Micro）**：區塊間距（Section spacing, 48~96px）必須顯著大於元件內部間距（4~16px），介面才有透氣呼吸感。
3. **10% 強調色預算紀律**：高彩度 Accent 色只能留給當前視圖中最關鍵的 1~2 個 Primary CTA 或關鍵狀態，嚴禁全頁到處是醒目高光。
4. **禁止用低對比灰字製造次級層級**：次要文字應透過適度縮小字級（如 14px vs 16px）或微調字重區分，其對比度仍需符合 WCAG ≥ 4.5:1，嚴禁淡成不可讀。
5. **明度階層取代黑濁陰影（Tonal Elevation）**：以 OKLCH 漸進明度 Surface 代表前後層級，而非疊加多層骯髒重黑陰影。
6. **狀態必須完整閉環**：任何互動元件嚴禁只設計 Default 狀態；Loading（防跳動骨架屏）、Focus-Visible（高對比輪廓環）、Empty（友善引導）皆為一等公民。

---

## 6. 工具腳本輔助

本 skill 附帶設計驗證與 Token 生成腳本，位於 `scripts/`：

- **規格書合規校驗器 (`scripts/verify_design_spec.py`)**：
  ```sh
  python3 /Users/axm/project/skill-packages/skills/human-design-thinking/scripts/verify_design_spec.py --spec design_spec.md
  ```
  自動檢查 60-30-10 預算聲明、OKLCH 色票語意、Modular Type Scale 比例一致性、8pt 空間網格倍數，以及是否遺漏 8 大互動狀態中的任何一項。

- **W3C DTCG Token 生成器 (`scripts/generate_tokens.py`)**：
  ```sh
  python3 /Users/axm/project/skill-packages/skills/human-design-thinking/scripts/generate_tokens.py --brand "#2563EB" --output tokens.json
  ```
  依據主品牌色與 OKLCH 演算法，自動推導相容 Material Design 3 語意角色之 Primitive/Semantic/Component 三層 Token，支援 JSON 與 CSS 格式輸出。

---

## 7. 交付完成條件

1. **上游架構自洽**：完成 5 階段推演，具備明確的 Persona、任務目標與資訊架構。
2. **多視角互搏閉環**：無論在多 Agent 或單 Agent 模式下，皆留下清晰的「設計提案 → 對抗質疑 → 修正抗辯 → 總監裁決」記錄，所有質疑皆有合理解法或明確 Trade-off。
3. **系統度量明確**：60-30-10 色階、OKLCH 數值、模組化字階、8pt 間距與 8 狀態矩陣全部數值化具體定義，無模糊形容詞。
4. **向下游交接清晰**：輸出之規格可直接交由前端工程師切版，或交由 `frontend-anti-slop` 進行流派選型、物理物料工藝注入與瀏覽器實機渲染觀看。
