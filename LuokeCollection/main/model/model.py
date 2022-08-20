from LuokeCollection.main.utils import PetInfo
import os
import json
from LuokeCollection.settings.dev import IMAGE, JSON
from ..utils import save_file


class Model:
    PETS = {}
    DATA = None

    def __init__(self, app):
        self.page_number = -1
        self.app = app
        self.load_pets()
        self.load_current_data()
        self.pet_select_rect = None

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

    # collection
    def set_page(self, page_number):
        print('a')
        temp = self.page_number
        self.page_number = min(
            len(self.PETS) // 9 + (0 if len(self.PETS) % 9 == 0 else 1),
            max(1, page_number),
        )
        if temp == self.page_number:
            return
        pet_page = []
        for i in range(9):
            pet_number = page_number * 9 + i - 8
            if self.PETS.get(pet_number) is None:
                break
            pet_page.append(self.PETS[pet_number])
        self.get_scene().set_page(pet_page)

    def set_info(self):
        self.get_scene().set_info()

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
        self.get_scene().set_pet_image(IMAGE(image_path, False))

    def save_rect(self, pet_number, x, y, w, h):
        rects = self.DATA.get("pet_rects", {})
        rects[pet_number] = [x, y, w, h]
        content = json.dumps(self.DATA, ensure_ascii=False)
        save_file("LuokeCollection/main/model/data.json", content)
