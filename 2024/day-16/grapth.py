def get_grid(area: str):
    return list(map(lambda line: list(line), area.split("\n")))


def render_grid(grid):
    return "\n".join(["".join(line) for line in grid])


def make_graph(grid):
    width, height = len(grid[0]), len(grid)


with open("test4.txt", "r") as f:
    area = f.read().strip()
