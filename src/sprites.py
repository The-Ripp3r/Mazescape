'''Sprites'''
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        #coordinates on the grid
        #x, y represent the top left hand corner of the image obj that is being drawn
        self.vx = 0
        self.vy = 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYERSPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYERSPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYERSPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYERSPEED
        if self.vx!=0 and self.vy!=0:
            self.vx *= 0.7071 #pythagorean theorem if it was v speed in one direction and you want to break it up into x and y; ensures diagonal speed isnt too fast
            self.vy *= 0.7071

    def collide(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0: #if moving to the right during collision
                    self.x = hits[0].rect.left - self.rect.width #put our left hand corner to the left hand corner of the object we hit and shift ourselves outside of tht object
                if self.vx < 0: #if moving to the left during collision
                    self.x = hits[0].rect.right # put our left hand corner to the right hand corner
                self.vx = 0 #redundant
                self.rect.x = self.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0: #if moving down during collision
                    self.y = hits[0].rect.top - self.rect.height 
                if self.vy < 0: #if moving up during collision
                    self.y = hits[0].rect.bottom 
                self.vy = 0 #redundant
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x 
        self.collide('x')
        self.rect.y = self.y
        self.collide('y') 

        # #win condition
        # if pg.sprite.spritecollide(self, self.game.win, False):
        #     self.game.quit_game()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups= game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups= game.all_sprites, game.win
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE