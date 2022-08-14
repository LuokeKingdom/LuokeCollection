import os
import json
import pygame
from pygame.locals import *

WIDTH = 1239
HEIGHT = 826
IMAGE = lambda name: pygame.image.load(
    os.path.join("LuokeCollection/assets/images/", name)
)
SOUND = lambda name: os.path.join("LuokeCollection/assets/sounds/", name)


def load_json(name):
    with open(os.path.join("LuokeCollection/assets/data/", name), encoding="utf8") as f:
        return json.load(f)


JSON = lambda name: load_json(name)
