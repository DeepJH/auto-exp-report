"""
tests/test_assembler.py
Ticket 5: 报告组装员 (Assembler) 契约与终稿验收测试
"""

import io
import json
import sys
import tempfile
from pathlib import Path
import docx
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_exp.assembler import prepare_assembly_handshake, verify_assembly_completion
from scripts.validate_final_report import validate_final_report

# 1x1 标准合法 PNG 图片字节
TINY_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def create_dummy_image(path: Path, min_size_bytes: int = 150 * 1024):
    """生成真实的临时测试图片文件（附带高熵载荷确保 zip 压缩后体积达到实图效果）"""
    import os
    # 生成真实的 150KB 图片数据
    path.write_bytes(TINY_PNG_BYTES + os.urandom(min_size_bytes))


def create_test_docx(target_path: Path, include_image: bool = False, pad_to_120kb: bool = False):
    """创建用于测试的 docx 文档"""
    doc = docx.Document()
    doc.add_heading("终稿实验报告", level=0)
    doc.add_paragraph("实验步骤及结果截图：")

    if include_image:
        temp_img = target_path.parent / "temp_screen.png"
        create_dummy_image(temp_img)
        doc.add_picture(str(temp_img))

    if pad_to_120kb:
        import os
        # 填充高熵随机文本确保压缩后依然 > 100KB
        for _ in range(40):
            doc.add_paragraph(os.urandom(3000).hex())

    target_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target_path)


def test_assembler_lifecycle(tmp_path: Path):
    course_slug = "cryptography"
    exp_id = "1"
    exp_dir = tmp_path / course_slug / "exps" / exp_id
    exp_dir.mkdir(parents=True, exist_ok=True)

    # 1. 模拟 Phase 1 遗留的初稿与模板工件
    (exp_dir / "report.docx").write_text("dummy draft")
    (exp_dir / "（密码学基础与应用）学号-姓名-实验1报告.docx").write_text("blank template")
    initial_state = {
        "course": course_slug,
        "exp_id": exp_id,
        "current_phase": 1,
        "status": "PHASE_1_COMPLETE",
        "artifacts": {
            "report_docx": f"{course_slug}/exps/{exp_id}/report.docx",
        },
    }
    with open(exp_dir / "workflow_state.json", "w", encoding="utf-8") as f:
        json.dump(initial_state, f)

    # 2. 触发组装员交接
    manifest = prepare_assembly_handshake(course_slug, exp_id, repo_root=tmp_path)
    assert (exp_dir / "assembly_manifest.json").is_file(), "assembly_manifest.json 未生成"
    assert len(manifest["screenshot_tasks"]) >= 1, "截图任务清单为空"

    with open(exp_dir / "workflow_state.json", "r", encoding="utf-8") as f:
        state_awaiting = json.load(f)
    assert state_awaiting["status"] == "AWAITING_ASSEMBLY", "状态未正确变更为 AWAITING_ASSEMBLY"

    # 3. 验收标准反向测试 A: 文件不存在
    assert not verify_assembly_completion(course_slug, exp_id, repo_root=tmp_path), "不存在的文件不应通过"

    # 4. 验收标准反向测试 B: 文件体积太小 (<100KB)
    final_docx_name = "2024000001张三实验1报告.docx"
    small_docx = exp_dir / final_docx_name
    create_test_docx(small_docx, include_image=False, pad_to_120kb=False)
    assert not verify_assembly_completion(course_slug, exp_id, repo_root=tmp_path), "体积过小的草稿不应通过"

    # 5. 验收标准反向测试 C: 体积够大 (>100KB) 但没有嵌入图片
    create_test_docx(small_docx, include_image=False, pad_to_120kb=True)
    assert not verify_assembly_completion(course_slug, exp_id, repo_root=tmp_path), "无图片的纯文本大文档不应通过"

    # 6. 验收标准正向测试: 体积大于 100KB 且包含真实嵌入图片
    create_test_docx(small_docx, include_image=True, pad_to_120kb=True)
    assert small_docx.stat().st_size > 100 * 1024, "测试文件体积未达到预期"
    success = verify_assembly_completion(course_slug, exp_id, repo_root=tmp_path)
    assert success, "合法合格终稿应当通过验证"

    # 验证状态流转至 ASSEMBLED
    with open(exp_dir / "workflow_state.json", "r", encoding="utf-8") as f:
        state_assembled = json.load(f)
    assert state_assembled["status"] == "ASSEMBLED", "状态未推进至 ASSEMBLED"
    print("\n✅ test_assembler_lifecycle 全部断言顺利通过！")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        test_assembler_lifecycle(Path(td))
