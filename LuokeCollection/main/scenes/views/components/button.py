import pygame
from pygame.locals import *
from ...utils import vec
from .container import Container

class Button(Container):
    def __init__(self, *args, **kwargs):
        # Default button
        if len(args) < 1 and not kwargs.get('image'):
            image = pygame.Surface([100,100])
            image.fill((255,255,255))
            kwargs['image'] = image
        super().__init__(*args, **kwargs)
        self.on_click = None
    
    def is_click(self, click_pos):
        return self.rect.collidepoint(click_pos)
    
    def click(self):
        if self.on_click:
            self.on_click()

    def update(self):
        # can be used for animation probably
        pass