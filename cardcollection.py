import pygame
import shared
from card import CardTemplate, DeckCard
import cardList
import decks
from collections import Counter

scale1 = shared.WIDTH / 1080
scale2 = shared.HEIGHT / 675

current_card_page = 0
last_page = -1

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
total_pages = (len(cardList.card) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE  # Total number of pages

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
deck_width = 126 * scale1
deck_height = 30 * scale2
deck_spacing = 0 * scale2
deck_start_x = shared.WIDTH - 307 * scale1
deck_start_y = 56 * scale2
cancel_button_size = (30 * scale1, 30 * scale2)

selected_deck_index = None
last_click_time = 0
double_click_delay = 400  # Time in milliseconds for double-click detection
typing_active = False
input_text = ""
selected_cost = None

card_objects = []

def draw_deck_list(mouse_pos, mouse_click, events):
    global deck_rects, cancel_buttons, selected_cost, current_page
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
        pygame.draw.rect(shared.screen, (0, 0, 0), rect, 1)

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

        # Draw deck name using draw_text_with_border
        if typing_active and selected_deck_index == i:
            pygame.draw.rect(shared.screen, (200, 200, 200), rect, 2)  # Highlight editing deck
            shared.draw_text_with_border(
                shared.screen, input_text, custom_font, 
                (255, 255, 255), (0, 0, 0),  # White text, Black border
                (deck_x + deck_width // 2, deck_y + deck_height // 2),
                align="center"
            )
        else:
            shared.draw_text_with_border(
                shared.screen, deck["name"], custom_font, 
                (255, 255, 255), (0, 0, 0),  # White text, Black border
                (deck_x + deck_width // 2, deck_y + deck_height // 2),
                align="center"
            )

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
    shared.draw_text_with_border(
    shared.screen, deck_count_text, custom_font, (255, 255, 255), (0, 0, 0),  
    [shared.WIDTH - 290 * scale1, 615 * scale2], 
    border_thickness=2, align="left"
    )
    
    for event in events:
        if event.type in [pygame.KEYDOWN, pygame.TEXTINPUT]:  # Capture typing events
            handle_text_input(event)

    # Back button
    back_rect = pygame.Rect(874 * scale1, 618 * scale2, 43*scale1, 18*scale2)
    pygame.draw.rect(shared.screen, (206, 176, 149), back_rect)
    back_text = custom_font.render("Back", True, (0, 0, 0))
    shared.screen.blit(back_text, (878 * scale1, 616 * scale2))  

    if back_rect.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, (255, 226, 199), back_rect)
        shared.screen.blit(back_text, (878 * scale1, 616 * scale2))
        if mouse_click[0]:
            shared.game_state = "menu"
            selected_cost = None    
            current_page = 0       

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
    global current_view, last_click_time, current_card_page

    if current_view != "deck_view":
        return

    deck = decks.decks[selected_deck_index]

    # Back button
    back_rect = pygame.Rect(874 * scale1, 618 * scale2, 43*scale1, 18*scale2)
    pygame.draw.rect(shared.screen, (206, 176, 149), back_rect)
    back_text = custom_font.render("Back", True, (0, 0, 0))
    shared.screen.blit(back_text, (878 * scale1, 616 * scale2))

    if back_rect.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, (255, 226, 199), back_rect)
        shared.screen.blit(back_text, (878 * scale1, 616 * scale2))
        if mouse_click[0]:
            current_view = "deck_list"  

    # Display deck name
    shared.draw_text_with_border(shared.screen, deck["name"], pygame.font.Font("fonts/belwe-bold-bt.ttf", int(14*scale1)), (255, 255, 255), (0, 0, 0), (shared.WIDTH - 250 * scale1, 40 * scale2), align="center")

    # Define card positions
    deck_card_x = shared.WIDTH - 307 * scale1  # X position for the cards
    deck_card_y = 56 * scale2  # Starting Y position for the first card
    deck_card_spacing = 30 * scale2  # Space between cards vertically

    # Count occurrences of each card in the selected deck
    card_counts = {}
    for card_name in deck["cards"]:
        card_counts[card_name] = card_counts.get(card_name, 0) + 1

    # Create a dictionary for quick lookups
    card_dict = {c[3]: (c[0], c[4]) for c in cardList.card}  # Maps name -> (cost, rarity)

    # Collect deck cards with cost
    deck_cards_data = [
        (card_name, count, *card_dict.get(card_name, ("?", "?"))) 
        for card_name, count in card_counts.items()
    ]

    # Store DeckCard instances for interaction
    deck_cards = []

    # Pagination logic for unique cards (show only the first 15 unique cards)
    unique_cards = list(card_counts.keys())  # Get unique card names
    cards_per_page = 18  # Cards shown per page
    total_pages = (len(unique_cards) - 1) // cards_per_page + 1  # Calculate total pages

    # Pagination logic: show only the current page's cards
    start_idx = current_card_page * cards_per_page
    end_idx = start_idx + cards_per_page
    page_cards = unique_cards[start_idx:end_idx]

    # Sort by cost (index 2 in the tuple)
    deck_cards_data.sort(key=lambda x: x[2] if isinstance(x[2], int) else float('inf'))

    # Render DeckCard objects for the current page (only unique cards)
    for card_name, count, card_cost, card_rarity in deck_cards_data[start_idx:end_idx]:  # Use sorted data
        deck_card = DeckCard(deck_card_x, deck_card_y, card_name, card_rarity, card_cost, count)
        deck_card.draw(shared.screen, mouse_pos)
        deck_cards.append(deck_card)
        deck_card_y += deck_card_spacing  # Increment the Y position for the next card

    # Localized positions for the pagination arrows in deck_view
    local_page_button_size = (17 * scale1, 31 * scale1)

    # Next button (right arrow) position
    next_button_image = pygame.image.load(shared.path + "image/rightarrow.png")
    next_button_image = pygame.transform.scale(next_button_image, local_page_button_size)
    next_button = next_button_image.get_rect(topright=(0.92 * shared.WIDTH, 0.82 * shared.HEIGHT))

    # Back button (left arrow) position
    back_button_image = pygame.image.load(shared.path + "image/leftarrow.png")
    back_button_image = pygame.transform.scale(back_button_image, local_page_button_size)
    back_button = back_button_image.get_rect(topright=(0.9 * shared.WIDTH, 0.82 * shared.HEIGHT))

    # Draw pagination arrows with hover effect (move buttons by 2 pixels)
    if current_card_page > 0:
        if back_button.collidepoint(mouse_pos):
            # Move the back button 2 pixels to the left on hover
            shared.screen.blit(back_button_image, (back_button.left - 2, back_button.top))
        else:
            shared.screen.blit(back_button_image, back_button.topleft)

    if current_card_page < total_pages - 1:
        if next_button.collidepoint(mouse_pos):
            # Move the next button 2 pixels to the right on hover
            shared.screen.blit(next_button_image, (next_button.left + 2, next_button.top))
        else:
            shared.screen.blit(next_button_image, next_button.topleft)

    # Handle button click for changing pages
    if back_button.collidepoint(mouse_pos) and mouse_click[0]:
        if current_card_page > 0:
            current_card_page -= 1  # Go to the previous page

    if next_button.collidepoint(mouse_pos) and mouse_click[0]:
        if current_card_page < total_pages - 1:
            current_card_page += 1  # Go to the next page

    # Check for cancel button clicks
    if mouse_click[0]:  # Left mouse click
        for deck_card in deck_cards:
            if deck_card.cancel_rect.collidepoint(mouse_pos):
                if deck_card.name in deck["cards"]:
                    deck["cards"].remove(deck_card.name)  # Remove one occurrence
                    decks.save_decks()  # Save changes
                    return  # Exit early to avoid issues with list modification

    for card_obj in card_objects:
        if card_obj.add_rect.collidepoint(mouse_pos):
            if mouse_click[0]:  # Left mouse button clicked

                #if selected_deck_index is not None and selected_deck_index < len(decks.decks):
                deck = decks.decks[selected_deck_index]  # Get the selected deck
                card_count = deck["cards"].count(card_obj.name)  # Count occurrences of the card

                    # Check if the card is legendary
                is_legendary = card_obj.rarity.lower() == "legendary"
                # contains_legendary = any(
                #     card_info[4].lower() == "legendary" for card_info in cardList.card if card_info[3] in deck["cards"]
                # )

                if len(deck["cards"]) < 30:  # Ensure deck size limit of 30 cards
                    # If the card is legendary, check if there is already one in the deck
                    if is_legendary and card_count == 1:
                        print("You can only have one legendary card in the deck!")
                    elif card_count < 2 or (is_legendary and card_count< 1):  # Each card can only appear up to 2 times
                        deck["cards"].append(card_obj.name)  
                        decks.save_decks()
                        # Recalculate card counts and sort deck cards
                        card_counts = Counter(deck["cards"])  # Count occurrences of each card
                        deck_cards_data = [
                            (card_name, count, *card_dict.get(card_name, ("?", "?"))) 
                            for card_name, count in card_counts.items()
                        ]
                        deck_cards_data.sort(key=lambda x: x[2] if isinstance(x[2], int) else float('inf'))

                            # After sorting, reapply pagination logic (if you are paginating)
                        unique_cards = list(card_counts.keys())  # Get unique card names
                        total_pages = (len(unique_cards) - 1) // cards_per_page + 1  # Calculate total pages
                        start_idx = current_card_page * cards_per_page
                        end_idx = start_idx + cards_per_page
                        page_cards = unique_cards[start_idx:end_idx]
                        break
            

    card_counts = Counter(deck["cards"])  # Count occurrences of each card
    total_cards = sum(card_counts.values())  # Sum up all card counts

    max_cards = 30
    total_cards_text = f"{total_cards}/{max_cards}"
    shared.draw_text_with_border(
        shared.screen, total_cards_text, custom_font, (255, 255, 255), (0, 0, 0),  # White text, black border
        [shared.WIDTH - 290 * scale1, 615 * scale2], 
        border_thickness=2, align="left"
    )

def display_cards(mouse_pos, mouse_click):
    global current_page, last_button_press, card_objects, selected_cost


    # Clear previous page's card objects
    card_objects = []

    # Draw filter buttons
    filter_button_width = 26 * scale1
    filter_button_height = 25 * scale2
    filter_button_margin = 2 * scale1
    manaT_image = pygame.image.load(shared.path + f"image/ManaT.png")
    manaT_image = pygame.transform.scale(manaT_image, (21*scale1, 20*scale1))
    manaF_image = pygame.image.load(shared.path + f"image/ManaF.png")
    manaF_image = pygame.transform.scale(manaF_image, (21*scale1, 20*scale1))
    filter_x = 221 * scale1
    filter_y = 608 * scale2

    for cost in range(8):  # Cost 0–6 and 7+
        label = str(cost)
        x = filter_x + cost * (filter_button_width + filter_button_margin)
        button_rect = pygame.Rect(x, filter_y, filter_button_width, filter_button_height)
        # Highlight if selected
        if selected_cost == cost:
            shared.screen.blit(manaF_image, (x, filter_y))
            shared.text(shared.screen, label, (150, 150, 150), int(16 * scale1), button_rect.center, "center", font=custom_font)
        else:
            shared.screen.blit(manaT_image, (x, filter_y))
            shared.text(shared.screen, label, (255, 255, 255), int(16 * scale1), button_rect.center, "center", font=custom_font)

        # Toggle filter on click
        if button_rect.collidepoint(mouse_pos) and mouse_click[0] and not last_button_press:
            if selected_cost == cost:
                selected_cost = None  # Turn off filter
                print(selected_cost)
            else:
                selected_cost = cost
                print(selected_cost)
            current_page = 0  # Reset page
    

    # Apply filtering
    sorted_cards = sorted(cardList.card, key=lambda c: c[0])
    if selected_cost is not None:
        if selected_cost < 7:
            sorted_cards = [card for card in sorted_cards if card[0] == selected_cost]
        else:
            sorted_cards = [card for card in sorted_cards if card[0] >= 7]

    # Pagination logic
    total_pages = (len(sorted_cards) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
    start_index = current_page * CARDS_PER_PAGE
    end_index = start_index + CARDS_PER_PAGE

    # Handle Next button
    if current_page < total_pages - 1:
        if next_button.collidepoint(mouse_pos):
            shared.screen.blit(next_button_image, (next_button.left + 3, next_button.top))  # Hover
            if mouse_click[0]:
                current_page += 1
        else:
            shared.screen.blit(next_button_image, next_button.topleft)

    # Handle Back button
    if current_page > 0:
        if back_button.collidepoint(mouse_pos):
            shared.screen.blit(back_button_image, (back_button.left - 3, back_button.top))  # Hover
            if mouse_click[0]:
                current_page -= 1
        else:
            shared.screen.blit(back_button_image, back_button.topleft)

    # Draw current page's cards
    for i, card_info in enumerate(sorted_cards[start_index:end_index]):
        row = i // cards_per_row
        col = i % cards_per_row
        x = start_x + col * card_spacing_x
        y = start_y + row * card_spacing_y

        cost, atk, hp, name, rarity, scale_factor, description, image, ext = card_info

        card_obj = CardTemplate(cost, atk, hp, name, rarity, x, y, description, scale_factor, image, ext)
        card_obj.draw()
        if current_view == "deck_view":
            card_obj.draw_plus_button(mouse_pos)
        card_objects.append(card_obj)

    # Display current page number
    page_number = f"Page {current_page + 1}"
    shared.text(shared.screen, page_number, (70, 70, 70), int(16 * scale2),
                [shared.WIDTH - 650 * scale1, shared.HEIGHT - 110 * scale2],
                "center", font=custom_font)
    
    last_button_press = mouse_click[0]


def cardcollection_main(mouse_pos, mouse_click, events):
    global total_pages
    total_pages = (len(cardList.card) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE

    shared.screen.blit(cardcollection_bg, (0, 0))  # Draw background
    shared.text(shared.screen, "My Decks", (30, 30, 30), int(9 * scale1), [shared.WIDTH - 242 * scale1, 22 * scale2], "center", font=custom_font)

    display_cards(mouse_pos, mouse_click)
    draw_deck_list(mouse_pos, mouse_click, events)
    draw_deck_view(mouse_pos, mouse_click)




    
