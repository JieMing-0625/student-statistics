"""学生信息统计工具
功能：读取学生 JSON 数据，统计成绩，输出结果到文件
"""
import json
from pathlib import Path



# 项目根目录（从 src/ 上跳一级到项目根）
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "students.json"
OUTPUT_DIR = BASE_DIR / "output"


def load_students(path: Path):
    if not path.exists():
        print(f"错误：文件不存在 - {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            students = json.load(f)
        return students
    except json.JSONDecodeError:
        print(f"错误：JSON 格式不正确 - {path}")
        return None



def validate_students(students):
    valid = []
    errors = []
    for i,s in enumerate(students):
        if "id" not in s:
            errors.append(f"第 {i+1} 个学生缺少 id 字段")
            continue
        if "name" not in s:
            errors.append(f"学生 {s['id']} 缺少 name 字段")
            continue
        if "score" not in s:
            errors.append(f"学生 {s['id']} 缺少 score 字段")
            continue
        if not isinstance(s["score"], (int, float)):
            errors.append(f"学生 {s['id']} 的 score 不是数字：{s['score']}")
            continue

        valid.append(s)
    return valid, errors


def calc_average(students):
    total = 0
    for s in students:
        total += s["score"]
    avg = total / len(students)
    return avg


def calc_max_min(students):
    mx = max(students,key=lambda s: s["score"])
    mn = min(students,key=lambda s: s["score"])
    return mx, mn


def count_passed(students):
    passed = 0
    for s in students:
        if s["score"] >= 60:
            passed += 1
    return passed


def find_by_id(students, student_id: str):
    for s in students:
        if s["id"] == student_id:
            return s
    return None


def save_result(content: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("=== 学生信息统计工具 ===")

    students = load_students(DATA_FILE)
    if students is None:
        print("读取数据失败，程序退出。")
        return

    students, errors = validate_students(students)
    if errors:
        print("数据校验警告：")
        for e in errors:
            print(f"  - {e}")

    if not students:
        print("没有有效学生数据，程序退出。")
        return

    # 3. 统计
    avg = calc_average(students)
    max_score, min_score = calc_max_min(students)
    passed = count_passed(students)

    # 4. 查询

    query_id = input("请输入你想要查询的学号:")
    target = find_by_id(students, query_id)
    if target:
        query_line = f"学号 {query_id}: {target['name']}，成绩 {target['score']}"
    else:
        query_line = f"学号 {query_id}: 未找到"

    # 5. 组装结果文本
    result = f"""学生总数: {len(students)}
平均分: {avg:.1f}
最高分: {max_score['name']} ({max_score['score']})
最低分: {min_score['name']} ({min_score['score']})
及格人数(>=60): {passed}
{query_line}
"""

    # 6. 输出到屏幕 + 文件
    print("\n--- 统计结果 ---")
    print(result)
    save_result(result, OUTPUT_DIR / "result.txt")
    print(f"结果已保存到 output/result.txt")


if __name__ == "__main__":
    main()
