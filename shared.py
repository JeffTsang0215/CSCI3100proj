import pygame, os, math, random

pygame.init()
path = os.path.dirname(os.path.abspath(__file__)) + '/'

renewed = False

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
fullscreen = False

if not(fullscreen):
    if WIDTH > HEIGHT:
        HEIGHT *= 3/4 
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

# game_state = "playing"
game_state = "login"

def text(screen, text, color, size, pos, align="left", font=None):
    text = text.encode("utf-8").decode("utf-8")
    
    # Use custom font if provided; otherwise, use system/default font
    if font is None:
        try:
            my_font = pygame.font.SysFont(pygame.font.get_fonts()[2], size)
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


def draw_text(surface, text, font, text_color, position, align="center"):
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



