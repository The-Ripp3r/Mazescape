''''''
import pygame as pg
import pytmx
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    """
    Represents a map of the maze in Mazescape.

    Attributes:
        wall_locs (dict): maps tilemap coordinates of walls to True
        teleport_locs (dict): maps tilemap coordinates of teleports to True
        player_loc (tuple): tilemap coordinates of the player sprite
        goal (tuple): tilemap coordinates of the goal sprite
        tile_height (int): the number of tilemap rows in the map
        width (int): the pixel width of the map
        height (int): the pixel height of the map
    """
    def __init__(self, filename):
        self.floor_locs = {}
        self.wall_locs = {}
        self.teleport_locs = {}
        self.player_loc = (SPAWN_X, SPAWN_Y)
        with open(filename, 'rt') as f:
                #loads map file and stores wall locations and player location
            row = 0
            for line in f:
                col = 0
                for tile in line:
                    if tile == "1":
                        self.wall_locs[col, row] = True
                    if tile == ".":
                        self.floor_locs[col, row] = True
                    if tile == "P":
                        self.player_loc = (col, row)   
                    if tile == "G":
                        self.goal = (col, row) 
                    if tile == "T":
                        self.teleport_locs[col, row] = True
                    col += 1
                self.tile_width = col
                row += 1
        
        self.tile_height = row
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE


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
        self.tile_width=len(self.grid[0])-1
        self.tile_height=len(self.grid)
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE

    
    def make_graph(self):
        graph={}
        for r in range(self.tile_height):
            for c in range(self.tile_width):
                if self.grid[r][c]==0:
                    #init
                    if (c,r) not in graph:
                        graph[(c,r)]=set()
                    #look at neighbors
                    for r_prime in range(-1, 2): #possible remove diagonals
                        for c_prime in range(-1, 2):
                            if r+r_prime<0 or c+c_prime<0 or r+r_prime>len(self.grid) or c+c_prime>len(self.grid[0]):
                                continue
                            if self.grid[r+r_prime][c+c_prime]==0:
                                if (c,r)!=(c+c_prime, r+r_prime):
                                    if c_prime==r_prime:
                                        continue
                                        # if c_prime<0 and r_prime<0: #top left
                                        #     if self.grid[r][c-1]==0 and self.grid[r-1][c]==0:
                                        #         graph[(c,r)].add((c+c_prime, r+r_prime))
                                        # if c_prime>0 and r_prime<0: #top right
                                        #     if self.grid[r][c+1]==0 and self.grid[r-1][c]==0:
                                        #         graph[(c,r)].add((c+c_prime, r+r_prime))
                                        # if c_prime<0 and r_prime>0: #bottom left
                                        #     if self.grid[r][c-1]==0 and self.grid[r+1][c]==0:
                                        #         graph[(c,r)].add((c+c_prime, r+r_prime))
                                        # if c_prime>0 and r_prime>0: #bottom right
                                        #     if self.grid[r+1][c]==0 and self.grid[r][c+1]==0:
                                        #         graph[(c,r)].add((c+c_prime, r+r_prime))
                                    else:
                                        graph[(c,r)].add((c+c_prime, r+r_prime))

        #add teleports
        for teleport in self.game.destinations:
            s=(teleport[0]+self.game.offset_x, int(teleport[1]+self.game.offset_y-1))
            e=(self.game.destinations[teleport][0]+self.game.offset_x, int(self.game.destinations[teleport][1]+self.game.offset_y-1))
            graph[s].add(e)
        
        return graph