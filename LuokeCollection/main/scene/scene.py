import pygame
from pygame.locals import *  # noqa
from ..utils import Mouse
from ..components.button import Button
from ..components.background import Background
from LuokeCollection.settings.dev import WIDTH, HEIGHT


class Scene:
    def __init__(self, screen, model, bg=None):
        if not bg:
            bg = pygame.Surface([WIDTH, HEIGHT])
            bg.fill((0, 0, 0))
        self.background = Background(bg)
        self.background_music = None
        self.screen = screen
        self.model = model
        self.is_pointer = False
        self.buttons_group = pygame.sprite.Group()
        self.others_group = pygame.sprite.Group()
        self.texts_group = pygame.sprite.Group()
        self.BUTTONS = {
            "pop": Button(x=700, y=100, on_click=lambda: self.model.close())
        }
        self.OTHERS = {}
        self.TEXTS = {}

    def display(self, mouse_pos, clicked):
        self.background.draw(self.screen)
        self.buttons_group.draw(self.screen)
        self.others_group.draw(self.screen)
        self.texts_group.draw(self.screen)
        Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, mouse_pos, clicked, pressed):
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
        self.buttons_group.empty()
        self.others_group.empty()
        self.texts_group.empty()
        self.others_group.add(list(self.OTHERS.values()))
        self.buttons_group.add(list(self.BUTTONS.values()))
        self.texts_group.add(list(self.TEXTS.values()))

    def side_effect(self):
        self.load_items()
