import pygame
import sys
from os.path import join

from scripts.levels import Block
from scripts.parameters import BG, FULLSCREEN_HEIGHT, FULLSCREEN_WIDTH, PLAYER_VEL, in_game, window
from scripts.levels import level


def draw(window, bg_image, player, objects, player_position, bg_images):
    '''
    Draw all the elements on the screen
    '''
    window.blit(bg_image, (0, 0))

    background_paralax_draw(bg_images, player_position)

    ## Old code to draw the floor blocks (not used anymore)
    ## for obj in objects:
    ##     if type(obj) == Block:
    ##         if obj.rect.x - player_position < FULLSCREEN_WIDTH and obj.rect.x - player_position > -obj.width:
    ##             obj.draw(window, player_position)

    # Update the terrain position and draw it
    level.run(player_position)

    # Draw the player
    player.draw(window)

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

def sound_off():
    pygame.mixer.music.stop()

def sound_on():
    pygame.mixer.music.load('assets/sounds/Seven Goblins - A2.mp3')
    pygame.mixer.music.play(-1)

def option_fullscreen():
    """
    Set the game in fullscreen or not
    """
    pygame.display.toggle_fullscreen()


def sound_options():
    """
    Display the sound options menu
    """
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
    """
    Display the pause menu
    """
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
                    return False
                
        pygame.display.update()

def options():
    """
    Display the options menu
    """
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
                    return
                if OPTIONS_FULLSCREEN.checkForInput(OPTIONS_MOUSE_POS):
                    option_fullscreen()
                if OPTIONS_SOUND.checkForInput(OPTIONS_MOUSE_POS):
                    sound_options()
                
        pygame.display.update()
        
def select_level():
    """
    Return the level number selected by the user or None if the user wants to go back to the main menu
    """
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

def background_paralax():
    bg_images = []
    for i in range(1,4): # 3 layers
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