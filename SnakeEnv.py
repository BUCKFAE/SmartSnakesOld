from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from re import S

import pygame
import abc
import tensorflow as tf
import numpy as np

from snake import Snake

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

class SnakeEnv(py_environment.PyEnvironment):

  def __init__(self, board_size, screen):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=2, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(board_size,), dtype=np.float32, minimum=0, name='observation')
    self._episode_ended = False

    self.snake = Snake()
    self.screen = screen

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self._episode_ended = False
    self.snake = Snake()
    return ts.restart(observation = self.snake.to_network_input())


  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    if action in [0, 1, 2]:
      reward, is_alive = self.snake.update(action - 1)
      if not is_alive:
          self._episode_ended = True
    else:
      raise ValueError('`action` should be 0 or 1.')

    # Drawing the snake
    self.draw_snake()

    if self._episode_ended:
      return ts.termination(self.snake.to_network_input(), reward)
    else:
      return ts.transition(self.snake.to_network_input(), reward=reward, discount=1.0)


  def draw_snake(self) -> None:

        screen = self.screen
        snake=self.snake

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
