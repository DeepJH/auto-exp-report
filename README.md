# auto-exp-report

[![GitHub Repo](https://img.shields.io/badge/GitHub-DeepJH%2Fauto--exp--report-181717?logo=github)](https://github.com/DeepJH/auto-exp-report)
[![Release](https://img.shields.io/badge/Release-v0.1.0-orange)](https://github.com/DeepJH/auto-exp-report/releases)
[![Issues](https://img.shields.io/github/issues/DeepJH/auto-exp-report?color=green)](https://github.com/DeepJH/auto-exp-report/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/DeepJH/auto-exp-report/blob/main/LICENSE)

> 🎓 **高校工科与计算机实验报告多 Agent 自动化工程流水线**  
> 🤖 依托 Google Antigravity (`agy`) 原生子代理编排，告别机械排版与虚假数据。严格遵循三阶段隔离门禁、官方大纲镜像驱动、去 AI 八股腔调与公网假数据物理隔离。  
> 🔗 **官方开源地址**：[https://github.com/DeepJH/auto-exp-report](https://github.com/DeepJH/auto-exp-report)

---

## 📑 目录

- [💡 一、这是什么东西，能干什么](#-一这是什么东西能干什么)
  - [1.1 一句话直观解释](#11-一句话直观解释)
  - [1.2 三种模式直观对比（为什么需要它？）](#12-三种模式直观对比为什么需要它)
  - [1.3 它到底能干什么？（全生命周期 6 大硬核能力）](#13-它到底能干什么全生命周期-6-大硬核能力)
- [🚀 二、怎么用的（Quick Start、概念和做法，及详细进阶教程）](#-二怎么用的quick-start概念和做法及详细进阶教程)
  - [2.1 极速上手 (Quick Start)](#21-极速上手-quick-start)
  - [2.2 核心概念与做法 (Concepts & Practice)](#22-核心概念与做法-concepts--practice)
  - [2.3 详细进阶教程 (Advanced Guide)](#23-详细进阶教程-advanced-guide)
- [⚙️ 三、运作方式和原理解析](#️-三运作方式和原理解析)
  - [3.1 端到端运作机制（How It Operates）](#31-端到端运作机制how-it-operates)
  - [3.2 底层技术原理解析（Deep Principle Analysis）](#32-底层技术原理解析deep-principle-analysis)
- [🌟 四、常见问题排查与未来规划 (FAQ & Roadmap)](#-四常见问题排查与未来规划-faq--roadmap)
  - [4.1 常见问题排查 (FAQ)](#41-常见问题排查-faq)
  - [4.2 未来演进路线 (Roadmap)](#42-未来演进路线-roadmap)
  - [4.3 开源许可证与贡献](#43-开源许可证与贡献)

---

## 💡 一、这是什么东西，能干什么

### 1.1 一句话直观解释

> 🎯 **“把老师发下来的实验指导书和空白 Word 报告往文件夹里一丢，敲一行命令，一个由 7 个 AI 专家组成的虚拟工程小组立刻开工：帮你写完算法代码、在电脑上实跑测试、测出纳秒级真数据、填好数据、排好 Word 表格、洗掉生硬的 AI 腔调，最后生成一份可以直接交作业的完整实验报告！”**

`auto-exp-report` 是一套专为高校工科、计算机与电子信息专业打造的**多 Agent 协同实验报告自动化工程流水线**。它原生运行于 Google Antigravity (`agy`) 平台，通过严格的 3 阶段工作流门禁，彻底解决传统大模型辅助生成报告时的“格式崩溃”、“幻觉瞎编”、“AI 论文腔”和“隐私泄漏”等顽疾。

---

### 1.2 三种模式直观对比（为什么需要它？）

| 痛点维度 | 😫 传统纯手工硬肝 | 🫠 单一 Prompt 裸问 ChatGPT | 🚀 auto-exp-report 多 Agent 流水线 |
| :--- | :--- | :--- | :--- |
| **耗时与心力** | 耗费 3~6 小时，格式排版让人崩溃 | 30 分钟，但要花 1 小时手工校正格式 | **仅需 3~5 分钟**，中途仅配合截取实操图 |
| **排版与表格** | 手工 Word 调间距，极易错乱跑位 | Markdown 贴进 Word 表格经常变形崩坏 | **Pandoc AST 强断言**，100% 原生 Word 表格 |
| **数据真实性** | 真实但反复手动测量记录极度繁琐 | **完全凭空捏造**，纳秒级延时张口就来 | **真实测试**，在宿主机实跑算法写入 measurements.json |
| **文风与质感** | 纯天然学生口吻 | 充满“综上所述”、“显而易见”AI 论文腔 | **独立 Humanizer**，还原工科生动手踩坑反思语气 |
| **截图与硬件** | 容易漏贴、顺序颠倒、图不对题 | 无法真正操作硬件与终端，流程断裂 | **契约交接清单**，明确提示执行命令与贴图位置 |
| **隐私与安全** | 经常手滑将学号姓名推到公开仓库 | 容易将真实学生信息和私有 Token 提交 | **Privacy Guard 强锁**，公私隔离 + 提交前拦截 |

---

### 1.3 它到底能干什么？（全生命周期 6 大硬核能力）

- 📖 **1. 官方材料逆向解构**：从老师发布的 PDF/Word 指导书中提取纯正大纲，生成单一真理源（SSoT），**大纲没有的绝不多做，杜绝幻觉扩充**；
- 💻 **2. 真实代码编写与验证**：自动生成最小化核心算法代码，并配套编写行级 I/O 输入输出重定向测试用例，实测确保代码 0 bug；
- ⏱️ **3. 宿主机真实运行与纳秒性能测量**：直接在宿主机真实执行算法，采集纳秒级性能基准耗时，将实测数据回填至报告表格；
- 📝 **4. Word 表格防崩坏与 AST 强校验**：自动构建 Word 初稿，逐段扫描验证表格 XML 节点，杜绝任何 Markdown 管道符降级退化；
- 🗣️ **5. 去 AI 八股腔自然学生口吻润色**：重写主观调试体会与总结，剔除虚假大话，呈现亲自动手排查 bug 的真实工科本科生口吻；
- 📦 **6. 纯净归档打包与 GitHub 发布**：自动剔除所有编译缓存（零 `__pycache__` 与 `.pyc`），打包规范命名的纯净 Zip 并自动发布 GitHub Release（内置中文重命名一键指引）。

---

## 🚀 二、怎么用的（Quick Start、概念和做法，及详细进阶教程）

### 2.1 极速上手 (Quick Start)

#### 🖥️ 运行环境要求
- **操作系统**：Linux 原生系统 或 Windows WSL2 (Ubuntu)。（*提示：Windows 原生 PowerShell 语法冗杂且存在历史包袱，严禁直接运行，强烈建议移步 WSL2*）；
- **基础依赖**：Python 3.10+、Git、Pandoc（用于编译 Word 文档）、GitHub CLI (`gh`，用于发布 Release）。

#### ⚡ 步骤 1：一键初始化环境
本项目严格遵循 Linux **PEP 668**（externally-managed-environment）规范，通过根目录脚本自动创建独立的 `.venv/` 虚拟环境，不污染系统全局 Python：

```bash
# 1. 克隆代码仓库
git clone https://github.com/DeepJH/auto-exp-report.git
cd auto-exp-report

# 2. 执行根目录一键配置脚本
./setup.sh

# 3. 激活虚拟环境
source .venv/bin/activate
```

#### 🔒 步骤 2：配置本地个人信息（仅需一次）
复制示例配置并填入您的真实信息。该文件被 `.gitignore` 彻底物理隔离，绝不会被意外推送到公网：

```bash
cp config.example.yaml config.local.yaml
```

编辑 `config.local.yaml`：
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
```

#### 🎯 步骤 3：三步极速完成一次实验报告
以“密码学基础与应用（`cryptography`）”的实验 1 为例：

1. **投喂材料**：
   ```bash
   mkdir -p workspace/cryptography/resource
   # 将老师发布的《实验指导书》和官方 Word 报告模板放入 resource/ 目录
   ```
2. **触发 Phase 1 全自动研制**：
   ```bash
   python3 -m auto_exp.cli run cryptography 1
   ```
   *流水线全自动完成逆向提取、代码编写、数据测试、Word 初稿编译与 AST 表格校验，并在控制台打印出实操截图交接清单后安全挂起。*
3. **补充实操截图并触发 Phase 3 终稿交付**：
   按交接清单提示，将初稿内容和真实测试截图填入待填模板，另存为终稿：
   ```text
   workspace/cryptography/exps/1/2024000001张三实验1报告.docx
   ```
   随后执行恢复交付命令：
   ```bash
   python3 -m auto_exp.cli resume cryptography 1
   ```
   *流水线自动执行终稿体积与图片强校验、纯净打包并在 GitHub 上发布交付物。*

---

### 2.2 核心概念与做法 (Concepts & Practice)

#### 🌟 (1) 唯一真理源 (Single Source of Truth, SSoT)
- **概念**：官方讲义与官方 Word 报告模板是最高真理。
- **做法**：Inspector 代理只从 `workspace/<course_slug>/resource/` 读取材料，逆向生成结构化大纲 `guide.md`。实验报告的章节与必填项完全镜像该大纲，**严禁超纲答题**。

#### 📂 (2) Report Workspace 拓扑结构
仓库默认内置 `workspace/` 作为实验根工作区，隔离布局如下：

```text
auto-exp-report/
├── setup.sh                                # 根目录一键环境配置入口 (软链接)
├── config.example.yaml                     # 公开示范配置（仅含白名单假数据）
├── config.local.yaml                       # [本地私有] 真实个人配置（被 .gitignore 隔离）
│
└── workspace/                              # 【默认内置实验工作区】
    └── <course_slug>/                      # 课程英文标识（如 cryptography）
        ├── resource/                       # 【只读真理源 (SSoT)】
        │   ├── 实验指导书.pdf/.docx          # 官方指导书
        │   └── 官方报告模板.docx             # 官方 Word 报告模板
        │
        └── exps/<exp_id>/                  # 【独立实验上下文 Exp Context】
            ├── guide.md                    # [Phase 1] 逆向结构化大纲
            ├── src/                        # [Phase 1] 核心代码与行级 I/O 测试
            ├── measurements.json           # [Phase 1] 真实纳秒级实测基准数据
            ├── report.raw.md               # [Phase 1] 镜像大纲草拟报告 (截图留空)
            ├── report.md                   # [Phase 1] Humanizer 润色后 Markdown
            ├── report.docx                 # [Phase 1 产物] 通过 AST 断言的 Word 初稿
            ├── assembly_manifest.json      # [Phase 2] 组装契约交接清单
            ├── <学号><姓名>实验<N>报告.docx  # [Phase 2 终稿] 填入截图后的完整报告
            └── release/                    # [Phase 3 产物]
                ├── <学号><姓名>实验<N>.zip # 零 pycache 纯净打包一体包
                ├── <学号><姓名>实验<N>报告.docx # 终稿备份
                └── notes.md                # 带中文置顶改名提示的发布说明
```

#### 🚪 (3) 三阶段隔离生命周期 (Three-Phase Lifecycle)
- **Phase 1 (全自动研制)**：逆向大纲 -> 编码实测 -> 初稿起草 -> 消除 AI 腔 -> Word 编译与表格 AST 断言 -> 导出交接单 -> **强行停机挂起**。
- **Phase 2 (人机协作贴图)**：提供结构化的操作交接清单（现阶段由学生执行命令截取真实窗口画面填入 Word 另存；预留标准接口供未来接入 Computer Use Agent 自动贴图）。
- **Phase 3 (验收与纯净交付)**：对终稿文件执行双重强验收（体积 > 100KB 且内部 `word/media/` 包含图片） -> 剥离编译缓存打包纯净 Zip -> 推送并发布 GitHub Release。

---

### 2.3 详细进阶教程 (Advanced Guide)

#### 🤖 (1) 在 Antigravity 对话中直接驱动
除了在终端运行 Python 模块，本项目深度适配了 Antigravity (`agy`) 原生 Agent 技能体系。在 Antigravity 会话窗口中，直接下发指令即可调用专职 Agent 团队：

```text
/auto-exp cryptography 1
```

Antigravity 会根据 `.agents/skills/auto-exp/SKILL.md` 的规约，按序唤起专职子代理自主研制并向您实时汇报进度。

#### 🔄 (2) 状态查询与断点续跑
如果流水线在某一步被中断，或者需要确认当前进度，可随时通过 CLI 检查或恢复：

```bash
# 检查当前实验进行到了哪一阶段、产生的文件与下一步动作
python3 -m auto_exp.cli status cryptography 1

# 恢复挂起流程（例如完成贴图后执行 Phase 3 验收交付）
python3 -m auto_exp.cli resume cryptography 1
```

#### 🔌 (3) 外部私有报告仓解耦模式
若希望将此自动化工程工具与您个人的私有实验报告仓库彻底物理隔离，只需在 `config.local.yaml` 中将 `workspace_dir` 指向外部绝对路径：

```yaml
workspace_dir: "/home/deepjh/workspace/my-private-lab-reports"
```

流水线会自动读取并输出到该外部目录，代码仓库本身保持纯净开源。

#### 🧪 (4) 行级 I/O 输入输出重定向测试机制
在 `src/` 目录下，工程师代理遵循严密的独立执行规范：
- `<module>_input.txt`：存放测试输入数据；
- `<module>_expected.txt`：存放预期标准答案；
- `<module>.py`：可直接通过 `python3 src/<module>.py < src/<module>_input.txt` 独立复现，保证任何批改助教都能一行命令跑通测试。

---

## ⚙️ 三、运作方式和原理解析

### 3.1 端到端运作机制（How It Operates）

流水线将原本混沌混乱的报告生成任务，解构为一条高度纪律化的**“数据流水线装配车间”**。调度中枢（Orchestrator）基于 `workflow_state.json` 强状态机，严格控制数据流与产物流转：

```text
========================================================================================
                      auto-exp-report 端到端运作流向全景图
========================================================================================

【输入材料】
  └── workspace/<course_slug>/resource/
        ├── 实验指导书.pdf/.docx ──┐
        └── 官方Word模板.docx ────┼─────────────────────────────────────────────────┐
                                  │                                                 │
【Phase 1: 全自动研制工序】        ▼                                                 │
  ├── 1. Inspector 解构师  ──> 逆向提取 guide.md (单一真理源 SSoT) ───────────────────┼──> 生成待填模板
  ├── 2. Engineer 工程师   ──> 编写 minimal 源码与行级 I/O 用例 -> src/             │
  ├── 3. Tester 测量员     ──> 宿主机执行测试，测出真实性能 -> measurements.json     │
  ├── 4. Writer 起草员     ──> 镜像大纲草拟毛坯报告 -> report.raw.md (截图留空)      │
  ├── 5. Humanizer 润色员  ──> 局部清洗 AI 腔 -> report.md -> Pandoc 编译 report.docx│
  │                            │                                                    │
  │                            ▼ 【AST 强断言通过 (Table >= 2, 管道符 = 0)】         │
  └── 6. Assembler 组装员  ──> 导出 assembly_manifest.json 契约清单                  │
                               │                                                    │
                               ▼ 🛑 【Phase 1 门禁强制安全挂起，打印人机交接单】     │
                                                                                    │
【Phase 2: 人机协同贴图】                                                            │
  └── 学生查看交接单 ───────> 宿主机执行实操命令截取真实画面 ───> 贴入待填模板 ───────┘
                               │
                               ▼ 另存为规范终稿：<学号><姓名>实验<N>报告.docx
                               
【Phase 3: 全自动强验收与纯净交付】
  ├── 1. Assembler 组装员  ──> 双重强验收 (文件体积 > 100KB 且物理嵌入 media 图片)
  └── 2. Releaser 归档员   ──> 递归过滤 __pycache__ / .pyc -> 纯净打包 release/*.zip
                               └── Git 推送对齐，自动发布附带中文改名指引的 GitHub Release
========================================================================================
```

---

### 3.2 底层技术原理解析（Deep Principle Analysis）

#### 🛡️ 原理解析 1：Pandoc 表格静默退化陷阱与 AST 双向断言机制
- **痛点黑盒**：Pandoc 在将 Markdown 编译为 Word 时，对表格前后的空行极其敏感。如果表格外部缺少空行包裹，或者表头与分隔行之间存在空行错位，Pandoc 解析器会**静默降级**，将表格识别为普通文本段落（Paragraph），导致在 Word 中变成一堆带有 `|` 字符的纯文本乱码。
- **破解原理**：
  1. **行状态机排版**：在 Markdown 生成与润色阶段，引入严格的三状态有限状态机（`OUTSIDE`、`IN_TABLE`、`DELIMITER`），强制确保表格块外部拥有独立的上下空行，同时表格内部行保持严格紧密连续；
  2. **底质 OpenXML 节点校验**：初稿生成后，流水线直接通过 `python-docx` 读取 Word 文档的底层 OpenXML 结构，校验原生 `<w:tbl>` 表格节点数必须 `>= 2`（基础信息表与结果表）；
  3. **段落管道符全量扫描**：逐段遍历文档中的段落文本，若检测到任何包含连续 `|` 字符的未降解文本段，立即报错中断，彻底封死排版崩坏暗坑。

#### 🎭 原理解析 2：去 AI 八股腔与 Markdown 结构免疫清洗算法
- **痛点黑盒**：通用大模型生成内容充斥“综上所述”、“不仅……而且……”等空洞套话。如果直接把整份报告交给大模型全文润色，大模型极易“误伤”已经排版好的代码块、测试数据表格或元数据占位符。
- **破解原理**：
  1. **精准靶向定位**：`auto_exp/humanizer.py` 仅提取报告中的“实验总结”、“心得体会”等主观反思段落，不触碰任何技术正文；
  2. **结构免疫保护**：使用独立临时 Token 标记保护代码块、表格以及截图占位符，使核心排版对大模型调用免疫；
  3. **工科生视角重构**：注入“工科本科生动手踩坑调试反思”提示词，将机械八股转换为亲身排查 bug 的真实体会（如单步打印、边界溢出排查），润色后重新组装并再次触发表格 AST 断言。

#### ⏱️ 原理解析 3：真实性保障与行级 I/O 隔离执行机制
- **痛点黑盒**：语言模型不具备物理世界的执行能力，让大模型直接生成测试结果，其耗时和数据完全来自统计概率脑补，违背工科实验的严肃性。
- **破解原理**：
  1. **行级输入输出对齐**：工程师代理在 `src/` 编写算法代码时，配套生成 `<module>_input.txt` 与 `<module>_expected.txt`；
  2. **本地子进程真跑**：测试代理直接启动 Python 子进程，利用标准输入重定向实跑代码，比对输出正确性；
  3. **纳秒级基准测量**：利用 `time.perf_counter_ns()` 在宿主机物理 CPU 上测量真实执行耗时，将实测纳秒/微秒数据序列化保存至 `measurements.json`，再回填至报告表格中，做到数据 100% 真实有据可查。

#### 📦 原理解析 4：零缓存纯净归档与 GitHub 非 ASCII 文件名防截断
- **痛点黑盒**：
  1. Python 运行后会在各级目录留下大量的 `__pycache__` 文件夹和 `.pyc` 字节码文件，直接压缩会导致提交物脏乱；
  2. GitHub Release 在上传非 ASCII 资源文件时，会将中文字符自动截断（例如 `2024000001张三实验1.zip` 会被 GitHub 自动截断为 `2024000001.zip`），导致学生或助教下载后名称残缺。
- **破解原理**：
  1. **纯净文件树遍历**：`auto_exp/releaser.py` 在 Zip 打包阶段执行黑名单递归剪枝，绝对排除所有 `__pycache__`、`.pyc` 及测试中间日志；
  2. **Release 顶部改名脚本**：在自动生成 GitHub Release 说明时，在文档最顶部生成一段包含正确中文全称的一键重命名 Shell 指令块，方便助教下载后一行命令一键恢复规范中文文件名。

#### 🔒 原理解析 5：公私数据多层物理隔离与提交拦截体系
- **痛点黑盒**：公开自动化仓库很容易由于手滑，将包含真实学号、姓名、私人 Token 的配置文件提交到 GitHub，造成不可逆的公网隐私泄露。
- **破解原理**：
  1. **物理隔离**：版本库追踪的 `config.example.yaml` 与测试用例中一律仅使用白名单假数据（“张三”、“2024000001”）；真实个人数据只存放在本地 `config.local.yaml`，受 `.gitignore` 保护；
  2. **Git 暂存区预检拦截**：`scripts/check_privacy.py` 钩子在 `git commit` 前读取 `git diff --cached` 真实暂存差异，用正则表达式深度扫描真实学号格式与私人密钥，凡有违规立即硬性阻断提交。

---

## 🌟 四、常见问题排查与未来规划 (FAQ & Roadmap)

### 4.1 常见问题排查 (FAQ)

- **Q1: 运行 `./setup.sh` 提示 Pandoc 未安装？**  
  答：Pandoc 是将 Markdown 高保真编译为 Word 文档的核心依赖。在 Ubuntu/Debian 环境下可直接通过包管理器安装：
  ```bash
  sudo apt update && sudo apt install -y pandoc
  ```

- **Q2: 为什么不支持在 Windows 原生 CMD 或 PowerShell 中运行？**  
  答：Linux 的 Shell 语法统一、管道重定向简洁高效；而 Windows PowerShell 带有历史包袱，在特殊字符转义、行尾 CRLF/LF 和子进程管理上极易产生不可预期的排版 bug。**强烈推荐使用 Windows WSL2 (Ubuntu)**，获得最稳定可靠的开发体验。

- **Q3: 为什么 Phase 2 必须设计为人机协作贴图，而不是直接全自动结束？**  
  答：工科实验报告普遍包含真实硬件开发板（如单片机、FPGA）、示波器波形或特定 GUI 工具界面。大模型无法脱离现实凭空制造真实的电路实物图像。通过导出结构化清单 `assembly_manifest.json`，确保实验数据的严肃性与严谨性。

- **Q4: 更换电脑或重装系统后，如何恢复已有的实验？**  
  答：本项目数据完全本地解耦。只需备份好您专属的 `workspace/` 目录以及 `config.local.yaml`，在新设备上运行 `./setup.sh` 后放回原位，即可无缝继续执行断点续跑。

---

### 4.2 未来演进路线 (Roadmap)

- [x] **v0.1.0**：完成 7 专职 Agent 阵列设计、三阶段门禁流转、表格 AST 强断言与隐私防线；
- [x] **v0.1.1**：内置 `workspace/` 规范拓扑与根目录一键脚本，全面适配 100% 纯 Markdown 跨平台高保真渲染；
- [ ] **Phase 2 自动化 (Computer Use 接管)**：引入 **Computer Use Agent**，直接驱动宿主机终端与系统窗口，全自动完成命令触发、窗口截屏与 Word 贴图，实现从 Phase 1 到 Phase 3 真正的全流程端到端零人工干预闭环。

---

### 4.3 开源许可证与贡献

本项目采用 [Apache 2.0 开源许可证](file:///home/deepjh/workspace/auto-exp-report/LICENSE)。  
欢迎提交 Issue 或 Pull Request 共同改进！如有任何疑问或特性建议，请前往 **[GitHub Issues](https://github.com/DeepJH/auto-exp-report/issues)** 反馈交流。
