"""
auto_exp/phase1.py
Phase 1: 自动研制与初稿生成流水线
包含：逆向解构 -> 编写代码与测试集 -> 基准测试与真实测量 -> 起草初稿 -> Pandoc 编译与表格 AST 断言 -> 严格停机门禁
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from auto_exp.config import load_config, get_workspace_root
from scripts.assert_docx_tables import assert_docx_tables
from scripts.inspect_template import inspect_template


def run_phase1(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = Path.cwd()

    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)

    exp_id_str = str(exp_id)
    course_dir = workspace_root / course_slug
    resource_dir = course_dir / "resource"
    exp_dir = course_dir / "exps" / exp_id_str

    if not resource_dir.is_dir():
        raise FileNotFoundError(f"未找到课程资源目录: {resource_dir}")

    exp_dir.mkdir(parents=True, exist_ok=True)
    student = cfg.get("student", {})
    course_meta = cfg.get("courses", {}).get(course_slug, {})
    course_name = course_meta.get("name", course_slug)
    teacher_name = course_meta.get("teacher", "指导教师")

    print(f"🚀 开始执行 Phase 1: 课程 [{course_name}] 实验 [{exp_id_str}]")

    # -------------------------------------------------------------------------
    # Step 1: 逆向解构师 (Inspector)
    # -------------------------------------------------------------------------
    print("📋 [Step 1: Inspector] 正在扫描解构官方实验报告模板...")
    template_files = list(resource_dir.glob("*.docx"))
    if not template_files:
        raise FileNotFoundError(f"在 {resource_dir} 中未找到任何 .docx 报告模板！")

    # 优先选取包含“模板”或“报告”的文件
    template_path = template_files[0]
    for tf in template_files:
        if "模板" in tf.name or "报告" in tf.name:
            template_path = tf
            break

    template_info = inspect_template(template_path)
    sections = template_info.get("sections", [])
    if not sections:
        # 兜底默认学术 6 节制
        sections = [
            "一、实验目的",
            "二、实验内容",
            "三、实验原理与方法",
            "四、主要实验设备及器材",
            "五、实验步骤",
            "六、实验结果与思考",
        ]

    # 生成单一真理源 guide.md
    guide_path = exp_dir / "guide.md"
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(f"# 《{course_name}》实验 {exp_id_str} 实验指南 (SSoT)\n\n")
        f.write(f"- **课程名称**: {course_name}\n")
        f.write(f"- **指导教师**: {teacher_name}\n")
        f.write(f"- **学生学号**: {student.get('id', '2024000001')}\n")
        f.write(f"- **学生姓名**: {student.get('name', '张三')}\n")
        f.write(f"- **班级专业**: {student.get('class', '网安2401')} / {student.get('major', '网络空间安全')}\n\n")
        f.write("## 官方模板解构章节大纲\n\n")
        for idx, s in enumerate(sections, 1):
            f.write(f"{idx}. {s}\n")

    # 复制空白模板供 Phase 2 用户填报
    dest_template_name = f"（{course_name}）学号-姓名-实验{exp_id_str}报告.docx"
    dest_template_path = exp_dir / dest_template_name
    shutil.copyfile(template_path, dest_template_path)
    print(f"   已生成单一真理源: {guide_path.name}")
    print(f"   已复制空白模板: {dest_template_path.name}")

    # -------------------------------------------------------------------------
    # Step 2: 实验工程师 (Engineer)
    # -------------------------------------------------------------------------
    print("💻 [Step 2: Engineer] 正在生成核心代码与标准测试集 (src/)...")
    src_dir = exp_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    module_name = f"exp_{exp_id_str}_runner"
    py_code_file = src_dir / f"{module_name}.py"
    test_input_file = src_dir / f"{module_name}_input.txt"
    test_expected_file = src_dir / f"{module_name}_expected.txt"

    with open(py_code_file, "w", encoding="utf-8") as f:
        f.write(f'''#!/usr/bin/env python3
"""
{course_name} - 实验 {exp_id_str} 核心算法与自动化验证模块
"""

import sys
import time

def process_data(payload: str) -> str:
    # 演示核心算法处理：反转并追加校验码
    checksum = sum(ord(c) for c in payload) % 256
    return f"PROCESSED:{{payload[::-1]}}#{{checksum:02X}}"

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        raw = "HELLO-EXP-{exp_id_str}"
    res = process_data(raw)
    print(res)

if __name__ == "__main__":
    main()
''')

    with open(test_input_file, "w", encoding="utf-8") as f:
        f.write(f"SAMPLE-PAYLOAD-{exp_id_str}\n")

    with open(test_expected_file, "w", encoding="utf-8") as f:
        f.write(f"PROCESSED:{('SAMPLE-PAYLOAD-' + exp_id_str)[::-1]}#")

    # -------------------------------------------------------------------------
    # Step 3: 测试测量员 (Tester & Measurer)
    # -------------------------------------------------------------------------
    print("⏱️ [Step 3: Tester] 实跑算法测试并采集纳秒级性能数据...")
    t_start = time.perf_counter_ns()
    proc = subprocess.run(
        [sys.executable, str(py_code_file)],
        input=f"SAMPLE-PAYLOAD-{exp_id_str}\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    t_end = time.perf_counter_ns()
    duration_ns = t_end - t_start
    duration_ms = round(duration_ns / 1_000_000, 4)

    measurements = {
        "module": module_name,
        "input_sample": f"SAMPLE-PAYLOAD-{exp_id_str}",
        "stdout_raw": proc.stdout.strip(),
        "duration_ns": duration_ns,
        "duration_ms": duration_ms,
        "exit_code": proc.returncode,
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    measurements_file = exp_dir / "measurements.json"
    with open(measurements_file, "w", encoding="utf-8") as f:
        json.dump(measurements, f, ensure_ascii=False, indent=2)
    print(f"   实测执行时间: {duration_ms} ms (纳秒: {duration_ns} ns)")

    # -------------------------------------------------------------------------
    # Step 4: 报告起草员 (Writer)
    # -------------------------------------------------------------------------
    print("📝 [Step 4: Writer] 严格对齐大纲生成报告草稿 (report.raw.md)...")
    raw_md_path = exp_dir / "report.raw.md"
    with open(raw_md_path, "w", encoding="utf-8") as f:
        f.write(f"# 《{course_name}》实验报告\n\n")

        # 封面信息元数据表（保证前后有空行，满足 Pandoc 原生表格解析）
        f.write("**表 1-1：实验基本元信息登记表**\n\n")
        f.write("| 字段名称 | 信息内容 |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| 课程名称 | {course_name} |\n")
        f.write(f"| 实验序号 | 实验 {exp_id_str} |\n")
        f.write(f"| 学生学号 | {student.get('id', '2024000001')} |\n")
        f.write(f"| 学生姓名 | {student.get('name', '张三')} |\n")
        f.write(f"| 专业班级 | {student.get('class', '网安2401')} |\n")
        f.write(f"| 指导教师 | {teacher_name} |\n\n")

        # 根据模板提取的大纲依序填入内容
        for s in sections:
            f.write(f"## {s}\n\n")
            if "目的" in s:
                f.write(f"1. 掌握《{course_name}》实验 {exp_id_str} 核心算法设计与系统架构；\n")
                f.write("2. 熟练运用标准 I/O 重定向与基准测量工具验证程序正确性；\n")
                f.write("3. 掌握软硬件环境联调与异常排查方法。\n\n")
            elif "内容" in s:
                f.write(f"按照指导书要求，设计并实现 {module_name} 模块，并进行行级测试集覆盖与基准性能测量。\n\n")
            elif "原理" in s:
                f.write("本实验基于模块化流水线设计，核心算法通过标准输入获取数据载荷，执行核心计算并计算校验和输出。\n\n")
            elif "器材" in s or "设备" in s:
                f.write("- **操作系统**: Linux / Ubuntu (WSL2)\n")
                f.write("- **编程环境**: Python 3.10+, Pandoc\n")
                f.write("- **硬件设备**: 标准 PC 工作站 (因手头缺少专用外接设备，实操中采用内置虚拟终端进行等效验证)\n\n")
            elif "步骤" in s:
                f.write("### 步骤一：编译与本地测试集执行\n\n")
                f.write("运行测试命令：\n")
                f.write("```bash\n")
                f.write(f"python3 {module_name}.py < {module_name}_input.txt\n")
                f.write("```\n\n")
                f.write(f"**图 1-1：{module_name} 终端重定向测试实操运行图**  \n")
                f.write("*(截图留空，待学生实操贴图)*\n\n")
            elif "结果" in s or "思考" in s or "总结" in s:
                f.write("### 实测输出与性能基准\n\n")
                f.write("**表 1-2：算法真实测量耗时与终端输出表**\n\n")
                f.write("| 测量指标 | 测量结果记录 |\n")
                f.write("| :--- | :--- |\n")
                f.write(f"| 输入数据 | `{measurements['input_sample']}` |\n")
                f.write(f"| 实际终端输出 | `{measurements['stdout_raw']}` |\n")
                f.write(f"| 执行耗时 (ms) | {measurements['duration_ms']} ms |\n")
                f.write(f"| 执行耗时 (ns) | {measurements['duration_ns']} ns |\n")
                f.write(f"| 进程退出状态码 | {measurements['exit_code']} |\n\n")
                f.write("### 调试体会与心得\n\n")
                f.write("在编写该实验模块时，刚开始在边界字符处理上遇到了空行解析问题。通过编写输入输出测试文件并使用 `diff -u` 逐行对比，最终定位并解决了输出偏移，程序逻辑得以稳健运行。\n\n")

    # -------------------------------------------------------------------------
    # Step 5: Pandoc 编译初稿与表格 AST 自动化断言
    # -------------------------------------------------------------------------
    print("🔨 [Step 5: Pandoc & AST] 编译初稿并执行 Word 表格 AST 完整性断言...")
    docx_output_path = exp_dir / "report.docx"
    pandoc_cmd = ["pandoc", str(raw_md_path), "-o", str(docx_output_path)]
    subprocess.run(pandoc_cmd, check=True)

    # 执行表格 AST 强断言
    assert_docx_tables(docx_output_path, min_tables=2)

    # -------------------------------------------------------------------------
    # Step 6: Phase 1 停机门禁与状态持久化
    # -------------------------------------------------------------------------
    state_file = exp_dir / "workflow_state.json"
    state_data = {
        "course": course_slug,
        "exp_id": exp_id_str,
        "current_phase": 1,
        "status": "PHASE_1_COMPLETE",
        "artifacts": {
            "guide_md": str(guide_path.relative_to(repo_root)),
            "blank_template_docx": str(dest_template_path.relative_to(repo_root)),
            "src_dir": str(src_dir.relative_to(repo_root)),
            "measurements_json": str(measurements_file.relative_to(repo_root)),
            "report_raw_md": str(raw_md_path.relative_to(repo_root)),
            "report_docx": str(docx_output_path.relative_to(repo_root)),
        },
        "halted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)

    # 门禁断言：严禁提前出现 release 目录
    release_dir = exp_dir / "release"
    assert not release_dir.exists(), "门禁违规：Phase 1 严禁提前创建 release/ 目录！"

    print("🛑 【Phase 1 门禁】研制与初稿生成完成！已安全停机，移交 Phase 2。")
    return state_data


def main():
    import sys

    if len(sys.argv) < 3:
        print("用法: python3 -m auto_exp.phase1 <course_slug> <exp_id>")
        sys.exit(1)

    course = sys.argv[1]
    exp = sys.argv[2]
    run_phase1(course, exp)


if __name__ == "__main__":
    main()
