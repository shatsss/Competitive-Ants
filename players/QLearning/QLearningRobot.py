import numpy as np

from players.AbstractPlayer import AbstractPlayer, distance
from players.QLearning.Q_table import Q_table


class QLearningRobot(AbstractPlayer):
    def __init__(self, player_id, number_of_train_iterations, lr, discount_factor, reconstructed_model, window_size):
        super().__init__(player_id)
        self.model = Q_table(number_of_train_iterations, lr, discount_factor, reconstructed_model=reconstructed_model,
                             window_size=window_size)

    def next_move(self, state, current_location, opponent_location, test_mode,
                  current_iteration_number, window_size):
        return self.get_next_location_and_action_of_RL_model(self.model, current_iteration_number,
                                                             current_location, state, test_mode)

    def create_state(self, current_location, opponent_location, graph, game_mode):
        if game_mode == "FCC":
            world = np.copy(graph.who_visited_first)
        elif game_mode == "LCC":
            world = np.copy(graph.who_visited_last)
        else:
            raise Exception()
        # set ours and opponent robots current locations
        world[current_location[0], current_location[1]] = 20
        world[opponent_location[0], opponent_location[1]] = 10

        # get only information in out sensing range
        sub_world = self.get_sub_world(current_location, world, graph, self.model.window_size)
        return np.expand_dims(sub_world, axis=2)

    def get_sub_world(self, current_location, world, graph, window_size):
        sub_world = np.zeros((window_size * 2 + 1, window_size * 2 + 1))
        for i in range(current_location[0] - window_size, current_location[0] + window_size + 1):
            for j in range(current_location[1] - window_size, current_location[1] + window_size + 1):
                i_index = i - (current_location[0] - window_size)
                j_index = j - (current_location[1] - window_size)
                if distance((i, j), current_location) > window_size:
                    sub_world[i_index, j_index] = -5
                elif (i, j) in graph.obstacles:
                    sub_world[i_index, j_index] = -2
                elif not graph.is_cell_legal((i, j)):
                    sub_world[i_index, j_index] = -1
                else:
                    sub_world[i_index, j_index] = world[i, j]
        return sub_world
