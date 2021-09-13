"""Snake"""

# Setting pygame window position
import os
from typing import Tuple
import sys

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200, 200)

# Other imports
import random
import pygame
import numpy as np
from directions import AbsoluteDirections, get_absolute_direction
from settings import FOOD_REWARD, KILL_AFTER_STEPS, SCREEN_WIDTH, SCREEN_HEIGHT, MAXIMUM_STEP_REWARD, STEP_REWARD


class Snake(pygame.sprite.Sprite):
    """Represents the snake on the board"""

    def __init__(self):
        """Init"""

        super().__init__()

        # Storing surfaces and rectangles
        self.surfaces = []
        self.rectangles = []

        # Direction the snake faces at startup
        self.facing = AbsoluteDirections.DOWN

        starting_pos = int(SCREEN_WIDTH / 2)

        # Crating the body pieces
        for current_id in range(4, -1, -1):
            current_surface = pygame.Surface((10, 10))
            current_surface.fill("#272b30")
            self.surfaces.append(current_surface)
            self.rectangles.append(current_surface.get_rect(center=(starting_pos, current_id * 10)))

        # Initial food surface / rectangle
        self.food_surface = pygame.Surface((10, 10))
        self.food_surface.fill("#ed0f46")

        # Spawning food
        self.spawn_food()

        # Moves made since last time on food
        self.move_counter = 0


    def update(self, relative_direction) -> Tuple[int, bool]:
        """Updates Snake position"""

        score = 0
        self.move_counter += 1

        # If we are on food tile
        if self.rectangles[0].colliderect(self.food_rectangle):

            # TODO: We finished the game!

            self.spawn_food()
            self.surfaces.append(pygame.Surface((10, 10)))
            self.surfaces[-1].fill("#272b30")
            score += FOOD_REWARD
            self.move_counter = 0
        else:
            del self.rectangles[-1]
            if self.move_counter < MAXIMUM_STEP_REWARD:
                score += STEP_REWARD

        # Extending the snake
        self.rectangles.insert(0, self.rectangles[0].copy())

        # Getting the absolute direction of the move
        absolute_move = get_absolute_direction(self.facing, relative_direction)

        # Moving the snake
        if absolute_move == AbsoluteDirections.UP:
            self.rectangles[0].move_ip(0, -10)
            self.facing = AbsoluteDirections.UP
        if absolute_move == AbsoluteDirections.RIGHT:
            self.rectangles[0].move_ip(10, 0)
            self.facing = AbsoluteDirections.RIGHT
        if absolute_move == AbsoluteDirections.DOWN:
            self.rectangles[0].move_ip(0, 10)
            self.facing = AbsoluteDirections.DOWN
        if absolute_move == AbsoluteDirections.LEFT:
            self.rectangles[0].move_ip(-10, 0)
            self.facing = AbsoluteDirections.LEFT

        # Checks if the snake is alive
        is_alive = True        
        if self.rectangles[0] in self.rectangles[1:]: is_alive = False
        if any([i < 0 for i in self.rectangles[0][:2]]): is_alive = False
        if self.rectangles[0][0] > SCREEN_WIDTH - 10: is_alive = False
        if self.rectangles[0][1] > SCREEN_HEIGHT - 10: is_alive = False
    
        if self.move_counter > KILL_AFTER_STEPS: is_alive = False

        return score, is_alive

    def get_head(self):
        """Returns the head of the snake"""
        return self.surfaces[0], self.rectangles[0]

    def get_body(self):
        """Returns the body of the snake"""
        return list(zip(self.surfaces[1:], self.rectangles[1:]))

    def spawn_food(self):
        """Creates food in a random location"""
        while True:

            lower_x = 0
            upper_x = int((SCREEN_WIDTH - 20) / 10)

            lower_y = 0
            upper_y = int((SCREEN_HEIGHT - 20) / 10)

            food_x = random.randint(lower_x, upper_x)
            food_y = random.randint(lower_y, upper_y)

            food_x_trans = food_x * 10 + 5
            food_y_trans = food_y * 10 + 5

            self.food_pos = (food_x_trans, food_y_trans)
            # print(f"Spawned new food at: {self.food_pos=}")
            if self.food_pos not in list(self.get_head()) + self.get_body():
                break

        food_x_rect = self.food_pos[0] + 5
        food_y_rect = self.food_pos[1] + 5

        self.food_rectangle = self.food_surface.get_rect(center=((food_x_rect, food_y_rect)))
        self.move_counter = 0

    def get_food(self):
        """Returns the food"""
        return self.food_surface, self.food_rectangle

    def to_network_input(self):
        squares = [(rect[0], rect[1]) for rect in self.rectangles]
        field = []
        for col in range(5, SCREEN_HEIGHT - 10, 10):
            curr = []
            for row in range(5, SCREEN_WIDTH - 10, 10):
                if (row, col) == self.food_pos:
                    curr += [1.0]
                else:
                    if (row, col) == squares[0]:
                        curr += [0.5]
                    else:
                        curr += [0.25] if (row, col) in squares else [0.0]

            field.append(curr)

        return np.array([j for sub in field for j in sub], dtype=np.float32)


