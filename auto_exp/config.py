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


def get_workspace_root(cfg: dict, default_root: Path | None = None) -> Path:
    """根据配置解析实验工作区的根目录，支持相对路径与绝对路径。
    若配置未指定，且当前根目录下存在 workspace/ 则默认使用 workspace/，否则使用当前根目录。"""
    if default_root is None:
        default_root = Path.cwd()
    default_ws = "workspace" if (default_root / "workspace").is_dir() else "."
    ws = cfg.get("workspace_dir", default_ws)
    p = Path(ws)
    if p.is_absolute():
        return p
    return (default_root / p).resolve()
