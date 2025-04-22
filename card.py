import pygame, os, random
import shared

scale1 = shared.WIDTH / 1080
scale2 = shared.HEIGHT / 675

class CardTemplate:
    BASE_SIZE = (140, 196)

    def __init__(self, cost, atk, hp, name, rarity, x, y, description, scale_factor=1.0, image=None, ext=None):
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.name = name
        self.rarity = rarity
        self.description = description
        self.scale_factor = scale_factor
        self.ext = ext or {}
        self.x, self.y = x, y

        self.card_width = int(self.BASE_SIZE[0] * scale_factor)
        self.card_height = int(self.BASE_SIZE[1] * scale_factor)
        self.rect = pygame.Rect(self.x, self.y, self.card_width, self.card_height)
        self.add_rect = pygame.Rect(self.x + self.BASE_SIZE[0] // 2 , self.y + self.BASE_SIZE[1] + int(25 * scale2), int(25 * scale1), int(25 * scale2))

        # Prepare static background
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
            mask = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            pygame.draw.ellipse(mask, (255, 255, 255, 255), (0, 0, image_width, image_height))
            self.card_image = raw_image.copy()
            self.card_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.image_x = (self.card_width - image_width) // 2 + 3
            self.image_y = int(13 * self.scale_factor)

        self.cached_surface = None
        self.generate_surface()

    def generate_surface(self):
        """Pre-renders the card into a surface."""
        self.cached_surface = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
        if not os.path.exists(shared.path + "fonts/belwe-bold-bt.ttf"):
            print("Missing font.")
            return

        font_path = os.path.join(shared.path, "fonts", "belwe-bold-bt.ttf")
        card_data_font = pygame.font.Font(font_path, int(28 * self.scale_factor))
        name_font = pygame.font.Font(font_path, int(10 * self.scale_factor))
        description_font = pygame.font.Font(font_path, int(10 * self.scale_factor))

        text_color = (255, 255, 255)
        border_color = (0, 0, 0)
        description_color = (0, 0, 0)

        cost_pos = (int(20 * self.scale_factor), int(28 * self.scale_factor))
        atk_pos = (int(22 * self.scale_factor), self.card_height - int(20 * self.scale_factor))
        hp_pos = (self.card_width - int(18 * self.scale_factor), self.card_height - int(18 * self.scale_factor))
        name_pos = (self.card_width // 2, int(107 * self.scale_factor))
        description_pos = (self.card_width // 2, int(150 * self.scale_factor))

        
        if self.card_image:
            self.cached_surface.blit(self.card_image, (self.image_x, self.image_y))
        self.cached_surface.blit(self.card_bg, (0, 0))

        shared.draw_text_with_border(self.cached_surface, str(self.cost), card_data_font, text_color, border_color, cost_pos, align="center")
        shared.draw_text_with_border(self.cached_surface, str(self.atk), card_data_font, text_color, border_color, atk_pos, align="center")
        shared.draw_text_with_border(self.cached_surface, str(self.hp), card_data_font, text_color, border_color, hp_pos, align="center")
        shared.draw_text_with_border(self.cached_surface, self.name, name_font, text_color, border_color, name_pos, align="center")
        shared.draw_text(self.cached_surface, self.description, description_font, description_color, description_pos, align="center")

    def draw(self, surface=None):
        if surface is None:
            surface = shared.screen
        surface.blit(self.cached_surface, (self.x, self.y))

    def draw_plus_button(self, mouse_pos):
        color = (180, 220, 180) if self.add_rect.collidepoint(mouse_pos) else (100, 200, 100)
        pygame.draw.rect(shared.screen, color, self.add_rect)
        font = pygame.font.Font(None, 24)
        plus_text = font.render("+", True, (255, 255, 255))
        plus_text_rect = plus_text.get_rect(center=self.add_rect.center)
        shared.screen.blit(plus_text, plus_text_rect)




        

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



