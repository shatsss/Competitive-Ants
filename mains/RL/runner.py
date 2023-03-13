import json
import pickle
import random
from statistics import mean

import numpy as np
from tensorflow import keras

from mains.GameSimulator import simulate, get_grid_type_as_string, get_grid_size, get_obstacles
from players.DQN.DQNRobot import DQNRobot
from players.HeuristicFunctions.StcPlayer import StcPlayer
from players.QLearning.QLearningRobot import QLearningRobot

random.seed(1997)
np.random.seed(1997)


def rl_runner(robot_type):
    print("Start")
    # hyper-params
    test_mode = True
    window_size = 3
    discount_factor_options = [0.99, 0.5]
    game_mode = "FCC"
    ###
    # 0 - obstacles-free
    # 1 - obstacles1
    # 2 - obstacles2
    ###
    obstacles_options = [0, 1, 2]
    number_of_epoch_configurations = [0, 1, 2]
    # end of hyper-params

    if test_mode:
        print("Test Mode")
    else:
        print("Train Mode")
    global_iteration_number = 0
    ###
    # 0 - T(2)-T(1)
    # 1 - T(2)
    # 2 - lcc_local_reward
    # 3 - fcc_local_reward
    ###
    if game_mode == "FCC":
        reward_configurations = [0, 1, 3]
    elif game_mode == "LCC":
        reward_configurations = [0, 1, 2]
    else:
        raise Exception()

    # main loop - tries different configurations per environment and reward functions
    for obstacles_option in obstacles_options:
        grid_size = get_grid_size(obstacles_option)
        grid_type = get_grid_type_as_string(obstacles_option)
        obstacles_list = get_obstacles(obstacles_option, grid_size)

        for reward_function in reward_configurations:
            reward_type = get_reward_type_as_a_string(reward_function)
            for future_factory in discount_factor_options:
                if robot_type == "DQN":
                    path_prefix = "../../../models/DQN/"
                elif robot_type == "QLearning":
                    path_prefix = "../../../models/QLearning/"
                else:
                    raise Exception()
                folder_path = path_prefix + "window_size-" + str(
                    window_size) + "/" + game_mode + "/" + grid_type + "/" + reward_type + "/" + str(grid_size) + "/"
                if test_mode:
                    number_of_runs = 500
                else:
                    number_of_runs = 10000
                for epoch_number in number_of_epoch_configurations:  # The different number of models
                    file_path = folder_path + "update_frequency" + str(25) + "future_factory" + str(
                        future_factory) + "random_factor" + str(5) + "lr" + str(0.001) + "epoch" + str(
                        epoch_number) + "-" + "iteration" + str(10000)
                    if test_mode:
                        if robot_type == "DQN":
                            reconstructed_model = keras.models.load_model(file_path + '.h5')
                        elif robot_type == "QLearning":
                            reconstructed_model = json.load(open(file_path))
                        else:
                            raise Exception()
                    else:
                        reconstructed_model = None
                    if robot_type == "DQN":
                        robot = DQNRobot(player_id=2, number_of_train_iterations=number_of_runs,
                                         lr=0.001,
                                         discount_factor=future_factory,
                                         reconstructed_model=reconstructed_model, window_size=window_size)
                    elif robot_type == "QLearning":
                        robot = QLearningRobot(player_id=2, number_of_train_iterations=number_of_runs,
                                               lr=0.001,
                                               discount_factor=future_factory,
                                               reconstructed_model=reconstructed_model, window_size=window_size)
                    else:
                        raise Exception()

                    players_list = [StcPlayer(id=1), robot]
                    configuration_fcc_results = []
                    configuration_number_of_wins = 0
                    configuration_number_of_draws = 0
                    configuration_number_of_loses = 0

                    file_name = "../../../initial_locations/" + str(
                        grid_size) + "/" + grid_type + "/" + str(
                        number_of_runs) + "/initial_locations-" + str(epoch_number)
                    with open(file_name, "rb") as fp:
                        initial_locations = pickle.load(fp)
                    for i in range(0, int(number_of_runs)):
                        scores, free_cells, global_iteration_number = simulate(grid_size, players_list,
                                                                               i,
                                                                               initial_locations[i],
                                                                               opponent_reward_function=reward_function,
                                                                               obstacles_list=obstacles_list,
                                                                               update_frequency=25,
                                                                               test_mode=test_mode,
                                                                               game_mode=game_mode,
                                                                               global_iteration_number=global_iteration_number,
                                                                               window_size=window_size)
                        if test_mode and sum(scores) != free_cells:
                            raise Exception()

                        if scores[0] < scores[1]:
                            configuration_number_of_wins += 1
                        elif scores[0] == scores[1]:
                            configuration_number_of_draws += 1
                        else:
                            configuration_number_of_loses += 1
                        configuration_fcc_results += [scores[1] / free_cells]

                    if not test_mode:
                        save_model_to_file(file_path, players_list, robot_type)

                    wins_percentage_configuration = configuration_number_of_wins / number_of_runs
                    draws_percentage_configuration = configuration_number_of_draws / number_of_runs
                    loses_percentage_configuration = configuration_number_of_loses / number_of_runs
                    fcc_average_configuration = mean(configuration_fcc_results)
                    print(
                        "Game: " + game_mode + " , Environment: " + grid_type + " , Window size: " + str(
                            window_size) + ", Reward function: " + reward_type + " , future factory: " + str(
                            future_factory) + " , model number: " + str(epoch_number) + " , wins: " + str(
                            wins_percentage_configuration) + " , fcc or lcc: " + str(fcc_average_configuration))


def save_model_to_file(file_path, players_list, robot_type):
    if robot_type == "DQN":
        players_list[1].model.dqn.save(file_path)
    elif robot_type == "QLearning":
        with open(file_path, 'w') as f:
            json.dump(players_list[1].model.q_table, f)
    else:
        raise Exception()


def get_reward_type_as_a_string(reward_function):
    if reward_function == 0:
        reward_type = "T(2)-T(1)"
    elif reward_function == 1:
        reward_type = "T(2)"
    elif reward_function == 2:
        reward_type = "lcc_reward"
    elif reward_function == 3:
        reward_type = "fcc_reward"
    else:
        raise Exception()
    return reward_type
