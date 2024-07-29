import pygame, sys
import json

from models.utils import Data
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


class Game:
    def __init__(self):

        self.image = Data()

        self.Background = Background(self.image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        self.String = String(display)

        self.Level = Level(1, self.image)
    def load_map(self, level = 1):
        self.Level.load_map(level)
        self.Level.create_data()
        self.Level.convert()
        self.Level.sort_by_type()
        self.Level.filter_type()

    def load_player(self, Name = "Ninja Frog"):
        images, y = self.image.load_images_main_character(Name)
        data_character = self.image.load_data_charactre(Name)
        self.Player = Character("Player", self.Level.start_pos_player()
                                , images, None, [False, False], 0.5, 0
                                , data_character, 4, 0)
        self.Player.set_action("Run")
        
        self.X = None
        self.Y = None

    def create_camera(self):
        self.Camera = Camera(self.Level.get_left_top(), self.Level.get_bottom_right(), (display.get_width(), display.get_height()))  
    def run(self):
        self.load_map()
        self.load_player()
        self.create_camera()
        running = True

        while running:

            display.fill((10, 10, 100))

            if self.X != None:
                if self.X:
                    self.Player.speed_x(3)
                else:
                    self.Player.speed_x(-3)
            else:
                if not self.Player.isHit():
                    self.Player.reset_speed(True)

            self.Background.render(display)

            self.Level.draw(display, self.Camera.get_scroll())
            self.Level.update_fps(clock.get_fps())
            
            clock.tick(60)

            if not self.Player.isDie():

                self.Player.update_speed()

                self.Player.run(self.Level)

            if not self.Player.isHit():
                self.Camera.update(self.Player.get_pos())

            self.Player.render(display, self.Camera.get_scroll(), True)

            # screen.fill((255, 255, 255))

            self.String.render(str(int(clock.get_fps())), pos=(100, 100))
            self.String.render(self.Player.action, pos=(100, 150))

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
                        self.Player.speed_y(-6)

                    if event.key == pygame.K_k:
                        self.load_map()
                        self.load_player()
                        self.create_camera()
                    
                    if event.key == pygame.K_l:
                        self.Player.reset()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.X = None

                    if event.key == pygame.K_RIGHT:
                        self.X = None

            screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
            pygame.display.update()


        
if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
sys.exit()
