# Built-in Workspace (默认内置实验工作区)

本目录为 `auto-exp-report` 系统默认的内置实验工作区。

## 目录组织方式

在此目录下创建各门课程子目录，并将任课教师下发的实验材料放入对应的 `resource/` 文件夹中：

```text
workspace/
└── <course_slug>/                          # 课程标识符（如 cryptography、embedded-system-security）
    ├── resource/                           # 【输入材料只读真理源】
    │   ├── 《XXX》实验指导书.pdf/.docx
    │   └── （XXX）学号-姓名-实验X报告模板.docx
    └── exps/<exp_id>/                      # 【实验流水线生成的工作区（自动产出）】
        ├── guide.md
        ├── src/
        ├── measurements.json
        ├── report.md
        ├── report.docx
        ├── assembly_manifest.json
        └── release/
```
