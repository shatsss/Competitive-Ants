import pickle

from environment.Graph import Graph


def main():
    if obstacles_option == "empty_grid":
        obstacles = []
    elif obstacles_option == "obstacles1" or obstacles_option == "obstacles2":
        with open("../obstacles/" + str(grid_size) + "/obstacles",
                  "rb") as tp:
            obstacles = pickle.load(tp)
    else:
        raise Exception()

    for i in range(0, number_of_epochs):
        initial_locations = []
        for _ in range(0, number_of_runs):
            initial_locations += [[Graph.get_random_cell(grid_size, obstacles) for _ in range(2)]]
        file_name = str(grid_size) + "/" + obstacles_option + "/" + str(
            number_of_runs) + "/initial_locations-" + str(i)
        with open(file_name, "wb") as fp:
            pickle.dump(initial_locations, fp)
        print(file_name)


if __name__ == '__main__':
    grid_size = 10
    number_of_runs = 100000
    number_of_epochs = 15
    obstacles_option = "empty_grid"
    main()
