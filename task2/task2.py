"""
Задание 2. Положение точек относительно эллипса.

Аргументы командной строки:
    task2.py <файл с центром и радиусами эллипса> <файл с координатами точек>

Файл эллипса (2 строки):
    cx cy   - координаты центра
    rx ry   - радиусы по осям X и Y

Файл точек: на каждой строке координаты одной точки "x y" (от 1 до 100 точек).

Для каждой точки выводится (каждая на отдельной строке):
    0 - точка лежит на эллипсе
    1 - точка внутри эллипса
    2 - точка снаружи эллипса

Используется тип Decimal, чтобы корректно работать с рациональными числами
в диапазоне от 10^-38 до 10^38 без потери точности, характерной для float.
"""
import sys
from decimal import Decimal, getcontext, InvalidOperation


def classify_point(x: Decimal, y: Decimal, cx: Decimal, cy: Decimal,
                    rx: Decimal, ry: Decimal) -> int:
    value = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
    if value == 1:
        return 0
    if value < 1:
        return 1
    return 2


def read_numbers(line: str):
    return [Decimal(token) for token in line.split()]


def main() -> None:
    # Достаточная точность для чисел из диапазона [1e-38, 1e38]
    getcontext().prec = 80

    args = sys.argv[1:]
    if len(args) != 2:
        print(
            "Использование: task2.py <файл_эллипса> <файл_точек>",
            file=sys.stderr,
        )
        sys.exit(1)

    ellipse_path, points_path = args

    try:
        with open(ellipse_path, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        cx, cy = read_numbers(lines[0])
        rx, ry = read_numbers(lines[1])
    except (OSError, InvalidOperation, IndexError, ValueError) as exc:
        print(f"Ошибка чтения файла эллипса: {exc}", file=sys.stderr)
        sys.exit(1)

    results = []
    try:
        with open(points_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                x, y = read_numbers(line)
                results.append(classify_point(x, y, cx, cy, rx, ry))
    except (OSError, InvalidOperation, ValueError) as exc:
        print(f"Ошибка чтения файла точек: {exc}", file=sys.stderr)
        sys.exit(1)

    for r in results:
        print(r)


if __name__ == "__main__":
    main()
