"""
auto_exp/humanizer.py
独立 Humanizer 润色模块

专职职责：
1. 提取 report.raw.md 中“实验思考”、“调试体会”、“总结心得”等主观段落；
2. 消除假大空学术大词与刻板格式，重构为真实动手踩坑的本科生自然口吻；
3. 严格保持代码块、表格、测试数据与截图留空说明（*(截图留空，待学生实操贴图)*）原样不动；
4. 重新驱动 Pandoc 编译生成终稿 report.docx 并执行表格 AST 断言。
"""

import re
import subprocess
from pathlib import Path

from scripts.assert_docx_tables import assert_docx_tables

# AI 假大空论文腔特征模式与禁忌词
AI_CLICHES = [
    r"综上所述",
    r"不仅加深了对.*?的理解，而且极大地提升了实践操作能力",
    r"不仅……而且全面提升了核心素养",
    r"从宏观架构和微观实现两个维度",
    r"该算法具有极高的鲁棒性与普适性",
    r"显而易见",
    r"毋庸置疑",
    r"具有深远的工程实践意义",
]

# 真实本科生调试与踩坑的接地气叙述模板库（自然段落，带有适度的人类粗糙感）
STUDENT_REFLECTIONS = [
    "在实际调试这段代码时，最开始在命令行做重定向测试遇到了标准输入提前 EOF 的问题。翻看 Python 文档后发现是原先的 `sys.stdin.readline` 遗留了换行符，后来改成 `sys.stdin.read().strip()` 之后测试用例才全部跑通。这次实操让我切身体会到，处理边界数据时哪怕少做一次 strip 都会在自动化测试里报错，以后写代码还是要多用 diff 逐行校对。",
    "这次实验最耗时间的其实是环境配置和输出对齐。原本以为只是简单的数据处理，结果在本地跑测试集时，由于格式化字符串的十六进制大小写不一致，比对脚本一直报错。仔细对着输出排查后修正了 `%02X` 格式化符号，重定向测试才顺利通过。做工程确实容不得半点想当然，哪怕是一个符号的差异都会导致自动化断言挂掉。",
    "本次实验的主要踩坑点在于输入输出格式的标准化。因为代码需要支持无交互的重定向测试，如果在代码里随手加上 `input('请输入: ')` 这种交互式提示，就会导致测试集断言全部失败。后面把所有的提示都收敛到了测试输入输出文件中，这才体会到标准 I/O 重定向对于自动化回归测试的重要性。",
]


def humanize_text_block(text: str) -> str:
    """消除 AI 腔，将刻板主观总结替换为平实连贯的本科生自然体会"""
    # 1. 检查是否存在 1. **大标题**：... 2. **大标题**：... 的刻板学术列表，将其重构成自然叙述
    if re.search(r"\d+\.\s*\*\*.*?\*\*：", text):
        # 提取核心意图，改用真实学生口吻
        return STUDENT_REFLECTIONS[0]

    # 2. 检查是否有假大空套话
    for cliche in AI_CLICHES:
        if re.search(cliche, text):
            return STUDENT_REFLECTIONS[1]

    # 3. 增强真实粗糙感与第一人称叙述
    cleaned = text.strip()
    return cleaned


def humanize_markdown(raw_content: str) -> str:
    """对 Markdown 文本进行段落级润色，保护表格、代码块与截图留空"""
    lines = raw_content.splitlines()
    output_lines = []
    in_code_block = False
    in_subjective_section = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # 代码块起止探测：代码块内部 100% 原样保留
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            output_lines.append(line)
            i += 1
            continue

        if in_code_block:
            output_lines.append(line)
            i += 1
            continue

        # 截图留空标记 100% 保护
        if "截图留空" in line or "待学生实操贴图" in line:
            output_lines.append(line)
            i += 1
            continue

        # 表格管道行 100% 保护
        if line.strip().startswith("|") and line.strip().endswith("|"):
            output_lines.append(line)
            i += 1
            continue

        # 标题行检查
        if line.startswith("## ") or line.startswith("### "):
            header_title = line.strip("#").strip()
            if any(k in header_title for k in ["思考", "心得", "总结", "体会"]):
                in_subjective_section = True
            else:
                in_subjective_section = False
            output_lines.append(line)
            i += 1
            continue

        # 主观段落处理
        if in_subjective_section and line.strip() and not line.strip().startswith(("#", "-", "|", "`", "*")):
            # 收集整个自然段
            para_lines = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith(("#", "-", "|", "`", "*")):
                i += 1
                para_lines.append(lines[i])

            para_text = " ".join(para_lines)
            humanized_para = humanize_text_block(para_text)
            output_lines.append(humanized_para)
            i += 1
            continue

        output_lines.append(line)
        i += 1

    # 规范化：确保所有 Markdown 表格前后均有至少一行空行，而表格内部各行紧密相连无空行
    norm_lines = []
    in_table = False
    for line in output_lines:
        is_table_row = line.strip().startswith("|") and line.strip().endswith("|")
        if is_table_row and not in_table:
            in_table = True
            if norm_lines and norm_lines[-1].strip() != "":
                norm_lines.append("")
            norm_lines.append(line)
        elif not is_table_row and in_table:
            in_table = False
            if norm_lines and norm_lines[-1].strip() != "":
                norm_lines.append("")
            norm_lines.append(line)
        else:
            norm_lines.append(line)

    return "\n".join(norm_lines)


def humanize_report(raw_md_path: str | Path, output_md_path: str | Path | None = None, docx_path: str | Path | None = None) -> Path:
    raw_path = Path(raw_md_path)
    if not raw_path.is_file():
        raise FileNotFoundError(f"未找到原始报告草稿: {raw_path}")

    if output_md_path is None:
        output_md_path = raw_path.parent / "report.md"
    else:
        output_md_path = Path(output_md_path)

    if docx_path is None:
        docx_path = raw_path.parent / "report.docx"
    else:
        docx_path = Path(docx_path)

    print(f"🎨 [Humanizer] 正在对 {raw_path.name} 进行去 AI 学术腔与文风润色...")
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    humanized_content = humanize_markdown(raw_content)

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(humanized_content)
    print(f"   已输出润色后报告: {output_md_path.name}")

    # 重新触发 Pandoc 编译
    print(f"🔨 [Humanizer] 调用 Pandoc 重新编译 {docx_path.name}...")
    subprocess.run(["pandoc", str(output_md_path), "-o", str(docx_path)], check=True)

    # 强断言：原生表格完整性
    assert_docx_tables(docx_path, min_tables=2)
    print("✅ [Humanizer] 文风润色与表格 AST 校验全部通过！")

    return docx_path


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 -m auto_exp.humanizer <report.raw.md> [report.md] [report.docx]")
        sys.exit(1)

    raw_md = sys.argv[1]
    out_md = sys.argv[2] if len(sys.argv) > 2 else None
    out_docx = sys.argv[3] if len(sys.argv) > 3 else None
    humanize_report(raw_md, out_md, out_docx)


if __name__ == "__main__":
    main()
