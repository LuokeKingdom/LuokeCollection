from re import A
import pygame
from pygame.locals import *
from LuokeCollection.main.scenes.utils import vec
from main import *
from main.app import App

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

app = App(screen)
app.change_scene('basic')
clock = pygame.time.Clock()
click_pos = vec(-1000,-1000)
pressing = False

running = True
while running:
    # Did the user click the window close button?
    click_pos.x = -1000
    click_pos.y = -1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # if event.button == 1:
            #     positions.append(event.pos)
            # elif event.button == 3:
            #     positions.clear()
            #     screen.fill(black)
            if pressing:
                click_pos.x = event.pos[0]
                click_pos.y = event.pos[1]
                pressing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressing = True
        

    # for position in positions:
    #     screen.blit(pet, position)
    

    app.update(click_pos)
    app.display()
    clock.tick(60)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
