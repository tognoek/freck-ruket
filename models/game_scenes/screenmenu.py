import pygame

class ScreenMenu:
    
    def __init__(self, display : pygame.Surface):
        self.display = display

    def render(self):
        sur = pygame.Surface((100, 100))
        sur.fill((255, 0, 0, 0.1))
        self.display.blit(sur, (20, 20))

    def click_mouse(self, x, y, z):
        if 20 <= x <= 120 and 20 <= y <= 120:
            return z == 1
        else:
            return False
    