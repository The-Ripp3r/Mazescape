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
VISION_RADIUS = 100
SPAWN_X = 10
SPAWN_Y = 10 #default; shouldn't need bc the map should have a span location

WIDTH = 768   # 24 tiles across
HEIGHT = 512  # 16 tiles down
FPS = 60
TITLE = "Mazescape"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYERSPEED = 200
PLAYERHEALTH= 30
PLAYER_HIT_RECT = pg.Rect(0, 0, 20, 20)
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
PLAYER_GREY_BACK_STILL = "p1_still_up_grey.png"

#monster settings
MONSTERSPEED = 30
DAMAGE=10
MONSTER_HIT_RECT = pg.Rect(0, 0, 20, 20)
MONSTER_IMG_FRONT_STILL = "monster_still_down.png"
MONSTER_IMG_FRONT_WALK1 = "monster_walk1_down.png"
MONSTER_IMG_FRONT_WALK2 = "monster_walk2_down.png"
MONSTER_IMG_BACK_STILL = "monster_still_up.png"
MONSTER_IMG_BACK_WALK1 = "monster_walk1_up.png"
MONSTER_IMG_BACK_WALK2 = "monster_walk2_up.png"
MONSTER_IMG_LEFT_STILL = "monster_still_left.png"
MONSTER_IMG_LEFT_WALK1 = "monster_walk1_left.png"
MONSTER_IMG_LEFT_WALK2 = "monster_walk2_left.png"
MONSTER_IMG_RIGHT_STILL = "monster_still_right.png"
MONSTER_IMG_RIGHT_WALK1 = "monster_walk1_right.png"
MONSTER_IMG_RIGHT_WALK2 = "monster_walk2_right.png"


