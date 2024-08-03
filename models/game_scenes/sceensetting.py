import pygame
from models.ui_components.button import ImageButton
from models.ui_components.button import ButtonImage
from models.ui_components.string import String
from models.utils import Data, Image

class ScrollBar:

    def __init__(self, name, image, background, values, pos):
        self.name = name
        self.image = image
        self.background = background
        self.values = values
        self.pos = pos
        self.index = 0

    def render(self, display):
        for i in range(10):
            if i < self.values:
                display.blit(self.background[0], (self.pos[0] + i * 22, self.pos[1]))
            else:
                display.blit(self.background[1], (self.pos[0] + i * 22, self.pos[1]))

        if self.values in [1, 2, 3]:
            self.index = 1
        if self.values in [4, 5, 6]:
            self.index = 2
        if self.values in [7, 8, 9, 10]:
            self.index = 3
        if self.values == 0:
            self.index = 0

        size = self.image[self.index].get_size()
        size = (int(size[0] / 2), int(size[1] / 2))
        image = pygame.transform.scale(self.image[self.index], size)

        display.blit(image, (self.pos[0] + 220, self.pos[1] + 2))

    def click_mouse(self, pos, z):
        for i in range(10):
            box = (self.pos[0] + i * 22, self.pos[1])
            if box[0] <= pos[0] < box[0] + 13 and box[1] <= pos[1] < box[1] + 41:
                if z == 1:
                    self.values = i + 1

        box = (self.pos[0] + 220, self.pos[1] + 2)
        size = self.image[self.index].get_size()
        size = (int(size[0] / 2), int(size[1] / 2))
        if box[0] <= pos[0] <= box[0] + size[0] and box[1] <= pos[1] <= box[1] + size[1]:
            if self.values == 0:
                self.values = 5
            else:
                self.values = 0
            

class ScreenSetting:
    def __init__(self, display):
        self.display = display
        self.String = String(self.display)
        self.images_level = Data().load_data_images_level()
        self.image_block = self.images_level["block"]
        size = self.image_block.get_size()
        size = (int(size[0] * 3), int(size[1] * 3))
        self.image_block = pygame.transform.scale(self.image_block, size)

        self.background = pygame.image.load("data/Images/Menu/Buttons/frame_black.png")
        self.background = pygame.transform.scale(self.background, (400, 200))

        self.page = 1
        self.old_page = 0

        self.levels = []
        image_back = Image().load_image_button("Back")
        self.button_back = ImageButton("back", image_back, (30, 30), 3)
        self.buttons = [self.button_back]

        image_on = Image().load_image_button("music_on")
        image_off = Image().load_image_button("music_off")

        image_0 = Image().load_image_button("music_0")
        image_1 = Image().load_image_button("music_1")
        image_2 = Image().load_image_button("music_2")
        image_3 = Image().load_image_button("music_3")
        iamge_level = [image_0, image_1, image_2, image_3]

        self.Music = ScrollBar("music", iamge_level, [image_on, image_off], 5, (220, 190))
        self.Sfx = ScrollBar("sfx", iamge_level, [image_on, image_off], 5, (220, 270))

        self.data_lock_levels = Data().load_data_lock_levels()

    def render(self):
        self.display.blit(self.background, (100, 150))
        self.String.render_until("setting", (188, 80), 4)
        self.String.render_until("music:", (120, 200), 2)
        self.String.render_until("spx:", (152, 280), 2)
        for i in self.levels:
            if i.is_block:
                self.display.blit(self.image_block, i.pos)
            else:
                self.display.blit(i.image, i.pos)
        for i in self.buttons:
            i.render(self.display)

        self.Music.render(self.display)
        self.Sfx.render(self.display)
        
        

    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
        self.Music.click_mouse((x, y), z)
        self.Sfx.click_mouse((x, y), z)
