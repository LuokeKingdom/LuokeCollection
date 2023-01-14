from LuokeCollection.main.utils import type2element
from .pet_status import PetStatus
from .skill_dictionary import skill_dictionary, SkillEffect


class ActionSolver:
    labels2function = {
        'a': 'attack',
        'p': 'potion',
    }
    def __init__(self, action_index, user, taker):
        self.primary = user
        self.secondary = taker
        self.user_status_change = PetStatus()
        self.taker_status_change = PetStatus()
        self.system = None
        self.action_index = action_index
        self.skill_effects = {k:SkillEffect.__dict__.get(v) for k,v in self.labels2function.items()}

    def solve(self, system):
        self.system = system
        index = self.action_index
        if index < 4:
            self.use_skill(index)
        elif index - 10 < 6:
            self.animate_change_pet(index-10)
        elif index - 100 < 6:
            self.skill_effects.get('p')(self, None, str(index-100))

    def use_skill(self, skill_index):
        skill = self.primary.skills[skill_index]
        self.append_log(f"使用了<{skill.name}>", self.primary.is_self)
        self.user_status_change.skill_PPs[skill_index][0] = -1
        skill_element = type2element(skill.type)
        if skill_element:
            pass
        labels = skill_dictionary.get(skill.name, 'a').split(' ')
        for label in labels:
            identifier = label[0]
            args = label[1:]
            self.skill_effects.get(identifier)(self, skill, args)


    def append_log(self, text, is_self):
        self.push_anim(
            "stuff_change",
            on_update=self.system.on_log_update,
            stuff=f"{'你' if is_self else '对手'}" + text,
        ).next_anim()

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
        self.append_log("回复了体力", pet.is_self)
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

    def animate_change_pet(self, new_pet_index):
        pet = self.primary
        new_pet = (self.system.team1 if pet.is_self else self.system.team2)[new_pet_index]
        scale_data, rev_data = self.get_scale_data([
            (0, 0),
            (1, -1),
        ])
        display = pet.sprite_display
        self.push_anim('scale', data=scale_data, display=display).next_anim()
        image_pos = display.get_pos()
        self.push_anim('stuff_change', on_update=lambda x: display.set_image(x).set_pos(*image_pos), stuff=new_pet.image)
        self.push_anim('scale', data=rev_data, display=display).next_anim()
        def change_function(pet_index):
            if pet.is_self:
                self.system.current_pet1 = pet_index
            else:
                self.system.current_pet2 = pet_index
        self.push_anim('stuff_change', on_update=lambda x: change_function(x), stuff=new_pet_index)
        self.append_log(f'将<{pet.info.name}>换成了<{new_pet.info.name}>', pet.is_self)

    def animate_potion(self, heal):
        pet = self.primary
        scale_data, rev_data = self.get_scale_data([
            (0, 0),
            (.3, .1),
        ])
        display = pet.sprite_display
        # potion animation
        self.append_log("使用了药剂", pet.is_self)
        self.push_anim('scale', data=scale_data, display=display).next_anim()
        self.animate_number(pet, heal)
        self.push_anim('scale', data=rev_data, display=display).next_anim()


    def push_anim(self, name, **kwargs):
        self.system.push_anim(name, **kwargs)
        return self

    def next_anim(self):
        self.system.next_anim()

    def get_position_data(self, data, inversed):
        data.sort()
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
        return position_data, reversed_data

    def get_scale_data(self, data):
        scale_data = sorted(data)
        reversed_data = self.reverse_data(scale_data)
        return scale_data, reversed_data

    def reverse_data(self, data):
        return list(
                zip(
                    list(
                        reversed(
                            [
                                data[-1][0] - data[i][0]
                                for i in range(len(data))
                            ]
                        )
                    ),
                    list(reversed(list(zip(*data))[1])),
                )
            )
