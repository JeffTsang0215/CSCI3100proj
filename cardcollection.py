import pygame, os, math, random
import shared

# Load and scale background
cardcollection_bg = pygame.image.load(shared.path + "image/cardcollection.png")
cardcollection_bg = pygame.transform.scale(cardcollection_bg, (shared.WIDTH, shared.HEIGHT))

# Load button images
return_button_image = pygame.image.load(shared.path + "image/returnarrow.png")
hover_button_image = pygame.image.load(shared.path + "image/returnarrow_hover.png")
click_button_image = pygame.image.load(shared.path + "image/returnarrow_click.png")

# Scale images
button_size = (50, 35)
return_button_image = pygame.transform.scale(return_button_image, button_size)
hover_button_image = pygame.transform.scale(hover_button_image, button_size) 
click_button_image = pygame.transform.scale(click_button_image, button_size) 

# Get button rect AFTER scaling
return_button = return_button_image.get_rect(topright=(0.945 * shared.WIDTH, 0.03 * shared.HEIGHT))

def cardcollection_main(mouse_pos, mouse_click):
    shared.screen.blit(cardcollection_bg, (0, 0))  # Draw background

    if return_button.collidepoint(mouse_pos):   #hover effect
        shared.screen.blit(hover_button_image, return_button.topleft) 
        if mouse_click[0]:      #click effect
            shared.screen.blit(click_button_image, return_button.topleft) 
            shared.game_state = "menu"
    else:
        shared.screen.blit(return_button_image, return_button.topleft)  

  

