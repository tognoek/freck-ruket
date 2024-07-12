import pygame, json
from models.game_entities.map import Map
from models.game_entities.trampoline import Trampoline
from models.game_entities.fire import Fire
from models.game_entities.fire_90 import Fire_90
from models.game_entities.spikes import Spikes
from models.game_entities.spikes_90 import Spikes_90
from models.utils import Data

class Level:
    def __init__(self, level, data : Data):
        self.data = data
        self.data_json = {}
        self.data_maps = []
        self.level = level
        self.left_top = (0, 0)
        self.bottom_right = (0, 0)
        self.data_entities = {}
        self.name_maps = ["block", "land", "blockgray", "metal", "line", "wall"]
        # self.name_traps = ""

    def create_data(self):
        self.image_trampoline = self.data.load_image_trap("Trampoline")[0]
        self.image_fire = self.data.load_image_trap("Fire")[0]
        self.image_fire_90 = self.data.load_image_trap("Fire", 90)[0]
        self.image_spikes = self.data.load_image_trap("Spikes")[0]
        self.image_spikes_90 = self.data.load_image_trap("Spikes", 90)[0]
        self.image_maps = self.data.convert_action_maps()

    def load_map(self, level = 1):
        self.level = level
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        self.data_json = data

    def convert(self):
        self.bottom_right = None
        self.left_top = None
        for dict_key, dict_value in self.data_json.items():
            for key, value in dict_value.items():
                if value["name"] != "player":
                    keys = value["name"].split("_")
                    pos = list(map(int, key.split(":")))
                    if keys[0] == "traps":
                        if keys[1] == "trampoline":
                            entity_map = Trampoline(value["name"], (pos[0], pos[1]), 
                                            self.image_trampoline, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Trampoline"))
                        if keys[1] == "fire":
                            if len(keys) > 2:
                                entity_map = Fire_90(value["name"], (pos[0], pos[1]), 
                                            self.image_fire_90, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Fire-90"))
                            else:
                                entity_map = Fire(value["name"], (pos[0], pos[1]), 
                                            self.image_fire, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Fire"))
                        if keys[1] == "spikes":
                            if len(keys) > 2:
                                entity_map = Spikes_90(value["name"], (pos[0], pos[1]), 
                                                self.image_spikes_90, None, value["flip"], 
                                                0, 0, 5, int(value["type"]), int(value["z-index"]),
                                                self.data.load_data_traps("Spikes-90"))
                            else:
                                entity_map = Spikes(value["name"], (pos[0], pos[1]), 
                                                self.image_spikes, None, value["flip"], 
                                                0, 0, 5, int(value["type"]), int(value["z-index"]),
                                                self.data.load_data_traps("Spikes"))
                            
                    else:
                        entity_map = Map(value["name"], (pos[0], pos[1]), 
                                            self.image_maps[value["name"]], None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]))
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

    def filter_type(self):
        self.traps = []
        self.maps = []
        for i in self.data_maps:
            if i.name.split("_")[0] == "traps":
                self.traps.append(i)
            else:
                self.maps.append(i)

    def get_traps(self):
        return self.traps
    
    def get_maps(self):
        return self.maps

    def get_left_top(self):
        return self.left_top
    
    def get_bottom_right(self):
        return self.bottom_right

    def sort_by_type(self):
        self.data_maps.sort(key = lambda item : item.z_index)
        # return self.data_maps
    
    def draw(self, surface : pygame.Surface, offset = (0, 0)):
        for entity_map in self.data_maps: 
            entity_map.update()
            surface.blit(pygame.transform.flip(entity_map.get_image(), entity_map.flip[0], entity_map.flip[1]), (entity_map.get_pos()[0] + offset[0], entity_map.get_pos()[1] + offset[1]))

    def start_pos_player(self):
        if "player" in self.data_json:
            key = list(self.data_json["player"].keys())
            pos = key[0]
            x, y = map(int, pos.split(":"))
            result = (x, y)
        else:
            result = (0, 0)  # Default position if player not found in the map
        return result
  