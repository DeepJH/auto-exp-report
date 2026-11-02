"""
auto_exp/assembler.py
Phase 2: 报告组装员 (Assembler)
负责管理 Phase 2 人机协作契约（现阶段交接给用户实操，未来作为 Computer Use Agent 的无缝升级切口）。
"""

import json
from pathlib import Path
from auto_exp.config import load_config, get_workspace_root
from scripts.validate_final_report import validate_final_report


def get_expected_final_filename(student_info: dict, exp_id: int | str) -> str:
    sid = student_info.get("id", "2024000001")
    sname = student_info.get("name", "张三")
    return f"{sid}{sname}实验{exp_id}报告.docx"


def prepare_assembly_handshake(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = Path.cwd()

    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)

    exp_id_str = str(exp_id)
    exp_dir = workspace_root / course_slug / "exps" / exp_id_str
    state_file = exp_dir / "workflow_state.json"

    if not state_file.is_file():
        raise FileNotFoundError(f"未找到该实验的状态记录: {state_file}。请先执行 Phase 1。")

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
    student = cfg.get("student", {})
    course_meta = cfg.get("courses", {}).get(course_slug, {})
    course_name = course_meta.get("name", course_slug)

    expected_final_name = get_expected_final_filename(student, exp_id_str)
    blank_template_name = f"（{course_name}）学号-姓名-实验{exp_id_str}报告.docx"

    # 生成标准清单 JSON (作为向用户展示的操作表，以及未来 Computer Use 的标准化任务输入)
    manifest = {
        "course_slug": course_slug,
        "course_name": course_name,
        "exp_id": exp_id_str,
        "blank_template_path": str((exp_dir / blank_template_name).relative_to(repo_root)),
        "draft_docx_path": str((exp_dir / "report.docx").relative_to(repo_root)),
        "expected_final_docx_path": str((exp_dir / expected_final_name).relative_to(repo_root)),
        "screenshot_tasks": [
            {
                "task_id": "screen_1",
                "caption": f"图 1-1：exp_{exp_id_str}_runner 终端重定向测试实操运行图",
                "command": f"python3 exp_{exp_id_str}_runner.py < exp_{exp_id_str}_runner_input.txt",
                "work_dir": f"{course_slug}/exps/{exp_id_str}/src",
                "placeholder_in_draft": "*(截图留空，待学生实操贴图)*",
            }
        ],
    }

    manifest_path = exp_dir / "assembly_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 更新状态为等待组装
    state["current_phase"] = 2
    state["status"] = "AWAITING_ASSEMBLY"
    state["artifacts"]["assembly_manifest_json"] = str(manifest_path.relative_to(repo_root))
    state["artifacts"]["expected_final_docx"] = str((exp_dir / expected_final_name).relative_to(repo_root))

    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # 向用户输出清晰的 Markdown 协作操作单
    print("\n" + "=" * 65)
    print(f"📋 【Phase 2 组装员交接单】课程: {course_name} | 实验 {exp_id_str}")
    print("=" * 65)
    print("报告初稿与空白模板已在实验目录就绪。请您完成实操并合成终稿：")
    print(f"\n1. 待填官方模板路径：\n   👉 {exp_dir / blank_template_name}")
    print(f"\n2. 初稿 Word 参考路径：\n   👉 {exp_dir / 'report.docx'}")
    print("\n3. 实操测试与截图任务清单：")
    for t in manifest["screenshot_tasks"]:
        print(f"   - 运行目录: {t['work_dir']}")
        print(f"     执行命令: {t['command']}")
        print(f"     截图图注: {t['caption']}")
    print(f"\n4. 终稿保存命名规范（必须严格一致！）：\n   💾 {exp_dir / expected_final_name}")
    print("\n完成贴图并保存后，只需在终端或对话中输入确认指令，组装员将自动验收并移交 Phase 3 发布！")
    print("=" * 65 + "\n")

    return manifest


def verify_assembly_completion(course_slug: str, exp_id: int | str, repo_root: Path | None = None) -> bool:
    if repo_root is None:
        repo_root = Path.cwd()

    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)

    exp_id_str = str(exp_id)
    exp_dir = workspace_root / course_slug / "exps" / exp_id_str
    state_file = exp_dir / "workflow_state.json"

    if not state_file.is_file():
        raise FileNotFoundError(f"未找到该实验的状态记录: {state_file}")

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    student = cfg.get("student", {})
    expected_final_name = get_expected_final_filename(student, exp_id_str)
    final_path = exp_dir / expected_final_name

    print(f"🔍 [Assembler] 正在对学生提交的终稿进行严谨核验: {final_path.name}...")
    if not validate_final_report(final_path):
        return False

    state["status"] = "ASSEMBLED"
    state["current_phase"] = 2
    state["artifacts"]["final_report_docx"] = str(final_path.relative_to(repo_root))
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print("🎉 [Assembler] 终稿验证全部通过！流程已推进至 ASSEMBLED，准备移交 Phase 3 发布。")
    return True
