from .battle_pet import BattlePet
from .battle_animation import BattleAnimation
import queue
from .action_solver import ActionSolver
from .animator import Animator
from .rng import rng


class BattleSystem:
    def __init__(self, pet_array_1, pet_array_2, display_function, client_id, seed):
        self.id = client_id
        self.done = False
        self.win = None
        self.anim_queue = queue.Queue()
        self.temp_anim = []
        self.curr_anim = [None]
        self.on_log_update = None
        self.animator = Animator(self)
        self.rng = rng(seed)
        self.display_function = display_function

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
        if pet1.health == 0:
            pet1_first = True
        elif pet2.health == 0:
            pet1_first = False
        else:
            pet1_first = pet1.SP > pet2.SP
            if pet1.SP == pet2.SP:
                half = self.rng.get() > 0.5
                pet1_first = half if self.id == 0 else not half

        def get_args():
            pet1, pet2 = self.get_pets()
            choice1, choice2 = self.choice1, self.choice2
            if not pet1_first:
                pet1, pet2 = pet2, pet1
                choice1, choice2 = choice2, choice1
            return pet1, pet2, choice1, choice2

        try:
            p1, p2, c1, c2 = get_args()
            can_move = self.preaction(p1, p2)
            p1, p2, c1, c2 = get_args()
            if can_move: self.action(p1, p2, c1)
            p1, p2, c1, c2 = get_args()
            self.postaction(p1, p2)
            p1, p2, c1, c2 = get_args()
            can_move = self.preaction(p2, p1)
            p1, p2, c1, c2 = get_args()
            if can_move: self.action(p2, p1, c2)
            p1, p2, c1, c2 = get_args()
            self.postaction(p2, p1)
        except Exception as e:
            print(e)

    def preaction(self, primary, secondary):
        can_move = primary.trigger_pre_effects(secondary)
        self.check_done()
        return can_move

    def action(self, primary, secondary, choice):
        ActionSolver(choice, primary, secondary).solve(self.animator, self.rng)
        self.check_done()

    def postaction(self, primary, secondary):
        secondary.trigger_post_effects(primary)
        self.check_done()

    def check_done(self):
        if all([i is None or i.health == 0 for i in self.team1]):
            self.done = True
            self.win = False
            raise Exception("Battle Finish!!!")
        if all([i is None or i.health == 0 for i in self.team2]):
            self.done = True
            self.win = True
            raise Exception("Battle Finish!!!")

    def push_anim(self, name, **kwargs):
        self.temp_anim.append(BattleAnimation.get(name, **kwargs))
        return self

    def next_anim(self):
        self.anim_queue.put(self.temp_anim)
        self.temp_anim = []
