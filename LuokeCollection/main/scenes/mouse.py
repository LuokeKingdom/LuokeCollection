import pygame
from pygame.locals import *
from settings.dev import WIDTH, HEIGHT, IMAGE

class Mouse:
    cursor_arrow = pygame.transform.scale(
        pygame.image.load(IMAGE('cursor.png')),
        (36, 54)
    )
    cursor_hand = pygame.transform.scale(
        pygame.image.load(IMAGE('hand.png')),
        (48, 54)
    )
    
    def draw(screen, mouse_pos, pointer):
        screen.blit(Mouse.cursor_hand if pointer else Mouse.cursor_arrow, mouse_pos)
        pass
