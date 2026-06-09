# Step 7: 论文写作

> 利用 Step 1-6 的所有产出，以 Zotero 条目、PDF 附件池和 `文献-Zotero架构对照.json` 作为证据底座，撰写正式学术论文。
> **核心原则：每处引用必须能追溯到 Zotero 条目与实际 PDF/笔记/标注证据，抑制大模型幻觉。**

---

## 1. 启动前读取 (Pre-read Checklist)

执行本步骤前，必须确认以下文件已加载：

- [ ] `研究主题.md` — Step 1 产出（研究方向 + 预审结论）
- [ ] `大纲关键词.md` — Step 2 产出（章节结构） + `.skill-state/term_aliases.md` 🆕
- [ ] `检索文献表.md` — Step 4 产出（参考文献 + 评分）
- [ ] `文献库.bib` — Step 4 产出（筛选后 BibTeX 文献库）
- [ ] `zotero-架构.md` — Step 6 产出（Zotero 集合结构）
- [ ] `文献-Zotero架构对照.json` — Step 6 产出（文献到集合、Zotero 条目、PDF 附件的完整机器映射；如直接基于 Zotero 写作，可由 Zotero MCP 动态生成最小映射）
- [ ] `文献-Zotero架构对照.md` — Step 6 产出（人工审阅版，可截断，不作为机器执行源；直接 Zotero 写作时可缺省）
- [ ] `pdf-附件池索引.json` — Step 6 产出（多来源 PDF 附件池、匹配状态、完整路径；直接 Zotero 写作时可缺省）
- [ ] `.skill-state/term_aliases.md` — 🆕 术语标准化映射（确保写作用词与检索一致）
- [ ] `references/literature-review-matrix-schema.md` — 综述矩阵 schema
- [ ] `references/journal-style-learning-guide.md` — 目标体裁/文档风格学习方法论（期刊、学位论文、会议论文、既有草稿均可适配）
- [ ] `references/gbt7714-2015-citation-format.md` — 引用格式规范
- [ ] `.skill-state/error_log.md` — 已知错误及修复规则

---

## 2. 适用任务 (Applicable Tasks)

- 撰写完整学术论文（paper_type × language × target_type）
- 写文献综述（review 类型专属 8 节骨架 + 7 条纪律）
- 写中英文双边摘要
- 撰写或续写学位论文、课程论文、会议论文、期刊论文的指定章节
- 基于已有草稿补写、改写、扩写其中一部分章节
- 实时引文支撑（7.7）
- 同行评审仿真 + Rebuttal 预演（7.9）
- 科研图表生成（7.10）
- 写后引用审计（7.11）

---

## 3. 不适用任务 (Non-applicable Tasks)

- 大纲生成 → 路由到 `agents/step_2_outline.md`
- 文献检索 → 路由到 `agents/step_4_search_score.md`
- 论文润色 → 路由到 `agents/step_8_polishing.md`

---

## 4. 输入要求 (Input Requirements)

| 输入 | 来源 | 格式 | 必选 |
|------|------|------|:--:|
| 研究主题 | Step 1 | .md | ✅ |
| 大纲关键词 | Step 2 | .md | ✅ |
| 检索文献表 | Step 4 | .md | ✅ |
| BibTeX 文献库 | Step 4 | .bib | ✅ |
| Zotero 架构 | Step 6 | .md/.json | ✅ |
| 文献-Zotero架构对照 | Step 6 / Zotero MCP 动态生成 | .json + .md | 推荐 |
| PDF 附件池索引 | Step 6 / Zotero MCP 动态生成 | .json | 可选 |
| Zotero 条目/PDF 附件 | Zotero 文库 | Zotero MCP | ✅ |
| 已有草稿/指定章节 | 用户提供 | .md/.docx/章节文本 | 可选 |
| 综述矩阵 | Step 7.1 | .csv/.md | 写作前生成 |
| 目标体裁/文档风格画像 | Step 7.2 | .md | 🆕 |
| 章节蓝图 | Step 7.2 | .md | 🆕 |

> Step 7 不再直接把 `paper-temp/*.pdf` 当作唯一知识库。PDF 可以来自 Step 5、原有文件、后续补下载、手动整理目录，或已经存在于 Zotero 条目附件中。若 `pdf-附件池索引.json` 不存在，但 Zotero 条目已带 PDF 附件，则以 Zotero MCP 的 `zotero_get_item_children` / `zotero_get_attachment_path` / `zotero_get_item_fulltext` 为准，必要时再生成临时 `pdf-附件池索引.json` 供审计复用。

**独立入口规则：**
如果用户已有 Zotero 文库、已有草稿、已有参考文献、已有 PDF 目录或只要求撰写/续写指定章节，可直接从 Step 7 开始，不要求补跑 Step 1-6。Agent 应先构造最小证据映射：目标章节、大纲片段、可用 Zotero/PDF/笔记证据、引用风险；只有证据不足影响关键 claim 时，才触发 `CP-CITATION-WARN` 或建议回退补证据。

---

## 5. 标准输出 (Standard Outputs)

| 输出 | 格式 | 说明 |
|------|------|------|
| 综述矩阵 | CSV/Markdown | 13 列证据矩阵 |
| research_dossier/ | 目录 | 样本状态 + 目标体裁/文档风格画像 + 章节蓝图 + 写作逻辑矩阵 |
| 论文初稿 | .md / .docx | 含完整结构和参考文献 |
| 指定章节草稿 | .md / .docx | chapter-only / continue-existing 模式产出 |
| 中→英术语对照表 | .md | zh-to-en 模式额外产出 |
| 评审报告 + rebuttal-预演 | .md → .pdf | 7.9 质量门产出 |
| 图表 | SVG/PDF/TIFF | 7.10 产出，保存到 figures/ |
| 引用审计报告 | .md → .pdf | 7.11 产出 |

---

## 6. 执行流程 (Execution Flow)

### 前置输入

写作开始前，确认以上所有前置输入文件可访问。Step 7 支持两种入口：

| 入口 | 适用场景 | 必要条件 | 处理方式 |
|------|----------|----------|----------|
| Step 6 产物入口 | 已按本工作流完成 Zotero 架构、对照和附件池 | `文献-Zotero架构对照.json`、Zotero 条目、PDF 附件 | 直接按 JSON 映射读取证据 |
| Zotero 直接入口 | 用户已有 Zotero 文库，未生成本工作流的附件池索引 | Zotero 集合/条目可读，核心条目有 PDF/笔记/标注 | 通过 Zotero MCP 动态读取条目、附件、笔记和全文，并生成最小映射 |

**缺少 `pdf-附件池索引.json` 时：**
1. 不阻塞写作。
2. 先用 Zotero MCP 读取目标集合或用户指定条目的 children/attachments。
3. 能获取本地路径时，动态写入或刷新 `pdf-附件池索引.json`。
4. 不能获取本地路径但能通过 `zotero_get_item_fulltext` 读到全文时，仍可生成综述矩阵和写作证据，但审计报告中标记 `pdf_path_unavailable`。
5. 如果条目既无附件、又无笔记/标注/全文，但有完整摘要和可靠元数据，则可作为“摘要级证据”；如果连摘要也缺失，则只能作为“元数据候选”。

**Step 7 的功能边界：**

| 子步骤 | 核心功能 | 主要输入 | 主要输出 |
|--------|----------|----------|----------|
| 7.1 | 生成文献证据矩阵 | Zotero 条目/笔记/标注、PDF 附件、对照 JSON | `综述矩阵.csv/.md` |
| 7.2 | 学习目标体裁/文档风格并生成章节蓝图 | 目标样本文献/学位论文规范/已有草稿、Step 2 大纲、综述矩阵 | `research_dossier/` |
| 7.3 | 论文类型、目标体裁与语言识别 | 研究主题、大纲、投稿/毕业/课程目标 | paper_type + target_type + language |
| 7.4 | 写作模式选择 | 写作范围、已有草稿、用户任务 | full / chapter-only / continue-existing 等 |
| 7.5 | 语言差异化规则 | language、术语表、目标体裁 | 术语与语言规范 |
| 7.6 | 章节级写作规则 | 大纲、矩阵、风格画像、已有草稿 | `论文初稿.md/.docx` 或指定章节草稿 |
| 7.7 | 实时引文支撑 | 已入库 Zotero 文献为主，新文献走回流闭环 | 段落引用匹配报告 |
| 7.8 | 防幻觉机制 | 引用、证据等级、JSON 追溯 | 引用安全规则 |
| 7.9 | 同行评审仿真 | 初稿、矩阵、风格画像 | `评审报告.md` + `rebuttal-预演.md` |
| 7.10 | 科研图表生成 | 初稿、数据文件、图表规范 | `figures/` + 图表清单 |
| 7.11 | 写后引用审计 | 初稿、Zotero 条目、PDF/笔记/标注证据 | `引用审计报告.md` |

### 7.1: 生成文献证据矩阵（写作前证据组织）

**13 列矩阵：** 作者年份 | 标题 | 研究问题 | 理论/概念 | 数据/样本 | 方法 | 核心发现 | 贡献 | 局限 | 与我的主题关系 | 可引用摘录 | 我的笔记 | DOI/URL

**输入优先级：**
```
0. 文献-Zotero架构对照.json / Zotero 动态映射     ← 机器主索引：tier/score/collection/zotero_item_key/pdf_path
1. Zotero 笔记 (zotero_get_notes)              ← 最高质量人工证据
2. PDF 标注/高亮 (zotero_get_annotations)       ← 精读标注
3. Zotero 元数据 (zotero_get_item_metadata)     ← 标题/作者/DOI/摘要/URL/Extra/source_id
4. PDF 全文 (zotero_get_item_fulltext)          ← 完整原文
5. BibTeX/中文元数据 JSON/摘要                  ← 摘要级证据，只能支撑低风险概括
```

> 不要一上来就读 PDF 全文。优先用 `文献-Zotero架构对照.json` 确定 T1/T2/T3、集合归属、Zotero item key 和 PDF 状态；如果该 JSON 不存在，则先从 Zotero 集合/标签/条目动态生成最小映射，再逐级读取笔记、标注、元数据和全文；`.md` 只用于人工审阅。

**纳入范围：**
- T1/T2/T3 均进入综述矩阵。T1/T2 是写作主证据，T3 作为背景、补充、反例或方法参照。
- T4 已在 Step 4 剔除，默认不进入 Step 7；如用户要求补充，只能作为“候选补查文献”，不得直接引用。
- 中文文献必须保留中文标题、作者、来源、年份、source/source_id、article_url；无真实 DOI 时不得用 `cnki.xxx` / `wanfang.xxx` 冒充 DOI。
- 写作优先使用 `VERIFIED` / `VERIFIED_LOCAL` 且 Tier 为 T1/T2 的文献；T3 主要作背景、补充、反例或方法参照。
- `WARN` 文献只能用于背景性描述、研究脉络或待补查线索，不能支撑关键结论、实验参数、性能提升、机制证明或强因果判断。
- `REJECT` 文献不得进入综述矩阵、正文引用或 Zotero 写入计划；若用户要求保留，只能放入“补查候选/异常清单”。

**仅有元数据/完整摘要的条目用途：**

| 证据状态 | 可用于 | 不可用于 | 引用强度 |
|----------|--------|----------|----------|
| 完整元数据 + 完整摘要，无 PDF | 综述矩阵的研究问题/方法概述/主题归类/背景句/待精读优先级 | 具体数据、实验参数、模型细节、强结论、页码级原文摘录 | Weak/Background |
| 完整元数据，无摘要、无 PDF | 去重、集合归类、检索补全、参考文献候选 | 正文 claim 支撑 | Candidate only |
| 元数据 + Zotero 笔记/标注，无 PDF | 若笔记/标注明确记录原文依据，可支撑对应 claim；同时标记需补 PDF | 超出笔记/标注范围的细节 | Moderate，需补全文 |
| Step 4 `WARN` 文献 | 背景、研究脉络、待补查线索 | 关键结论、强 claim、实验数据、机制证明 | Weak/Background |

> 摘要可以派上用场，但不能被当作全文。它适合判断“这篇文献研究什么、用了什么大类方法、与主题是否相关”，不适合支撑“作者具体发现了多少、参数如何设置、机制如何证明”这类强断言。

**缺失值约定：** `未提及`（论文确实未讨论）/ `待补充`（计划后续补全）/ `推断：{内容}`（基于已有信息合理推断）

### 7.2: 目标体裁/文档风格学习与写作蓝图

**核心理念：** paper_type 轴告诉你"写什么类型的论文"，目标体裁/文档风格学习告诉你"这份文本应该按什么规范、结构深度和语言节奏来写"。目标可以是期刊，也可以是学位论文、会议论文、课程论文、开题报告，或用户已有草稿的既有风格。

**目标类型：**

| target_type | 适用场景 | 风格/结构依据 |
|-------------|----------|---------------|
| `journal` | 目标期刊论文 | 目标期刊近期样文、author guidelines、投稿模板 |
| `thesis` | 硕士/博士学位论文 | 学校论文规范、学院模板、已有章节、大纲结构 |
| `conference` | 会议论文 | 会议模板、页数限制、领域样文 |
| `course-paper` | 课程论文/阶段报告 | 课程要求、教师给定格式、已有材料 |
| `existing-draft` | 已有部分内容，只续写/改写一部分 | 用户已有草稿的术语、语气、标题层级、引用格式 |

**写作范围：**
- `full-document`：从大纲开始撰写完整论文。
- `chapter-only`：只撰写一个或多个指定章节，如“绪论”“文献综述”“方法”“讨论”。
- `continue-existing`：在已有草稿基础上续写、补写或局部替换。
- `abstract-only`：只写中文摘要、英文摘要或双边摘要。
- `revision-only`：不新增主体内容，只根据证据和风格规则修改已有章节。

**工作流：**
```
Step 7.2-0: 样本盘点      → style_sample_status.md/json (样本来源、数量、缺口、回退策略)
Step 7.2-1: 风格剖析      → style_profile.md             (四维度量化：格式化/结构/引用/语言)
Step 7.2-2: 章节蓝图      → section_blueprints.md         (逐节写作计划：论证链+证据映射+图表位置)
Step 7.2-3: 写作逻辑矩阵  → writing_rationale_matrix.md    (逐单元理由)
Step 7.2-4: LaTeX 校验    → latex_check.md（可选）
```

**两种分析深度：**

| 模式 | 范文数 | 时长 | 产出 | 适用场景 |
|------|:---:|------|------|------|
| **Flash** | 3 篇 | ~3 min | `style_profile.md` | 初次投稿该期刊 |
| **Pro** | 6 篇 | ~8 min | `style_profile.md` + `research_dossier.md` | 核心目标期刊/学位论文/既有草稿 |

```bash
python3 scripts/learn_journal_style.py --target-type journal --target-name "Applied Thermal Engineering" --sample-source zotero --collection "目标期刊样本" --mode flash
python3 scripts/learn_journal_style.py --target-type thesis --target-name "硕士学位论文" --sample-source draft --draft 论文已有草稿.md --mode flash
python3 scripts/generate_section_blueprints.py research_dossier/style_profile.md 大纲关键词.md --evidence 综述矩阵.csv --output research_dossier/
python3 scripts/generate_writing_rationale.py research_dossier/section_blueprints.md --style-profile research_dossier/style_profile.md --output research_dossier/writing_rationale_matrix.md
```

> 目标样本是“风格学习语料”，不等同于 Step 4 的主题文献库。样本可来自目标期刊近期代表作、学位论文模板、学校格式规范、用户指定 PDF 目录、Zotero 样本集合或已有草稿；不得默认使用 `paper-temp/` 中的全部研究文献作为目标风格样本。

**样本集合命名约定：**

| target_type | 推荐 Zotero 集合名 | 说明 |
|-------------|--------------------|------|
| `journal` | `目标风格样本 / 期刊-{target_name}` | 目标期刊近期样文、投稿模板、author guidelines |
| `thesis` | `目标风格样本 / 学位论文-{学校或层级}` | 学校模板、学院规范、优秀学位论文、已有章节 |
| `conference` | `目标风格样本 / 会议-{target_name}` | 会议模板、页数限制、领域样文 |
| `course-paper` | `目标风格样本 / 课程论文-{课程名}` | 课程要求、评分 rubrics、已有材料 |
| `existing-draft` | `目标风格样本 / 已有草稿-{项目名}` | 用户草稿、已定稿章节、导师修改稿 |

> 集合名只是推荐约定，不是硬性要求；如果用户直接提供目录、文件或草稿，也可以作为样本源。但 7.2 必须把实际使用的样本写入 `style_sample_status.md/json`。

**样本来源规则：**
1. 优先使用用户指定的样本 PDF、Zotero 集合、学校模板、投稿模板或已有草稿。
2. `journal` 未指定样本时，可从 Step 4/6 中筛选 `publication_title` 与目标期刊一致的近期 T1/T2 文献。
3. `thesis` 未指定样本时，使用学校/学院格式规范和已有章节；没有规范时先生成通用学位论文蓝图并标记待确认。
4. 样本不足时，先报告缺口，再建议补充目标样本；不要把非目标体裁文本混入风格画像。
5. 风格学习只学习结构、语气、引用密度、图表呈现和章节节奏；不得复制句子或段落。

**样本数量与回退策略：**

| 状态 | 样本条件 | 处理方式 | confidence |
|------|----------|----------|------------|
| 充足 | `journal/conference` ≥ 3 篇；`thesis` ≥ 1 个模板/规范 + 1 篇样文或已有章节；`existing-draft` ≥ 1500 字 | 正常生成风格画像和章节蓝图 | high |
| 偏少 | `journal/conference` 1-2 篇；`thesis` 只有模板/规范或只有已有章节；`existing-draft` 500-1500 字 | 生成低样本风格画像，标记缺口，不阻塞写作 | medium |
| 缺失 | 无可用样本，仅有 target_type / target_name | 使用通用体裁规则 + Step 2 大纲，必须提示用户补样本 | low |

**`style_sample_status.md` 推荐格式：**

```md
# 目标风格样本状态

target_type: thesis
target_name: 硕士学位论文
sample_source: existing_draft + university_template
sample_count: 2
confidence: medium

## 已使用样本
1. 论文已有草稿.md
2. 学校硕士论文模板.docx

## 缺口
- 缺少优秀学位论文样本
- 缺少学院具体格式细则

## 回退策略
使用学校模板 + 已有草稿风格 + 通用硕士论文结构规则。
```

**`style_sample_status.json` 最低字段：**

```json
{
  "target_type": "thesis",
  "target_name": "硕士学位论文",
  "sample_source": ["existing_draft", "university_template"],
  "sample_count": 2,
  "confidence": "medium",
  "samples": [
    {"title": "论文已有草稿.md", "source_type": "draft", "path_or_zotero_key": "论文已有草稿.md"},
    {"title": "学校硕士论文模板.docx", "source_type": "template", "path_or_zotero_key": "学校硕士论文模板.docx"}
  ],
  "gaps": ["缺少优秀学位论文样本", "缺少学院具体格式细则"],
  "fallback_strategy": "使用学校模板 + 已有草稿风格 + 通用硕士论文结构规则"
}
```

### 7.3: 论文类型、目标体裁与语言识别

**轴一：论文类型（paper_type）**

| paper_type | 特征 | 典型章节骨架 |
|------------|------|-------------|
| **research** | 有明确的实验/仿真研究 | intro → related-work → method → experiments → discussion → conclusion |
| **methods** | 侧重方法/工具创新 | intro → problem-statement → design → implementation → validation → comparison |
| **hypothesis** | 先提假设再做实验检验 | background → hypothesis → test-design → results → implications |
| **algorithmic** | 算法/模型为核心贡献 | intro → preliminaries → algorithm → analysis → experiments → related-work |
| **review** | 系统综述/调研 | 8 节文献综述骨架 |

**轴二：语言 / 投稿目标（language）**

| language | 场景 | 引用格式 |
|----------|------|---------|
| **en** | 直接用英文撰写 | IEEE / APA / Nature |
| **zh** | 用中文撰写 | GB/T 7714 |
| **zh-to-en** | 中文草稿→英文成稿 | 按目标体裁/投稿目标 |

**轴三：目标体裁（target_type）**

| target_type | 写作重点 |
|-------------|----------|
| **journal** | 问题集中、贡献明确、篇幅紧凑、结果导向 |
| **thesis** | 结构完整、背景充分、方法细节完整、论证链清楚 |
| **conference** | 篇幅受限、贡献和实验结果前置 |
| **course-paper** | 符合课程要求，重视概念解释和规范表达 |
| **existing-draft** | 保持已有章节风格、术语、编号、引用格式一致 |

### 7.4: 写作模式选择

| 模式 | 触发场景 |
|------|----------|
| `full` | 已有清晰大纲和文献，直接逐章完整撰写 |
| `outline-only` | 不确定结构，先生成详细大纲 |
| `plan` | 需要多轮引导交互来厘清论点 |
| `abstract-only` | 仅写中英文摘要 |
| `argument-first` | 先写一句话核心论点，确保方向正确再展开 |
| `chapter-only` | 只写一个或多个指定章节 |
| `continue-existing` | 已有部分内容，只补写、续写或局部改写 |

**已有草稿处理规则：**
- 先识别已有草稿的标题层级、术语、引用格式、语气和章节编号。
- 新写内容必须与已有内容保持结构和语言一致，除非用户明确要求重构。
- 只写部分章节时，不擅自改动其他章节；只在必要处提出“需前后文同步”的提示。
- 如果已有草稿中的引用缺证据，标记为 `needs_evidence_audit`，不要默认删除。

### 7.5: 语言差异化规则

**zh-to-en 特殊规则（中国研究者最常用场景）：**
1. 术语锁定：写作开始前先列出"中→英关键术语对照表"
2. 中文笔记→英文翻译四步法（提取论点→按英文逻辑重排序→英文撰写→检查翻译腔）
3. 识别中文写作特有的"英文不该有"的模式
4. 中文数字和单位的英文转换

### 7.6: 章节级写作规则

**摘要：** en: 150-250 words / zh: 300-500 字 | 结构：问题→方法→关键结果→意义

**引言/绪论：** 三层递进（大背景→子领域 gap→本文贡献 3-5 条）| 贡献条目标注对应章节

**相关工作/文献综述：** 按主题分组，**禁止按论文逐条罗列** | 每组末尾对比"本文与这些工作的不同"

**方法/实验方案：** 先符号后公式 | 按逻辑顺序非时间线 | 图表在引用后出现

**实验与结果：** 以研究问题开头 | 图表自包含 | 数据→分析→解释三层递进

**结论：** 不是摘要的复读 | 诚实说局限（2-3 条） | 具体未来方向

#### 7.6.1 段落与句子级自查

**① 每段一个工作（One paragraph, one job）：** 8 种可选类型：context / gap / approach / result / comparison / mechanism / implication / limitation

**② 从证据向外写：** 证据/数据 → 解释 → 结论

**③ 校准动词强度：** show/demonstrate → suggest/indicate → may/could

**④ 清除虚假新颖性声明：** 扫描 first/novel/unprecedented 等词的滥用

**⑤ 段落流检查：** 一段一个信息，首句是主题句，后续句与上句有显式关系

#### 7.6.2 术语对齐检查

- 每章写作前，确认本章核心术语与 `.skill-state/term_aliases.md` 中 Recommended page 匹配
- 中文论文：全篇统一使用 Main Term 的中文形式
- 英文论文：全篇统一使用 Main Term 的英文形式
- 同一概念在全文中的术语形式不超过 1 个（禁止同义词轮换）

### 7.7: 实时引文支撑

**分段引用工作流（Zotero 优先）：**
```
写完一段正文 →
  ① Segment — 将段落拆为可引用的 claim 片段
  ② Parse — 每个 claim 提取关键词 + 判断是否需要新引用
  ③ Match — 优先在综述矩阵、文献-Zotero架构对照.json、Zotero 集合内匹配已有证据
     优先级：VERIFIED/VERIFIED_LOCAL + T1/T2 → VERIFIED/VERIFIED_LOCAL + T3 → WARN 背景性用途
  ④ Read — 读取 Zotero 笔记/标注/元数据；必要时读取 PDF 全文页段
  ⑤ Evaluate — 判断 Strong/Moderate/Weak，并记录支撑句或证据位置
  ⑥ Report — 每段写完后简要报告引文匹配结果
  ⑦ 用户确认后写入引用标注，并记录 zotero_item_key / citekey
```

**引用密度指南：** 引言每 2-3 句 1 条 | 相关工作每段 3-8 条 | 方法每段 1-2 条 | 实验每段 1-3 条 | 讨论每段 2-4 条 | 结论 0-1 条

**摘要级引用规则：**
- 只有完整摘要、无 PDF 的条目，可以用于背景性、领域概况性、研究主题归类性引用。
- 引用标记必须记录为 `evidence_level=abstract_only`，7.11 审计时单独列出。
- 不得用摘要级证据支撑具体实验数据、参数、机制解释、效果提升百分比或“证明/证实”类强动词。
- 写作主证据不足时，应回到 Step 5/6 补 PDF 或补全文，而不是提高摘要级证据的强度。

**新增引用回流规则：**
- 如果现有 Zotero 文库无法支撑某个 claim，不允许现场编造或只凭网页摘要引用。
- 新引用必须走 Step 4/6 小闭环：检索/评分 → 加入 `文献库.bib` 或增量 bib → 补充中文元数据 → PDF 下载/附件池匹配 → Zotero 入库 → 更新 `文献-Zotero架构对照.json` → 再进入 7.7。
- 紧急写作时可在段落中保留 `[待补引用: claim]`，但不得进入最终稿。

### 7.8: 防幻觉机制（核心）

| 机制 | 说明 |
|------|------|
| **先读后写** | 引用某篇文献前，必须读取 PDF 全文 |
| **交互确认** | 每章写前与用户沟通参考哪几篇 PDF |
| **索引必达** | 每处引用标注索引号 |
| **不编造引用** | 未读取过 PDF 的文献，不得引用 |
| **原文比对** | 引用具体数据时注明 PDF 来源 |
| **JSON 追溯** | 每条引用能追溯到 `文献-Zotero架构对照.json` 的 citekey/zotero_item_key/pdf_path |
| **中文元数据完整** | 中文引用必须核对 title/authors/year/publication/source_id/article_url，不依赖 DOI |
| **摘要级降权** | 只有摘要无全文的条目必须标记为 abstract_only，不能支撑强 claim |
| **可信度降权** | Step 4 `WARN` 条目只能作背景；`REJECT` 条目禁止进入正文引用 |

### 7.9: 同行评审仿真（质量门）

五维度评分（0-10 分 + 权重）：原创性 20% / 方法严谨性 25% / 证据充分性 25% / 论证连贯性 15% / 写作质量 15%

三审稿人视角：Reviewer A（方法严谨性）/ Reviewer B（创新性）/ Reviewer C（清晰度与完整性）

Rebuttal Letter 预演：不等真实投稿，在质量门阶段就预演 rebuttal——暴露"以为能说服审稿人、实际说服不了"的薄弱环节。

**限 2 轮修改。** 评分 < 5 的维度 → 回到对应步骤补足。

### 7.10: 科研图表生成 🆕

支持 10 种图表类型（grouped_bar / stacked_bar / trend_line / heatmap_seq / heatmap_div / bubble_scatter / radar_polar / gridspec / fill_between）。

```bash
python3 scripts/generate_figures.py 论文初稿.md --data data/ --output figures/
```

设计规则：三级信息层次 / 直标优于图例 / 无反冗余面板 / 低饱和度配色 / 绿色红色仅用于方向性。

### 7.11: 写后引用审计 🆕

> 核心目的：抓"LLM 把标题相关的论文当成支撑某个具体声明的论文"这种张冠李戴。

```
稿件 → 提取所有引用标记 [1][2]...[N] → 逐条：
  ① 通过 citekey / zotero_item_key 定位 Zotero 条目与对照 JSON 记录
  ② 读取 Zotero 笔记、PDF 标注、元数据、PDF 全文证据
  ③ 定位稿件中引用该论文的具体声明（claim sentence）
  ④ 判断：原文/笔记/标注是否支撑这个 claim？
     ✅ 支撑 / 🟡 弱支撑 / ❌ 不支撑
  ⑤ 输出审计报告
```

```bash
python3 scripts/citation_audit.py 论文初稿.md --mapping 文献-Zotero架构对照.json --pdf-index pdf-附件池索引.json --output 引用审计报告.md
# 若没有附件池索引，但引用均能定位到 Zotero 条目：
python3 scripts/citation_audit.py 论文初稿.md --zotero-collection "论文文献库" --output 引用审计报告.md
```

四种误引模式：标题-摘要张冠李戴 / 综述当实证 / 贡献过度归因 / 数据编造

> Crossref / Semantic Scholar 摘要只能作为补充核验，不能替代 Zotero 条目和 PDF 原文。CNKI/万方中文文献尤其必须以本地元数据、详情页 URL、PDF 原文和 Zotero Extra/source_id 为审计依据。

### CHECKPOINT W — CP-CITATION-WARN

当 `WARN` 文献、弱引用、摘要级证据、无 PDF 条目或审计中的“不支撑/弱支撑”将被用于关键 claim 时，必须输出 checkpoint 块并等待用户明确确认。普通背景性描述、研究脉络说明、综述矩阵候选记录和待补查清单不触发 checkpoint。`REJECT` 仍禁止进入正文关键引用和 Zotero 写入计划。

```md
## CHECKPOINT W — CP-CITATION-WARN

entry_mode: normal_chain|direct_entry|resume|repair|partial_artifact
status: blocked
blocks_next: using risky evidence in key claims
must_confirm: true

summary:
- 列出异常文献/引用、风险类型和受影响 claim。

user_options:
1. 删除或替换异常引用
2. 保留但标注为背景/待补证据
3. 回退 Step 4/5/6 小闭环补证据
4. 逐条人工审查

does_not_block:
- WARN 文献用于背景性描述、研究脉络或待补查线索
- 摘要级证据用于领域概况、主题归类或精读优先级判断
- 综述矩阵中的候选记录、异常清单和低风险描述性整理

required_confirmation:
- “确认 CP-CITATION-WARN”
```

---

## 7. 质量门槛 (Quality Gates)

- [ ] paper_type 和 language 已识别
- [ ] 7.1 文献证据矩阵：13 列完整，证据优先级规则已遵循
- [ ] 7.2 目标体裁/文档风格：`style_sample_status.md/json` 已生成，Flash 或 Pro 模式已完成，style_profile.md 已生成
- [ ] 防幻觉机制：每处引用均来自 Zotero 条目和实际 PDF/笔记/标注证据
- [ ] T1/T2/T3 覆盖：矩阵覆盖 Step 6 中所有 T1/T2/T3，写作引用优先使用 T1/T2，T3 用途已标明
- [ ] Step 4 可信度约束：关键 claim 均由 `VERIFIED` / `VERIFIED_LOCAL` 文献支撑；WARN 仅作背景；REJECT 未进入正文
- [ ] 7.6.1 段落自查：每段一个工作 / 从证据向外写 / 动词校准 / 无虚假新颖性 / 段落流
- [ ] 🆕 术语对齐：核心术语与 `.skill-state/term_aliases.md` 一致
- [ ] 7.9 同行评审：五维评分全部 ≥ 5 分（<5 分已回退修复）
- [ ] 7.11 引用审计：❌ 不支撑引用已移除或替换

---

## 8. 收尾检查 (Closing Checks)

### 产出完整性
- [ ] `论文初稿.md` 已生成
- [ ] `论文初稿.docx` 已自动生成
- [ ] `综述矩阵.csv` + `综述矩阵.md` 已生成
- [ ] 目标体裁/文档风格产出：`research_dossier/` 目录完整，含 `style_sample_status.md/json`
- [ ] `评审报告.md` + `rebuttal-预演.md` 已生成
- [ ] `引用审计报告.md` 已生成
- [ ] figures/ 目录图表完整

### 术语对齐检查 🆕
- [ ] 逐章扫描核心术语，确认与 `.skill-state/term_aliases.md` 一致
- [ ] 发现术语不一致 → 修正为 Main Term → 如 Main Term 不当 → 更新 term_aliases.md → 记录到 decision_log.md

### 错误日志更新 🆕
- [ ] 本轮是否出现新的 AI 操作错误？
  - 引用编造 → 追加到 `.skill-state/error_log.md`
  - 综述矩阵证据填充错误 → 追加到 `.skill-state/error_log.md`
  - 目标体裁/文档风格分析偏差 → 追加到 `.skill-state/error_log.md`
  - 术语混用 → 追加到 `.skill-state/error_log.md`
  - 7.11 审计发现系统性误引 → 追加到 `.skill-state/error_log.md`

### 决策日志更新 🆕
- [ ] 是否调整了章节结构？→ 记录到 `.skill-state/decision_log.md`
- [ ] 是否修改了 paper_type 判定？→ 记录到 `.skill-state/decision_log.md`

### 下一步提示
- [ ] 向用户明确说明下一步：论文润色（Step 8）
  > **下一步 → Step 8：** 同行评审通过 + rebuttal 预演无遗漏 + 引用审计无重大问题后，进入精炼润色、去 AI 痕迹，提升至可投稿水平。

---

## 9. 故障排除 (Troubleshooting)

常见问题参见 `agents/known_pitfalls.md`。本 Step 特有的问题：

- **引用不足**：运行 7.7 扩展搜索补充引用；检查引用密度指南
- **现有 Zotero 文库不能支撑 claim**：回到 Step 4/6 小闭环补文献、补 PDF、补入库，再继续写作
- **AI 痕迹明显**：7.6.1 自查步骤逐项检查；Step 8 Level 3 去 AI 化
- **引用审计大量不支撑**：7.11 逐条处理，❌ 级别优先替换或移除
- **术语不一致**：回查 `.skill-state/term_aliases.md`，全篇统一为 Main Term
