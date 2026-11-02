#!/usr/bin/env python3
"""
scripts/inspect_template.py
Word 实验报告模板深度逆向解构工具

功能：
1. 扫描官方 .docx 模板的表头与封面表格字段；
2. 提取正文章节大纲体系（例如典型 6 节制 vs 7 节制）；
3. 判定是否存在思考题/加分项大节，产出结构化解构元数据。
"""

import json
import re
import sys
from pathlib import Path
import docx


def inspect_template(template_path: str | Path) -> dict:
    path = Path(template_path)
    if not path.is_file():
        raise FileNotFoundError(f"模板文件不存在: {path}")

    doc = docx.Document(path)

    # 1. 提取封面与表头表格中的文本
    cover_fields = []
    for table in doc.tables[:2]:  # 通常封面在第 1 或第 2 个表格
        for row in table.rows:
            for cell in row.cells:
                text = cell.text.strip()
                if text and text not in cover_fields:
                    cover_fields.append(text)

    # 2. 识别正文章节大纲 (以中文数字或常见标题模式开头)
    heading_patterns = [
        r"^[一二三四五六七八九十]+[、. ]\s*(.+)$",
        r"^第[一二三四五六七八九十]+部分[、. ]\s*(.+)$",
        r"^[0-9]+[、. ]\s*(.+)$",
    ]

    sections = []
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        # 优先使用 Word 原生标题样式或正则匹配
        is_heading = p.style.name.startswith("Heading") or any(
            re.match(pat, txt) for pat in heading_patterns
        )
        if is_heading:
            sections.append(txt)

    # 若未识别出任何章节段落，退化为扫描非空段落中的关键大节字样
    if not sections:
        core_keywords = ["实验目的", "实验内容", "实验原理", "实验设备", "器材", "实验步骤", "实验结果", "总结", "心得", "思考题"]
        for p in doc.paragraphs:
            txt = p.text.strip()
            if any(k in txt for k in core_keywords) and len(txt) < 30:
                if txt not in sections:
                    sections.append(txt)

    has_thinking_questions = any("思考题" in s for s in sections)
    has_bonus = any("加分" in s or "创新" in s for s in sections)

    result = {
        "template_name": path.name,
        "cover_fields_detected": cover_fields[:15],
        "section_count": len(sections),
        "sections": sections,
        "has_thinking_questions": has_thinking_questions,
        "has_bonus": has_bonus,
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/inspect_template.py <template.docx>")
        sys.exit(1)

    template_file = sys.argv[1]
    res = inspect_template(template_file)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
