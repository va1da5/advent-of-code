import math
import string


def get_matrix(area: str):
    return list(map(lambda line: list(line), area.split("\n")))


def render_matrix(matrix):
    return "\n".join(["".join(line) for line in matrix])


def get_antennas_in_range(matrix, x, y):
    antennas = []
    for angle in range(0, 360, 1):
        for i in range(1, len(matrix) * 2):
            lx = round(x + (i * math.sin(math.radians(angle))))
            ly = round(y - (i * math.cos(math.radians(angle))))

            if lx > -1 and lx < len(matrix[0]) and ly > -1 and ly < len(matrix):
                if matrix[y][x] == matrix[ly][lx]:
                    if (lx, ly) not in antennas:
                        antennas.append((lx, ly))
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
                antennas.append((matrix[y][x], x, y))
    return antennas


def is_valid_point(matrix, x: int, y: int):
    if y > -1 and y < len(matrix):
        if x > -1 and x < len(matrix[y]):
            return True
    return False


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


def main():
    matrix = get_matrix(area)

    antinodes = []

    for _, x, y in get_antennas(matrix):
        for other_antenna in get_antennas_in_range(matrix, x, y):
            px, py = get_placement((x, y), other_antenna)
            if is_valid_point(matrix, px, py):
                antinodes.append((px, py))

    print(f"Count: {len(set(antinodes))}")
    # Correct: 371

    for x, y in set(antinodes):
        matrix[x][y] = "#"

    print(render_matrix(matrix))


if __name__ == "__main__":
    main()
