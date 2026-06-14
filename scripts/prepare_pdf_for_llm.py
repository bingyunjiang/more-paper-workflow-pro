#!/usr/bin/env python3
"""
轻量 PDF -> 文本准备脚本。

目标：
1. 从 PDF 提取全文文本
2. 执行基础清洗
3. 输出 raw / clean / chunks 三层结果
4. 保留可回查锚点，供 Step 7 / 7.15 / 8 复用

这个脚本刻意保持轻量，不试图完美恢复复杂公式、表格或版面结构。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def extract_pages(pdf_path: Path) -> list[str]:
    import fitz

    doc = fitz.open(pdf_path)
    pages: list[str] = []
    try:
        for page in doc:
            pages.append(page.get_text() or "")
    finally:
        doc.close()
    return pages


def normalize_line(line: str) -> str:
    line = line.replace("\u00ad", "")
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def looks_like_page_number(line: str) -> bool:
    return bool(re.fullmatch(r"[0-9]{1,4}", line.strip()))


def looks_like_running_header(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) < 4:
        return False
    if len(stripped) > 90:
        return False
    if re.search(r"(doi|vol\.|volume|issue|copyright|received|accepted)", stripped, flags=re.I):
        return True
    upper_ratio = sum(1 for c in stripped if c.isupper()) / max(len(stripped), 1)
    return upper_ratio > 0.55 and len(stripped.split()) <= 12


def merge_lines(lines: list[str]) -> str:
    out: list[str] = []
    buffer = ""
    for raw in lines:
        line = normalize_line(raw)
        if not line:
            if buffer:
                out.append(buffer.strip())
                buffer = ""
            out.append("")
            continue
        if looks_like_page_number(line) or looks_like_running_header(line):
            continue
        if buffer and buffer.endswith("-") and line:
            buffer = buffer[:-1] + line
            continue
        if buffer and not re.search(r"[.!?;:。！？；：]$", buffer) and not re.match(r"^(#+|\[Figure|\[Equation|Table\s+\d+|Figure\s+\d+)", line):
            buffer += " " + line
        else:
            if buffer:
                out.append(buffer.strip())
            buffer = line
    if buffer:
        out.append(buffer.strip())
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def detect_risk_flags(text: str) -> list[str]:
    flags: list[str] = []
    if re.search(r"\b(eq\.?|equation)\b|\([0-9]+\)", text, flags=re.I):
        flags.append("equation")
    if re.search(r"\btable\s+[0-9]+\b", text, flags=re.I):
        flags.append("table")
    if re.search(r"\bfigure\s+[0-9]+\b|\bfig\.\s*[0-9]+\b", text, flags=re.I):
        flags.append("figure_caption")
    if re.search(r"\bappendix\b|\bsupplementary\b", text, flags=re.I):
        flags.append("appendix_detail")
    return sorted(set(flags))


def split_chunks(clean_text: str, chunk_words: int) -> list[dict[str, Any]]:
    paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
    chunks: list[dict[str, Any]] = []
    current: list[str] = []
    current_words = 0
    seq = 1

    for para in paragraphs:
        words = len(para.split())
        if current and current_words + words > chunk_words:
            joined = "\n\n".join(current).strip()
            chunks.append(
                {
                    "chunk_seq": seq,
                    "text": joined,
                    "risk_flags": detect_risk_flags(joined),
                }
            )
            seq += 1
            current = []
            current_words = 0
        current.append(para)
        current_words += words

    if current:
        joined = "\n\n".join(current).strip()
        chunks.append(
            {
                "chunk_seq": seq,
                "text": joined,
                "risk_flags": detect_risk_flags(joined),
            }
        )
    return chunks


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare PDF text for Step 7/8 LLM use.")
    parser.add_argument("--pdf", required=True, help="PDF file path")
    parser.add_argument("--out-dir", default="pdf-prepared", help="Output directory")
    parser.add_argument("--paper-title", default="", help="Paper title")
    parser.add_argument("--citekey", default="", help="BibTeX citekey")
    parser.add_argument("--zotero-item-key", default="", help="Zotero item key")
    parser.add_argument("--section", default="", help="Optional section label")
    parser.add_argument("--evidence-level", default="pdf_fulltext_supported",
                        choices=["metadata_only", "notes_or_abstract_supported", "pdf_fulltext_supported"])
    parser.add_argument("--chunk-words", type=int, default=1200, help="Approximate words per chunk")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    out_dir = Path(args.out_dir).expanduser().resolve()
    stem = pdf_path.stem
    raw_path = out_dir / f"{stem}.raw.md"
    clean_path = out_dir / f"{stem}.clean.md"
    chunks_path = out_dir / f"{stem}.chunks.json"
    report_path = out_dir / f"{stem}.extraction_report.json"
    artifact_index_path = out_dir / "prepared_pdf_artifacts.json"

    try:
        pages = extract_pages(pdf_path)
    except ImportError:
        raise SystemExit("Missing dependency: PyMuPDF (fitz). Install with `pip install pymupdf`.")

    raw_blocks = []
    for idx, text in enumerate(pages, start=1):
        raw_blocks.append(f"## Page {idx}\n\n{text.strip()}\n")
    raw_text = "\n".join(raw_blocks).strip() + "\n"

    clean_text = merge_lines(raw_text.splitlines())
    chunks = split_chunks(clean_text, args.chunk_words)

    chunk_payload = []
    for item in chunks:
        chunk_id = f"{stem}_{item['chunk_seq']:03d}"
        must_check_pdf = bool(item["risk_flags"])
        chunk_payload.append(
            {
                "chunk_id": chunk_id,
                "paper_title": args.paper_title or stem,
                "citekey": args.citekey,
                "zotero_item_key": args.zotero_item_key,
                "source_pdf": str(pdf_path),
                "pages": "",
                "section": args.section,
                "evidence_level": args.evidence_level,
                "must_check_pdf": must_check_pdf,
                "risk_flags": item["risk_flags"],
                "text": item["text"],
            }
        )

    report = {
        "source_pdf": str(pdf_path),
        "paper_title": args.paper_title or stem,
        "citekey": args.citekey,
        "zotero_item_key": args.zotero_item_key,
        "page_count": len(pages),
        "chunk_count": len(chunk_payload),
        "evidence_level": args.evidence_level,
        "notes": [
            "raw.md is the direct extracted layer",
            "clean.md is the cleaned reading layer",
            "chunks.json is the LLM working layer",
            "original PDF remains the truth source for quotes, pages, equations, tables, and figure captions",
        ],
    }

    artifact_entry = {
        "source_pdf": str(pdf_path),
        "paper_title": args.paper_title or stem,
        "citekey": args.citekey,
        "zotero_item_key": args.zotero_item_key,
        "raw_md": str(raw_path),
        "clean_md": str(clean_path),
        "chunks_json": str(chunks_path),
        "extraction_report_json": str(report_path),
        "evidence_level": args.evidence_level,
        "must_check_pdf": any(chunk.get("must_check_pdf") for chunk in chunk_payload),
        "risk_flags": sorted({flag for chunk in chunk_payload for flag in chunk.get("risk_flags", [])}),
    }

    artifact_index = {"artifacts": [artifact_entry]}

    write_text(raw_path, raw_text)
    write_text(clean_path, clean_text)
    write_json(chunks_path, chunk_payload)
    write_json(report_path, report)
    write_json(artifact_index_path, artifact_index)

    print(f"RAW: {raw_path}")
    print(f"CLEAN: {clean_path}")
    print(f"CHUNKS: {chunks_path}")
    print(f"REPORT: {report_path}")
    print(f"ARTIFACT_INDEX: {artifact_index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
