from queue import PriorityQueue

EMPTY = "."
BARRIER = "#"
START = "S"
END = "E"
TURN_PENALTY = 1000


class Node:
    position = None  # (x, y)
    original_value = None
    value = None  # character
    neighbors = None  # [(Node(), >),..]
    direction = None  # ^, >, v, <
    touched = False

    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.original_value = value
        self.neighbors = []

    def get_position(self):
        return self.position

    def is_barrier(self):
        return self.value == BARRIER

    def is_start(self):
        return self.value == START

    def is_end(self):
        return self.value == END

    def update_neighbors(self, grid):
        self.neighbors = []

        x, y = self.position
        max_y = len(grid)
        max_x = len(grid[0])

        if y < max_y - 1 and not grid[y + 1][x].is_barrier():
            self.neighbors.append((grid[y + 1][x], "v"))

        if y > 0 and not grid[y - 1][x].is_barrier():
            self.neighbors.append((grid[y - 1][x], "^"))

        if x < max_x - 1 and not grid[y][x + 1].is_barrier():
            self.neighbors.append((grid[y][x + 1], ">"))

        if x > 0 and not grid[y][x - 1].is_barrier():
            self.neighbors.append((grid[y][x - 1], "<"))

    def __str__(self):
        return f"{self.position} {self.value}"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return False


def get_matrix(area: str):
    return list(map(lambda line: list(line), area.split("\n")))


def render_matrix(matrix):
    return "\n".join(["".join(line) for line in matrix])


def make_grid(matrix):
    grid = []
    for y in range(len(matrix)):
        grid.append([])
        for x in range(len(matrix[y])):
            value = matrix[y][x]
            spot = Node((x, y), value)
            grid[y].append(spot)
    return grid


def draw_grid(grid):
    return "\n".join(["".join([node.value for node in row]) for row in grid])


def grid_update_neighbors(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def dijkstra(grid, start_node, end_node):
    previous = {node: None for row in grid for node in row}
    visited = {node: False for row in grid for node in row}
    distances = {node: float("inf") for row in grid for node in row}
    distances[start_node] = 0

    queue = PriorityQueue()
    queue.put((0, start_node, start_node.direction))

    while not queue.empty():
        current_distance, current_node, current_direction = queue.get()
        visited[current_node] = True

        for neighbor, neighbor_direction in current_node.neighbors:
            if visited[neighbor]:
                continue

            weight = 1
            if current_direction != neighbor_direction:
                weight = 1 + TURN_PENALTY

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                queue.put((new_distance, neighbor, neighbor_direction))

    return distances[end_node]


def get_position(matrix, element):
    for y in range(len(matrix)):
        try:
            x = matrix[y].index(element)
            return (x, y)
        except ValueError:
            continue


with open("input.txt", "r") as f:
    area = f.read().strip()

matrix = get_matrix(area)


grid = make_grid(matrix)

sx, sy = get_position(matrix, START)
ex, ey = get_position(matrix, END)

start_node = grid[sy][sx]
end_node = grid[ey][ex]

start_node.direction = ">"

grid_update_neighbors(grid)

distance = dijkstra(grid, start_node, end_node)

print(f"{distance=}")
