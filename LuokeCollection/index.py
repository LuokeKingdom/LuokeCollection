import pygame
from pygame.locals import *
from LuokeCollection.main.scenes.utils import vec
from main.app import App
from settings.dev import WIDTH, HEIGHT


pygame.init()
black = (0, 0, 0)
GAME_RESOLUTION = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(GAME_RESOLUTION)
Icon = pygame.image.load("assets\png\icon.png")
cursor_arrow = pygame.transform.scale(
    pygame.image.load("assets/png/cursor.png"), (36, 54)
)
cursor_hand = pygame.transform.scale(
    pygame.image.load("assets/png/hand.png"), (48, 54)
)

pygame.display.set_caption("Roco Collection 洛克王國 寵物圖鑑")
pygame.display.set_icon(Icon)
positions = []
pygame.mouse.set_visible(False)

app = App(screen)
app.change_scene("init")
clock = pygame.time.Clock()
click_pos = vec(-1000, -1000)
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
    screen.blit(cursor_arrow, pygame.mouse.get_pos())
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
