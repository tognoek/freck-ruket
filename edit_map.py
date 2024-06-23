import pygame, sys
import json

from ENV import WINDOWS_SCREEN, DISPLAY_SIZE, IMAGE_SIZE, RATIO

pygame.init()

screen = pygame.display.set_mode(WINDOWS_SCREEN)

pygame.display.set_caption("Edit Map");

icon = pygame.image.load("data/icon.png")

pygame.display.set_icon(icon)
display = pygame.Surface(DISPLAY_SIZE)

block = pygame.Surface((32, 32))
block.fill((255, 255, 255))

data_map = {}

data_map["block"] = block

data = {}

with open("data/Json/Level/level_1.json", "r") as file:
    data_json = json.load(file)

data = data_json["map"]


clock = pygame.time.Clock()

speed_offset = 3

offset = (0, 0)

pos = (0, 0)

def save_map(data):
    with open("data/Json/Level/level_1.json", "w") as file:
        json.dump(data, file, indent=3)

action = {"up": False, "down": False, "left": False, "right": False}

while True:

    if action["up"]:
        offset = (offset[0], offset[1] + speed_offset)
    if action["down"]:
        offset = (offset[0], offset[1] - speed_offset)
    if action["left"]:
        offset = (offset[0] + speed_offset, offset[1])
    if action["right"]:
        offset = (offset[0] - speed_offset, offset[1])

    mousedown = pygame.mouse.get_pos()

    mousedown = (int(mousedown[0] / RATIO[0]), int(mousedown[1] / RATIO[1]))

    mousedown = (mousedown[0] - offset[0], mousedown[1] - offset[1])

    if mousedown[0] < 0:
        mousedown = (mousedown[0] - IMAGE_SIZE[0], mousedown[1])

    if mousedown[1] < 0:
        mousedown = (mousedown[0], mousedown[1] - IMAGE_SIZE[1])


    pos = (int(mousedown[0] / IMAGE_SIZE[0]), int(mousedown[1] / IMAGE_SIZE[1]))


    display.fill((0, 0, 0))

    offset_line = (int(offset[0] % IMAGE_SIZE[0]), int(offset[1] % IMAGE_SIZE[1]))

    for i in range(int(DISPLAY_SIZE[0] / IMAGE_SIZE[0]) + 2):
        if i % 2 == 0:
            color = (100, 100, 100)
        else:
            color = (255, 255, 255)
        pygame.draw.line(display, color, (i * IMAGE_SIZE[0]+ offset_line[0], 0), (i * IMAGE_SIZE[0]+ offset_line[0], DISPLAY_SIZE[1]), 1)

    for i in range(int(DISPLAY_SIZE[1] / IMAGE_SIZE[1] + 2)):
        if i % 2 == 1:
            color = (100, 100, 100)
        else:
            color = (255, 255, 255)
        pygame.draw.line(display, color, (0, i * IMAGE_SIZE[1] + offset_line[1]), (DISPLAY_SIZE[0], i * IMAGE_SIZE[1] + offset_line[1]), 1)

    for key, value in data.items():
        x, y = map(int, key.split(":"))
        x, y = x * IMAGE_SIZE[0] + offset[0], y * IMAGE_SIZE[1] + offset[1]  
        display.blit(data_map[value["name"]], (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data_json["map"] = data
            save_map(data_json)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                key = str(pos[0]) + ":" + str(pos[1])
                value = {
                        "name" : "block",
                         "type" : 1,
                         "flip" : False
                         }
                data[key] = value

            if event.button == 3:
                key = str(pos[0]) + ":" + str(pos[1])
                data.pop(key)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                data_json["map"] = data 
                save_map(data_json)
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_UP:
                action["up"] = True
            if event.key == pygame.K_DOWN:
                action["down"] = True
            if event.key == pygame.K_LEFT:
                action["left"] = True
            if event.key == pygame.K_RIGHT:
                action["right"] = True

            if event.key == pygame.K_k:
                speed_offset += 1
                if speed_offset > 32:
                    speed_offset = 32
            
            if event.key == pygame.K_l:
                speed_offset -= 1
                if speed_offset < 1:
                    speed_offset = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                action["up"] = False
            if event.key == pygame.K_DOWN:
                action["down"] = False
            if event.key == pygame.K_LEFT:
                action["left"] = False
            if event.key == pygame.K_RIGHT:
                action["right"] = False
    screen.fill((0,0,0))
    screen.blit(pygame.transform.scale(display, WINDOWS_SCREEN), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()

