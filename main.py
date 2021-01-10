"""Main"""

import random
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

    # Creating initial population
    brains = []

    for current_id in range(0, 100):
        current_brain_moves = []
        print("Creating brain {}".format(current_id))
        for _ in range(0, 10_000):
            current_brain_moves.append(random.choice(list(RelativeDirections)))
        current_brain = {'id': current_id, 'moves': current_brain_moves, 'score': 0}
        brains.append(current_brain)


    # Main loop
    for current_generation in range(0, 1_000_000):

        print("Current Generation: {}".format(current_generation))
        
        # Crossover
        if not current_generation == 0:
            new_pool = []
            avg = 0
            for current_brain in brains:
                avg += current_brain['score']
                for i in range(0, current_brain['score']):
                    new_pool.append(current_brain)
            avg /= len(brains)

            print("Avg: {}".format(avg))
            brains_to_create = len(brains)
            brains = []
            for current_brain in range(0, brains_to_create):
                break_point = random.randint(0, 10_000)
                first_brain = random.choice(new_pool)
                second_brain = random.choice(new_pool)
                new_moves = first_brain['moves'][:break_point] + second_brain['moves'][break_point:]
                new_brain = {'id': current_brain, 'moves': new_moves, 'score': 0}
                brains.append(new_brain)


        for current_brain in brains:

            alive = True
            snake = Snake()

            for current_move in current_brain['moves']:

                # Snake died last move
                if not alive:
                    break

                # Getting the next move
                next_move = current_move
     
                # Exit conditiion - TODO
                if not running:
                    break

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
                current_brain['score'] += snake.update(next_move)

                # Setting backround color
                screen.fill(("#16a085"))

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

                # Checking if the snake hit itself
                if any([snake_head[1].colliderect(body_piece[1]) for body_piece in snake_body]):
                    alive = False

                # Checking if the snake is out of bounds
                if snake_head[1].x < 0 or snake_head[1].y < 0 \
                        or snake_head[1].center[0] > SCREEN_WIDTH \
                        or snake_head[1].center[1] > SCREEN_HEIGHT:
                    alive = False

                # Pushing changes to screen
                pygame.display.flip()
                clock.tick(10000000000)

if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
