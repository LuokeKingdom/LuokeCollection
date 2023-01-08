from .battle_pet import BattlePet
from .battle_animation import BattleAnimation
import queue
import random

class BattleSystem:
    def __init__(self, pet_array_1, pet_array_2):
        self.queue_number = 4
        self.current_queue_index = 0
        self.animation_queues = [queue.Queue(10) for i in range(self.queue_number)]
        self.current_animations = [None]*self.queue_number

        self.team1 = [None if args is None else BattlePet(*args) for args in pet_array_1]
        self.choice1 = None
        self.log1 = []

        self.team2 = [None if args is None else BattlePet(*args) for args in pet_array_2]
        self.choice2 = None
        self.log2 = []

    def get_pets(self):
        return self.team1[0], self.team2[0]
    
    def set_damage_display(self, display1, display2):
        for i in self.team1:
            if i is not None:
                i.damage_display = display1
        for i in self.team2:
            if i is not None:
                i.damage_display = display2
    
    def has_animation(self):
        return all([i is None for i in self.current_animations]) and all([i.empty() for i in self.animation_queues])

    def update_animation(self, delta_time):
        if all([i is None for i in self.current_animations]) and self.has_animation():
            for i in range(self.queue_number):
                self.current_animations[i] = self.animation_queues[i].get()
        for i in range(self.queue_number):
            current_animation = self.current_animations[i]
            if current_animation is not None and current_animation.done:
                self.current_animations[i] = None
            if current_animation is not None:
                current_animation.update(delta_time)

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
        self.push_anim('none', pet=primary, interval=1).next_anim()
        self.push_anim('damage', damage=-100, pet=secondary, interval=1).next_anim()
        damage = primary.AD + int(primary.skills[choice].power)
        secondary.HP -= damage
        pass

    def postaction(self, primary, secondary):
        pass

    def push_anim(self, name, **kwargs):
        self.animation_queues[self.current_queue_index].put(BattleAnimation.get(name, **kwargs))
        return self

    def next_anim(self):
        # add None to unused queues
        for i in range(self.current_queue_index, self.queue_number):
            self.animation_queues[i].put(None)
        # reset animation pipeline
        self.current_queue_index = 0