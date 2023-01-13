import pygame
from pygame.locals import *  # noqa
from ..utils import Mouse
from ..components.background import Background
from LuokeCollection.settings.dev import WIDTH, HEIGHT, IMAGE


class Scene:
    def __init__(
        self, screen, model, bg_file="place_holder.png", width=None, height=None
    ):
        bg = IMAGE(bg_file)
        if (width is None) or (height is None):
            self.background = Background(bg)
        else:
            self.background = Background(bg, width, height)
        self.background_music = None
        self.screen = screen
        self.model = model
        self.is_pointer = False
        self.buttons_group = pygame.sprite.Group()
        self.others_group = pygame.sprite.Group()
        self.texts_group = pygame.sprite.Group()
        self.layer_number = 6
        self.LAYERS = [{} for i in range(self.layer_number)]
        self.GROUPS = [pygame.sprite.Group() for i in range(self.layer_number)]

    def __getattr__(self, name):
        if name == "BUTTONS":
            return self.LAYERS[1]
        if name == "OTHERS":
            return self.LAYERS[2]
        if name == "TEXTS":
            return self.LAYERS[3]
        else:
            raise Exception("ATTRIBUTE NOT FOUND")

    def display(self, mouse_pos, clicked):
        self.background.draw(self.screen)
        for i in range(self.layer_number):
            self.GROUPS[i].draw(self.screen)
        Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, delta_time, mouse_pos, clicked, pressed):
        btns = self.BUTTONS.values()
        others = self.OTHERS.values()
        self.is_pointer = False
        for button in btns:
            button.hovered = False
        for button in btns:
            button.update(mouse_pos, clicked, pressed)
            if button.hovered:
                self.is_pointer = True
        for other in others:
            other.update()

    def load_items(self):
        for i in range(self.layer_number):
            self.GROUPS[i].empty()
            self.GROUPS[i].add(list(self.LAYERS[i].values()))

    def side_effect(self, **kwargs):
        self.load_items()
