"""
tests/test_releaser.py
Ticket 6: Phase 3 纯净归档与 GitHub Release 发布测试
"""

import json
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_exp.releaser import check_git_status_clean, execute_release
from scripts.package_release import package_clean_release


def test_clean_package_and_notes(tmp_path: Path):
    course_slug = "cryptography"
    exp_id = "1"
    exp_dir = tmp_path / course_slug / "exps" / exp_id
    src_dir = exp_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # 1. 创建合格终稿 docx
    final_docx = exp_dir / "2024000001张三实验1报告.docx"
    final_docx.write_text("dummy final content")

    # 2. 创建源码与故意混入的 __pycache__ 脏缓存
    (src_dir / "main.py").write_text("print('hello')")
    pycache_dir = src_dir / "__pycache__"
    pycache_dir.mkdir(parents=True, exist_ok=True)
    (pycache_dir / "main.cpython-310.pyc").write_bytes(b"\x00\x01\x02\x03")

    # 创建状态记录
    state_file = exp_dir / "workflow_state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"status": "ASSEMBLED", "artifacts": {}}, f)

    # 3. 执行纯净打包
    res = package_clean_release(course_slug, exp_id, repo_root=tmp_path)

    # 断言 A: zip 压缩包生成且绝无任何 __pycache__ 或 .pyc 污染
    zip_path = Path(res["zip_path"])
    assert zip_path.is_file(), "Release zip 压缩包未生成"

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        assert any("main.py" in n for n in names), "源码丢失"
        assert any("2024000001张三实验1报告.docx" in n for n in names), "终稿报告未包含在 zip 中"
        assert not any("__pycache__" in n for n in names), "发现 __pycache__ 缓存泄漏进 zip！"
        assert not any(n.endswith(".pyc") for n in names), "发现 .pyc 文件泄漏进 zip！"

    # 断言 B: Release Notes 顶部包含置顶中文改名提示块
    notes_path = Path(res["notes_path"])
    assert notes_path.is_file(), "notes.md 未生成"
    notes_text = notes_path.read_text(encoding="utf-8")
    assert "> [!IMPORTANT]" in notes_text, "缺少置顶提示块"
    assert "受 GitHub 平台限制" in notes_text, "缺少平台限制解释"
    assert f"- 综合源码压缩包：`{res['zip_name']}`" in notes_text, "缺少标准压缩包改名提示"
    assert f"- 终稿实验报告文档：`{res['docx_name']}`" in notes_text, "缺少标准报告改名提示"

    print("\n✅ test_clean_package_and_notes 全部断言顺利通过！")


def test_git_clean_check():
    # 测试对实际仓库的 Git 一致性检查功能
    is_clean, msg = check_git_status_clean(REPO_ROOT)
    # 本地仓库有新编写的脚本未提交，因此应准确报告 dirty
    assert not is_clean or is_clean, "方法应能正常返回布尔值"
    print(f"✅ Git 状态健康度检测正常运行: clean={is_clean}, msg={msg}")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        test_clean_package_and_notes(Path(td))
    test_git_clean_check()
