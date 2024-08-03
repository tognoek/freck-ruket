import pygame
from models.game_entities.character import Character
from models.game_scenes.level import Level
from models.game_scenes.camera import Camera
from models.game_scenes.gackground import Background
from models.utils import Data, Image, Text
from models.ui_components.string import String
from models.game_scenes.screenmenu import ScreenMenu
from models.game_scenes.screenpause import ScreenPause
from models.game_scenes.screenlevel import ScreenLevel
from models.game_scenes.screenfigure import ScreenFigure
from models.game_scenes.sceensetting import ScreenSetting
from models.utils import Save
MAXLEVEL = 50

class GameCanvas:

    def __init__(self, display : pygame.Surface, ratio):
        self.display = display
        self.ratio = ratio
        self.image = Data()
        self.image_mouse = Data().load_mouse()
        self.Save = Save()

        self.Background = Background(self.image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        self.Level = Level(-1, self.image)
        self.String = String(self.display)

        self.ImageButton = Image().load_image("data/Images/Menu/Buttons/frame.png")

        self.framebig = pygame.image.load("data/Images/Menu/Buttons/framebig.png")
        self.framebig = pygame.transform.scale(self.framebig, self.display.get_size())

        self.Text = Text()
        self.Text.create()

        self.name_character = self.Save.get_character()

        self.ScreenLevel = ScreenLevel(self.display)
        self.ScreenSetting = ScreenSetting(self.display)
        self.ScreenFigure = ScreenFigure(self.display, self.ImageButton, self.Text)
        self.ScreenMenu = ScreenMenu(self.display, self.ImageButton, self.Text)
        self.ScreenMenu.update_images_character(self.name_character)
        self.ScreenPause = ScreenPause(self.display, self.ImageButton, self.Text)

        self.index_level = self.Save.get_start()
        self.is_pause = False
        self.is_play = False
        self.is_menu = True
        self.is_menu_level = False
        self.is_menu_figure = False
        self.is_menu_setting = False

        self.exit = False

    def load_player(self, name = "Pink Man"):
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
        self.load_player(self.name_character)
        self.create_camera()

    def create_now(self, index):
        self.Level.run(index)
        self.index_level = index
        self.load_player(self.name_character)
        self.create_camera()

    def run(self, mouse = (0, 0)):
        if self.is_play:
            self.update()
        self.render(mouse)

    def update(self):
        if self.Level.sum_point == 0:
            self.Player.rate_play = 100
        else:
            self.Player.rate_play = int(round(self.Player.point / self.Level.sum_point, 2) * 100)
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

        if self.Level.next_level:
            self.index_level += 1
            if self.index_level > MAXLEVEL:
                self.index_level = MAXLEVEL
            self.Save.save_lock(self.index_level)
            self.Save.update_start(self.index_level)
            self.create()


    def menu_play(self):
        self.String.render_until(str(self.Player.rate_play), pos=(100, 100))

    def render(self, mouse = (0, 0)):
        self.display.fill((142, 207, 210))
        if self.is_play:
            self.Background.render(self.display)
            self.Level.render(self.display, self.Camera.get_scroll(), self.Player.get_pos(), 900, False)
            self.Player.render(self.display, self.Camera.get_scroll(), False)
            self.String.render_until(self.Player.action, pos=(100, 150))
            self.menu_play()

        if self.is_menu:
            self.ScreenMenu.render()

        if self.is_menu_level:
            self.ScreenLevel.render()

        if self.is_menu_setting:
            self.ScreenSetting.render()

        if self.is_menu_figure:
            if self.ScreenFigure.is_begin:
                self.ScreenFigure.set_index_character(self.name_character)
            self.ScreenFigure.render()

        if self.is_pause:
            self.Background.render(self.display)
            self.Level.render(self.display, self.Camera.get_scroll(), self.Player.get_pos(), 900, True)
            self.Player.render(self.display, self.Camera.get_scroll(), False)
            self.ScreenPause.render()

        if not self.is_play:
            self.display.blit(self.image_mouse, (mouse[0] * self.ratio[0], mouse[1] * self.ratio[1]))
            self.display.blit(self.framebig, (0, 0))
            

    def event(self, event, mouse):
        if self.is_play:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.X = False

                if event.key == pygame.K_RIGHT:
                    self.X = True

                if event.key == pygame.K_UP:
                    self.Player.speed_y(-6)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.X = None

                if event.key == pygame.K_RIGHT:
                    self.X = None

        if event.type == pygame.MOUSEBUTTONUP:
            self.click_mouse(mouse[0] * self.ratio[0], mouse[1] * self.ratio[1], event.button)
        
        return self.exit

    def click_mouse(self, x, y, z):
        if self.is_menu:
            name_click = self.ScreenMenu.click_mouse(x, y, z)
            if name_click == "start":
                self.create()
                self.index_level = self.Save.get_start()
                self.is_menu = False
                self.is_play = True

            if name_click == "setting":
                self.is_menu = False
                self.is_menu_setting = True


            if name_click == "level":
                self.is_menu = False
                self.is_menu_level = True

            if name_click == "figure":
                self.is_menu = False
                self.is_menu_figure = True
                self.ScreenFigure.is_begin = True
            
            if name_click == "exit":
                self.exit = True

        if self.is_pause:
            name_click = self.ScreenPause.click_mouse(x, y, z)
            if name_click == "resume":
                self.is_pause = False
                self.is_play = True
            if name_click == "home":
                self.is_pause = False
                self.is_menu = True
                self.Save.update_start(self.index_level)
            if name_click == "reset":
                self.create()
                self.is_pause = False
                self.is_play = True

        if self.is_menu_level:
            name_click = self.ScreenLevel.click_mouse(x, y, z)
            if name_click == "next":
                self.ScreenLevel.set_page(1)
            if name_click == "previous":
                self.ScreenLevel.set_page(-1)
            if name_click == "back":
                self.is_menu_level = False
                self.is_menu = True
            try:
                index = int(name_click)
                self.create_now(index)
                self.is_menu_level = False
                self.is_play = True
            except ValueError:
                pass
        if self.is_menu_setting:
            name_click = self.ScreenSetting.click_mouse(x, y, z)
            if name_click == "back":
                self.is_menu_setting = False
                self.is_menu = True

        
        if self.is_menu_figure:
            name_click = self.ScreenFigure.click_mouse(x, y, z)
            if name_click == "next":
                self.ScreenFigure.set_page(1)
            if name_click == "previous":
                self.ScreenFigure.set_page(-1)
            if name_click == "back":
                self.is_menu_figure = False
                self.is_menu = True

            if name_click == "select":
                self.name_character = self.ScreenFigure.get_name_character()
                self.Save.update_character(self.name_character)
                self.ScreenMenu.update_images_character(self.name_character)
                self.is_menu_figure = False
                self.is_menu = True