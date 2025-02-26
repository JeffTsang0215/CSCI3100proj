import pygame
from prompt_toolkit.output.win32 import BACKGROUND_COLOR

import shared
import sqlite3
import bcrypt

# Colors
BACKGROUNDCOLOR = (105, 77, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ACTIVE_COLOR = (204, 119, 34)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

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
    def __init__(self, x, y, w, h, text='', max_length = 16, is_username = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.max_length = max_length
        self.is_username = is_username
        self.active = False
        self.txt_surface = font.render(self.text, True, BLACK)
        self.last_key_time = 0

    def handle_mouse_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            self.color = ACTIVE_COLOR
        else:
            self.active = False
            self.color = GRAY

    def update(self, current_time):
        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                if current_time - self.last_key_time > 150:
                    self.text = self.text[:-1]
                    self.txt_surface = font.render(self.text, True, BLACK)
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
                            self.txt_surface = font.render(self.text, True, BLACK)
                            self.last_key_time = current_time

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

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
username_box = InputBox(shared.WIDTH / 2 - 250, shared.HEIGHT / 2 - 70, 500, 40, max_length = 16, is_username=True)
password_box = InputBox(shared.WIDTH / 2 - 250, shared.HEIGHT / 2 - 20, 500, 40, max_length = 32)
login_button = pygame.Rect(shared.WIDTH / 2 - 250, shared.HEIGHT / 2 + 30, 500, 40)
register_button = pygame.Rect(shared.WIDTH / 2 - 250, shared.HEIGHT / 2 + 80, 500, 40)

def loginSystem_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
        if login_button.collidepoint(mouse_pos):
            login_user(username_box.text, password_box.text)
            # If login successful, clear inputs immediately
            if shared.game_state == "menu":
                username_box.text = ""
                password_box.text = ""
                username_box.txt_surface = font.render("", True, BLACK)
                password_box.txt_surface = font.render("", True, BLACK)
                return  # Exit early to prevent further processing

        elif register_button.collidepoint(mouse_pos):
            register_user(username_box.text, password_box.text)

        # Handle input box clicks on press
    if current_mouse_pressed and not previous_mouse_pressed:
        username_box.handle_mouse_click(mouse_pos)
        password_box.handle_mouse_click(mouse_pos)
        error_message = ""

    # Update input boxes
    username_box.update(current_time)
    password_box.update(current_time)

    prev_mouse_click = mouse_click

    # Only draw login screen if we're still in login state
    if shared.game_state == "login":
        # Draw everything
        shared.screen.fill(BACKGROUNDCOLOR)
        username_box.draw(shared.screen)
        password_box.draw(shared.screen)

        # Draw buttons
        pygame.draw.rect(shared.screen, GRAY, login_button)
        shared.text(shared.screen, "Login", BLACK, 36, login_button.center, "center")
        pygame.draw.rect(shared.screen, GRAY, register_button)
        shared.text(shared.screen, "Register", BLACK, 36, register_button.center, "center")

        # Draw error message
        if error_message:
            error_y = shared.HEIGHT / 2 + 140
            shared.text(shared.screen, error_message, error_color, 30,
                        (shared.WIDTH / 2, error_y), "center")