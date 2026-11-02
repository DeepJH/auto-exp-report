"""
tests/test_phase1.py
Phase 1 基础研制闭环端到端验证测试
"""

import shutil
import sys
import tempfile
from pathlib import Path

# 将项目根目录加入模块搜索路径
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import docx

from auto_exp.phase1 import run_phase1
from scripts.assert_docx_tables import assert_docx_tables


def create_mock_template(target_path: Path):
    """动态生成带有封面表格与标准六大节的官方报告模板 docx"""
    doc = docx.Document()
    doc.add_heading("《密码学基础与应用》实验报告模板", level=0)

    # 封面元信息表格
    table = doc.add_table(rows=3, cols=2)
    table.rows[0].cells[0].text = "课程名称"
    table.rows[0].cells[1].text = "密码学基础与应用"
    table.rows[1].cells[0].text = "学生姓名"
    table.rows[1].cells[1].text = "张三"
    table.rows[2].cells[0].text = "学生学号"
    table.rows[2].cells[1].text = "2024000001"

    # 标准 6 节制大纲
    sections = [
        "一、实验目的",
        "二、实验内容",
        "三、实验原理与方法",
        "四、主要实验设备及器材",
        "五、实验步骤",
        "六、实验结果与思考",
    ]
    for s in sections:
        doc.add_heading(s, level=1)
        doc.add_paragraph("（此处为模板占位说明文字）")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target_path)


def test_phase1_end_to_end(tmp_path: Path):
    # 1. 准备测试工程目录与假数据配置
    course_slug = "cryptography"
    exp_id = "1"
    resource_dir = tmp_path / course_slug / "resource"
    template_file = resource_dir / "（密码学基础与应用）学号-姓名-实验1模板.docx"
    create_mock_template(template_file)

    # 创建示例假数据配置
    example_config = tmp_path / "config.example.yaml"
    with open(example_config, "w", encoding="utf-8") as f:
        f.write("""
student:
  id: "2024000001"
  name: "张三"
  class: "网安2401"
courses:
  cryptography:
    name: "密码学基础与应用"
    teacher: "李老师"
""")

    # 2. 运行 Phase 1 全自动流水线
    state = run_phase1(course_slug, exp_id, repo_root=tmp_path)

    # 3. 验收标准断言
    exp_dir = tmp_path / course_slug / "exps" / exp_id

    # 断言 A: 核心工件齐全
    assert (exp_dir / "guide.md").is_file(), "guide.md 未生成"
    assert (exp_dir / "src" / "exp_1_runner.py").is_file(), "核心源码未生成"
    assert (exp_dir / "measurements.json").is_file(), "真实测试数据未生成"
    assert (exp_dir / "report.docx").is_file(), "初稿 report.docx 未生成"
    assert (exp_dir / "workflow_state.json").is_file(), "状态文件未生成"

    # 断言 B: 表格 AST 解析完整，无管道符残留，且表格数 >= 2
    assert_docx_tables(exp_dir / "report.docx", min_tables=2)

    # 断言 C: Phase 1 停机门禁：严禁生成 release 目录
    assert not (exp_dir / "release").exists(), "Phase 1 违规生成了 release/ 目录"
    assert state["status"] == "PHASE_1_COMPLETE", "状态未正确标记为 PHASE_1_COMPLETE"
    print("\n✅ test_phase1_end_to_end 全部断言顺利通过！")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        test_phase1_end_to_end(Path(td))
