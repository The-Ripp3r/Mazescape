# Mazescape

A Pygame based game designed to introduce key concepts of robotics to younger audiences (e.g. high school freshman).

The game does not directly talk about robotics but instead creates a game setting in which to win you must utilize particular
techniques found in certain robotics problems. For instance, mode 1 gives you a map of the maze but you do not know where you
are in the map so the player guesses their location by using their limited field of view provided by the flashlight. After making
a guess, they implictly confirm thier prediction by exploring more parts of the maze by moving and interacting with other segments
of the enviornment with their flashlight.  Similarly, in robotics cars use a sensor (e.g. lidar) to get a small view of their 
immediate surroundings and guess at the probablity of a particular guess location being true in respect to the given map.

In short, mode 1 is the localization mode, and is designed to teach that a robot's perspective only sees segments of the environment and updates predictions
with each new piece of information.  Mode 2 removes the map but this time the enviornment has pre designed unique landmarks distributed
throughout the enviornment.  Mode 2 is the SLAM mode, and is designed to impart the concept of loop closure via landmarks.

Libraries used: pygame, os, sys
