from time import perf_counter


def get_combination(fields, needs, placed, board_size, combinations=None):
    """Поиск комбинаций размещения фигур"""
    if combinations is None:
        combinations = []

    if placed == needs:
        solutions.append(tuple(combinations))
        return True

    while fields:
        # ставим новую фигуру
        x, y = fields.pop()

        combinations.append((x, y))
        save = fields.copy()
        # удаляем битые поля вновь добавленной фигурой
        remove_attacked_cells(fields, x, y, board_size)

        get_combination(fields, needs, placed + 1, board_size, combinations)

        # Восстанавливаем предыдущее состояние (убираем фигуру)
        combinations.pop()  # Удаляем последнюю добавленную комбинацию
        fields = save.copy()
    return False


def remove_attacked_cells(fields, x: int, y: int, N: int) -> set:
    """Удаление с доски битых и занятых полей."""
    fields.discard((x, y))

    # Проход по горизонтали и вертикали соседних ячеек
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            fields.discard((nx, ny))

    # Проход по диагоналям
    for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        nx, ny = x + dx, y + dy
        while 0 <= nx < N and 0 <= ny < N:
            fields.discard((nx, ny))
            nx += dx
            ny += dy


if __name__ == '__main__':
    # обработка исходных данных
    with open("input.txt", 'r') as file:
        lines = file.readlines()
        data = list(map(int, lines[0].split()))
        # размер доски; дополнительное количество фигур для размещения; количество предустановленных фигур
        N, L, K = data[0], data[1], data[2]
        # координаты преустановленных фигур
        positions = [tuple(map(int, line.split())) for line in lines[1:K+1]]
    # создание доски
    board = set()
    for n in range(N):
        for m in range(N):
            board.add((n, m))
    preocupated = []  # писок координат предустановленных фигур
    # обработка предустановленных фигур
    for x, y in positions:
        preocupated.append((x, y))
        remove_attacked_cells(board, x, y, N)

        solutions = []  # список координат найденных решений
        start_time = perf_counter()
        # Запускаем рекурсивное размещение фигур
        get_combination(board, L, 0, N)

        end_time = perf_counter()
        total_time = end_time - start_time
        amount = len(solutions)
        print(f'Количество вариантов: {amount}\t Параметры: {N, L, K}\t Время поиска: {total_time:.2f} c')

        # Записываем результаты в output.txt
        with open("output.txt", 'w') as out_file:
            print(f'Идет запись в файл...')
            if not solutions:
                out_file.write("no solution")
            for solution in solutions:
                full_solution = preocupated + list(solution)  # добавляем координаты предустановленных фигур
                out_file.write("".join(f"({x},{y})" for x, y in full_solution) + "\n")