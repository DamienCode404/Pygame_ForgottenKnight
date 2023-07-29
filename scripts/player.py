import pygame

from scripts.load_animations import load_sprite_sheets
from scripts.parameters import FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT, block_size, scroll_area_width, FPS
from scripts.levels import level
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
        self.position_x = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        self.fall_count = 0

    def move(self, dx, dy):
        #self.rect.x += dx
        self.position_x += dx
        self.rect.y += dy
        level.terrain_sprites.update(self.position_x)

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

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))