import copy
from LuokeCollection.main.utils import PetInfo
import os
import json
from LuokeCollection.settings.dev import IMAGE, JSON
from ..utils import save_file


class Model:
    PETS = {}
    DATA = None

    def __init__(self, app):
        self.page_number = 1
        self.app = app
        self.load_pets()
        self.load_current_data()
        self.pet_select_rect = None
        self.pet_number_select_rect = 1

    def close(self):
        self.app.pop_scene()

    def open(self, name):
        self.app.push_scene(name)

    def get_scene(self):
        return self.app.scene

    def load_pets(self):
        for i in range(201):
            try:
                info_path = os.path.join(str(i).zfill(4), "info.json")
                skill_path = os.path.join(str(i).zfill(4), "skills.json")
                info = JSON(info_path)
                info["skills"] = JSON(skill_path)
                info["secondary_element"] = info.get("secondary_element")
                info["path"] = str(i).zfill(4)
                self.PETS[info["number"]] = PetInfo(**info)
            except:
                continue

    def load_current_data(self):
        self.DATA = JSON("LuokeCollection/main/model/data.json", False)
        a = copy.copy(self.DATA.get("pet_rects"))
        if a is None:
            return
        for i in a:
            del self.DATA["pet_rects"][i]
            self.DATA["pet_rects"][int(i)] = a[i]

    # collection
    def set_page(self, page_number):
        self.page_number = min(
            len(self.PETS) // 9 + (0 if len(self.PETS) % 9 == 0 else 1),
            max(1, page_number),
        )
        pet_page = []
        for i in range(9):
            pet_number = page_number * 9 + i - 8
            if self.PETS.get(pet_number) is None:
                break
            pet_page.append(self.PETS[pet_number])
        self.get_scene().set_page(pet_page)

    def set_info(self, offset):
        self.get_scene().set_info(self.PETS[(self.page_number - 1) * 9 + offset])

    def previous_page(self):
        self.set_page(self.page_number - 1)

    def next_page(self):
        self.set_page(self.page_number + 1)

    # select_rect
    def set_pet_select_rect(self, pet_number):
        self.pet_select_rect = self.PETS[pet_number]
        image_path = os.path.join(
            "LuokeCollection/assets/data/", self.pet_select_rect.path, "display.png"
        )
        scene = self.get_scene()
        scene.set_pet_image(IMAGE(image_path, False))
        self.DATA["pet_rects"] = self.DATA.get("pet_rects", {})
        scene.rect = self.DATA["pet_rects"].get(pet_number)

    def previous_pet(self):
        self.pet_number_select_rect = max(1, self.pet_number_select_rect - 1)
        self.set_pet_select_rect(self.pet_number_select_rect)

    def next_pet(self):
        self.pet_number_select_rect = min(200, self.pet_number_select_rect + 1)
        self.set_pet_select_rect(self.pet_number_select_rect)

    def save_rect(self, x, y, w, h):
        self.DATA["pet_rects"] = self.DATA.get("pet_rects", {})
        pet_num = int(self.pet_number_select_rect)

        if self.DATA["pet_rects"].get(pet_num) is None:
            self.DATA["pet_rects"][pet_num] = [x, y, w, h]
        else:
            del self.DATA["pet_rects"][pet_num]
            self.DATA["pet_rects"][pet_num] = [x, y, w, h]

        content = json.dumps(self.DATA, ensure_ascii=False)
        save_file("LuokeCollection/main/model/data.json", content)
