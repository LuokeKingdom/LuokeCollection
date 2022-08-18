import os
import json
import pygame
from pygame.locals import *

WIDTH = 1239
HEIGHT = 826
IMAGE = lambda name, relative=True: pygame.image.load(
    os.path.join("LuokeCollection/assets/images/", name) if relative else name
)
SOUND = lambda name: os.path.join("LuokeCollection/assets/sounds/", name)


def load_json(name, relative):
    with open(
        os.path.join("LuokeCollection/assets/data/", name) if relative else name,
        encoding="utf8",
    ) as f:
        return json.load(f)


JSON = lambda name, relative=True: load_json(name, relative)
