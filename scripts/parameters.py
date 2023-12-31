import pygame

from os.path import join

info = pygame.display.Info()
FULLSCREEN_WIDTH = info.current_w
FULLSCREEN_HEIGHT = info.current_h

window = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))

FPS = 60
PLAYER_VEL = 8

in_game = False

block_size = 24

scroll_area_width = 200

BG = pygame.image.load(join("assets", "menu", "Background.png")).convert_alpha()
BG = pygame.transform.scale(BG, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))

BG_MAIN = pygame.image.load(join("assets", "menu", "Background_test.png")).convert_alpha()
BG_MAIN = pygame.transform.scale(BG_MAIN, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))