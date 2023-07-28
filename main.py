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

from scripts.display import *

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