import pygame
import random
import numpy as np
import time             # Import time module for performance measurement

import csv

from pygame.math import Vector2

class Apple:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset()

    def reset(self):
        self.position = Vector2(random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))

    def show(self, screen):
        rect = pygame.Rect(self.position.x * 30, self.position.y * 30, 30, 30)
        pygame.draw.rect(screen, (255, 0, 0), rect)



class Snake:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.q_table = np.zeros((grid_width, grid_height, 4))  # Simplified Q-table
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01
        self.reset()

    def reset(self):
        center = Vector2(self.grid_width // 2, self.grid_height // 2)
        self.body = [center, center - Vector2(0, 1), center - Vector2(0, 2)]
        self.direction = Vector2(0, 1)  # Start moving downwards

    def update(self, apple):
        start_time = time.time()  # Start timing for this iteration

        current_state = (int(self.body[0].x), int(self.body[0].y))
        valid_actions = self.get_valid_actions()

        if not valid_actions:  # Check if there are no valid actions
            print("No valid moves available. Resetting snake.")
            self.reset()  # Reset the game or handle game over scenario
            return time.time() - start_time

        if random.random() < self.epsilon:
            action = random.choice(valid_actions)
        else:
            action = max(valid_actions, key=lambda x: self.q_table[current_state + (x,)])

        move = Vector2(0, 1) if action == 0 else Vector2(0, -1) if action == 1 else Vector2(1, 0) if action == 2 else Vector2(-1, 0)
        new_head = self.body[0] + move
    
        reward = 100 if new_head == apple.position else -1
        new_state = (int(new_head.x), int(new_head.y))
    
        self.body.insert(0, new_head)
        if new_head == apple.position:
            apple.reset()
        else:
            self.body.pop()

        self.update_q_table(current_state, action, reward, new_state)
    
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
    
        # Calculate and return the time taken for this iteration
        return time.time() - start_time

    


    def get_valid_actions(self):
        actions = []
        head = self.body[0]
        if head.y + 1 < self.grid_height and Vector2(head.x, head.y + 1) not in self.body:
            actions.append(0)  # Down
        if head.y - 1 >= 0 and Vector2(head.x, head.y - 1) not in self.body:
            actions.append(1)  # Up
        if head.x + 1 < self.grid_width and Vector2(head.x + 1, head.y) not in self.body:
            actions.append(2)  # Right
        if head.x - 1 >= 0 and Vector2(head.x - 1, head.y) not in self.body:
            actions.append(3)  # Left
        return actions

    def update_q_table(self, state, action, reward, new_state):
        old_value = self.q_table[state + (action,)]
        future_rewards = np.max(self.q_table[new_state])
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * future_rewards - old_value)
        self.q_table[state + (action,)] = new_value

    def show(self, screen):
        for block in self.body:
            rect = pygame.Rect(block.x * 30, block.y * 30, 30, 30)
            pygame.draw.rect(screen, (0, 255, 0), rect)

def main():
    pygame.init()
    grid_width, grid_height = 40, 20
    screen = pygame.display.set_mode((1200, 600))
    snake = Snake(grid_width, grid_height)
    apple = Apple(grid_width, grid_height)
    clock = pygame.time.Clock()

    computation_times = []  # To store computation times for each frame
    apples_collected = []  # To store the count of apples collected over time

    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((51, 51, 51))
        computation_start = time.time()  # Start time for computation
        snake.update(apple)  # Update the snake and apple positions
        computation_times.append(time.time() - computation_start)  # Compute and store the time taken for the update

        snake.show(screen)
        apple.show(screen)
        pygame.display.flip()
        clock.tick(100)  # High tick rate for faster simulation

        apples_collected.append(len(snake.body) - 3)  # Store the current count of apples collected

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed Time:", elapsed_time, "seconds")

    # Save the collected data to a CSV file
    with open('QLearning_Performance_Data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Computation_Time', 'Apples_Collected'])
        writer.writeheader()
        for comp_time, apples in zip(computation_times, apples_collected):
            writer.writerow({'Computation_Time': comp_time, 'Apples_Collected': apples})

    pygame.quit()

if __name__ == '__main__':
    main()
