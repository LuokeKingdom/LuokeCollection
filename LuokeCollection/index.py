import pygame
from pygame.locals import *
from LuokeCollection.main.scenes.utils import vec
from main.app import App
from settings.dev import WIDTH, HEIGHT, IMAGE


# pygame setup
pygame.init()
GAME_RESOLUTION = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(GAME_RESOLUTION)
Icon = pygame.image.load(IMAGE("icon.png"))
pygame.display.set_caption("Roco Collection 洛克王國 寵物圖鑑")
pygame.display.set_icon(Icon)
pygame.mouse.set_visible(False)

# app settings
app = App(screen)
app.change_scene("init")
clock = pygame.time.Clock()
click_pos = vec(-1000, -1000)
mouse_pos = vec(0, 0)
pressing = False

# draw loop
running = True
while running:
    click_pos.x, click_pos.y = -1000, -1000
    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if pressing:
                click_pos.x, click_pos.y = event.pos
                pressing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressing = True

    app.update(mouse_pos, click_pos)
    app.display(mouse_pos, click_pos)
    clock.tick(60)
    pygame.display.flip()

# app exit
pygame.quit()
