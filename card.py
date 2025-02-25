import pygame, os, math, random
import shared

class CardTemplate:
    CARD_SIZE = (140, 196)  # default card size

    def __init__(self, cost, atk, hp, rarity, x, y, image=None, ext=None):
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.rarity = rarity
        self.x = x
        self.y = y
        self.ext = ext or {}  # Safe dictionary handling

        # Load and scale card background based on rarity
        rarity_images = {
            "common": "Common Card.png",
            "rare": "Rare Card.png",
            "epic": "Epic Card.png",
            "legendary": "Legendary Card.png",
        }

        image_path = rarity_images.get(rarity, "Default Card.png")  # Fallback image
        self.card_bg = pygame.image.load(shared.path + f"image/{image_path}")
        self.card_bg = pygame.transform.scale(self.card_bg, self.CARD_SIZE)  # Scale to uniform size

        # Get card width and height after scaling
        self.card_width, self.card_height = self.CARD_SIZE

    def draw(self):
        """Draws the card on the screen with cost, attack, and health indicators."""
        if self.card_bg:
            shared.screen.blit(self.card_bg, (self.x, self.y))  # Draw card background

         # Define text properties
        font_size = 20
        text_color = (255, 255, 255)  # White text

        # Positions of numbers relative to card position
        cost_pos = (self.x + 21, self.y + 31)  # Top-left corner (cost)
        atk_pos = (self.x + 22, self.y + self.card_height - 16)  # Bottom-left corner (attack)
        hp_pos = (self.x + self.card_width - 19, self.y + self.card_height - 15)  # Bottom-right corner (health)

        # Draw only the numbers without any background circles
        shared.text(shared.screen, str(self.cost), text_color, font_size, cost_pos, "center")
        shared.text(shared.screen, str(self.atk), text_color, font_size, atk_pos, "center")
        shared.text(shared.screen, str(self.hp), text_color, font_size, hp_pos, "center")