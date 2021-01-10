"""Snake"""
import random
import pygame
from directions import AbsoluteDirections, get_absolute_direction
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, RANOM_SEED

class Snake(pygame.sprite.Sprite):
    """Represents the snake on the board"""
    def __init__(self):
        """Init"""

        super().__init__()

        # Storing surfaces and rectangles
        self.surfaces = []
        self.rectangles = []

        # Stores food positons
        self.food_positions = []

        random.seed(RANOM_SEED)

        # Creating the food
        for _ in range(0, 100):
            randx = round(random.randint(0, SCREEN_WIDTH), -1)
            randy = round(random.randint(0, SCREEN_HEIGHT), -1)
            self.food_positions.append((randx, randy))

        # Id of the current food
        self.current_food = 0

        self.create_food_at(self.food_positions[0])

        # 0 -> UP, 1 -> RIGHT, 2 -> DOWN, 3 -> LEFT
        self.facing = AbsoluteDirections.DOWN

        # Crating the body pieces
        for current_id in range(10, -1, -1):
            current_surface = pygame.Surface((10, 10))
            current_surface.fill(("#272b30"))
            self.surfaces.append(current_surface)
            self.rectangles.append(current_surface.get_rect(center = (10, current_id * 10)))

    def update(self, relative_direction):
        """Updates Snake position"""

        score = 0

        # If we are on food tile
        if self.rectangles[0].colliderect(self.food_rectangle):
            self.current_food += 1
            self.create_food_at(self.food_positions[self.current_food])
            self.surfaces.append(pygame.Surface((10, 10)))
            self.surfaces[-1].fill("#272b30")
            score += 500
        else:
            del self.rectangles[-1]
            score += 1

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

        return score

    def get_head(self):
        """Returns the head of the snake"""
        return self.surfaces[0], self.rectangles[0]

    def get_body(self):
        """Returns the body of the snake"""
        return list(zip(self.surfaces[1:], self.rectangles[1:]))

    def get_food(self):
        """Returns the food"""
        return self.food_surface, self.food_rectangle

    def create_food_at(self, food_position):
        """Sets the food to be at the given coordinates"""
        self.food_surface = pygame.Surface((10, 10))
        self.food_surface.fill("#ed0f46")
        foodx = food_position[0]
        foody = food_position[1]
        self.food_rectangle = self.food_surface.get_rect(center = (foodx, foody))
