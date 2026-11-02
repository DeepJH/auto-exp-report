#!/usr/bin/env python3
"""
scripts/package_release.py
Phase 3 纯净归档与 Release 产物生成工具

功能：
1. 本地生成 release/ 交付目录；
2. 纯净打包生成 <学号><姓名>实验<N>.zip，强断言剔除所有 __pycache__、.pyc 与临时构建缓存；
3. 生成带有置顶中文文件名改名提示的 Release 说明文档 notes.md。
"""

import os
import shutil
import sys
import zipfile
from pathlib import Path

from auto_exp.config import load_config, get_workspace_root
from auto_exp.assembler import get_expected_final_filename


def generate_release_notes(course_name: str, exp_id: str, zip_filename: str, docx_filename: str) -> str:
    """生成符合规范的 GitHub Release Notes 说明，顶部置顶代码块改名提示"""
    notes = f"""> [!IMPORTANT]
> **📥 资产下载与规范重命名提示**  
> 受 GitHub 平台限制，Release 附件文件名中的非 ASCII 中文字符在上传时会被自动截断（下载后文件名将显示为 `<学号>.zip` 与 `<学号>.docx`）。  
> 请在下载后**直接点击复制以下标准文件名**进行重命名交卷：
> - 综合源码压缩包：`{zip_filename}`
> - 终稿实验报告文档：`{docx_filename}`

---

## 【{course_name}】实验{exp_id} 成果归档

### 核心产物清单
- **纯净源码包**：`{zip_filename}`（包含 `src/` 核心算法源码与测试用例，已排除所有 Python 缓存与临时文件）
- **实验报告终稿**：`{docx_filename}`（包含完整实操终端截图与调试心得，Word 原生表格格式完好）

### 归档环境信息
- 操作系统: Linux / WSL2 (Ubuntu)
- 语言标准: Python 3.10+, Pandoc
- 交付状态: 自动化构建与 AST 表格断言全部通过
"""
    return notes


def package_clean_release(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = Path.cwd()

    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)

    exp_id_str = str(exp_id)
    exp_dir = workspace_root / course_slug / "exps" / exp_id_str
    if not exp_dir.is_dir():
        raise FileNotFoundError(f"实验目录不存在: {exp_dir}")
    student = cfg.get("student", {})
    course_meta = cfg.get("courses", {}).get(course_slug, {})
    course_name = course_meta.get("name", course_slug)

    sid = student.get("id", "2024000001")
    sname = student.get("name", "张三")

    final_docx_name = get_expected_final_filename(student, exp_id_str)
    final_docx_path = exp_dir / final_docx_name
    src_dir = exp_dir / "src"

    if not final_docx_path.is_file():
        raise FileNotFoundError(f"未找到学生提交的终稿报告: {final_docx_path}。无法打包！")
    if not src_dir.is_dir():
        raise FileNotFoundError(f"未找到实验源码目录: {src_dir}")

    # 1. 准备 release 交付目录
    release_dir = exp_dir / "release"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    # 2. 复制独立终稿文档到 release/
    dest_docx_path = release_dir / final_docx_name
    shutil.copyfile(final_docx_path, dest_docx_path)

    # 3. 复制纯净源码到 release/src/（清理内部潜在缓存）
    dest_src_dir = release_dir / "src"
    shutil.copytree(
        src_dir,
        dest_src_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".pio", "*.tmp"),
    )

    # 4. 打包无缓存 zip
    zip_name = f"{sid}{sname}实验{exp_id_str}.zip"
    zip_path = release_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 添加终稿 docx
        zf.write(dest_docx_path, arcname=final_docx_name)
        # 添加纯净源码目录
        for root, dirs, files in os.walk(dest_src_dir):
            for file in files:
                file_path = Path(root) / file
                # 再次过滤缓存
                if "__pycache__" in str(file_path) or file.endswith((".pyc", ".pyo")):
                    continue
                rel_path = file_path.relative_to(release_dir)
                zf.write(file_path, arcname=str(rel_path))

    # 5. 纯净归档强断言：验证 zip 内部绝无任何 __pycache__ 或 .pyc
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        dirty_entries = [n for n in namelist if "__pycache__" in n or n.endswith((".pyc", ".pyo"))]
        if dirty_entries:
            raise AssertionError(f"❌ 归档污染：zip 压缩包中发现 Python 编译缓存残留: {dirty_entries}")

    # 6. 生成 Release Notes
    notes_content = generate_release_notes(course_name, exp_id_str, zip_name, final_docx_name)
    notes_path = release_dir / "notes.md"
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(notes_content)

    def _safe_display_rel(p: Path) -> str:
        try:
            return str(p.relative_to(repo_root))
        except ValueError:
            try:
                return str(p.relative_to(workspace_root))
            except ValueError:
                return str(p)

    print(f"📦 纯净打包完成！\n"
          f"   交付目录: {_safe_display_rel(release_dir)}\n"
          f"   源码报告一体包: {zip_name} (包含文件 {len(namelist)} 个，缓存残留 0)\n"
          f"   独立报告备份: {final_docx_name}\n"
          f"   Release 说明文件: notes.md")

    return {
        "release_dir": str(release_dir),
        "zip_path": str(zip_path),
        "docx_path": str(dest_docx_path),
        "notes_path": str(notes_path),
        "zip_name": zip_name,
        "docx_name": final_docx_name,
        "tag_name": f"{course_slug}-exp-{exp_id_str}",
        "release_title": f"【{course_name}】实验{exp_id_str} 成果归档",
    }


def main():
    if len(sys.argv) < 3:
        print("用法: python3 scripts/package_release.py <course_slug> <exp_id>")
        sys.exit(1)

    course = sys.argv[1]
    exp = sys.argv[2]
    package_clean_release(course, exp)


if __name__ == "__main__":
    main()
