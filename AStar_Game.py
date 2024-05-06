import pygame
import random

from pygame.math import Vector2
import heapq


import time

class Apple:

    def __init__(self):
        self.boxes = [Vector2(i, j) for i in range(40) for j in range(20)]
        self.generate([Vector2(0, 0), Vector2(1, 0), Vector2(2, 0)])


    def generate(self, snake_body):
        empty_boxes = [box for box in self.boxes if box not in snake_body]
        if not empty_boxes:
            return False
        self.position = random.choice(empty_boxes)
        return True


    def show(self, screen):
        rect = pygame.Rect(self.position.x * 30, self.position.y * 30, 30, 30)
        pygame.draw.rect(screen, (255, 0, 0), rect)


class Node:

    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return (self.position.x, self.position.y) == (other.position.x, other.position.y)

    def __hash__(self):
        return hash((self.position.x, self.position.y))


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar_search(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, start)
    closed_set = set()


    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add((current_node.position.x, current_node.position.y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = Vector2(current_node.position.x + dx, current_node.position.y + dy)
            if 0 <= neighbor_pos.x < 40 and 0 <= neighbor_pos.y < 20:
                if (neighbor_pos.x, neighbor_pos.y) not in closed_set and grid[int(neighbor_pos.y)][int(neighbor_pos.x)] == 0:
                    neighbor = Node(neighbor_pos, current_node)
                    neighbor.g = current_node.g + 1
                    neighbor.h = heuristic(neighbor.position, goal.position)
                    neighbor.f = neighbor.g + neighbor.h
                    if not any(n.position == neighbor.position and n.g <= neighbor.g for n in open_set):
                        heapq.heappush(open_set, neighbor)

    return None


class Snake:

    def __init__(self):
        self.body = [Vector2(i, 0) for i in range(3)]
        self.direction = Vector2(1, 0)
        self.path = []

    def update(self, apple, grid):
        # Update grid to reflect current snake positions as obstacles
        for y in range(20):
            for x in range(40):
                grid[y][x] = 0
        for block in self.body:
            grid[int(block.y)][int(block.x)] = -1

        if not self.path or self.get_head_position() == self.path[-1]:
            start = Node(self.get_head_position())
            goal = Node(apple.position)
            self.path = astar_search(grid, start, goal)
            if not self.path:
                print("No path found!")
                return False


        next_position = self.path.pop(0)
        self.body.append(next_position)
        if next_position == apple.position:
            apple.generate(self.body)
        else:
            self.body.pop(0)
        return True


    def get_head_position(self):
        return self.body[-1]

    def show(self, screen):
        for block in self.body:
            rect = pygame.Rect(block.x * 30, block.y * 30, 30, 30)
            pygame.draw.rect(screen, (0, 164, 239), rect)




def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    grid = [[0 for _ in range(40)] for _ in range(20)]
    for block in snake.body:
        grid[int(block.y)][int(block.x)] = -1

    # Timing measurement
    start_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        screen.fill((51, 51, 51))
        if not snake.update(apple, grid):
            running = False
        snake.show(screen)
        apple.show(screen)
        pygame.display.flip()
        clock.tick(5)

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("A* Algorithm:")
    print("Elapsed Time:", elapsed_time, "seconds")

    # Calculate path length
    path_length = len(snake.body)  # Length of snake body represents path length
    print("Path Length:", path_length)

    pygame.quit()

if __name__ == '__main__':
    main()