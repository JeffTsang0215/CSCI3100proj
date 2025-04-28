import pygame, os, math, random
import shared

# Load background
bg = pygame.image.load(shared.path + "image/choosehero_bgv2.png")
bg = pygame.transform.scale(bg, (shared.WIDTH, shared.HEIGHT))

#Scale
scale2 = shared.HEIGHT / 675
scale1 = shared.WIDTH / 1080

#Font and colors
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
selected_ai = 0

ai_images_main = [
    pygame.image.load(shared.path + "image/Alt-Heroes_Mage_Jaina.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Demon-Hunter_Illidan.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Druid_Malfurion.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Warrior_Garrosh.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Shaman_Thrall.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Warlock_Guldan.png"),
    pygame.image.load(shared.path + "image/Alt-Heroes_Hunter_Rexxar.png"),
    pygame.image.load(shared.path + "image/rogue_hero.png"),
]
def draw(mouse_pos, mouse_click):
    global selected_ai
    shared.text(shared.screen, "Choose Your Hero", BLACK ,int(20 * scale2),(0.50*shared.WIDTH, 0.055*shared.HEIGHT), "center")

        # Load images
    ai_images = [
        pygame.image.load(shared.path + "image/Alt-Heroes_Mage_Jaina.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Demon-Hunter_Illidan.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Druid_Malfurion.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Warrior_Garrosh.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Shaman_Thrall.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Warlock_Guldan.png"),
        pygame.image.load(shared.path + "image/Alt-Heroes_Hunter_Rexxar.png"),
        pygame.image.load(shared.path + "image/rogue_hero.png"),
    ]

    ai_names = ["Mage", "Demon Hunter", "Druid", "Warrior", "Shaman", "Warlock", "Hunter", "Rogue"]

    # Determine size
    AI_size = (40 * 4 * scale1, 45.3 * 4 * scale1)
    ai_images = [pygame.transform.scale(img, AI_size) for img in ai_images]

    # Define buttons (rects)
    ai_buttons = []
    columns = 4
    rows = 2
    padding_x = shared.WIDTH * 0.05
    padding_y = shared.HEIGHT * 0.08

    image_width = AI_size[0]
    image_height = AI_size[1]

    start_x = (shared.WIDTH - (columns * image_width + (columns - 1) * padding_x)) / 2
    start_y = (shared.HEIGHT - (rows * image_height + (rows - 1) * padding_y)) / 2

    for i in range(8):
        col = i % columns
        row = i // columns
        x = start_x + col * (image_width + padding_x)
        y = start_y + row * (image_height + padding_y)
        rect = ai_images[i].get_rect(topleft=(x, y))
        ai_buttons.append(rect)

    # Draw images
    for i in range(8):
        shared.screen.blit(ai_images[i], ai_buttons[i])
        shared.text(shared.screen, ai_names[i], BLACK ,int(18 * scale2),(ai_buttons[i].centerx, ai_buttons[i].bottom + 0.01*shared.HEIGHT), "center")

    # Handle click
    if mouse_click[0]:  # Left mouse button
        for i, rect in enumerate(ai_buttons):
            if rect.collidepoint(mouse_pos):
                selected_ai = i  # Save selected index (0~7)

    # Draw border if selected
    if selected_ai is not None:
        pygame.draw.rect(shared.screen, BORDER_COLOR, ai_buttons[selected_ai].inflate(int(10 * scale1), int(40 * scale1)), int(4 * scale1))


        #Back_button
    back_rect = pygame.Rect(0.47*shared.WIDTH,0.91*shared.HEIGHT,0.06*shared.WIDTH, 0.04*shared.HEIGHT)
    back_hovered = back_rect.collidepoint(mouse_pos)
    if back_hovered:
        color = HOVER_COLOR
    else:
        color = BUTTON_COLOR
        
    if back_hovered and mouse_click[0]:
        shared.game_state = "menu"

    pygame.draw.rect(shared.screen, color, back_rect)
    shared.text(shared.screen, "Back",BLACK,int(18 * scale2),back_rect.center, "center")


def main(mouse_pos, mouse_click):
    shared.screen.blit(bg, (0, 0))
    draw(mouse_pos, mouse_click)