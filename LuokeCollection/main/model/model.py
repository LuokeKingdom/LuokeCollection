import copy
from LuokeCollection.main.battle.battle_system import BattleSystem
from LuokeCollection.main.scene.collection_scene import CollectionScene
from LuokeCollection.main.scene.battle_prep_scene import BattlePrepScene
from .sound import Channel
from ..utils import PetInfo, SkillInfo
import os
import json
import threading
from _thread import start_new_thread
from ...settings.dev import IMAGE, JSON, SOUND
from ..utils import save_file
from ..network.client import Client

import pygame
from pygame.locals import *  # noqa


class Model:
    PETS = {}
    DATA = None

    def __init__(self, app):
        self.app = app
        self.client = None
        self.opponent_pets = None
        self.opponent_index = None
        self.battle_ready = False
        self.self_action_chosen = -1
        self.oppo_action_chosen = -1
        self.action_sent = False

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
        self.battle_prep_pet_number = 0
        self.battle_pet_content = ""
        self.battle_prep_offset = 0

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

    def open(self, name, **kwargs):
        self.app.push_scene(name, **kwargs)

    def open_pop_up(self, name, **kwargs):
        self.app.open_pop_up(name, **kwargs)

    def close_pop_up(self):
        self.app.close_pop_up()

    def get_scene(self):
        return self.app.scene

    def load_pets(self):
        for i in range(201):
            if i == 100:
                continue
            try:
                info_path = os.path.join(str(i).zfill(4), "info.json")
                skill_path = os.path.join(str(i).zfill(4), "skills.json")
                info = JSON(info_path)
                info["skills"] = list(
                    map(
                        lambda x: SkillInfo(index=x[0], **(x[1])),
                        enumerate(JSON(skill_path)),
                    )
                )
                info["secondary_element"] = info.get("secondary_element")
                info["path"] = str(i).zfill(4)
                self.PETS[info["number"]] = PetInfo(**info)
            except Exception as e:
                print(e)
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
        scene = self.get_scene()
        if offset is not None:
            self.pet_number_training = (self.pet_page_number - 1) * 9 + offset
        scene.set_info(self.PETS[self.pet_number_training])
        if isinstance(scene, CollectionScene):
            if offset is None:
                offset = (self.pet_number_training - 1) % 9
            else:
                offset -= 1
            i = offset // 3
            j = offset % 3
            x = 272 + j * 161
            y = 204 + i * 146
            scene.BUTTONS["edit_avatar"].set_pos(x, y)

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
    def load_skills(self, saved_skills=[-1, -1, -1, -1]):
        pet_info = self.PETS[self.pet_number_training]
        scene = self.get_scene()
        for i in range(4):
            try:
                scene.set_skill(
                    i, pet_info.skills[(self.skill_page_number - 1) * 4 + i]
                )
            except Exception as e:
                print(e)
                scene.set_skill(i, None)
        for i in range(4):
            if saved_skills[i] >= 0:
                scene.set_skill(i + 4, pet_info.skills[saved_skills[i]])
            else:
                scene.set_skill(i + 4, None)
        self.MAX_SKILL_PAGE = len(pet_info.skills) // 4 + (
            0 if len(pet_info.skills) % 4 == 0 else 1
        )

    def previous_skill_page(self):
        if self.skill_page_number == 1:
            self.error_sound.play()
            return
        self.skill_page_number -= 1
        pet_info = self.PETS[self.pet_number_training]
        scene = self.get_scene()
        for i in range(4):
            try:
                scene.set_skill(
                    i, pet_info.skills[(self.skill_page_number - 1) * 4 + i]
                )
            except Exception as e:
                print(e)
                scene.set_skill(i, None)

    def next_skill_page(self):
        if self.skill_page_number == self.MAX_SKILL_PAGE:
            self.error_sound.play()
            return
        self.skill_page_number += 1
        pet_info = self.PETS[self.pet_number_training]
        scene = self.get_scene()
        for i in range(4):
            try:
                scene.set_skill(
                    i, pet_info.skills[(self.skill_page_number - 1) * 4 + i]
                )
            except Exception as e:
                print(e)
                scene.set_skill(i, None)

    def save_pet_content(self, talent_map, skills):
        object = {
            "number": self.pet_number_training,
            "talent_map": talent_map,
            "skills": skills,
        }
        self.battle_pet_content = json.dumps(object, ensure_ascii=False)
        self.open_pop_up("pet_position_select")

    def save_pet_file(self, index):
        save_file(f"assets/battle/pet_{index}.json", self.battle_pet_content)
        self.close_pop_up()

    def replace_skills(self, current_slots):
        for i in range(4):
            pet_info = self.PETS[self.pet_number_training]
            scene = self.get_scene()
            if current_slots[i] == -1:
                scene.set_skill(i + 4, None)
            else:
                scene.set_skill(i + 4, pet_info.skills[current_slots[i]])

    # battle preparation
    def set_battle_prep(self, offset=-1):
        scene = self.get_scene()
        if isinstance(scene, BattlePrepScene):
            battle_pet = self.get_battle_pet(offset)
            if battle_pet is None:
                self.error_sound.play()
                return
            self.battle_prep_offset = offset
            self.pet_number_training = battle_pet["number"]
            scene.talent_map = battle_pet["talent_map"]
            scene.set_info(self.PETS[self.pet_number_training])
            for i in range(4):
                if battle_pet["skills"][i] == -1:
                    scene.set_skill(i, None)
                else:
                    scene.set_skill(
                        i,
                        self.PETS[self.pet_number_training].skills[
                            battle_pet["skills"][i]
                        ],
                    )

    def get_battle_pet(self, offset):
        if offset == -1:
            return self.pet_number_training
        pet_path = os.path.join("assets/battle/", f"pet_{offset}.json")
        if os.path.exists(pet_path):
            return JSON(pet_path, False)
        return None

    def get_battle_pets(self):
        return [self.get_battle_pet(i) for i in range(6)]

    def ready_for_battle(self):
        self.battle_ready = True
        print("READY")

    def get_battle_system(self):
        print("Start get")
        pet_array_1 = []
        battle_pets = self.get_battle_pets()
        for battle_pet in battle_pets:
            if battle_pet is None:
                pet_array_1.append(None)
                continue
            pet_array_1.append(
                (
                    self.PETS[battle_pet["number"]],
                    battle_pet["talent_map"],
                    battle_pet["skills"],
                )
            )
        pet_array_2 = []
        for battle_pet in self.opponent_pets:
            if battle_pet is None:
                pet_array_2.append(None)
                continue
            pet_array_2.append(
                (
                    self.PETS[battle_pet["number"]],
                    battle_pet["talent_map"],
                    battle_pet["skills"],
                )
            )
        scene = self.get_scene()
        print("Before init battle system")
        return BattleSystem(
            pet_array_1,
            pet_array_2,
            scene.display_pets,
            self.client.id,
            self.client.seed,
        )

    def client_init(self):
        self.client = Client(self.get_battle_pets())
        start_new_thread(self.threaded_client, ())

    def threaded_client(self):
        while 1:
            self.client_update()

    def client_update(self):
        reply_args = None, None, None
        scene = self.get_scene()
        try:
            if self.client is None:
                return
            obj = self.client.receive(2048)
            # print(obj)
            if not obj:
                pass
            elif obj.id == 0:
                if obj.opponent is not None and self.opponent_pets is None:
                    self.opponent_index = obj.opponent
                    reply_args = False, True, None
                # else:
                # reply_args = True, False, None
                if self.opponent_pets is not None and self.battle_ready:
                    reply_args = True, True, None
                if isinstance(scene, BattlePrepScene):
                    if obj.ready is True:
                        self.open("battle")
                        reply_args = True, True, -1
                else:
                    if self.self_action_chosen > -1 and not self.action_sent:
                        reply_args = True, False, self.self_action_chosen
                        self.action_sent = True
                    if obj.ready is True and obj.accept is False:
                        self.oppo_action_chosen = obj.choice
            else:
                self.opponent_pets = obj.data
            self.client.reply(*reply_args, self.opponent_index)
        except Exception as e:
            print(e)

    def reset_turn(self):
        print("RESET")
        scene = self.get_scene()
        self.action_sent = False
        self.self_action_chosen = -1
        self.oppo_action_chosen = -1
        scene.is_preparing = True
        scene.timer = 0
        scene.display_pets()
        scene.turn_begun = False
