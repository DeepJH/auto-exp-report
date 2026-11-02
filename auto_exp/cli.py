"""
auto_exp/cli.py
auto-exp-report 总调度器命令行入口与状态机引擎

命令：
- auto-exp run <course_slug> <exp_id>     : 启动或继续实验流水线（未完成 Phase 1 则执行研制与润色，挂起等待 Phase 2；已就绪则验收并发布 Phase 3）
- auto-exp resume <course_slug> <exp_id>  : 明确唤醒并验收学生提交的终稿，顺利放行后完成 Phase 3 打包发布
- auto-exp status <course_slug> <exp_id>  : 查询指定实验的当前执行阶段与工件清单
"""

import argparse
import json
import sys
from pathlib import Path

from auto_exp.assembler import prepare_assembly_handshake, verify_assembly_completion
from auto_exp.config import load_config, get_workspace_root
from auto_exp.humanizer import humanize_report
from auto_exp.phase1 import run_phase1
from auto_exp.releaser import execute_release


def get_exp_state(course_slug: str, exp_id: int | str, repo_root: Path) -> dict | None:
    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)
    state_file = workspace_root / course_slug / "exps" / str(exp_id) / "workflow_state.json"
    if state_file.is_file():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def cmd_run(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> None:
    if repo_root is None:
        repo_root = Path.cwd()

    state = get_exp_state(course_slug, exp_id, repo_root)
    status = state.get("status") if state else "INIT"

    # 分支 1: 初次运行或处于研制中 -> 执行 Phase 1 研制与 Humanizer 润色
    if status in ("INIT", None):
        print(f"🎯 [Orchestrator] 初始化实验流水线: {course_slug} 实验 {exp_id}")
        run_phase1(course_slug, exp_id, repo_root)

        # 紧跟独立 Humanizer 润色并重新断言
        cfg = load_config(repo_root)
        workspace_root = get_workspace_root(cfg, repo_root)
        exp_dir = workspace_root / course_slug / "exps" / str(exp_id)
        raw_md = exp_dir / "report.raw.md"
        report_md = exp_dir / "report.md"
        report_docx = exp_dir / "report.docx"
        humanize_report(raw_md, report_md, report_docx)

        # 触发 Phase 2 报告组装员交接单生成
        prepare_assembly_handshake(course_slug, exp_id, repo_root)
        print("⏸️ [Orchestrator] 流程已在 Phase 2 安全挂起。请按交接单提示贴图合成终稿后，执行: auto-exp resume <course> <exp>")
        return

    # 分支 2: 正处于等待组装阶段 -> 尝试验收终稿
    if status == "AWAITING_ASSEMBLY":
        print(f"🔄 [Orchestrator] 检测到当前处于等待组装阶段，正在执行终稿验收...")
        if verify_assembly_completion(course_slug, exp_id, repo_root):
            # 验收通过，顺流执行 Phase 3 纯净打包
            execute_release(course_slug, exp_id, publish=False, repo_root=repo_root)
        else:
            print("⚠️ [Orchestrator] 终稿验收未通过，流程继续保持挂起等待状态。")
        return

    # 分支 3: 已经完成组装但未发布 -> 执行 Phase 3
    if status == "ASSEMBLED":
        print(f"📦 [Orchestrator] 终稿已就绪，正在执行 Phase 3 发布与纯净打包...")
        execute_release(course_slug, exp_id, publish=False, repo_root=repo_root)
        return

    if status == "RELEASED":
        print(f"✨ [Orchestrator] 该实验已于此前全部交付完成（状态: RELEASED）。如需重新生成请先清理对应目录。")


def cmd_resume(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> None:
    if repo_root is None:
        repo_root = Path.cwd()

    print(f"🚀 [Orchestrator] 收到学生终稿交卷信号，开始执行验收...")
    if verify_assembly_completion(course_slug, exp_id, repo_root):
        execute_release(course_slug, exp_id, publish=False, repo_root=repo_root)
    else:
        sys.exit(1)


def cmd_status(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> None:
    if repo_root is None:
        repo_root = Path.cwd()

    state = get_exp_state(course_slug, exp_id, repo_root)
    if not state:
        print(f"ℹ️ 该实验尚未初始化或未找到状态记录: {course_slug} 实验 {exp_id}")
        return

    print(json.dumps(state, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="auto-exp-report 多 Agent 自动化实验报告流水线总调度器")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # run 子命令
    p_run = subparsers.add_parser("run", help="启动或继续实验全流程")
    p_run.add_argument("course", help="课程标识符（如 cryptography）")
    p_run.add_argument("exp", help="实验序号（如 1）")

    # resume 子命令
    p_resume = subparsers.add_parser("resume", help="提交终稿后恢复流水线并交付打包")
    p_resume.add_argument("course", help="课程标识符")
    p_resume.add_argument("exp", help="实验序号")

    # status 子命令
    p_status = subparsers.add_parser("status", help="查询当前实验状态与工件")
    p_status.add_argument("course", help="课程标识符")
    p_status.add_argument("exp", help="实验序号")

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args.course, args.exp)
    elif args.command == "resume":
        cmd_resume(args.course, args.exp)
    elif args.command == "status":
        cmd_status(args.course, args.exp)


if __name__ == "__main__":
    main()
