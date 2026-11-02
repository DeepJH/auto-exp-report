#!/usr/bin/env python3
"""
scripts/check_privacy.py
auto-exp-report 公网隐私防御与提交前强校验工具

在 git commit 或 git push 前执行，扫描暂存区与版本库文件，
严防真实个人学号、真实姓名、私人 Token 泄漏至公开仓库。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# 合法公开示范假数据白名单
ALLOWED_DUMMY_IDS = {
    "2024000000",
    "2024000001",
    "2024000002",
    "2024000003",
    "1234567890",
}
ALLOWED_DUMMY_NAMES = {
    "张三",
    "李四",
    "王五",
    "赵六",
    "某某大学",
    "计算机与网络空间安全学院",
    "李老师",
    "王老师",
    "赵老师",
}

# 敏感令牌与私钥特征正则
SECRET_PATTERNS = [
    (r"ghp_[a-zA-Z0-9]{36,}", "GitHub Personal Access Token"),
    (r"github_pat_[a-zA-Z0-9_]{50,}", "GitHub Fine-grained PAT"),
    (r"-----BEGIN\s+(?:RSA|OPENSSH|EC|DSA)?\s*PRIVATE KEY-----", "Private Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key"),
]


def load_local_private_targets(repo_root: Path) -> tuple[set[str], set[str]]:
    """若存在本地私有配置 config.local.yaml，读取其中的真实学号和姓名作为待拦截黑名单"""
    forbidden_ids = set()
    forbidden_names = set()

    local_config = repo_root / "config.local.yaml"
    if local_config.is_file():
        try:
            import yaml
            with open(local_config, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            student = data.get("student", {})
            sid = str(student.get("id", "")).strip()
            name = str(student.get("name", "")).strip()
            if sid and sid not in ALLOWED_DUMMY_IDS:
                forbidden_ids.add(sid)
            if name and name not in ALLOWED_DUMMY_NAMES:
                forbidden_names.add(name)
        except Exception:
            pass

    return forbidden_ids, forbidden_names


def get_staged_diff() -> str:
    """获取 git 暂存区的新增变更文本"""
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "-U0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return res.stdout
    except subprocess.CalledProcessError:
        return ""


def get_staged_filenames() -> list[str]:
    """获取暂存区待提交的文件名列表"""
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def inspect_privacy() -> list[str]:
    violations = []
    repo_root = Path(__file__).resolve().parent.parent

    # 1. 检查暂存区文件名是否误添加了本地私有配置文件
    staged_files = get_staged_filenames()
    for fname in staged_files:
        path = Path(fname)
        if "local" in path.name.lower() or path.name in {"config.yaml", ".env"}:
            violations.append(
                f"🚨 禁止将本地私有配置文件提交至版本库: {fname}（请使用 .gitignore 忽略）"
            )

    # 2. 读取动态黑名单（若用户在本地配置中填了真实学号/姓名）
    forbidden_ids, forbidden_names = load_local_private_targets(repo_root)

    # 3. 扫描暂存区新增文本行
    diff_text = get_staged_diff()
    current_file = "unknown"
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue

        added_content = line[1:]

        # 检测 Secret 令牌特征
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, added_content):
                violations.append(
                    f"🚨 在 {current_file} 中检测到疑似敏感凭证 [{desc}]: {added_content[:20]}..."
                )

        # 检测动态真实学号黑名单
        for fid in forbidden_ids:
            if fid in added_content:
                violations.append(
                    f"🚨 在 {current_file} 中检测到真实学号残留 [{fid}]"
                )

        # 检测动态真实姓名黑名单
        for fname_target in forbidden_names:
            if fname_target in added_content:
                violations.append(
                    f"🚨 在 {current_file} 中检测到真实姓名残留 [{fname_target}]"
                )

        # 启发式检测疑似高校 10-12 位学号格式
        # 排除白名单中的假学号
        id_matches = re.findall(r"\b(20[12]\d{7,10})\b", added_content)
        for matched_id in id_matches:
            if matched_id not in ALLOWED_DUMMY_IDS:
                violations.append(
                    f"🚨 在 {current_file} 中检测到疑似真实学号格式 [{matched_id}] (公开仓库仅允许使用白名单假数据: {ALLOWED_DUMMY_IDS})"
                )

    return violations


def main():
    print("🔒 正在执行公网隐私与敏感信息防御扫描 (scripts/check_privacy.py)...")
    violations = inspect_privacy()
    if violations:
        print("\n" + "=" * 60)
        print("❌ 安全拦截：检测到可能泄露真实个人信息或敏感凭证！")
        print("=" * 60)
        for v in violations:
            print(f"  {v}")
        print("\n👉 修复建议：")
        print("  1. 确保所有版本库追踪文件全部使用合规假数据（如 '张三', '2024000001'）；")
        print("  2. 真实信息只能保存在 config.local.yaml 或 *.local.* 中；")
        print("  3. 使用 git reset HEAD <file> 撤出暂存区，修正后再行提交。")
        sys.exit(1)

    print("✅ 隐私与敏感信息安全检查通过 (暂存区无真实敏感数据残留)。")
    sys.exit(0)


if __name__ == "__main__":
    main()
