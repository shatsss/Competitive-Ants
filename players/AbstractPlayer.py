import random
from abc import ABC, abstractmethod

from environment.Graph import Graph


def distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


class AbstractPlayer(ABC):
    def __init__(self, id):
        self.player_id = id
        self.graph: Graph = None

    def set_graph(self, graph: Graph):
        self.graph = graph

    @abstractmethod
    def next_move(self, current_location, opponent_location, test_mode, current_iteration_number):
        pass

    def get_player_id(self):
        return self.player_id

    # according to current location and action, we calculate the next location
    def get_next_location_according_to_action(self, current_location, index):
        if index == 0:
            if current_location[0] - 1 >= 0:
                return current_location[0] - 1, current_location[1]
            else:
                return current_location
        elif index == 1:
            if current_location[1] + 1 < self.graph.grid_size:
                return current_location[0], current_location[1] + 1
            else:
                return current_location
        elif index == 2:
            if current_location[0] + 1 < self.graph.grid_size:
                return current_location[0] + 1, current_location[1]
            else:
                return current_location
        elif index == 3:
            if current_location[1] - 1 >= 0:
                return current_location[0], current_location[1] - 1
            else:
                return current_location
        else:
            raise Exception()

    # we assume that the grid can be separated to 2x2 big cells
    # each big cell consists of 4 cells
    @staticmethod
    def get_cells_of_big_node(sub_node):
        if sub_node[0] % 2 == 0 and sub_node[1] % 2 == 0:
            return [sub_node, (sub_node[0] + 1, sub_node[1]), (sub_node[0], sub_node[1] + 1),
                    (sub_node[0] + 1, sub_node[1] + 1)]
        elif sub_node[0] % 2 == 0 and sub_node[1] % 2 == 1:
            return [sub_node, (sub_node[0], sub_node[1] - 1), (sub_node[0] + 1, sub_node[1]),
                    (sub_node[0] + 1, sub_node[1] - 1)]
        elif sub_node[0] % 2 == 1 and sub_node[1] % 2 == 0:
            return (sub_node, (sub_node[0] - 1, sub_node[1]), (sub_node[0], sub_node[1] + 1),
                    (sub_node[0] - 1, sub_node[1] + 1))
        else:
            return (sub_node, (sub_node[0] - 1, sub_node[1]), (sub_node[0], sub_node[1] - 1),
                    (sub_node[0] - 1, sub_node[1] - 1))

    def get_neighbors_of_sub_cell(self, current_location):
        neighbors = [(current_location[0] - 1, current_location[1]), (current_location[0] + 1, current_location[1]),
                     (current_location[0], current_location[1] - 1), (current_location[0], current_location[1] + 1)]
        return list(filter(self.graph.is_cell_legal, neighbors))

    # given a current location and possible next locations, the function chooses the best next location
    def get_next_cell(self, next_location, next_location_in_same_sub_cell, player_id):
        if all([self.graph.is_cell_legal(sub_node) and not self.graph.is_cell_have_been_visited_by_player(sub_node,
                                                                                                          player_id) for
                sub_node in
                self.get_cells_of_big_node(next_location)]) or (self.graph.is_cell_have_been_visited_by_player(
            next_location_in_same_sub_cell, player_id) and self.graph.is_cell_legal(next_location)):
            return next_location
        else:
            return next_location_in_same_sub_cell

    # return next location according to the STC algorithm
    def run_stc(self, current_location, id_to_look):
        if current_location[0] % 2 == 0:
            if current_location[1] % 2 == 0:
                next_location = (current_location[0], current_location[1] - 1)
                next_location_in_same_sub_cell = (current_location[0] + 1, current_location[1])
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)

            else:
                next_location_in_same_sub_cell = (current_location[0], current_location[1] - 1)
                next_location = (current_location[0] - 1, current_location[1])
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)
        else:
            if current_location[1] % 2 == 0:
                next_location_in_same_sub_cell = (current_location[0], current_location[1] + 1)
                next_location = (current_location[0] + 1, current_location[1])
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)
            else:
                next_location_in_same_sub_cell = (current_location[0] - 1, current_location[1])
                next_location = (current_location[0], current_location[1] + 1)
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)

    # return next location according to the reverse-STC algorithm
    def run_reverse_stc(self, current_location, id_to_look):
        if current_location[0] % 2 == 0:
            if current_location[1] % 2 == 0:
                next_location = (current_location[0] - 1, current_location[1])
                next_location_in_same_sub_cell = (current_location[0], current_location[1] + 1)
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)

            else:
                next_location_in_same_sub_cell = (current_location[0] + 1, current_location[1])
                next_location = (current_location[0], current_location[1] + 1)
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)
        else:
            if current_location[1] % 2 == 0:
                next_location_in_same_sub_cell = (current_location[0] - 1, current_location[1])
                next_location = (current_location[0], current_location[1] - 1)
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)
            else:
                next_location_in_same_sub_cell = (current_location[0], current_location[1] - 1)
                next_location = (current_location[0] + 1, current_location[1])
                return self.get_next_cell(next_location, next_location_in_same_sub_cell, id_to_look)

    # returns the next location and action selected by the RL model
    def get_next_location_and_action_of_RL_model(self, rl_mode, current_iteration_number, current_location, state,
                                                 test_mode):
        action = rl_mode.act(state, current_iteration_number, test_mode)
        next_location = self.get_next_location_according_to_action(current_location, action)
        while test_mode and (next_location == current_location or self.graph.is_obstacle(next_location)):
            action = random.randrange(rl_mode.action_space_size)
            next_location = self.get_next_location_according_to_action(current_location, action)
        return next_location, action
