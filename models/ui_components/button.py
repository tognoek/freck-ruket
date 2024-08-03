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

class ButtonImage:
    def __init__(self, name, text, pos, image, data_text, ratio = 1, max_width = None) -> None:
        self.name = name
        self.pos = pos
        self.text = data_text.get_text(text)
        self.len = len(text)
        self.image = image
        self.ratio = ratio
        self.max = max_width
        self.is_click = False
        self.width = int(8 * self.ratio)
        self.height = int(10 * self.ratio)
        if self.max is not None:
            self.width_image_button = max(self.width * self.len + 20 * self.ratio, self.max * self.ratio)
        else:
            self.width_image_button = self.width * self.len + 20 * self.ratio
        self.height_image_button = self.height + 14 * self.ratio

    def click_mouse(self, pos, z):
        self.is_click = False
        if self.pos[0] <= pos[0] and self.pos[0] + self.width_image_button >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.height_image_button >= pos[1]:
                self.is_click = z == 1
        return self.is_click

    def render(self, surface : pygame.Surface):
        surface.blit(pygame.transform.scale(self.image,(self.width_image_button, self.height_image_button)), self.pos)
        left_text = self.width_image_button - self.width * self.len
        left_text = left_text / 2
        for i, v in enumerate(self.text):
            image = pygame.transform.scale(v,(self.width, self.height))
            surface.blit(image, (int(self.pos[0] + left_text + self.width * i), int(self.pos[1] + 5 * self.ratio)))

class ImageButton:

    def __init__(self, name, image, pos, ratio = 1) -> None:
        self.name = name
        self.pos = pos
        self.image = pygame.transform.scale(image, (image.get_width() * ratio, image.get_height() * ratio))
        self.ratio = ratio

    def render(self, display):
        display.blit(self.image, self.pos)

    def click_mouse(self, pos, z):
        if self.pos[0] <= pos[0] and self.pos[0] + self.image.get_width() >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.image.get_height() >= pos[1]:
                return z == 1
            
        return False
        
        

