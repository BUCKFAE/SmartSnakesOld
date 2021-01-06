"""Snake"""
import random
import pygame

class Snake(pygame.sprite.Sprite):
    """Represents the snake on the board"""
    def __init__(self):
        """Init"""

        super().__init__()

        # Storing surfaces and rectangles
        self.surfaces = []
        self.rectangles = []

        # 0 -> UP, 1 -> RIGHT, 2 -> DOWN, 3 -> LEFT
        self.facing = 2

        # Crating the body pieces
        for current_id in range(0, 5):
            current_surface = pygame.Surface((10, 10))
            current_surface.fill(("#272b30"))
            self.surfaces.append(current_surface)
            self.rectangles.append(current_surface.get_rect(center = (10, current_id * 10)))

    def update(self):
        """Updates Snake position"""
        del self.rectangles[0]
        self.rectangles.insert(len(self.rectangles) - 1, self.rectangles[-1].copy())

        if random.getrandbits(1):
            self.rectangles[-1].move_ip(10, 0)
        else:
            self.rectangles[-1].move_ip(0, 10)

    def get_head(self):
        """Returns the head of the snake"""
        return self.surfaces[0], self.rectangles[0]

    def get_body(self):
        """Returns the body of the snake"""
        return list(zip(self.surfaces[1:], self.rectangles[1:]))
