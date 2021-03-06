# Mazescape

A Pygame based game designed to introduce key concepts of robotics to younger audiences (e.g. high school freshman). The player is placed into a haunted maze and must find the pentagram to escape!  Avoid the Jevil.

The game does not directly talk about robotics but instead creates a game setting in which to win you must utilize particular
techniques found in certain robotics problems. For instance, mode 1 gives you a map of the maze but you do not know where you
are in the map so the player guesses their location by using their limited field of view provided by the flashlight. After making a guess, they implictly confirm/update thier guess as they explore more parts of the maze with their flashlight.  Similarly, robots/autonomous cars use a sensor (e.g. lidar) to get a small view of their immediate surroundings and calculate the probablity of a particular guess being true in respect to the given map of the environment.

In short, mode 1 is the localization mode, and is designed to teach that a robot's perspective only sees segments of the environment and updates predictions with each new piece of information.  Mode 2 removes the map but this time the enviornment has pre-designed unique landmarks distributed throughout the enviornment.  Mode 2 is the SLAM mode, and is designed to impart the concept of loop closure via landmarks.

Other featured concepts include odometry, noise, kidnapped robot problem, and more!

Libraries used: pygame, os, sys

## Running the game
1) Install python3 (3.8+)
2) Install [pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)
3) `pip install pygame-menu==2.3.3`
4) Install pytmx (pip install)
5) Install heapdict (pip install)
6) `pip install opencv-python`
7) Clone the repo
8) `cd src/`
9) `python3 main.py`

## Bugs/Suggestions

Although the game is still currently in development ("checkout" the dev branch!), if you find a bug and want to report it or you have a suggestion for the game, please feel free to send me an email at esr@mit.edu
