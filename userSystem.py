import pygame

import cardList
import shared
import decks
import sqlite3
import bcrypt
import re

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
font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(32 * scale)))
password_font = pygame.font.SysFont("Arial", int(round(32 * scale)))

# Background of login page
login_bg = pygame.image.load(shared.path + "image/loginBackground.png")
login_bg = pygame.transform.scale(login_bg, (shared.WIDTH, shared.HEIGHT))

# button for view and hide password
view_button_image = pygame.image.load(shared.path + "image/view.png")
hide_button_image = pygame.image.load(shared.path + "image/hide.png")

view_button_image = pygame.transform.scale(view_button_image, (60 * scale, 60 * scale))
hide_button_image = pygame.transform.scale(hide_button_image, (60 * scale, 60 * scale))

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
                 security_question1 TEXT NOT NULL,
                 security_answer1 TEXT NOT NULL,
                 security_question2 TEXT NOT NULL,
                 security_answer2 TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_card_collection
                (username TEXT PRIMARY KEY UNIQUE,
                 unlock_cards TEXT NOT NULL,
                 decks TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_progress
                (username TEXT PRIMARY KEY UNIQUE,
                 gold INT NOT NULL,
                 battle_record TEXT NOT NULL)''')
conn.commit()

class InputBox:
    def __init__(self, x, y, w, h, text = '', empty_text = '', outline = BLACK, alpha = 255, max_length = 16, is_username = False, is_password = False, is_license_key = False, is_security_question=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.outline = outline
        self.alpha = alpha
        self.text = text
        self.empty_text = empty_text
        self.max_length = max_length
        self.is_username = is_username
        self.is_password = is_password
        self.is_license_key = is_license_key
        self.is_security_question = is_security_question
        self.show_password = not is_password
        self.active = False
        self.cursor_position = 0
        self.last_backspace_time = 0  # Separate timer for backspace
        self.last_space_time = 0 # Separate timer for space key
        self.key_states = {}  # {key_code: (last_time, repeat_phase)}

        # Eye button for password fields
        if self.is_password:
            button_size = int(60 * scale)
            self.eye_button = pygame.Rect(
                self.rect.right + 10,
                self.rect.y + (self.rect.height - button_size) // 2,
                button_size,
                button_size
            )
            # Load eye button images
            self.view_button_image = pygame.transform.scale(
                pygame.image.load(shared.path + "image/view.png"),
                (button_size, button_size)
            )
            self.hide_button_image = pygame.transform.scale(
                pygame.image.load(shared.path + "image/hide.png"),
                (button_size, button_size)
            )
        else:
            self.eye_button = None
            self.view_button_image = None
            self.hide_button_image = None

    def handle_mouse_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            self.color = ACTIVE_COLOR
            self.cursor_position = len(self.text)
        elif self.is_password and self.eye_button and self.eye_button.collidepoint(mouse_pos):
            self.show_password = not self.show_password # Toggle password visibility
        else:
            self.active = False
            self.color = WHITE
            self.cursor_position = len(self.text)

    def _handle_arrow_keys(self, keys, current_time):
        arrow_repeat_delay = 200  # milliseconds between repeats

        # Left arrow
        if keys[pygame.K_LEFT]:
            if pygame.K_LEFT not in self.key_states:
                self.cursor_position = max(0, self.cursor_position - 1)
                self.key_states[pygame.K_LEFT] = (current_time, 'initial')
            else:
                last_time, phase = self.key_states[pygame.K_LEFT]
                elapsed = current_time - last_time
                if (phase == 'initial' and elapsed >= 500) or (phase == 'repeat' and elapsed >= arrow_repeat_delay):
                    self.cursor_position = max(0, self.cursor_position - 1)
                    self.key_states[pygame.K_LEFT] = (current_time, 'repeat')
        elif pygame.K_LEFT in self.key_states:
            del self.key_states[pygame.K_LEFT]

        # Right arrow
        if keys[pygame.K_RIGHT]:
            if pygame.K_RIGHT not in self.key_states:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
                self.key_states[pygame.K_RIGHT] = (current_time, 'initial')
            else:
                last_time, phase = self.key_states[pygame.K_RIGHT]
                elapsed = current_time - last_time
                if (phase == 'initial' and elapsed >= 500) or (phase == 'repeat' and elapsed >= arrow_repeat_delay):
                    self.cursor_position = min(len(self.text), self.cursor_position + 1)
                    self.key_states[pygame.K_RIGHT] = (current_time, 'repeat')
        elif pygame.K_RIGHT in self.key_states:
            del self.key_states[pygame.K_RIGHT]

    def update(self, current_time):
        if self.active:
            keys = pygame.key.get_pressed()

            # Handle arrow keys
            self._handle_arrow_keys(keys, current_time)

            # Handle backspace
            if keys[pygame.K_BACKSPACE]:
                if (current_time - self.last_backspace_time > 150) and (self.cursor_position > 0):
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                    self.cursor_position = max(0, self.cursor_position - 1)
                    self.last_backspace_time = current_time
            else:
                # Reset backspace timer when key is released
                self.last_backspace_time = 0

            # Handle space character
            if keys[pygame.K_SPACE]:
                if current_time - self.last_space_time > 1000:
                    if len(self.text) < self.max_length and self.is_security_question:
                        self.text = self.text[:self.cursor_position] + " " + self.text[self.cursor_position:]
                        self.cursor_position += 1
                    self.last_space_time = current_time
            else:
                # Reset space timer when key is released
                self.last_space_time = 0

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
        """Validate characters for username and security question fields"""
        if self.is_username:
            return char.isalnum() or char == '_'
        if self.is_license_key:
            return char.isalnum() or char == '-'
        if self.is_security_question:
            return char.isalnum() or char == ' ' or char in shifted_characters.values()
        return char.isalnum() or char in shifted_characters.values()

    def _add_char(self, char):
        """Safely add character to input"""
        if len(self.text) < self.max_length:
            self.text = self.text[:self.cursor_position] + char + self.text[self.cursor_position:]
            self.cursor_position += 1

    def draw(self, screen):
        box_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        box_surface.fill((*self.color, self.alpha))
        screen.blit(box_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.outline, self.rect, 2)

        # Prepare displayed text
        if self.text == '':
            displayed_text = self.empty_text
            color = DARK_GRAY
        else:
            if self.is_password and not self.show_password:
                displayed_text = '●' * len(self.text)
            else:
                displayed_text = self.text
            color = WHITE

        # Render text
        if self.is_password and not self.show_password and self.text != "":
            txt_surface = password_font.render(displayed_text, True, color)
        else:
            txt_surface = font.render(displayed_text, True, color)
        screen.blit(txt_surface, (self.rect.x + 15, self.rect.y + 10))

        if self.is_password and self.eye_button:
            # Draw the appropriate eye button image
            if self.show_password:
                screen.blit(self.hide_button_image, self.eye_button)
            else:
                screen.blit(self.view_button_image, self.eye_button)

        # Draw cursor
        if self.active:
            cursor_text = displayed_text[:self.cursor_position]
            cursor_x = self.rect.x + 15 + font.size(cursor_text)[0]
            cursor_y = self.rect.y + 10
            cursor_height = font.get_height()
            pygame.draw.line(screen, WHITE, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + cursor_height), 2)


class DropdownMenu:
    def __init__(self, x, y, w, h, questions, alpha=130):
        self.rect = pygame.Rect(x, y, w, h)
        self.options_rect = pygame.Rect(x, y + h, w, h * len(questions)) # Adjust height based on number of questions
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
            return True
        self.is_open = False
        return False
    
    def handle_release(self, mouse_pos):
        if self.is_open and self.options_rect.collidepoint(mouse_pos):
            index = (mouse_pos[1] - self.options_rect.y) // self.rect.height
            if 0 <= index < len(self.questions):
                self.selected_question = self.questions[index]
                self.txt_surface = font.render(self.selected_question, True, WHITE)
                self.is_open = False
                return True
        return False

    def draw(self, screen):
        # Main box
        box_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        box_surface.fill((*self.color, self.alpha))
        screen.blit(box_surface, self.rect)
        pygame.draw.rect(screen, self.outline, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 15 * scale, self.rect.y + 10 * scale))

    def draw_options(self, screen):
        # Draw the dropdown options only when the dropdown is open
        if self.is_open:
            options_surface = pygame.Surface((self.options_rect.w, self.options_rect.h), pygame.SRCALPHA)
            options_surface.fill((*self.color, self.alpha))
            screen.blit(options_surface, self.options_rect)
            pygame.draw.rect(screen, self.outline, self.options_rect, 2)
            
            for i, question in enumerate(self.questions):
                option_rect = pygame.Rect(
                    self.options_rect.x,
                    self.options_rect.y + i * self.rect.height,
                    self.options_rect.w,
                    self.rect.height
                )
                
                # Draw option background
                option_surface = pygame.Surface((option_rect.w, option_rect.h), pygame.SRCALPHA)
                option_surface.fill((*self.color, self.alpha))
                screen.blit(option_surface, option_rect)
                
                # Draw bottom border for all except last option
                if i < len(self.questions) - 1:
                    pygame.draw.line(screen, self.outline, 
                                    (option_rect.left, option_rect.bottom - 1),
                                    (option_rect.right, option_rect.bottom - 1), 2)
                
                # Draw question text
                text = font.render(question, True, WHITE)
                text_rect = text.get_rect()
                text_rect.x = option_rect.x + 15 * scale
                text_rect.centery = option_rect.centery
                screen.blit(text, text_rect)

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
                shared.user_name = username
                cardList.load_unlock_cards()
                decks.load_decks()
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

stored_license_key = ""

def validate_license_key(license_key):
    global error_message, error_color, stored_license_key
    if not license_key:
        error_message = "License key cannot be empty!"
        error_color = RED
        return

    if not re.match(r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$', license_key):
        error_message = "Inputted license key has wrong format"
        error_color = RED
        return

    try:
        cursor.execute('SELECT is_consumed FROM licenses WHERE license_key = ?', (license_key,))
        license_status = cursor.fetchone()
        if not license_status:
            error_message = "Inputted license key does not exist!"
            error_color = RED
            return
        is_consumed = bool(license_status[0])
        if is_consumed:
            error_message = "Inputted license key is consumed!"
            error_color = RED
            return
        # If the license key is valid go the register page
        stored_license_key = license_key
        shared.game_state = "register"
        error_message = "License key validated!"
        error_color = GREEN
        return
    except Exception as e:
        error_message = f"Login error: {str(e)}"
        error_color = RED

def register_user(username, password, security_question1, security_answer1, security_question2, security_answer2):
    global error_message, error_color
    # some default setting of a new user account
    default_gold = 500

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
    if security_question1 == "" or security_question2 == "":
        error_message = "Both security question must be selected!"
        error_color = RED
        return
    if security_question1 == security_question2:
        error_message = "Two security questions must be different!"
        error_color = RED
        return
    if security_answer1 == "" or security_answer2 == "":
        error_message = "Verification answers cannot be empty!"
        error_color = RED
        return
    print(security_answer1, security_answer2)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_security_answer1 = bcrypt.hashpw(security_answer1.encode('utf-8'), bcrypt.gensalt())
    hashed_security_answer2 = bcrypt.hashpw(security_answer2.encode('utf-8'), bcrypt.gensalt())
    try:
        # initialize the account
        cursor.execute('INSERT INTO users (username, password, security_question1, security_answer1, security_question2, security_answer2) VALUES (?, ?, ?, ?, ?, ?)',
                       (username, hashed_password.decode('utf-8'), security_question1, hashed_security_answer1.decode('utf-8'), security_question2, hashed_security_answer2.decode('utf-8')))
        cursor.execute('INSERT INTO user_card_collection (username, unlock_cards, decks) VALUES (?, ?, ?)',
                       (username, cardList.starter_card_json, decks.starter_deck_json))
        cursor.execute('INSERT INTO user_progress (username, gold, battle_record) VALUES (?, ?, ?)',
                       (username, default_gold, ""))
        cursor.execute('UPDATE licenses SET is_consumed = 1 WHERE license_key = ?', (stored_license_key,))
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
# login page
login_username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text = '<USERNAME>', alpha = 130, max_length = 16, is_username=True)
login_password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (80 * scale), 800 * scale, 60 * scale, empty_text = '<PASSWORD>', alpha = 130, max_length = 32, is_password=True)
login_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (210 * scale), (800 * scale), (60 * scale))
forgot_password_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (290 * scale), (800 * scale), (60 * scale))
createAccount_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (370 * scale), (800 * scale), (60 * scale))
# input license key page
license_key_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text = '<LICENSE KEY>', alpha = 130, max_length = 14, is_license_key=True)
continue_register_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (290 * scale), (800 * scale), (60 * scale))
return_login_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (370 * scale), (800 * scale), (60 * scale))
# register page
register_username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (440 * scale), 800 * scale, 60 * scale, empty_text = '<USERNAME>', alpha = 130, max_length = 16, is_username=True)
register_password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (310 * scale), 800 * scale, 60 * scale, empty_text = '<PASSWORD>', alpha = 130, max_length = 32, is_password=True)
# Security questions
security_questions = [
    "What was the name of your first pet?",
    "What city were you born in?",
    "What was your childhood nickname?",
    "What is your favourite movie?"
]
# Security question dropdown
security_dropdown1 = DropdownMenu(
    shared.WIDTH/2 - 400*scale,
    shared.HEIGHT/2 - 50*scale,
    800*scale,
    60*scale,
    security_questions,
    alpha = 255
)
security_answer_box1 = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (20 * scale), 800 * scale, 60 * scale, empty_text = '<ANSWER>', alpha = 130, max_length = 32, is_security_question=True)
# Security question dropdown
security_dropdown2 = DropdownMenu(
    shared.WIDTH/2 - 400*scale,
    shared.HEIGHT/2 + 90*scale,
    800*scale,
    60*scale,
    security_questions,
    alpha = 255
)
security_answer_box2 = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (160 * scale), 800 * scale, 60 * scale, empty_text = '<ANSWER>', alpha = 130, max_length = 32, is_security_question=True)
register_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (290 * scale), (800 * scale), (60 * scale))
return_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (370 * scale), (800 * scale), (60 * scale))
# forget password page
forgot_username_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text='<USERNAME>', alpha=130, max_length=16, is_username=True)
proceed_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (290 * scale), (800 * scale), (60 * scale))
return_to_login_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (370 * scale), (800 * scale), (60 * scale))
# reset password page
security_answer1_reset = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (160 * scale), 800 * scale, 60 * scale, empty_text='<ANSWER>', alpha=130, max_length=32, is_security_question=True)
security_answer2_reset = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 - (40 * scale), 800 * scale, 60 * scale, empty_text='<ANSWER>', alpha=130, max_length=32, is_security_question=True)
new_password_box = InputBox(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (80 * scale), 800 * scale, 60 * scale, empty_text='<NEW PASSWORD>', alpha=130, max_length=32, is_password=True)
confirm_reset_button = pygame.Rect(shared.WIDTH / 2 - (400 * scale), shared.HEIGHT / 2 + (290 * scale), (800 * scale), (60 * scale))

# Pre-render guideline text surfaces for register page
register_guidelines = [
    ("-Username must contain 3-16 characters", 26, (shared.HEIGHT/2 - 380 * scale), "left"),
    ("-Username can include letters, numbers, and underscores(_)", 26, (shared.HEIGHT/2 - 350 * scale), "left"),
    ("-Password must contain 8-32 characters", 26, (shared.HEIGHT/2 - 250 * scale), "left"),
    ("-Password can include letters, numbers, and special characters", 26, (shared.HEIGHT/2 - 220 * scale), "left"),
    ("  (e.g. !, @, <, /, [, ...)", 26, (shared.HEIGHT/2 - 190 * scale), "left"),
    ("-Password must include a number, uppercase, and lowercase letter", 26, (shared.HEIGHT/2 - 160 * scale), "left"),
    ("Security questions for password recovery", 36, (shared.HEIGHT/2 - 90 * scale), "left"),
    ("-Security questions' answers are case-sensitive", 26, (shared.HEIGHT/2 + 220 * scale), "left")
]

register_guideline_surfaces = []
for text, size_rel, y_rel, align in register_guidelines:
    guideline_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(24 * scale * (size_rel/26))))
    text_surf = guideline_font.render(text, True, WHITE)
    x_pos = shared.WIDTH/2 - (400 * scale) if align == "left" else shared.WIDTH/2
    register_guideline_surfaces.append((text_surf, (x_pos, y_rel)))

# Pre-render guideline text surfaces for license key page
license_key_guidelines = [
    ("-License keys are formated as AAAA-BBBB-CCCC", 26, (shared.HEIGHT/2 - 100 * scale), "left"),
    ("-Hyphens are needed", 26, (shared.HEIGHT/2 - 70 * scale), "left"),
    ("-The license key will not be consumed if account registration are not", 26, (shared.HEIGHT/2 - 40 * scale), "left"),
    ("  completed", 26, (shared.HEIGHT/2 - 10* scale), "left"),
]

license_key_guidelines_surfaces = []
for text, size_rel, y_rel, align in license_key_guidelines:
    guideline_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(24 * scale)))
    text_surf = guideline_font.render(text, True, WHITE)
    x_pos = shared.WIDTH/2 - (400 * scale) if align == "left" else shared.WIDTH/2
    license_key_guidelines_surfaces.append((text_surf, (x_pos, y_rel)))

# Pre-render button text surfaces
button_font_size = int(round(36 * scale))
button_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", button_font_size)

login_text_surface = button_font.render("Login", True, WHITE)
forgot_password_text = button_font.render("Forget password", True, WHITE)
create_acc_text_surface = button_font.render("Create a new account", True, WHITE)
continue_register_text_surface = button_font.render("Continue registration", True, WHITE)
proceed_text = button_font.render("Proceed with password reset", True, WHITE)
confirm_reset_text = button_font.render("Confirm & reset with new password", True, WHITE)
register_text_surface = button_font.render("Register", True, WHITE)
return_text_surface = button_font.render("Return to login page", True, WHITE)
# Error message size
error_font_size = int(round(36 * scale))

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
    pygame.draw.rect(shared.screen, ORANGE, forgot_password_button)
    pygame.draw.rect(shared.screen, ORANGE, createAccount_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size, (shared.WIDTH / 2, shared.HEIGHT / 2 + (190 * scale)), "center")

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

    if forgot_password_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, forgot_password_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
            shared.game_state = "forgot_password"
            login_username_box.text = ""
            login_password_box.text = ""
            prev_mouse_click = (False, False, False)
            error_message = ""
            return

    if createAccount_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, createAccount_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            shared.game_state = "license_key"
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
    shared.screen.blit(forgot_password_text, forgot_password_text.get_rect(center=forgot_password_button.center))
    shared.screen.blit(create_acc_text_surface, create_acc_text_surface.get_rect(center=createAccount_button.center))
    prev_mouse_click = mouse_click

def license_key_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    shared.screen.blit(login_bg, (0, 0))
    license_key_box.draw(shared.screen)
    for surf, pos in license_key_guidelines_surfaces:
        shared.screen.blit(surf, pos)
    pygame.draw.rect(shared.screen, ORANGE, continue_register_button)
    pygame.draw.rect(shared.screen, ORANGE, return_login_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size,
                    (shared.WIDTH / 2, shared.HEIGHT / 2 + (270 * scale)), "center")

    if continue_register_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, continue_register_button) # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            validate_license_key(license_key_box.text)
            if shared.game_state == "register":
                license_key_box.text = ""
                prev_mouse_click = (False, False, False)
                error_message = ""
                return  # Exit early to prevent further processing

    if return_login_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, return_login_button)  # Hover effect
        if previous_mouse_pressed and not current_mouse_pressed:
        # Check if mouse was released over a button
            shared.game_state = "login"
            license_key_box.text = ""
            prev_mouse_click = (False, False, False)
            error_message = ""
            return  # Exit early to prevent further processing

    # Handle input box clicks on press
    if current_mouse_pressed and not previous_mouse_pressed:
        license_key_box.handle_mouse_click(mouse_pos)
        error_message = ""

    # Update input boxes
    license_key_box.update(current_time)

    # Button text (using pre-rendered surfaces)
    shared.screen.blit(continue_register_text_surface, continue_register_text_surface.get_rect(center=continue_register_button.center))
    shared.screen.blit(return_text_surface, return_text_surface.get_rect(center=return_login_button.center))

    prev_mouse_click = mouse_click

def registerSystem_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    # Draw background & pre-rendered guidelines
    shared.screen.blit(login_bg, (0, 0))
    for surf, pos in register_guideline_surfaces:
        shared.screen.blit(surf, pos)

    # Draw page and input boxes
    register_username_box.draw(shared.screen)
    register_password_box.draw(shared.screen)
    security_answer_box1.draw(shared.screen)
    security_dropdown1.draw(shared.screen)
    security_answer_box2.draw(shared.screen)
    security_dropdown2.draw(shared.screen)    

    # Draw buttons
    pygame.draw.rect(shared.screen, ORANGE, register_button)
    pygame.draw.rect(shared.screen, ORANGE, return_button)

    # Draw error message
    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size,(shared.WIDTH / 2, shared.HEIGHT / 2 + (270 * scale)), "center")

    # Handle dropdown interactions first
    if current_mouse_pressed and not previous_mouse_pressed:
        if security_dropdown1.handle_click(mouse_pos):
            security_dropdown2.is_open = False  # Close the other dropdown
        elif security_dropdown2.handle_click(mouse_pos):
            security_dropdown1.is_open = False  # Close the other dropdown
        else:
            # Handle other input boxes
            register_username_box.handle_mouse_click(mouse_pos)
            register_password_box.handle_mouse_click(mouse_pos)
            security_answer_box1.handle_mouse_click(mouse_pos)
            security_answer_box2.handle_mouse_click(mouse_pos)

    if register_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, register_button)  # Hover effect
    if return_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, return_button)  # Hover effect

    # Handle dropdown item selection on mouse release
    if not current_mouse_pressed and previous_mouse_pressed:
        if security_dropdown1.handle_release(mouse_pos) or security_dropdown2.handle_release(mouse_pos):
            # If an item was selected, ignore other interactions
            pass
        else:
            # Handle button interactions only if no dropdown is open
            if not security_dropdown1.is_open and not security_dropdown2.is_open:
                if register_button.collidepoint(mouse_pos):
                    if previous_mouse_pressed and not current_mouse_pressed:
                        # Check if mouse was released over a button
                        register_user(register_username_box.text, register_password_box.text, security_dropdown1.selected_question, security_answer_box1.text, security_dropdown2.selected_question, security_answer_box2.text)
                 
                if return_button.collidepoint(mouse_pos):
                    if previous_mouse_pressed and not current_mouse_pressed:
                        # Check if mouse was released over a button
                        shared.game_state = "login"
                        register_username_box.text = ""
                        register_password_box.text = ""
                        security_dropdown1.selected_question = ""
                        security_dropdown1.txt_surface = font.render("Select security question", True, GRAY)
                        security_answer_box1.text = ""
                        security_dropdown2.selected_question = ""
                        security_dropdown2.txt_surface = font.render("Select security question", True, GRAY)
                        security_answer_box2.text = ""
                        prev_mouse_click = (False, False, False)
                        error_message = ""
                        return

    # Update input boxes
    register_username_box.update(current_time)
    register_password_box.update(current_time)
    security_answer_box1.update(current_time)
    security_answer_box2.update(current_time)

    shared.screen.blit(register_text_surface, register_text_surface.get_rect(center=register_button.center))
    shared.screen.blit(return_text_surface, return_text_surface.get_rect(center=return_button.center))

    # Draw dropdown options last (only if dropdown is open)
    if security_dropdown1.is_open:
        security_dropdown1.draw_options(shared.screen)  # Draw dropdown options
    if security_dropdown2.is_open:
        security_dropdown2.draw_options(shared.screen)  # Draw dropdown options
    
    prev_mouse_click = mouse_click

def forgot_password_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message, error_color
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    shared.screen.blit(login_bg, (0, 0))
    forgot_username_box.draw(shared.screen)

    pygame.draw.rect(shared.screen, ORANGE, proceed_button)
    pygame.draw.rect(shared.screen, ORANGE, return_to_login_button)

    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size, (shared.WIDTH / 2, shared.HEIGHT / 2 + (270 * scale)), "center")

    if proceed_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, proceed_button)
        if previous_mouse_pressed and not current_mouse_pressed:
            if not forgot_username_box.text:
                error_message = "Username cannot be empty!"
                error_color = RED
            else:
                cursor.execute('SELECT security_question1, security_question2 FROM users WHERE username = ?', (forgot_username_box.text,))
                user = cursor.fetchone()
                if user:
                    shared.security_questions = user
                    shared.reset_username = forgot_username_box.text
                    shared.game_state = "reset_password"
                    forgot_username_box.text = ""
                    error_message = ""
                else:
                    error_message = "Username does not exist!"
                    error_color = RED

    if return_to_login_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, return_to_login_button)
        if previous_mouse_pressed and not current_mouse_pressed:
            shared.game_state = "login"
            forgot_username_box.text = ""
            error_message = ""

    if current_mouse_pressed and not previous_mouse_pressed:
        forgot_username_box.handle_mouse_click(mouse_pos)

    forgot_username_box.update(current_time)

    shared.screen.blit(proceed_text, proceed_text.get_rect(center=proceed_button.center))
    shared.screen.blit(return_text_surface, return_text_surface.get_rect(center=return_to_login_button.center))
    prev_mouse_click = mouse_click

def reset_password_main(mouse_pos, mouse_click):
    global prev_mouse_click, error_message, error_color
    current_time = pygame.time.get_ticks()
    current_mouse_pressed = mouse_click[0]
    previous_mouse_pressed = prev_mouse_click[0]

    shared.screen.blit(login_bg, (0, 0))

    # Display Recovery questions
    questions_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(32 * scale)))
    q1_text = questions_font.render(f"Recovery Q1: {shared.security_questions[0]}", True, WHITE)
    q2_text = questions_font.render(f"Recovery Q2: {shared.security_questions[1]}", True, WHITE)
    shared.screen.blit(q1_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 - 200*scale))
    shared.screen.blit(q2_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 - 80*scale))

    # Display New Password Instructions
    new_password_instruction_title_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(32 * scale)))
    new_password_instruction_title_text = new_password_instruction_title_font.render("Enter your new password here", True, WHITE)
    new_password_instruction_detail_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(round(26 * scale)))
    new_password_instruction_one_text = new_password_instruction_detail_font.render("-Password must contain 8-32 characters", True, WHITE)
    new_password_instruction_two_text = new_password_instruction_detail_font.render("-It can include letters, numbers, and special characters", True, WHITE)
    new_password_instruction_three_text = new_password_instruction_detail_font.render("-You must include a number, uppercase, and lowercase letter", True, WHITE)
    shared.screen.blit(new_password_instruction_title_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 + 40*scale))
    shared.screen.blit(new_password_instruction_one_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 + 140*scale))
    shared.screen.blit(new_password_instruction_two_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 + 160*scale))
    shared.screen.blit(new_password_instruction_three_text, (shared.WIDTH/2 - 400*scale, shared.HEIGHT/2 + 180*scale))


    security_answer1_reset.draw(shared.screen)
    security_answer2_reset.draw(shared.screen)
    new_password_box.draw(shared.screen)

    pygame.draw.rect(shared.screen, ORANGE, confirm_reset_button)
    pygame.draw.rect(shared.screen, ORANGE, return_to_login_button)

    if error_message:
        shared.text(shared.screen, error_message, error_color, error_font_size, (shared.WIDTH / 2, shared.HEIGHT / 2 + (270 * scale)), "center")

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
            # Approve password if have at least 1 number, lower-case and upper-case letter.
            if has_number and has_upper and has_lower:
                return True

    if confirm_reset_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, confirm_reset_button)
        if previous_mouse_pressed and not current_mouse_pressed:
            if not security_answer1_reset.text or not security_answer2_reset.text or not new_password_box.text:
                error_message = "All fields must be filled!"
                error_color = RED
            else:
                # Verify security answers and new password
                cursor.execute('SELECT security_answer1, security_answer2 FROM users WHERE username = ?', (shared.reset_username,))
                answers = cursor.fetchone()
                if bcrypt.checkpw(security_answer1_reset.text.encode('utf-8'), answers[0].encode('utf-8')) and \
                   bcrypt.checkpw(security_answer2_reset.text.encode('utf-8'), answers[1].encode('utf-8')):
                    # Verify password requirements
                    if len(new_password_box.text) < 8:
                        error_message = "Password cannot be less than 8 characters!"
                        error_color = RED
                    elif not verify_password(new_password_box.text):
                        error_message = "Password must contain 1 number, 1 uppercase letter, and 1 lowercase letter!"
                        error_color = RED
                    else:
                        # Update password
                        hashed_password = bcrypt.hashpw(new_password_box.text.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('UPDATE users SET password = ? WHERE username = ?', 
                                      (hashed_password.decode('utf-8'), shared.reset_username))
                        conn.commit()
                        error_message = "Password reset successful!"
                        error_color = GREEN
                        # shared.game_state = "login"
                        security_answer1_reset.text = ""
                        security_answer2_reset.text = ""
                        new_password_box.text = ""
                else:
                    error_message = "Security answers do not match!"
                    error_color = RED

    if return_to_login_button.collidepoint(mouse_pos):
        pygame.draw.rect(shared.screen, HOVER_COLOR, return_to_login_button)
        if previous_mouse_pressed and not current_mouse_pressed:
            shared.game_state = "login"
            security_answer1_reset.text = ""
            security_answer2_reset.text = ""
            new_password_box.text = ""
            error_message = ""

    if current_mouse_pressed and not previous_mouse_pressed:
        security_answer1_reset.handle_mouse_click(mouse_pos)
        security_answer2_reset.handle_mouse_click(mouse_pos)
        new_password_box.handle_mouse_click(mouse_pos)

    security_answer1_reset.update(current_time)
    security_answer2_reset.update(current_time)
    new_password_box.update(current_time)

    shared.screen.blit(confirm_reset_text, confirm_reset_text.get_rect(center=confirm_reset_button.center))
    shared.screen.blit(return_text_surface, return_text_surface.get_rect(center=return_to_login_button.center))
    prev_mouse_click = mouse_click
    