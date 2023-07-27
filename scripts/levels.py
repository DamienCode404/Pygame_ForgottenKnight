import pygame
from os.path import join
from scripts.importation import *
from scripts.parameters import block_size, FULLSCREEN_HEIGHT

level_0 = {
    'terrain': 'levels/0/level_0_terrain.csv',
    'coins': 'levels/0/level_0_coins.csv',
    'lamp': 'levels/0/level_0_lamp.csv',
    'player': 'levels/0/level_0_player.csv',
    'shop': 'levels/0/level_0_shop.csv'}

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        
        # terrain 
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain', 3)
        
        # coins
        # coins_layout = import_csv_layout(level_data['coins'])
        # self.coins_sprites = self.create_tile_group(coins_layout, 'coins')        
            
            
    def create_tile_group(self, layout, type, resize = 1):
        sprite_group = pygame.sprite.Group()
        resize_offset_y = FULLSCREEN_HEIGHT - (block_size * resize * len(layout))
        print(resize_offset_y)

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * block_size * resize
                    y = resize_offset_y + (row_index * block_size * resize)

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('assets/terrain/oak_woods_tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        tile_surface = pygame.transform.scale(tile_surface, (block_size*resize, block_size*resize))                        
                        sprite = StaticTile(block_size, x, y, tile_surface, 'terrain')
                        
                    # if type == 'coins':
                    #     coins_tile_list = import_cut_graphics('assets/coins/MonedaD.png')
                    #     tile_surface = coins_tile_list[int(val)]
                    #     sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    sprite_group.add(sprite)

        return sprite_group
                                            
    def run(self, offset_x):
        # terrain
        x_shift = self.world_shift - offset_x
        self.world_shift = offset_x

        self.terrain_sprites.update(x_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # lamp
        # self.coins_sprites.draw(self.display_surface)
        # self.coins_sprites.update(self.world_shift)

def get_block(size):
    path = join("assets", "terrain", "oak_woods_tileset.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(24, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(surface, (250, 80))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
