import pygame
import shared
from card import CardTemplate
from cardList import card
import decks

scale1 = shared.WIDTH / 1080
scale2 = shared.HEIGHT / 675

# Load background
cardcollection_bg = pygame.image.load(shared.path + "image/cardcollection.png")
cardcollection_bg = pygame.transform.scale(cardcollection_bg, (shared.WIDTH, shared.HEIGHT))

# Load button images
return_button_image = pygame.image.load(shared.path + "image/returnarrow.png")
hover_button_image = pygame.image.load(shared.path + "image/returnarrow_hover.png")
click_button_image = pygame.image.load(shared.path + "image/returnarrow_click.png")

# Scale return button
return_button_size = (50 * scale1, 35 * scale1)
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
page_button_size = (25 * scale1 , 45 * scale1)
next_button_image = pygame.image.load(shared.path + "image/rightarrow.png")
next_button_image = pygame.transform.scale(next_button_image, page_button_size)
next_button = next_button_image.get_rect(topright=(0.65 * shared.WIDTH, 0.435 * shared.HEIGHT))

back_button_image = pygame.image.load(shared.path + "image/leftarrow.png")
back_button_image = pygame.transform.scale(back_button_image, page_button_size)
back_button = back_button_image.get_rect(topright=(0.17 * shared.WIDTH, 0.435 * shared.HEIGHT))

# Define grid layout positions
start_x = 150 * scale1
start_y = 70  * scale2
card_spacing_x = 140  * scale1
card_spacing_y = 260  * scale2
cards_per_row = 4  

# Deck settings
max_decks = 18
max_cards_per_deck = 30
deck_rects = []
cancel_buttons = []

# Define deck UI properties
deck_width = 122 * scale1
deck_height = 30 * scale2
deck_spacing = 0 * scale2
deck_start_x = shared.WIDTH - 305 * scale1
deck_start_y = 60 * scale2
cancel_button_size = (30 * scale1, 30 * scale2)

def draw_deck_list(mouse_pos, mouse_click):
    global deck_rects
    deck_rects.clear()

    # Define colors
    deck_color = (137, 84, 39)  # Default deck color (blue)
    hover_color = (204, 134, 76)  # Hover color (light blue)
    text_color = (255, 255, 255)  # White text
    plus_color = (100, 200, 100)  # Green "+" button
    plus_hover_color = (180, 220, 180)  # Lighter green for hover

    # Draw existing decks
    for i, deck in enumerate(decks.decks):
        deck_x = deck_start_x
        deck_y = deck_start_y + i * (deck_height + deck_spacing)
        rect = pygame.Rect(deck_x, deck_y, deck_width, deck_height)
        deck_rects.append(rect)
        
        # Cancel button position (right of the deck)
        cancel_x = deck_x + deck_width 
        cancel_y = deck_y + (deck_height - cancel_button_size[1]) // 2 * scale2
        cancel_rect = pygame.Rect(cancel_x, cancel_y, *cancel_button_size)

        # Change color on hover
        pygame.draw.rect(shared.screen, deck_color, rect)  # Default color
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(shared.screen, hover_color, rect)  # Hover effect

            #if mouse_click[0]:  
               # print(f"Selected {deck['name']}")  # Placeholder for selection

        # Draw the cancel button (rectangle)
        pygame.draw.rect(shared.screen, (200, 0, 0), (cancel_x, cancel_y, cancel_button_size[0], cancel_button_size[1]), 0)
        # Draw only the "-" text (no background)
        shared.text(shared.screen, "-", (255, 255, 255), int(20 * scale1), [cancel_x + cancel_button_size[0] // 2, cancel_y + cancel_button_size[1] // 2], "center")

            

        # Draw deck name
        shared.text(shared.screen, deck['name'], text_color, int(16 * scale1), [deck_x + deck_width / 2, deck_y + deck_height / 2], "center")

    # Draw "+" button (only if below max_decks)
    if len(decks.decks) < max_decks:
        plus_x = deck_start_x
        plus_y = deck_start_y + len(decks.decks) * (deck_height + deck_spacing)
        plus_rect = pygame.Rect(plus_x, plus_y, deck_width, deck_height)

        # Change "+" button color on hover
        if plus_rect.collidepoint(mouse_pos):
            pygame.draw.rect(shared.screen, plus_hover_color, plus_rect)  # Hover effect
            if mouse_click[0]:  
                new_deck_name = f"Deck {len(decks.decks) + 1}"
                decks.decks.append({"name": new_deck_name, "cards": []})
                print(f"Added {new_deck_name}")
        else:
            pygame.draw.rect(shared.screen, plus_color, plus_rect)  # Default green

        # Draw "+" button text
        shared.text(shared.screen, "+", text_color, int(16 * scale1), [plus_x + deck_width / 2, plus_y + deck_height / 2], "center")

        # Display the total number of decks
        deck_count_text = f"{len(decks.decks)}/{max_decks}"
        shared.text(shared.screen, deck_count_text, (255, 255, 255), int(14 * scale1), [shared.WIDTH - 296 * scale1, 617 * scale2], "left")



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

    shared.text(shared.screen, "My Decks", (0, 0, 0), int(12 * scale1), [shared.WIDTH - 242 * scale1, 22 * scale2], "center")

    # Display page number at the bottom center
    page_number = f"Page {current_page + 1}"
    shared.text(shared.screen, page_number, (70, 70, 70), int(16 * scale2), [shared.WIDTH - 650 * scale1, shared.HEIGHT - 110 * scale2], "center")

    draw_deck_list(mouse_pos, mouse_click)

    for i, cancel_rect in enumerate(cancel_buttons):
            if cancel_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Clicked the "-" symbol
                del decks[i]
                break


    



    
