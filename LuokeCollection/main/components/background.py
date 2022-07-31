from .container import Container


class Background(Container):
    def __init__(self, image):
        super().__init__(image=image)

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=screen.get_rect().center))

    def update(self):
        pass
