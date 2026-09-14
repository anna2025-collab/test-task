"""
Задание 4. Минимальное количество ходов для выравнивания массива.

За один ход можно увеличить или уменьшить один элемент массива на 1.
Нужно найти минимальное суммарное количество ходов, чтобы все элементы
массива стали равны одному и тому же числу. Ограничение — не более 20 ходов.

Элементы массива читаются построчно из файла, путь к которому передаётся
аргументом командной строки:
    task4.py <файл_с_числами>

Минимальная суммарная сумма |a_i - x| по всем i достигается, когда x - медиана
массива, поэтому достаточно отсортировать массив и посчитать отклонения от
медианы.
"""
import sys

MAX_MOVES = 20


def min_moves_to_equalize(nums: list) -> int:
    sorted_nums = sorted(nums)
    median = sorted_nums[len(sorted_nums) // 2]
    return sum(abs(x - median) for x in nums)


def main() -> None:
    args = sys.argv[1:]
    if len(args) != 1:
        print("Использование: task4.py <файл_с_числами>", file=sys.stderr)
        sys.exit(1)

    file_path = args[0]
    try:
        with open(file_path, encoding="utf-8") as f:
            nums = [int(line.strip()) for line in f if line.strip()]
    except (OSError, ValueError) as exc:
        print(f"Ошибка чтения файла: {exc}", file=sys.stderr)
        sys.exit(1)

    if not nums:
        print("Файл не содержит чисел", file=sys.stderr)
        sys.exit(1)

    moves = min_moves_to_equalize(nums)

    if moves <= MAX_MOVES:
        print(moves)
    else:
        print(
            "«20 ходов недостаточно для приведения всех элементов "
            "массива к одному числу»"
        )


if __name__ == "__main__":
    main()
