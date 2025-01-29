from time import time
import os
os.remove("output.txt")

file = open("output.txt", "a")
def searching(board: list, n: int, placed: int, l: int, res: list, attacked: set, x0=0, y0=0):
    """поиск верных комбинаций"""
    if placed == l:
        # сохранение верной комбинации с последующим её занесением в список результатов
        comb = ((row, col) for row in range(0, n) for col in range(0, n) if board[row][col] == 1)
        if comb not in res:
            global file
            file.write(" ".join(f"{x, y}" for x, y in list(comb)))
            file.write("\n")
            res.append(list(comb))
        attacked.clear()
        return
    for x in range(x0, n):
        for y in range(y0 + 1 if x == x0 else 0, n):
            # проверка на то, что клетка для установления фигуры не находится под боем и
            # дальнейшее её занесение в переменную attacked вместе с полями, которые атакует эта фигура
            if (x, y) not in attacked:
                attacked1 = attacked.copy()
                board[x][y] = 1
                save_attacked_fields(n, x, y, attacked)  # TODO реализовать проверку
                searching(board, n, placed + 1, l, res, attacked, x, y)
                board[x][y] = 0
                attacked = attacked1.copy()


def save_attacked_fields(n: int, x: int, y: int, attacked: set):
    """сохранение атакованных полей"""
    if (x, y) in attacked:
        return
    attacked.add((x, y))
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for dx, dy in directions:
        x1 = x + dx  # новая координата строки клетки поля для короля
        y1 = y + dy  # новая координата столбца клетки поля для короля
        if 0 <= x1 < n and 0 <= y1 < n:
            # сохранение клетки поля, находящейся под боем
            attacked.add((x1, y1))
    for dx, dy in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
        x1 = x + dx  # новая координата строки клетки поля для слона
        y1 = y + dy  # новая координата столбца клетки поля для слона
        while 0 <= x1 < n and 0 <= y1 < n:
            attacked.add((x1, y1))  # сохранение клетки поля, находящейся под боем
            x1 = x1 + dx  # новая координата строки клетки поля для слона
            y1 = y1 + dy  # новая координата столбца клетки поля для слона


def steps(board: list, N: int, x: int, y: int):
    """отображение клеток, стоящих под боем"""
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for dx, dy in directions:
        x1 = x + dx  # новая координата строки клетки поля для короля
        y1 = y + dy  # новая координата столбца клетки поля для короля
        if 0 <= x1 < N and 0 <= y1 < N:
            # помечание клетки, находящейся под боем
            board[x1][y1] = "*"
    for dx, dy in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
        x1 = x + dx  # новая координата строки клетки поля для слона
        y1 = y + dy  # новая координата столбца клетки поля для слона
        while 0 <= x1 < N and 0 <= y1 < N:
            board[x1][y1] = "*"  # помечание клетки, находящейся под боем
            x1 = x1 + dx  # новая координата строки клетки поля для слона
            y1 = y1 + dy  # новая координата столбца клетки поля для слона


def showing(count: int, combinations: list, n: int):
    """отображение поставленных фигур"""
    for i, comb in enumerate(combinations, 0):
        if count == i:
            break
        print(f"Комбинация {i + 1}")
        desk = creation(n)  # создание доски
        for x, y in comb:
            desk[x][y] = "#"  # отмечаем поле, на котором находится фигура
            steps(desk, n, x, y)
        for x in desk:
            print(" ".join(x))  # распечатывание доски с отмеченными фигурами и полями, находящимися под боем


def creation(n: int):
    """создание доски"""
    desk = [["0"] * n for i in range(n)]
    return desk


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
    inp1 = lines[0].split()
    inp2 = lines[1:]
    N = int(inp1[0])  # сторона доски
    L = int(inp1[1])  # количество фигур, которые нужно расставить на доске
    K = int(inp1[2])  # количество предустановленных фигур
    board = [[0]*N for i in range(N)]  # создаём доску
    attacked_fields = set()  # множество полей, находящихся под ударом
    for a in inp2[:K]:
        a = a.split()
        x = int(a[0])  # строка доски
        y = int(a[1])  # столбец доски
        board[x][y] = 1  # установка фигуры по заранее запланированным координатам
        save_attacked_fields(N, x, y, attacked_fields)
    results = []  # список всех возможных вариантов
    start = time()  # начало отсчёта времени
    searching(board, N, 0, L, results, attacked_fields)
    file.close()
    end = time()  # конец отсчёта времени
    print(f"Кол-во вариантов: {len(results)}, параметры: {N, L, K}, время: {round(end - start, 2)}")
    # with open("output.txt", "w") as file:
    #     for result in results:
    #         записываем в файл отдельными строками каждую комбинацию
            # file.write(" ".join(f"{x, y}" for x, y in result))
            # file.write("\n")
        # if not results:
        #     file.write("No solution")
    if not results:
        print("No solution")
    try:
        # показ досок с фигурами и находящимися под боем полями
        s = int(input("количество досок с фигурами: "))
        showing(s, results, N)
    except:
        print("введены некорректные данные")
