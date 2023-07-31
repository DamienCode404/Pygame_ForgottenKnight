import pygame

from scripts.load_animations import load_sprite_sheets
from scripts.parameters import *
from scripts.levels import level
class Player(pygame.sprite.Sprite):
    # Redimensionner le personnage in game
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("animation", 120, 80, True)
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.sprite_sheet = "_Idle"
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.attack = False
        self.attack_count = 0
        self.position_x = FULLSCREEN_HEIGHT/2 # position x tracking camera position default value
        self.position_y = -300 # position y tracking camera position default value
        self.animation_cancelable = True
        self.update_sprite()
        self.update()

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        self.fall_count = 0

    def move(self, dx, dy):
        #Update the player position x value to be able to move the terrain in the opposite direction
        self.position_x += dx
        # self.rect.y += dy

        #Update the player position x value to be able to move the terrain in the opposite direction
        self.position_y += dy
        # self.rect.x += dx
        
        # Update the terrain position
        level.terrain_sprites.update(self.position_x, self.position_y)

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

    def move_right(self, vel):
        self.x_vel = vel

        if self.direction != "right":
            self.direction = "right"

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
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]

        new_sprite_sheet = self.sprite_sheet
        new_animation_cancelable = True
        # Boolean to check if the current sprite is the last one of the animation
        is_last_sprite = self.animation_count // self.ANIMATION_DELAY == len(sprites)
        if self.hit:
            new_sprite_sheet = "_Hit"
        elif self.jump_count != 0:
            if self.jump_count == 1:
                new_sprite_sheet = "_Jump"
            else :
                # Check if the current sprite is the last of the roll animation
                if is_last_sprite and self.sprite_sheet == "_Roll" or self.jump_count < 0:
                    self.jump_count = -1
                    new_sprite_sheet = "_Fall"

                else:
                    new_sprite_sheet = "_Roll" # Faire en sorte que l'animation se termine avant "_Fall"
                    new_animation_cancelable = False

        elif self.y_vel > self.GRAVITY * 2:
            new_sprite_sheet = "_Fall"
        elif self.x_vel != 0:
            new_sprite_sheet = "_Run"
        elif self.attack:
            new_animation_cancelable = False
            if self.attack_count % 2 == 0:
                new_sprite_sheet = "_Attack"
            else:
                new_sprite_sheet = "_Attack2"
        else:
            new_sprite_sheet = "_Idle"
        
        if new_sprite_sheet != self.sprite_sheet and (is_last_sprite or self.animation_cancelable):
            self.animation_cancelable = new_animation_cancelable
            self.sprite_sheet = new_sprite_sheet
            self.animation_count = 0
            self.update()

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        if self.sprite_sheet == "_Attack" and sprite_index == len(sprites) - 1:
            self.attack = False
        elif self.sprite_sheet == "_Attack2" and sprite_index == len(sprites) - 1:
            self.attack = False
            #self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))