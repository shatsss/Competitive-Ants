import random

import numpy as np


# This class represents the environment
# The cells of the environment updated according to the players actions

class Graph:
    def __init__(self, grid_size, obstacles_list=None):
        self.empty_grid = np.zeros((grid_size, grid_size))
        self.who_visited_first = np.copy(self.empty_grid)
        self.who_visited_last = np.copy(self.empty_grid)
        self.obstacles = obstacles_list
        self.visited_cells_per_player = {}  # the cells that have been visited per player dictionary
        self.grid_size = grid_size
        self.number_of_cells_visited = 0

    def is_obstacle(self, location):
        return location in self.obstacles

    ###
    # 1 - opponent's id
    # 2 - ours player id
    ###
    def set_visited(self, location, id_of_player, both_players_visited_in_the_same_time):
        if both_players_visited_in_the_same_time:
            if self.get_visited_value_of_cell(location) == 0:
                self.who_visited_first[location] = 3  # 3 means that the cell visited by both players in the same time
                self.number_of_cells_visited += 1
            self.who_visited_last[location] = 3 # both players visited the cell at the same time
        else:
            if self.get_visited_value_of_cell(location) == 0:
                self.who_visited_first[location] = id_of_player  # we set player_id as who visited first the cell
                self.number_of_cells_visited += 1
            self.who_visited_last[location] = id_of_player

        if id_of_player not in self.visited_cells_per_player.keys():
            self.visited_cells_per_player[id_of_player] = np.copy(self.empty_grid)
        self.visited_cells_per_player[id_of_player][location] = id_of_player

    def get_first_player_who_visited_the_cell(self, location):
        return np.copy(self.who_visited_first[location])

    def get_last_player_who_visited_the_cell(self, location):
        return np.copy(self.who_visited_last[location])

    def is_cell_have_been_visited_by_player(self, location, player_id):
        return player_id in self.visited_cells_per_player.keys() and self.visited_cells_per_player[player_id][
            location] == player_id

    def is_cell_legal(self, location):
        return (0 <= location[0] < self.grid_size and 0 <= location[
            1] < self.grid_size) and location not in self.obstacles

    ###
    # 0 - not visited
    # 1 - visited by the opponent
    # 2 - visited by ours player
    # 3 - visited by both player in the same time
    ###
    def get_visited_value_of_cell(self, location):
        cell_value = 0
        for value in self.visited_cells_per_player.values():
            cell_value += value[location]
        return cell_value

    def is_visited_last_by_both_players(self, location):
        return self.who_visited_last[location] == 3

    def is_visited_last_by_player(self, location, player_id):
        return self.who_visited_last[location] == player_id

    def is_cell_not_visited_by_any_player(self, location):
        return self.get_visited_value_of_cell(location) == 0

    @staticmethod
    def get_random_cell(grid_size, obstacles):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        while (x, y) in obstacles:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)
        return x, y

    def all_vertices_visited(self):
        return (self.number_of_cells_visited + len(self.obstacles)) == self.grid_size ** 2
