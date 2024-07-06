import pygame, json
from models.game_entities.map import Map
from models.utils import Image

class Level:
    def __init__(self, level, image : Image):
        self.data_images = image.convert_action_maps()

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
        for dict_key, dict_value in self.data_json.items():
            for key, value in dict_value.items():
                if value["name"] != "player":
                    pos = list(map(int, key.split(":")))
                    entity_map = Map(value["name"], (pos[0], pos[1]), self.data_images[value["name"]], None, value["flip"], 0, 0, 5, int(value["type"]), int(value["z-index"]))
                    self.data_maps.append(entity_map)
                    if self.left_top == None:
                        self.left_top = (entity_map.pos[0], entity_map.pos[1])
                    elif self.left_top[0] > entity_map.pos[0]:
                        self.left_top = (entity_map.pos[0], self.left_top[1])
                    elif self.left_top[1] >  entity_map.pos[1]:
                        self.left_top = (self.left_top[0],  entity_map.pos[1])
                    if self.bottom_right == None:
                        self.bottom_right = (entity_map.pos[0],  entity_map.pos[1])
                    elif self.bottom_right[0] < entity_map.rect().right:
                        self.bottom_right = (entity_map.rect().right, self.bottom_right[1])
                    elif self.bottom_right[1] < entity_map.rect().bottom:
                        self.bottom_right = (self.bottom_right[0], entity_map.rect().bottom)

    def get_left_top(self):
        return self.left_top
    
    def get_bottom_right(self):
        return self.bottom_right

    def get_full_map(self):
        self.data_maps.sort(key = lambda item : item.z_index)
        return self.data_maps
    
    def draw(self, surface : pygame.Surface, offset = (0, 0)):
        for entity_map in self.data_maps: 
            surface.blit(pygame.transform.flip(entity_map.get_image(), entity_map.flip, False), (entity_map.get_pos()[0] + offset[0], entity_map.get_pos()[1] + offset[1]))

    def start_pos_player(self):
        if "player" in self.data_json:
            key = list(self.data_json["player"].keys())
            pos = key[0]
            x, y = map(int, pos.split(":"))
            result = (x, y)
        else:
            result = (0, 0)  # Default position if player not found in the map
        return result
  