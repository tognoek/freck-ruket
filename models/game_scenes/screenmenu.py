import pygame
from models.ui_components.button import ButtonImage

class ScreenMenu:
    
    def __init__(self, display : pygame.Surface, image_button, data_text):
        self.display = display
        self.image_button = image_button
        self.data_text = data_text
        self.buttons = []
        self.is_menu = False

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
        if not self.is_menu:
            self.create_menu()
            self.is_menu = True
            print("Create Menu")
        for i in self.buttons:
            i.render(self.display)

    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
    