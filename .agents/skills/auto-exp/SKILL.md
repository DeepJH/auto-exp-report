---
name: auto-exp
description: Autonomous multi-agent engineering workflow for university lab reports across Phase 1 (Research & Drafting), Phase 2 (Screenshot & Assembly Handoff), and Phase 3 (Clean Delivery & Release). Use via /auto-exp <course> <N>.
---

# Auto Exp Report Orchestration Skill

A disciplined, reproducible multi-agent engineering workflow system for university engineering lab reports, dividing labor across **7 specialized subagents** guided by strict quality gates.

## 核心心法与铁律（Core Philosophy）

1. **以指导书和报告模板为第一真理源（Templates & Manuals First）**：
   - 实验的章节体系完全由官方实验报告模板决定。
   - **没有的绝对不要做（No Unrequested Work）**：模板或指导书中未要求的内容（例如没有独立的思考题章节等），坚决不做，严禁擅自加戏。
2. **严禁将用户的 Prompt 元指令当作正文输出（No Meta-Instruction Leaks）**：
   - 报告正文中严禁出现 `（含代码占位符）`、`此处为代码占位` 等机械指令字样，必须使用正规技术报告标题与完整代码展示。
3. **如实交代器材替代（Factual Substitutions）**：
   - 遇器材限制客观说明原因（如采用板载 LED 等效验证），严禁主观臆断学生的态度（如嫌接线麻烦）。
4. **工作区解耦与定位（Workspace Definition）**：
   - 单一实验工作区定义为 `<workspace_root>/<course>/exps/<exp_id>/`；
   - 允许通过 `config.yaml` 中的 `workspace_dir` 自定义根路径（默认为 `.`），支持生成引擎与报告归档仓库物理解耦。
5. **表格 AST 状态机规范与终稿多维断言**：
   - Markdown 表格前后必须由状态机保留至少一行空行，而表格内部行与行紧密相连，杜绝 Pandoc 管道符降级；
   - 终稿 docx 必须通过体积 (>100KB) 与内部嵌入图片（`word/media/` 非空）双重断言方可放行。
6. **工作三阶段严格隔离**：
   - **Phase 1（全自动）**：完成代码、测试、初稿并在通过 AST 表格断言后**立刻停机**；
   - **Phase 2（人机协作）**：输出操作清单交由学生在宿主机实操截图并填入官方模板另存为终稿；
   - **Phase 3（全自动）**：终稿验收合格后，执行纯净无缓存打包并发布 GitHub Release。
7. **公网隐私零泄漏防御（Privacy Guard）**：
   - 追踪文件必须 100% 使用假数据（“张三”、“2024000001”）；真实配置只能存在于本地被忽略的 `*.local.*` 中。

---

## 7 专职 Agent 阵列职责与分工

```text
========================================================================================
[调度器 Orchestrator] 统筹生命周期与状态流转 (workflow_state.json)
========================================================================================
  Phase 1:
    1. 逆向解构师 (Inspector)   : 扫描模板大纲与字段 -> guide.md + 待填模板.docx
    2. 实验工程师 (Engineer)    : 编写极简源码与测试集 -> src/
    3. 测试测量员 (Tester)      : 实跑测试采集真实纳秒耗时 -> measurements.json
    4. 报告起草员 (Writer)      : 严格镜像大纲草拟 -> report.raw.md (截图留空)
    5. 独立润色员 (Humanizer)   : 去 AI 腔调/学生口吻润色 -> report.docx (AST表格断言通过)
    ==> 【Phase 1 门禁停机，移交组装员】
  Phase 2:
    6. 报告组装员 (Assembler)   : 输出截图清单与命令 -> 挂起等待学生贴图终稿
                                : 验收终稿 (体积 > 100KB, 图片已嵌入)
                                (未来无缝升级为 Computer Use 自动化 Agent)
    ==> 【Phase 2 门禁通过，移交发布】
  Phase 3:
    7. 交付归档员 (Releaser)    : 纯净打包(0 pycache) -> release/*.zip + docx
                                : Git 推送对齐，GitHub Release 发布 (带置顶中文改名提示)
========================================================================================
```

---

## 快速使用指令 (Execution Workflow)

在当前工作区启动终端或会话，执行以下步骤：

### 1. 触发实验研制 (Phase 1)
```bash
.venv/bin/python3 -m auto_exp.cli run <course_slug> <exp_id>
```
*例如：* `.venv/bin/python3 -m auto_exp.cli run cryptography 1`
- 自动完成模板解构、代码编写、数据采集与润色；
- 运行 `scripts/assert_docx_tables.py` 确保 Word 原生表格完好；
- **自动挂起**并打印清晰的 Phase 2 人机交接单。

### 2. 人机协作贴图 (Phase 2)
- 用户在电脑上运行操作单列出的命令并截取终端/硬件图；
- 打开实验目录下的空白模板，将截图贴入并另存为：`exps/<N>/<学号><姓名>实验<N>报告.docx`。

### 3. 终稿验收与发布 (Phase 3)
```bash
.venv/bin/python3 -m auto_exp.cli resume <course_slug> <exp_id>
```
- 组装员自动核验文件体积与图片嵌入完整度；
- 验收通过后，交付归档员自动排除所有 `__pycache__` 生成纯净 zip，并创建 GitHub Release。
