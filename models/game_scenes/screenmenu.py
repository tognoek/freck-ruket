import pygame
from models.ui_components.button import ButtonImage
from models.ui_components.string import String
from models.utils import Data

class ScreenMenu:
    
    def __init__(self, display : pygame.Surface, image_button, data_text, name_character = "Pink Man"):
        self.display = display
        self.image_button = image_button
        self.data_text = data_text

        self.name_character = name_character

        self.Data = Data()

        self.character = Data().load_images_main_character(self.name_character)[0]["Run"]

        self.way = pygame.image.load("data/Images/Terrain/way1.png")

        self.String = String(self.display)

        self.buttons = []
        self.is_create = False

        self.frame = 0
        self.frame_size = 5

    def update_images_character(self, name):
        self.name_character = name
        self.character = Data().load_images_main_character(self.name_character)[0]["Run"]

    def update_character(self):
        self.frame = self.frame + 1
        if self.frame >= len(self.character) * self.frame_size:
            self.frame = 0

    def render_character(self, ratio = 5):
        self.update_character()
        size = self.character[self.frame // self.frame_size].get_size()
        pos = (100, 130)
        self.display.blit(pygame.transform.scale(self.character[self.frame // self.frame_size], (int(size[0] * ratio), int(size[1] * ratio))), pos)
        size_way = self.way.get_size()
        pos_way = (pos[0] - (size_way[0] * ratio - size[0] * ratio) // 2, pos[1] + size[1] * ratio)
        self.display.blit(pygame.transform.scale(self.way, (size_way[0] * ratio, size_way[1] * ratio)), pos_way)

    def create_menu(self):
        button_start = ButtonImage("start", "start", (340, 140 - 20), self.image_button, self.data_text, 2, 100)
        self.buttons.append(button_start)
        button_level = ButtonImage("level", "level", (340, 200 - 20), self.image_button, self.data_text, 2, 100)
        self.buttons.append(button_level)
        button_figure = ButtonImage("figure", "figure", (340, 260 - 20), self.image_button, self.data_text, 2, 100)
        self.buttons.append(button_figure)
        button_setting = ButtonImage("setting", "setting", (340, 320 - 20), self.image_button, self.data_text, 2, 100)
        self.buttons.append(button_setting)
        button_exit = ButtonImage("exit", "exit", (340, 380 - 20), self.image_button, self.data_text, 2, 100)
        self.buttons.append(button_exit)

    def render(self):
        if not self.is_create:
            self.create_menu()
            self.is_create = True
        for i in self.buttons:
            i.render(self.display)

        self.String.render_until("freck ruket", (124, 50), 4)
        self.render_character()


    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
    