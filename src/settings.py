import pygame as pg
'''Settings'''

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKRED = (139, 0, 0)
LIGHTBLUE = (0, 191, 255)

# game settings
#update: I changed the window screen to be comparable to a nintendo DS screen to emulate pokemon
# the maps are currently 32x32 tiles but we can increase that to arbitrary dimensions
# I wanted 24*16 with a tile size of 32 pixels bc that would allow 24x24 pixel or 32x32 pixel sprites
VISION_RADIUS = 100
SPAWN_X = 10
SPAWN_Y = 10 #default; shouldn't need bc the map should have a span location

WIDTH = 768   # 16 * 64 or 32 * 32 or 64 * 16; 1024; I changed it to 32*24 so 24 tiles across
HEIGHT = 512  # 16 * 48 or 32 * 24 or 64 * 12; 768; I changed it to 32*16  so 16 tiles down
FPS = 60
TITLE = "Mazescape"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYERSPEED = 200
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_IMG_FRONT_STILL = "p1_still.png"
PLAYER_IMG_FRONT_WALK1 = "p1_walk1.png"
PLAYER_IMG_FRONT_WALK2 = "p1_walk2.png"
PLAYER_IMG_BACK_STILL = "p1_still_up.png"
PLAYER_IMG_BACK_WALK1 = "p1_walk1_up.png"
PLAYER_IMG_BACK_WALK2 = "p1_walk2_up.png"
PLAYER_IMG_LEFT_STILL = "p1_still_left.png"
PLAYER_IMG_LEFT_WALK1 = "p1_walk1_left.png"
PLAYER_IMG_LEFT_WALK2 = "p1_walk2_left.png"
PLAYER_IMG_RIGHT_STILL = "p1_still_right.png"
PLAYER_IMG_RIGHT_WALK1 = "p1_walk1_right.png"
PLAYER_IMG_RIGHT_WALK2 = "p1_walk2_right.png"



