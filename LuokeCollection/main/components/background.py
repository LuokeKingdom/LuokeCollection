from .container import Container
from LuokeCollection.settings.dev import WIDTH, HEIGHT


class Background(Container):
    def __init__(self, image, width=WIDTH, height=HEIGHT):
        super().__init__(image=image, width=width, height=height)

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=screen.get_rect().center))

    def update(self):
        pass
