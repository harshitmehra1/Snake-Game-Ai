import pygame
import random
from pygame.math import Vector2
from collections import deque


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
        self.position = position  # Position as Vector2
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def bfs_search(grid, start, goal):
    queue = deque([start])
    came_from = {(start.position.x, start.position.y): None}  # Use tuple for position

    while queue:
        current_node = queue.popleft()

        if current_node.position == goal.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = came_from[(current_node.position.x, current_node.position.y)]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = Vector2(current_node.position.x + dx, current_node.position.y + dy)
            if 0 <= neighbor_pos.x < 40 and 0 <= neighbor_pos.y < 20:
                neighbor = Node(neighbor_pos, current_node)
                neighbor_tuple = (neighbor_pos.x, neighbor_pos.y)
                if neighbor_tuple not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor_tuple] = current_node

    return None

class Snake:
    def __init__(self):
        self.body = [Vector2(i, 0) for i in range(3)]
        self.direction = Vector2(1, 0)
        self.path = []

    def update(self, apple, grid):
        for y in range(20):
            for x in range(40):
                grid[y][x] = 0
        for block in self.body:
            grid[int(block.y)][int(block.x)] = -1

        if not self.path or self.get_head_position() == self.path[-1]:
            start = Node(self.get_head_position())
            goal = Node(apple.position)
            self.path = bfs_search(grid, start, goal)
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
            pygame.draw.rect(screen, (0, 255, 0), rect)  # Snake color changed to green



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
            if event.type == pygame.QUIT:
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
    print("BFS Algorithm:")
    print("Elapsed Time:", elapsed_time, "seconds")

    # Calculate path length
    path_length = len(snake.body)  # Length of snake body represents path length
    print("Path Length:", path_length)

    pygame.quit()

if __name__ == '__main__':
    main()