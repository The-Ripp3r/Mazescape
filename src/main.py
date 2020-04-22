'''Tilemap game'''
import sys
from os import path
import pygame as pg
from settings import *
from sprites import *
from tilemap import *

class Game:
    """
    Represents the Mazescape game
    """
    def __init__(self):
        """
        Initialize Game settings.

        :param self.screen: (Surface) the screen for the game
        :param self.clock: (Clock) clock to keep track of time
        :param self.folder: (str) directory for this file
        """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # pg.key.set_repeat(250, 100)
        self.folder = path.dirname(__file__)
        self.load_data('research_map', 'research_map_tp')

    def load_data(self, map_name, tp_name):
        """
        Loads data for a specific game level.
        
        :param map_name: (str) name of the map without the extension (e.g. 'research_map'). 
                               map_name is a .txt located in map subfolder of self.folder.
        :param self.map: (Map) represents the map of the maze
        :param self.teleport_map: (str) path to file that maps teleport locations 
        """
        map_loc = 'maps/' + map_name + '.txt'
        self.map = Map(path.join(self.folder, map_loc))
        self.teleport_map = 'maps/' + tp_name + '.txt'

    def new(self):
        """
        Initialize and setup a new game level

        :param self.all_sprites: (Group) container class to hold multiple Sprite objects
        :param self.walls: (Group) container class to hold multiple Wall objects
        :param self.teleports: (Group) container class to hold multiple Teleport objects
        :param self.win: (Group) container class to hold win conditions
        :param self.player: (Player) represents the player on the map
        :param self.goal: (Goal) represents the goal on the map
        :param self.camera: (Camera) represents the camera on the map
        """
        self.all_sprites = pg.sprite.Group() 
        self.walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group() 
        self.win = pg.sprite.Group() 
        self.player = Player(self, self.map.player_loc[0], self.map.player_loc[1])
        self.goal = Goal(self, self.map.goal[0], self.map.goal[1])
        for loc in self.map.wall_locs:
            Wall(self, loc[0], loc[1])
        for loc in self.map.teleport_locs:
            Teleport(self, loc[0], loc[1], self.teleport_map)
        
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        """
        Runs the Mazescape game.

        :param self.playing: (bool) if the player is playing the game
        :param self.dt: (int) the framerate of the game
        """
        #game loop set self.playing to False to end game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit_game(self):
        """
        Quits the Mazescape game
        """
        pg.quit()
        sys.exit()

    def events(self):
        """
        Catches all game-related events
        """
        #   catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit_game()

        #   win condition
        if pg.sprite.spritecollide(self.player, self.win, False):
            self.quit_game()

        
        #   teleportation
        tel_block_hit = pg.sprite.spritecollide(self.player, self.teleports, False)
        if tel_block_hit:
            #   Find the other teleport block
            destination_x, destination_y = tel_block_hit[0].tp_x, tel_block_hit[0].tp_y
            #   Adjust the destination by considering player's movement
            x_modifier = 0
            if self.player.vx > 0:
                x_modifier = 1
            elif self.player.vx < 0:
                x_modifier = -1
            y_modifier = 0
            if self.player.vy > 0:
                y_modifier = 1
            elif self.player.vy < 0:
                y_modifier = -1
            self.player.x = (destination_x + x_modifier) * TILESIZE
            self.player.y = (destination_y + y_modifier) * TILESIZE

                
    def update(self):
        """
        Updates the frame of the game
        """
        self.all_sprites.update() #*************
        self.camera.update(self.player)


    def draw_grid(self):
        """
        Draws a grid onto the map
        """
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
      
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        
    def draw(self):
        """
        Draws the given map level by layering all the sprites.
        """
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #   Layer all sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #   Reduce vision of the map
        # for r in range(VISION_RADIUS, 600):
        #     pg.draw.circle(self.screen, BLACK, (int(WIDTH/2), int(HEIGHT/2)), r, 1)
        pg.display.flip() #update the full display surface to the screen

    def show_start_screen(self):
        """
        Displays the Mazescape start screen
        """
        pass

    def show_go_screen(self):
        pass

#create game
g= Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
