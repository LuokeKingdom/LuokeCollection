import random


class rng:
    count = 0

    def __init__(self, seed):
        if self.count != 0:
            raise Exception("Multiple rng not allowed!")
        self.generator = self._generator(seed)
        self.count += 1

    def _generator(self, seed):
        random.seed(seed)
        while 1:
            yield random.random()

    def get(self):
        return next(self.generator)
