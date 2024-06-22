import pygame, sys

from scripts.utils import Image

from scripts.entities import *

pygame.init()

clock = pygame.time.Clock()

WINDOWS_SCREEN = (960, 720)

DISPLAY_SIZE = (480, 360)

screen = pygame.display.set_mode(WINDOWS_SCREEN)

display = pygame.Surface(DISPLAY_SIZE)

Image = Image()

class Game:
    def __init__(self):
        pass

    def run(self):


        x, y = Image.load_images_main_character("Mask Dude")
        Player = Entiti("Player", (100, 100), x, None, False, 0.5, 0, 4)
        Player.set_action("Wall Jump")
        running = True

        while running:

            clock.tick(60)

            Player.update()

            display.blit(Player.get_image(), Player.pos)


            screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()


            screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
            pygame.display.update()


        
if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
sys.exit()
