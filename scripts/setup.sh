#!/usr/bin/env bash
# ==============================================================================
# auto-exp-report 一键环境配置与平台检查脚本
# 遵循 PEP 668 规范，自动管理 .venv 虚拟环境并隔离依赖
# ==============================================================================

set -euo pipefail

# 1. 平台检测与拦截
OS_NAME="$(uname -s 2>/dev/null || echo "Unknown")"
case "$OS_NAME" in
  CYGWIN*|MINGW*|MSYS*|Windows_NT)
    echo "💡 检测到 Windows 原生环境：Linux 的 Shell 统一简洁好用，而 PowerShell 带有历史包袱，语法相对诡异冗杂。用 PowerShell 只会害了你 [doge]，强烈推荐移步 WSL2 (Ubuntu)！" >&2
    exit 1
    ;;
esac

# 2. 定位项目根目录 (兼容软链接与直接调用)
if git rev-parse --show-toplevel &>/dev/null; then
  REPO_ROOT="$(git rev-parse --show-toplevel)"
else
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi
cd "${REPO_ROOT}"

echo "=========================================================="
echo "🚀 开始配置 auto-exp-report 运行环境..."
echo "=========================================================="

# 3. 基础系统工具检测
echo "🔍 检查系统基础命令..."
MISSING_TOOLS=()

if ! command -v python3 &>/dev/null; then
  MISSING_TOOLS+=("python3")
fi

if ! command -v pandoc &>/dev/null; then
  MISSING_TOOLS+=("pandoc")
fi

if ! command -v gh &>/dev/null; then
  MISSING_TOOLS+=("gh (GitHub CLI)")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
  echo "⚠️ 缺少以下系统工具: ${MISSING_TOOLS[*]}"
  echo "👉 在 Ubuntu/Debian/WSL2 中可通过以下命令快速安装："
  echo "   sudo apt update && sudo apt install -y python3 python3-venv python3-pip pandoc gh"
  exit 1
fi

echo "✅ 系统基础命令检查通过: python3, pandoc, gh 就绪。"

# 4. PEP 668 合规：创建并配置 Python 虚拟环境 (.venv)
VENV_DIR="${REPO_ROOT}/.venv"
if [ ! -d "${VENV_DIR}" ]; then
  echo "📦 正在创建独立的 Python 虚拟环境 (${VENV_DIR})..."
  python3 -m venv "${VENV_DIR}" || {
    echo "❌ 创建虚拟环境失败。若缺少 venv 模块，请执行: sudo apt install python3-venv" >&2
    exit 1
  }
fi

echo "🔌 激活虚拟环境并安装 Python 依赖..."
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

pip install --quiet --upgrade pip
pip install --quiet -r "${REPO_ROOT}/requirements.txt"

# 5. 依赖加载验证
python3 -c "import docx, yaml; print('✅ Python 核心依赖验证通过 (python-docx, pyyaml)')"

# 6. 本地配置模板初始化
if [ ! -f "${REPO_ROOT}/config.local.yaml" ] && [ ! -f "${REPO_ROOT}/config.yaml" ]; then
  echo "📝 未检测到本地配置，正在基于 config.example.yaml 创建 config.local.yaml..."
  cp "${REPO_ROOT}/config.example.yaml" "${REPO_ROOT}/config.local.yaml"
  echo "💡 已生成 config.local.yaml（该文件已被 .gitignore 隔离，可在此填写真实学号姓名）。"
else
  echo "✅ 本地配置文件已存在。"
fi

echo "=========================================================="
echo "🎉 环境配置全部就绪！"
echo "   虚拟环境路径: ${VENV_DIR}"
echo "   运行前可执行: source .venv/bin/activate"
echo "=========================================================="
