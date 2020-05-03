'''Sprites'''
import pygame as pg
from settings import *
from os import path
from tilemap import collide_hit_rect
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
        self.vel = vec(0, 0)
        self.pos = vec(x, y) #* TILESIZE
        self.counter=0
        self.step=1

        #images
        left_w1=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_LEFT_WALK1)).convert_alpha()
        left_still=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_LEFT_STILL)).convert_alpha()
        left_w2=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_LEFT_WALK2)).convert_alpha()
        right_w1=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_RIGHT_WALK1)).convert_alpha()
        right_still=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_RIGHT_STILL)).convert_alpha()
        right_w2=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_RIGHT_WALK2)).convert_alpha()
        up_w1=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_BACK_WALK1)).convert_alpha()
        up_still=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_BACK_STILL)).convert_alpha()
        up_w2=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_BACK_WALK2)).convert_alpha()
        down_w1=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_FRONT_WALK1)).convert_alpha()
        down_still=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_FRONT_STILL)).convert_alpha()
        down_w2=pg.image.load(path.join(self.game.sprite_folder, PLAYER_IMG_FRONT_WALK2)).convert_alpha()
        self.img_map={'left':{0:left_w1, 1:left_still, 2:left_w2},
                    'right':{0:right_w1, 1:right_still, 2:right_w2},
                    'up':{0:up_w1, 1:up_still, 2:up_w2},
                    'down':{0:down_w1, 1:down_still, 2:down_w2}}

        self.image = down_still
        self.rect = self.image.get_rect()
        self.hit_rect=PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center


    def get_keys(self):
        self.vel = vec(0, 0)
        keys=pg.key.get_pressed()
        self.counter+=1
        if self.counter%10==0:
            self.step+=1
        if self.step==3:
            self.step=0
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.image = self.img_map['down'][self.step]
            self.vel.y = PLAYERSPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.image = self.img_map['up'][self.step]
            self.vel.y = -PLAYERSPEED
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.image = self.img_map['left'][self.step]
            self.vel.x = -PLAYERSPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.image = self.img_map['right'][self.step]
            self.vel.x = PLAYERSPEED
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071 #pythagorean theorem if it was v speed in one direction and you want to break it up into x and y; ensures diagonal speed isnt too fast

    def collide_wall(self, dir):
        """
        Handles collisions between the Player sprite and Wall Sprite. 
        Updates the pixel location of the player sprite.

        Args:
            dir (str): direction of the sprite collisions, either "x" or "y"
        """
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0: #if moving to the right during collision
                    self.pos.x = hits[0].rect.left - self.hit_rect.width/2 #put our left hand corner to the left hand corner of the object we hit and shift ourselves outside of tht object
                if self.vel.x < 0: #if moving to the left during collision
                    self.pos.x = hits[0].rect.right + self.hit_rect.width/2 # put our left hand corner to the right hand corner
                self.vel.x = 0 #redundant
                # print("hyuck")
                self.hit_rect.centerx = self.pos.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0: #if moving down during collision
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2 
                if self.vel.y < 0: #if moving up during collision
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0 #redundant
                # print("hyuck")
                self.hit_rect.centery = self.pos.y

    def update(self):
        """
        Updates the x and y pixel coordinates of the player
        based on the velocities.
        """
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect=self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.collide_wall('x')
        self.hit_rect.centery = self.pos.y
        self.collide_wall('y') 
        self.rect.center = self.hit_rect.center


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups= game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 

class Pentagram(pg.sprite.Sprite):
 
    def __init__(self, game, x, y, w, h):
        self.groups= game.win
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 

class Mirror(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, destinations):
        self.groups = game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 
        print(x,y)
        print(destinations)
        self.tp_x, self.tp_y = destinations[(int(self.rect.x/TILESIZE), int(self.rect.y/TILESIZE))] #destination pt

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

