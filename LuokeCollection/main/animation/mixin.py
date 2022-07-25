class Mixin:
    def effect(self, current_time):
        pass

    def progress(self, current_time):
        if not self.transition:
            return 1
        return min(1, (current_time - self.start_time) / self.transition)
