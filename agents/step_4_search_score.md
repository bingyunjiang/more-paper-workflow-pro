# Step 4: 多渠道检索与相关性筛选

> 按 Step 3 方案的 L1→L2→L3 分层路由逐子课题检索，对结果进行 5 维度评分和 Tier 分级筛选。

---

## 1. 启动前读取 (Pre-read Checklist)

执行本步骤前，必须确认以下文件已加载：

- [ ] `agents/step_3_search_plan.md` — 检索方案（含 L1→L2→L3 路由和概念块布尔查询）
- [ ] `references/search-query-frameworks.md` — 检索查询框架参考
- [ ] `references/error_log.md` — 已知错误及修复规则
- [ ] `references/decision_log.md` — 影响本 Step 的结构性决策

---

## 2. 适用任务 (Applicable Tasks)

- 按检索方案的 L1→L2→L3 分层路由逐子课题执行文献检索
- 对检索结果进行引文验证（DOI 有效性 + 元数据完整性）
- 多源检索结果 DOI 去重合并
- 五维度相关性评分（主题匹配度/方法学严谨性/来源质量/时效性/影响力）
- Tier 分级筛选（T1/T2/T3/T4）
- 统一 .bib 导出（含评分标签和子课题归属）

---

## 3. 不适用任务 (Non-applicable Tasks)

以下任务不属于本 Step 范围：

- 检索方案设计 → 路由到 `agents/step_3_search_plan.md`
- PDF 下载 → 路由到 `agents/step_5_download.md`
- 文献综述矩阵 → 路由到 `agents/step_6_zotero.md`

---

## 4. 输入要求 (Input Requirements)

| 输入 | 来源 | 格式 | 必选 |
|------|------|------|:--:|
| 检索方案 | Step 3 | .md | ✅ |
| 检索执行参数 | 检索方案中的 L1/L2/L3 路由配置 | 文本 | ✅ |

---

## 5. 标准输出 (Standard Outputs)

| 输出 | 格式 | 说明 |
|------|------|------|
| 检索文献表 | .md / .xlsx | 含评分列的文献表格 |
| 检索文献表 PDF | .pdf | 自动由 md_to_pdf.py 生成 |
| 文献库 | .bib | 统一 BibTeX 格式，含 Tier/Score 标签 + 子课题归属 |

---

## 6. 执行流程 (Execution Flow)

### 检索执行

按 Step 3 方案的 L1→L2→L3 分层路由逐子课题检索：

```bash
# L1 OpenAlex：每子课题跑 3 策略（relevance + cited + recent），每策略 50 条
python3 scripts/search_by_topic.py --bool query_plan.json \
  --source openalex --strategy relevance --limit 50 --output s1_l1_rel.bib
python3 scripts/search_by_topic.py --bool query_plan.json \
  --source openalex --strategy cited --limit 50 --output s1_l1_cited.bib
python3 scripts/search_by_topic.py --bool query_plan.json \
  --source openalex --strategy recent --limit 50 --output s1_l1_recent.bib

# L2 Semantic Scholar：CS 交叉子领域并行，传统工科在 L1<30 时回退
python3 scripts/search_by_topic.py --bool query_plan.json \
  --source semantic_scholar --limit 50 --output s1_l2.bib

# 传统用法（向后兼容，不使用概念块）：
python3 scripts/search_by_topic.py "cold plate liquid cooling optimization" \
  --t1 openalex --t2 semantic_scholar --limit 50 --output s1_results.bib
```

### 4a: 引文验证

在评分之前先验证——剔除 DOI 无效、元数据残缺的条目，避免后续下载白费功夫。

```
检索结果 → 逐条验证：
  ① DOI 格式合法性（正则 + Crossref API 校验）
  ② 元数据完整性：title / authors / year / journal 是否在结果中存在
  ③ 标记问题条目：
     ⚠️ DOI 无效 → 跳过（无法下载）
     ⚠️ 缺作者/年份 → 尝试从 Crossref 补全
     ✅ 完整 → 进入评分
```

### 4b: DOI 去重

多源检索会产生重复（同一篇论文从 Semantic Scholar 和 Crossref 各返回一次）：

```
去重策略：
  - 主键：DOI（大小写 + 前缀统一后比对）
  - 无 DOI 时：title + first_author + year 组合键
  - 冲突时保留元数据最完整的条目
```

### 相关性评分（v3.0 五维度）

检索结果按以下维度打分（每项 0-5 分，满分 25）：

| 维度 | 权重 | 说明 |
|------|:----:|------|
| 主题匹配度 | **35%** | 标题+摘要与研究主题的相关程度；同一论文出现在 ≥2 条策略线中 → 该维度满分 |
| 方法学严谨性 | **20%** | 采用的方法/实验设计是否可靠——有实验验证 > 纯仿真，有对照实验 > 无对照 |
| 来源质量 | **15%** | 期刊/会议等级（SCI 一区/CCF-A > 二区 > 三区/四区 > 无检索） |
| 时效性 | **15%** | 近 3 年 5 分，近 5 年 4 分，近 10 年 3 分，更早 2 分 |
| 影响力 | **15%** | 引用量 + Semantic Scholar influentialCitationCount |

### 筛选标准

| 等级 | 分数范围 | 处理 |
|------|---------|------|
| ⭐ Tier 1 | ≥20 | 核心文献，必须下载 |
| 📘 Tier 2 | 15-19 | 重要文献，尽量下载 |
| 📄 Tier 3 | 10-14 | 参考文献，有选择下载 |
| ⬜ Tier 4 | <10 | 剔除 |

### 4c: 统一 .bib 导出

```bash
# 将检索文献表转换为 .bib（含评分注释）
python3 scripts/search_by_topic.py --export-bib 检索文献表.md --output 文献库.bib

# 转换格式（如需要）
python3 scripts/search_by_topic.py --convert 文献库.bib --to ris  # → Zotero/EndNote
python3 scripts/search_by_topic.py --convert 文献库.bib --to nbib # → PubMed
```

**.bib 文件含评分标签：**
```bibtex
@article{liu_topology_2025,
  title     = {Topology Optimization of Cold Plate Flow Channels...},
  author    = {Liu, ... and Zhang, ...},
  journal   = {Applied Thermal Engineering},
  year      = {2025},
  doi       = {10.1016/j.applthermaleng.2025.127040},
  note      = {Tier 1 | Score: 22/25 | S1: 冷板拓扑优化}
}
```

> `note` 字段保留了 Tier 等级、评分和子课题归属，导入 Zotero 后可在 Extra 字段中查看。

---

## 7. 质量门槛 (Quality Gates)

- [ ] 引文验证已完成——无效 DOI 已剔除
- [ ] DOI 去重已完成——无重复条目
- [ ] 五维度评分已完成——Tier 分级合理
- [ ] .bib 文件已导出且含评分标签
- [ ] 检索文献表.md 已生成且含评分列

---

## 8. 收尾检查 (Closing Checks)

### 产出完整性
- [ ] `检索文献表.md` 已生成
- [ ] `检索文献表.pdf` 已自动生成（`md_to_pdf.py 检索文献表.md`）
- [ ] `文献库.bib` 已导出

### 错误日志更新 🆕
- [ ] 本轮执行中是否出现新的 AI 操作错误？
  - 评分偏差（高估/低估某类论文）→ 追加到 `references/error_log.md`
  - DOI 验证失败的新模式 → 追加到 `references/error_log.md`
  - 如有其他新错误：追加到 `references/error_log.md`

### 决策日志更新 🆕
- [ ] 是否调整了评分权重？→ 记录到 `references/decision_log.md`
- [ ] 是否修改了筛选阈值？→ 记录到 `references/decision_log.md`

### 下一步提示
- [ ] 向用户明确说明下一步：开始批量下载（Step 5）
  > **下一步 → Step 5：** 开始批量下载。按出版商自动路由：全部论文先走 Sci-Hub（老论文免费下）；未下载到的按 DOI 前缀分流 → `10.1016/` 走 SD CDP，`10.1109/` 走 IEEE CDP，其余走 Generic CDP。

---

## 9. 故障排除 (Troubleshooting)

常见问题参见 `agents/known_pitfalls.md`。本 Step 特有的问题：

- **Pre-flight 检查失败**：运行 `python3 scripts/search_by_topic.py --preflight` 验证各 API 端点可达性
- **检索结果过少**：检查 AND 块数是否超过 4；回退到 L2/L3
- **评分偏差**：回顾 error_log 中的评分偏差记录
