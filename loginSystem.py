import pygame

import shared
import sqlite3
import bcrypt

#scale
scale = shared.HEIGHT / 1080

# Colors
BACKGROUNDCOLOR = (105, 77, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
ACTIVE_COLOR = (204, 119, 34)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (178, 86, 13)
HOVER_COLOR = (141, 64, 4)

# Fonts
font = pygame.font.Font(None, int(round(48 * scale)))

login_bg = pygame.image.load(shared.path + "image/loginBackground.png")
login_bg = pygame.transform.scale(login_bg, (shared.WIDTH, shared.HEIGHT))

# Define shifted characters mapping
shifted_characters = {
    pygame.K_1: '!',    pygame.K_2: '@',
    pygame.K_3: '#',    pygame.K_4: '$',
    pygame.K_5: '%',    pygame.K_6: '^',
    pygame.K_7: '&',    pygame.K_8: '*',
    pygame.K_9: '(',    pygame.K_0: ')',
    pygame.K_MINUS: '_', pygame.K_EQUALS: '+',
    pygame.K_COMMA: '<', pygame.K_PERIOD: '>',
    pygame.K_SLASH: '?', pygame.K_SEMICOLON: ':',
    pygame.K_QUOTE: '"',  pygame.K_LEFTBRACKET: '{',
    pygame.K_RIGHTBRACKET: '}', pygame.K_BACKSLASH: '|',
    pygame.K_BACKQUOTE: '~'
}

# Database setup
conn = sqlite3.connect(shared.path + 'database/database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY UNIQUE,
                 password TEXT NOT NULL)''')
conn.commit()

class InputBox:
    def __init__(self, x, y, w, h, text = '', empty_text = '', outline = BLACK, alpha = 255, max_length = 16, is_username = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.outline = outline
        self.alpha = alpha
        self.text = text
        self.empty_text = empty_text
        self.max_length = max_length
        self.is_username = is_username
        self.active = False
        self.txt_surface = font.render(self.text, True, WHITE)
        self.last_key_time = 0

    def handle_mouse_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            self.color = ACTIVE_COLOR
        else:
            self.active = False
            self.color = WHITE

    def update(self, current_time):
        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                if current_time - self.last_key_time > 150:
                    self.text = self.text[:-1]
                    self.txt_surface = font.render(self.text, True, WHITE)
                    self.last_key_time = current_time
            else:
                # Add length check before adding new characters
                if len(self.text) >= self.max_length:
                    return  # Don't process input if max length reached
                shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                for key_code in range(33, 127): #All special characters, numbers, upper&lower-case letter
                    if keys[key_code]:
                        if current_time - self.last_key_time > 100:
                            char = chr(key_code)
                            if shift_pressed:
                                # Handle shift-modified characters
                                if key_code in range(pygame.K_a, pygame.K_z + 1):
                                    char = char.upper()
                                elif key_code in range(pygame.K_EXCLAIM, pygame.K_BACKQUOTE + 1):
                                    # Handle shifted number keys for symbols
                                    char = shifted_characters.get(key_code, char)

                            # Validate characters for username
                            if self.is_username:
                                if not (char.isalnum() or char == '_'):
                                    continue  # Skip invalid characters

                            self.text += char
                            self.txt_surface = font.render(self.text, True, WHITE)
                            self.last_key_time = current_time

    def draw(self, screen):
        box_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        box_surface.fill((*self.color, self.alpha))
        screen.blit(box_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.outline, self.rect, 2)
        if self.text == '':
            self.txt_surface = font.render(self.empty_text, True, DARK_GRAY)
        screen.blit(self.txt_surface, (self.rect.x + (15 * scale), self.rect.y + (15 * scale)))

# Error message variables
error_message = ""
error_color = RED
prev_mouse_click = (False, False, False)

def login_user(username, password):
    global error_message, error_color
    if not username or not password:
        error_message = "Username/password cannot be empty!"
        error_color = RED
        return
    try:
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                # Clear messages and change state immediately
                error_message = ""
                shared.game_state = "menu"
                return  # Exit function immediately
            else:
                error_message = "Incorrect password!"
                error_color = RED
        else:
            error_message = "Username not found!"
            error_color = RED
    except Exception as e:
        error_message = f"Login error: {str(e)}"
        error_color = RED


def register_user(username, password):
    global error_message, error_color
    if not username or not password:
        error_message = "Username/password cannot be empty!"
        error_color = RED
        return
    if len(username) < 3:
        error_message = "Username cannot be less than 3 characters!"
        error_color = RED
        return
    if len(password) < 8:
        error_message = "Password cannot be less than 8 characters!"
        error_color = RED
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                       (username, hashed_password.decode('utf-8')))
        conn.commit()
        error_message = "Registration successful!"
        error_color = GREEN
    except sqlite3.IntegrityError:
        error_message = "Username already exists!"
        error_color = RED
    except Exception as e:
        error_message = f"Registration error: {str(e)}"
        error_color = RED

# Initialize input boxes and buttons
username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text = '<USERNAME>', alpha = 130, max_length = 16, is_username=True)
password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (20 * scale), 800 * scale, 60 * scale, empty_text = '<PASSWORD>', alpha = 130, max_length = 32)
login_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (260 * scale), (800 * scale), (60 * scale))
register_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (340 * scale), (800 * scale), (60 * scale))

def loginSystem_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    # Draw window and input boxes
    shared.screen.blit(login_bg, (0, 0))
    username_box.draw(shared.screen)
    password_box.draw(shared.screen)

    # Draw buttons
    pygame.draw.rect(shared.screen, ORANGE, login_button)
    pygame.draw.rect(shared.screen, ORANGE, register_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, 26, (shared.WIDTH / 2, shared.HEIGHT / 2 + (220 * scale)), "center")

    if login_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, login_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            login_user(username_box.text, password_box.text)
            # If login successful, clear inputs immediately
            if shared.game_state == "menu":
                username_box.text = ""
                password_box.text = ""
                username_box.txt_surface = font.render("", True, BLACK)
                password_box.txt_surface = font.render("", True, BLACK)
                return  # Exit early to prevent further processing

    if register_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, register_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            register_user(username_box.text, password_box.text)

    # Handle input box clicks on press
    if current_mouse_pressed and not previous_mouse_pressed:
        username_box.handle_mouse_click(mouse_pos)
        password_box.handle_mouse_click(mouse_pos)
        error_message = ""

    # Update input boxes
    username_box.update(current_time)
    password_box.update(current_time)

    # Guidelines for username and password
    shared.text(shared.screen, "-Username must contain 3-16 characters", WHITE, int(round(28 * scale)), (shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (100 * scale)), "left")
    shared.text(shared.screen, "-Username can include letters, numbers, and underscores(_)", WHITE, int(round(28 * scale)), (shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (70 * scale)), "left")
    shared.text(shared.screen, "-Password must contain 8-32 characters", WHITE, int(round(28 * scale)), (shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (40 * scale)), "left")
    shared.text(shared.screen, "-Password can include letters, numbers, and special characters", WHITE, int(round(28 * scale)), (shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (70 * scale)), "left")
    shared.text(shared.screen, " (e.g. !, @, <, /, [, ...)", WHITE, int(round(28 * scale)), (shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (100 * scale)), "left")

    shared.text(shared.screen, "Login", WHITE, int(round(36 * scale)), login_button.center, "center")
    shared.text(shared.screen, "Register", WHITE, int(round(36 * scale)), register_button.center, "center")
    prev_mouse_click = mouse_click

