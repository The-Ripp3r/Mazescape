'''Settings'''

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
#update: I changed the window screen to be comparable to a nintendo DS screen to emulate pokemon
# the maps are currently 32x32 tiles but we can increase that to arbitrary dimensions
# I wanted 24*16 with a tile size of 32 pixels bc that would allow 24x24 pixel or 32x32 pixel sprites
VISION_RADIUS = 100


WIDTH = 768   # 16 * 64 or 32 * 32 or 64 * 16; 1024; I changed it to 32*24 so 24 tiles across
HEIGHT = 512  # 16 * 48 or 32 * 24 or 64 * 12; 768; I changed it to 32*16  so 16 tiles down
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYERSPEED = 300
