import pygame
from models.ui_components.button import ImageButton
from models.ui_components.button import ButtonImage
from models.ui_components.string import String
from models.utils import Data, Image

class Level:

    def __init__(self, name, image, pos):
        self.name = name
        self.image = image
        self.pos = pos
        self.is_block = True

    def click_mouse(self, pos, z):
        if self.is_block:
            return False
        if self.pos[0] <= pos[0] and self.pos[0] + self.image.get_width() >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.image.get_height() >= pos[1]:
                return z == 1
            


class ScreenLevel:
    def __init__(self, display):
        self.display = display
        self.String = String(self.display)
        self.images_level = Data().load_data_images_level()
        self.image_block = self.images_level["block"]
        size = self.image_block.get_size()
        size = (int(size[0] * 3), int(size[1] * 3))
        self.image_block = pygame.transform.scale(self.image_block, size)

        self.background = pygame.image.load("data/Images/Menu/Buttons/frame_black.png")
        self.background = pygame.transform.scale(self.background, (320, 220))

        self.page = 1

        self.levels = []
        image_next = Image().load_image_button("Next")
        self.button_next = ImageButton("next", image_next, (430, 210), 3)
        image_previous = Image().load_image_button("Previous")
        self.button_previous = ImageButton("previous", image_previous, (110, 210), 3)
        image_back = Image().load_image_button("Back")
        self.button_back = ImageButton("back", image_back, (30, 30), 3)
        self.buttons = [self.button_next, self.button_previous, self.button_back]
        self.data_lock_levels = Data().load_data_lock_levels()

    def render(self):
        self.data_lock_levels = Data().load_data_lock_levels()
        self.display.blit(self.background, (140, 130))
        pos = (205, 150)
        t = 0
        r = 0
        if True:
            self.levels = []
            for i in range((self.page - 1) * 9, self.page * 9):
                if i > 49:
                    break
                name = str(f"{i+1:02}")
                image = self.images_level[name]
                size = image.get_size()
                size = (int(size[0] * 3), int(size[1] * 3))
                image = pygame.transform.scale(image, size)
                level = Level(name, image, (pos[0] + t * (size[0] + 10), pos[1] + r * (size[1] + 10)))
                level.is_block = self.data_lock_levels[name]
                self.levels.append(level)
                t = t + 1
                if t == 3:
                    t = 0
                    r = r + 1
        self.String.render_until("level", (220, 60), 4)
        for i in self.levels:
            if i.is_block:
                self.display.blit(self.image_block, i.pos)
            else:
                self.display.blit(i.image, i.pos)
        for i in self.buttons:
            i.render(self.display)
        
        

    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
        for i in self.levels:
            if i.click_mouse((x, y), z):
                return i.name
        return "tognoek"

    def set_page(self, index):
        page = self.page + index
        if page < 1:
            page = 1
        if page > 6:
            page = 6
        is_check = True
        for i in range((page - 1) * 9, page * 9):
            name = str(f"{i+1:02}")
            if not self.data_lock_levels[name]:
                is_check = False
                break
        if not is_check:
            self.page = page