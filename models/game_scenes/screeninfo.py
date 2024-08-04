import pygame
from models.utils import Image

class ScreenInfo:

    def __init__(self, display : pygame.Surface):
        self.display = display
        self.path_ratio = "data/Images/Menu/Buttons/background_ratio.png"
        self.on = "data/Images/Menu/Buttons/ratio_on.png"
        self.off = "data/Images/Menu/Buttons/ratio_off.png"
        self.image_ratio = Image().load_image(self.path_ratio)
        self.image_on = Image().load_image(self.on)
        self.image_off = Image().load_image(self.off)
        self.size = self.image_ratio.get_size()
        sur = pygame.Surface(self.size)
        sur.blit(self.image_ratio, (0, 0))
        sur.set_colorkey((0, 0, 0))
        self.sur = sur
        self.sub_pos = (27, 12)
        self.sub_size = (11, 36)
        self.pos = (15, 15)

    def render(self, rate):
        rate = int(rate / 10) * 2
        for i in range(20):
            if i < rate:
                self.sur.blit(self.image_on, (self.sub_pos[0] + i * (self.sub_size[0] + 2), self.sub_pos[1]))
            else:
                self.sur.blit(self.image_off, (self.sub_pos[0] + i * (self.sub_size[0] + 2), self.sub_pos[1]))
        ratio = 0.4
        size = (self.size[0] * ratio, self.size[1] * ratio)
        image = pygame.transform.scale(self.sur, size)
        self.display.blit(image, self.pos)
