"""
tests/test_cli.py
auto-exp-report CLI 命令行接口与状态流转测试（US 21）
验证：
1. CLI 命令行解析（run, resume, status 以及 --publish 选项）；
2. 调度器 run/resume 分支的状态机流转；
3. status 查询命令输出。
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_exp.cli import main, cmd_run, cmd_resume, cmd_status, get_exp_state


def test_cli_argument_parsing():
    """测试命令行参数解析与 --publish 选项"""
    # 1. 测试 run --publish
    with patch("sys.argv", ["auto-exp", "run", "cryptography", "1", "--publish"]), \
         patch("auto_exp.cli.cmd_run") as mock_run:
        main()
        mock_run.assert_called_once_with("cryptography", "1", publish=True)

    # 2. 测试 run 默认不带 --publish
    with patch("sys.argv", ["auto-exp", "run", "cryptography", "2"]), \
         patch("auto_exp.cli.cmd_run") as mock_run:
        main()
        mock_run.assert_called_once_with("cryptography", "2", publish=False)

    # 3. 测试 resume --publish
    with patch("sys.argv", ["auto-exp", "resume", "cryptography", "1", "--publish"]), \
         patch("auto_exp.cli.cmd_resume") as mock_resume:
        main()
        mock_resume.assert_called_once_with("cryptography", "1", publish=True)

    # 4. 测试 status
    with patch("sys.argv", ["auto-exp", "status", "cryptography", "1"]), \
         patch("auto_exp.cli.cmd_status") as mock_status:
        main()
        mock_status.assert_called_once_with("cryptography", "1")


def test_cmd_run_transitions(tmp_path: Path):
    """测试 cmd_run 针对不同前置状态的状态流转"""
    course_slug = "cryptography"
    exp_id = "1"
    exp_dir = tmp_path / course_slug / "exps" / exp_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    state_file = exp_dir / "workflow_state.json"

    # 状态 A: INIT -> 触发 Phase 1 研制与 Phase 2 握手挂起
    with patch("auto_exp.cli.run_phase1") as mock_p1, \
         patch("auto_exp.cli.prepare_assembly_handshake") as mock_handshake:
        cmd_run(course_slug, exp_id, publish=False, repo_root=tmp_path)
        mock_p1.assert_called_once_with(course_slug, exp_id, tmp_path)
        mock_handshake.assert_called_once_with(course_slug, exp_id, tmp_path)

    # 状态 B: AWAITING_ASSEMBLY 且验收成功 -> 顺流进入 Phase 3
    state_file.write_text(json.dumps({"status": "AWAITING_ASSEMBLY"}), encoding="utf-8")
    with patch("auto_exp.cli.verify_assembly_completion", return_value=True), \
         patch("auto_exp.cli.execute_release") as mock_release:
        cmd_run(course_slug, exp_id, publish=True, repo_root=tmp_path)
        mock_release.assert_called_once_with(course_slug, exp_id, publish=True, repo_root=tmp_path)

    # 状态 C: ASSEMBLED -> 直接执行 Phase 3
    state_file.write_text(json.dumps({"status": "ASSEMBLED"}), encoding="utf-8")
    with patch("auto_exp.cli.execute_release") as mock_release:
        cmd_run(course_slug, exp_id, publish=False, repo_root=tmp_path)
        mock_release.assert_called_once_with(course_slug, exp_id, publish=False, repo_root=tmp_path)


def test_cmd_resume_transitions(tmp_path: Path):
    """测试 cmd_resume 验收与放行"""
    course_slug = "cryptography"
    exp_id = "1"

    # 验收通过 -> 执行发布
    with patch("auto_exp.cli.verify_assembly_completion", return_value=True), \
         patch("auto_exp.cli.execute_release") as mock_release:
        cmd_resume(course_slug, exp_id, publish=True, repo_root=tmp_path)
        mock_release.assert_called_once_with(course_slug, exp_id, publish=True, repo_root=tmp_path)

    # 验收未通过 -> 退出异常
    with patch("auto_exp.cli.verify_assembly_completion", return_value=False):
        try:
            cmd_resume(course_slug, exp_id, publish=False, repo_root=tmp_path)
            assert False, "验收未通过应抛出 SystemExit"
        except SystemExit as e:
            assert e.code == 1


def test_cmd_status_output(tmp_path: Path, capsys=None):
    """测试 cmd_status 查询逻辑"""
    course_slug = "cryptography"
    exp_id = "1"
    exp_dir = tmp_path / course_slug / "exps" / exp_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    state_file = exp_dir / "workflow_state.json"
    dummy_state = {"status": "PHASE_1_COMPLETE", "current_phase": 1}
    state_file.write_text(json.dumps(dummy_state), encoding="utf-8")

    st = get_exp_state(course_slug, exp_id, tmp_path)
    assert st == dummy_state


if __name__ == "__main__":
    test_cli_argument_parsing()
    with tempfile.TemporaryDirectory() as td:
        test_cmd_run_transitions(Path(td))
        test_cmd_resume_transitions(Path(td))
        test_cmd_status_output(Path(td))
    print("\n✅ test_cli 全部断言顺利通过！")
