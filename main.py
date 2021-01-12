"""Main"""

import random
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_LEFT, K_RIGHT

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, POOL_SIZE, MOVE_ARRAY_LENGTH
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

    # Creating initial population
    brains = []

    # Creating all brains of the initial population
    for current_id in range(0, POOL_SIZE):
        current_brain_moves = []
        print("Creating brain {}".format(current_id))
        for _ in range(0, MOVE_ARRAY_LENGTH):
            current_brain_moves.append(random.choice(list(RelativeDirections)))
        current_brain = {'id': current_id, 'moves': current_brain_moves, 'score': 0}
        brains.append(current_brain)

    # ID of the current generation
    current_generation = 0

    # Main loop
    while True:

        # Exit condition
        if not running:
            break

        # Crossover
        if not current_generation == 0:

            # Stores the new gene pool
            new_pool = []

            # Average score of the previous population
            avg_sore = 0

            # Evaluating all brains
            for current_brain in brains:
                avg_sore += current_brain['score']
                for _ in range(0, current_brain['score']):
                    new_pool.append(current_brain)

            # Calculating the average score
            avg_sore /= len(brains)

            print("Average score generation {}: {}".format(current_generation, avg_sore))

            # Stores how many new brains we need to create
            brains_to_create = len(brains)

            # Clearing the old brains
            brains = []

            # Creating new brains
            for current_brain in range(0, brains_to_create):

                # Random break point
                break_point = random.randint(0, 10_000)

                # Choosing parents
                first_brain = random.choice(new_pool)
                second_brain = random.choice(new_pool)

                # Creating moves for the new brains
                new_moves = first_brain['moves'][:break_point] + second_brain['moves'][break_point:]

                # Mutating moves
                for move_id in range(0, len(new_moves)):
                    if random.randint(0, 100) < 2:
                        new_moves[move_id] = random.choice(list(RelativeDirections))

                # Creating the new brain
                brains.append({'id': current_brain, 'moves': new_moves, 'score': 0})

        # Evaluating all brains
        for current_brain in brains:

            alive = True
            snake = Snake()

            # Exit condition
            if not running:
                break

            # Moving the snake
            for current_move in current_brain['moves']:

                # Snake died last move
                if not alive:
                    break

                # Getting the next move
                next_move = current_move

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

                # Exit condition
                if not running:
                    break

                # Updating the snake position
                current_brain['score'] += snake.update(next_move)

                # Setting background color
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
                clock.tick(10000)

        # Increasing generation counter
        current_generation += 1


if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
