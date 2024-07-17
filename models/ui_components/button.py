import pygame


class Button:
    def __init__(self, name, text, color_on, color_off, pos, size, image = None) -> None:
        self.name = name
        self.text_show = text
        self.color_on = color_on
        self.color_off = color_off
        self.pos = pos
        self.size = size
        self.type = False
        self.image = image
        self.name_render = self.text_show
        self.font = pygame.font.Font(None, 18)

    def set_name(self, name_acction = None):
        if name_acction is not None:
            self.name_render = name_acction
        else:
            self.name_render = self.text_show

    def set_type(self, pos = (0, 0), type_click = -1):
        if self.pos[0] <= pos[0] and self.pos[0] + self.size_button[0] >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.size_button[1] >= pos[1]:  
                if type_click == 1:
                    self.type = not self.type
                    return True
                else:
                    return False

    def on_off(self):
        self.type = not self.type

    def render(self, surface : pygame.Surface):
        if self.type:
            self.text = self.font.render(self.name_render, True, self.color_on)
        else:
            self.text = self.font.render(self.name_render, True, self.color_off)
        self.size_button = (self.text.get_width() + self.size[0] + 2, self.text.get_height() + self.size[1] + 2)
        background = pygame.Surface(self.size_button)
        background.fill((0, 0, 0))
        pygame.draw.rect(background, (255, 255, 255), (1, 1, self.size_button[0] - 2, self.size_button[1] - 2))
        pos_text = (background.get_width() // 2 - self.text.get_width() // 2, background.get_height() // 2 - self.text.get_height() // 2)
        background.blit(self.text, pos_text)
        surface.blit(background, self.pos)
