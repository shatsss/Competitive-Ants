import random

import numpy as np
from tensorflow import keras


class DQN:

    def __init__(self, number_of_train_iterations, lr, discount_factor, reconstructed_model, window_size):
        self.window_size = window_size
        # in the test, we have a trained model
        if reconstructed_model is not None:
            self.dqn = reconstructed_model
        else:
            self.dqn = self.create_model(lr=lr)
        self.number_of_train_iterations = number_of_train_iterations
        self.action_space_size = 4
        self.min_epsilon = 0.0
        self.max_epsilon = 1
        self.discount_factor = discount_factor
        self.batch_size = 128
        self.memory_size = 50000
        self.memory = []
        self.memory_current_index = 0

    # creates the architecture of the model
    def create_model(self, lr):
        model = keras.Sequential()
        model.add(keras.layers.Conv2D(32, (3, 3), padding='same', strides=1,
                                      input_shape=(self.window_size * 2 + 1, self.window_size * 2 + 1, 4),
                                      activation='selu'))
        model.add(keras.layers.Conv2D(64, (3, 3), padding="same", activation="selu", strides=1))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(128, activation='selu'))
        model.add(keras.layers.Dense(4, activation='linear'))

        optimizer = keras.optimizers.Adam(learning_rate=lr)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mse'])
        return model

    # saved transition into the memory
    def push(self, transition):
        if len(self.memory) < self.memory_size:
            self.memory.append(None)
        self.memory[self.memory_current_index] = transition
        self.memory_current_index = (self.memory_current_index + 1) % self.memory_size

    # we use epsilon-greedy for the randomness, after number_of_train_iterations/5 (2000) iterations we reach an epsilon 0.
    def get_current_epsilon(self, current_iteration_number):
        r = max((self.number_of_train_iterations - current_iteration_number * 5) / self.number_of_train_iterations, 0)
        return (self.max_epsilon - self.min_epsilon) * r + self.min_epsilon

    # choose next action of a player
    def act(self, state, current_iteration_number, test_mode):
        if not test_mode and \
                np.random.uniform(0, 1) < self.get_current_epsilon(current_iteration_number=current_iteration_number):
            return random.randrange(self.action_space_size)
        else:
            expanded_state = np.expand_dims(state, axis=0)
            act_values = self.dqn(expanded_state)
            return np.argmax(act_values[0])

    # update the model in batches
    def update_model(self):
        minibatch = random.choices(self.memory, k=self.batch_size)
        states = np.array([i.state for i in minibatch])
        actions = np.array([i.action for i in minibatch])
        rewards = np.array([i.reward for i in minibatch])
        next_states = np.array([i.next_state for i in minibatch])
        dones = np.array([i.done for i in minibatch])

        targets = rewards + self.discount_factor * (np.amax(self.dqn.predict_on_batch(next_states), axis=1)) * (
                1 - dones)
        targets_full = np.array(self.dqn.predict_on_batch(states))
        for i in range(self.batch_size):
            targets_full[i][actions[i]] = targets[i]

        self.dqn.fit(states, targets_full, verbose=0)
