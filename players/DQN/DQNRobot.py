import numpy as np

from players.AbstractPlayer import AbstractPlayer, distance
from players.DQN.DQN import DQN


class DQNRobot(AbstractPlayer):
    def __init__(self, player_id, number_of_train_iterations, lr, discount_factor, reconstructed_model, window_size):
        super().__init__(player_id)
        self.model = DQN(number_of_train_iterations, lr, discount_factor, reconstructed_model=reconstructed_model,
                         window_size=window_size)

    def next_move(self, state, current_location, opponent_location, test_mode, current_iteration_number, window_size):
        return self.get_next_location_and_action_of_RL_model(self.model, current_iteration_number,
                                                             current_location, state, test_mode)

    def create_state(self, current_location, opponent_location, graph, game_mode):
        agent_position = self.get_agents_positions_frame(current_location, opponent_location, graph,
                                                         self.model.window_size)
        agent_obstacles = self.get_agent_obstacles_frame(current_location, graph, self.model.window_size)
        first_pheromones = self.get_who_visited_the_cells_first_frame(current_location, graph, self.model.window_size)
        last_pheromones = self.get_who_visited_the_cells_last_frame(current_location, graph, self.model.window_size)

        return np.stack([agent_position, agent_obstacles, first_pheromones, last_pheromones], axis=-1)

    def get_agents_positions_frame(self, current_location, opponent_location, graph, window_size):
        sub_world = np.zeros((window_size * 2 + 1, window_size * 2 + 1))
        for i in range(current_location[0] - window_size, current_location[0] + window_size + 1):
            for j in range(current_location[1] - window_size, current_location[1] + window_size + 1):
                i_index_in_frame = i - (current_location[0] - window_size)
                j_index_in_frame = j - (current_location[1] - window_size)
                if distance((i, j), current_location) > window_size:
                    sub_world[i_index_in_frame, j_index_in_frame] = -5
                elif not graph.is_cell_legal((i, j)):
                    sub_world[i_index_in_frame, j_index_in_frame] = -1
                else:
                    if (i, j) == current_location:
                        sub_world[i_index_in_frame, j_index_in_frame] = 2
                    elif (i, j) == opponent_location:
                        sub_world[i_index_in_frame, j_index_in_frame] = 1
                    else:
                        sub_world[i_index_in_frame, j_index_in_frame] = 0
        return sub_world

    def get_agent_obstacles_frame(self, current_location, graph, window_size):
        sub_world = np.zeros((window_size * 2 + 1, window_size * 2 + 1))
        for i in range(current_location[0] - window_size, current_location[0] + window_size + 1):
            for j in range(current_location[1] - window_size, current_location[1] + window_size + 1):
                i_index_in_frame = i - (current_location[0] - window_size)
                j_index_in_frame = j - (current_location[1] - window_size)
                if distance((i, j), current_location) > window_size:
                    sub_world[i_index_in_frame, j_index_in_frame] = -5
                elif (i, j) in graph.obstacles:
                    sub_world[i_index_in_frame, j_index_in_frame] = 1
                elif not graph.is_cell_legal((i, j)):
                    sub_world[i_index_in_frame, j_index_in_frame] = -1
                else:
                    sub_world[i_index_in_frame, j_index_in_frame] = 0
        return sub_world

    def get_who_visited_the_cells_first_frame(self, current_location, graph, window_size):
        sub_world = np.zeros((window_size * 2 + 1, window_size * 2 + 1))
        for i in range(current_location[0] - window_size, current_location[0] + window_size + 1):
            for j in range(current_location[1] - window_size, current_location[1] + window_size + 1):
                i_index_in_frame = i - (current_location[0] - window_size)
                j_index_in_frame = j - (current_location[1] - window_size)
                if distance((i, j), current_location) > window_size:
                    sub_world[i_index_in_frame, j_index_in_frame] = -5
                elif not graph.is_cell_legal((i, j)):
                    sub_world[i_index_in_frame, j_index_in_frame] = -1
                else:
                    sub_world[i_index_in_frame, j_index_in_frame] = graph.get_first_player_who_visited_the_cell((i, j))
        return sub_world

    def get_who_visited_the_cells_last_frame(self, current_location, graph, window_size):
        sub_world = np.zeros((window_size * 2 + 1, window_size * 2 + 1))
        for i in range(current_location[0] - window_size, current_location[0] + window_size + 1):
            for j in range(current_location[1] - window_size, current_location[1] + window_size + 1):
                i_index_in_frame = i - (current_location[0] - window_size)
                j_index_in_frame = j - (current_location[1] - window_size)
                if distance((i, j), current_location) > window_size:
                    sub_world[i_index_in_frame, j_index_in_frame] = -5
                elif not graph.is_cell_legal((i, j)):
                    sub_world[i_index_in_frame, j_index_in_frame] = -1
                else:
                    sub_world[i_index_in_frame, j_index_in_frame] = graph.get_last_player_who_visited_the_cell((i, j))
        return sub_world
