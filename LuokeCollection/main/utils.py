import pygame
from pygame.locals import *  # noqa
from LuokeCollection.settings.dev import IMAGE
from collections import namedtuple
import os


def save_file(pathname, content):
    f = open(os.path.join(pathname), "w", encoding="utf8")
    f.write(content)
    f.close()


SkillInfo = namedtuple(
    "SkillInfo",
    ["name", "type", "power", "PP", "effect"],
)

PetInfo = namedtuple(
    "PetInfo",
    [
        "name",
        "element",
        "secondary_element",
        "number",
        "weight",
        "height",
        "desc",
        "stats",
        "skills",
        "path",
    ],
)

ELEMENT = namedtuple("ELEMENT", ["image", "color"])

ELEMENT_FILES = {
    "草": "elements/grass.png",
    "火": "elements/fire.png",
    "翼": "elements/air.png",
    "虫": "elements/bug.png",
    "恶魔": "elements/demon.png",
    "土": "elements/dirt.png",
    "龙": "elements/dragon.png",
    "武": "elements/fight.png",
    "幽灵": "elements/ghost.png",
    "神火": "elements/godfire.png",
    "神草": "elements/godgrass.png",
    "神水": "elements/godwater.png",
    "萌": "elements/heart.png",
    "冰": "elements/ice.png",
    "光": "elements/light.png",
    "电": "elements/lightening.png",
    "机械": "elements/mech.png",
    "毒": "elements/poison.png",
    "普通": "elements/regular.png",
    "石": "elements/rock.png",
    "水": "elements/water.png",
}
ELEMENT2COLOR = {
    "幽灵": (172, 140, 140),
    "草": (130, 182, 64),
    "火": (246, 102, 18),
    "翼": (165, 156, 223),
    "虫": (189, 218, 126),
    "恶魔": (214, 111, 110),
    "土": (169, 133, 106),
    "龙": (231, 179, 91),
    "武": (219, 108, 45),
    "神火": (241, 167, 82),
    "神草": (165, 225, 114),
    "神水": (130, 208, 245),
    "萌": (244, 77, 149),
    "冰": (200, 234, 243),
    "光": (225, 128, 12),
    "电": (247, 165, 1),
    "机械": (176, 177, 182),
    "毒": (130, 150, 158),
    "普通": (251, 217, 42),
    "石": (166, 156, 120),
    "水": (108, 206, 246),
}


def add_average_color(image_map):
    def get_color(img):
        color_sum_r = 0
        color_sum_g = 0
        color_sum_b = 0
        color_sum_a = 0
        w, h = img.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = img.get_at((x, y))
                color_sum_a += a / 255
                color_sum_r += r * a / 255
                color_sum_g += g * a / 255
                color_sum_b += b * a / 255
        return tuple(
            map(lambda x: int(x / color_sum_a), [color_sum_r, color_sum_g, color_sum_b])
        )

    for key in image_map:
        print('"' + key + '": ' + str(get_color(image_map[key].image)) + ",")

    return image_map


ELEMENT_MAP = {
    key: ELEMENT(IMAGE(val), ELEMENT2COLOR[key]) for key, val in ELEMENT_FILES.items()
}


def type2element(t):
    if t[1] == "系":
        return t[0]
    return t[:2]


class vec(list):
    def __init__(self, x, y=0):
        if isinstance(x, list) or isinstance(x, tuple):
            super().__init__(x)
        else:
            super().__init__([x, y])

    def __getattr__(self, name: str):
        if name == "x":
            return self[0]
        elif name == "y":
            return self[1]

    def __setattr__(self, name: str, value):
        if name == "x":
            self[0] = value
        elif name == "y":
            self[1] = value

    def __str__(self):
        return f"<{self.x}, {self.y}>"

    def __add__(self, other):
        if isinstance(other, vec):
            return vec(self[0] + other[0], self[1] + other[1])
        return None

    def __sub__(self, other):
        if isinstance(other, vec):
            return vec(self[0] - other[0], self[1] - other[1])
        return None

    def __mul__(self, other):
        if isinstance(other, vec):
            return vec(self[0] * other[0], self[1] * other[1])
        else:
            # scalar
            return vec(self[0] * other, self[1] * other)

    # def __mod__(self, other):
    #     if isinstance(other, vec):
    #         # cross product
    #         return self.x*other.y - self.y*other.x
    #     return None

    def __truediv__(self, other):
        if isinstance(other, vec):
            if other[0] * other[1] == 0:
                return None
            return vec(self[0] / other[0], self[1] / other[1])
        else:
            # scalar
            return vec(self[0] / other, self[1] / other)

    def map(self, func):
        return vec(func(self[0]), func(self[1]))

    def unit(self):
        return self / self.length()

    def length(self):
        return (self[0] ** 2 + self[1] ** 2) ** 0.5


class Mouse:
    cursor_arrow = pygame.transform.scale(IMAGE("cursor.png"), (36, 54))
    cursor_hand = pygame.transform.scale(IMAGE("hand.png"), (48, 54))

    def draw(screen, mouse_pos, is_pointer):
        screen.blit(Mouse.cursor_hand if is_pointer else Mouse.cursor_arrow, mouse_pos)
        pass
