'''Tilemap game'''
import sys
from os import path
import pygame as pg
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # pg.key.set_repeat(250, 100)
        self.folder = path.dirname(__file__)
        self.load_data()

    def load_data(self):
        self.map = Map(path.join(self.folder, 'maps/research_map.txt'))

    def new(self):
        #init all vars and do all setup for a new game
        self.all_sprites = pg.sprite.Group() #a container class to hold multiple Sprite obj
        self.walls = pg.sprite.Group() #a container class to hold multiple Wall obj
        self.win = pg.sprite.Group() #a container class to hold win conditions
        self.player = Player(self, self.map.player_loc[0], self.map.player_loc[1])
        self.goal = Goal(self, self.map.goal[0], self.map.goal[1])
        for loc in self.map.wall_locs:
            Wall(self, loc[0], loc[1])
        
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        #game loop set self.playing to False to end game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit_game(self):
        pg.quit()
        sys.exit()

    def events(self):
        #catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit_game()

        #win condition
        if pg.sprite.spritecollide(self.player, self.win, False):
            self.quit_game()
                
    def update(self):
        self.all_sprites.update() #*************
        self.camera.update(self.player)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
      
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for r in range(VISION_RADIUS, 600):
            pg.draw.circle(self.screen, BLACK, (int(WIDTH/2), int(HEIGHT/2)), r, 1)
        pg.display.flip() #update the full display surface to the screen



    def show_start_screen(self):
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
