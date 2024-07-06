import pygame, sys
import json

from models.utils import Image
from ENV import WINDOWS_SCREEN, DISPLAY_SIZE
from models.game_scenes.level import Level
from models.game_entities.character import Character
from models.game_scenes.camera import Camera
from models.ui_components.button import Button
from models.ui_components.string import String

from models.game_scenes.gackground import Background

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOWS_SCREEN)

icon = pygame.image.load("data/icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Tog")

display = pygame.Surface(DISPLAY_SIZE)

image = Image()

class Game:
    def __init__(self):

        self.Background = Background(image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))

        self.Level = Level(1, image)
        self.Level.load_map()
        self.Level.convert()

        self.String = String(display)

        self.start_player = self.Level.start_pos_player()

        self.Camera = Camera(self.Level.get_left_top(), self.Level.get_bottom_right(), (display.get_width(), display.get_height()))
        
        Name = "Mask Dude"

        images, y = image.load_images_main_character(Name)
        data_character = image.load_data_charactre(Name)
        self.Player = Character("Player", self.start_player, images, None, False, 0.5, 0, data_character, 8, 0)
        self.Player.set_action("Run")
        
        self.X = None
        self.Y = None

    def run(self):

        running = True

        while running:

            display.fill((10, 10, 100))

            if self.X != None:
                if self.X:
                    self.Player.speed_x(3)
                else:
                    self.Player.speed_x(-3)
            else:
                self.Player.reset_speed(True)

            self.Background.render(display)

            self.Level.draw(display, self.Camera.get_scroll())
            clock.tick(60)

            self.Player.update_speed()

            self.Player.update(self.Level.get_full_map())

            self.Camera.update(self.Player.get_pos())

            self.Player.render(display, self.Camera.get_scroll(), False)

            # screen.fill((255, 255, 255))

            self.String.render(str(int(clock.get_fps())), pos=(100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        self.X = False

                    if event.key == pygame.K_RIGHT:
                        self.X = True

                    if event.key == pygame.K_UP:
                        self.Player.speed_y(-5)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.X = None

                    if event.key == pygame.K_RIGHT:
                        self.Player.reset_speed(True)

            screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
            pygame.display.update()


        
if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
sys.exit()
