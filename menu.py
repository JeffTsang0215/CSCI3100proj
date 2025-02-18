import pygame, os, math, random
import shared


menu_bg = pygame.image.load(shared.path + "image/hearthstone background.png")
menu_bg = pygame.transform.scale(menu_bg, (shared.WIDTH, shared.HEIGHT))
button_color = (137,84,39)
hover_color = (204,134,76)
border_color = (255, 255, 0)  # Yellow border color
border_thickness = round(0.005 * shared.HEIGHT) # Border thickness
buttons = [
    [(0.42*shared.WIDTH , 0.33*shared.HEIGHT), (0.44*shared.WIDTH, 0.28*shared.HEIGHT), (0.565*shared.WIDTH, 0.28*shared.HEIGHT), (0.58*shared.WIDTH, 0.33*shared.HEIGHT)],  # Button 1
    [(0.415*shared.WIDTH, 0.345*shared.HEIGHT), (0.40*shared.WIDTH, 0.40*shared.HEIGHT), (0.60*shared.WIDTH, 0.40*shared.HEIGHT),(0.585*shared.WIDTH, 0.345*shared.HEIGHT)],  # Button 2
    [(0.40*shared.WIDTH, 0.42*shared.HEIGHT), (0.42*shared.WIDTH, 0.48*shared.HEIGHT), (0.58*shared.WIDTH, 0.48*shared.HEIGHT),(0.60*shared.WIDTH, 0.42*shared.HEIGHT)],  # Button 3
    #[(200, 450), (400, 450), (370, 500), (230, 500)],  # Button 4
]

def menu_main(mouse_pos, mouse_click):
    shared.screen.blit(menu_bg,(0,0))

    for i, button in enumerate(buttons):
        # Check if mouse is inside the trapezium
        polygon_rect = pygame.draw.polygon(shared.screen, button_color, button)
        if polygon_rect.collidepoint(mouse_pos):
            pygame.draw.polygon(shared.screen, hover_color, button)  # Hover effect
            if mouse_click[0]:  # Left mouse button clicked
                pygame.draw.polygon(shared.screen, border_color, button, border_thickness)  # Click effect
                print(f"Button {i+1} clicked!")

    shared.text(shared.screen, "Play Game", (0, 0, 0), int(shared.WIDTH/64), (0.50*shared.WIDTH, 0.305*shared.HEIGHT), "center")

