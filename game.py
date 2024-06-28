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

    def load_map(self):
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        self.data_json = data

    def convert(self):
        for key, value in self.data_json["map"].items():
            x, y = map(int, key.split(":"))
            entity_map = Map(value["name"], (x, y), self.data_images[value["name"]], None, False, 0, 0, 5, 1)
            self.data_maps.append(entity_map)

    def get_full_map(self):
        return self.data_maps   
    
    def draw(self, surface : pygame.Surface, offset = (0, 0)):
        for entity_map in self.data_maps: 
            surface.blit(pygame.transform.flip(entity_map.get_image(), entity_map.flip, False), entity_map.get_pos())

    def start_pos_player(self):
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        result = (int(data["start"]["x"]), int(data["start"]["y"]))
        return result

class Game:
    def __init__(self):

        self.Background = Background(Image.load_background())
        self.Background.create("Blue", (display.get_width(), display.get_height()))

        self.Level = Level(1)
        self.Level.load_map()
        self.Level.convert()

        self.String = String(display)

        self.start_player = self.Level.start_pos_player()

    def run(self):

        Name = "Mask Dude"

        x, y = Image.load_images_main_character(Name)
        data_character = Image.load_data_charactre(Name)
        Player = Character("Player", self.start_player, x, None, False, 0.5, 0, data_character, 8, 0)
        Player.set_action("Run")
        running = True

        while running:

            display.fill((10, 10, 100))
            self.Background.render(display)

            self.Level.draw(display)

            clock.tick(60)

            Player.update_speed()

            Player.update(self.Level.get_full_map())

            Player.render(display, (0, 0))

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
                        Player.speed_x(-3)

                    if event.key == pygame.K_RIGHT:
                        Player.speed_x(3)

                    if event.key == pygame.K_UP:
                        Player.speed_y(-8)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        Player.reset_speed(True)

                    if event.key == pygame.K_RIGHT:
                        Player.reset_speed(True)

            screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
            pygame.display.update()


        
if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
sys.exit()
