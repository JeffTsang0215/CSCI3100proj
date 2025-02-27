import pygame
import shared
from card import CardTemplate
from cardList import card  # Import card data

# Load background
cardcollection_bg = pygame.image.load(shared.path + "image/cardcollection.png")
cardcollection_bg = pygame.transform.scale(cardcollection_bg, (shared.WIDTH, shared.HEIGHT))

# Load button images
return_button_image = pygame.image.load(shared.path + "image/returnarrow.png")
hover_button_image = pygame.image.load(shared.path + "image/returnarrow_hover.png")
click_button_image = pygame.image.load(shared.path + "image/returnarrow_click.png")

# Scale return button
return_button_size = (50, 35)
return_button_image = pygame.transform.scale(return_button_image, return_button_size)
hover_button_image = pygame.transform.scale(hover_button_image, return_button_size)
click_button_image = pygame.transform.scale(click_button_image, return_button_size)

# Get button rect AFTER scaling
return_button = return_button_image.get_rect(topright=(0.945 * shared.WIDTH, 0.03 * shared.HEIGHT))

# Pagination settings
CARDS_PER_PAGE = 8
current_page = 0
last_button_press = 0  # Prevents multiple quick clicks
total_pages = (len(card) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE  # Total number of pages

# Navigation buttons
page_button_size = (25, 45)
next_button_image = pygame.image.load(shared.path + "image/rightarrow.png")
next_button_image = pygame.transform.scale(next_button_image, page_button_size)
next_button = next_button_image.get_rect(topright=(0.65 * shared.WIDTH, 0.42 * shared.HEIGHT))

back_button_image = pygame.image.load(shared.path + "image/leftarrow.png")
back_button_image = pygame.transform.scale(back_button_image, page_button_size)
back_button = back_button_image.get_rect(topright=(0.17 * shared.WIDTH, 0.42 * shared.HEIGHT))

# Define grid layout positions
start_x = 150  
start_y = 70   
card_spacing_x = 140  
card_spacing_y = 260  
cards_per_row = 4  

def cardcollection_main(mouse_pos, mouse_click):
    global current_page, last_button_press

    shared.screen.blit(cardcollection_bg, (0, 0))  # Draw background

    # Handle return button
    if return_button.collidepoint(mouse_pos):
        shared.screen.blit(hover_button_image, return_button.topleft)
        if mouse_click[0]:
            shared.screen.blit(click_button_image, return_button.topleft)
            shared.game_state = "menu"
    else:
        shared.screen.blit(return_button_image, return_button.topleft)

    # Handle next button (only if NOT on the last page)
    if current_page < total_pages - 1:
        if next_button.collidepoint(mouse_pos):
            shared.screen.blit(next_button_image, (next_button.left + 3, next_button.top))  # Hover effect
            if mouse_click[0] and (pygame.time.get_ticks() - last_button_press > 50):  
                current_page += 1  
                last_button_press = pygame.time.get_ticks()
        else:
            shared.screen.blit(next_button_image, next_button.topleft)

    # Handle back button (only if NOT on the first page)
    if current_page > 0:
        if back_button.collidepoint(mouse_pos):
            shared.screen.blit(back_button_image, (back_button.left - 3, back_button.top))  # Hover effect
            if mouse_click[0] and (pygame.time.get_ticks() - last_button_press > 50):  
                current_page -= 1  
                last_button_press = pygame.time.get_ticks()
        else:
            shared.screen.blit(back_button_image, back_button.topleft)

    # Draw only the cards for the current page
    start_index = current_page * CARDS_PER_PAGE
    end_index = start_index + CARDS_PER_PAGE

    for i, card_info in enumerate(card[start_index:end_index]):  
        row = i // cards_per_row  
        col = i % cards_per_row  
        x = start_x + col * card_spacing_x
        y = start_y + row * card_spacing_y
        cost, atk, hp, name, rarity, scale_factor,description, image, ext = card_info
        CardTemplate(cost, atk, hp, name, rarity, x, y, description, scale_factor, image, ext).draw()

    shared.text(shared.screen, "My Decks", (0, 0, 0), 12, [shared.WIDTH - 242, 22], "center")

    # Display page number at the bottom center
    page_number = f"Page {current_page + 1}"
    shared.text(shared.screen, page_number, (70, 70, 70), 16, [shared.WIDTH - 650, shared.HEIGHT - 120], "center")

