import pygame, os, math, random
import shared
import decks

# Load background
bg = pygame.image.load(shared.path + "image/choosedeck.png")
bg = pygame.transform.scale(bg, (shared.WIDTH, shared.HEIGHT))
scale2 = shared.HEIGHT / 675
scale1 = shared.WIDTH / 1080

# Font and colors
FONT = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(16 * scale2))
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
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
selected_index = None
page = 0


def draw_decks(mouse_pos, mouse_click):
    global selected_index
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
            decks.decks[i]["name"],
            FONT,
            WHITE,
            BLACK,
            (x + DECK_WIDTH / 2, y + DECK_HEIGHT/ 2 - FONT.get_height() / 4),
            border_thickness = int(1.6*scale2),
            align="center"
        )

        # Handle click
        if hovered and mouse_click[0]:
            selected_index = i

def draw_button(mouse_pos, mouse_click):
    global page
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


    #Card collection button
    card_rect = pygame.Rect(0.31*shared.WIDTH,0.895*shared.HEIGHT,0.135*shared.WIDTH, 0.03*shared.HEIGHT)
    card_hovered = card_rect.collidepoint(mouse_pos)
    if card_hovered:
        color = HOVER_COLOR
    else:
        color = BUTTON_COLOR
    
    if card_hovered and mouse_click[0]:
        shared.game_state = "card_collection"
    
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


def main(mouse_pos, mouse_click):
    shared.screen.blit(bg, (0, 0))
    draw_decks(mouse_pos, mouse_click)
    draw_button(mouse_pos, mouse_click)
