import pygame
from pygame.locals import *  # noqa
from LuokeCollection.main.utils import vec
from LuokeCollection.main.app import App
from LuokeCollection.settings.dev import WIDTH, HEIGHT, IMAGE


# pygame setup
pygame.init()
GAME_RESOLUTION = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(GAME_RESOLUTION)
Icon = IMAGE("icon.png")
pygame.display.set_caption("Roco Collection 洛克王國 寵物圖鑑")
pygame.display.set_icon(Icon)
pygame.mouse.set_visible(False)

# app settings
app = App(screen)
app.change_scene("init")
app.open_pop_up("splash")
clock = pygame.time.Clock()
clicked = False
mouse_pos = vec(0, 0)
pressing = False

# draw loop
running = True
while running:
    clicked = False
    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if pressing:
                clicked = event.button
                pressing = False
                # development purpose
                if clicked == 1:
                    print(str(mouse_pos) + " is clicked!")
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressing = True

    app.update(mouse_pos, clicked)
    app.display(mouse_pos, clicked)
    clock.tick(60)
    pygame.display.flip()

# app exit
app.model.stop = True
app.model.loading_thread.join()
pygame.quit()
