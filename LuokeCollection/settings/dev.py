import os
import json
import pygame
from pygame.locals import *
from ..main.model.sound import Channel, Sound

WIDTH = 1239
HEIGHT = 826
IMAGE = lambda name, relative=True: pygame.image.load(
    (os.path.join("assets/images/", name) if relative else name)
)
SOUND = lambda name, channel: Sound(os.path.join("assets/sounds/", name), channel)


def load_json(name, relative):
    with open(
        os.path.join("assets/data/", name) if relative else name,
        encoding="utf8",
    ) as f:
        return json.load(f)


JSON = lambda name, relative=True: load_json(name, relative)
