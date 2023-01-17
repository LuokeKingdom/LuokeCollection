class Pack:
    def __init__(self):
        self.id = 0
        self.ready = None
        self.accept = None
        self.choice = -1
        self.opponent = None

    def __str__(self):
        return f'ready: <{self.ready}>, accept: <{self.accept}>, choice: <{self.choice}>, oppo: <{self.opponent}>'

class Pets:
    def __init__(self, pets):
        self.id = 1
        self.data = pets

    def __str__(self):
        return str(len(self.data))