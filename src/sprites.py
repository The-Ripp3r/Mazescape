'''Sprites'''
import pygame as pg
from settings import *
import math
import heapdict
from os import path
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def distance(p0, p1):
    '''
    Heuristic used in A*
    Calculates Euclidian two points; currently used between p pt and self.goal
    '''
    #distance from pt to goal
    #will later change to dubin curve to return val and new orientation
    return math.sqrt((p1[0]-p0[0])**2 + (p1[1]-p0[1])**2)


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
        self._layer=PLAYER_LAYER
        self.groups = game.moving_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vel = vec(0, 0)
        self.pos = vec(x, y) #* TILESIZE
        self.frame_counter=0 #counts frames
        self.image_counter=1 #switch for images
        self.flicker_image_counter=True
        self.pause=0 #used to pause the player after teleports
        self.pause_transition=0 #0 for mirror, 1 for damage
        self.direction=None #used for flicker animations
        self.name="player"
        self.health=PLAYERHEALTH
        self.dir = None #current direction of player

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

        #teleport images
        teleport_back=pg.image.load(path.join(self.game.sprite_folder, PLAYER_TELEPORT_BACK_STILL)).convert_alpha()
        hurt_right=pg.image.load(path.join(self.game.sprite_folder, PLAYER_HURT_RIGHT)).convert_alpha()
        hurt_left=pg.image.load(path.join(self.game.sprite_folder, PLAYER_HURT_LEFT)).convert_alpha()
        hurt_up=pg.image.load(path.join(self.game.sprite_folder, PLAYER_HURT_UP)).convert_alpha()
        hurt_down=pg.image.load(path.join(self.game.sprite_folder, PLAYER_HURT_DOWN)).convert_alpha()
        self.flicker_map={0:{0:teleport_back, 1:up_still}, 1:{'right':{0:hurt_right, 1:right_still}, 
        'left':{0:hurt_left, 1:left_still}, 
        'up':{0:hurt_up, 1:up_still}, 
        'down':{0:hurt_down, 1:down_still}
            }
        }

        self.image = down_still
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.hit_rect=PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center


    def get_keys(self):
        self.vel = vec(0, 0)
        keys=pg.key.get_pressed()
        self.frame_counter+=1
        if self.frame_counter%10==0: #every 10 frames
            self.image_counter+=1
        if self.image_counter==3:
            self.image_counter=0
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.image = self.img_map['down'][self.image_counter]
            self.vel.y = PLAYERSPEED
            self.dir = 'down'
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.image = self.img_map['up'][self.image_counter]
            self.vel.y = -PLAYERSPEED
            self.dir = 'up'
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.image = self.img_map['left'][self.image_counter]
            self.vel.x = -PLAYERSPEED
            self.dir = 'left'
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.image = self.img_map['right'][self.image_counter]
            self.vel.x = PLAYERSPEED
            self.dir = 'right'
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071 #pythagorean theorem if it was v speed in one direction and you want to break it up into x and y; ensures diagonal speed isnt too fast

    def collide_wall(self, dir):
        """
        Handles collisions between the Player sprite and Wall Sprite. 
        Updates the pixel location of the player sprite.

        Args:
            dir (str): direction of the sprite collisions, either "x" or "y"
        """

        moving_against_wall=False

        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > self.hit_rect.centerx: #if moving to the right during collision
                    moving_against_wall=True
                    self.pos.x = hits[0].rect.left - self.hit_rect.width/2 #put our left hand corner to the left hand corner of the object we hit and shift ourselves outside of tht object
                if hits[0].rect.centerx < self.hit_rect.centerx: #if moving to the left during collision
                    moving_against_wall=True
                    self.pos.x = hits[0].rect.right + self.hit_rect.width/2 # put our left hand corner to the right hand corner
                self.vel.x = 0 #redundant
                self.hit_rect.centerx = self.pos.x

        if dir == "y": #analgous to x case
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centery > self.hit_rect.centery: #if moving down during collision
                    moving_against_wall=True
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2 
                if hits[0].rect.centery < self.hit_rect.centery: #if moving up during collision
                    moving_against_wall=True
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0 #redundant
                self.hit_rect.centery = self.pos.y

        if moving_against_wall:
            if not self.game.wall_channel.get_busy():
                self.game.wall_channel.play(self.game.wall_sound)

    def update(self):
        """
        Updates the x and y pixel coordinates of the player
        based on the velocities.
        """
        if self.pause>0:
            self.paused()
            return

        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect=self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.collide_wall('x')
        self.hit_rect.centery = self.pos.y
        self.collide_wall('y') 
        self.rect.center = self.hit_rect.center

    def draw_health(self):
        pass

    def paused(self):
        if self.direction!=None: 
            self.image=self.flicker_map[self.pause_transition][self.direction][0]
        else: 
            self.image=self.flicker_map[self.pause_transition][0]
        self.pause-=1
        if self.pause==0:
            self.flicker_image_counter=True
            if self.direction!=None: 
                self.image=self.flicker_map[self.pause_transition][self.direction][1]
            else: 
                self.image=self.flicker_map[self.pause_transition][1]
            self.direction=None #reset
        elif self.pause<=30:
            if self.pause%ANIMATION_FLICKER_SPEED==0:
                if self.direction!=None: 
                    self.image=self.flicker_map[self.pause_transition][self.direction][self.flicker_image_counter]
                else: 
                    self.image=self.flicker_map[self.pause_transition][self.flicker_image_counter]
                self.flicker_image_counter=not self.flicker_image_counter
                
        
class Monster(pg.sprite.Sprite):
    
    def __init__(self, game, x, y):
        self._layer=MONSTER_LAYER
        self.groups = game.moving_sprites, game.threat
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vel = vec(0, 0)
        self.pos = vec(x, y) 
        self.counter=0
        self.step=1
        self.name="monster"
        self.pause=0

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


    def monsterspeed(self):
        speed=max(MONSTERSPEED, MONSTERSPEED*(1+(((len(self.path)*32-MONSTER_BUBBLE_DISTANCE)/32)*0.04)))
        return speed

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


    def get_closest_free_square(self, sprite):
        current=(sprite.pos.x/TILESIZE, sprite.pos.y/TILESIZE)
        
        reference=(round(current[0]), round(current[1]))
        d={}
        for x_prime in range(-3,4):
            for y_prime in range(-3,4):
                possible_loc=(reference[0]+x_prime, reference[1]+y_prime)
                if possible_loc in self.game.graph:
                    d[possible_loc]=distance(current, possible_loc)
        
        if len(d)==0:
            return reference  

        return min(d, key=d.get)



    def generate_path(self):
        '''
        A* algorithm that returns a reverse parent dictionary
        ''' 

        start=self.get_closest_free_square(self) #current monster location
        goal=self.get_closest_free_square(self.game.player) #players location

        d = {start:0} #keeps track of shortest distance
        h = {} #keeps of track heuristic values
        parent = {} #map from node to parent node; reconstruct with this starting from goal pt
        visited = {} #make sure we dont revist nodes
        unvisited = heapdict.heapdict()#queue is ordered by f(n) = g(n) (distance from start node to current node) + h(n) (some heuristic) 

        current = start
        while current != goal:
            for neighbor in self.game.graph[current]:
                #look at unvisited neighbors 
                if neighbor not in visited:
                    val = d[current] + distance(current, neighbor) #this is all euclidian distance; distance from start to neighbor
                    if neighbor not in d:
                        d[neighbor] = float('inf') #this is much faster than d.get(key, default), inside in case we dont reach certain points
                    if val<d[neighbor]: #update
                        #need to update queue too; just add it or replace current value in queue with f(n)
                        if neighbor not in h:
                            h[neighbor] = distance(neighbor, goal) #straight line distance
                            # later use dubin curves and store oritentation as well, this is 
                        unvisited[neighbor] = val + h[neighbor] #could potentially store heuristic vals separately
                        d[neighbor] = val 
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
        #current_location = self.get_closest_free_square(self)
        current_location=self.pos
        dest=(self.next_step[0]*TILESIZE, self.next_step[1]*TILESIZE)

        self.counter+=1
        if self.counter%ANIMATION_WALKING_SPEED==0: #every 10 frames
            self.step+=1
        if self.step==3:
            self.step=0
        
        #if current_location==self.next_step:
        if distance(current_location, dest)<5:
            self.next_step=self.path[self.next_step]

        if current_location[0]-dest[0]<-2:
            self.right=True
        if current_location[0]-dest[0]>2:
            self.left=True

        if current_location[1]-dest[1]<-2:
            self.down=True
        if current_location[1]-dest[1]>2:
            self.up=True

        if self.down:
            self.image = self.img_map['down'][self.step]
            self.vel.y = self.monsterspeed()
        if self.up:
            self.image = self.img_map['up'][self.step]
            self.vel.y = -self.monsterspeed()
        if self.left:
            self.image = self.img_map['left'][self.step]
            self.vel.x = -self.monsterspeed()
        if self.right:
            self.image = self.img_map['right'][self.step]
            self.vel.x = self.monsterspeed()
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        """
        Updates the x and y pixel coordinates of the player
        based on the velocities.
        """
        if self.pause>0:
            self.pause-=1
            return

        #make path every 100 frames or something
        if self.counter%100==0:
            self.generate_path()
        
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
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 

class Pentagram(pg.sprite.Sprite):
 
    def __init__(self, game, x, y, w, h):
        self.groups= game.win
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 
        self.pt = (round(x/TILESIZE), round(y/TILESIZE))

class Mirror(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, destinations):
        self.groups = game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y 
        self.tp_x, self.tp_y = destinations[(int(self.rect.x/TILESIZE), int(self.rect.y/TILESIZE))] #destination pt

class Flashlight(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer=FLASHLIGHT_LAYER
        self.groups = game.static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images=[]
        filename = 'glow_v0.png'
        for i in range(10):
            img = pg.image.load(path.join(game.animation_folder, filename)).convert_alpha()
            if i<5:    
                img = pg.transform.scale(img, (400-10*i, 400))
            if i>=5:
                img = self.images[9-i]
            self.images.append(img)

        self.image=self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.frame=0
        self.frame_rate=10
        self.last_update=pg.time.get_ticks()
        self.on=True
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(self.images):
                self.frame=0
            center=self.rect.center
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            
class Darkness(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer=DARKNESS_LAYER
        self.groups = game.static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.visible= pg.image.load(path.join(game.animation_folder, "visible.png")).convert_alpha()
        self.blackout= pg.image.load(path.join(game.animation_folder, "darkness.png")).convert_alpha()
        self.image = self.visible
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.on=False

    def update(self):
        if self.on:
            self.image=self.blackout
        else:
            self.image=self.visible

class Heart(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer=HEART_LAYER
        self.groups = game.hearts, game.static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(path.join(game.sprite_folder, HEART_FILE)).convert_alpha()
        self.dissolve_images=[]
        for i in range(9):
            filename = 'dissolve_{}.png'.format(i)
            img = pg.image.load(path.join(game.animation_folder, filename)).convert_alpha()
            self.dissolve_images.append(img)

        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.dissolve=False
        self.frame=-1
        self.frame_rate=90
        self.last_update=pg.time.get_ticks()

    def update(self):
        if self.dissolve:
            now = pg.time.get_ticks()
            if now - self.last_update>self.frame_rate:
                self.last_update=now
                self.frame+=1
                if self.frame==len(self.dissolve_images):
                    self.kill()
                    return
                center=self.rect.center
                self.image = self.dissolve_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Minimap(pg.sprite.Sprite):
    def __init__(self, game, filename):
        self._layer=MINIMAP_LAYER
        self.groups = game.static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(path.join(game.map_folder, filename)).convert_alpha()
        self.image = pg.transform.scale(self.image, (WIDTH//3, HEIGHT//3))
        self.rect = self.image.get_rect()
        self.rect = MINIMAP_LOCATION

    def update(self):
        pass

class Battery(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BATTERY_LAYER
        self.groups = game.static_sprites
        self.game=game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = [] 
        for i in range(4):
            filename = 'battery_{}.png'.format(i)
            img = pg.image.load(path.join(game.animation_folder, filename)).convert_alpha()
            self.images.append(img)

        self.image=self.images[-1]
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.dissolve=False
        self.bars=3
        self.duration=BATTERY_DURATION
        self.last_update=pg.time.get_ticks()

    def update(self):
        if self.game.flashlight.on:        
            now = pg.time.get_ticks()
            if now - self.last_update>self.duration:
                self.last_update=now
                self.bars-=1
                center=self.rect.center
                self.image = self.images[self.bars]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.duration=BATTERY_DURATION
                if self.bars==0:
                    self.game.transition=True
                    self.game.darkness.on=True
                    self.game.darkness.image=self.game.darkness.blackout