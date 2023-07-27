import sys
import os
from os import walk
from csv import reader
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Forgotten Knight")
# pygame.display.set_icon(pygame.load.image("assets/"))

info = pygame.display.Info()
FULLSCREEN_WIDTH = info.current_w
FULLSCREEN_HEIGHT = info.current_h

FPS = 60
PLAYER_VEL = 8

block_size = 24

window = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))

level_0 = {
    'terrain': 'levels/0/level_0_terrain.csv',
    'coins': 'levels/0/level_0_coins.csv',
    'lamp': 'levels/0/level_0_lamp.csv',
    'player': 'levels/0/level_0_player.csv',
    'shop': 'levels/0/level_0_shop.csv'}

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, width, height, direction=False):
    path = join("assets", dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface, (450, 300))) # Resize character in game
            
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites


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
        self.image = surface
        self.name = name

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        
        # terrain 
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # coins
        # coins_layout = import_csv_layout(level_data['coins'])
        # self.coins_sprites = self.create_tile_group(coins_layout, 'coins')        
            
            
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * block_size
                    y = row_index * block_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('assets/terrain/oak_woods_tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(block_size, x, y, tile_surface)
                        
                    # if type == 'coins':
                    #     coins_tile_list = import_cut_graphics('assets/coins/MonedaD.png')
                    #     tile_surface = coins_tile_list[int(val)]
                    #     sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    sprite_group.add(sprite)

        return sprite_group
                                            
    def run(self):
        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
        # lamp
        # self.coins_sprites.draw(self.display_surface)
        # self.coins_sprites.update(self.world_shift)

level = Level(level_0, window)

def get_block(size):
    path = join("assets", "terrain", "oak_woods_tileset.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(24, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(surface, (250, 80))


class Player(pygame.sprite.Sprite):
    # Redimensionner le personnage in game
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("animation", 120, 80, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.attack = False
        self.attack_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def attacking(self):
        self.attack = True
        self.attack_count += 1
        self.animation_count = 0
    
    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "_Idle"
        if self.hit:
            sprite_sheet = "_Hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "_Jump"
            else:
                sprite_sheet = "_Roll" # Faire en sorte que l'animation se termine avant "_Fall"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "_Fall"
        elif self.x_vel != 0:
            sprite_sheet = "_Run"
        elif self.attack:
            if self.attack_count % 2 == 0:
                sprite_sheet = "_Attack"
            else:
                sprite_sheet = "_Attack2"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        if sprite_sheet == "_Attack" and sprite_index == len(sprites) - 1:
            self.attack = False
        elif sprite_sheet == "_Attack2" and sprite_index == len(sprites) - 1:
            self.attack = False
            self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


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


def draw(window, bg_image, player, objects, offset_x):
    window.blit(bg_image, (0, 0))

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, window):
		if self.image is not None:
			window.blit(self.image, self.rect)
		window.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    font_path = "assets/font.ttf"
    return pygame.font.Font(font_path, size)

BG = pygame.image.load(join("assets", "menu", "Background.png")).convert_alpha()
BG = pygame.transform.scale(BG, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))

def sound_off():
    pygame.mixer.music.stop()

def sound_on():
    pygame.mixer.music.load('assets/sounds/Seven Goblins - A2.mp3')
    pygame.mixer.music.play(-1)

def option_fullscreen():
    pass

def sound_options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render("SOUND", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((FULLSCREEN_WIDTH/2), 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        SOUND_ON = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 500), 
                            text_input="ON", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SOUND_OFF = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 700), 
                            text_input="OFF", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BACK = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 900), 
                            text_input="BACK", font=get_font(90), base_color="#d7fcd4", hovering_color="White")
        

        for button in [SOUND_ON, SOUND_OFF, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    options()
                if SOUND_ON.checkForInput(OPTIONS_MOUSE_POS):
                    sound_on()
                if SOUND_OFF.checkForInput(OPTIONS_MOUSE_POS):
                    sound_off()
                
        pygame.display.update()

def pause():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render("PAUSE", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((FULLSCREEN_WIDTH/2), 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTIONS_FULLSCREEN = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 500), 
                            text_input="FULLSCREEN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_MENU = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 700), 
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_SOUND = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 900), 
                            text_input="SOUND", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_RESUME = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 1100), 
                            text_input="RESUME", font=get_font(90), base_color="#d7fcd4", hovering_color="White")

        for button in [OPTIONS_FULLSCREEN, OPTIONS_SOUND, OPTIONS_RESUME]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_FULLSCREEN.checkForInput(OPTIONS_MOUSE_POS):
                    option_fullscreen()
                if OPTIONS_MENU.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_SOUND.checkForInput(OPTIONS_MOUSE_POS):
                    sound_options()
                if OPTIONS_RESUME.checkForInput(OPTIONS_MOUSE_POS):
                    if in_game:
                        return
                    else :
                        select_level()
                
        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((FULLSCREEN_WIDTH/2), 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTIONS_FULLSCREEN = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 500), 
                            text_input="FULLSCREEN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_SOUND = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 700), 
                            text_input="SOUND", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        OPTIONS_BACK = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 900), 
                            text_input="BACK", font=get_font(90), base_color="#d7fcd4", hovering_color="White")

        for button in [OPTIONS_FULLSCREEN, OPTIONS_SOUND, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_FULLSCREEN.checkForInput(OPTIONS_MOUSE_POS):
                    option_fullscreen()
                if OPTIONS_SOUND.checkForInput(OPTIONS_MOUSE_POS):
                    sound_options()
                
        pygame.display.update()
        
def select_level():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render("LEVELS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((FULLSCREEN_WIDTH/2), 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)

        LEVEL_1 = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 500), 
                            text_input="LEVEL 1", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        LEVEL_2 = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 600), 
                            text_input="LEVEL 2", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        LEVEL_3 = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 700), 
                            text_input="LEVEL 3", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        
        OPTIONS_BACK = Button(image=None, pos=((FULLSCREEN_WIDTH/2), 900), 
                            text_input="BACK", font=get_font(90), base_color="#d7fcd4", hovering_color="White")
        
        for button in [LEVEL_1, LEVEL_2, LEVEL_3, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1.checkForInput(OPTIONS_MOUSE_POS):
                    game(window)
                if LEVEL_2.checkForInput(OPTIONS_MOUSE_POS):
                    game(window)
                if LEVEL_3.checkForInput(OPTIONS_MOUSE_POS):
                    game(window)
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                
        pygame.display.update()

in_game = False

def game(window):
    clock = pygame.time.Clock()
    
    bg_image = pygame.image.load(join("assets", "img", "Background.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))
    
    # Create the player instance
    player = Player(100, 100, 50, 50)
    
    # Create the floor blocks (terrain)
    floor = [Block(i * block_size, FULLSCREEN_HEIGHT - block_size, block_size)
             for i in range(-FULLSCREEN_WIDTH // block_size, (FULLSCREEN_WIDTH * 2) // block_size)]
    
    # Additional blocks
    objects = [*floor]
    
    global in_game  
    in_game = True

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    player.attacking()

        player.loop(FPS)
        handle_move(player, objects)
        draw(window, bg_image, player, objects, offset_x)
        pygame.display.update()
        level.run()
        clock.tick(FPS)

        if ((player.rect.right - offset_x >= FULLSCREEN_WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__game__":
    game(window)

def main_menu():
    while True:
        window.blit(BG, (0, 0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("FORGOTTEN KNIGHT", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((FULLSCREEN_WIDTH/2), 200))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=((FULLSCREEN_WIDTH/2), 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=((FULLSCREEN_WIDTH/2), 600), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=((FULLSCREEN_WIDTH/2), 800), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
               
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_level()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
main_menu()