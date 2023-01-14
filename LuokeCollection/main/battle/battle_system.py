from .battle_pet import BattlePet
from .battle_animation import BattleAnimation
import queue
import random
from .action_solver import ActionSolver


class BattleSystem:
    def __init__(self, pet_array_1, pet_array_2):
        self.done = False
        self.win = None
        self.anim_queue = queue.Queue()
        self.temp_anim = []
        self.curr_anim = [None]
        self.on_log_update = None

        self.team1 = [
            None if args is None else BattlePet(*args) for args in pet_array_1
        ]
        self.current_pet1 = 0
        self.choice1 = None
        self.log1 = []
        for i in self.team1:
            if i is not None:
                i.is_self = True
                i.image = i.get_image()

        self.team2 = [
            None if args is None else BattlePet(*args) for args in pet_array_2
        ]
        self.current_pet2 = 0
        self.choice2 = None
        self.log2 = []
        for i in self.team2:
            if i is not None:
                i.image = i.get_image()

    def get_pets(self):
        return self.team1[self.current_pet1], self.team2[self.current_pet2]

    def set_pets(self, next1, next2):
        self.current_pet1 = next1
        self.current_pet2 = next2

    def set_number_display(self, display1, display2):
        for i in self.team1:
            if i is not None:
                i.number_display = display1
        for i in self.team2:
            if i is not None:
                i.number_display = display2

    def set_health_display(self, display1, display2):
        for i in self.team1:
            if i is not None:
                i.health_display = display1
        for i in self.team2:
            if i is not None:
                i.health_display = display2

    def set_sprite_display(self, display1, display2):
        for i in self.team1:
            if i is not None:
                i.sprite_display = display1
        for i in self.team2:
            if i is not None:
                i.sprite_display = display2

    def has_animation(self):
        return (
            not all([i is None for i in self.curr_anim]) or not self.anim_queue.empty()
        )

    def update_animation(self, delta_time):
        if all([i is None for i in self.curr_anim]):
            self.curr_anim = self.anim_queue.get()
        for i in range(len(self.curr_anim)):
            anim = self.curr_anim[i]
            if anim is not None and anim.done:
                self.curr_anim[i] = None
            if anim is not None:
                anim.update(delta_time)

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
        try:
            if self.preaction(pet1, pet2):
                self.action(pet1, pet2, choice1)
            self.postaction(pet1, pet2)
            if self.preaction(pet2, pet1):
                self.action(pet2, pet1, choice2)
            self.postaction(pet2, pet1)
        except Exception as e:
            print(e)
            pet1, pet2 = self.get_pets()
            self.win = pet1.health != 0

    def preaction(self, primary, secondary):
        return True

    def action(self, primary, secondary, choice):
        ActionSolver(choice, primary, secondary).solve(self)
        if secondary.health == 0:
            self.done = True
            raise Exception("Battle Finish!!!")

    def postaction(self, primary, secondary):
        pass

    def push_anim(self, name, **kwargs):
        self.temp_anim.append(BattleAnimation.get(name, **kwargs))
        return self

    def next_anim(self):
        self.anim_queue.put(self.temp_anim)
        self.temp_anim = []
    
