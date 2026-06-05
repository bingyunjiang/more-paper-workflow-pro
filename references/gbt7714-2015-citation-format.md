# GB/T 7714-2015 Reference Rules

Use these concise rules when generating the final `参考文献` section for the DOCX literature review.

## Ordering

1. Put Chinese references first.
2. Put English and other non-Chinese references after Chinese references.
3. Within Chinese references, sort by the first author's surname or available Zotero creator field. If pinyin sorting is not available, use the displayed author string consistently.
4. Within English references, sort alphabetically by the first author's surname.
5. If the user requests numbered references, number the final sorted list from 1 onward.

## Author Names

- Chinese authors: preserve Chinese names as displayed in Zotero.
- English authors: use surname first when metadata permits, for example `Smith J`.
- For multiple authors, include all authors when practical. If the author list is very long, use the available Zotero author list or abbreviate cautiously with `等` for Chinese and `et al.` for English when needed.

## Common Formats

Journal article:

```text
作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.
```

Book:

```text
作者. 题名[M]. 出版地: 出版者, 年.
```

Book chapter:

```text
作者. 析出文献题名[M]//主编. 书名. 出版地: 出版者, 年: 起止页码.
```

Conference paper:

```text
作者. 题名[C]//会议名. 出版地: 出版者, 年: 起止页码.
```

Dissertation:

```text
作者. 题名[D]. 保存地: 保存单位, 年.
```

Report:

```text
作者. 题名[R]. 出版地: 出版者, 年.
```

Online source:

```text
作者. 题名[EB/OL]. (发表日期)[引用日期]. URL.
```

## Missing Metadata

- Prefer Zotero metadata over inferred fields.
- If pages, issue, publisher, or place are missing, omit the missing segment rather than inventing it.
- Preserve DOI or URL when it helps identify the source, especially when publication fields are incomplete.
- Do not silently drop a cited source because metadata is incomplete.
