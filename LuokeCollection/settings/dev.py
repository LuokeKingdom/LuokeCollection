import os
import json
import pygame
from pygame.locals import *  # noqa
from ..main.model.sound import Sound

WIDTH = 1239
HEIGHT = 826
PORT = 5050


def IMAGE(name, relative=True):
    return pygame.image.load(
        (os.path.join("assets/images/", name) if relative else name)
    )


def SOUND(name, channel):
    return Sound(os.path.join("assets/sounds/", name), channel)


def JSON(name, relative=True):
    with open(
        os.path.join("assets/data/", name) if relative else name,
        encoding="utf8",
    ) as f:
        return json.load(f)
