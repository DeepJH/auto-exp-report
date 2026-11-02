#!/usr/bin/env python3
"""
scripts/validate_final_report.py
学生最终提交报告 (<学号><姓名>实验<N>报告.docx) 强断言核验工具

验收规则：
1. 终稿文件必须存在且能被合法解压读取；
2. 文件体积必须大于 100KB（防止学生未贴图直接提交空草稿）；
3. docx 内部 word/media/ 目录下必须包含真实嵌入的图片文件。
"""

import sys
import zipfile
from pathlib import Path
import docx

MIN_DOCX_SIZE_BYTES = 100 * 1024  # 100 KB


def validate_final_report(docx_path: str | Path, min_size_bytes: int = MIN_DOCX_SIZE_BYTES) -> bool:
    path = Path(docx_path)
    if not path.is_file():
        print(f"❌ 验收失败：终稿报告文件不存在: {path}", file=sys.stderr)
        return False

    size_bytes = path.stat().st_size
    size_kb = round(size_bytes / 1024, 2)

    # 1. 体积断言 (> 100KB)
    if size_bytes < min_size_bytes:
        print(
            f"❌ 验收失败：终稿文件体积仅有 {size_kb} KB（小于门禁 {min_size_bytes // 1024} KB）。\n"
            f"   原因：学生很可能尚未将实操截图贴入官方模板，或提交了未完成的草稿！",
            file=sys.stderr,
        )
        return False

    # 2. 压缩包结构与嵌入图片断言 (word/media/)
    try:
        with zipfile.ZipFile(path, "r") as zf:
            media_files = [
                name for name in zf.namelist()
                if name.startswith("word/media/") and not name.endswith("/")
            ]
            if not media_files:
                print(
                    "❌ 验收失败：Word 文档内部未检测到任何嵌入图片（word/media/ 目录为空）！\n"
                    "   请打开待填模板，将实操终端或硬件截图粘贴进相应图注位置。",
                    file=sys.stderr,
                )
                return False
    except zipfile.BadZipFile:
        print(f"❌ 验收失败：文档已损坏，非合法的 docx 文件: {path}", file=sys.stderr)
        return False

    # 3. python-docx 可读性验证
    try:
        doc = docx.Document(path)
        para_count = len(doc.paragraphs)
    except Exception as e:
        print(f"❌ 验收失败：无法解析 Word 段落结构: {e}", file=sys.stderr)
        return False

    print(
        f"✅ 终稿报告验收通过！\n"
        f"   文件路径: {path.name}\n"
        f"   文件体积: {size_kb} KB\n"
        f"   嵌入图片: {len(media_files)} 张\n"
        f"   段落总数: {para_count}"
    )
    return True


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/validate_final_report.py <final_report.docx> [min_size_kb=100]")
        sys.exit(1)

    target_docx = sys.argv[1]
    min_kb = int(sys.argv[2]) * 1024 if len(sys.argv) > 2 else MIN_DOCX_SIZE_BYTES

    if not validate_final_report(target_docx, min_kb):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
