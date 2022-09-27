import copy
from .sound import Channel
from ..utils import PetInfo, SkillInfo
import os
import json
import threading
from ...settings.dev import IMAGE, JSON, SOUND
from ..utils import save_file

import pygame
from pygame.locals import *  # noqa


class Model:
    PETS = {}
    DATA = None

    def __init__(self, app):
        self.app = app
        self.load_pets()
        self.load_current_data()
        self.error_sound = SOUND("click-error.wav", Channel.GAME)
        self.saved_sound = SOUND("saved.wav", Channel.GAME)
        self.pet_page_number = 1
        self.MAX_PAGE = len(self.PETS) // 9 + (0 if len(self.PETS) % 9 == 0 else 1)
        self.MAX_SKILL_PAGE = 0
        self.pet_select_rect = None
        self.pet_number_training = 1
        self.skill_page_number = 1

        self.pet_rects = {}

        def load_pet_rects_async():
            for pet_number in range(1, len(self.PETS) + 1):
                if self.stop:
                    return
                self._load_pet_rect(pet_number)

        self.loading_thread = threading.Thread(target=load_pet_rects_async)
        self.stop = False
        self.loading_thread.start()

    def close(self):
        self.app.pop_scene()

    def open(self, name):
        self.app.push_scene(name)

    def close_pop_up(self):
        self.app.close_pop_up()

    def get_scene(self):
        return self.app.scene

    def load_pets(self):
        for i in range(201):
            try:
                info_path = os.path.join(str(i).zfill(4), "info.json")
                skill_path = os.path.join(str(i).zfill(4), "skills.json")
                info = JSON(info_path)
                info["skills"] = list(map(lambda x: SkillInfo(**x), JSON(skill_path)))
                info["secondary_element"] = info.get("secondary_element")
                info["path"] = str(i).zfill(4)
                self.PETS[info["number"]] = PetInfo(**info)
            except Exception:
                continue

    def load_current_data(self):
        self.DATA = JSON("assets/data.json", False)
        a = copy.copy(self.DATA.get("pet_rects"))
        if a is None:
            return
        for i in a:
            del self.DATA["pet_rects"][i]
            self.DATA["pet_rects"][int(i)] = a[i]

    # collection
    def set_page(self):
        pet_page = []
        for i in range(9):
            pet_number = self.pet_page_number * 9 + i - 8
            if self.PETS.get(pet_number) is None:
                break
            pet_page.append(self.PETS[pet_number])
        self.get_scene().set_page(pet_page)

    def set_info(self, offset=None):
        if offset is not None:
            self.pet_number_training = (self.pet_page_number - 1) * 9 + offset
        self.get_scene().set_info(self.PETS[self.pet_number_training])

    def previous_page(self):
        if self.pet_page_number == 1:
            self.error_sound.play()
            return
        self.pet_page_number -= 1
        self.set_page()

    def next_page(self):
        if self.pet_page_number == self.MAX_PAGE:
            self.error_sound.play()
            return
        self.pet_page_number += 1
        self.set_page()

    # select_rect
    def set_pet_select_rect(self):
        self.pet_select_rect = self.PETS[self.pet_number_training]
        image_path = os.path.join(
            "assets/data/", self.pet_select_rect.path, "display.png"
        )
        scene = self.get_scene()
        scene.set_pet_image(IMAGE(image_path, False))
        self.DATA["pet_rects"] = self.DATA.get("pet_rects", {})
        scene.rect = self.DATA["pet_rects"].get(self.pet_number_training)
        scene.TEXTS["warning"].change_text("")

    def _load_pet_rect(self, pet_number):
        pet_info = self.PETS[pet_number]
        pet_image = IMAGE(
            os.path.join("assets/data/", pet_info.path, "display.png"),
            False,
        )
        self.DATA["pet_rects"] = self.DATA.get("pet_rects", {})
        rect = self.DATA["pet_rects"].get(pet_info.number)
        if rect:
            canvas = pygame.Surface([rect[2], rect[2]], pygame.SRCALPHA)
            canvas.blit(pet_image.subsurface(*rect), (0, 0))
            pet_image = pygame.transform.smoothscale(canvas, (100, 100))
        self.pet_rects[pet_number] = pet_image if rect else None

    def save_rect(self, x, y, w, h):
        self.DATA["pet_rects"] = self.DATA.get("pet_rects", {})
        pet_num = int(self.pet_number_training)

        if self.DATA["pet_rects"].get(pet_num) is None:
            self.DATA["pet_rects"][pet_num] = [x, y, w, h]
        else:
            del self.DATA["pet_rects"][pet_num]
            self.DATA["pet_rects"][pet_num] = [x, y, w, h]

        content = json.dumps(self.DATA, ensure_ascii=False)
        save_file("assets/data.json", content)
        self._load_pet_rect(pet_num)

    # training
    def load_skills(self):
        pet_info = self.PETS[self.pet_number_training]
        scene = self.get_scene()
        for i in range(4, 8):
            try:
                scene.set_skill(i, pet_info.skills[self.skill_page_number * 4 + i - 8])
            except:
                scene.set_skill(i, None)
        self.MAX_SKILL_PAGE = len(pet_info.skills) // 4 + (
            0 if len(pet_info.skills) % 4 == 0 else 1
        )

    def previous_skill_page(self):
        if self.skill_page_number == 1:
            self.error_sound.play()
            return
        self.skill_page_number -= 1
        self.load_skills()

    def next_skill_page(self):
        if self.skill_page_number == self.MAX_SKILL_PAGE:
            self.error_sound.play()
            return
        self.skill_page_number += 1
        self.load_skills()
