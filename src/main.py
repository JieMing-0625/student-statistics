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
    """读取 JSON 文件，返回学生列表
    需要处理三种异常：
      1. 文件不存在 (FileNotFoundError)
      2. JSON 格式错误 (json.JSONDecodeError)
      3. 文件是空的
    返回：学生列表；如果出错返回 None
    """
    # TODO: 实现这个函数
    # 提示：
    # 1. if not path.exists(): 打印错误，return None
    # 2. with open(path, "r", encoding="utf-8") as f:
    #      students = json.load(f)
    # 3. 用 try/except 包住，打印具体错误信息

    if not path.exists():
        print(f'wrong,the text is not exist - {path}')
        return None
    else:
        try:
           with open(path, "r", encoding="utf-8") as f:
               students = json.load(f)
               return students
        except FileNotFoundError:
            print('can\'t find the text')
            return None
        except json.JSONDecodeError:
            print('json error')
            return None



def validate_students(students):
    """校验每个学生是否有 id、name、score 三个字段，且 score 是数字
    返回：(合法学生列表, 错误信息列表)
    """
    valid = []
    errors = []
    for i,s in enumerate(students):
        # TODO: 检查 s 里有没有 "id"、"name"、"score"
        # 如果缺字段，往 errors 里加一条说明
        # 如果 score 不是数字（int/float），也记为错误
        # 合法的才 append 到 valid
        if "id" not in s:
            errors.append(f"the {i+1} lack id")
            continue
        if "name" not in s:
            errors.append(f"student{s['id']} lack name")
            continue
        if "score" not in s:
            errors.append(f"student{s['id']} lack score")
            continue
        if not isinstance(s["score"], (int,float)):
            errors.append(f'student{s["id"]} score is not int or float')
            continue

        valid.append(s)
    return valid, errors


def calc_average(students):
    """计算平均分，保留一位小数"""
    # TODO: 平均分 = 总分 / 人数
    total = 0
    for s in students:
        total += s["score"]
    avg = total / len(students)
    return avg


def calc_max_min(students):
    """返回 (最高分, 最低分)"""
    # TODO: 用 max() 和 min()，key=lambda s: s["score"]
    mx = max(students,key=lambda s: s["score"])
    mn = min(students,key=lambda s: s["score"])
    return mx, mn


def count_passed(students):
    """统计及格人数（score >= 60）"""
    # TODO
    passed = 0
    for s in students:
        if s["score"] >= 60:
            passed += 1
    return passed


def find_by_id(students, student_id: str):
    """根据学号查找学生，找不到返回 None"""
    # TODO: 遍历比较 s["id"] == student_id
    for s in students:
        if s["id"] == student_id:
            return s
    return None


def save_result(content: str, path: Path):
    """把结果写入文件，自动创建 output 目录"""
    # TODO:
    # path.parent.mkdir(parents=True, exist_ok=True)
    # with open(path, "w", encoding="utf-8") as f:
    #     f.write(content)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("=== 学生信息统计工具 ===")

    # 1. 读取数据
    students = load_students(DATA_FILE)
    if students is None:
        print("读取数据失败，程序退出。")
        return

    # 2. 校验数据
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
