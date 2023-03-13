import pickle
import random

import numpy as np

from environment.Graph import Graph
from players.HeuristicFunctions.StcPlayer import StcPlayer

random.seed(1997)
np.random.seed(1997)


def get_new_obstacle_location(grid_size, obstacles_list):
    cell = Graph.get_random_cell(grid_size, obstacles_list)
    while cell[0] < 2 or cell[0] > grid_size - 3 or cell[1] < 2 or cell[
        1] > grid_size - 3:  # we don't want cells in the borders of the grid
        cell = Graph.get_random_cell(grid_size, obstacles_list)
    return cell


def check_the_graph_is_fully_connected_with_the_new_cell(obstacles_list, cell, grid_size):
    obstacles_list_with_new_cell = obstacles_list + list(StcPlayer.get_cells_of_big_node(cell))
    graph = Graph(grid_size, obstacles_list=obstacles_list_with_new_cell)
    stc_player = StcPlayer(id=1)
    stc_player.set_graph(graph)
    current_cell = Graph.get_random_cell(grid_size, obstacles_list_with_new_cell)
    graph.set_visited(current_cell, stc_player.player_id, both_players_visited_in_the_same_time=False)
    for _ in range(grid_size ** 2 - len(obstacles_list_with_new_cell) - 1):
        next_location = stc_player.next_move(current_cell)
        if not graph.is_cell_legal(next_location) or graph.is_cell_have_been_visited_by_player(next_location,
                                                                                               stc_player.player_id):
            break
        graph.set_visited(next_location, stc_player.player_id, both_players_visited_in_the_same_time=False)
        current_cell = next_location
    if graph.all_vertices_visited():
        return obstacles_list_with_new_cell
    else:
        return obstacles_list


def main():
    grid_size = 10
    obstacles_list = []
    while len(obstacles_list) < grid_size ** 2 / 4:
        cell = get_new_obstacle_location(grid_size, obstacles_list)
        # check if the new cell is an obstacle, we can reach all free cells in the graph
        obstacles_list = check_the_graph_is_fully_connected_with_the_new_cell(obstacles_list, cell, grid_size)

    with open(str(grid_size) + "/obstacles", "wb") as fp:
        pickle.dump(obstacles_list, fp)

    # validation that it works
    with open(str(grid_size) + "/obstacles", "rb") as fp:
        obstacles_list = pickle.load(fp)
    print(obstacles_list)


if __name__ == '__main__':
    main()
