'''Sprites'''
import pygame as pg
from settings import *
import math
import heapdict
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
        self.counter=0 #counts frames
        self.step=1 #switch for images
        self.name="player"

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
        self.rect.center=(x,y)
        self.hit_rect=PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center


    def get_keys(self):
        self.vel = vec(0, 0)
        keys=pg.key.get_pressed()
        self.counter+=1
        if self.counter%10==0: #every 10 frames
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
                self.hit_rect.centerx = self.pos.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0: #if moving down during collision
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2 
                if self.vel.y < 0: #if moving up during collision
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0 #redundant
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



class Monster(pg.sprite.Sprite):
    
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.threat
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vel = vec(0, 0)
        self.pos = vec(x, y) 
        self.counter=0
        self.step=1
        self.name="monster"

        #images
        left_w1=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_LEFT_WALK1)).convert_alpha()
        left_still=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_LEFT_STILL)).convert_alpha()
        left_w2=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_LEFT_WALK2)).convert_alpha()
        right_w1=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_RIGHT_WALK1)).convert_alpha()
        right_still=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_RIGHT_STILL)).convert_alpha()
        right_w2=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_RIGHT_WALK2)).convert_alpha()
        up_w1=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_BACK_WALK1)).convert_alpha()
        up_still=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_BACK_STILL)).convert_alpha()
        up_w2=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_BACK_WALK2)).convert_alpha()
        down_w1=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_FRONT_WALK1)).convert_alpha()
        down_still=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_FRONT_STILL)).convert_alpha()
        down_w2=pg.image.load(path.join(self.game.sprite_folder, MONSTER_IMG_FRONT_WALK2)).convert_alpha()
        self.img_map={'left':{0:left_w1, 1:left_still, 2:left_w2},
                    'right':{0:right_w1, 1:right_still, 2:right_w2},
                    'up':{0:up_w1, 1:up_still, 2:up_w2},
                    'down':{0:down_w1, 1:down_still, 2:down_w2}}

        self.image = down_still
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.hit_rect=MONSTER_HIT_RECT
        self.hit_rect.center = self.rect.center

        #path
        self.path={}
        self.next_step=()

        #buttons
        self.left=False
        self.right=False
        self.up=False
        self.down=False

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
                self.hit_rect.centerx = self.pos.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0: #if moving down during collision
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2 
                if self.vel.y < 0: #if moving up during collision
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0 #redundant
                self.hit_rect.centery = self.pos.y

    def heuristic(self, p0, p1):
        '''
        Heuristic used in A*
        Calculates Euclidian two points; currently used between p pt and self.goal
        '''
        #distance from pt to goal
        #will later change to dubin curve to return val and new orientation
        return math.sqrt((p1[0]-p0[0])**2 + (p1[1]-p0[1])**2)

    def get_closest_free_square(self, sprite):
        current=(sprite.pos.x/TILESIZE, sprite.pos.y/TILESIZE)
        
        reference=(round(current[0]), round(current[1]))
        d={}
        for x_prime in range(-1,2):
            for y_prime in range(-1,2):
                possible_loc=(reference[0]+x_prime, reference[1]+y_prime)
                if possible_loc in self.game.graph:
                    d[possible_loc]=self.heuristic(current, possible_loc)
        
        if len(d)==0:
            print("SHOULD NEVER HAPPEN")
            print(current)
            print(sprite.name)
            return reference  

        return min(d, key=d.get)



    def generate_path(self):
        '''
        A* algorithm that returns a reverse parent dictionary
        ''' 

        start=self.get_closest_free_square(self) #current monster location
        goal=self.get_closest_free_square(self.game.player) #players location

        distance = {start:0} #keeps track of shortest distance
        h = {} #keeps of track heuristic values
        parent = {} #map from node to parent node; reconstruct with this starting from goal pt
        visited = {} #make sure we dont revist nodes
        unvisited = heapdict.heapdict()#queue is ordered by f(n) = g(n) (distance from start node to current node) + h(n) (some heuristic) 

        current = start
        while current != goal:
            for neighbor in self.game.graph[current]:
                #look at unvisited neighbors 
                if neighbor not in visited:
                    val = distance[current] + self.heuristic(current, neighbor) #this is all euclidian distance; distance from start to neighbor
                    if neighbor not in distance:
                        distance[neighbor] = float('inf') #this is much faster than d.get(key, default), inside in case we dont reach certain points
                    if val<distance[neighbor]: #update
                        #need to update queue too; just add it or replace current value in queue with f(n)
                        if neighbor not in h:
                            h[neighbor] = self.heuristic(neighbor, goal) #straight line distance
                            # later use dubin curves and store oritentation as well, this is 
                        unvisited[neighbor] = val + h[neighbor] #could potentially store heuristic vals separately
                        distance[neighbor] = val 
                        parent[neighbor] = current #we found a new "shortest distance" with our current node so update parent

            visited[current] = True #update visited; i think this order is right
            current = unvisited.popitem()[0]
        
        #reverse the parent dictionary into self.path
        pt = goal
        path = {}
        while pt != start:
            child = parent[pt]
            path[child]=pt
            pt=child

        self.path=path
        self.path[goal]=goal #for when the monster reaches the player
        self.next_step=self.path[start]

    def get_keys(self):
        self.vel = vec(0, 0)
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        current_location = self.get_closest_free_square(self)
        
        self.counter+=1
        if self.counter%10==0: #every 10 frames
            self.step+=1
        if self.step==3:
            self.step=0
        
        if current_location==self.next_step:
            self.next_step=self.path[self.next_step]

        if current_location[0]-self.next_step[0]<0:
            self.right=True
        if current_location[0]-self.next_step[0]>0:
            self.left=True

        if current_location[1]-self.next_step[1]<0:
            self.down=True
        if current_location[1]-self.next_step[1]>0:
            self.up=True

        if self.down:
            #print("down")
            self.image = self.img_map['down'][self.step]
            self.vel.y = MONSTERSPEED
        if self.up:
            #print("up")
            self.image = self.img_map['up'][self.step]
            self.vel.y = -MONSTERSPEED
        if self.left:
            #print("left")
            self.image = self.img_map['left'][self.step]
            self.vel.x = -MONSTERSPEED
        if self.right:
            #print("right")
            self.image = self.img_map['right'][self.step]
            self.vel.x = MONSTERSPEED
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        """
        Updates the x and y pixel coordinates of the player
        based on the velocities.
        """
        #make path every 100 frames or something
        if self.counter%100==0:
            print('generating')
            print(self.counter)
            self.generate_path()
            print("finished")
        
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
        # print(x,y)
        # print(destinations)
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

