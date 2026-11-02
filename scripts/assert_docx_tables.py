#!/usr/bin/env python3
"""
scripts/assert_docx_tables.py
Word 表格 AST 完整性自动化断言工具

断言规则：
1. 正文段落中严禁残留未被 Pandoc 正确解析的 Markdown 管道符表格行（`|`）；
2. 原生 Word 表格数量必须符合预期（默认至少 2 个表格：元数据表与实验实测数据表）。
"""

import sys
from pathlib import Path
import docx


def assert_docx_tables(docx_path: str | Path, min_tables: int = 2) -> None:
    path = Path(docx_path)
    if not path.is_file():
        print(f"❌ 错误：Word 文档不存在: {path}", file=sys.stderr)
        sys.exit(1)

    doc = docx.Document(path)

    # 1. 断言：文档正文段落中严禁残留未解析的表格管道符
    # 过滤掉合法的单个反引号内或明确说明的场景，重点检测形如 | col | col | 的管道符表格残片
    pipe_paras = [
        p.text.strip()
        for p in doc.paragraphs
        if "|" in p.text and (p.text.strip().startswith("|") or p.text.strip().endswith("|"))
    ]

    if pipe_paras:
        print("❌ 断言失败：发现未被 Pandoc 解析的 Markdown 管道符表格残留！", file=sys.stderr)
        for p in pipe_paras:
            print(f"   残余段落: {p}", file=sys.stderr)
        print("💡 原因分析：Markdown 表格前后必须至少保留一行完整空行（尤其是紧跟粗体题注之后）。", file=sys.stderr)
        sys.exit(1)

    # 2. 动态断言：Word 原生表格数量
    table_count = len(doc.tables)
    if table_count < min_tables:
        print(
            f"❌ 断言失败：Word 原生表格数量不足！预期至少 {min_tables} 个，实际仅发现 {table_count} 个表格。",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"✅ Pandoc 表格解析与格式断言通过（成功解析原生表格 {table_count} 个，管道符残留 0）。"
    )


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/assert_docx_tables.py <report.docx> [min_tables=2]")
        sys.exit(1)

    docx_file = sys.argv[1]
    min_t = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    assert_docx_tables(docx_file, min_t)


if __name__ == "__main__":
    main()
