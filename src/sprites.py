'''Sprites'''
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """
    Represents the main player sprite in Mazescape.

    Attributes:
        groups (Group): the sprite group container classes Player is part of
        game (Game): the game Player is part of
        image (Surface): the image of the Player sprite
        rect (Rect): a Rect object representing the Player sprite
        vx (float): the x direction velocity of the player object in the game in pixels 
            per second, where >0 means to the right
        vy (float): the y direction velocity of the player object in the game in pixels
            per second, where >0 means upwards
        x (float): the x pixel location of the player sprite
        y (float): the y pixel locaiton of the player sprite
    """
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
        """
        Handles collisions between the Player sprite and Wall Sprite. 
        Updates the pixel location of the player sprite.

        Args:
            dir (str): direction of the sprite collisions, either "x" or "y"
        """
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
        """
        Updates the x and y pixel coordinates of the player
        based on the velocities.
        """
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
    """
    Represents a wall sprite of a maze in Mazescape.

    Attributes:
        groups (Group): the sprite group container classes Wall is part of
        game (Game): the game Wall is part of
        image (Surface): the image of the Wall sprite
        rect (Rect): a Rect object representing the Wall sprite
        x (float): the x pixel location of the wall sprite
        y (float): the y pixel locaiton of the wall sprite
    """
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
    """
    Represents a Teleport sprite of a maze in Mazescape.

    Attributes:
        groups (Group): the sprite group container classes Teleport is part of
        game (Game): the game Teleport is part of
        image (Surface): the image of the Teleport sprite
        rect (Rect): a Rect object representing the Teleport sprite
        x (float): the x pixel location of the Teleport sprite
        y (float): the y pixel locaiton of the Teleport sprite
    """
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
            #   destinations is a dict mapping each tilemap teleport coordinate to
            #   the destination tilemap coordinate
            destinations = eval(f.read())
            self.tp_x, self.tp_y = destinations[(self.rect.x/TILESIZE, self.rect.y/TILESIZE)] #destination pt

class Goal(pg.sprite.Sprite):
    """
    Represents a Goal sprite of a maze in Mazescape.

    Attributes:
        groups (Group): the sprite group container classes Goal is part of
        game (Game): the game Goal is part of
        image (Surface): the image of the Goal sprite
        rect (Rect): a Rect object representing the Goal sprite
        x (float): the x pixel location of the Goal sprite
        y (float): the y pixel locaiton of the Goal sprite
    """
    def __init__(self, game, x, y):
        self.groups= game.all_sprites, game.win
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
