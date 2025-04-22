import pygame, os, math, random
import shared

bg = pygame.image.load(shared.path + "image/choosedeck.png")
bg = pygame.transform.scale(bg, (shared.WIDTH, shared.HEIGHT))

def main(mouse_pos, mouse_click):
    shared.screen.blit(bg,(0,0))