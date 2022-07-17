import pygame
from pygame.locals import *
from .view import View
from .components.button import Button

class InitView(View):
  BUTTONS = {
    'collection': Button(x=100, y=100)
  }
  def __init__(self, *args, **kwargs):
    kwargs['bg'] = pygame.image.load("LuokeCollection/assets/images/init_bg.jpg")
    super(InitView, self).__init__(*args, **kwargs)