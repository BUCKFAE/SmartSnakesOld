"""Main"""

import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_LEFT, K_RIGHT

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from snake import Snake
from directions import RelativeDirections

def main():
    """Entry point of the program"""

    # Initializing pygame
    pygame.init()
    pygame.display.set_caption('Smart Snakes - Buckfae')

    # Setting up the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Clock
    clock = pygame.time.Clock()

    # Creating the snake
    snake = Snake()

    # Variable that controls the main loop
    running = True

    # Main loop
    while running:

        # Default move
        next_move = RelativeDirections.AHEAD

        # Event queue
        for event in pygame.event.get():

            # Key was pressed
            if event.type == KEYDOWN:

                # Escape key was pressed
                if event.key == K_ESCAPE:
                    running = False

                # Movement
                if event.key == K_UP:
                    next_move = RelativeDirections.AHEAD
                if event.key == K_LEFT:
                    next_move = RelativeDirections.LEFT
                if event.key == K_RIGHT:
                    next_move = RelativeDirections.RIGHT

            # Quit
            if event.type == QUIT:
                running = False

        # Updating the snake position
        snake.update(next_move)

        # Setting backround color
        screen.fill(("#16a085"))

        # Getting the different parts of the snake
        snake_head = snake.get_head()
        snake_body = snake.get_body()

        # Drawing the snake
        screen.blit(snake_head[0], snake_head[1])
        for snake_body_piece in snake_body:
            screen.blit(snake_body_piece[0], snake_body_piece[1])

        # Pushing changes to screen
        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
