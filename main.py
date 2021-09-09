"""Main"""
from __future__ import absolute_import, division, print_function

from SnakeEnv import SnakeEnv

import random
import pygame
from pygame.constants import K_SPACE
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_d

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from snake import Snake
from directions import RelativeDirections

import base64
import imageio
import IPython
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import pyvirtualdisplay

import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import sequential
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

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

    board_size = int(((SCREEN_WIDTH - 10) / 10) * ((SCREEN_WIDTH - 10) / 10))

    print(f"{board_size=}")

    env = SnakeEnv(board_size=board_size, screen=screen)
    utils.validate_py_environment(env, episodes=5)

    train_env = tf_py_environment.TFPyEnvironment(env)
    eval_env = tf_py_environment.TFPyEnvironment(env)

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


        clock.tick(current_speed)

        # Increasing generation counter
        current_generation += 1


if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
