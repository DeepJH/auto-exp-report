"""
auto_exp/releaser.py
Phase 3: 交付归档员 (Releaser)
负责纯净打包、Git 一致性预检、隐私拦截与 GitHub Release 线上发布。
"""

import json
import subprocess
import sys
from pathlib import Path

from auto_exp.config import load_config, get_workspace_root
from scripts.package_release import package_clean_release


def check_git_status_clean(repo_root: Path) -> tuple[bool, str]:
    """检查本地 Git 状态是否干净、是否与远程分支对齐"""
    try:
        # 1. 检查是否存在未提交的代码变动
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        # 过滤被允许的未追踪文件
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        dirty = [l for l in lines if not any(k in l for k in [".local", ".venv", "release/"])]
        if dirty:
            return False, f"本地存在未提交的代码修改: {dirty}。发布前必须先 commit。"

        # 2. 检查是否有未推送至远程的 commit
        push_check = subprocess.run(
            ["git", "status", "-uno"],
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if "Your branch is ahead of" in push_check.stdout:
            return False, "本地有未推送的 Commit，必须先执行 git push origin main，以防 Tag 脱节。"

        return True, "Git 状态健康"
    except Exception as e:
        return False, f"Git 检查失败: {e}"


def execute_release(course_slug: str, exp_id: int | str, publish: bool = False, repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = Path.cwd()

    cfg = load_config(repo_root)
    workspace_root = get_workspace_root(cfg, repo_root)

    exp_id_str = str(exp_id)
    exp_dir = workspace_root / course_slug / "exps" / exp_id_str
    state_file = exp_dir / "workflow_state.json"

    if not state_file.is_file():
        raise FileNotFoundError(f"未找到该实验的状态记录: {state_file}")

    print(f"🚀 [Releaser] 开始启动 Phase 3 规范交付流程...")

    # 1. 安全警惕与隐私前置拦截
    privacy_script = repo_root / "scripts" / "check_privacy.py"
    if privacy_script.is_file():
        print("🔒 [Releaser] 执行发布前隐私安全扫描...")
        proc = subprocess.run([sys.executable, str(privacy_script)], cwd=str(repo_root))
        if proc.returncode != 0:
            raise RuntimeError("隐私安全扫描未通过，已阻断发布！")

    # 2. 本地纯净打包与 notes.md 生成
    package_info = package_clean_release(course_slug, exp_id_str, repo_root)

    # 3. 校验并发布至 GitHub Release (若用户启用 publish)
    if publish:
        print("🔍 [Releaser] 检查 Git 分支远程一致性...")
        is_clean, msg = check_git_status_clean(repo_root)
        if not is_clean:
            raise RuntimeError(f"Git 一致性检查未通过: {msg}")

        tag_name = package_info["tag_name"]
        print(f"🌐 [Releaser] 正在使用 gh release 发布资产 ({tag_name})...")
        cmd = [
            "gh", "release", "create", tag_name,
            package_info["zip_path"],
            package_info["docx_path"],
            "--title", package_info["release_title"],
            "--notes-file", package_info["notes_path"],
        ]
        subprocess.run(cmd, cwd=str(repo_root), check=True)
        print(f"✅ GitHub Release {tag_name} 发布成功！")

    # 4. 更新工作流状态为已发布
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    def _safe_rel(p: str | Path) -> str:
        target = Path(p)
        try:
            return str(target.relative_to(repo_root))
        except ValueError:
            try:
                return str(target.relative_to(workspace_root))
            except ValueError:
                return str(target)

    state["current_phase"] = 3
    state["status"] = "RELEASED"
    state["artifacts"]["release_dir"] = _safe_rel(package_info["release_dir"])
    state["artifacts"]["release_zip"] = _safe_rel(package_info["zip_path"])
    state["artifacts"]["tag_name"] = package_info["tag_name"]

    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print("🎉 【Phase 3 完成】实验全部流程圆满交付！")
    return package_info
