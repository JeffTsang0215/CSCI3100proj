import pygame, os, math, random
import shared

class CardTemplate:
    BASE_SIZE = (140, 196)  # Base card size

    def __init__(self, cost, atk, hp, name, rarity, description, x, y, scale_factor=1.0, image=None, ext=None):
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

        # Scale the card's position (ensuring it remains centered)
        self.x = x
        self.y = y

        # Load and scale card background based on rarity
        rarity_images = {
            "common": "Common Card.png",
            "rare": "Rare Card.png",
            "epic": "Epic Card.png",
            "legendary": "Legendary Card.png",
        }
        image_path = rarity_images.get(rarity, "Default Card.png")  
        self.card_bg = pygame.image.load(shared.path + f"image/{image_path}")
        self.card_bg = pygame.transform.scale(self.card_bg, (self.card_width, self.card_height))

    def draw(self):
        """Draws the card on the screen with cost, attack, and health indicators."""
        if self.card_bg:
            shared.screen.blit(self.card_bg, (self.x, self.y))  

        # Define text properties
        font_size = int(20 * self.scale_factor)  # Scale text size
        text_color = (255, 255, 255)
        name_font_size = int(10 * self.scale_factor)
        description_color = (0,0,0)  

        # Scale positions relative to the card
        cost_pos = (self.x + int(21 * self.scale_factor), self.y + int(31 * self.scale_factor))
        atk_pos = (self.x + int(22 * self.scale_factor), self.y + self.card_height - int(16 * self.scale_factor))
        hp_pos = (self.x + self.card_width - int(18 * self.scale_factor), self.y + self.card_height - int(15 * self.scale_factor))
        name_pos = (self.x + self.card_width // 2, self.y + int(107 * self.scale_factor))
        description_pos = (self.x + int(40 * self.scale_factor), self.y + int(150 * self.scale_factor))
    
        # Draw the scaled text positions
        shared.text(shared.screen, str(self.cost), text_color, font_size, cost_pos, "center")
        shared.text(shared.screen, str(self.atk), text_color, font_size, atk_pos, "center")
        shared.text(shared.screen, str(self.hp), text_color, font_size, hp_pos, "center")
        shared.text(shared.screen, str(self.name), text_color, name_font_size, name_pos, "center")
        shared.text(shared.screen, str(self.description), description_color, name_font_size, description_pos, "left")


