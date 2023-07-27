import pygame
import sys

pygame.init()

pygame.display.set_caption("Forgotten Knight")
pygame.display.set_icon(pygame.image.load("assets/logo/icon.png"))

from scripts.parameters import *

from scripts.levels import *

from scripts.load_animations import *

from scripts.importation import *

from scripts.player import Player

def draw(window, bg_image, player, objects, offset_x, bg_images):
    window.blit(bg_image, (0, 0))

    background_paralax_draw(bg_images, offset_x)

    for obj in objects:
        if type(obj) == Block:
            if obj.rect.x - offset_x < FULLSCREEN_WIDTH and obj.rect.x - offset_x > -obj.width:
                obj.draw(window, offset_x)

    level.run(offset_x)

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
                    return
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

        for button in [OPTIONS_FULLSCREEN, OPTIONS_MENU, OPTIONS_SOUND, OPTIONS_RESUME]:
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
                    return True
                if OPTIONS_SOUND.checkForInput(OPTIONS_MOUSE_POS):
                    sound_options()
                if OPTIONS_RESUME.checkForInput(OPTIONS_MOUSE_POS):
                    if in_game:
                        return False
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
                    return 1
                if LEVEL_2.checkForInput(OPTIONS_MOUSE_POS):
                    return 2
                if LEVEL_3.checkForInput(OPTIONS_MOUSE_POS):
                    return 3
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return None
                
        pygame.display.update()


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



level = Level(level_0, window)


def background_paralax():
    bg_images = []
    for i in range(1,4):
        bg_image = pygame.image.load(join("assets", "img", f"background_layer_{i}.png")).convert_alpha()
        bg_images.append(pygame.transform.scale(bg_image, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT)))
    return bg_images

def background_paralax_draw(bg_images, offset_x):
    bg_width = bg_images[0].get_width()

    for i in range(len(bg_images)):
        for n in range(-1, 2):
            window.blit(bg_images[i], (-(offset_x *(i/10+0.25)) % bg_width + n * bg_width, 0))

def background():
    bg_image = pygame.image.load(join("assets", "img", "Background.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))
    return bg_image

def game(window):
    clock = pygame.time.Clock()
    bg_images = background_paralax()
    bg_image = bg_images[0]
    
    # Create the player instance
    player = Player(100, 100, 50, 50)
    
    # Create the floor blocks (terrain)
    floor = [Block(i * block_size, FULLSCREEN_HEIGHT - block_size, block_size)
             for i in range(-FULLSCREEN_WIDTH // block_size, (FULLSCREEN_WIDTH * 2) // block_size)]
    
    # Additional blocks
    objects = [*floor, *level.terrain_sprites]
    
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
                    return_to_menu = pause()
                    if return_to_menu:
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    player.attacking()

        player.loop(FPS)
        handle_move(player, objects)
        draw(window, bg_image, player, objects, offset_x, bg_images)
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
                    level_number = select_level()
                    if level_number is not None:
                        #mettre le level en question
                        game(window)                    
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
main_menu()