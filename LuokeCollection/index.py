from re import A
import pygame
from pygame.locals import *
from main import *

pygame.init()
GAME_RESOLUTION = (1080, 720)
black = (0, 0, 0)
screen = pygame.display.set_mode(GAME_RESOLUTION)
Icon = pygame.image.load("assets\png\icon.png")
pet = pygame.transform.scale(
    pygame.image.load("assets/png/display.png"), (103.8, 148.9)
)
pygame.display.set_caption("Roco Collection 洛克王國 寵物圖鑑")
pygame.display.set_icon(Icon)
positions = []

running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                positions.append(event.pos)
            elif event.button == 3:
                positions.clear()
                screen.fill(black)

    for position in positions:
        screen.blit(pet, position)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
