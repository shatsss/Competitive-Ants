<h1>Competitive Ant Coverage: The Value of Pursuit
</h1>
In this project, we test different types of algorithms for the competitive ant coverage problem.


<h3>Requirements</h3>
The following dependencies are required to run the project:

1. matplotlib==3.6.2
2. numpy==1.24.1
3. tensorflow==2.11.0

<h3>Running the Project</h3>
To run the different types of algorithms, go to the mains directory and run the main files. No additional configuration
is required.

In the mains/RL/runner.py file, you can change the following variables in the RL games:

1. test_mode - This variable determines whether to train a new model or test an existing model.
2. game_mode - Determines whether to play FCC or LCC game.
3. obstacles_options - A list of environments we play. If we want a single environment to be tested\trained, create a
   list with a single number (0 - obstacle_free, 1-obstacles1, 2-obstacles2).
4. number_of_epoch_configurations - List of model numbers per configuration.
5. discount_factor_options - Options for the discount factor that will be used in the RL models.
6. window_size - What is the sensing-range of the model.

<h3>Directories</h3>

1. calculator - Calculates the new scores of both players according to their next locations and the game they play.
2. drawer - Responsible for drawing the game.
3. environment - Contains the data about the graph and holds information about the pheromones of the players.
4. initial_locations - Contains the initial locations for the games and contains a creator that is responsible for
   creating new initial locations.
5. mains - The main package, responsible for running the games.
6. models - Contains all trained models in the RL section.
7. obstacles - Contains the obstacles for obstacle1 and obstacles2 environments. It also contains a creator that creates
   new obstacles.
8. players - Contains the implementations of all different types of algorithms. The logic of the algorithms can be found
   there.

<h3>Creating Initial Locations</h3>
To create different initial locations, first, run the obstacles/obstacles_creator.py file to create new obstacles, then
run the initial_locations/initial_locations_creator.py file. (This step is not required).

<h3>Additional Information</h3>
The robot_id of the opponent is 1, and ours is 2. The opponent robot runs the STC algorithm without knowing it competes.
In order to animate the game, go to mains/GameSimulator.py file and change animate variable from False to True.