import random
class rng:
    count = 0
    def __init__(self):
        if self.count != 0:
            raise Exception("Multiple rng not allowed!")
        self.generator = self._generator()
        self.count += 1

    def _generator(self):
        random.seed(10)
        while 1:
            yield random.random()
    
    def get(self):
        return next(self.generator)

