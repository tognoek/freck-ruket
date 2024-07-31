import pygame
from models.game_entities.character import Character
from models.game_scenes.level import Level
from models.game_scenes.camera import Camera
from models.game_scenes.gackground import Background
from models.utils import Data
from models.ui_components.string import String
from models.game_scenes.screenmenu import ScreenMenu
from models.game_scenes.screenpause import ScreenPause


class GameCanvas:

    def __init__(self, display : pygame.Surface, ratio):
        self.display = display
        self.ratio = ratio
        self.image = Data()
        self.image_mouse = Data().load_mouse()

        self.Background = Background(self.image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        self.Level = Level(1, self.image)
        self.String = String(self.display)

        self.ScreenMenu = ScreenMenu(self.display)
        self.ScreenPause = ScreenPause(self.display)

        self.index_level = 1
        self.is_pause = False
        self.is_play = False
        self.is_menu = True

    def load_player(self, name = "Ninja Frog"):
        images, y = self.image.load_images_main_character(name)
        data_character = self.image.load_data_charactre(name)
        self.Player = Character("Player", self.Level.start_pos_player()
                                , images, None, [False, False], 0.5, 0
                                , data_character, 4, 0)
        self.Player.set_action("Run")
        
        self.X = None
        self.Y = None

    def create_camera(self):
        self.Camera = Camera(self.Level.get_left_top(), self.Level.get_bottom_right(), 
                             (self.display.get_width(), self.display.get_height()))  

    def create(self):
        self.Level.run(self.index_level)
        self.load_player()
        self.create_camera()

    def run(self, mouse = (0, 0)):
        if self.is_play:
            self.update()
        self.render(mouse)

    def update(self):
        if self.X != None:
            if self.X:
                self.Player.speed_x(3)
            else:
                self.Player.speed_x(-3)
        else:
            if not self.Player.isHit():
                self.Player.reset_speed(True)

        if not self.Player.isDie():
            self.Player.update_speed()
            self.Player.run(self.Level)

        if not self.Player.isHit():
            self.Camera.update(self.Player.get_pos())

        self.Level.update(self.Player.get_pos())

    def render(self, mouse = (0, 0)):
        if self.is_play:
            self.Background.render(self.display)
            self.Level.render(self.display, self.Camera.get_scroll(), self.Player.get_pos(), 500, False)
            self.Player.render(self.display, self.Camera.get_scroll(), True)
            self.String.render_until(self.Player.action, pos=(100, 150))

        if self.is_menu:
            self.ScreenMenu.render()

        if self.is_pause:
            self.Background.render(self.display)
            self.Level.render(self.display, self.Camera.get_scroll(), self.Player.get_pos(), 500, True)
            self.Player.render(self.display, self.Camera.get_scroll(), True)
            self.ScreenPause.render()

        if not self.is_play:
            self.display.blit(self.image_mouse, (mouse[0] * self.ratio[0], mouse[1] * self.ratio[1]))

    def event(self, event, mouse):
        if self.is_play:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.X = False

                if event.key == pygame.K_RIGHT:
                    self.X = True

                if event.key == pygame.K_UP:
                    self.Player.speed_y(-6)

                if event.key == pygame.K_k:
                    self.create()
                        
                if event.key == pygame.K_l:
                    self.Player.reset()

                if event.key == pygame.K_i:
                    self.is_pause = True
                    self.is_play = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.X = None

                if event.key == pygame.K_RIGHT:
                    self.X = None

        if event.type == pygame.MOUSEBUTTONUP:
            self.click_mouse(mouse[0] * self.ratio[0], mouse[1] * self.ratio[1], event.button)

    def click_mouse(self, x, y, z):
        if self.is_menu:
            if self.ScreenMenu.click_mouse(x, y, z):
                self.is_menu = False
                self.is_play = True

        if self.is_pause:
            if self.ScreenPause.click_mouse(x, y, z):
                self.is_pause = False
                self.is_play = True