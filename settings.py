"""Settings"""

# Screen Settings
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100

# Reward for landing on food
FOOD_REWARD = 1

# For how many steps the snake will be rewarded (resets after hitting food)
STEP_REWARD = 0
KILL_AFTER_STEPS = 200
MAXIMUM_STEP_REWARD = 200

LEARNING_RATE = 1e-4

NUM_EVAL_EPISODES = 25
REPLAY_BUFFER_MAX_LENGTH = 10000
INITIAL_COLLECTION_STEPS = 1000

BATCH_SIZE = 32
NUM_ITERATIONS = 50000000

LOG_INTERVAL = 200
EVAL_INTERVAL = 1000
COLLECT_STEPS_PER_ITERATION = 1