"""Main"""

import random
import pygame
from pygame.constants import K_SPACE
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_d

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

    # Variable that controls the main loop
    running = True

    # Framerate
    current_speed = 3

    # ID of the current generation
    current_generation = 0

    snake = Snake()


    # Main loop
    while True:

        make_step = False

        # Exit condition
        if not running:
            break

        # Event queue
        for event in pygame.event.get():

            # Key was pressed
            if event.type == KEYDOWN:
                # Stopping simulation
                if event.key == K_ESCAPE:
                    running = False
                # Changing speed
                if event.key == K_UP:
                    current_speed = 30
                    print("Speed reset to 30 FPS!")
                if event.key == K_LEFT:
                    current_speed /= 2
                    print("Speed is now {} FPS".format(current_speed))
                if event.key == K_RIGHT:
                    current_speed *= 2
                    print("Speed is now {} FPS".format(current_speed))
                if event.key == K_SPACE:
                    make_step = True

            # Quit
            if event.type == QUIT:
                running = False

        if not make_step: continue

        next_move = random.choice(list(RelativeDirections))
        print(f"Next move: {next_move}")



        score, is_alive = snake.update(next_move)
        print(f"{score=}, {is_alive=}")
        draw_snake(screen=screen, snake=snake)

        # End of a generation
        if not is_alive:
            print(f"Snake died with a score of {score}")
            running = False

        clock.tick(current_speed)

        # Increasing generation counter
        current_generation += 1


def draw_snake(screen, snake) -> None:

    screen.fill("#16a085")

    # Getting the different parts of the snake
    snake_head = snake.get_head()
    snake_body = snake.get_body()
    snake_food = snake.get_food()

    # Drawing the snake
    screen.blit(snake_head[0], snake_head[1])
    for snake_body_piece in snake_body:
        screen.blit(snake_body_piece[0], snake_body_piece[1])

    # Drawing the food
    screen.blit(snake_food[0], snake_food[1])
    pygame.display.flip()

if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
