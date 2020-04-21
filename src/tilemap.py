''''''
import pygame as pg
from settings import *

class Map:

    def __init__(self, filename):
        self.wall_locs = {}
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
                    col += 1
                self.tile_width = col
                row += 1
        
        self.tile_height = row
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE

class Camera: #the idea here is to draw the map/drawing offset from the screen so that the screen is always fixed on the player
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width #map width
        self.height = height #map height
    
    def update(self, target): #remember camera keeps track of the offset as its location so the camera is the opposite of player movement
        #remember the camera doesnt move in respect to the world
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        #limits for camera scrolling to make sure player doesnt see beyond map
        # x = min(0, x) #makes sure offset is never bigger than 0, left
        # y = min(0, y) #top
        # # #x, y are in pixels so the mimimum that the offset can be is - (map width - screen size) offset is the left hand corner of the camera
        # x = max(-(self.width - WIDTH), x) #right
        # y = max(-(self.height-HEIGHT), y) #bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
        

    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

   