'''Sprites'''
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
    

    def get_keys(self):
        self.vel = vec(0, 0)
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYERSPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYERSPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYERSPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYERSPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071 #pythagorean theorem if it was v speed in one direction and you want to break it up into x and y; ensures diagonal speed isnt too fast

    def collide(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0: #if moving to the right during collision
                    self.pos.x = hits[0].rect.left - self.rect.width #put our left hand corner to the left hand corner of the object we hit and shift ourselves outside of tht object
                if self.vel.x < 0: #if moving to the left during collision
                    self.pos.x = hits[0].rect.right # put our left hand corner to the right hand corner
                self.vel.x = 0 #redundant
                self.rect.x = self.pos.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0: #if moving down during collision
                    self.pos.y = hits[0].rect.top - self.rect.height 
                if self.vel.y < 0: #if moving up during collision
                    self.pos.y = hits[0].rect.bottom 
                self.vel.y = 0 #redundant
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide('x')
        self.rect.y = self.pos.y
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
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y, filename):
        self.groups = game.all_sprites, game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        with open(filename, 'rt') as f:
            destinations = eval(f.read())
            self.tp_x, self.tp_y = destinations[(self.rect.x/TILESIZE, self.rect.y/TILESIZE)] #destination pt

class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups= game.all_sprites, game.win
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE