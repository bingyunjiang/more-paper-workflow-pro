# Review Matrix Schema

Use this schema before extracting a Zotero collection tree into a thematic literature review matrix.

The evidence base must include the target collection and all nested subcollections, regardless of depth. Deduplicate items by Zotero item key first and DOI second. Every deduplicated parent item must have one row in the CSV.

## Default Columns

Keep this exact column order in both Markdown and CSV outputs:

1. 作者年份
2. 标题
3. 研究问题
4. 理论/概念
5. 数据/样本
6. 方法
7. 核心发现
8. 贡献
9. 局限
10. 与我的主题关系
11. 可引用摘录
12. 我的笔记/批注
13. DOI/URL

## Field Rules

- 作者年份: Use first author surname or Chinese author name plus publication year. If no year is available, use `年份未明`.
- 标题: Use the Zotero item title. Do not shorten unless it is too long for a readable Markdown table.
- 研究问题: Extract the paper's question, objective, or problem statement from notes, annotation comments, highlights, abstract, or full text evidence.
- 理论/概念: Capture named theories, conceptual frameworks, constructs, mechanisms, or keywords that organize the paper.
- 数据/样本: Capture data source, corpus, field site, sample size, period, country or region, and population when available.
- 方法: Capture research design, model, identification strategy, experiment, qualitative method, computational method, or analytical technique.
- 核心发现: Summarize the main findings in 1-3 concise claims grounded in evidence.
- 贡献: State what the paper adds to the literature, method, theory, data, or empirical evidence.
- 局限: Use explicit author limitations, reviewer-style limitations from notes, or gaps clearly supported by the available evidence.
- 与我的主题关系: Connect the item to the user's stated review topic or research question. If the user has not stated a topic, infer cautiously from the collection name and mark the connection as `推断`.
- 可引用摘录: Include one short excerpt from a note, annotation, highlight, or abstract when useful. Keep it brief and avoid long verbatim passages.
- 我的笔记/批注: Summarize user-authored Zotero notes and annotation comments. Preserve especially useful questions, doubts, or synthesis points.
- DOI/URL: Prefer DOI. If DOI is unavailable, use Zotero URL, publisher URL, arXiv URL, or item URL.

## Evidence Priority

Use sources in this order:

1. User-authored Zotero child notes.
2. Annotation comments attached to highlights or area annotations.
3. Highlighted text from Zotero annotations.
4. Zotero metadata and abstract.
5. Targeted PDF pages or PDF full text, only when the above sources are insufficient.

Do not use PDF full text as the first step. It is expensive and often unnecessary for a review matrix based on notes.

## Missing Values And Uncertainty

- Use `未提及` when the available evidence does not mention a field.
- Use `待补充` when the field is important for synthesis but cannot be filled without manual reading.
- Use `推断:` before cautious inferences made from a collection name, abstract, or surrounding evidence.
- Do not invent methods, samples, findings, or limitations.
- If two sources conflict, keep the conflict visible in the relevant cell.

## Output Rules

- Produce a Markdown version for immediate review.
- Save a UTF-8 CSV file in the current working directory unless the user gives a destination.
- Use one CSV row per Zotero parent item.
- Include every deduplicated parent item from the target collection and all nested subcollections.
- Preserve stable column order.
- Keep CSV cells concise. Prefer semicolons over line breaks inside cells.
- For small collections, a single Markdown table is acceptable.
- For large collections, provide a compact Markdown summary table plus per-item sections when the wide table becomes hard to read.
