"""Snake"""

import pygame

class Snake(pygame.sprite.Sprite):
    """Represents the snake on the board"""
    def __init__(self):
        """Init"""

        super().__init__()

        # Storing surfaces and rectangles
        self.surfaces = []
        self.rectangles = []

        # Crating the body pieces
        for current_id in range(0, 5):
            current_surface = pygame.Surface((10, 10))
            current_surface.fill(("#272b30"))
            self.surfaces.append(current_surface)
            self.rectangles.append(current_surface.get_rect(center = (10, current_id * 10)))

    def update(self):
        """Updates Snake position"""
        for current_rectangle in self.rectangles:
            current_rectangle.move_ip(0, 10)

    def get_head(self):
        """Returns the head of the snake"""
        return self.surfaces[0], self.rectangles[0]

    def get_body(self):
        """Returns the body of the snake"""
        return list(zip(self.surfaces[1:], self.rectangles[1:]))
