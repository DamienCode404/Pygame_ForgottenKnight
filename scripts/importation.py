import pygame

from os import walk
from csv import reader
from scripts.parameters import block_size

def import_folder(path):
    for information in walk(path):
        print(information)

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / block_size)
    tile_num_y = int(surface.get_size()[1] / block_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * block_size
            y = row * block_size
            new_surf = pygame.Surface((block_size, block_size))
            new_surf.blit(surface, (0, 0), pygame.Rect(x,y,block_size, block_size))
            cut_tiles.append(new_surf)
            
    return cut_tiles

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x, y))
        
    def update(self, shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface, name = None):
        super().__init__(size, x, y)
        self.static_x = x
        self.static_y = y
        self.image = surface
        self.image.set_colorkey((0,0,0))
        self.name = name

    def update(self, player_position_x):
        self.rect.x = self.static_x - player_position_x
        #self.rect.y = self.static_y - player_position_y