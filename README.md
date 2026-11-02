# auto-exp-report

<p align="center">
  <a href="https://github.com/DeepJH/auto-exp-report"><img src="https://img.shields.io/badge/GitHub-DeepJH%2Fauto--exp--report-181717?logo=github" alt="GitHub Repo"></a>
  <a href="https://github.com/DeepJH/auto-exp-report/releases"><img src="https://img.shields.io/github/v/release/DeepJH/auto-exp-report?color=orange&label=Release" alt="Latest Release"></a>
  <a href="https://github.com/DeepJH/auto-exp-report/issues"><img src="https://img.shields.io/github/issues/DeepJH/auto-exp-report?color=green" alt="Issues"></a>
  <a href="https://github.com/DeepJH/auto-exp-report/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
</p>

> 🎓 **高校工科与计算机实验报告多 Agent 自动化工程流水线**  
> 依托 Google Antigravity (`agy`) 原生子代理编排，严格遵循三阶段隔离门禁、模板大纲驱动、去 AI 学术腔调与公网假数据物理隔离。  
> 🔗 **官方开源地址**：[https://github.com/DeepJH/auto-exp-report](https://github.com/DeepJH/auto-exp-report)

---

## 目录

- [核心心法与特性](#-核心心法与特性)
- [Report Workspace 在哪里？怎么定义的？](#-report-workspace-在哪里怎么定义的)
- [环境一键配置 (仅支持 Linux / WSL2)](#-环境一键配置-仅支持-linux--wsl2)
- [快速上手使用教程](#-快速上手使用教程)
  - [第 0 步：准备输入材料](#第-0-步准备输入材料)
  - [第 1 步：触发 Phase 1 全自动研制](#第-1-步触发-phase-1-全自动研制)
  - [第 2 步：Phase 2 人机协作实操截图与终稿组装](#第-2-步phase-2-人机协作实操截图与终稿组装)
  - [第 3 步：Phase 3 终稿强验收与纯净交付](#第-3-步phase-3-终稿强验收与纯净交付)
- [7 专职 Agent 阵列职责](#-7-专职-agent-阵列职责)
- [公网安全与隐私防御 (Privacy Guard)](#-公网安全与隐私防御-privacy-guard)

---

## 🌟 核心心法与特性

1. **以官方模板为最高真理源（Templates First）**：
   - 章节结构与必做任务严格由官方实验报告模板驱动，**模板没有的坚决不做**（不擅自做多余思考题或扩充项）。
2. **严禁泄漏 Prompt 元指令**：
   - 报告正文绝不出现 `（含代码占位符）` 等机械字符，完全呈现正规学术文档的严谨排版。
3. **真实测量，拒绝凭空捏造**：
   - 测试代理在宿主机实跑算法，采集纳秒级性能耗时与真实终端输出回填至报告表格。
4. **独立 Humanizer 剔除 AI 腔**：
   - 专门 Agent 重写主观调试心得，采用亲自动手踩坑的本科生自然口吻，消除刻板学术套话。
5. **表格 AST 强断言**：
   - 动态检测导出的 Word 原生表格数量，彻底解决 Pandoc 静默退化为 Markdown 管道符文本的暗坑。
6. **三阶段严格门禁**：
   - Phase 1 严格止步于初稿 `report.docx`；
   - Phase 2 作为人机交接切口（现阶段手动贴图，未来 Computer Use 零摩擦无缝接管）；
   - Phase 3 用户确认后方可执行无缓存纯净打包与 GitHub Release。

---

## 📂 Report Workspace 在哪里？怎么定义的？

### 1. 默认内置工作区 (`workspace/`)
仓库默认内置了 `workspace/` 目录作为开箱即用的实验工作区，目录布局完全隔离：

```text
auto-exp-report/
├── setup.sh                                # 【根目录快捷入口】一键环境配置软链接
├── config.example.yaml                     # 公开示范配置（仅包含假数据）
├── config.local.yaml                       # [本地私有] 个人真实配置（已加入 .gitignore）
│
└── workspace/                              # 【⭐ 默认内置实验工作区】
    └── <course_slug>/                      # 课程分类目录（如 cryptography / embedded-system-security）
        ├── resource/                       # 【只读真理源 (SSoT)】
        │   ├── 《XXX》实验指导书.pdf/.docx   # 官方实验指导书
        │   └── （XXX）学号-姓名-实验X报告模板.docx # 官方 Word 报告模板
        │
        └── exps/<exp_id>/                  # 【各实验独立上下文 Exp Context】
            ├── guide.md                    # [Phase 1] 解构生成的单一真理源
            ├── （课程）学号-姓名-实验N报告.docx # [Phase 1] 待填官方模板备份
            ├── src/                        # [Phase 1] 核心代码与行级 I/O 测试用例
            │   ├── <module>.py
            │   ├── <module>_input.txt
            │   └── <module>_expected.txt
            ├── measurements.json           # [Phase 1] 真实纳秒级测量性能数据
            ├── report.raw.md               # [Phase 1] 镜像大纲的草拟报告 (截图留空)
            ├── report.md                   # [Phase 1] 经 Humanizer 润色后的 Markdown
            ├── report.docx                 # [Phase 1 终点] 通过表格 AST 断言的 Word 初稿
            ├── assembly_manifest.json      # [Phase 2] 组装员给出的操作清单契约
            ├── <学号><姓名>实验<N>报告.docx  # [Phase 2 产物] 用户填入实操截图合成的终稿
            └── release/                    # [Phase 3 交付产物]
                ├── <学号><姓名>实验<N>.zip # 纯净源码 + 终稿一体压缩包 (0 pycache)
                ├── <学号><姓名>实验<N>报告.docx # 独立终稿报告备份
                └── notes.md                # 包含置顶中文改名提示的 Release 说明
```

### 2. 怎么定义的？（灵活解耦配置）
在 [auto_exp/config.py](file:///home/deepjh/workspace/auto-exp-report/auto_exp/config.py) 中通过 `get_workspace_root()` 动态解析：
- **内置模式**：默认 `workspace_dir: "workspace"`，所有课程材料集中存放于仓库内 `workspace/` 目录下；
- **解耦模式**：若希望将生成工具与个人私有报告仓库彻底分开，只需在 `config.local.yaml` 中将 `workspace_dir` 指向外部目录：
  ```yaml
  workspace_dir: "/home/deepjh/workspace/my-lab-reports"
  ```
  流水线会自动将各门课的 `resource/` 与 `exps/` 挂载到该外部路径。

---

## 🛠️ 环境一键配置 (仅支持 Linux / WSL2)

> 💡 **平台说明**：  
> Linux 的 Shell 统一简洁好用，而 PowerShell 带有历史包袱，语法相对诡异冗杂。用 PowerShell 只会害了你 [doge]，**强烈推荐在 Linux 原生环境或 Windows WSL2 (Ubuntu) 下运行**！

### 1. 运行一键配置脚本
本项目严格遵循 Python **PEP 668** 规范，自动创建独立的 `.venv/` 虚拟环境，绝不污染系统全局 Python。可在根目录直接运行：

```bash
# 1. 克隆代码仓库
git clone https://github.com/DeepJH/auto-exp-report.git
cd auto-exp-report

# 2. 根目录直接执行一键配置
./setup.sh
```

### 2. 激活虚拟环境
```bash
source .venv/bin/activate
```

### 3. 配置个人元数据
```bash
# 复制示例配置
cp config.example.yaml config.local.yaml
```
打开 `config.local.yaml`，填入您的真实信息（该文件已被 `.gitignore` 强力屏蔽，绝不会提交至 Git）：
```yaml
workspace_dir: "workspace"

student:
  id: "2024000001"
  name: "张三"
  class: "网安2401"
  major: "网络空间安全"
  college: "计算机与网络空间安全学院"

courses:
  cryptography:
    name: "密码学基础与应用"
    teacher: "李老师"
  embedded-system-security:
    name: "嵌入式系统安全"
    teacher: "赵老师"
```

---

## 🚀 快速上手使用教程

### 第 0 步：准备输入材料
在准备做某门课的实验前，在 `workspace/` 下创建课程目录与 `resource/` 文件夹，放入官方材料：
```bash
mkdir -p workspace/cryptography/resource
# 将学校老师给的指导书和报告模板放入 resource/ 目录：
# 例如：workspace/cryptography/resource/《密码学基础与应用》实验指导书.pdf
# 例如：workspace/cryptography/resource/（密码学基础与应用）学号-姓名-实验1报告模板.docx
```

---

### 第 1 步：触发 Phase 1 全自动研制
在终端中执行启动命令（或者在 Antigravity 交互会话中输入 `/auto-exp cryptography 1`）：

```bash
python3 -m auto_exp.cli run cryptography 1
```

**发生了什么**：
1. **Inspector**：逆向解构官方模板表格与大纲，生成单一真理源 `guide.md` 并复制出待填模板；
2. **Engineer**：根据指导书在 `src/` 编写算法代码及行级 I/O 测试用例；
3. **Tester**：运行测试并纳秒计时，回填真实结果到 `measurements.json`；
4. **Writer**：镜像大纲起草毛坯报告 `report.raw.md`，显式留下截图占位 `*(截图留空，待学生实操贴图)*`；
5. **Humanizer**：重写主观调试心得与反思，消除假大空论文腔，调用 Pandoc 编译为 `report.docx`；
6. **AST 断言**：自动断言原生表格 >= 2 且管道符 `|` 残留为 0；
7. **门禁停机**：流程打印交接单并**安全挂起**！

---

### 第 2 步：Phase 2 人机协作实操截图与终稿组装
查看终端输出的 **【Phase 2 组装员交接单】**（亦可查看 `assembly_manifest.json`）：
1. 按照交接单中的命令，在宿主机/真实硬件开发板上执行测试（如 `python3 src/exp_1_runner.py`），截取真实的终端/硬件运行图；
2. 打开实验目录下的待填模板文档：`workspace/cryptography/exps/1/（密码学基础与应用）学号-姓名-实验1报告.docx`；
3. 将初稿 `report.docx` 中的内容与您的真实截图填入，排版完毕后另存为规范名称：
   ```text
   workspace/cryptography/exps/1/2024000001张三实验1报告.docx
   ```

*(注：该交接单采用统一的 JSON 契约，未来将无缝接入 Computer Use Agent 自动执行终端截图与 Word 贴图排版！)*

---

### 第 3 步：Phase 3 终稿强验收与纯净交付
完成终稿保存后，执行恢复命令：

```bash
python3 -m auto_exp.cli resume cryptography 1
```

**发生了什么**：
1. **Assembler 验收**：调用 `validate_final_report.py` 强校验终稿文件，确认体积 > 100KB 且内部包含真实嵌入图片（拦截未截图空草稿）；
2. **Releaser 打包**：调用 `package_release.py` 自动排除所有 `__pycache__` 与 `.pyc`，生成纯净一体包 `release/<学号><姓名>实验1.zip`；
3. **Git 预检与推送**：自动检查分支同步；
4. **Release 发布**：自动创建 GitHub Release，上传 zip 与 docx，并在 Release Notes **最顶部置顶中文改名提示块**（解决 GitHub 下载非 ASCII 中文字符自动截断的平台问题）。

---

## 🤖 7 专职 Agent 阵列职责

```text
========================================================================================
[调度器 Orchestrator] 状态机与门禁生命周期总控 (workflow_state.json)
========================================================================================
  Phase 1 (全自动研制):
    1. 逆向解构师 (Inspector)   : 模板逆向提取真理源 guide.md + 待填模板
    2. 实验工程师 (Engineer)    : 编写 minimal 源码与行级重定向测试 -> src/
    3. 测试测量员 (Tester)      : 实跑测试采集纳秒性能数据 -> measurements.json
    4. 报告起草员 (Writer)      : 严格镜像大纲草拟 -> report.raw.md (截图留空)
    5. 独立润色员 (Humanizer)   : 去学术腔/接地气学生视角润色 -> report.docx (AST断言)
    ==> 【Phase 1 门禁停机，移交组装员】
  Phase 2 (人机交接，未来 Computer Use):
    6. 报告组装员 (Assembler)   : 导出 assembly_manifest.json 挂起等待学生贴图终稿
                                : 验收终稿 (体积 > 100KB, 图片已嵌入)
  Phase 3 (全自动交付):
    7. 交付归档员 (Releaser)    : 纯净打包(0 pycache) -> release/*.zip + docx
                                : Git 推送对齐，GitHub Release 发布 (带置顶中文改名提示)
========================================================================================
```

---

## 🔒 公网安全与隐私防御 (Privacy Guard)

本项目为 GitHub 公开仓库，**严禁将真实学号、姓名、私人令牌提交至远程仓库**！

系统内置了 `scripts/check_privacy.py` 强校验工具：
- 仓库代码、示例配置、自动化测试中 100% 采用白名单假数据（如“张三”、“2024000001”）；
- 真实个人信息仅允许保存在本地被 `.gitignore` 物理隔离的 `config.local.yaml` 中；
- 每次 `git commit` 或 `git push` 前，自动化扫描器将全面扫描暂存区与提交内容，一旦检测到任何疑似真实学号或敏感 Token，将**硬性阻断提交并警报**。
- 若有任何使用疑问或 Bug，欢迎通过 **[GitHub Issues](https://github.com/DeepJH/auto-exp-report/issues)** 反馈。
