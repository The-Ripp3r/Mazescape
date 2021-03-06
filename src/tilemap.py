''''''
import pygame as pg
import pytmx
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_hit2_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        tmp_surface=pg.Surface((self.width, self.height))
        self.render(tmp_surface)
        return tmp_surface

class Camera:
    """
    Represents a camera, which is the view the player sprite has of the map on the screen. 
    The idea here is to draw the map/drawing offset from the screen so that the screen 
    is always fixed on the player.

    Attributes:
        camera (Rect): the camera view with the specified pixel width/height
        width (int): pixel width of the camera
        height (int): pixel height of the camera
    """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width #map width
        self.height = height #map height
    

    def update(self, target):
        """
        Updates the Rect position of the camera. Remember camera keeps track of the offset 
        as its location so the camera is the opposite of player movement.
        """
        #remember the camera doesnt move in respect to the world
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        self.camera = pg.Rect(x, y, self.width, self.height)


    def apply(self, entity):
        """
        Updates an entity's Rect position based on where the Camera is located

        Args:
            entity (Sprite): the sprite to update the location for
        
        Returns:
            A Rect, which is a new rectangle that is moved by the offset of
            self.camera.topleft. It doesnt change the old one
        """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect): #made for map bc it is not a sprite
        return rect.move(self.camera.topleft)


class OccupancyGrid:
    def __init__(self, game, filename):
        self.game=game 
        self.grid=[]
        #make python occupancy grid
        with open(filename, 'rt') as f:
                #loads map file and stores wall locations and player location
            for line in f:
                row=[]
                for tile in line:
                    if tile=='0' or tile=='1':
                        row.append(int(tile))
                self.grid.append(row)
        self.tile_width=len(self.grid[0])
        self.tile_height=len(self.grid)
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE

    
    def make_graph(self):
        graph={}
        #generate nodes
        for r in range(self.tile_height):
            for c in range(self.tile_width):
                if self.grid[r][c]==0:
                    count=0
                    #special case of top three in corner; look at txt file and try and eliminate corners
                    for r_prime in range(-1,1):
                        for c_prime in range(-1,1):
                            if r+r_prime<0 or c+c_prime<0 or r+r_prime>len(self.grid) or c+c_prime>len(self.grid[0]):
                                continue
                            if self.grid[r+r_prime][c+c_prime]==0:
                                count+=1
                    
                    if count==4:
                        graph[(c,r)]=set()

        #generate edges
        for valid_node in graph:
            for r_prime in range(-1, 2): #possible remove diagonals
                for c_prime in range(-1, 2):
                    # if c_prime==r_prime:
                    #     continue
                    possible_neighbor=(valid_node[0]+c_prime, valid_node[1]+r_prime)
                    if possible_neighbor in graph:
                        graph[valid_node].add(possible_neighbor)


        #add teleports
        for teleport in self.game.destinations:
            s=(teleport[0]+self.game.offset_x, int(teleport[1]+self.game.offset_y-1))
            e=(self.game.destinations[teleport][0]+self.game.offset_x, int(self.game.destinations[teleport][1]+self.game.offset_y-1))
            graph[s].add(e)
            
        return graph