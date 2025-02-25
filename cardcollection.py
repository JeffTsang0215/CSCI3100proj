import pygame, os, math, random
import shared
from card import CardTemplate

# Load and scale background
cardcollection_bg = pygame.image.load(shared.path + "image/cardcollection.png")
cardcollection_bg = pygame.transform.scale(cardcollection_bg, (shared.WIDTH, shared.HEIGHT))

# Load button images
return_button_image = pygame.image.load(shared.path + "image/returnarrow.png")
hover_button_image = pygame.image.load(shared.path + "image/returnarrow_hover.png")
click_button_image = pygame.image.load(shared.path + "image/returnarrow_click.png")

# Scale images
return_button_size = (50, 35)
return_button_image = pygame.transform.scale(return_button_image, return_button_size)
hover_button_image = pygame.transform.scale(hover_button_image, return_button_size) 
click_button_image = pygame.transform.scale(click_button_image, return_button_size) 

# Get button rect AFTER scaling
return_button = return_button_image.get_rect(topright=(0.945 * shared.WIDTH, 0.03 * shared.HEIGHT))

# Next button
page_button_size = (25, 45)
next_button_image = pygame.image.load(shared.path + "image/rightarrow.png")
next_button_image = pygame.transform.scale(next_button_image, page_button_size)
next_button = next_button_image.get_rect(topright=(0.65 * shared.WIDTH, 0.42 * shared.HEIGHT))


# Define starting position and spacing
start_x = 150  
start_y = 70   
card_spacing_x = 140  
card_spacing_y = 260  
cards_per_row = 4  # Number of cards per row

# Create a list of cards dynamically from a database (Example data)
card_data = [
    (2, 3, 5, "common"),
    (4, 5, 6, "rare"),
    (6, 7, 8, "epic"),
    (8, 9, 10, "legendary"),
    (3, 4, 6, "common"),
    (5, 6, 7, "rare"),
    (7, 8, 9, "epic"),
    (9, 10, 11, "legendary"),
]

# Create CardTemplate objects dynamically
cards = []
for i, (cost, atk, hp, rarity) in enumerate(card_data):
    row = i // cards_per_row  # Determines the row (0 or 1)
    col = i % cards_per_row   # Determines the column (0 to 3)
    x = start_x + col * card_spacing_x
    y = start_y + row * card_spacing_y
    cards.append(CardTemplate(cost, atk, hp, rarity, x, y))

def cardcollection_main(mouse_pos, mouse_click):
    shared.screen.blit(cardcollection_bg, (0, 0))  # Draw background

    # Handle hover and click effects for the return button
    if return_button.collidepoint(mouse_pos):   
        shared.screen.blit(hover_button_image, return_button.topleft) 
        if mouse_click[0]:  
            shared.screen.blit(click_button_image, return_button.topleft) 
            shared.game_state = "menu"
    else:
        shared.screen.blit(return_button_image, return_button.topleft)  

    if next_button.collidepoint(mouse_pos):  
        hovered_pos = (next_button.left + 3, next_button.top)  # Move 3 pixels to the right
        shared.screen.blit(next_button_image, hovered_pos)
    else:
        shared.screen.blit(next_button_image, next_button.topleft)  # Default position

    # Draw the cards every frame
    for card in cards:
        card.draw()
