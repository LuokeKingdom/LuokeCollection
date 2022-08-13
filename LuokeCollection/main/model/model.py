from LuokeCollection.main.utils import PetInfo
import os
from LuokeCollection.settings.dev import (
    IMAGE,
    JSON
)

class Model:
    PETS = {}
    def __init__(self):
        self.load_pets()
        pass

    def load_pets(self):
        for i in range(201):
            try:
                info_path = os.path.join(str(i).zfill(4), 'info.json')
                skill_path = os.path.join(str(i).zfill(4), 'skills.json')
                info = JSON(info_path)
                info['skills'] = JSON(skill_path)
                info['secondary_element'] = info.get('secondary_element')
                self.PETS[info['number']] = PetInfo(**info)
            except:
                print(i)
                continue



