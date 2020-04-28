''''''
import pygame as pg
from settings import *

class Map:
    """
    Represents a map of the maze in Mazescape.

    Attributes:
        wall_locs (dict): maps tilemap coordinates of walls to True
        teleport_locs (dict): maps tilemap coordinates of teleports to True
        player_loc (tuple): tilemap coordinates of the player sprite
        goal (tuple): tilemap coordinates of the goal sprite
        tile_height (int): the number of tilemap rows in the map
        width (int): the pixel width of the map
        height (int): the pixel height of the map
    """
    def __init__(self, filename):
        self.wall_locs = {}
        self.teleport_locs = {}
        self.player_loc = (SPAWN_X, SPAWN_Y)
        with open(filename, 'rt') as f:
                #loads map file and stores wall locations and player location
            row = 0
            for line in f:
                col = 0
                for tile in line:
                    if tile == "1":
                        self.wall_locs[col, row] = True
                    if tile == "P":
                        self.player_loc = (col, row)   
                    if tile == "G":
                        self.goal = (col, row) 
                    if tile == "T":
                        self.teleport_locs[col, row] = True
                    col += 1
                self.tile_width = col
                row += 1
        
        self.tile_height = row
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE

class Camera:
    """
    Represents a camera, which is the view the player sprite has of the map on the screen. 
    The idea here is to draw the map/drawing offset from the screen so that the screen 
    is always fixed on the player.

    Attributes:
        camera (Rect): the camera view with the specified pixel width/height
        width (int): pixel width of the camera
        height (int): pixel height of the camera
    """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width #map width
        self.height = height #map height
    

    def update(self, target):
        """
        Updates the Rect position of the camera. Remember camera keeps track of the offset 
        as its location so the camera is the opposite of player movement.
        """
        #remember the camera doesnt move in respect to the world
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        self.camera = pg.Rect(x, y, self.width, self.height)


    def apply(self, entity):
        """
        Updates an entity's Rect position based on where the Camera is located

        Args:
            entity (Sprite): the sprite to update the location for
        
        Returns:
            A Rect, which is a new rectangle that is moved by the offset of
            self.camera.topleft. It doesnt change the old one
        """
        return entity.rect.move(self.camera.topleft)

   