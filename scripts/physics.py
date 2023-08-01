import pygame
from scripts.parameters import *
from scripts.levels import level_map0, level_map1

def handle_vertical_collision(player, objects, dy):
    
    # collided_objects = []
    
    # for obj in objects:
    #     if pygame.sprite.collide_mask(player, obj):
    #         if dy > 0:
    #             player.rect.bottom = obj.rect.top
    #             player.landed()
    #         elif dy < 0:
    #             player.rect.top = obj.rect.bottom
    #             player.hit_head()

    #         collided_objects.append(obj)

    vertical_collided_objects = []
    collided_objects = pygame.sprite.spritecollide(player, objects, False, pygame.sprite.collide_mask)
    if dy > 0 :
        for collided_object in collided_objects:
            player.rect.bottom = collided_object.rect.top + 1
            player.landed()

    elif dy < 0:
        for collided_object in collided_objects:
            player.rect.top = collided_object.rect.bottom
            player.hit_head()

            vertical_collided_objects.append(collided_object)

    return vertical_collided_objects

def collide(player, objects, dx):
    player.move(dx * 1.2, -1)
    #player.update()
    # old
    # collided_object = None
    # To get the first object collided with the player
    collided_object = pygame.sprite.spritecollideany(player, objects, pygame.sprite.collide_mask)

    # To get all the objects collided with the player
    #  collided_object = pygame.sprite.spritecollide(player, objects, False, pygame.sprite.collide_mask)

    # old
    # for obj in objects:
    #     if pygame.sprite.collide_mask(player, obj):
    #         collided_object = obj
    #         break

    player.move(-dx * 1.2, 1)
    #player.update()
    return collided_object

def handle_move(player, objects):
    # player.scroll_x()
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
        if obj and obj.name == "damage_src":
            player.make_hit()