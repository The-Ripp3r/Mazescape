'''Tilemap game'''
import sys
from os import path
import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250, 100)
        self.folder = path.dirname(__file__)
        self.wall_locs = {}
        self.player_loc = (1, 1)
        self.load_data()

    def load_data(self):
        #loads map file and stores wall locations and player location
        with open(path.join(self.folder, 'map.txt'), 'rt') as f:
            row = 0
            for line in f:
                col = 0
                for tile in line:
                    if tile == "1":
                        self.wall_locs[col, row] = True
                    if tile == "P":
                        self.player_loc = (col, row)    
                    col += 1
                row += 1

    def new(self):
        #init all vars and do all setup for a new game
        self.all_sprites = pg.sprite.Group() #a container class to hold multiple Sprite obj
        self.walls = pg.sprite.Group() #a container class to hold multiple Wall obj
        self.player = Player(self, self.player_loc[0], self.player_loc[1])
        for loc in self.wall_locs:
            Wall(self, loc[0], loc[1])


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
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                
    def update(self):
        self.all_sprites.update() #*************

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
      
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
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
