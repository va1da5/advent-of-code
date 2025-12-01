from queue import PriorityQueue
from colorama import Back, Fore
from colorama.ansi import clear_screen
import time
from collections import defaultdict
import math


EMPTY = "."
BARRIER = "#"
START = "S"
END = "E"
TURN_PENALTY = 1000

DIRECTIONS = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}


class Node:
    position = None  # (x, y)
    original_value = None
    value = None  # character
    neighbors = None  # [(Node(), >),..]
    direction = None  # ^, >, v, <
    touched = False
    is_visited = False
    is_highlighted = False
    is_in_path = False

    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.original_value = value
        self.neighbors = []

    def get_value(self):
        if self.is_highlighted:
            return Back.CYAN + self.value + Back.RESET

        if self.is_in_path:
            return Back.YELLOW + self.value + Back.RESET

        if self.is_visited:
            return Fore.RED + self.value + Fore.RESET

        return self.value

    def get_position(self):
        return self.position

    def is_barrier(self):
        return self.value == BARRIER

    def is_start(self):
        return self.value == START

    def is_end(self):
        return self.value == END

    def set_in_path(self):
        self.is_in_path = True

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
    return "\n".join(["".join([node.get_value() for node in row]) for row in grid])


def grid_update_neighbors(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def manhattan_distance(current, finish):
    cx, cy = current
    fx, fy = finish
    return abs(cx - fx) + abs(cy - fy)


def euclidean_distance(current, finish):
    cx, cy = current
    fx, fy = finish
    return math.sqrt(pow(cx - fx, 2) + pow(cy - fy, 2))


def no_distance(a, b):
    return 0


def reconstruct_path(came_from, current):
    current.set_in_path()
    while current in came_from:
        current = came_from[current]
        current.set_in_path()


def get_shortest_path(came_from, current):
    path = [current.get_position()]
    while current in came_from:
        current = came_from[current]
        if current == None:
            return path
        current.set_in_path()
        path.append(current.get_position())
    return path


def inf():
    return float("inf")


def a_star(start_node, end_node, draw):
    queue = PriorityQueue()
    queue.put((0, start_node, start_node.direction))
    came_from = {}

    h = euclidean_distance

    visited = defaultdict(bool)
    g_score = defaultdict(inf)
    g_score[start_node] = 0
    f_score = defaultdict(inf)
    f_score[start_node] = h(start_node.get_position(), end_node.get_position())

    while not queue.empty():
        current_score, current_node, current_direction = queue.get()  # [1:]
        visited[current_node] = True

        draw(current_node, came_from)

        # if current_node == end_node:
        #     reconstruct_path(came_from, end_node)
        #     return get_shortest_path(came_from, end_node)

        if f_score[current_node] < current_score:
            continue

        for neighbor, neighbor_direction in current_node.neighbors:
            if visited[neighbor]:
                continue

            score = 1
            if current_direction != neighbor_direction:
                score += TURN_PENALTY

            temp_g_score = g_score[current_node] + score
            temp_f_score = temp_g_score + h(
                neighbor.get_position(), end_node.get_position()
            )

            if f_score[neighbor] < temp_f_score:
                continue

            came_from[neighbor] = current_node
            g_score[neighbor] = temp_g_score
            f_score[neighbor] = temp_f_score
            queue.put((f_score[neighbor], neighbor, neighbor_direction))

    # print(f"{g_score[end_node]=}")
    return came_from, g_score
    return get_shortest_path(came_from, end_node)


def dijkstra(grid, start_node, end_node, draw):
    # raise NotImplementedError()
    previous = {node: None for row in grid for node in row}
    visited = {node: False for row in grid for node in row}
    distances = {node: float("inf") for row in grid for node in row}
    distances[start_node] = 0

    queue = PriorityQueue()
    queue.put((0, start_node, start_node.direction))

    while not queue.empty():
        current_distance, current_node, current_direction = queue.get()
        visited[current_node] = True

        draw(current_node)

        for neighbor, neighbor_direction in current_node.neighbors:
            if visited[neighbor]:
                continue

            weight = 1
            if current_direction != neighbor_direction:
                weight = 1001

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                queue.put((new_distance, neighbor, neighbor_direction))

    return get_shortest_path(previous, end_node)


def get_score(start_node, end_node, path):
    seen = {start_node.get_position()}
    current_node = start_node
    direction = current_node.direction
    score = 0

    while current_node != end_node:
        # print(f"{current_node} {score=}")
        for neighbor, neighbor_direction in current_node.neighbors:
            if neighbor.get_position() not in path or neighbor.get_position() in seen:
                continue

            if direction == neighbor_direction:
                score += 1
                current_node = neighbor
                seen.add(neighbor.get_position())
                # print("🟡 + 1")
                break

            score += 1001
            current_node = neighbor
            direction = neighbor_direction
            seen.add(neighbor.get_position())
        # else:
        # print("🟢 + 1001")

    return score


def get_position(matrix, element):
    for y in range(len(matrix)):
        try:
            x = matrix[y].index(element)
            return (x, y)
        except ValueError:
            continue


with open("test4.txt", "r") as f:
    area = f.read().strip()

matrix = get_matrix(area)

# print(render_matrix(matrix))
# print()

grid = make_grid(matrix)

sx, sy = get_position(matrix, START)
ex, ey = get_position(matrix, END)

start_node = grid[sy][sx]
end_node = grid[ey][ex]

start_node.direction = ">"

grid_update_neighbors(grid)

# shortest_path = astar(grid, start_node, end_node)

# score = get_score(start_node, end_node, shortest_path)

# print(f"{score=}")
# print(draw_grid(grid))


def draw(node, trail):
    def reset(node):
        node.is_highlighted = False
        node.is_in_path = False

    [reset(node) for row in grid for node in row]
    reconstruct_path(trail, node)
    print(clear_screen())
    node.is_highlighted = True
    print(draw_grid(grid))
    node.is_visited = True
    time.sleep(0.05)


# shortest_path = dijkstra(grid, start_node, end_node, lambda node: draw(node))

trail, distance = a_star(start_node, end_node, lambda node, trail: draw(node, trail))
# trail, distance = a_star(start_node, end_node, lambda node, trail: 0)

# shortest_path = get_shortest_path(trail, end_node)
# score = get_score(start_node, end_node, shortest_path)

# print(trail)

draw(end_node, trail)

# print(clear_screen())
print(f"{distance[end_node]=}")
# print(f"{score=}")
# print(draw_grid(grid))
