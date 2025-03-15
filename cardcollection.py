import pygame
import shared
from card import CardTemplate, DeckCard
from cardList import card
import decks
import pygame.time

scale1 = shared.WIDTH / 1080
scale2 = shared.HEIGHT / 675

# Load background
cardcollection_bg = pygame.image.load(shared.path + "image/cardcollection.png")
cardcollection_bg = pygame.transform.scale(cardcollection_bg, (shared.WIDTH, shared.HEIGHT))

custom_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(16 * scale2))
current_view = "deck_list"  # Can be "deck_list" or "deck_view"
selected_deck_index = None


# Load button images
return_button_image = pygame.image.load(shared.path + "image/returnarrow.png")
hover_button_image = pygame.image.load(shared.path + "image/returnarrow_hover.png")
click_button_image = pygame.image.load(shared.path + "image/returnarrow_click.png")

# Scale return button
return_button_size = (50 * scale1, 35 * scale1)
return_button_image = pygame.transform.scale(return_button_image, return_button_size)
hover_button_image = pygame.transform.scale(hover_button_image, return_button_size)
click_button_image = pygame.transform.scale(click_button_image, return_button_size)

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

selected_deck_index = None
last_click_time = 0
double_click_delay = 400  # Time in milliseconds for double-click detection
typing_active = False
input_text = ""

card_objects = []

def draw_deck_list(mouse_pos, mouse_click):
    global deck_rects, cancel_buttons
    global selected_deck_index, last_click_time, typing_active, input_text, current_view
    
    if current_view != "deck_list":
        return

    deck_rects.clear()
    cancel_buttons.clear()

    # Define colors
    deck_color = (137, 84, 39)  
    hover_color = (204, 134, 76)  
    text_color = (255, 255, 255)  
    plus_color = (100, 200, 100)  
    plus_hover_color = (180, 220, 180)  
    default_cancel_color = (255, 255, 255)  # White "-"
    hover_cancel_color = (255, 0, 0)  # Red "-"

    # Draw existing decks
    for i, deck in enumerate(decks.decks):
        deck_x = deck_start_x
        deck_y = deck_start_y + i * (deck_height + deck_spacing)
        rect = pygame.Rect(deck_x, deck_y, deck_width, deck_height)
        deck_rects.append(rect)
        
        # Cancel button position
        cancel_x = deck_x + deck_width 
        cancel_y = deck_y + (deck_height - cancel_button_size[1]) // 2
        cancel_rect = pygame.Rect(cancel_x, cancel_y, *cancel_button_size)
        cancel_buttons.append(cancel_rect)

        # Draw deck rectangle
        pygame.draw.rect(shared.screen, deck_color, rect)
        pygame.draw.rect(shared.screen, (0, 0, 0), rect, 2)

        # Apply deck hover effect
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(shared.screen, hover_color, rect)
            
            if mouse_click[0]:  # Left-click to open deck
                selected_deck_index = i
                current_view = "deck_view"  # Switch to deck view
                return

            if mouse_click[2]:  # Right-click detected for renaming
                typing_active = True
                selected_deck_index = i
                input_text = deck["name"]

        # Draw deck name
        if typing_active and selected_deck_index == i:
            pygame.draw.rect(shared.screen, (200, 200, 200), rect, 2)  # Highlight editing deck
            text_surface = custom_font.render(input_text, True, (255, 255, 255))
            #shared.draw_text_with_border(shared.screen, deck["name"], pygame.font.Font("fonts/belwe-bold-bt.ttf", 16), (255, 255, 255), (0, 0, 0), (shared.WIDTH - 250 * scale1, 40 * scale2), align="center")
        else:
            text_surface = custom_font.render(deck["name"], True, (255, 255, 255))
            #shared.draw_text_with_border(shared.screen, deck["name"], pygame.font.Font("fonts/belwe-bold-bt.ttf", 16), (255, 255, 255), (0, 0, 0), (shared.WIDTH - 250 * scale1, 40 * scale2), align="center")

        text_rect = text_surface.get_rect(center=(deck_x + deck_width / 2, deck_y + deck_height / 2))
        shared.screen.blit(text_surface, text_rect)

        # Delete deck button hover effect
        cancel_text_color = default_cancel_color  # Default White
        if cancel_rect.collidepoint(mouse_pos):
            cancel_text_color = hover_cancel_color  # Change to Red when hovered

        # Draw only the "-" text (NO background)
        shared.text(shared.screen, "-", cancel_text_color, int(20 * scale1), 
                    [cancel_x + cancel_button_size[0] // 2, cancel_y + cancel_button_size[1] // 2], "center")

    # Handle cancel button click
    if mouse_click[0]:  
        for i, cancel_rect in enumerate(cancel_buttons):
            if cancel_rect.collidepoint(mouse_pos):
                del decks.decks[i]  # Remove deck
                decks.save_decks()  # Save updated decks
                return  

    # Draw "+" button
    if len(decks.decks) < max_decks:
        plus_x = deck_start_x
        plus_y = deck_start_y + len(decks.decks) * (deck_height + deck_spacing)
        plus_rect = pygame.Rect(plus_x, plus_y, deck_width, deck_height)

        if plus_rect.collidepoint(mouse_pos):
            pygame.draw.rect(shared.screen, plus_hover_color, plus_rect)
            if mouse_click[0]:  
                new_deck_name = f"New Deck"
                decks.decks.append({"name": new_deck_name, "cards": []})
                decks.save_decks()  # Save new deck
        else:
            pygame.draw.rect(shared.screen, plus_color, plus_rect)

        # Draw "+" button text
        shared.text(shared.screen, "+", text_color, int(16 * scale1), 
                    [plus_x + deck_width / 2, plus_y + deck_height / 2], "center", font=custom_font)

    # Display total number of decks
    deck_count_text = f"{len(decks.decks)}/{max_decks}"
    shared.text(shared.screen, deck_count_text, (255, 255, 255), int(14 * scale1), 
                [shared.WIDTH - 290 * scale1, 615 * scale2], "left", font=custom_font)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        elif event.type in [pygame.KEYDOWN, pygame.TEXTINPUT]:  # Capture typing events
            handle_text_input(event)

    # Back button
    back_rect = pygame.Rect(874 * scale1, 618 * scale2, 45, 18)
    pygame.draw.rect(shared.screen, (206, 176, 149), back_rect)
    back_text = custom_font.render("Back", True, (0, 0, 0))
    shared.screen.blit(back_text, (878 * scale1, 616 * scale2))  

    if back_rect.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, (255, 226, 199), back_rect)
        shared.screen.blit(back_text, (878 * scale1, 616 * scale2))
        if mouse_click[0]:
            shared.game_state = "menu"           

def handle_text_input(event):
    global input_text, typing_active, selected_deck_index

    if typing_active and selected_deck_index is not None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to save
                if input_text.strip():  # Avoid empty names
                    decks.decks[selected_deck_index]["name"] = input_text
                    decks.save_decks()  # Save changes
                typing_active = False  # Exit rename mode
            elif event.key == pygame.K_BACKSPACE:  # Delete last character
                input_text = input_text[:-1]
        elif event.type == pygame.TEXTINPUT:  # Capture normal typing
            input_text += event.text  # Append typed character

def draw_deck_view(mouse_pos, mouse_click):
    global current_view, last_click_time  

    if current_view != "deck_view":
        return
    
    deck = decks.decks[selected_deck_index]

     # Back button
    back_rect = pygame.Rect(874 * scale1, 618 * scale2, 45, 18)
    pygame.draw.rect(shared.screen, (206, 176, 149), back_rect)
    back_text = custom_font.render("Back", True, (0, 0, 0))
    shared.screen.blit(back_text, (878 * scale1, 616 * scale2))

    if back_rect.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, (255, 226, 199), back_rect)
        shared.screen.blit(back_text, (878 * scale1, 616 * scale2))
        if mouse_click[0]:
            current_view = "deck_list"  


    # Display deck name
    shared.draw_text_with_border(shared.screen, deck["name"], pygame.font.Font("fonts/belwe-bold-bt.ttf", 16), (255, 255, 255), (0, 0, 0), (shared.WIDTH - 250 * scale1, 40 * scale2), align="center")

    # Define card positions
    deck_card_x = shared.WIDTH - 290 * scale1  
    deck_card_y = 70 * scale2
    deck_card_spacing = 35 * scale2  

    # Count occurrences of each card in the selected deck
    card_counts = {}
    for card_name in deck["cards"]:
        card_counts[card_name] = card_counts.get(card_name, 0) + 1

    # Store DeckCard instances for interaction
    deck_cards = []

    # Render DeckCard objects
    for card_name, count in card_counts.items():
        card_cost = next((c[0] for c in card if c[3] == card_name), "?")  

        deck_card = DeckCard(deck_card_x - 20 * scale1, deck_card_y - 10 * scale2, card_name, card_cost, count)
        deck_card.draw(shared.screen, mouse_pos)

        deck_cards.append(deck_card)  # Store for interaction

        deck_card_y += deck_card_spacing  

    # Check for cancel button clicks
    if mouse_click[0]:  # Left mouse click
        for deck_card in deck_cards:
            if deck_card.cancel_rect.collidepoint(mouse_pos):
                if deck_card.name in deck["cards"]:
                    deck["cards"].remove(deck_card.name)  # Remove one occurrence
                    decks.save_decks()  # Save changes
                    return  # Exit early to avoid issues with list modification

    # Ensure `current_time` is set before checking double-click
    current_time = pygame.time.get_ticks()
    double_click_delay = 400  # Time in milliseconds

    for card_obj in card_objects:
        if card_obj.rect.collidepoint(mouse_pos):
            if mouse_click[0]:  # Left mouse button clicked
                if last_click_time and (current_time - last_click_time < double_click_delay):  
                    if selected_deck_index is not None and selected_deck_index < len(decks.decks):
                        deck = decks.decks[selected_deck_index]  # Get the selected deck
                        card_count = deck["cards"].count(card_obj.name)  # Count occurrences of the card

                        if len(deck["cards"]) < 30:  # Ensure deck size limit of 30 cards
                            if card_count < 2:  # Each card can only appear up to 2 times
                                deck["cards"].append(card_obj.name)  
                                decks.save_decks()
                                break
                
                # Update last_click_time only after a click is detected
                last_click_time = current_time

    #card_count = f"{len(decks.cards)}/{max_decks}"
    #shared.text(shared.screen, deck_count_text, (255, 255, 255), int(14 * scale1), 
     #           [shared.WIDTH - 290 * scale1, 615 * scale2], "left", font=custom_font)

def cardcollection_main(mouse_pos, mouse_click):
    global current_page, last_button_press

    shared.screen.blit(cardcollection_bg, (0, 0))  # Draw background

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
        cost, atk, hp, name, rarity, scale_factor, description, image, ext = card_info

        card_obj = CardTemplate(cost, atk, hp, name, rarity, x, y, description, scale_factor, image, ext)
        card_obj.draw()
        card_objects.append(card_obj)  # Store card object

    shared.text(shared.screen, "My Decks", (30, 30, 30), int(9 * scale1), [shared.WIDTH - 242 * scale1, 22 * scale2], "center", font=custom_font)

    # Display page number at the bottom center
    page_number = f"Page {current_page + 1}"
    shared.text(shared.screen, page_number, (70, 70, 70), int(16 * scale2), [shared.WIDTH - 650 * scale1, shared.HEIGHT - 110 * scale2], "center", font=custom_font)


    draw_deck_list(mouse_pos, mouse_click)
    draw_deck_view(mouse_pos, mouse_click)
    



    
