# 决策日志 (Decision Log)

> 跨会话积累的结构性设计决策。当工作流规则、评分标准、章节骨架、下载策略等发生变更时，
> 记录决策背景和影响范围。供后续使用者和 AI agent 理解"为什么当初这样设计"。
>
> 设计原则：**每个非显而易见的决策都应留下可追溯的记录。**
> 借鉴来源：ResearchWiki `memory/decision_log.md`。

## 记录格式

每条决策记录包含以下字段：

| 字段 | 说明 |
|------|------|
| **日期** | 决策日期 (YYYY-MM-DD) |
| **Decision** | 决策内容（一句话概括） |
| **Reason** | 为什么做这个决策（背景、约束、替代方案及放弃原因） |
| **Impact** | 影响范围（哪些 Step、哪些 agent 文件、哪些产出） |
| **Status** | 状态（提议 / 已采纳 / 已废弃 / 已替代） |
| **Related error** | 关联的错误日志条目（如有） |

---

## 决策记录

<!-- 
格式模板（新决策追加到下方）：

### YYYY-MM-DD | 决策标题 | 状态
- **Decision:** 
- **Reason:** 
- **Impact:** 
- **Status:** 
- **Related error:** 
-->

### 2026-06-05 | SKILL.md 拆分为 Agent 模块 | 已采纳
- **Decision:** 将 3284 行 SKILL.md 拆分为 ~200 行轻量路由器 + `agents/` 目录下 9 个独立 agent 文件
- **Reason:** 单文件过长导致 AI 上下文消耗过大；独立 agent 文件可按需加载，降低 token 消耗；ResearchWiki 已验证此模式的可行性；每个 agent 文件遵循标准 9 段模板，行为可预测、可审计
- **Impact:** 所有 Step；新增 `agents/` 目录 + `references/error_log.md` + `references/decision_log.md` + `references/term_aliases.md`
- **Status:** 已采纳
- **Related error:** —

### 2026-06-05 | Step 7 Agent 保持合并（暂不拆分子步骤） | 已采纳
- **Decision:** Step 7（写作、7g 图表、7h 引用审计）暂不拆分为独立 agent 文件，保持在 `agents/step_7_writing.md` 中
- **Reason:** 7g（~101 行）和 7h（~63 行）与写作流程紧密耦合；分散到独立文件会增加 agent 加载次数；设定阈值为 1000 行——超过时自动触发拆分
- **Impact:** `agents/step_7_writing.md` 约 938 行（原 898 + 模板开销 40）
- **Status:** 已采纳
- **Related error:** —

### 2026-06-05 | 术语标准化机制基于 term_aliases.md | 已采纳
- **Decision:** 采用 `references/term_aliases.md` 文件作为跨步骤术语标准化机制，Step 2 填充 → Step 3 检索 → Step 7 写作 → Step 8 校验
- **Reason:** 解决"Step 2 用 liquid cooling，Step 7 写成 water cooling"的不一致问题；ResearchWiki 已验证 term_aliases 模式的可行性；无需新增 Python 脚本，纯规则约束
- **Impact:** Step 2/3/7/8 的 agent 文件；新增 `references/term_aliases.md`
- **Status:** 已采纳
- **Related error:** —
