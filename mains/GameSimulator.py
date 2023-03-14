import pickle

import numpy as np

from calculator.scores_calculator import update_scores
from drawer.GraphDrawer import GraphDrawer
from environment.Graph import Graph
from environment.Transition import Transition
from players.AbstractPlayer import distance
from players.DQN.DQNRobot import DQNRobot
from players.QLearning.QLearningRobot import QLearningRobot

BAD_REWARD = -0.25


def simulate(grid_size, players_list, train_iteration_number, initial_locations,
             opponent_reward_function, obstacles_list, update_frequency, test_mode, animate=False, game_mode=None,
             global_iteration_number=None, window_size=None):
    if animate:
        drawer = GraphDrawer()
    graph = Graph(grid_size, obstacles_list=obstacles_list)
    for player in players_list:
        player.set_graph(graph)

    current_locations = initial_locations
    if animate:
        drawer.add_locations(current_locations[1], current_locations[0])
    set_initial_locations_as_visited(current_locations, graph, players_list)

    scores = np.zeros(len(players_list))
    if current_locations[0] == current_locations[1]:
        scores += 0.5
    else:
        scores += 1

    total_number_of_iterations = graph.grid_size ** 2 - len(graph.obstacles)
    current_iteration_number = 0
    next_locations = [None, None]

    while current_iteration_number < total_number_of_iterations - 1:
        player_0_next_location = players_list[0].next_move(current_locations[0])
        if isinstance(players_list[1], DQNRobot) or isinstance(players_list[1], QLearningRobot):
            state = players_list[1].create_state(current_locations[1], current_locations[0], graph, game_mode=game_mode)
            player_1_next_location, action = players_list[1].next_move(state, current_locations[1],
                                                                       current_locations[0],
                                                                       test_mode, train_iteration_number, window_size)
        else:
            player_1_next_location, _ = players_list[1].next_move(current_locations[1], current_locations[0],
                                                                  player_0_next_location)
        if distance(player_1_next_location, current_locations[1]) > 1:  # validation that next move is legal
            raise Exception()

        if (isinstance(players_list[1], DQNRobot) or isinstance(players_list[1],
                                                                QLearningRobot)) and (player_1_next_location ==
                                                                                      current_locations[
                                                                                          1] or not graph.is_cell_legal(
                    player_1_next_location)):
            reward = -2 * (graph.grid_size ** 2)
            if isinstance(players_list[1], DQNRobot):
                next_state = np.full((window_size * 2 + 1, window_size * 2 + 1, 4), -100)
            elif isinstance(players_list[1], QLearningRobot):
                next_state = np.full((window_size * 2 + 1, window_size * 2 + 1, 1), -100)
            else:
                raise Exception()
            if not test_mode:
                players_list[1].model.push(Transition(state, action, reward, next_state, True))
            break

        next_locations = [player_0_next_location, player_1_next_location]
        previous_scores = scores.copy()
        update_scores(game_mode, graph, next_locations, player_0_next_location,
                      player_1_next_location, players_list, scores)

        if animate:
            drawer.draw(game_mode=game_mode, graph=graph, next_locations=next_locations)

        player_1_cell_visited_last_value = graph.get_last_player_who_visited_the_cell(player_1_next_location)
        both_players_visited_simultaneously = next_locations[0] == next_locations[1]
        graph.set_visited(player_0_next_location, players_list[0].get_player_id(), both_players_visited_simultaneously)
        graph.set_visited(player_1_next_location, players_list[1].get_player_id(), both_players_visited_simultaneously)

        if not test_mode and isinstance(players_list[1], DQNRobot) or isinstance(players_list[1], QLearningRobot):
            next_state = players_list[1].create_state(player_1_next_location, player_0_next_location, graph,
                                                      game_mode=game_mode)
            reward = get_reward(scores, previous_scores, opponent_reward_function, player_1_cell_visited_last_value)
            players_list[1].model.push(Transition(state, action, reward, next_state, False))
            if global_iteration_number % update_frequency == 0:
                players_list[1].model.update_model()

        current_locations = next_locations
        current_iteration_number += 1
        global_iteration_number += 1

    if animate:
        drawer.finish()
    return scores, graph.grid_size ** 2 - len(graph.obstacles), global_iteration_number


def get_reward(scores, previous_scores, opponent_reward_function, player_1_cell_visited_last_value):
    new_scores = scores - previous_scores
    # T(2)-T(1)
    if opponent_reward_function == 0:
        if (new_scores[1]) == 0:
            return BAD_REWARD - new_scores[0]
        else:
            return new_scores[1] - new_scores[0]
    # T(2)
    elif opponent_reward_function == 1:
        if new_scores[1] == 0:
            return BAD_REWARD
        else:
            return new_scores[1]
    # lcc_local_reward
    elif opponent_reward_function == 2:
        if player_1_cell_visited_last_value == 1:
            return 2
        elif player_1_cell_visited_last_value == 0 or player_1_cell_visited_last_value == 3:
            return 1
        elif player_1_cell_visited_last_value == 2:
            return BAD_REWARD
        else:
            raise Exception(str(player_1_cell_visited_last_value) + " is not valid")
    # fcc_local_reward
    elif opponent_reward_function == 3:
        if player_1_cell_visited_last_value == 0:
            return 1
        else:
            return BAD_REWARD


def set_initial_locations_as_visited(current_locations, graph, players_list):
    for i, current_location in enumerate(current_locations):
        if current_locations[0] == current_locations[1]:
            both_visited = True
        else:
            both_visited = False
        graph.set_visited(location=current_location, id_of_player=players_list[i].player_id,
                          both_players_visited_in_the_same_time=both_visited)


def get_grid_type_as_string(obstacles_option):
    if obstacles_option == 0:
        grid_type = "empty_grid"
    elif obstacles_option == 1:
        grid_type = "obstacles1"
    elif obstacles_option == 2:
        grid_type = "obstacles2"
    else:
        raise Exception()
    return grid_type


def get_obstacles(obstacles_option, grid_size):
    if obstacles_option == 2 or obstacles_option == 1:
        with open("../../../obstacles/" + str(grid_size) + "/obstacles",
                  "rb") as tp:
            obstacles_list = pickle.load(tp)
    else:  # obstacles_option = 0, free-obstacles grid
        obstacles_list = []
    return obstacles_list


def get_grid_size(obstacles_option):
    if obstacles_option == 2:
        grid_size = 14
    else:
        grid_size = 10
    return grid_size
