"""
tests/test_privacy.py
测试 scripts/check_privacy.py 隐私安全防御工具
验证：
1. 白名单假数据（“张三”、“2024000001”等）顺利放行；
2. 真实学号格式、非白名单私人敏感学号被精准拦截；
3. GitHub PAT、私钥等敏感凭证被精准拦截；
4. 暂存区添加 local 私有配置文件被精准拦截；
5. config.local.yaml 中提取的动态敏感目标被精准拦截。
"""

import re
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.check_privacy import (
    ALLOWED_DUMMY_IDS,
    ALLOWED_DUMMY_NAMES,
    SECRET_PATTERNS,
    load_local_private_targets,
    inspect_privacy,
)


def test_dummy_data_whitelist():
    """验证标准假数据在白名单内"""
    assert "2024000001" in ALLOWED_DUMMY_IDS
    assert "张三" in ALLOWED_DUMMY_NAMES
    assert "网安2401" not in ALLOWED_DUMMY_IDS


def test_secret_patterns_detection():
    """验证各种敏感凭证正则能够准确命中"""
    test_secrets = [
        ("ghp_" + "A" * 36, "GitHub Personal Access Token"),
        ("github_pat_" + "B" * 50, "GitHub Fine-grained PAT"),
        ("-----" + "BEGIN RSA PRIVATE KEY-----", "Private Key"),
        ("AIza" + "a" * 35, "Google API Key"),
        ("sk-" + "c" * 48, "OpenAI API Key"),
    ]

    for secret, desc in test_secrets:
        matched = False
        for pat, pat_desc in SECRET_PATTERNS:
            if re.search(pat, secret):
                matched = True
                assert pat_desc == desc
                break
        assert matched, f"未能成功识别敏感凭证: {desc}"


def test_dynamic_forbidden_targets_from_local_config(tmp_path: Path):
    """验证从 config.local.yaml 动态加载非白名单真实身份"""
    # 场景 A: 包含白名单假数据，不应进入拦截黑名单
    local_cfg = tmp_path / "config.local.yaml"
    local_cfg.write_text("""
student:
  id: "2024000001"
  name: "张三"
""", encoding="utf-8")

    f_ids, f_names = load_local_private_targets(tmp_path)
    assert len(f_ids) == 0, "合规假数据学号不应进入黑名单"
    assert len(f_names) == 0, "合规假数据姓名不应进入黑名单"

    # 场景 B: 包含真实学号与姓名，应精准识别为待拦截黑名单
    fake_sensitive_id = "2021" + "098765"
    local_cfg.write_text(f"""
student:
  id: "{fake_sensitive_id}"
  name: "真实同学"
""", encoding="utf-8")

    f_ids, f_names = load_local_private_targets(tmp_path)
    assert fake_sensitive_id in f_ids, "真实学号未被加入待拦截黑名单"
    assert "真实同学" in f_names, "真实姓名未被加入待拦截黑名单"


def test_inspect_privacy_mock_staged_diff():
    """通过模拟暂存区 diff 测试完整检测逻辑"""
    # 场景 1: 合规白名单假数据 -> 无任何告警
    safe_diff = """+++ b/report.md
+ 学号: 2024000001, 姓名: 张三
+ 课程: 密码学基础与应用
"""
    with patch("scripts.check_privacy.get_staged_filenames", return_value=["report.md"]), \
         patch("scripts.check_privacy.get_staged_diff", return_value=safe_diff), \
         patch("scripts.check_privacy.load_local_private_targets", return_value=(set(), set())):
        violations = inspect_privacy()
        assert len(violations) == 0, f"合规假数据不应触发任何违规告警: {violations}"

    # 场景 2: 暂存区含有非法真实学号格式
    sensitive_student_id = "2021" + "123456"
    bad_id_diff = f"""+++ b/report.md
+ 学生学号: {sensitive_student_id}
"""
    with patch("scripts.check_privacy.get_staged_filenames", return_value=["report.md"]), \
         patch("scripts.check_privacy.get_staged_diff", return_value=bad_id_diff), \
         patch("scripts.check_privacy.load_local_private_targets", return_value=(set(), set())):
        violations = inspect_privacy()
        assert any(f"疑似真实学号格式 [{sensitive_student_id}]" in v for v in violations), "未能检测出非白名单真实学号"

    # 场景 3: 暂存区含有 GitHub PAT 敏感令牌
    token_diff = "+++ b/secret.txt\n+ my_token = 'ghp_" + "1" * 36 + "'\n"
    with patch("scripts.check_privacy.get_staged_filenames", return_value=["secret.txt"]), \
         patch("scripts.check_privacy.get_staged_diff", return_value=token_diff), \
         patch("scripts.check_privacy.load_local_private_targets", return_value=(set(), set())):
        violations = inspect_privacy()
        assert any("GitHub Personal Access Token" in v for v in violations), "未能拦截敏感 GitHub PAT"

    # 场景 4: 暂存区误将 config.local.yaml 追踪纳入版本控制
    with patch("scripts.check_privacy.get_staged_filenames", return_value=["config.local.yaml"]), \
         patch("scripts.check_privacy.get_staged_diff", return_value=""), \
         patch("scripts.check_privacy.load_local_private_targets", return_value=(set(), set())):
        violations = inspect_privacy()
        assert any("禁止将本地私有配置文件提交至版本库" in v for v in violations), "未能拦截本地私有配置文件"

    # 场景 5: 暂存区含有在动态黑名单中的真实姓名
    name_diff = "+++ b/notes.txt\n+ 开发者: 真实同学\n"
    with patch("scripts.check_privacy.get_staged_filenames", return_value=["notes.txt"]), \
         patch("scripts.check_privacy.get_staged_diff", return_value=name_diff), \
         patch("scripts.check_privacy.load_local_private_targets", return_value=(set(), {"真实同学"})):
        violations = inspect_privacy()
        assert any("真实姓名残留 [真实同学]" in v for v in violations), "未能拦截动态黑名单真实姓名"

    print("\n✅ test_privacy 全部断言顺利通过！")


if __name__ == "__main__":
    test_dummy_data_whitelist()
    test_secret_patterns_detection()
    with tempfile.TemporaryDirectory() as td:
        test_dynamic_forbidden_targets_from_local_config(Path(td))
    test_inspect_privacy_mock_staged_diff()
