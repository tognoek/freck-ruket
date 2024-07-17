import pygame


class Input():
    def __init__(self, name, pos, size):
        self.name = name
        self.pos = pos
        self.size = size
        self.font = pygame.font.Font(None, 18)
        self.text = ""
        self.selected = False

    def add_char(self, char):
        self.text = self.text + char

    def get_text(self):
        return self.text
    
    def set_text(self, text):
        self.text = text
    
    def select_input(self, pos, type_click):
        self.selected = False
        if self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]:
            if type_click == 1:
                self.selected = True

        if self.selected:
            self.text = ""
                
    def backspace(self):
        if self.text:
            self.text = self.text[:-1]

    def render(self, surface : pygame.Surface):
        text = self.font.render(self.text, True, (0, 0, 0))
        if text.get_width() + 4 > self.size[0]:
            background = pygame.Surface((text.get_width() + 6, self.size[1]))
        else:
            background = pygame.Surface(self.size)
        if not self.selected:
            background.fill((0, 0, 0))
        else:
            background.fill((255, 0, 0))
        pygame.draw.rect(background, (255, 255, 255), (1, 1, background.get_width() - 2, self.size[1] - 2))
        background.blit(text, (4, int(self.size[1] / 2 - text.get_height() / 2)))
        surface.blit(background, self.pos)