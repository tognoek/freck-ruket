import pygame
from models.ui_components.button import ButtonImage

class ScreenPause:
    
    def __init__(self, display : pygame.Surface, image_button, data_text):
        self.display = display
        self.image_button = image_button
        self.data_text = data_text

        Resume = ButtonImage("resume", "resume", (200, 170),
                                  self.image_button, self.data_text, 2, 100)
        Reset = ButtonImage("reset", "reset", (200, 230),
                                  self.image_button, self.data_text, 2, 100)
        Home = ButtonImage("home", "home", (200, 290),
                                  self.image_button, self.data_text, 2, 100)
        

        self.buttons = [Resume,Reset, Home]


    def render(self):
        bgr_sur = pygame.Surface((self.display.get_width(), self.display.get_height()))
        bgr_sur.fill((100, 100, 100))
        bgr_sur.set_alpha(100)
        self.display.blit(bgr_sur, (0, 0))
        for i in self.buttons:
            i.render(self.display)
    def click_mouse(self, x, y, z):
        for i in self.buttons:
            if i.click_mouse((x, y), z):
                return i.name
    