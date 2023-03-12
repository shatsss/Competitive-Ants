import random

import numpy as np


class Q_table:

    def __init__(self, number_of_train_iterations, lr, discount_factor, reconstructed_model=None, window_size=None):
        if reconstructed_model is not None:
            self.q_table = reconstructed_model
        else:
            self.q_table = {}
        self.window_size = window_size
        self.number_of_train_iterations = number_of_train_iterations
        self.action_space_size = 4
        self.min_epsilon = 0.0
        self.max_epsilon = 1.0
        self.learning_rate = lr
        self.discount_factor = discount_factor
        self.batch_size = 128
        self.memory_size = 50000
        self.memory = []
        self.memory_current_index = 0

    def act(self, state, current_iteration_number, test_mode):
        id_of_state = self.get_id_of_state(state)
        if (not test_mode and np.random.uniform(0, 1) < self.get_current_epsilon(
                current_iteration_number=current_iteration_number)) or id_of_state not in self.q_table.keys():
            return random.randrange(self.action_space_size)
        else:
            return np.argmax(self.q_table[id_of_state])

    # after number_of_train_iterations/5 (2000( iterations, we get an epsilon 0.
    def get_current_epsilon(self, current_iteration_number):
        r = max((self.number_of_train_iterations - current_iteration_number * 5) / self.number_of_train_iterations, 0)
        return (self.max_epsilon - self.min_epsilon) * r + self.min_epsilon

    def push(self, transition):
        if len(self.memory) < self.memory_size:
            self.memory.append(None)
        self.memory[self.memory_current_index] = transition
        self.memory_current_index = (self.memory_current_index + 1) % self.memory_size

    def update_model(self):
        minibatch = random.choices(self.memory, k=self.batch_size)
        for transition in minibatch:
            id_of_state = self.get_id_of_state(transition.state)
            if id_of_state not in self.q_table.keys():
                self.q_table[id_of_state] = [0, 0, 0, 0]

            id_of_next_state = self.get_id_of_state(transition.next_state)
            if id_of_next_state not in self.q_table.keys():
                self.q_table[id_of_next_state] = [0, 0, 0, 0]

            self.q_table[id_of_state][transition.action] = self.q_table[id_of_state][
                                                               transition.action] + self.learning_rate * (
                                                                   transition.reward + self.discount_factor * np.max(
                                                               self.q_table[id_of_next_state][:]) -
                                                                   self.q_table[id_of_state][transition.action])

    def get_id_of_state(self, state):
        res = tuple(map(tuple, state.reshape(self.window_size * 2 + 1, self.window_size * 2 + 1)))
        return self.convert_tuple_of_tuples_to_string(res)

    def convert_tuple_of_tuples_to_string(self, t):
        tup = tuple(tuple(map(float, tup)) for tup in t)
        tup = sum(tup, ())
        y = list(tup)
        tup = tuple(y)
        return ','.join([str(value) for value in tup])
