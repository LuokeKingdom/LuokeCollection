from .battle_pet import BattlePet

class BattleSystem:
    def __init__(self, pet_array_1, pet_array_2):
        self.team1 = [None if args is None else BattlePet(*args) for args in pet_array_1]
        self.team2 = [None if args is None else BattlePet(*args) for args in pet_array_2]

    def get_pets(self):
        return self.team1[0], self.team2[0]

    def prepare(self):
        pass

    def act(self):
        if (self.preaction()):
            self.action()
        self.postaction()
        pass

    def preaction(self):
        pass

    def action(self):
        pass

    def postaction(self):
        pass
