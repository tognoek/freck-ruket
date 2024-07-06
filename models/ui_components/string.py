import pygame

class String:
    def __init__(self, surface : pygame.Surface) -> None:
        self.surface = surface

    def create_text(self, text, color =(255, 255, 255), font = 18):
        font = pygame.font.Font(None, font)
        self.text = font.render(text, True, color)
    
    def render_edit(self, center = False):
        if center:
            pos = (self.surface.get_width() // 2 - self.text.get_width() // 2, self.surface.get_height() // 2 - self.text.get_height() // 2)
        self.surface.blit(self.text, pos)

    def render(self, text, pos = (0, 0), color =(255, 255, 255), font = 18, center = False):
        font = pygame.font.Font(None, font)
        text = font.render(text, True, color)
        if center:
            pos = (self.surface.get_width() // 2 - text.get_width() // 2, self.surface.get_height() // 2 - text.get_height() // 2)
        self.surface.blit(text, pos)
