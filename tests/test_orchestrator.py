"""
tests/test_orchestrator.py
Ticket 7: auto-exp-report 调度器状态机与端到端集成测试
"""

import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
import docx

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_exp.cli import cmd_run, cmd_resume, get_exp_state
from scripts.assert_docx_tables import assert_docx_tables

TINY_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def create_mock_template(target_path: Path):
    doc = docx.Document()
    doc.add_heading("《密码学基础与应用》实验报告模板", level=0)
    table = doc.add_table(rows=2, cols=2)
    table.rows[0].cells[0].text = "课程"
    table.rows[0].cells[1].text = "密码学基础与应用"
    table.rows[1].cells[0].text = "学号"
    table.rows[1].cells[1].text = "2024000001"
    for s in ["一、实验目的", "二、实验内容", "三、实验原理", "四、主要设备", "五、实验步骤", "六、实验结果与思考"]:
        doc.add_heading(s, level=1)
        doc.add_paragraph("模板段落")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target_path)


def create_mock_final_docx(path: Path):
    doc = docx.Document()
    doc.add_heading("终稿实验报告", level=0)
    temp_img = path.parent / "temp.png"
    temp_img.write_bytes(TINY_PNG_BYTES + os.urandom(150 * 1024))
    doc.add_picture(str(temp_img))
    for _ in range(30):
        doc.add_paragraph(os.urandom(2000).hex())
    doc.save(path)


def test_full_orchestrator_lifecycle(tmp_path: Path):
    course_slug = "cryptography"
    exp_id = "1"
    res_dir = tmp_path / course_slug / "resource"
    template_file = res_dir / "（密码学基础与应用）学号-姓名-实验1模板.docx"
    create_mock_template(template_file)

    # 1. 触发初次执行 (cmd_run)
    cmd_run(course_slug, exp_id, repo_root=tmp_path)

    exp_dir = tmp_path / course_slug / "exps" / exp_id
    state_p1 = get_exp_state(course_slug, exp_id, tmp_path)
    assert state_p1 is not None
    assert state_p1["status"] == "AWAITING_ASSEMBLY", "状态未正确停在 AWAITING_ASSEMBLY"
    assert (exp_dir / "report.docx").is_file(), "初稿 report.docx 未生成"
    assert (exp_dir / "assembly_manifest.json").is_file(), "assembly_manifest.json 未生成"
    assert not (exp_dir / "release").exists(), "Phase 1 门禁违规生成了 release/"

    # 表格 AST 强断言通过
    assert_docx_tables(exp_dir / "report.docx", min_tables=2)

    # 2. 模拟学生完成实操截图合成终稿
    final_docx = exp_dir / "2024000001张三实验1报告.docx"
    create_mock_final_docx(final_docx)

    # 3. 唤醒并执行恢复交卷 (cmd_resume)
    cmd_resume(course_slug, exp_id, repo_root=tmp_path)

    state_final = get_exp_state(course_slug, exp_id, tmp_path)
    assert state_final["status"] == "RELEASED", "状态未更新至 RELEASED"

    # 断言纯净 release
    release_dir = exp_dir / "release"
    assert release_dir.is_dir(), "release 目录未生成"
    zip_file = release_dir / "2024000001张三实验1.zip"
    assert zip_file.is_file(), "zip 交付包未生成"

    with zipfile.ZipFile(zip_file, "r") as zf:
        names = zf.namelist()
        assert not any("__pycache__" in n for n in names), "zip 中残留 __pycache__"

    print("\n✅ test_full_orchestrator_lifecycle 端到端全流程测试顺利通过！")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        test_full_orchestrator_lifecycle(Path(td))
