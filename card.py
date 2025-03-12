import pygame, os, random
import shared

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
            raw_image = pygame.image.load(shared.path + f"image/{image}")
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

    def draw_text_with_border(self, surface, text, font, text_color, border_color, position, border_thickness=2, align="center"):
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


    def draw_text(self, surface, text, font, text_color, position, align="center"):
        """Draws normal text without a border."""
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()

        if align == "center":
            text_rect.center = position
        elif align == "left":
            text_rect.topleft = position
        elif align == "right":
            text_rect.topright = position

        surface.blit(text_surface, text_rect)


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

        # Draw text with border effect
        self.draw_text_with_border(shared.screen, str(self.cost), card_data_font, text_color, border_color, cost_pos, align="center")
        self.draw_text_with_border(shared.screen, str(self.atk), card_data_font, text_color, border_color, atk_pos, align="center")
        self.draw_text_with_border(shared.screen, str(self.hp), card_data_font, text_color, border_color, hp_pos, align="center")
        self.draw_text_with_border(shared.screen, str(self.name), name_font, text_color, border_color, name_pos, align="center")
        self.draw_text(shared.screen, str(self.description), name_font, description_color, description_pos, align="center")




class DeckCard:
    BASE_SIZE = (145, 35)

    def __init__(self, x, y, name, cost, count=1, image=None):
        self.x = x
        self.y = y
        self.name = name
        self.cost = cost
        self.count = count  # Number of times this card appears in the deck
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, *self.BASE_SIZE)

    def draw(self, screen, font):
        # Background rectangle
        pygame.draw.rect(screen, (137, 84, 39), self.rect) 
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # White border

        # Render cost on the left
        cost_text = font.render(str(self.cost), True, (255, 255, 255))
        screen.blit(cost_text, (self.x + 5, self.y + 5))

        # Render name in the center
        name_text = font.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.x + self.BASE_SIZE[0] // 2, self.y + 15))
        screen.blit(name_text, name_rect)

        # Render count on the right (e.g., "x1" or "x2")
        #count_text = font.render(f"x{self.count}", True, (255, 255, 255))
        #screen.blit(count_text, (self.x + self.BASE_SIZE[0] - 20, self.y + 5))

        # Render count only if it's 2
        if self.count == 2:
            count_text = font.render(f"x2", True, (255, 255, 255))
            screen.blit(count_text, (self.x + self.BASE_SIZE[0] - 20, self.y + 5))

        

