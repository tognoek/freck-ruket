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
#  mảng 2 chiều chứa ảnh phân theo tên

data_images_x = {}
# danh sách các ảnh hiển thị ngang

data_images_y = {}
# danh sách các ảnh hiển thị dọc

for i in name_data_maps: # lọc ra các ảnh theo tiền tố của tên
    key = i.split('_')[0]
    if key not in data_maps_convert:
        data_maps_convert[key] = {}
        name_key_maps.append(key)
        data_images_x[key] = data_maps[i]
    
    data_maps_convert[key][i] = data_maps[i]
index_name_data_map = 0
index_entity_data_map = 0
list_name_maps_in_data_convert = list(data_maps_convert[name_key_maps[0]].keys())

for i in data_maps_convert[name_key_maps[0]].keys():
    data_images_y[i] = data_maps[i]

data = {}

with open("data/Json/Level/level_1.json", "r") as file:
    data_json = json.load(file)

data = data_json["map"]

clock = pygame.time.Clock()

speed_offset = 3

offset = (0, 0)

offset_screen = (screen.get_width() - display.get_width(), screen.get_height() - display.get_height())

pos = (0, 0)

alt_c = False
pos_begin_select = None
update_map = True

def render(surface : pygame.Surface, image : pygame.Surface, size = (0, 0), pos = (0, 0), rect = False):
    scale_x = size[0] / image.get_width()
    scale_y = size[1] / image.get_height()
    if scale_x > scale_y:
        image = pygame.transform.scale(image, (scale_y * image.get_width() - 4, scale_y * image.get_height() - 4))
    else:
        image = pygame.transform.scale(image, (scale_x * image.get_width() - 4, scale_x * image.get_height() - 4))

    size_x = image.get_width()
    size_y = image.get_height()
    
    surface.blit(image, (pos[0] + int((size[0] - size_x) / 2), pos[1] + int((size[1] - size_y) / 2)))
    if rect:
        pygame.draw.rect(surface, (255, 0, 0), (pos[0], pos[1], size[0], size[1]), 1)


def save_map(data):
    with open("data/Json/Level/level_1.json", "w") as file:
        json.dump(data, file, indent=3)

action = {"up": False, "down": False, "left": False, "right": False}

button_left = Button("Left", "X", (255, 0, 0), (0, 0, 255), (800, 35), (10, 5))
button_right = Button("Right", "X", (255, 0, 0), (0, 0, 255), (900, 35), (10, 5))
button_top = Button("Top", "X", (255, 0, 0), (0, 0, 255), (850, 5), (10, 5))
button_buttom = Button("Bottom", "X", (255, 0, 0), (0, 0, 255), (850, 65), (10, 5))
button_xy = Button("xy", "X-axis", (25, 30 , 10), (25, 30 , 10), (650, 15), (10, 5))
button_center = Button("center", "center", (255, 0, 0), (0, 0 , 255), (720, 15), (10, 5))
button_type_1 = Button("type_1", "1", (255, 0, 0), (0, 0, 255), (650, 55), (10, 5))
button_type_2 = Button("type_2", "2", (255, 0, 0), (0, 0, 255), (700, 55), (10, 5))
button_type_3 = Button("type_3", "3", (255, 0, 0), (0, 0, 255), (750, 55), (10, 5))
rect_status = pygame.Surface((60, 30))
rect_status.fill((0, 0, 0))
pygame.draw.rect(rect_status, (255, 255, 255), (1, 1, 58, 28))

buttons = [button_left, button_right, button_top, button_buttom, button_xy, button_center, button_type_1, button_type_2, button_type_3]
buttons[6].on_off()

status_button = {}
for i in buttons:
    status_button[i.name] = False

old_data = []

pos_rect_mini = None
rect_mini = pygame.Surface((8, 8))
x_random = [33, 47]

tool_ponit_map = [-2, -2, 1]
vector_tool = False
entity_maps = []
begin_select = False

list_select = []
minimap_select = None
key_select = None

class MiniMap:
    def __init__(self, surface : pygame.Surface, name, e_type, flip, x, y, select = False):
        self.surface = surface
        self.name = name
        self.e_type = e_type
        self.flip = flip
        self.x = x
        self.y = y
        self.select = select
    def height(self):
        return self.surface.get_height()
    
    def width(self):
        return self.surface.get_width()

    def bottom(self):
        return self.surface.get_height() + self.y
    
    def right(self):
        return self.surface.get_width() + self.x
    
    def rect(self):
        return pygame.Rect((self.x, self.y), self.surface.get_size())

    def collision(self, pos):
        rect_1 = pygame.Rect((pos[0], pos[1]), (1, 1))
        rect_2 = pygame.Rect((self.x, self.y), self.surface.get_size())
        return rect_1.collidedict(rect_2)
    
    def render(self, surface : pygame.Surface, offset = (0, 0)):
        surface.blit(self.surface, (self.x + offset[0], self.y + offset[1]))
        if self.e_type == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x + offset[0], self.y + offset[1], self.surface.get_width(), self.surface.get_height()), 2)
        if self.e_type == 3:
            pygame.draw.rect(surface, (0, 255, 0), (self.x + offset[0], self.y + offset[1], self.surface.get_width(), self.surface.get_height()), 2)
        if self.select:
            pygame.draw.rect(surface, (255, 0, 0), (self.x + offset[0], self.y + offset[1], self.surface.get_width(), self.surface.get_height()), 1)

        
def x_axis(surface : pygame.Surface, pos = (0, 0), vector = False):
    if vector:
        x = (pos[0], pos[0] + 200)
    else:
        x = (pos[0] - 200, pos[0])
    y = (pos[1], pos[1] + surface.get_height())
    result = None
    for i in entity_maps:
        if i.x >= x[0] and i.right() <= x[1]:
            if i.y <= y[0] and i.bottom() >= y[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.x < result.x:
                            result = i
                    else:
                        if i.right() > result.right():
                            result = i

            if i.bottom() >= y[0] and i.bottom() <= y[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.x < result.x:
                            result = i
                    else:
                        if i.right() > result.right():
                            result = i

            if i.y >= y[0] and i.y <= y[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.x < result.x:
                            result = i
                    else:
                        if i.right() > result.right():
                            result = i

    return result

def y_axis(surface : pygame.Surface, pos = (0, 0), vector = False):
    x = (pos[0], pos[0] + surface.get_width())
    if vector:
        y = (pos[1], pos[1] + 200)
    else:
        y = (pos[1] - 200, pos[1])
    result = None
    for i in entity_maps:
        if i.y >= y[0] and i.bottom() <= y[1]:
            if i.x <= x[0] and i.right() >= x[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.y < result.y:
                            result = i
                    else:
                        if i.bottom() > result.bottom():
                            result = i

            if i.right() >= x[0] and i.right() <= x[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.y < result.y:
                            result = i
                    else:
                        if i.bottom() > result.bottom():
                            result = i

            if i.x >= x[0] and i.x <= x[1]:
                if result == None:
                    result = i
                else:
                    if vector:
                        if i.y < result.y:
                            result = i
                    else:
                        if i.bottom() > result.bottom():
                            result = i

    return result

def center(surface : pygame.Surface, mouse = (0, 0)):
    for i in entity_maps:
        if mouse[0] >= i.x and mouse[0] + surface.get_width() <= i.right():
            if mouse[1] >= i.y and mouse[1] + surface.get_height() <= i.bottom():
                return (int(i.x + ((i.width() - surface.get_width()) / 2)), int(i.y + ((i.height() - surface.get_height()) / 2)))
    return None

def tool(type_tool, surface : pygame.Surface, mouse = (0, 0)):
    global data, vector_tool

    map_left = x_axis(surface, mouse, False) 
    map_right = x_axis(surface, mouse, True)
    map_top = y_axis(surface, mouse, False)
    map_bottom = y_axis(surface, mouse, True)
    size = surface.get_size()
    if type_tool[0] == -1:
        if type_tool[1] == -1:
            # left and top
            if vector_tool:
                if map_top != None:
                    return map_top.rect().bottomleft
                else:
                    if map_left != None:
                        return map_left.rect().topright
            else:
                if map_left != None:
                    return map_left.rect().topright
                else:
                    if map_top != None:
                        return map_top.rect().bottomleft
        if type_tool[1] == 1:
            # left and bottom
            if vector_tool:
                if map_bottom != None:
                    return (map_bottom.rect().topleft[0], map_bottom.rect().topleft[1] - surface.get_height())
                else:
                    if map_left != None:
                        return (map_left.rect().bottomright[0], map_left.rect().bottomright[1] - surface.get_height())
            else:
                if map_left != None:
                    return (map_left.rect().bottomright[0], map_left.rect().bottomright[1] - surface.get_height())
                else:
                    if map_bottom != None:
                        return (map_bottom.rect().topleft[0], map_bottom.rect().topleft[1] - surface.get_height())
        if type_tool[1] == 0:
            # center top - bottom and left
            if map_left != None:
                return (map_left.rect().right, int(map_left.rect().top + ((map_left.rect().height - surface.get_height()) / 2) + surface.get_height() / 2))
        if type_tool[1] == -2:
            # only left
            if map_left != None:
                return (map_left.right(), mouse[1])
    if type_tool[0] == 1:
        if type_tool[1] == -1:
            # right and top
            if vector_tool:
                if map_top != None:
                    return (map_top.rect().bottomright[0] - surface.get_width(), map_top.rect().bottomright[1])
                else:
                    if map_right != None:
                        return (map_right.rect().topleft[0] - surface.get_width(), map_right.rect().topleft[1])
            else:
                if map_right != None:
                    return (map_right.rect().topleft[0] - surface.get_width(), map_right.rect().topleft[1])
                else:
                    if map_top != None:
                        return(map_top.rect().bottomright[0] - surface.get_width(), map_top.rect().bottomright[1])
        if type_tool[1] == 1:
            # right and bottom
            if vector_tool:
                if map_bottom != None:
                    return (map_bottom.rect().topright[0] - surface.get_width(), map_bottom.rect().topright[1] - surface.get_height())
                else:
                    if map_right != None:
                        return (map_right.rect().bottomleft[0] - surface.get_width(), map_right.rect().bottomleft[1] - surface.get_height())
            else:
                if map_right != None:
                    return (map_right.rect().bottomleft[0] - surface.get_width(), map_right.rect().bottomleft[1] - surface.get_height())
                else:
                    if map_bottom != None:
                        return (map_bottom.rect().topright[0] - surface.get_width(), map_bottom.rect().topright[1] - surface.get_height())
        if type_tool[1] == 0:
            # center top - bottom and right
            if map_right != None:
                return (map_right.rect().left - surface.get_width(), int(map_right.rect().top + ((map_right.rect().height - surface.get_height()) / 2) + surface.get_height() / 2))
        if type_tool[1] == -2:
            # only right
            if map_right != None:
                return (map_right.x - surface.get_width(), mouse[1])
    if type_tool[0] == -2:
        if type_tool[1] == -1:
            # only top
            if map_top != None:
                return (mouse[0], map_top.bottom())
        if type_tool[1] == 1:
            # only bottom
            if map_bottom != None:
                return (mouse[0], map_bottom.y - surface.get_height())
        if type_tool[1] == 0:
            # center top - bottom
            pass
        if type_tool[1] == -2:
            # free
            pass
    if type_tool[0] == 0:       
        if type_tool[1] == -1:
            # center left - right and top
            if map_top != None:
                return (int(map_top.rect().left + ((map_top.rect().width - surface.get_width()) / 2)), map_top.rect().bottom)
        if type_tool[1] == 1:
            # center left - right and bottom
            if map_bottom != None:
                return (int(map_bottom.rect().left + ((map_bottom.rect().width - surface.get_width()) / 2)), map_bottom.rect().top - surface.get_height())
        if type_tool[1] == 0:
            # center 
            return center(surface, mouse)
            pass
        if type_tool[1] == -2:
            # center left - right
            pass

    return None
        

while True:
    pos_rect_mini = None
    if status_button["Left"]:
        if status_button["Right"]:
            pos_rect_mini = (854, 33)
            tool_ponit_map[0] = 0
        else:
            pos_rect_mini = (831, 33)
            tool_ponit_map[0] = -1
    else:
        if status_button["Right"]:
            pos_rect_mini = (881, 33)
            tool_ponit_map[0] = 1
        else:
            tool_ponit_map[0] = -2
    
    if status_button["Top"]:
        if pos_rect_mini == None:
            pos_rect_mini = (835, 19)
        if status_button["Bottom"]:
            pos_rect_mini = (pos_rect_mini[0], 39)
            tool_ponit_map[1] = 0
        else:
            pos_rect_mini = (pos_rect_mini[0], 31)
            tool_ponit_map[1] = -1
    else:
        if status_button["Bottom"]:
            if pos_rect_mini == None:
                pos_rect_mini = (835, 19)
            pos_rect_mini = (pos_rect_mini[0], 51)
            tool_ponit_map[1] = 1
        else:
            tool_ponit_map[1] = -2

    if status_button["center"]:
        tool_ponit_map[0] = 0
        tool_ponit_map[1] = 0
        pos_rect_mini = (854, 39)


    if action["up"]:
        offset = (offset[0], offset[1] + speed_offset)
    if action["down"]:
        offset = (offset[0], offset[1] - speed_offset)
    if action["left"]:
        offset = (offset[0] + speed_offset, offset[1])
    if action["right"]:
        offset = (offset[0] - speed_offset, offset[1])


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

    mousedown = pygame.mouse.get_pos()

    mouse = mousedown

    mousedown = (mousedown[0] - offset[0], mousedown[1] - offset[1])

    pos = (int(mousedown[0] - offset_screen[0]), int(mousedown[1] - offset_screen[1]))
    pos_tool = tool(tool_ponit_map, image_real, pos)
    if pos_tool is not None:
        pos_tool_show = (int(pos_tool[0] + offset[0]), int(pos_tool[1] + offset[1]))
    else:
        pos_tool = pos
        pos_tool_show = (int(mouse[0] - offset_screen[0]), int(mouse[1] - offset_screen[1]))

    if update_map:
        entity_maps = []
        for key, value in data.items():
            x, y = map(int, key.split(":"))
            entity_maps.append(MiniMap(data_maps[value["name"]], value["name"], value["type"], value["flip"], x, y, False))
            # x, y = x + offset[0], y + offset[1]  
            # display.blit(data_maps[value["name"]], (x, y))
        update_map = False

    if alt_c:
        if pos_begin_select != None:
            begin = (0, 0)
            if pos_begin_select[0] < mouse[0]:
                begin = (pos_begin_select[0], begin[1])
            else:
                begin = (mouse[0], begin[1])
            
            if pos_begin_select[1] < mouse[1]:
                begin = (begin[0], pos_begin_select[1])
            else:
                begin = (begin[0], mouse[1])

            end = (0, 0)
            if pos_begin_select[0] > mouse[0]:
                end = (pos_begin_select[0], end[1])
            else:
                end = (mouse[0], end[1])
            
            if pos_begin_select[1] > mouse[1]:
                end = (end[0], pos_begin_select[1])
            else:
                end = (end[0], mouse[1])
            size = ((end[0] - begin[0]), (end[1] - begin[1]))


            for i in entity_maps:
                if i.x + offset[0] >= begin[0] - SIZE_SHOW[0] and i.x + offset[0] <= end[0] - SIZE_SHOW[0]:
                    if i.y + offset[1] >= begin[1] - SIZE_SHOW[1] and i.y + offset[1] <= end[1] - SIZE_SHOW[1]:
                        i.select = True

                    if i.bottom() + offset[1] >= begin[1] - SIZE_SHOW[1] and i.bottom() + offset[1] <= end[1] - SIZE_SHOW[1]:
                        i.select = True

                if i.right() + offset[0] >= begin[0] - SIZE_SHOW[0] and i.right() + offset[0] <= end[0] - SIZE_SHOW[0]:
                    if i.y + offset[1] >= begin[1] - SIZE_SHOW[1] and i.y + offset[1] <= end[1] - SIZE_SHOW[1]:
                        i.select = True

                    if i.bottom() + offset[1] >= begin[1] - SIZE_SHOW[1] and i.bottom() + offset[1] <= end[1] - SIZE_SHOW[1]:
                        i.select = True
                if begin_select:
                    if begin[0] - SIZE_SHOW[0] >= i.x + offset[0] and end[0] - SIZE_SHOW[0] <= i.right() + offset[0]:
                        if begin[1] - SIZE_SHOW[1] >= i.y + offset[1] and end[1] - SIZE_SHOW[1] <= i.bottom() + offset[1]:
                            i.select = not i.select
                            begin_select = False
                
        for i in entity_maps:
            if key_select != None:
                if i.x == key_select[0] and i.y == key_select[1]:
                    i.select = True
                    key_select = None
                
   

    if pos_rect_mini != None:
        screen.blit(rect_mini, pos_rect_mini)
    
    list_select = []
    for i in entity_maps:
        i.render(display, offset)
        if i.select:
            list_select.append(i)

    if len(list_select) == 1:
        minimap_select = list_select[0]
    else:
        minimap_select = None

    if alt_c:
        if pos_begin_select != None:
            pygame.draw.rect(display, (255, 0, 0), (begin[0] - SIZE_SHOW[0], begin[1] - SIZE_SHOW[1], size[0], size[1]), 1)
    else:
        pygame.draw.rect(display, (25, 125, 0), (pos_tool_show[0], pos_tool_show[1], image_real.get_width(), image_real.get_height()))

    for index, (key, value) in enumerate(data_images_x.items()):
        i = int(index / 2)
        r = index % 2
        pos_x = SIZE_SHOW[0] * 2 + i * int(SIZE_SHOW[0] / 2)
        pos_y = int(SIZE_SHOW[1] / 2) * r
        size_image = (int(SIZE_SHOW[0] / 2), int(SIZE_SHOW[1] / 2))
        if key == name_key_maps[index_name_data_map]:
            render(screen, value, size_image, (pos_x, pos_y), True)
        else:
            render(screen, value, size_image, (pos_x, pos_y), False)

    print(name_key_maps[index_name_data_map])

    for index, (key, value) in enumerate(data_images_y.items()):
        i = int(index / 2)
        r = index % 2
        pos_x = int(SIZE_SHOW[0] / 2) * r
        pos_y = SIZE_SHOW[1] + i * int(SIZE_SHOW[1] / 2)
        size_image = (int(SIZE_SHOW[0] / 2), int(SIZE_SHOW[1] / 2))
        if key == list_name_maps_in_data_convert[index_entity_data_map]:
            render(screen, value, size_image, (pos_x, pos_y), True)
        else:
            render(screen, value, size_image, (pos_x, pos_y), False)


    for i in buttons:
        i.render(screen)

    type_map = 1
    for i in range(3):
        if buttons[i + 6].type:
            type_map = i + 1
        
    if len(list_select) > 0:
        type_map = int(list_select[0].e_type)
        for i in list_select:
            if int(i.e_type) != type_map:
                type_map = -1
                break

        for i in range(3):
            buttons[6 + i].type = False
        if type_map != -1:
            buttons[6 + type_map - 1].on_off()

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
                    update_map = True

            if keys[pygame.K_LCTRL] and keys[pygame.K_c]:
                status_button["center"] = not status_button["center"]
                buttons[5].on_off()

            if keys[pygame.K_LCTRL] and keys[pygame.K_1]:
                status_button["Left"] = not status_button["Left"]
                buttons[0].on_off()

            if keys[pygame.K_LCTRL] and keys[pygame.K_2]:
                status_button["Right"] = not status_button["Right"]
                buttons[1].on_off()

            if keys[pygame.K_LCTRL] and keys[pygame.K_3]:
                status_button["Top"] = not status_button["Top"]
                buttons[2].on_off()

            if keys[pygame.K_LCTRL] and keys[pygame.K_4]:
                status_button["Bottom"] = not status_button["Bottom"]
                buttons[3].on_off()

            if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
                status_button["xy"] = not status_button["xy"]
                buttons[4].on_off()
                if status_button["xy"]:
                    buttons[4].set_name("Y-axis")
                    vector_tool = True
                else:
                    buttons[4].set_name("X-axis")
                    vector_tool = False

            if keys[pygame.K_LALT] or keys[pygame.K_RALT]:
                if keys[pygame.K_c]:
                    alt_c = not alt_c
                    update_map = True
                
                if keys[pygame.K_d] and alt_c:
                    old_data.append(data.copy())
                    if len(old_data) > 30:
                        old_data.pop(0)
                    for i in entity_maps:
                        if i.select:
                            data.pop(str(i.x) + ":" + str(i.y))
                    update_map = True

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if keys[pygame.K_a] and alt_c:
                    for i in entity_maps:
                        i.select = True

            if keys[pygame.K_l]:
                update_map = True
                alt_c = not alt_c
            
            if minimap_select != None:

                if keys[pygame.K_w] and alt_c:
                    old_data.append(data.copy())
                    key = str(minimap_select.x) + ":" + str(minimap_select.y)
                    key_new = str(minimap_select.x) + ":" + str(minimap_select.y - 1)
                    key_select = (minimap_select.x, minimap_select.y - 1)
                    data.pop(key)
                    values = {
                                "name" : minimap_select.name,
                                "type" : minimap_select.e_type,
                                "flip" : minimap_select.flip
                            }
                    data[key_new] = values
                    update_map = True
                
                if keys[pygame.K_s] and alt_c:
                    old_data.append(data.copy())
                    key = str(minimap_select.x) + ":" + str(minimap_select.y)
                    key_new = str(minimap_select.x) + ":" + str(minimap_select.y + 1)
                    key_select = (minimap_select.x, minimap_select.y + 1)
                    data.pop(key)
                    values = {
                                "name" : minimap_select.name,
                                "type" : minimap_select.e_type,
                                "flip" : minimap_select.flip
                            }
                    data[key_new] = values
                    update_map = True
                
                if keys[pygame.K_a] and alt_c:
                    old_data.append(data.copy())
                    key = str(minimap_select.x) + ":" + str(minimap_select.y)
                    key_new = str(minimap_select.x - 1) + ":" + str(minimap_select.y)
                    key_select = (minimap_select.x - 1, minimap_select.y)
                    data.pop(key)
                    values = {
                                "name" : minimap_select.name,
                                "type" : minimap_select.e_type,
                                "flip" : minimap_select.flip
                            }
                    data[key_new] = values
                    update_map = True
                
                if keys[pygame.K_d] and alt_c and not keys[pygame.K_LALT] and not keys[pygame.K_RALT]:
                    old_data.append(data.copy())
                    key = str(minimap_select.x) + ":" + str(minimap_select.y)
                    key_new = str(minimap_select.x + 1) + ":" + str(minimap_select.y)
                    key_select = (minimap_select.x + 1, minimap_select.y)
                    data.pop(key)
                    values = {
                                "name" : minimap_select.name,
                                "type" : minimap_select.e_type,
                                "flip" : minimap_select.flip
                            }
                    data[key_new] = values
                    update_map = True



        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in buttons:
                if i.set_type(mouse, event.button):
                    status_button[i.name] = not status_button[i.name]
                    if i.name == "xy":
                        if status_button[i.name]:
                            i.set_name("Y-axis")
                            vector_tool = True
                        else:
                            i.set_name("X-axis")
                            vector_tool = False

                    if i.name.split('_')[0] == "type":
                        for t in range(3):
                            buttons[t+6].type = False
                        i.on_off()
                        if len(list_select) > 0:
                            print(i.name.split('_')[1])
                            old_data.append(data.copy())
                            if len(old_data) > 30:
                                old_data.pop(0)
                            for ir in entity_maps:
                                if ir.select:
                                    key = str(ir.x) + ":" + str(ir.y)
                                    data[key]["type"] = int(i.name.split('_')[1])
                            update_map = True
            
            if alt_c:
                if event.button == 1 and mouse[0] > SIZE_SHOW[0] and mouse[1] > SIZE_SHOW[1]:
                    pos_begin_select = mouse
                    begin_select = True
            else:
                pos_begin_select = None
                if event.button == 1 and mouse[0] > SIZE_SHOW[0] and mouse[1] > SIZE_SHOW[1]:
                    key = str(pos_tool[0]) + ":" + str(pos_tool[1])
                    value = {
                                "name" : list_name_maps_in_data_convert[index_entity_data_map],
                                "type" : type_map,
                                "flip" : False
                            }
                    old_data.append(data.copy())
                    if len(old_data) > 30:
                        old_data.pop(0)
                    data[key] = value
                    update_map = True
                if event.button == 4:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        index_entity_data_map = 0
                        index_name_data_map -= 1
                        if index_name_data_map < 0:
                            index_name_data_map = len(name_key_maps) - 1
                        list_name_maps_in_data_convert = list(data_maps_convert[name_key_maps[index_name_data_map]].keys())
                        data_images_y = {}
                        for i in data_maps_convert[name_key_maps[index_name_data_map]].keys():
                            data_images_y[i] = data_maps[i]
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
                        data_images_y = {}
                        for i in data_maps_convert[name_key_maps[index_name_data_map]].keys():
                            data_images_y[i] = data_maps[i]
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

        if event.type == pygame.MOUSEBUTTONUP:
            pos_begin_select = None

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

