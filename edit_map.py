import pygame, sys
import json
from scripts.utils import *
from scripts.entities import *

from ENV import WINDOWS_SCREEN, EDIT_SIZE, DISPLAY_SIZE

pygame.init()

screen = pygame.display.set_mode(WINDOWS_SCREEN)

pygame.display.set_caption("Edit Map");

icon = pygame.image.load("data/icon.png")

pygame.display.set_icon(icon)
display = pygame.Surface(EDIT_SIZE)

SIZE_IMAGE_SHOW = (int((WINDOWS_SCREEN[0] - EDIT_SIZE[0]) / 10 * 7), int((WINDOWS_SCREEN[1] - EDIT_SIZE[1]) / 10 * 7))
SIZE_SHOW = (int(WINDOWS_SCREEN[0] - EDIT_SIZE[0]), int((WINDOWS_SCREEN[1] - EDIT_SIZE[1])))

tognoek = pygame.Surface((display.get_width() - 2, display.get_height() - 2))
tognoek.fill((100, 50, 20))

data_maps = Image().load_data_maps()

name_data_maps = list(data_maps.keys())
name_key_maps = []
data_maps_convert = {}
for i in name_data_maps:
    key = i.split('_')[0]
    if key not in data_maps_convert:
        data_maps_convert[key] = {}
        name_key_maps.append(key)
    else:
        data_maps_convert[key][i] = data_maps[i]
index_name_data_map = 0
index_entity_data_map = 0
list_name_maps_in_data_convert = list(data_maps_convert[name_key_maps[0]].keys())

data = {}

with open("data/Json/Level/level_1.json", "r") as file:
    data_json = json.load(file)

data = data_json["map"]


clock = pygame.time.Clock()

speed_offset = 3

offset = (0, 0)

offset_screen = (screen.get_width() - display.get_width(), screen.get_height() - display.get_height())

pos = (0, 0)

def save_map(data):
    with open("data/Json/Level/level_1.json", "w") as file:
        json.dump(data, file, indent=3)

action = {"up": False, "down": False, "left": False, "right": False}

Button = Button("Theo X", (255, 0, 0), (0, 0, 255), (500, 20), (10, 5))


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

    mouse = mousedown

    mousedown = (mousedown[0] - offset[0], mousedown[1] - offset[1])


    pos = (int(mousedown[0] - offset_screen[0]), int(mousedown[1] - offset_screen[1]))


    display.fill((0, 0, 0))
    screen.fill((250,200,110))
    display.blit(tognoek, (1, 1))

    image_real = data_maps[list_name_maps_in_data_convert[index_entity_data_map]]

    width = image_real.get_width()
    height = image_real.get_height()
    if width < SIZE_IMAGE_SHOW[0] or height < SIZE_IMAGE_SHOW[1]:
        if width < height:
            scale = SIZE_IMAGE_SHOW[0] / height
        else:
            scale = SIZE_IMAGE_SHOW[1] / width
        image_show = pygame.transform.scale(image_real, (int(width * scale), int(scale * height)))
    else:
        image_show = image_real
    
    screen.blit(image_show, (int((SIZE_SHOW[0] - image_show.get_width()) / 2), int((SIZE_SHOW[1] - image_show.get_height()) / 2)))
    screen.blit(image_real, (int((SIZE_SHOW[0] - image_real.get_width()) / 2 + SIZE_SHOW[0]), int((SIZE_SHOW[1] - image_real.get_height()) / 2)))

    for key, value in data.items():
        x, y = map(int, key.split(":"))
        x, y = x + offset[0], y + offset[1]  
        display.blit(data_maps[value["name"]], (x, y))

    Button.set_type(mouse)

    Button.render(screen)

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
                        "name" : list_name_maps_in_data_convert[index_entity_data_map],
                         "type" : 1,
                         "flip" : False
                         }
            data[key] = value
            keys = pygame.key.get_pressed()
            if event.button == 4:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    index_entity_data_map = 0
                    index_name_data_map -= 1
                    if index_name_data_map < 0:
                        index_name_data_map = len(name_key_maps) - 1
                    list_name_maps_in_data_convert = list(data_maps_convert[name_key_maps[index_name_data_map]].keys())
                else:
                    index_entity_data_map -= 1
                    if index_entity_data_map < 0:
                        index_entity_data_map = len(list_name_maps_in_data_convert) - 1
            if event.button == 5:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    index_entity_data_map = 0
                    index_name_data_map += 1
                    if index_name_data_map >= len(name_key_maps):
                        index_name_data_map = 0
                    list_name_maps_in_data_convert = list(data_maps_convert[name_key_maps[index_name_data_map]].keys())
                else:
                    index_entity_data_map += 1
                    if index_entity_data_map >= len(list_name_maps_in_data_convert):
                        index_entity_data_map = 0

            if event.button == 3:
                key = str(pos[0]) + ":" + str(pos[1])
                if key in data:
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
    screen.blit(pygame.transform.scale(display, EDIT_SIZE), (WINDOWS_SCREEN[0] - EDIT_SIZE[0], WINDOWS_SCREEN[1] - EDIT_SIZE[1]))
    pygame.display.update()
    clock.tick(60)

pygame.quit()

