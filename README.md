# 学生信息统计工具

## 项目功能
读取学生成绩 JSON 文件，统计平均分、最高分、最低分、及格人数，并支持按学号查询。

## 运行环境
- Python 3.10+
- 无第三方依赖（只用标准库）

## 如何运行
```powershell
cd student-statistics
python src/main.py
```

## 输入数据格式
`data/students.json` 是一个 JSON 数组，每个学生对象包含：
- `id`：学号（字符串）
- `name`：姓名（字符串）
- `score`：成绩（数字，0-100）

示例：
```json
[
  { "id": "2026001", "name": "Alice", "score": 92 }
]
```

## 输出内容
程序会在终端打印统计结果，并保存到 `output/result.txt`。

## 已知限制
- 成绩范围假设为 0-100，未做越界校验
- 查询学号目前写死在代码里，未做成命令行参数
