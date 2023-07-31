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

from scripts.physics import *

def game(window):
    '''
    Main game loop
    '''
    clock = pygame.time.Clock()
    bg_images = background_paralax()
    bg_image = bg_images[0]
    
    # Create the player instance
    player = Player(FULLSCREEN_WIDTH/3, 100, 50, 50)
    
    # Additional blocks
    objects = [*level.terrain_sprites]
    
    global in_game  
    in_game = True

    run = True
    while run:
        # Check main loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            # Check for key presses
            if event.type == pygame.KEYDOWN:
                # Check for escape key
                if event.key == pygame.K_ESCAPE:
                    go_to_menu = pause()
                    if go_to_menu:
                        return
                # Check for space key (jump)
                if event.key == pygame.K_SPACE and player.jump_count < 2 and player.jump_count > -1:
                    player.jump()

            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for left mouse button (attack)
                if event.button == pygame.BUTTON_LEFT:
                    player.attacking()

        # Update the player
        player.loop(FPS)
        # Update the player physics
        handle_move(player, objects)
        # Draw all the elements
        draw(window, bg_image, player, objects, player.position_x, player.position_y, bg_images)
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == "__game__":
    game(window)
    
def main_menu():
    while True:
        window.blit(BG_MAIN, (0, 0))
        
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