# auto-exp-report

[![GitHub Repo](https://img.shields.io/badge/GitHub-DeepJH%2Fauto--exp--report-181717?logo=github)](https://github.com/DeepJH/auto-exp-report)
[![Release](https://img.shields.io/badge/Release-v0.1.0-orange)](https://github.com/DeepJH/auto-exp-report/releases)
[![Issues](https://img.shields.io/github/issues/DeepJH/auto-exp-report?color=green)](https://github.com/DeepJH/auto-exp-report/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/DeepJH/auto-exp-report/blob/main/LICENSE)

> 🎓 **高校工科与计算机实验报告多 Agent 自动化工程流水线**  
> 依托 Google Antigravity (agy) 原生子代理编排，严格遵循三阶段隔离门禁、模板大纲驱动、去 AI 学术腔调与公网假数据物理隔离。  
> 🔗 **官方开源地址**：[https://github.com/DeepJH/auto-exp-report](https://github.com/DeepJH/auto-exp-report)

---

## 目录

- [一、这是什么东西，能干什么](#一这是什么东西能干什么)
  - [1. 这是什么东西](#1-这是什么东西)
  - [2. 解决的核心痛点](#2-解决的核心痛点)
  - [3. 能干什么（全生命周期能力）](#3-能干什么全生命周期能力)
- [二、怎么用的（Quick Start、概念与做法，及详细进阶教程）](#二怎么用的quick-start概念与做法及详细进阶教程)
  - [1. 极速上手 (Quick Start)](#1-极速上手-quick-start)
  - [2. 核心概念与做法 (Concepts & Practice)](#2-核心概念与做法-concepts--practice)
  - [3. 详细进阶教程 (Advanced Guide)](#3-详细进阶教程-advanced-guide)
- [三、特点与原理](#三特点与原理)
  - [1. 7 专职 Agent 阵列协同架构](#1-7-专职-agent-阵列协同架构)
  - [2. 表格 AST 强断言与格式防劣化机制](#2-表格-ast-强断言与格式防劣化机制)
  - [3. 独立 Humanizer 去 AI 腔演化原理](#3-独立-humanizer-去-ai-腔演化原理)
  - [4. 纯净归档与 Release 中文重命名自动化](#4-纯净归档与-release-中文重命名自动化)
  - [5. Privacy Guard 公网隐私防线](#5-privacy-guard-公网隐私防线)

---

## 一、这是什么东西，能干什么

### 1. 这是什么东西

`auto-exp-report` 是一套专为高校工科与计算机专业打造的**多 Agent 协同实验报告自动化工程流水线**。

它原生运行于 Google Antigravity (`agy`) 平台环境，通过将复杂的“写实验代码、跑真实测试、算基准性能、逆向排版模板、撰写初稿、去 AI 痕迹润色、贴实操截图、打包归档交付”拆解为 7 个各司其职的专职子代理与严苛的 3 阶段工作流门禁，帮助高校学生和研究人员摆脱繁琐冗余的报告排版与格式机械劳动。

### 2. 解决的核心痛点

在传统的实验报告撰写与现存的大模型辅助生成方案中，普遍存在以下严重痛点：

1. **模板格式混乱与大纲漂移**：大模型生成内容时容易自作主张新增不属于模板的章节，或遗漏老师强制要求的必填表格；
2. **严重的 AI 腔调与空话套话**：常见生成工具充满“综上所述”、“显而易见”、“具有重要意义”等八股套话，极易被任课教师识破；
3. **测试数据凭空捏造（幻觉假数据）**：大模型无法直接在本地环境执行复杂算法，报告中的吞吐量、纳秒延时、内存占用往往全凭模型脑补；
4. **Markdown 导出 Word 时表格静默退化**：Pandoc 在编译缺乏严格空行包裹的管道符表格时，会静默将其退化为纯文本段落（残存大量 `|` 字符），排版瞬间崩坏；
5. **实操截图与硬件调试无法无缝衔接**：传统脚本要么妄图假装自己截了图，要么流程直接断裂，缺少清晰的人机协同交接契约；
6. **公网个人隐私泄漏隐患**：开源自动化项目常诱导学生将真实的学号、姓名、班级和敏感令牌硬编码并提交至公开 GitHub 仓库。

### 3. 能干什么（全生命周期能力）

`auto-exp-report` 提供贯穿实验全生命周期的自动化工程能力：

- **大纲与模板逆向**：自动提取课程官方实验指导书与 Word 模板大纲，生成单一真理源（SSoT），模板没有的坚决不做；
- **全真实代码与性能实测**：在宿主环境生成并执行算法代码及行级 I/O 校验用例，采集微秒/纳秒级真实性能耗时回填报告；
- **表格 AST 强校验**：自动校验编译生成的 Word 文档原生表格节点数（>= 2）与段落文本，杜绝任何管道符退化；
- **纯正学生口吻润色 (Humanizer)**：重写主观调试心得与反思，还原“亲自动手踩坑调试”的工科本科生真实口吻；
- **清晰的人机交接协议**：导出结构化组装清单 `assembly_manifest.json`，明确告知用户需要实操截取的终端/硬件图，并预留未来 Computer Use 自动截屏能力；
- **强校验交付与纯净归档**：校验终稿文件体积（> 100KB）与内部媒体图片嵌入，自动剥离所有 `__pycache__` 与 `.pyc` 缓存，打包规范格式的纯净 Zip 并发布带中文重命名指引的 GitHub Release。

---

## 二、怎么用的（Quick Start、概念与做法，及详细进阶教程）

### 1. 极速上手 (Quick Start)

#### 运行环境要求
- **操作系统**：Linux 原生系统 或 Windows WSL2 (Ubuntu)。（Windows 原生 PowerShell 语法冗杂且存在历史包袱，严禁直接运行，请移步 WSL2）；
- **环境依赖**：Python 3.10+、Git、Pandoc（用于编译 Word 文档）、GitHub CLI (`gh`，用于自动发布 Release）。

#### 步骤 1：一键初始化环境
本项目严格遵循 Linux PEP 668（externally-managed-environment）规范，通过根目录的一键配置脚本自动创建 `.venv` 虚拟环境，不污染系统全局：

```bash
# 克隆代码仓库
git clone https://github.com/DeepJH/auto-exp-report.git
cd auto-exp-report

# 执行根目录一键配置脚本
./setup.sh

# 激活虚拟环境
source .venv/bin/activate
```

#### 步骤 2：配置本地个人信息（仅需一次）
复制示例配置并填入您的真实信息。该文件被 `.gitignore` 彻底物理隔离，绝不会提交至公网：

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

#### 步骤 3：三步极速完成一次实验报告
以“密码学基础与应用”课程的实验 1 为例：

1. **投入输入材料**：
   ```bash
   mkdir -p workspace/cryptography/resource
   # 将老师给的《指导书》和官方 Word 报告模板放入 resource/ 目录
   ```
2. **触发 Phase 1 全自动研制**：
   ```bash
   python3 -m auto_exp.cli run cryptography 1
   ```
   流水线全自动完成逆向提取、代码编写、数据测试、Word 初稿编译与 AST 表格校验，并在控制台打印出实操截图交接清单后安全挂起。
3. **补充截图并触发 Phase 3 终稿交付**：
   按交接清单提示，将初稿内容和真实测试截图填入待填模板，另存为 `workspace/cryptography/exps/1/2024000001张三实验1报告.docx`，随后执行恢复交付：
   ```bash
   python3 -m auto_exp.cli resume cryptography 1
   ```
   流水线完成终稿图片强校验、纯净打包与自动发布。

---

### 2. 核心概念与做法 (Concepts & Practice)

#### (1) 唯一真理源 (Single Source of Truth, SSoT)
- **概念**：官方讲义与官方 Word 报告模板是最高真理。
- **做法**：Inspector 代理只从 `workspace/<course_slug>/resource/` 读取材料，逆向生成结构化大纲 `guide.md`。实验报告的章节与必填项完全镜像该大纲，**严禁超纲答题**。

#### (2) Report Workspace 拓扑结构
仓库默认内置 `workspace/` 作为实验根工作区，隔离布局如下：

```text
auto-exp-report/
├── setup.sh                                # 根目录一键环境配置入口
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

#### (3) 三阶段隔离生命周期 (Three-Phase Lifecycle)
- **Phase 1 (全自动研制)**：逆向大纲 -> 编码实测 -> 初稿起草 -> 消除 AI 腔 -> Word 编译与表格 AST 断言 -> 导出交接单 -> **强行停机挂起**。
- **Phase 2 (人机协作贴图)**：提供结构化的操作交接清单（现阶段由学生执行命令截取真实窗口画面填入 Word 另存；预留标准接口供未来接入 Computer Use Agent 自动贴图）。
- **Phase 3 (验收与纯净交付)**：对终稿文件执行双重强验收（体积 > 100KB 且内部 `word/media/` 包含图片） -> 剥离编译缓存打包纯净 Zip -> 推送并发布 GitHub Release。

---

### 3. 详细进阶教程 (Advanced Guide)

#### (1) 在 Antigravity 对话中直接驱动
除了在终端运行 Python 模块，本项目深度适配了 Antigravity (`agy`) 原生 Agent 技能体系。在 Antigravity 会话窗口中，直接下发指令即可调用专职 Agent 团队：

```text
/auto-exp cryptography 1
```

Antigravity 会根据 `.agents/skills/auto-exp/SKILL.md` 的规范，按序唤起专职子代理自主研制并向您实时汇报进度。

#### (2) 状态查询与断点续跑
如果流水线在某一步被中断，或者需要确认当前进度，可随时通过 CLI 检查或恢复：

```bash
# 检查当前实验进行到了哪一阶段、产生的文件与下一步动作
python3 -m auto_exp.cli status cryptography 1

# 恢复挂起流程（例如完成贴图后执行 Phase 3 验收交付）
python3 -m auto_exp.cli resume cryptography 1
```

#### (3) 外部私有报告仓解耦模式
若希望将此自动化工程工具与您个人的私有实验报告仓库彻底物理隔离，只需在 `config.local.yaml` 中将 `workspace_dir` 指向外部绝对路径：

```yaml
workspace_dir: "/home/deepjh/workspace/my-private-lab-reports"
```

流水线会自动读取并输出到该外部目录，代码仓库本身保持纯净开源。

---

## 三、特点与原理

### 1. 7 专职 Agent 阵列协同架构

流水线采用职责高度单一的专职 Agent 阵列，由调度器（Orchestrator）基于 `workflow_state.json` 强状态机进行严谨编排：

```text
[Orchestrator 调度中枢] (基于 workflow_state.json 驱动三阶段状态流转)
  │
  ├── Phase 1 全自动研制
  │   ├── 1. 逆向解构师 (Inspector Agent)   : 提取 guide.md 规范与待填模板
  │   ├── 2. 实验工程师 (Engineer Agent)    : 编写 minimal 核心算法代码 -> src/
  │   ├── 3. 测试测量员 (Tester Agent)      : 运行真实测试并纳秒计时 -> measurements.json
  │   ├── 4. 报告起草员 (Writer Agent)      : 严格镜像大纲编写初稿 -> report.raw.md
  │   └── 5. 独立润色员 (Humanizer Agent)   : 去八股腔/自然学生视角 -> report.docx (AST断言)
  │
  ├── Phase 2 人机协同接力 (未来 Computer Use 无缝接入)
  │   └── 6. 报告组装员 (Assembler Agent)   : 导出 assembly_manifest.json 挂起等待贴图
  │                                         : 双重阈值验收终稿 (体积 > 100KB, 图片已嵌入)
  └── Phase 3 纯净归档交付
      └── 7. 交付归档员 (Releaser Agent)    : 纯净打包 (0 pycache) -> release/*.zip
                                            : 对齐 Git 推送并自动发布带中文改名指引的 Release
```

### 2. 表格 AST 强断言与格式防劣化机制

#### 痛点根源
使用 Pandoc 将 Markdown 编译为 Word 时，Markdown 管道符表格前后若未保留空行，或表头与分隔行之间存在空行错位，Pandoc 会**静默降级**，将表格输出为纯文本段落（残存大量 `|` 字符），导致文档在 Word 中完全报废。

#### 实现原理
`auto_exp/phase1.py` 和 `scripts/assert_docx_tables.py` 实现了 Pandoc AST（抽象语法树）双向强断言：
1. **Word 节点校验**：通过 `python-docx` 检查编译后的 `report.docx` 中原生 `Table` XML 节点数必须 `>= 2`（至少包含信息表与测试结果表）；
2. **残余段落扫描**：逐段遍历文档中的所有文本段落，严禁出现包含 2 个以上 `|` 管道符的段落（误降级的表格残片）；
3. **状态机安全排版**：在生成 Markdown 时采用行状态机，严格确保表格外部具有独立空行，而表格内部行紧密连续，彻底封死格式退化暗坑。

### 3. 独立 Humanizer 去 AI 腔演化原理

#### 痛点根源
直接让通用 LLM 撰写实验总结与反思，往往充斥着过度工整的排比句、宏大叙事的学术腔（如“本实验不仅深化了理论认识，更提升了实践技能”），显得极为假大空。

#### 实现原理
`auto_exp/humanizer.py` 引入独立的重写算法：
1. **关键词清洗**：扫描并剔除“综上所述”、“不仅……而且……”等刻板八股模板词；
2. **角色语调重构**：将总结与调试心得转换为工科本科生真实动手的自然语调（例如：“在最初实现循环移位时遇到了越界报错，通过单步打印排查出索引计算偏差，修正后通过测试”）；
3. **结构免疫保护**：在重写反思段落时，使用占位符保护代码块、原生 Markdown 表格与截图提示标记不受任何破坏，润色完毕后重新校验表格 AST。

### 4. 纯净归档与 Release 中文重命名自动化

#### 纯净打包设计
高校实验提交对源码目录规范要求严格。`auto_exp/releaser.py` 在执行 Zip 打包时，自动进行递归过滤：
- 严格排除所有 `__pycache__` 文件夹、`.pyc` 字节码文件、临时测试日志；
- 将规范命名的终稿 Word 报告与纯净源码组织为标准的单一交付压缩包。

#### 解决 GitHub 非 ASCII 文件名截断
GitHub Release 上传非 ASCII 资产时，会将中文字符自动截断或转义（例如 `2024000001张三实验1.zip` 会被 GitHub 自动截断为 `2024000001.zip`）。流水线在自动生成 Release Notes 时，在**最顶部置顶一段高亮提示与中文一键重命名代码块**，便于下载者或批改助教一键复制还原标准中文文件名。

### 5. Privacy Guard 公网隐私防线

本项目为公开开源仓库，为防止任何真实个人隐私泄漏，设立了多层物理防线：

1. **示例与跟踪文件 100% 假数据**：仓库追踪的 `config.example.yaml`、测试用例和文档中，统一使用白名单假数据（如姓名 `张三`、学号 `2024000001`）；
2. **本地配置物理隔离**：个人真实数据仅存放在 `config.local.yaml`，该文件已被 `.gitignore` 强力屏蔽；
3. **提交前强校验 (`scripts/check_privacy.py`)**：每次 `git commit` 或 `git push` 前，扫描器扫描 Git 暂存区差异，使用正则表达式强行拦截任何非假数据的真实学号、真实姓名及敏感 Token；凡有违规，硬性中止提交并报警。

---

> 💡 欢迎在使用过程中提交建议或反馈，详见 [GitHub Issues](https://github.com/DeepJH/auto-exp-report/issues)。
