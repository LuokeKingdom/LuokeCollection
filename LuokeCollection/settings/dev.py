import os
import pygame
from pygame.locals import *

WIDTH = 1239
HEIGHT = 826
IMAGE = lambda name: pygame.image.load(
    os.path.join("LuokeCollection/assets/images/", name)
)
SOUND = lambda name: os.path.join("LuokeCollection/assets/sounds/", name)
