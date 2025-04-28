import pygame, os, math, random
import shared
import decks
import cardList

# Load background
bg = pygame.image.load(shared.path + "image/choosedeck.png")
bg = pygame.transform.scale(bg, (shared.WIDTH, shared.HEIGHT))


# Track selection
selected_ai = "priest"
#Scale
scale2 = shared.HEIGHT / 675
scale1 = shared.WIDTH / 1080

# Font and colors
FONT = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(16 * scale2))
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GREY = (30, 30, 30)
HOVER_COLOR = (204, 134, 76)
SELECTED_COLOR = (100, 149, 237)
BLACK = (0, 0, 0)
DECK_COLOR = (137, 84, 39)
BORDER_COLOR = (255, 255, 0)  # Yellow border color
BUTTON_COLOR = (206, 176, 149)

# Layout constants
DECK_WIDTH, DECK_HEIGHT = 0.11*shared.WIDTH, 0.1*shared.HEIGHT
PADDING = 0.04 * shared.HEIGHT
MARGIN_X, MARGIN_Y = 0.18* shared.WIDTH , 0.30* shared.HEIGHT
DECKS_PER_ROW = 3
ROWS = 3
DECKS_PER_PAGE = DECKS_PER_ROW * ROWS

# Track selected and page state
selected_index = 0
page = 0
user_card = None
ai_card = None

def click_circle(mouse_pos, center, radius):
    return (mouse_pos[0] - center[0]) ** 2 + (mouse_pos[1] - center[1]) ** 2 <= radius ** 2

def draw_decks(mouse_pos, mouse_click):
    global selected_index, user_card
    start_index = page * DECKS_PER_PAGE
    end_index = min(start_index + DECKS_PER_PAGE, len(decks.decks))

    for i in range(start_index, end_index):
        local_index = i - start_index
        row = local_index // DECKS_PER_ROW
        col = local_index % DECKS_PER_ROW

        x = MARGIN_X + col * (DECK_WIDTH + PADDING)
        y = MARGIN_Y + row * (DECK_HEIGHT + PADDING)
        rect = pygame.Rect(x, y, DECK_WIDTH, DECK_HEIGHT)

        # Determine visual state
        hovered = rect.collidepoint(mouse_pos)
        color = DECK_COLOR
        if hovered:
            color = HOVER_COLOR
        
        if len(decks.decks[i]["cards"]) != 30:
            color = DARK_GREY

        # Draw filled background first
        pygame.draw.rect(shared.screen, color, rect)

        # Then draw border depending on state
        if i == selected_index:
            pygame.draw.rect(shared.screen, BORDER_COLOR, rect, int(5*scale2))
        else:
            pygame.draw.rect(shared.screen, BLACK, rect, int(1.6*scale2))
        

        # Draw deck name with border using shared's function
        shared.draw_text_with_border(
            shared.screen,
            decks.decks[i]["name"] + "\n" + str(len(decks.decks[i]["cards"])) + "/30",
            FONT,
            WHITE,
            BLACK,
            (x + DECK_WIDTH / 2, y + DECK_HEIGHT/ 2 - FONT.get_height() / 4),
            border_thickness = int(1.6*scale2),
            align="center"
        )

        # Handle click
        if hovered and mouse_click[0] and len(decks.decks[i]["cards"]) == 30:
            selected_index = i
            user_card = cardList.load_deck_from_names(decks.decks[i])

def draw_button(mouse_pos, mouse_click):
    global page, selected_ai, ai_card, selected_index, user_card

    #Back_button
    back_rect = pygame.Rect(0.808*shared.WIDTH,0.905*shared.HEIGHT,0.04*shared.WIDTH, 0.03*shared.HEIGHT)
    back_hovered = back_rect.collidepoint(mouse_pos)
    if back_hovered:
        color = HOVER_COLOR
    else:
        color = BUTTON_COLOR
        
    if back_hovered and mouse_click[0]:
        shared.game_state = "menu"

    pygame.draw.rect(shared.screen, color, back_rect)
    shared.text(shared.screen, "Back",BLACK,int(16 * scale2),back_rect.center, "center")


    # Card collection button
    card_rect = pygame.Rect(0.31 * shared.WIDTH, 0.895 * shared.HEIGHT, 0.135 * shared.WIDTH, 0.03 * shared.HEIGHT)
    card_hovered = card_rect.collidepoint(mouse_pos)
    color = HOVER_COLOR if card_hovered else BUTTON_COLOR

    pygame.draw.rect(shared.screen, color, card_rect)  # Draw the button (if not already drawn elsewhere)

    if card_hovered and mouse_click[0]:
            shared.previous_state = "choosedeck"
            shared.game_state = "card_collection"
            shared.input_blocked_frames = 5
    
    
    pygame.draw.rect(shared.screen, color, card_rect)
    shared.text(shared.screen, "Card Collections",BLACK,int(16 * scale2),card_rect.center, "center")

    #Deck buttons
    page_button_size = (40 * scale1 , 60 * scale1)
    next_button_image = pygame.image.load(shared.path + "image/rightarrow.png")
    next_button_image = pygame.transform.scale(next_button_image, page_button_size)
    next_button = next_button_image.get_rect(topright=(0.61 * shared.WIDTH, 0.44 * shared.HEIGHT))

    back_button_image = pygame.image.load(shared.path + "image/leftarrow.png")
    back_button_image = pygame.transform.scale(back_button_image, page_button_size)
    back_button = back_button_image.get_rect(topright=(0.15 * shared.WIDTH, 0.44 * shared.HEIGHT))

    if page == 1 and len(decks.decks) > 9:
        if back_button.collidepoint(mouse_pos):
            # Move the back button 2 pixels to the left on hover
            shared.screen.blit(back_button_image, (back_button.left - 2, back_button.top))
            
            # Handle button click for changing pages
            if mouse_click[0]:
                page = 0  # Go to the previous page
        else:
            shared.screen.blit(back_button_image, back_button.topleft)

    elif page == 0 and len(decks.decks) > 9:
        if next_button.collidepoint(mouse_pos):
            # Move the next button 2 pixels to the right on hover
            shared.screen.blit(next_button_image, (next_button.left + 2, next_button.top))

            # Handle button click for changing pages
            if mouse_click[0]:
                page = 1  # Go to the previous page
        else:
            shared.screen.blit(next_button_image, next_button.topleft)

    #Draw two AI
    #Load image
    priest = pygame.image.load(shared.path + "image/Heroes_Priest.png")
    paladin = pygame.image.load(shared.path + "image/Heroes_Paladin_Uther.png")

    #Determine Size
    AI_size = (40*3*scale1, 45.3*3*scale1)
    priest = pygame.transform.scale(priest,AI_size)
    paladin = pygame.transform.scale(paladin,AI_size)
    priest_button = priest.get_rect(topleft = (0.675*shared.WIDTH, 0.18*shared.HEIGHT))
    paladin_button = priest.get_rect(topleft = (0.675*shared.WIDTH, 0.45*shared.HEIGHT))

    # Draw images
    shared.screen.blit(priest, priest_button)
    shared.text(shared.screen, "Priest", WHITE ,int(16 * scale2),(priest_button.centerx, priest_button.bottom + 0.01*shared.HEIGHT), "center")
    shared.screen.blit(paladin, paladin_button)
    shared.text(shared.screen, "Paladin", WHITE ,int(16 * scale2),(paladin_button.centerx, paladin_button.bottom + 0.01*shared.HEIGHT), "center")

    # Check for click with mouse_click[0] (left button)
    if mouse_click[0]:  # Left mouse button is held down
        if priest_button.collidepoint(mouse_pos):
            selected_ai = "priest"
        elif paladin_button.collidepoint(mouse_pos):
            selected_ai = "paladin"

    # Draw border if selected
    if selected_ai == "priest":
        # Copy the priest_button
        border_rect = priest_button.copy()
        
        # Expand width normally
        border_rect.x -= int(5 * scale1)
        border_rect.width += int(10 * scale1)
        
        # Expand top a little (normal)
        border_rect.y -= int(5 * scale1)
        border_rect.height += int(5 * scale1)  # small top increase

        # Expand bottom more 
        border_rect.height += int(25 * scale1)

        pygame.draw.rect(shared.screen, BORDER_COLOR, border_rect, int(4 * scale1))
        ai_card = cardList.load_deck_from_names(decks.AI_deck_1[0])

    elif selected_ai == "paladin":
        border_rect = paladin_button.copy()
        border_rect.x -= int(5 * scale1)
        border_rect.width += int(10 * scale1)
        border_rect.y -= int(5 * scale1)
        border_rect.height += int(5 * scale1) + int(25 * scale1)

        pygame.draw.rect(shared.screen, BORDER_COLOR, border_rect, int(4 * scale1))
        ai_card = cardList.load_deck_from_names(decks.AI_deck_2[0])


    #Some text
    shared.text(shared.screen, "Choose Your Deck",WHITE, int(16 * scale2),(0.37*shared.WIDTH, 0.125*shared.HEIGHT), "center")
    shared.text(shared.screen, "Choose Your Opponent",WHITE, int(16 * scale2),(0.73*shared.WIDTH, 0.135*shared.HEIGHT), "center")

    #Start button
    circle_center = (0.73*shared.WIDTH, 0.824*shared.HEIGHT)
    circle_radius = 0.075*shared.HEIGHT
    start_hovered = click_circle(mouse_pos, circle_center,circle_radius)

    if start_hovered:
        start_colour = HOVER_COLOR
    else:
        start_colour = BUTTON_COLOR
    
    pygame.draw.circle(shared.screen, start_colour,circle_center,circle_radius)

    if start_hovered and mouse_click[0]:
        #check if player has a deck
        if user_card == None:
            user_card = cardList.load_deck_from_names(decks.decks[selected_index])
        shared.game_state = "playing"

    shared.text(shared.screen, "Play",BLACK,int(20 * scale2),circle_center, "center")

def main(mouse_pos, mouse_click):
    shared.screen.blit(bg, (0, 0))
    draw_decks(mouse_pos, mouse_click)
    draw_button(mouse_pos, mouse_click)
