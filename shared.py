import pygame, os, math, random, json, sqlite3

pygame.init()
path = os.path.dirname(os.path.abspath(__file__)) + '/'

renewed = False

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
fullscreen = False
DB_PATH = "database/database.db"

if not(fullscreen):
    if WIDTH > HEIGHT:
        HEIGHT *= 4/5
        WIDTH = HEIGHT * 16 / 9
        if WIDTH > pygame.display.Info().current_w:
            WIDTH = pygame.display.Info().current_w
            HEIGHT = WIDTH * 9 /16
    else:
        HEIGHT = HEIGHT/WIDTH
        WIDTH *= 3/4
        HEIGHT = WIDTH/HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60

# game_state = "playing" | "menu" | "login" | "lost" | "win"
game_state = "login"
# the user that is playing this game
user_name = ""

def text(screen, text, color, size, pos, align="left", font=None):
    text = text.encode("utf-8").decode("utf-8")
    
    # Use custom font if provided; otherwise, use system/default font
    if font is None:
        try:
            my_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", size)
        except Exception:
            my_font = pygame.font.Font(pygame.font.get_default_font(), size)
    else:
        my_font = font  # Use the provided custom font

    text_surface = my_font.render(text, True, color)
    
    if align == "left":
        screen.blit(text_surface, pos)
    elif align in ["center", "centre"]:
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

def draw_text_with_border(surface, text, font, text_color, border_color, position, border_thickness=2, align="center"):
    """Draws text with a border (outline effect)."""
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    # Adjust the position based on alignment
    if align == "center":
        text_rect.center = position
    elif align == "left":
        text_rect.topleft = position
    elif align == "right":
        text_rect.topright = position

    # Draw border (outline effect)
    for dx in [-border_thickness, 0, border_thickness]:
        for dy in [-border_thickness, 0, border_thickness]:
            if dx == 0 and dy == 0:
                continue
            border_surface = font.render(text, True, border_color)
            border_rect = border_surface.get_rect(center=text_rect.center)
            border_rect.move_ip(dx, dy)
            surface.blit(border_surface, border_rect)

    # Draw main text on top
    surface.blit(text_surface, text_rect)


# def draw_text(surface, text, font, text_color, position, align="center"):
#     """Draws normal text without a border."""
#     text_surface = font.render(text, True, text_color)
#     text_rect = text_surface.get_rect()

#     if align == "center":
#         text_rect.center = position
#     elif align == "left":
#         text_rect.topleft = position
#     elif align == "right":
#         text_rect.topright = position

#     surface.blit(text_surface, text_rect)

def draw_text(surface, text, font, text_color, position, align="center", line_spacing = HEIGHT/300):
    """Draws multiline text with optional alignment and line spacing."""
    lines = text.split('\n')
    line_surfaces = [font.render(line, True, text_color) for line in lines]
    line_heights = [surf.get_height() for surf in line_surfaces]
    total_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    # Start y-coordinate depending on alignment
    x, y = position
    if align == "center":
        y -= total_height // 2
    elif align == "bottom":
        y -= total_height
    # If align == "top", we don't modify y

    for i, line_surface in enumerate(line_surfaces):
        line_rect = line_surface.get_rect()
        line_y = y + sum(line_heights[:i]) + i * line_spacing

        if align == "center":
            line_rect.centerx = x
        elif align == "left":
            line_rect.x = x
        elif align == "right":
            line_rect.right = x

        line_rect.y = line_y
        surface.blit(line_surface, line_rect)


game_data = { 'username': "", 'money': 0 }

def save_game_data(data):
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)

def load_game_data():
    try:
        with open("data.json", "r") as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        return game_data

def update_user_gold(username, amount):
    """
    Updates a user's gold by a specific amount.
    Positive amount = gain gold
    Negative amount = spend gold
    """
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT gold FROM user_progress WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row:
        current_gold = row[0]
        new_gold = current_gold + amount

        # Optional: Prevent negative gold
        if new_gold < 0:
            print("Not enough gold!")
            conn.close()
            return False

        cursor.execute("UPDATE user_progress SET gold = ? WHERE username = ?", (new_gold, username))
        conn.commit()
        print(f"Gold updated by {amount}. New balance: {new_gold}")
        conn.close()
        return True
    else:
        print("User not found.")
        conn.close()
        return False
