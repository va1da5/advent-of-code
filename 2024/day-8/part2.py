import math
import string
import time


def get_matrix(area: str):
    return list(map(lambda line: list(line), area.split("\n")))


def render_matrix(matrix):
    return "\n".join(["".join(line) for line in matrix])


def clear_screen():
    print("\033[H\033[2J")


def get_antennas_of_same_frequency(matrix, x, y):
    current = matrix[y][x]
    antennas = []
    for my in range(len(matrix)):
        for mx in range(len(matrix[y])):
            if (x != mx or y != my) and matrix[my][mx] == current:
                antennas.append((mx, my))
    return antennas


def get_distance(a: tuple, b: tuple):
    ax, ay = a
    bx, by = b

    x = abs(ax - bx)
    y = abs(ay - by)

    return math.sqrt(pow(x, 2) + pow(y, 2))


def get_placement(a: tuple, b: tuple):
    ax, ay = a
    bx, by = b

    x = ax - bx
    y = ay - by
    # print(f"{x=} {y=}")
    c = get_distance(a, b)

    nx = (2 * abs(x) * c) / c
    ny = (2 * abs(y) * c) / c

    px = int(ax + nx)
    py = int(ay + ny)

    if x > 0:
        px = int(ax - nx)

    if y > 0:
        py = int(ay - ny)

    return (px, py)


def get_antennas(matrix):
    antennas = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] not in string.punctuation:
                antennas.append((x, y))
    return antennas


def is_valid_point(matrix, x: int, y: int):
    if y > -1 and y < len(matrix):
        if x > -1 and x < len(matrix[y]):
            return True
    return False


def visualize(area, src_antenna, dst_antenna, antinodes):
    sx, sy = src_antenna
    dx, dy = dst_antenna
    matrix = get_matrix(area)
    s_original = matrix[sy][sx]
    d_original = matrix[dy][dx]

    for x, y in set(antinodes):
        matrix[y][x] = "\033[44m" + matrix[y][x] + "\033[0m"
    matrix[sy][sx] = "\033[41m" + s_original + "\033[0m"
    matrix[dy][dx] = "\033[45m" + d_original + "\033[0m"
    print(render_matrix(matrix))


def get_antennas_of_same_frequency(matrix, x, y):
    current = matrix[y][x]
    antennas = []
    for my in range(len(matrix)):
        for mx in range(len(matrix[y])):
            if (x != mx or y != my) and matrix[my][mx] == current:
                antennas.append((mx, my))
    return antennas


def get_resonant_locations(matrix: list, source_antenna: tuple, remote_antenna: tuple):
    nodes = [source_antenna, remote_antenna]
    # nodes = [source_antenna, remote_antenna]
    source_node = tuple([*source_antenna])
    next_node = tuple([*remote_antenna])
    while True:
        px, py = get_placement(source_node, next_node)

        if is_valid_point(matrix, px, py):
            nodes.append((px, py))
            # nodes.extend([source_node, next_node])
            # nodes.extend([source_antenna, remote_antenna])
            source_node = tuple([*next_node])
            next_node = (px, py)
            continue
        break
    return list(set(nodes))


def get_resonant_antinodes(area: str):
    matrix = get_matrix(area)
    antinodes = []

    for x, y in get_antennas(matrix):
        for remote_antenna in get_antennas_of_same_frequency(matrix, x, y):
            nodes = get_resonant_locations(matrix, (x, y), remote_antenna)
            antinodes.extend(nodes)
    return tuple(set(antinodes))


def get_resonant_antinodes_visual(area: str):
    matrix = get_matrix(area)
    antinodes = []

    for x, y in get_antennas(matrix):
        for remote_antenna in get_antennas_of_same_frequency(matrix, x, y):
            nodes = get_resonant_locations(matrix, (x, y), remote_antenna)
            antinodes.extend(nodes)

            print(f"Count: {len(nodes)}")
            visualize(area, (x, y), remote_antenna, nodes)
            time.sleep(0.5)
            # input()
            clear_screen()

    return tuple(set(antinodes))


def main():
    # area = """
    # ........................
    # .......#................
    # ........................
    # .........O...#..........
    # ............O...........
    # ...........O............
    # ........................
    # ..........O.O...........
    # ........................
    # .........#...#..........
    # ........................
    # ........................
    # """.strip()

    with open("input.txt", "r") as f:
        area = f.read().strip()

    get_resonant_antinodes_visual(area)


if __name__ == "__main__":
    main()
