import pygame, os, random
import shared

scale1 = shared.WIDTH / 1080
scale2 = shared.HEIGHT / 675

class CardTemplate:
    BASE_SIZE = (140, 196)  # Base card size

    def __init__(self, cost, atk, hp, name, rarity, x, y, description, scale_factor=1.0, image=None, ext=None):
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.name = name
        self.rarity = rarity
        self.description = description
        self.scale_factor = scale_factor
        self.ext = ext or {}

        # Scale the card dimensions
        self.card_width = int(self.BASE_SIZE[0] * scale_factor)
        self.card_height = int(self.BASE_SIZE[1] * scale_factor)

        # Card position
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.card_width, self.card_height)
        self.add_rect = pygame.Rect(self.x + self.BASE_SIZE[0] // 2 , self.y + self.BASE_SIZE[1] + int(25 * scale2), int(25 * scale1), int(25 * scale2))
        # Load and scale card background based on rarity
        rarity_images = {
            "common": "CommonCard.png",
            "rare": "RareCard.png",
            "epic": "EpicCard.png",
            "legendary": "LegendaryCard.png",
        }
        image_path = rarity_images.get(rarity, "Default Card.png")
        self.card_bg = pygame.image.load(shared.path + f"image/{image_path}")
        self.card_bg = pygame.transform.scale(self.card_bg, (self.card_width, self.card_height))

        self.card_image = None
        if image:
            raw_image = pygame.image.load(shared.path + f"image/{image}").convert_alpha()
            image_width = int(self.card_width * 0.65)
            image_height = int(self.card_height * 0.6)
            raw_image = pygame.transform.scale(raw_image, (image_width, image_height))

            # Create an oval mask
            mask = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            pygame.draw.ellipse(mask, (255, 255, 255, 255), (0, 0, image_width, image_height))

            # Apply the mask to the image
            self.card_image = raw_image.copy()
            self.card_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Position image on the card
            self.image_x = self.x + (self.card_width - image_width) // 2 + 3
            self.image_y = self.y + int(13 * self.scale_factor)


    def draw(self):
        """Draws the card with its image, background, and text indicators."""
        if self.card_image:
            shared.screen.blit(self.card_image, (self.image_x, self.image_y))

        if self.card_bg:
            shared.screen.blit(self.card_bg, (self.x, self.y))

        # Load font
        font_path = os.path.join(shared.path, "fonts", "belwe-bold-bt.ttf")
        if not os.path.exists(font_path):
            print(f"Error: Font not found at {font_path}")  # Debugging message
            return  # Stop execution if font is missing

        card_data_font = pygame.font.Font(font_path, int(28 * self.scale_factor))
        name_font = pygame.font.Font(font_path, int(10 * self.scale_factor))
        description_font = pygame.font.Font(font_path, int(10 * self.scale_factor))

        text_color = (255, 255, 255)  # White text
        border_color = (0, 0, 0)  # Black outline
        description_color = (0, 0, 0)

        # Scale positions
        cost_pos = (self.x + int(20 * self.scale_factor), self.y + int(28 * self.scale_factor))
        atk_pos = (self.x + int(22 * self.scale_factor), self.y + self.card_height - int(20 * self.scale_factor))
        hp_pos = (self.x + self.card_width - int(18 * self.scale_factor), self.y + self.card_height - int(18 * self.scale_factor))
        name_pos = (self.x + self.card_width // 2, self.y + int(107 * self.scale_factor))
        description_pos = (self.x + self.card_width // 2, self.y + int(150 * self.scale_factor))

        # Draw text with border effect using shared function
        shared.draw_text_with_border(shared.screen, str(self.cost), card_data_font, text_color, border_color, cost_pos, align="center")
        shared.draw_text_with_border(shared.screen, str(self.atk), card_data_font, text_color, border_color, atk_pos, align="center")
        shared.draw_text_with_border(shared.screen, str(self.hp), card_data_font, text_color, border_color, hp_pos, align="center")
        shared.draw_text_with_border(shared.screen, self.name, name_font, text_color, border_color, name_pos, align="center")
        shared.draw_text(shared.screen, self.description, description_font, description_color, description_pos, align="center")

    def draw_plus_button(self, mouse_pos):  
            if self.add_rect.collidepoint(mouse_pos):
                add_rect_color = (180, 220, 180)  # Lighter green when hovered
            else:
                add_rect_color = (100, 200, 100)  # Default green

            pygame.draw.rect(shared.screen, add_rect_color, self.add_rect)  # Draw button

            # Render the "+" text
            font = pygame.font.Font(None, 24)
            plus_text = font.render("+", True, (255, 255, 255))  # White text
            plus_text_rect = plus_text.get_rect(center=self.add_rect.center)  # Center text

            shared.screen.blit(plus_text, plus_text_rect)  # Draw text on button



        

class DeckCard:
    BASE_SIZE = (126*scale1, 30*scale2)

    def __init__(self, x, y, name, rarity,  cost, count=1):
        self.x = x
        self.y = y
        self.name = name
        self.cost = cost
        self.count = count  
        self.rect = pygame.Rect(self.x, self.y, *self.BASE_SIZE)
        self.countrect = pygame.Rect(self.x + self.BASE_SIZE[0] - self.BASE_SIZE[1] + 5*scale1, self.y + 2*scale2, self.BASE_SIZE[1] - 7*scale1, self.BASE_SIZE[1] - 3*scale1)
        self.rarity = rarity

        # Define cancel button area 
        self.cancel_rect = pygame.Rect(self.x + self.BASE_SIZE[0], self.y, 30, 30)

    def draw(self, screen, mouse_pos):
        # Create fontsd
        deck_name_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(10*scale1))  
        cost_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(24*scale1))  # Larger font for cost
        count_font = pygame.font.Font("fonts/belwe-bold-bt.ttf", int(14*scale1))  

        text_color = (255, 255, 255) 
        border_color = (0, 0, 0)  
        count_color = (255, 215, 0)

        # Background rectangle
        pygame.draw.rect(screen, (137, 84, 39), self.rect)  
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border

        # Load and draw the mana image
        mana_image = pygame.image.load(shared.path + "image/ManaT.png")
        mana_image = pygame.transform.scale(mana_image, (30*scale1, 30*scale2))  
        screen.blit(mana_image, (self.x - 10 * scale1, self.y))  
        star_image = pygame.image.load(shared.path + f"image/legendary star.png")

        star_width = self.BASE_SIZE[1] * 0.4
        star_height = self.BASE_SIZE[1] * 0.4

        star_image = pygame.transform.scale(star_image, (star_width, star_height))

        # Draw cost with border
        cost_pos = (self.x + 5 * scale1, self.y + 14 * scale2)
        shared.draw_text_with_border(screen, str(self.cost), cost_font, text_color, border_color, cost_pos, align="center")

        # Draw name with border
        name_pos = (self.x + self.BASE_SIZE[0] // 2 - 43*scale1, self.y + self.BASE_SIZE[1] // 2 - 7*scale2)
        shared.draw_text_with_border(screen, self.name, deck_name_font, text_color, border_color, name_pos, align="left")

        if self.rarity == "legendary":
            # Draw a star symbol ★ 
            pygame.draw.rect(screen, (117, 64, 19), self.countrect)
            screen.blit(star_image, (self.x + self.BASE_SIZE[0] - 18*scale1, self.y + 9*scale2))
        
          # Draw count if it's 2
        elif self.count == 2:
            pygame.draw.rect(screen, (117, 64, 19), self.countrect)
            count_pos = (self.x + self.BASE_SIZE[0] - 13*scale1, self.y + 15*scale2)
            shared.draw_text(screen, "2", count_font, count_color, count_pos, align='center')

        # Change cancel button color on hover
        cancel_text_color = (255, 255, 255)  
        if self.cancel_rect.collidepoint(mouse_pos):
            cancel_text_color = (255, 50, 50)  # Red when hovered

        # Render "-" using shared.text
        shared.text(screen, "-", cancel_text_color, int(20 * scale1), 
            [self.x + self.BASE_SIZE[0] + 10*scale1, self.y + 17*scale2], "center") 


    def handle_event(self, event, deck):
        """Check if the cancel button is clicked and remove the card from the deck."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            if self.cancel_rect.collidepoint(event.pos):
                if self.name in deck["cards"]:
                    deck["cards"].remove(self.name)  # Remove one occurrence
                    print(f"Removed {self.name} from deck")
                    return True  # Indicate the card was removed
        return False



