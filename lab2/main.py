import random
import math
from tkinter import *

color_path = "red"
color_default = "yellow"
color_text = "black"
text_font = "Verdana 14"
text_font_small = "Verdana 8"
header_width = 40
point_width = 3
line_width = 1


def select_edges(r, r_count):
    l = len(r)
    i = 0
    while (i < r_count) and (i < l):
        n = random.randint(1, l - i)
        j = 0
        num = 0
        while j < n:
            if r[num][3] == 0:
                j += 1
            num += 1
        r[num - 1][3] = 1
        i += 1


def generate_edges(v_count, r_count):
    r = []
    num = 0
    for i in range(v_count):
        for j in range(i):
            r.append([num, i, j, 0])
            num += 1
    select_edges(r, r_count)
    return r


def generate_graph(v_count, r_count):
    random.seed()
    graph = [[] for i in range(v_count)]
    r = generate_edges(v_count, r_count)
    for i in range(len(r)):
        if r[i][3] == 1:
            graph[r[i][1]].append(r[i][2])
            graph[r[i][2]].append(r[i][1])
    return graph


def graph_draw_euler_path(graph, size, path):
    window = Tk()
    window.title('Граф - цикл Эйлера')
    canvas = Canvas(window, width=size, height=size, bg="gray")
    R = (size - header_width) // 2 - 2 * point_width - 10
    x0 = size // 2
    y0 = size // 2 + header_width // 2
    n = len(graph)

    def get_v_x(i):
        return x0 + R * math.cos(2 * math.pi / n * i)

    def get_v_y(i):
        return y0 + R * math.sin(2 * math.pi / n * i)

    # рисуем ребра
    for i in range(n):
        v = graph[i]
        x = get_v_x(i)
        y = get_v_y(i)
        for j in range(len(v)):
            x1 = get_v_x(v[j])
            y1 = get_v_y(v[j])
            canvas.create_line(x, y, x1, y1, width=line_width, fill=color_default)
    # рисуем вершины - правильный n-угольник
    for i in range(n):
        x = get_v_x(i)
        y = get_v_y(i)
        canvas.create_oval([x - point_width, y - point_width], [x + point_width, y + point_width], fill=color_default)
        canvas.create_text(x, y, text=str(i), justify=CENTER, font=text_font, fill=color_text)
    # рисуем путь
    s = ''
    if len(path) > 0:
        for i in range(len(path)):
            s = s + ' ' + str(path[i])
    else:
        s = 'Цикл не найден'
    canvas.create_text(100, 30, text=s, justify=RIGHT, font=text_font_small, fill=color_text)
    canvas.pack()
    window.mainloop()


def graph_draw_hamiltonian_path(graph, size, path):
    window = Tk()
    window.title('Граф - цикл Гамильтона')
    canvas = Canvas(window, width=size, height=size, bg="gray")
    R = (size - header_width) // 2 - 2 * point_width - 10
    x0 = size // 2
    y0 = size // 2 + header_width // 2
    n = len(graph)

    def get_v_x(i):
        return x0 + R * math.cos(2 * math.pi / n * i)

    def get_v_y(i):
        return y0 + R * math.sin(2 * math.pi / n * i)

    # рисуем ребра
    for i in range(n):
        v = graph[i]
        x = get_v_x(i)
        y = get_v_y(i)
        for j in range(len(v)):
            x1 = get_v_x(v[j])
            y1 = get_v_y(v[j])
            canvas.create_line(x, y, x1, y1, width=line_width, fill=color_default)

    # рисуем вершины - правильный n-угольник
    for i in range(n):
        x = get_v_x(i)
        y = get_v_y(i)
        canvas.create_oval([x - point_width, y - point_width], [x + point_width, y + point_width], fill=color_default)
        canvas.create_text(x, y, text=str(i), justify=CENTER, font=text_font, fill=color_text)

    # рисуем путь
    s = ''
    if len(path):
        for i in range(len(path) - 1):
            x = get_v_x(path[i])
            y = get_v_y(path[i])
            x1 = get_v_x(path[i + 1])
            y1 = get_v_y(path[i + 1])
            canvas.create_line(x, y, x1, y1, width=line_width, fill=color_path);
            s = s + ' ' + str(path[i])
        s = s + ' ' + str(path[len(path) - 1])
    else:
        s = 'Цикл не найден'
    canvas.create_text(100, 30, text=s, justify=RIGHT, font=text_font_small, fill=color_text)
    canvas.pack()
    window.mainloop()


def vertex_clone(v):
    v_new = []
    for i in v:
        v_new.append(i)
    return v_new


def graph_clone(g):
    g_new = []
    for v in g:
        g_new.append(vertex_clone(v))
    return g_new


def vertex_del_edge(v, i):
    v.remove(i)


def graph_del_edge(g, i, j):
    vertex_del_edge(g[i], j)
    vertex_del_edge(g[j], i)


def graph_have_edges(g):
    for v in g:
        if len(v) > 0:
            return True
    return False


def find_euler_path_start(g):
    start_v = -1
    for i in range(len(g)):
        v = g[i]
        if len(v) % 2 == 1:
            return -1
        if start_v == -1 and len(v) > 0:
            start_v = i
    return start_v


def graph_find_euler_path(g_in):
    path = []
    g = graph_clone(g_in)
    if len(g) == 0:
        return path
    start_v = find_euler_path_start(g)
    if start_v < 0:
        return path
    stack = [start_v]
    while len(stack) > 0:
        i = stack[-1]
        v = g[i]
        if (len(v) == 0):
            stack.pop()
            path.append(i)
        else:
            j = v[0]
            stack.append(j)
            graph_del_edge(g, i, j)
    if graph_have_edges(g):
        return []
    else:
        return path


def is_edge(g, i, j):
    try:
        g[i].index(j)
        return True
    except ValueError:
        return False


def graph_find_hamiltonian_path_quick(g):
    n = len(g)
    if n == 0:
        return []
    path = [i for i in range(n)]
    for k in range(n * (n - 1)):
        if not is_edge(g, path[0], path[1]):
            i = 2
            if i + 1 > n - 1:
                return []
            while (not is_edge(g, path[0], path[i])) or (not is_edge(g, path[1], path[i + 1])):
                i += 1
                if i + 1 > n - 1:
                    return []
            path[1], path[i] = path[i], path[1]
        path.append(path[0])
        path.pop(0)
    path.append(path[0])
    return path


def graph_find_hamiltonian_path(g):
    n = len(g)
    if n == 0:
        return []
    visited = [False] * n
    path = []

    def hamilton(curr):
        path.append(curr)
        if len(path) == n:
            if is_edge(g, path[0], path[-1]):
                return True
            else:
                path.pop()
                return False
        visited[curr] = True
        for next in range(n):
            if is_edge(g, curr, next) and not visited[next]:
                if hamilton(next):
                    return True
        visited[curr] = False
        path.pop()
        return False

    path1 = graph_find_hamiltonian_path_quick(g)
    if len(path1) > 0:
        return path1

    if hamilton(0):
        path.append(path[0])
        return path
    else:
        return []


def check_graph(g):
    for i in range(len(g)):
        for j in g[i]:
            if not is_edge(g, j, i):
                return False
    return True


def graph_save_txt(file_path, g):
    with open(file_path, "wt") as f:
        for i in range(len(g)):
            if i > 0:
                f.write('\n')
            for j in range(len(g[i])):
                if j > 0:
                    f.write(' ')
                f.write(str(g[i][j]))


def graph_read_txt(file_path):
    g = []
    with open(file_path, "rt") as f:
        for line in f.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            v = []
            if len(line) > 0:
                sv = line.split(" ")
                v = [int(sv[i]) for i in range(len(sv))]
            g.append(v)
    if not check_graph(g):
        return []
    return g


if __name__ == '__main__':
    graph = generate_graph(5, 10)
    # graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
    # graph = [[1, 3], [0, 2, 3], [1, 3], [1, 2, 0]]
    #graph = graph_read_txt("1.txt")
    if len(graph) == 0:
        print('Граф пустой или некорректен')
    else:
        print('Граф')
        print(graph)

        path = graph_find_euler_path(graph)
        graph_draw_euler_path(graph, 900, path)
        print('Цикл Эйлера')
        print(path)

        path = graph_find_hamiltonian_path(graph)
        graph_draw_hamiltonian_path(graph, 900, path)
        print('Цикл Гамильтона')
        print(path)
        #graph_save_txt("1.txt", graph)
