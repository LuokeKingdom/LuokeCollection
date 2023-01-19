class Animator:
    def __init__(self, system):
        self.system = system

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
        if damage=="miss":
            self.animate_number(secondary, "miss")
        else:
            self.animate_number(secondary, -damage)
        self.push_anim(
            "position", data=rev_data2, display=primary.sprite_display
        ).next_anim()
        self.push_anim(
            "position", data=rev_data1, display=primary.sprite_display
        ).next_anim()

    def animate_number(self, pet, number):
        text, color = None, None
        if number=="miss":
            text="miss"
            color=(30, 144, 255)
        else:
            text="+" + str(number) if number > 0 else number
            color=(255, 0, 0) if number < 0 else (0, 255, 0)
        self.push_anim(
            "text",
            text=text,
            color=color,
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

    def animate_change_pet(self, pet, new_pet_index):
        new_pet = (self.system.team1 if pet.is_self else self.system.team2)[
            new_pet_index
        ]
        scale_data, rev_data = self.get_scale_data(
            [
                (0, 0),
                (1, -1),
            ]
        )
        display = pet.sprite_display
        self.push_anim("scale", data=scale_data, display=display).next_anim()
        image_pos = display.get_pos()
        self.push_anim(
            "stuff_change",
            on_update=lambda x: display.set_image(x).set_pos(*image_pos),
            stuff=new_pet.image,
        )
        self.push_anim("scale", data=rev_data, display=display).next_anim()
        self.push_anim(
            "stuff_change",
            on_update=lambda x: self.system.display_function(),
            stuff=None,
        )
        self.append_log(f"将<{pet.info.name}>换成了<{new_pet.info.name}>", pet.is_self)

    def animate_potion(self, pet, heal):
        scale_data, rev_data = self.get_scale_data(
            [
                (0, 0),
                (0.3, 0.1),
            ]
        )
        display = pet.sprite_display
        # potion animation
        self.append_log("使用了药剂", pet.is_self)
        self.push_anim("scale", data=scale_data, display=display).next_anim()
        self.animate_number(pet, heal)
        self.push_anim("scale", data=rev_data, display=display).next_anim()

    def animate_burn(self, pet):
        self.push_anim("none", interval=0.5).next_anim()
        self.append_log(f"<{pet.info.name}>烧伤了", pet.is_self)

    def animate_jisheng(self, pet):
        self.push_anim("none", interval=0.5).next_anim()
        self.append_log(f"<{pet.info.name}>被寄生了", pet.is_self)

    def animate_poison(self, pet):
        self.push_anim("none", interval=0.5).next_anim()
        self.append_log(f"<{pet.info.name}>中毒了", pet.is_self)

    def animate_sleep(self, pet):
        self.push_anim("none", interval=0.5).next_anim()
        self.append_log(f"<{pet.info.name}>睡着了", pet.is_self)

    def animate_effect(self, primary, secondary, effect):
        scale_data, rev_data = self.get_scale_data(
            [
                (0, 0),
                (0.1, 0.05),
                (0.2, 0),
                (0.3, -0.05),
                (0.4, 0)
            ]
        )
        display = secondary.sprite_display
        # effect animation
        self.push_anim("scale", data=scale_data, display=display).next_anim()
        self.push_anim("scale", data=rev_data, display=display).next_anim()
        

    def animate_buff(self, pet, stat_label):
        scale_data, rev_data = self.get_scale_data(
            [
                (0, 0),
                (0.3, 0.1),
                (0.4, 0.15)
            ]
        )
        display = pet.sprite_display
        # effect animation
        self.push_anim("scale", data=scale_data, display=display).next_anim()
        self.push_anim("scale", data=rev_data, display=display).next_anim()
        
    def animate_debuff(self, pet, stat_label):
        scale_data, rev_data = self.get_scale_data(
            [
                (0, 0),
                (0.3, -0.1),
                (0.4, -0.15)
            ]
        )
        display = pet.sprite_display
        # effect animation
        self.push_anim("scale", data=scale_data, display=display).next_anim()
        self.push_anim("scale", data=rev_data, display=display).next_anim()
        
    def animate_move(self, pet):
        pos_data1, rev_data1 = self.get_position_data(
            [
                (0.0, (0, 0)),
                (0.1, (-20, 0)),
                (0.2, (-30, 0)),
                (0.3, (-35, 0)),
                (0.4, (-38, 0)),
                (0.5, (-35, 0)),
                (0.6, (-30, 0)),
                (0.7, (-20, 0)),
                (0.8, (-10, 0)),
                (0.9, (0, 0))
            ],
            pet.is_self,
        )
        self.push_anim(
            "position", data=pos_data1, display=pet.sprite_display
        )









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
                list(reversed([data[-1][0] - data[i][0] for i in range(len(data))])),
                list(reversed(list(zip(*data))[1])),
            )
        )
