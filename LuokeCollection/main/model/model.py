from LuokeCollection.main.utils import PetInfo
import os
from LuokeCollection.settings.dev import (
    IMAGE,
    JSON
)

class Model:
    PETS = {}
    def __init__(self, app):
        self.page_number = -1
        self.app = app
        self.load_pets()
    
    def close(self): self.app.pop_scene()

    def open(self, name): self.app.push_scene(name)
    
    def get_view(self):
        return self.app.scene.view
    
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

    def set_page(self, page_number):
        temp = self.page_number
        self.page_number = min(len(self.PETS)//9+(0 if len(self.PETS)%9==0 else 1), max(1, page_number))
        if temp==self.page_number: return
        pet_page = []
        for i in range(9):
            pet_number = page_number*9+i-8
            if self.PETS.get(pet_number) is None: break
            pet_page.append(self.PETS[pet_number])
        self.get_view().set_page(pet_page)
    
    def set_info(self):
        self.get_view().set_info()

    def previous_page(self): self.set_page(self.page_number-1)

    def next_page(self): self.set_page(self.page_number+1)
        
        
        


        


