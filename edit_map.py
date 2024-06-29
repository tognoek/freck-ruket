import pygame, sys, random
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

button_left = Button("Left", "X", (255, 0, 0), (0, 0, 255), (800, 35), (10, 5))
button_right = Button("Right", "X", (255, 0, 0), (0, 0, 255), (900, 35), (10, 5))
button_top = Button("Top", "X", (255, 0, 0), (0, 0, 255), (850, 5), (10, 5))
button_buttom = Button("Bottom", "X", (255, 0, 0), (0, 0, 255), (850, 65), (10, 5))
button_xy = Button("xy", "X-axis", (255, 0, 0), (0, 0 , 255), (650, 35), (10, 5))
button_centr = Button("center", "center", (255, 0, 0), (0, 0 , 255), (730, 35), (10, 5))
rect_status = pygame.Surface((60, 30))
rect_status.fill((0, 0, 0))
pygame.draw.rect(rect_status, (255, 255, 255), (1, 1, 58, 28))

buttons = [button_left, button_right, button_top, button_buttom, button_xy, button_centr]

status_button = {}
for i in buttons:
    status_button[i.name] = False

old_data = []

pos_rect_mini = None
rect_mini = pygame.Surface((8, 8))
x_random = [33, 47]
while True:

    pos_rect_mini = None
    if status_button["Left"]:
        if status_button["Right"]:
            pos_rect_mini = (854, 33)
        else:
            pos_rect_mini = (831, 33)
    else:
        if status_button["Right"]:
            pos_rect_mini = (881, 33)
    
    if status_button["Top"]:
        if pos_rect_mini == None:
            pos_rect_mini = (835, 19)
        if status_button["Bottom"]:
            pos_rect_mini = (pos_rect_mini[0], 39)
        else:
            pos_rect_mini = (pos_rect_mini[0], 31)
    else:
        if status_button["Bottom"]:
            if pos_rect_mini == None:
                pos_rect_mini = (835, 19)
            pos_rect_mini = (pos_rect_mini[0], 51)

    if status_button["center"]:
        pos_rect_mini = (854, 39)


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

    screen.blit(rect_status, (830, 30))

    if pos_rect_mini != None:
        screen.blit(rect_mini, pos_rect_mini)

    for key, value in data.items():
        x, y = map(int, key.split(":"))
        x, y = x + offset[0], y + offset[1]  
        display.blit(data_maps[value["name"]], (x, y))

    for i in buttons:
        i.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data_json["map"] = data
            save_map(data_json)
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_z] and keys[pygame.K_LCTRL]:
                if len(old_data) > 0:
                    data = old_data[-1]
                    old_data.pop()


        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in buttons:
                if i.set_type(mouse, event.button):
                    status_button[i.name] = not status_button[i.name]
                    if i.name == "xy":
                        if status_button[i.name]:
                            i.set_name("Y-axis")
                        else:
                            i.set_name("X-axis")

            if event.button == 1:
                key = str(pos[0]) + ":" + str(pos[1])
                value = {
                        "name" : list_name_maps_in_data_convert[index_entity_data_map],
                         "type" : 1,
                         "flip" : False
                         }
                old_data.append(data.copy())
                if len(old_data) > 30:
                    old_data.pop(0)
                data[key] = value
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
                    old_data.append(data)
                    if len(old_data) > 4:
                        old_data.pop(0)
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

