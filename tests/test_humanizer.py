"""
tests/test_humanizer.py
Ticket 4: Humanizer 独立润色模块验证测试
"""

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_exp.humanizer import humanize_report
from scripts.assert_docx_tables import assert_docx_tables


def test_humanizer_pipeline(tmp_path: Path):
    raw_md_path = tmp_path / "report.raw.md"
    report_md_path = tmp_path / "report.md"
    report_docx_path = tmp_path / "report.docx"

    # 构造带有刻板 AI 腔调、代码块、截图留空和标准表格的输入文本
    sample_content = """# 实验报告测试

**表 1-1：学生元信息登记表**

| 学号 | 姓名 | 班级 |
| :--- | :--- | :--- |
| 2024000001 | 张三 | 网安2401 |

## 五、实验步骤

运行命令：
```bash
python3 main.py < input.txt
```

**图 5-1：终端输出截图**  
*(截图留空，待学生实操贴图)*

## 六、实验结果与思考

### 调试体会与心得

综上所述，本实验不仅加深了对核心算法的理解，而且极大地提升了实践操作能力。1. **避免调用栈溢出**：通过循环代替递归；2. **提升内存局部性**：优化数据访问。

**表 1-2：实测数据表**

| 测量项 | 数值 |
| :--- | :--- |
| 耗时 | 12.34 ms |
| 状态码 | 0 |
"""
    with open(raw_md_path, "w", encoding="utf-8") as f:
        f.write(sample_content)

    # 执行 Humanizer 润色与编译
    humanize_report(raw_md_path, report_md_path, report_docx_path)

    # 1. 验证润色后的 report.md
    with open(report_md_path, "r", encoding="utf-8") as f:
        humanized_text = f.read()

    # 断言 A: AI 套话与刻板小标题已被剔除
    assert "综上所述" not in humanized_text, "AI 假大空词汇未被剔除"
    assert "不仅加深了对核心算法的理解" not in humanized_text, "刻板套话未被剔除"
    assert "1. **避免调用栈溢出**：" not in humanized_text, "刻板数字列表未被剔除"

    # 断言 B: 代码块、截图留空与表格 100% 完好无损
    assert "python3 main.py < input.txt" in humanized_text, "代码块被损坏"
    assert "*(截图留空，待学生实操贴图)*" in humanized_text, "截图留空标记被损坏"
    assert "| 2024000001 | 张三 | 网安2401 |" in humanized_text, "表格数据被损坏"
    assert "| 耗时 | 12.34 ms |" in humanized_text, "实测数据表被损坏"

    # 断言 C: report.docx 成功编译并通过 AST 原生表格数量检验 (>= 2) 与管道符零残留
    assert report_docx_path.is_file(), "report.docx 未生成"
    assert_docx_tables(report_docx_path, min_tables=2)
    print("\n✅ test_humanizer_pipeline 全部断言顺利通过！")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        test_humanizer_pipeline(Path(td))
