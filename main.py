"""Main"""
from __future__ import absolute_import, division, print_function

from SnakeEnv import SnakeEnv

import random
import pygame
from pygame.constants import K_SPACE
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_d

from settings import *
from snake import Snake
from directions import RelativeDirections

from tensorflow.keras import datasets, layers, models
import base64
import imageio
import IPython
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
import datetime


def main():
    """Entry point of the program"""

    # Initializing pygame
    pygame.init()
    pygame.display.set_caption('Smart Snakes - Buckfae')

    # Setting up the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #screen = None


    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    train_log_dir = 'logs/snake/' + current_time + '/train'
    train_summary_writer = tf.summary.create_file_writer(train_log_dir)


    # Variable that controls the main loop
    running = True

    # Framerate
    current_speed = 3

    # ID of the current generation
    current_generation = 0

    board_size_x = int((SCREEN_WIDTH - 10) / 10)
    board_size_y = int((SCREEN_HEIGHT - 10) / 10)

    print(f"{board_size_x=}")
    print(f"{board_size_y=}")

    env = SnakeEnv(board_size_x * board_size_y, screen=screen)
    utils.validate_py_environment(env, episodes=5)

    train_env = tf_py_environment.TFPyEnvironment(env)
    eval_env = tf_py_environment.TFPyEnvironment(env)

    q_net = create_neural_network(train_env)

    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)

    train_step_counter = tf.Variable(0)

    agent = dqn_agent.DqnAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)

    agent.initialize()

    eval_policy = agent.policy
    collect_policy = agent.collect_policy

    random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())

    avg_random = compute_avg_return(eval_env, random_policy, NUM_EVAL_EPISODES)
    print(f"Average random agent: {avg_random}")

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=train_env.batch_size,
        max_length=REPLAY_BUFFER_MAX_LENGTH)

    collect_data(train_env, random_policy, replay_buffer, INITIAL_COLLECTION_STEPS)

    dataset = replay_buffer.as_dataset(
        num_parallel_calls=3, 
        sample_batch_size=BATCH_SIZE, 
        num_steps=2).prefetch(3)

    iterator = iter(dataset)
    print(iterator)


    # (Optional) Optimize by wrapping some of the code in a graph using TF function.
    agent.train = common.function(agent.train)

    # Reset the train step
    agent.train_step_counter.assign(0)

    # Evaluate the agent's policy once before training.
    avg_return = compute_avg_return(eval_env, agent.policy, NUM_EVAL_EPISODES)
    returns = [avg_return]

    for i in range(NUM_ITERATIONS):


        # Collect a few steps using collect_policy and save to the replay buffer.
        collect_data(train_env, agent.collect_policy, replay_buffer, COLLECT_STEPS_PER_ITERATION)

        # Sample a batch of data from the buffer and update the agent's network.
        experience, unused_info = next(iterator)
        train_loss = agent.train(experience).loss

        step = agent.train_step_counter.numpy() - 1

        #if step % LOG_INTERVAL == 0:
            #print('step = {0}: loss = {1}'.format(step, train_loss))

        if step % EVAL_INTERVAL == 0:
            avg_return = compute_avg_return(eval_env, agent.policy, NUM_EVAL_EPISODES)
            print('step = {0}: Average Return = {1}'.format(step, avg_return))
            returns.append(avg_return)

            with train_summary_writer.as_default():

                tf.summary.scalar('Average return', avg_return, step=step)




def create_neural_network(env):
    fc_layer_params = (160, 160, 50, 10, 10, 10)
    action_tensor_spec = tensor_spec.from_spec(env.action_spec())
    num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

    # Define a helper function to create Dense layers configured with the right
    # activation and kernel initializer.
    def dense_layer(num_units):
        return tf.keras.layers.Dense(
            num_units,
            activation=tf.keras.activations.sigmoid)

    # QNetwork consists of a sequence of Dense layers followed by a dense layer
    # with `num_actions` units to generate one q_value per available action as
    # it's output.
    dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
    q_values_layer = tf.keras.layers.Dense(
        num_actions,
        activation=None,
        kernel_initializer=tf.keras.initializers.RandomUniform(
            minval=-0.03, maxval=0.03),
        bias_initializer=tf.keras.initializers.Constant(-0.2))
    return sequential.Sequential(dense_layers + [q_values_layer])

def compute_avg_return(environment, policy, num_episodes=10):

  total_return = 0.0
  for _ in range(num_episodes):

    time_step = environment.reset()
    episode_return = 0.0

    while not time_step.is_last():
      action_step = policy.action(time_step)
      time_step = environment.step(action_step.action)
      episode_return += time_step.reward
    total_return += episode_return

  avg_return = total_return / num_episodes
  return avg_return.numpy()[0]

def collect_step(environment, policy, buffer):
  time_step = environment.current_time_step()
  action_step = policy.action(time_step)
  next_time_step = environment.step(action_step.action)
  traj = trajectory.from_transition(time_step, action_step, next_time_step)

  # Add trajectory to the replay buffer
  buffer.add_batch(traj)

def collect_data(env, policy, buffer, steps):
  for _ in range(steps):
    collect_step(env, policy, buffer)

if __name__ == "__main__":
    print("SmartSnakes - by Buckfae")
    main()
