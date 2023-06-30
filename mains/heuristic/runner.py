import pickle
import random
from statistics import mean

import numpy as np

from mains.GameSimulator import simulate, get_grid_type_as_string, get_grid_size, get_obstacles
from players.HeuristicFunctions.StcPlayer import StcPlayer

random.seed(1997)
np.random.seed(1997)


# main heuristic algorithms class, runs different configurations (for example, different environments)
# Per configuration, the class simulates 500 different runs
# Per run, the class simulate a game of both players and calculates the scores of both players
# The final result is the average scores across 500 simulations
def heuristic_runner(player, game_mode):
    global_iteration_number = 0
    ###
    # 0 - obstacles-free
    # 1 - obstacles1
    # 2 - obstacles2
    ###
    obstacles_options = [0, 1, 2]
    # different configurations
    for obstacles_option in obstacles_options:
        grid_size = get_grid_size(obstacles_option)
        grid_type = get_grid_type_as_string(obstacles_option)
        obstacles_list = get_obstacles(obstacles_option, grid_size)
        players_list = [StcPlayer(id=1), player]

        number_of_wins_of_the_model = 0
        number_of_draws_of_the_model = 0
        number_of_loses_of_the_model = 0
        fcc_results_of_the_model = []

        number_of_runs = 500

        file_name = "../../../initial_locations/" + str(grid_size) + "/" + grid_type + "/" + str(
            number_of_runs) + "/initial_locations-0"
        with open(file_name, "rb") as fp:
            initial_locations = pickle.load(fp)
        # simulates 500 runs
        for i in range(0, int(number_of_runs)):
            # simulates specific run
            scores, number_of_free_cells, global_iteration_number = simulate(grid_size,
                                                                             players_list,
                                                                             i,
                                                                             initial_locations[i],
                                                                             opponent_reward_function=None,
                                                                             obstacles_list=obstacles_list,
                                                                             update_frequency=None,
                                                                             test_mode=True,
                                                                             game_mode=game_mode,
                                                                             global_iteration_number=global_iteration_number)
            if sum(scores) != number_of_free_cells:
                raise Exception()

            if scores[0] <= scores[1]:
                number_of_wins_of_the_model += 1
            elif scores[0] == scores[1]:
                number_of_draws_of_the_model += 1
            else:
                number_of_loses_of_the_model += 1

            fcc_results_of_the_model += [scores[1] / number_of_free_cells]
        # average across 500 simulations
        win_percentage_of_the_model = number_of_wins_of_the_model / number_of_runs
        draw_percentage_of_the_model = number_of_draws_of_the_model / number_of_runs
        loss_percentage_of_the_model = number_of_loses_of_the_model / number_of_runs
        fcc_average_of_the_model = mean(fcc_results_of_the_model)
        print(
            "grid size: " + str(grid_size) + " , grid_type: " + str(
                grid_type) + " , wins: " + str(
                win_percentage_of_the_model) + " , draws: " + str(
                draw_percentage_of_the_model) + " , loses: " + str(
                loss_percentage_of_the_model) + " , fcc: " + str(
                fcc_average_of_the_model))
