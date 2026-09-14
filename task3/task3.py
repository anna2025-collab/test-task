"""
Задание 3. Формирование report.json на основании tests.json и values.json.

Аргументы командной строки (в указанном порядке):
    task3.py <values.json> <tests.json> <report.json>

values.json - плоский список результатов прохождения тестов с уникальными id:
    {"values": [{"id": 2, "value": "passed"}, ...]}

tests.json - вложенная структура отчёта (вложенность произвольной глубины),
где узлы могут содержать поле "value" (которое нужно заполнить) и/или список
дочерних узлов "values":
    {"tests": [{"id": 2, "title": "...", "value": ""}, ...]}

report.json - результат: та же структура, что и в tests.json, но с
заполненными полями "value" на основании values.json (по совпадению id).
Узлы, для чьих id не нашлось значения в values.json, остаются без изменений.
"""
import sys
import json


def build_values_map(values_data: dict) -> dict:
    return {item["id"]: item["value"] for item in values_data.get("values", [])}


def fill_values(node, values_map: dict) -> None:
    """Рекурсивно проходит структуру tests.json и заполняет поле "value"
    у узлов, у которых оно присутствует, используя values_map по id."""
    if isinstance(node, dict):
        if "id" in node and "value" in node and node["id"] in values_map:
            node["value"] = values_map[node["id"]]
        # Дочерние узлы хранятся в списке "values" (не путать с полем "value")
        children = node.get("values")
        if isinstance(children, list):
            for child in children:
                fill_values(child, values_map)
        # На случай другой вложенности (например, "tests" внутри узла)
        for key, val in node.items():
            if key != "values" and isinstance(val, (dict, list)):
                fill_values(val, values_map)
    elif isinstance(node, list):
        for item in node:
            fill_values(item, values_map)


def main() -> None:
    args = sys.argv[1:]
    if len(args) != 3:
        print(
            "Использование: task3.py <values.json> <tests.json> <report.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    values_path, tests_path, report_path = args

    with open(values_path, encoding="utf-8") as f:
        values_data = json.load(f)
    with open(tests_path, encoding="utf-8") as f:
        tests_data = json.load(f)

    values_map = build_values_map(values_data)
    fill_values(tests_data, values_map)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(tests_data, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
