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

        self.team1 = [
            None if args is None else BattlePet(*args) for args in pet_array_1
        ]
        self.choice1 = None
        self.log1 = []
        for i in self.team1:
            if i is not None:
                i.is_self = True

        self.team2 = [
            None if args is None else BattlePet(*args) for args in pet_array_2
        ]
        self.choice2 = None
        self.log2 = []

    def get_pets(self):
        return self.team1[0], self.team2[0]

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
        result = ActionSolver(choice, primary, secondary)
        damage_taker, damage_user = result.get_damage()
        heal_taker, heal_user = result.get_heal()
        if damage_taker is not None:
            secondary.change_health(-damage_taker)
            self.animate_attack(primary, secondary, damage_taker)
        if damage_user is not None:
            primary.change_health(-damage_user)
            self.animate_number(primary, -damage_user)
        if heal_user is not None:
            primary.change_health(heal_user)
            self.animate_heal(primary, heal_user)
        if heal_taker is not None:
            secondary.change_health(heal_taker)
            self.animate_heal(secondary, heal_taker)

        if secondary.health == 0:
            self.done = True
            raise Exception("Battle Finish!!!")

    def postaction(self, primary, secondary):
        pass

    def animate_attack(self, primary, secondary, damage):

        pos_data1, rev_data1 = self.get_position_data(
            [
                (0, (0, 0)),
                (0.6, (200, 0)),
                (0.7, (265, 0)),
            ],
            not primary.is_self,
        )
        pos_data2, rev_data2 = self.get_position_data(
            [
                (0.1, (310, 0)),
                (0.2, (300, 0)),
            ],
            not primary.is_self,
        )

        self.push_anim(
            "position", data=pos_data1, display=primary.sprite_display
        ).next_anim()
        self.push_anim("position", data=pos_data2, display=primary.sprite_display)
        self.animate_number(secondary, -damage)
        self.push_anim(
            "position", data=rev_data2, display=primary.sprite_display
        ).next_anim()
        self.push_anim(
            "position", data=rev_data1, display=primary.sprite_display
        ).next_anim()

    def animate_number(self, pet, number):
        self.push_anim(
            "text",
            text="+" + str(number) if number > 0 else number,
            color=(255, 0, 0) if number < 0 else (0, 255, 0),
            display=pet.number_display,
            interval=1,
        )
        self.push_anim(
            "text_change", text=pet.health, display=pet.health_display
        ).next_anim()
        self.push_anim("none", interval=0.5).next_anim()

    def animate_heal(self, pet, heal):
        pos_data1, rev_data1 = self.get_position_data(
            [
                (0.0, (0, 0)),
                (0.2, (0, -3)),
                (0.4, (0, -7)),
                (0.6, (0, -15)),
            ],
            pet.is_self,
        )
        self.push_anim(
            "position", data=pos_data1, display=pet.sprite_display
        ).next_anim()
        self.animate_number(pet, heal)
        self.push_anim(
            "position", data=rev_data1, display=pet.sprite_display
        ).next_anim()

    def push_anim(self, name, **kwargs):
        self.temp_anim.append(BattleAnimation.get(name, **kwargs))
        return self

    def next_anim(self):
        self.anim_queue.put(self.temp_anim)
        self.temp_anim = []

    def get_position_data(self, data, inversed):
        position_data = list(
            map(lambda x: (x[0], (-x[1][0], x[1][1])) if inversed else x, data)
        )
        reversed_data = list(
            zip(
                list(
                    reversed(
                        [
                            position_data[-1][0] - position_data[i][0]
                            for i in range(len(position_data))
                        ]
                    )
                ),
                list(reversed(list(zip(*position_data))[1])),
            )
        )
        print(position_data, reversed_data)
        return position_data, reversed_data
