import pygame, sys
import json

from scripts.utils import Image
from ENV import WINDOWS_SCREEN, DISPLAY_SIZE
from scripts.entities import *

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOWS_SCREEN)

icon = pygame.image.load("data/icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Tog")

display = pygame.Surface(DISPLAY_SIZE)

Image = Image()

class Level:
    def __init__(self, level = 1):
        
        block = pygame.Surface((32, 32))
        block_q = pygame.Surface((28, 28))
        block_q.fill((5, 5, 5))
        block.fill((255, 255, 255))
        block.blit(block_q, (2, 2))


        self.data_images = Image.convert_action_maps()

        self.data_json = {}
        self.data_maps = []
        self.level = level
        self.left_top = (0, 0)
        self.bottom_right = (0, 0)

    def load_map(self):
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        self.data_json = data

    def convert(self):
        self.bottom_right = None
        self.left_top = None
        for key, value in self.data_json["map"].items():
            x, y = map(int, key.split(":"))
            entity_map = Map(value["name"], (x, y), self.data_images[value["name"]], None, value["flip"], 0, 0, 5, int(value["type"]))
            self.data_maps.append(entity_map)
            if self.left_top == None:
                self.left_top = (x, y)
            elif self.left_top[0] > x:
                self.left_top = (x, self.left_top[1])
            elif self.left_top[1] > y:
                self.left_top = (self.left_top[0], y)
            if self.bottom_right == None:
                self.bottom_right = (x, y)
            elif self.bottom_right[0] < entity_map.rect().right:
                self.bottom_right = (entity_map.rect().right, self.bottom_right[1])
            elif self.bottom_right[1] < entity_map.rect().bottom:
                self.bottom_right = (self.bottom_right[0], entity_map.rect().bottom)

    def get_left_top(self):
        return self.left_top
    
    def get_bottom_right(self):
        return self.bottom_right

    def get_full_map(self):
        return self.data_maps   
    
    def draw(self, surface : pygame.Surface, offset = (0, 0)):
        for entity_map in self.data_maps: 
            surface.blit(pygame.transform.flip(entity_map.get_image(), entity_map.flip, False), (entity_map.get_pos()[0] + offset[0], entity_map.get_pos()[1] + offset[1]))

    def start_pos_player(self):
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        result = (int(data["start"]["x"]), int(data["start"]["y"]))
        return result
    
class Camera:
    def __init__(self, left_top, bottom_right, size_scroll):
        self.left_top = left_top
        self.bottom_right = bottom_right
        self.size_scroll = size_scroll
        self.scroll = [0, 0]

    def update(self, pos = (0, 0), rate = 30):
        self.scroll[0] += (self.size_scroll[0] / 2 - pos[0] - self.scroll[0]) / rate
        self.scroll[1] += (self.size_scroll[1] / 2 - pos[1] - self.scroll[1]) / rate
        self.scroll[0] = min(self.scroll[0], -1 * self.left_top[0])
        self.scroll[0] = max(self.scroll[0], -1 * (self.bottom_right[0] - self.size_scroll[0]))
        self.scroll[1] = min(self.scroll[1], -1 * self.left_top[1])
        self.scroll[1] = max(self.scroll[1], -1 * (self.bottom_right[1] - self.size_scroll[1]))
        print(self.scroll)

    def get_scroll(self):
        return (int(self.scroll[0]), int(self.scroll[1]))

class Game:
    def __init__(self):

        self.Background = Background(Image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))

        self.Level = Level(1)
        self.Level.load_map()
        self.Level.convert()

        self.String = String(display)

        self.start_player = self.Level.start_pos_player()

        self.Camera = Camera(self.Level.get_left_top(), self.Level.get_bottom_right(), (display.get_width(), display.get_height()))

        print(self.Level.get_left_top(), self.Level.get_bottom_right())
        
        Name = "Mask Dude"

        images, y = Image.load_images_main_character(Name)
        data_character = Image.load_data_charactre(Name)
        self.Player = Character("Player", self.start_player, images, None, False, 0.5, 0, data_character, 8, 0)
        self.Player.set_action("Run")

    def run(self):

        running = True

        while running:

            display.fill((10, 10, 100))
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
                        self.Player.speed_x(-3)

                    if event.key == pygame.K_RIGHT:
                        self.Player.speed_x(3)

                    if event.key == pygame.K_UP:
                        self.Player.speed_y(-5)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.Player.reset_speed(True)

                    if event.key == pygame.K_RIGHT:
                        self.Player.reset_speed(True)

            screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
            pygame.display.update()


        
if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
sys.exit()
