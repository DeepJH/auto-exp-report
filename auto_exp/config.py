"""
auto_exp/config.py
统一配置读取模块
读取优先级：config.local.yaml -> config.yaml -> ~/.config/auto-exp/config.yaml -> config.example.yaml
"""

from pathlib import Path
import yaml

DEFAULT_STUDENT = {
    "id": "2024000001",
    "name": "张三",
    "class": "网安2401",
    "major": "网络空间安全",
    "college": "计算机与网络空间安全学院",
}


def load_config(repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = Path.cwd()

    candidate_paths = [
        repo_root / "config.local.yaml",
        repo_root / "config.yaml",
        Path.home() / ".config" / "auto-exp" / "config.yaml",
        repo_root / "config.example.yaml",
    ]

    for path in candidate_paths:
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                if "student" not in cfg:
                    cfg["student"] = DEFAULT_STUDENT
                return cfg
            except Exception:
                continue

    return {"student": DEFAULT_STUDENT, "courses": {}}
