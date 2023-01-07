from .battle_pet import BattlePet
from .battle_animation import BattleAnimation
import queue
import random

class BattleSystem:
    def __init__(self, pet_array_1, pet_array_2):
        self.team1 = [None if args is None else BattlePet(*args) for args in pet_array_1]
        self.animation_queue1 = queue.Queue(20)
        self.current_animation1 = None
        self.choice1 = None
        self.log1 = []

        self.team2 = [None if args is None else BattlePet(*args) for args in pet_array_2]
        self.choice2 = None
        self.animation_queue2 = queue.Queue(20)
        self.current_animation2 = None
        self.log2 = []

    def get_pets(self):
        return self.team1[0], self.team2[0]
    
    def has_animation(self):
        return not (self.current_animation1 is None and self.current_animation2 is None and self.animation_queue1.empty() and self.animation_queue2.empty())

    def update_animation(self, delta_time):
        if self.current_animation1 is not None and self.current_animation1.done:
            self.current_animation1 = None
        if self.current_animation1 is None and not self.animation_queue1.empty():
            self.current_animation1 = self.animation_queue1.get()
        if self.current_animation1 is not None:
            self.current_animation1.update(delta_time)

        if self.current_animation2 is not None and self.current_animation2.done:
            self.current_animation2 = None
        if self.current_animation2 is None and not self.animation_queue2.empty():
            self.current_animation2 = self.animation_queue2.get()
        if self.current_animation2 is not None:
            self.current_animation2.update(delta_time)

    def prepare(self, team1_choice, team2_choice):
        self.choice1 = team1_choice
        self.choice2 = team2_choice
        self.log1.append(team1_choice)
        self.log2.append(team2_choice)

    def act(self):
        pet1, pet2 = self.get_pets()
        choice1, choice2 = self.choice1, self.choice2
        pet1_first = pet1.SP > pet2.SP
        if pet1.SP == pet2.SP:
            pet1_first = random.choice([True, False])
        if not pet1_first:
            pet1, pet2 = pet2, pet1
            choice1, choice2 = choice2, choice1
        if (self.preaction(pet1, pet2)):
            self.action(pet1, pet2, choice1)
        self.postaction(pet1, pet2)
        if (self.preaction(pet2, pet1)):
            self.action(pet2, pet1, choice2)
        self.postaction(pet2, pet1)

    def preaction(self, primary, secondary):
        return True

    def action(self, primary, secondary, choice):
        self.animation_queue1.put(self.anim('none', primary, interval=1))
        self.animation_queue2.put(self.anim('none', secondary, interval=1))
        damage = primary.AD + int(primary.skills[choice].power)
        secondary.HP -= damage
        pass

    def postaction(self, primary, secondary):
        pass

    def anim(self, name, pet, **kwargs):
        return BattleAnimation.get(name, pet, **kwargs)
