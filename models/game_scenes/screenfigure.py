import pygame
from models.ui_components.button import ImageButton
from models.ui_components.button import ButtonImage
from models.ui_components.string import String
from models.utils import Image

class Character:

    def __init__(self, name, image, pos, ratio):
        self.name = name
        self.image = image
        size = self.image.get_size()
        size = (int(size[0] * ratio), int(size[1] * ratio))
        self.image = pygame.transform.scale(self.image, size)
        self.pos = pos

    def render(self, display):
        display.blit(self.image, self.pos)

    def click_mouse(self, pos, z):
        if self.pos[0] <= pos[0] and self.pos[0] + self.image.get_width() >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.image.get_height() >= pos[1]:
                return z == 1
            


class ScreenFigure:
    def __init__(self, display, image_button, data_text):
        self.display = display
        self.String = String(self.display)
        self.image_button = image_button
        self.data_text = data_text

        self.background = pygame.image.load("data/Images/Menu/Buttons/frame_black.png")
        self.background = pygame.transform.scale(self.background, (280, 250))

        self.page = 1
        self.old_page = 0

        self.is_begin = True

        image_next = Image().load_image_button("Next")
        self.button_next = ImageButton("next", image_next, (410, 230), 3)
        image_previous = Image().load_image_button("Previous")
        self.button_previous = ImageButton("previous", image_previous, (130, 230), 3)
        image_back = Image().load_image_button("Back")
        self.button_back = ImageButton("back", image_back, (30, 30), 3)
        self.button_select = ButtonImage("select", "select", (228, 320), self.image_button, self.data_text, 2)
        self.buttons = [self.button_next, self.button_previous, self.button_back, self.button_select]

        self.name_characters = ["Mask Dude", "Ninja Frog", "Pink Man", "Virtual Guy"]
        self.image_character = Image().load_image_character(self.name_characters[self.page - 1])
        self.Character = Character(self.name_characters[self.page - 1], self.image_character, (236, 120), 4)

    def render(self):
        if self.page != self.old_page:
            self.old_page = self.page
            self.image_character = Image().load_image_character(self.name_characters[self.page - 1])
            self.Character = Character(self.name_characters[self.page - 1], self.image_character, (236, 120), 4)



        self.display.blit(self.background, (160, 130))
        self.String.render_until("Figure", (220 - 24, 50), 4)
        self.String.render_until(self.name_characters[self.page - 1], 
                                 (300 - len(self.name_characters[self.page - 1]) * 8 * 2 / 2, 270), 2)
        for i in self.buttons:
            i.render(self.display)

        self.Character.render(self.display)
        

    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
            
    def set_index_character(self, name):
        self.page = 1
        self.old_page = 0
        for i in range(len(self.name_characters)):
            if self.name_characters[i] == name:
                self.page = i + 1
        self.is_begin = False

    def get_name_character(self):
        return self.name_characters[self.page - 1]
            
    def set_page(self, index):
        self.page = self.page + index
        if self.page < 1:
            self.page = 4
        if self.page > 4:
            self.page = 1