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
game_state = "menu"

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



