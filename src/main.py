'''Tilemap game'''
import sys
import wave
from os import path
import pygame as pg
import menu
from settings import *
from sprites import *
from tilemap import *
import time
from random import uniform, choice, randint

class Game:
    """
    Represents the Mazescape game.

    Attributes:
        General Game Settings:
            screen (Surface): the screen for the game
            clock (Clock): clock to keep track of time
            folder (str): directory for this file
            dt (milliseconds): the time increments 
    
        Map Data:
            map (Map): represents the map of the maze
            minimap (Surface): the minimap of the maze
            teleport_map (str): path to file that has dict of teleport locations 
        
        Maze Level Data:
            moving_sprites (Group): container class to hold multiple Sprite objects
            walls (Group): container class to hold multiple Wall objects
            teleports (Group): container class to hold multiple Teleport objects
            win (Group): container class to hold win conditions
            player (Player): represents the player on the map
            player_img (Surface): image of the player 
            goal (Goal): represents the goal on the map
            camera (Camera): represents the camera on the map
    """
    def __init__(self, mode):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        #folder names
        self.game_folder = path.dirname(__file__)
        self.sprite_folder = path.join(self.game_folder, 'sprites')
        self.animation_folder = path.join(self.game_folder, 'animation')
        self.map_folder = path.join(self.game_folder, 'maps')
        #set mode
        self.mode = mode
        minimap = 'extended_map.png' if mode == '1' else None
     

        #tuning
        self.offset_x=1
        self.offset_y=2.5
        self.lost=False
        
        self.load_data('extended_map.tmx', 'extended_map.txt', 'extended_map_tp.txt', minimap_name=minimap)

    def load_data(self, map_name, grid_name, tp_name, minimap_name=None):
        """
        Loads data for a specific game map level.

        Args:
            map_name (str): name of the map without the extension (e.g. 'research_map'). 
                map_name is a .txt located in map subfolder of self.folder.
            minimap_name (str): name of the minimap without the extension (e.g. 'research_minimap'). 
                minimap_name is a .png located in map subfolder of self.folder.
            tp_name (str): name of the file without the extension (e.g. 'reserach_map_tp').
                maps coordinates of teleport tiles to each other in pairs.
                tp_name is a .txt located in map subfolder of self.folder.
        """
        
        self.map= TiledMap(path.join(self.map_folder, map_name))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        if minimap_name != None:
            self.minimap = pg.image.load(path.join(self.map_folder, minimap_name)).convert_alpha()
            self.minimap = pg.transform.scale(self.minimap, (WIDTH//3, HEIGHT//3))
        
        with open(path.join(self.map_folder, tp_name), 'rt') as f:
            #   destinations is a dict mapping each tilemap teleport coordinate to
            #   the destination tilemap coordinate
            self.destinations = eval(f.read())

        self.grid= OccupancyGrid(self, path.join(self.map_folder, grid_name)) #down here because it needs destinations
        self.graph = self.grid.make_graph()

    def new(self):
        """
        Initialize and setup a new maze level.
        """
        #groups for drawing
        self.moving_sprites = pg.sprite.LayeredUpdates() 
        self.static_sprites = pg.sprite.LayeredUpdates()
        #other groups
        self.walls = pg.sprite.Group()
        self.teleports = pg.sprite.Group() 
        self.win = pg.sprite.Group() 
        self.threat = pg.sprite.Group()
        self.hearts= pg.sprite.Group()
        
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "monster":
                self.monster = Monster(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "mirror":
                Mirror(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, self.destinations)
            if tile_object.name == "pentagram":
                self.goal=Pentagram(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)

        self.flashlight=Flashlight(self, int(WIDTH/2), int(HEIGHT/2))
        for i in range (3):
            Heart(self, 726-37*(2-i), 20)
        self.dark=Darkness(self, int(WIDTH/2), int(HEIGHT/2))
        self.draw_debug = False
        
    def run(self):
        """
        Runs the Mazescape game.
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
                    menu.paused = True
                    menu.pause_menu() #code gets stuck in this call until a button is pressed in the pause menu
                    self.clock=pg.time.Clock()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

        #   win condition
        if pg.sprite.spritecollide(self.player, self.win, False, collide_hit_rect):
            menu.win_menu()

        #got hit condition
        if pg.sprite.spritecollide(self.player, self.threat, False, collide_hit2_rect):
            self.hit()

        self.portal(self.player)
        self.portal(self.monster)
    
    def hit(self):
        self.player.health-=DAMAGE
        for heart in self.hearts:
            heart.dissolve=True
            break
        if self.player.health<=0:
            self.lost=True
        else:
            self.attack_sequence()
            self.transmit(self.player)
 

    def transmit(self, p):
        while True:
            possible_loc=(randint(0, self.grid.tile_width-1), randint(0, self.grid.tile_height-1))
            if possible_loc in self.graph and distance(possible_loc, self.goal.pt)>20 and distance(possible_loc, (round(self.monster.pos[0]/TILESIZE), round(self.monster.pos[1]/TILESIZE)))>10:
                p.pos.x=possible_loc[0]*TILESIZE
                p.pos.y=possible_loc[1]*TILESIZE
                p.hit_rect.centerx= int(p.pos.x)
                p.hit_rect.centery= int(p.pos.y)
                p.rect.center=p.hit_rect.center
                return


    def portal(self, sprite):
        #   teleportation
        tel_block_hit = pg.sprite.spritecollide(sprite, self.teleports, False)
        if tel_block_hit:
            #   Find the other teleport block
            destination_x, destination_y = tel_block_hit[0].tp_x, tel_block_hit[0].tp_y
            sprite.pos.x = (destination_x+self.offset_x) * TILESIZE
            sprite.pos.y = (destination_y+self.offset_y) * TILESIZE

            sprite.hit_rect.centerx= int(sprite.pos.x)
            sprite.hit_rect.centery= int(sprite.pos.y)
            sprite.rect.center=sprite.hit_rect.center

            if sprite.name=='player':
                self.player.pause=PAUSE_DURATION # 2 second wait time
                self.player.image=self.player.grey_map[0]

            if sprite.name=='monster':
                sprite.generate_path()


    def update(self):
        """
        Updates the frame of the game
        """
        self.moving_sprites.update() 
        self.static_sprites.update()
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
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        #   Layer player and monsters on map
        for sprite in self.moving_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(sprite.hit_rect), 1)
        
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(wall.rect), 1)
            for mirror in self.teleports:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(mirror.rect), 1)
            for goal in self.win:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(goal.rect), 1)
            dest=(self.monster.next_step[0]*TILESIZE, self.monster.next_step[1]*TILESIZE)
            next_step=pg.Rect(0, 0, 20, 20)
            next_step.center=dest
            pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(next_step), 1)
            
        for sprite in self.static_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        # # # #   Reduce vision of the map
        # for r in range(VISION_RADIUS, 475):
        #     pg.draw.circle(self.screen, BLACK, (int(WIDTH/2), int(HEIGHT/2)), r, 1)


        #   Layer on the minimap if in mode 1
        if self.mode == '1':
            self.screen.blit(self.minimap, [10, 10])

        if self.lost:
            self.losing_sequence()
        
        pg.display.flip() #update the full display surface to the screen

    def draw_text(self, text, font, color, surface, x, y): #use for narrative in end sequence
        """
        Draws text onto a given surface.

        Args:
            text (str): non-empty text to display
            font (Font): the font to display the text in
            surface (Surface): the surface to display text on
            x (int): the top left x-coordinate for the text
            y (int): the top left y-coordinate for the text
        """
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def beginning_sequence(self):
        pass

    def losing_sequence(self):
        self.draw_text("You died", pg.font.SysFont('Arial', 60, 'bold'), DARKRED, self.screen, self.camera.apply(self.player).centerx+10, self.camera.apply(self.player).centery)
        pg.display.flip()
        time.sleep(3)
        menu.run_menu()

    def attack_sequence(self):
        pass

def run_game(mode):
    #create game
    g= Game(mode)
    while True:
        g.new()
        g.beginning_sequence()
        g.run()

#   Music
pg.init()
# pg.mixer.music.load(MUSIC_FILE)
# pg.mixer.music.play(-1)
#   Run Game
menu.game_function = run_game
menu.run_menu()
