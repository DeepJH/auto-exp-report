"""
tests/test_workspace_decoupling.py
测试自定义 workspace_dir 配置与工作区解耦完整生命周期（US 27）
验证：
1. 引擎与目标实验工作区完全物理隔离；
2. Phase 1、Phase 2、Phase 3 在外部自定义目录中完整运行；
3. workflow_state.json 和 assembly_manifest.json 相对路径计算安全无崩溃。
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
        doc.add_paragraph("模板段落说明")
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


def test_custom_workspace_lifecycle():
    with tempfile.TemporaryDirectory() as td_repo, tempfile.TemporaryDirectory() as td_ws:
        repo_dir = Path(td_repo)
        custom_ws_dir = Path(td_ws) / "my_external_courses"
        custom_ws_dir.mkdir(parents=True, exist_ok=True)

        course_slug = "cryptography"
        exp_id = "1"

        # 1. 在 repo_dir 下写入解耦配置文件，指定外部 workspace_dir
        config_path = repo_dir / "config.yaml"
        config_path.write_text(f"""
workspace_dir: "{custom_ws_dir}"
student:
  id: "2024000001"
  name: "张三"
  class: "网安2401"
courses:
  cryptography:
    name: "密码学基础与应用"
    teacher: "李老师"
""", encoding="utf-8")

        # 2. 在外部工作区下准备实验资源
        res_dir = custom_ws_dir / course_slug / "resource"
        template_file = res_dir / "（密码学基础与应用）学号-姓名-实验1模板.docx"
        create_mock_template(template_file)

        # 3. 执行 Phase 1 研制与 Phase 2 挂起
        cmd_run(course_slug, exp_id, repo_root=repo_dir)

        # 验证产物全部落入外部 custom_ws_dir，而非 repo_dir
        exp_dir = custom_ws_dir / course_slug / "exps" / exp_id
        assert exp_dir.is_dir(), "实验目录未在外部工作区创建"
        assert not (repo_dir / course_slug).exists(), "仓库根目录被错误污染！"

        # 验证状态与工件
        state_p1 = get_exp_state(course_slug, exp_id, repo_dir)
        assert state_p1 is not None
        assert state_p1["status"] == "AWAITING_ASSEMBLY"
        assert (exp_dir / "guide.md").is_file()
        assert (exp_dir / "src" / "exp_1_runner.py").is_file()
        assert (exp_dir / "report.docx").is_file()
        assert (exp_dir / "assembly_manifest.json").is_file()

        # 校验 Word 原生表格 AST
        assert_docx_tables(exp_dir / "report.docx", min_tables=2)

        # 4. 模拟学生在外部工作区完成截图合成终稿
        final_docx = exp_dir / "2024000001张三实验1报告.docx"
        create_mock_final_docx(final_docx)

        # 5. 唤醒并交卷验收 (Phase 3 发布打包)
        cmd_resume(course_slug, exp_id, repo_root=repo_dir)

        # 验证交付产物
        state_final = get_exp_state(course_slug, exp_id, repo_dir)
        assert state_final["status"] == "RELEASED"
        release_dir = exp_dir / "release"
        assert release_dir.is_dir()
        zip_path = release_dir / "2024000001张三实验1.zip"
        assert zip_path.is_file()

        # 验证 zip 纯净度
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            assert not any("__pycache__" in n for n in names)
            assert not any(n.endswith(".pyc") for n in names)

        print("\n✅ test_custom_workspace_lifecycle 自定义外部工作区解耦测试顺利通过！")


if __name__ == "__main__":
    test_custom_workspace_lifecycle()
