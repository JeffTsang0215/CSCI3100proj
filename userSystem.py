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

# Background of login page
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
                 password TEXT NOT NULL,
                 security_question TEXT NOT NULL,
                 security_answer TEXT NOT NULL)''')
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
        self.last_backspace_time = 0  # Separate timer for backspace
        self.key_states = {}  # {key_code: (last_time, repeat_phase)}

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

            # Handle backspace
            if keys[pygame.K_BACKSPACE]:
                if current_time - self.last_backspace_time > 150:
                    self.text = self.text[:-1]
                    self.txt_surface = font.render(self.text, True, WHITE)
                    self.last_backspace_time = current_time
            else:
                # Reset backspace timer when key is released
                self.last_backspace_time = 0

            # Process character keys
            if len(self.text) < self.max_length:
                shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

                # Check all possible keys
                for key_code in range(33, 127):
                    if keys[key_code]:
                        char = self._get_char(key_code, shift_pressed)
                        if not self._validate_char(char):
                            continue

                        # Key state management
                        if key_code not in self.key_states:
                            # New key press - immediate input
                            self._add_char(char)
                            self.key_states[key_code] = (current_time, 'initial')
                        else:
                            last_time, phase = self.key_states[key_code]
                            elapsed = current_time - last_time

                            if phase == 'initial' and elapsed >= 500:
                                self._add_char(char)
                                self.key_states[key_code] = (current_time, 'repeat')
                            elif phase == 'repeat' and elapsed >= 200:
                                self._add_char(char)
                                self.key_states[key_code] = (current_time, 'repeat')
                    else:
                        # Remove released keys from tracking
                        if key_code in self.key_states:
                            del self.key_states[key_code]

    def _get_char(self, key_code, shift_pressed):
        """Convert key code to character with shift handling"""
        char = chr(key_code)
        if shift_pressed:
            if pygame.K_a <= key_code <= pygame.K_z:
                return char.upper()
            return shifted_characters.get(key_code, char)
        return char.lower() if pygame.K_a <= key_code <= pygame.K_z else char

    def _validate_char(self, char):
        """Validate characters for username fields"""
        if self.is_username:
            return char.isalnum() or char == '_'
        return True

    def _add_char(self, char):
        """Safely add character to input"""
        if len(self.text) < self.max_length:
            self.text += char
            self.txt_surface = font.render(self.text, True, WHITE)

    def draw(self, screen):
        box_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        box_surface.fill((*self.color, self.alpha))
        screen.blit(box_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.outline, self.rect, 2)
        if self.text == '':
            self.txt_surface = font.render(self.empty_text, True, DARK_GRAY)
        screen.blit(self.txt_surface, (self.rect.x + (15 * scale), self.rect.y + (15 * scale)))


class DropdownMenu:
    def __init__(self, x, y, w, h, questions, alpha=130):
        self.rect = pygame.Rect(x, y, w, h)
        self.options_rect = pygame.Rect(x, y + h, w, h * 3)
        self.questions = questions
        self.selected_question = ""
        self.is_open = False
        self.alpha = alpha
        self.color = DARK_GRAY
        self.outline = BLACK
        self.txt_surface = font.render("Select security question", True, GRAY)

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_open = not self.is_open
            return True
        elif self.is_open and self.options_rect.collidepoint(mouse_pos):
            index = (mouse_pos[1] - self.options_rect.y) // self.rect.height
            if 0 <= index < len(self.questions):
                self.selected_question = self.questions[index]
                self.txt_surface = font.render(self.selected_question, True, WHITE)
                self.is_open = False
            return True
        self.is_open = False
        return False

    def draw(self, screen):
        # Main box
        box_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        box_surface.fill((*self.color, self.alpha))
        screen.blit(box_surface, self.rect)
        pygame.draw.rect(screen, self.outline, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 15 * scale, self.rect.y + 15 * scale))

        # Dropdown options
        if self.is_open:
            options_surface = pygame.Surface((self.options_rect.w, self.options_rect.h), pygame.SRCALPHA)
            options_surface.fill((*self.color, self.alpha))
            screen.blit(options_surface, self.options_rect)
            pygame.draw.rect(screen, self.outline, self.options_rect, 2)
            for i, question in enumerate(self.questions):
                option_rect = pygame.Rect(self.options_rect.x, self.options_rect.y + i * 60 * scale, self.options_rect.w, 60 * scale)
                # Draw bottom border for all except last option
                if i < len(self.questions) - 1:
                    pygame.draw.line(screen, self.outline, (option_rect.left, option_rect.bottom - 1), (option_rect.right, option_rect.bottom - 1), 2)

            for i, question in enumerate(self.questions):
                text = font.render(question, True, WHITE)
                pos = (self.options_rect.x + 15 * scale, self.options_rect.y + 15 * scale + i * self.rect.height)
                screen.blit(text, pos)

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


def register_user(username, password, security_question, security_answer):
    global error_message, error_color

    def verify_password(password):
        """Helper function to check password validity"""
        has_number = False
        has_upper = False
        has_lower = False

        for char in password:
            if char.isdigit():
                has_number = True
            elif char.islower():
                has_lower = True
            elif char.isupper():
                has_upper = True
            # Approve password have at least 1 number, lower-case and upper-case letter.
            if has_number and has_upper and has_lower:
                return True

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
    if not verify_password(password):
        error_message = "Password must contain 1 number, 1 uppercase letter, and 1 lowercase letter!"
        error_color = RED
        return
    if security_question == "":
        error_message = "A security question must be selected!"
        error_color = RED
        return
    if security_answer == "":
        error_message = "Verification answer cannot be empty!"
        error_color = RED
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_security_answer = bcrypt.hashpw(security_answer.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)',
                       (username, hashed_password.decode('utf-8'), security_question, hashed_security_answer.decode('utf-8')))
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
login_username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text = '<USERNAME>', alpha = 130, max_length = 16, is_username=True)
login_password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (80 * scale), 800 * scale, 60 * scale, empty_text = '<PASSWORD>', alpha = 130, max_length = 32)
register_username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (400 * scale), 800 * scale, 60 * scale, empty_text = '<USERNAME>', alpha = 130, max_length = 16, is_username=True)
register_password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (270 * scale), 800 * scale, 60 * scale, empty_text = '<PASSWORD>', alpha = 130, max_length = 32)
security_answer_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (60 * scale), 800 * scale, 60 * scale, empty_text = '<ANSWER>', alpha = 130, max_length = 32)
login_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (260 * scale), (800 * scale), (60 * scale))
register_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (260 * scale), (800 * scale), (60 * scale))
createAccount_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (340 * scale), (800 * scale), (60 * scale))
return_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (340 * scale), (800 * scale), (60 * scale))

# Pre-render guideline text surfaces for register page
register_guidelines = [
    ("-Username must contain 3-16 characters", 26, (shared.HEIGHT/2 - 340 * scale), "left"),
    ("-Username can include letters, numbers, and underscores(_)", 26, (shared.HEIGHT/2 - 310 * scale), "left"),
    ("-Password must contain 8-32 characters", 26, (shared.HEIGHT/2 - 210 * scale), "left"),
    ("-Password can include letters, numbers, and special characters", 26, (shared.HEIGHT/2 - 180 * scale), "left"),
    ("  (e.g. !, @, <, /, [, ...)", 26, (shared.HEIGHT/2 - 150 * scale), "left"),
    ("-Password must include a number, uppercase, and lowercase", 26, (shared.HEIGHT/2 - 120 * scale), "left"),
    ("  letter", 26, (shared.HEIGHT/2 - 90 * scale), "left"),
    ("Security question for password recovery", 36, (shared.HEIGHT/2 - 50 * scale), "left"),
    ("-Security question answer is case-sensitive", 26, (shared.HEIGHT/2 + 120 * scale), "left")
]

guideline_surfaces = []
for text, size_rel, y_rel, align in register_guidelines:
    font_size = int(round(size_rel * scale))
    guideline_font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_surf = guideline_font.render(text, True, WHITE)
    x_pos = shared.WIDTH/2 - (400 * scale) if align == "left" else shared.WIDTH/2
    guideline_surfaces.append((text_surf, (x_pos, y_rel)))

# Security questions
security_questions = [
    "What was the name of your first pet?",
    "What city were you born in?",
    "What was your childhood nickname?"
]

# Security question dropdown
security_dropdown = DropdownMenu(
    shared.WIDTH/2 - 400*scale,
    shared.HEIGHT/2 - 10*scale,
    800*scale,
    60*scale,
    security_questions,
    alpha = 255
)

# Pre-render button text surfaces
button_font_size = int(round(36 * scale))
button_font = pygame.font.Font(pygame.font.get_default_font(), button_font_size)

# Error message size
error_font_size = int(round(36 * scale))

login_text_surface = button_font.render("Login", True, WHITE)
create_acc_text_surface = button_font.render("Create a new account", True, WHITE)
register_text_surface = button_font.render("Register", True, WHITE)
return_text_surface = button_font.render("Return to login page", True, WHITE)

def loginSystem_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    # Draw window and input boxes
    shared.screen.blit(login_bg, (0, 0))
    login_username_box.draw(shared.screen)
    login_password_box.draw(shared.screen)

    # Draw buttons
    pygame.draw.rect(shared.screen, ORANGE, login_button)
    pygame.draw.rect(shared.screen, ORANGE, createAccount_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size, (shared.WIDTH / 2, shared.HEIGHT / 2 + (220 * scale)), "center")

    if login_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, login_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            login_user(login_username_box.text, login_password_box.text)
            # If login successful, clear inputs immediately
            if shared.game_state == "menu":
                login_username_box.text = ""
                login_password_box.text = ""
                return  # Exit early to prevent further processing

    if createAccount_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, createAccount_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            shared.game_state = "register"
            login_username_box.text = ""
            login_password_box.text = ""
            prev_mouse_click = (False, False, False)
            error_message = ""
            return

    # Handle input box clicks on press
    if current_mouse_pressed and not previous_mouse_pressed:
        login_username_box.handle_mouse_click(mouse_pos)
        login_password_box.handle_mouse_click(mouse_pos)
        error_message = ""

    # Update input boxes
    login_username_box.update(current_time)
    login_password_box.update(current_time)

    # Button text (using pre-rendered surfaces)
    shared.screen.blit(login_text_surface, login_text_surface.get_rect(center=login_button.center))
    shared.screen.blit(create_acc_text_surface, create_acc_text_surface.get_rect(center=createAccount_button.center))
    prev_mouse_click = mouse_click

def registerSystem_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    # Draw background & pre-rendered guidelines
    shared.screen.blit(login_bg, (0, 0))
    for surf, pos in guideline_surfaces:
        shared.screen.blit(surf, pos)

    # Draw page and input boxes
    register_username_box.draw(shared.screen)
    register_password_box.draw(shared.screen)
    security_answer_box.draw(shared.screen)
    security_dropdown.draw(shared.screen)

    # Draw buttons
    pygame.draw.rect(shared.screen, ORANGE, register_button)
    pygame.draw.rect(shared.screen, ORANGE, return_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size,(shared.WIDTH / 2, shared.HEIGHT / 2 + (220 * scale)), "center")

    if register_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, register_button)  # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
            # Check if mouse was released over a button
            register_user(register_username_box.text, register_password_box.text, security_dropdown.selected_question, security_answer_box.text)

    if return_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, return_button)  # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
            # Check if mouse was released over a button
            shared.game_state = "login"
            register_username_box.text = ""
            register_password_box.text = ""
            security_dropdown.selected_question = ""
            security_dropdown.txt_surface = font.render("Select security question", True, GRAY)
            security_answer_box.text = ""
            prev_mouse_click = (False, False, False)
            error_message = ""
            return

    # Handle input box clicks on press
    if current_mouse_pressed and not previous_mouse_pressed:
        if security_dropdown.handle_click(mouse_pos):
            # Close other input boxes if dropdown was clicked
            register_username_box.active = False
            register_password_box.active = False
            security_answer_box.active = False
            register_username_box.color = WHITE
            register_password_box.color = WHITE
            security_answer_box.color = WHITE
        else:
            # Handle other input boxes
            register_username_box.handle_mouse_click(mouse_pos)
            register_password_box.handle_mouse_click(mouse_pos)
            security_answer_box.handle_mouse_click(mouse_pos)
            error_message = ""

    # Update input boxes
    register_username_box.update(current_time)
    register_password_box.update(current_time)
    security_answer_box.update(current_time)

    shared.screen.blit(register_text_surface, register_text_surface.get_rect(center=register_button.center))
    shared.screen.blit(return_text_surface, return_text_surface.get_rect(center=return_button.center))
    prev_mouse_click = mouse_click