labyrint = [[1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1 - Стена(препятствие), 0 - свободная ячейка(куда можем переместиться)
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]]


def searсh_path(data, x, y, short_path={}, full_path={},
                count=0):  # data-лабиринт; х,у - точка, где мы сейчас находимся
    # short_path - {key=точка куда идём: value=откуда идём}
    # full_path - {key=точка : value=кол-во шагов до точки}
    # count - номер шага
    full_path[(x, y)] = count  # Записываем точку и сколько шагов до неё на данном этапе
    if x == 3 and y == 7:  # Точка выхода из лабиринта
        return full_path, short_path
    walks = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up,left, down, right,
    for walk_X, walk_Y in walks:
        if data[x + walk_X][y + walk_Y] == 0 and (0 < x + walk_X < 9 and 0 < y + walk_Y < 9):  # Если ячейка свободна
            # и мы не вышли за границы лабиринта
            check = full_path.get((x + walk_X, y + walk_Y))  # Смотрим на точку, куда хотим пойти и сколько до неё шагов
            # Если check=None, значит в точке ещё не были
            if check != None and check > count:  # Если мы были уже в этой точке и расстояние до неё больше, чем номер шага
                # на данном этапе
                full_path[
                    (x + walk_X, y + walk_Y)] = count  # Перезаписываем full_path, т.к нашли более короткую дистанцию
                short_path[(x + walk_X, y + walk_Y)] = (x, y)  # Пепрезаписываем short_path, потому что нашли точку, из
                # которой в данную можно попасть короче
                searсh_path(data, x + walk_X, y + walk_Y, short_path, full_path,
                            count + 1)  # Увеличиваем шаг и запускаем
                # рекурсивно функцию
            else:
                if (x + walk_X, y + walk_Y) not in full_path.keys():  # Если в токе, куда собираемся пойти еще не были
                    short_path[(x + walk_X, y + walk_Y)] = (x, y)  # записываем {куда идём:откуда идём}
                    searсh_path(data, x + walk_X, y + walk_Y, short_path, full_path, count + 1)  # запускаем рекурсию
                    # с шагом +1
    return full_path, short_path


def short_path(data, path=[], start=(3, 1), end=(3, 7)):  # Сюда прилетает short_path из search_path, когда нашли выход
    # data=short_path, start - координата точки входа, end - выхода
    # path - короткий путь в виде списка координат из лабиринта
    """Здесь мы рекурсивно пробегаемся из конечной точки в начальную, восстанавливая путь по лабиринту:
    берём {точка, куда пришли(допустим А) : точка откуда пришли (в точку А) - Б}"""
    if len(path) == 0:
        path.append(end)
    path.append(data[end])
    if data[end] == start:
        return path
    else:
        short_path(data, path, start, data[end])
    return path


p = searсh_path(labyrint, 3, 1)
if p is None:
    print('No Exit!!!')
else:
    short = short_path(p[1])
    short.reverse()
    for walk in short:
        labyrint[walk[0]][walk[1]] = 3  # Здесь мы просто указываем в графе путь к выходу цифрой 3
    for see in labyrint:
        print(see)