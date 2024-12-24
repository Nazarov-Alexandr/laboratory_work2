from time import time


def searching(board, n, placed, l, res, attacked, x0=0, y0=0):
    """поиск верных комбинаций"""
    if placed == l:
        comb = ((row, col) for row in range(0, n) for col in range(0, n) if board[row][col] == 1)
        if comb not in res:
            res.append(list(comb))
        attacked.clear()
        return
    for x in range(x0, n):
        for y in range(y0 + 1 if x == x0 else 0, n):
            if (x, y) not in attacked:
                attacked1 = attacked.copy()
                board[x][y] = 1
                save_attacked_fields(n, x, y, attacked)  # TODO реализовать проверку
                searching(board, n, placed + 1, l, res, attacked, x, y)
                board[x][y] = 0
                attacked = attacked1.copy()


def save_attacked_fields(n, x, y, attacked):
    """"""
    if (x, y) in attacked:
        return
    attacked.add((x, y))
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for dx, dy in directions:
        x1 = x + dx
        y1 = y + dy
        if 0 <= x1 < n and 0 <= y1 < n:
            attacked.add((x1, y1))
    for dx, dy in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
        x1 = x + dx
        y1 = y + dy
        while 0 <= x1 < n and 0 <= y1 < n:
            attacked.add((x1, y1))
            x1 = x1 + dx
            y1 = y1 + dy


def steps(board, N, x, y):
    """отображение клеток, стоящих под боем"""
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for dx, dy in directions:
        x1 = x + dx
        y1 = y + dy
        if 0 <= x1 < N and 0 <= y1 < N:
            board[x1][y1] = "*"
    for dx, dy in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
        x1 = x + dx
        y1 = y + dy
        while 0 <= x1 < N and 0 <= y1 < N:
            board[x1][y1] = "*"
            x1 = x1 + dx
            y1 = y1 + dy


def showing(count, combinations, n):
    """отображение поставленных фигур"""
    for i, comb in enumerate(combinations, 0):
        if count == i:
            break
        print(f"Комбинация {i + 1}")
        desk = creation(n)
        for x, y in comb:
            desk[x][y] = "#"
            steps(desk, n, x, y)
        for x in desk:
            print(" ".join(x))


def creation(n):
    """создание доски"""
    desk = [["0"] * n for i in range(n)]
    return desk


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
    inp1 = lines[0].split()
    inp2 = lines[1:]
    N = int(inp1[0])
    L = int(inp1[1])
    K = int(inp1[2])
    board = [[0]*N for i in range(N)]
    attacked_fields = set()
    for a in inp2[:K]:
        a = a.split()
        x = int(a[0])
        y = int(a[1])
        board[x][y] = 1
        save_attacked_fields(N, x, y, attacked_fields)
    results = []
    start = time()
    searching(board, N, 0, L, results, attacked_fields)
    end = time()
    print(f"Кол-во вариантов: {len(results)}, параметры: {N, L, K}, время: {round(end - start, 2)}")
    with open("output.txt", "w") as file:
        for result in results:
            file.write(" ".join(f"{x, y}" for x, y in result))
            file.write("\n")
        if not results:
            file.write("No solution")
    if not results:
        print("No solution")
    try:
        s = int(input("количество досок с фигурами: "))
        showing(s, results, N)
    except:
        print("введены некорректные данные")
