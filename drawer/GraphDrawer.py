import numpy as np
from matplotlib import pyplot as plt


class GraphDrawer:
    def __init__(self):
        plt.ion()
        fig, ax = plt.subplots()
        fig.canvas.draw()

        self.ax = ax
        self.fig = fig
        self.robot_locations_x = []
        self.robot_locations_y = []
        self.opponent_locations_x = []
        self.opponent_locations_y = []

    def add_locations(self, robot_location, opponent_location):
        self.robot_locations_x += [robot_location[0] - 0.25]
        self.robot_locations_y += [robot_location[1] - 0.25]
        self.opponent_locations_x += [opponent_location[0] + 0.25]
        self.opponent_locations_y += [opponent_location[1] + 0.25]

    def draw(self, game_mode, graph, next_locations):
        self.add_locations(next_locations[1], next_locations[0])
        self.ax.clear()
        if game_mode == "LCC":
            matrix = np.copy(graph.who_visited_last)
        elif game_mode == "FCC":
            matrix = np.copy(graph.who_visited_first)
        else:
            raise Exception()

        our_robot_next_location_value = matrix[next_locations[1]]
        opponent_robot_next_location_value = matrix[next_locations[0]]

        matrix[next_locations[1]] = 20
        matrix[next_locations[0]] = 10

        for obstacle in graph.obstacles:
            matrix[obstacle] = -1
        self.ax.imshow(matrix, cmap='binary')
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                plt.plot(self.robot_locations_y, self.robot_locations_x, linestyle='--', color='blue')
                plt.plot(self.opponent_locations_y, self.opponent_locations_x, linestyle='--',
                         color='maroon')

                if matrix[i, j] == 0:
                    self.ax.add_artist(self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='white', edgecolor='black', linewidth=1)))
                elif matrix[i, j] == -1:
                    self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='black', edgecolor='black', linewidth=1))
                elif matrix[i, j] == 1:
                    self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='tomato', edgecolor='black', linewidth=1))
                elif matrix[i, j] == 2 or matrix[i, j] == 5:
                    self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='cornflowerblue', edgecolor='black',
                                      linewidth=1))

                elif matrix[i, j] == 3 or matrix[i, j] == 6:
                    self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='green', edgecolor='black', linewidth=1))
                elif matrix[i, j] == 20:
                    if our_robot_next_location_value == 1:
                        if game_mode == "LCC":
                            facecolor = "lightsteelblue"
                        else:
                            facecolor = 'tomato'
                    else:

                        if our_robot_next_location_value == 2 or our_robot_next_location_value == 5:
                            facecolor = 'lightsteelblue'
                        elif our_robot_next_location_value == 3 or our_robot_next_location_value == 6:
                            if game_mode == "LCC":
                                facecolor = "lightsteelblue"
                            else:
                                facecolor = 'green'
                        else:
                            facecolor = 'lightsteelblue'
                    self.ax.add_artist(
                        plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=facecolor, edgecolor='black',
                                      linewidth=1))
                    self.ax.add_artist(plt.Circle((j, i), 0.3, facecolor='cornflowerblue', edgecolor='black',
                                                  linewidth=1))
                elif matrix[i, j] == 10:

                    if opponent_robot_next_location_value == 2 or opponent_robot_next_location_value == 5:
                        if game_mode == "LCC":
                            facecolor = 'pink'
                        else:
                            facecolor = 'cornflowerblue'
                    elif opponent_robot_next_location_value == 1:
                        facecolor = 'tomato'

                    elif opponent_robot_next_location_value == 3 or opponent_robot_next_location_value == 6:
                        if game_mode == "LCC":
                            facecolor = 'pink'
                        else:
                            facecolor = 'green'
                    else:
                        facecolor = 'pink'
                    self.ax.add_artist(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=facecolor, edgecolor='black',
                                                     linewidth=1))
                    self.ax.add_artist(plt.Circle((j, i), 0.3, facecolor='tomato', edgecolor='black',
                                                  linewidth=1))
                else:
                    raise Exception()
        self.fig.canvas.flush_events()
        plt.pause(0.1)

    def finish(self):
        plt.ioff()
        plt.show()
