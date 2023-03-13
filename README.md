This project requires:
1. matplotlib==3.6.2
2. numpy==1.24.1
3. tensorflow==2.11.0

In order to run the different types of algorithms, go to the mains directory and run the main files.
The implementation of these algorithms can be found in the players' directory.
In order to train and test different configurations of the RL algorithms, change the hyper-params found in the
mains/RL/runner.py file.


In order to create different initial locations, first, run obstacles/obstacles_creator.py file in order to create
new obstacles, then run initial_locations/initial_locations_creator.py file. (This step is not required).


We have three different environments. 0-obstacles-free, 1-obstacles1 and 2-obstacles2.
In addition, the robot_id of the opponent is 1 and ours is 2. The opponent robot runs the STC algorithm without knowing
it competes.