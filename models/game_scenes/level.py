import pygame, json
from models.game_entities.traps.map import Map
from models.game_entities.traps.trampoline import Trampoline
from models.game_entities.traps.fire import Fire
from models.game_entities.traps.fire_90 import Fire_90
from models.game_entities.traps.spikes import Spikes
from models.game_entities.traps.spikes_90 import Spikes_90
from models.game_entities.traps.fan import Fan
from models.game_entities.traps.saw import Saw
from models.game_entities.traps.spiked_ball import SpikedBall
from models.game_entities.traps.falling_platforms import FallingPlatforms
from models.game_entities.traps.rock_head import RockHead
from models.game_entities.traps.spike_head import SpikeHead
from models.game_entities.traps.arrow import Arrow
from models.game_entities.traps.blocks import Blocks
from models.game_entities.items.fruits import Fruits
from models.game_entities.items.box1 import Box1
from models.game_entities.items.box2 import Box2
from models.game_entities.items.box3 import Box3
from models.game_entities.items.checkpoint import CheckPoint
from models.utils import Data
import math

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
        self.is_create = False
        self.fps = 60
        self.sum_point = 0
        self.next_level = False
        # self.name_traps = ""

    def create_data(self):
        if self.is_create:
            return
        self.is_create = True
        self.image_trampoline = self.data.load_image_traps("Trampoline")[0]
        self.image_fire = self.data.load_image_traps("Fire")[0]
        self.image_fire_90 = self.data.load_image_traps("Fire", 90)[0]
        self.image_spikes = self.data.load_image_traps("Spikes")[0]
        self.image_spikes_90 = self.data.load_image_traps("Spikes", 90)[0]
        self.image_fan = self.data.load_image_traps("Fan")[0]
        self.image_saw = self.data.load_image_traps("Saw")[0]
        self.image_spiked_ball = self.data.load_image_traps("Spiked Ball")[0]
        self.image_falling_platforms = self.data.load_image_traps("Falling Platforms")[0]
        self.image_rock_head = self.data.load_image_traps("Rock Head")[0]
        self.image_spike_head = self.data.load_image_traps("Spike Head")[0]
        self.image_arrow = self.data.load_image_traps("Arrow")[0]
        self.image_blocks = self.data.load_image_traps("Blocks")[0]
        self.image_fruits = self.data.load_image_items("Fruits")[0]
        self.image_box1 = self.data.load_image_items("Box1")[0]
        self.image_box2 = self.data.load_image_items("Box2")[0]
        self.image_box3 = self.data.load_image_items("Box3")[0]
        self.image_checkpoint = self.data.load_image_items("Check Point")[0]
        self.image_maps = self.data.convert_action_maps()

    def load_map(self, level = 1):
        self.level = level
        with open(f"data/Json/Level/level_{self.level}.json") as file:
            data = json.load(file)
        self.data_json = data
        self.data_maps = []

    def convert(self):
        self.bottom_right = None
        self.left_top = None
        saw = []
        spiked_ball = []
        for dict_key, dict_value in self.data_json.items():
            for key, value in dict_value.items():
                if value["name"] != "player":
                    keys = value["name"].split("_")
                    pos = list(map(int, key.split(":")))
                    entity_map = None
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
                        if keys[1] == "fan":
                            entity_map = Fan(value["name"], (pos[0], pos[1]), 
                                            self.image_fan, None, value["flip"], 
                                            0, 0, 3, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Fan"))
                            
                        if keys[1] == "fallingplatforms":
                            entity_map = FallingPlatforms(value["name"], (pos[0], pos[1]), 
                                            self.image_falling_platforms, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Falling Platforms"))
                            
                        if keys[1] == "rockhead":
                            vector = list(map(int, value["values"]))
                            entity_map = RockHead(value["name"], (pos[0], pos[1]), 
                                            self.image_rock_head, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Rock Head"), vector)
                        if keys[1] == "spikehead":
                            vector = list(map(int, value["values"]))
                            entity_map = SpikeHead(value["name"], (pos[0], pos[1]), 
                                            self.image_spike_head, None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Spike Head"), vector)
                        if keys[1] == "arrow":
                            entity_map = Arrow(value["name"], (pos[0], pos[1]), 
                                            self.image_arrow, None, value["flip"], 
                                            0, 0, 7, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Arrow"))
                            
                        if keys[1] == "blocks":
                            entity_map = Blocks(value["name"], (pos[0], pos[1]), 
                                            self.image_blocks, None, value["flip"], 
                                            0, 0, 3, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_traps("Blocks"))

                        if keys[1] == "saw":
                            temp = []
                            sub_temp = []
                            for i in value["values"]:
                                if len(i) > 0:
                                    sub_temp.append(int(i))
                            temp.append(sub_temp)
                            temp.append(pos)
                            temp.append(value["flip"])
                            temp.append(value["type"])
                            temp.append(value["z-index"])
                            saw.append(temp)
                        
                        if keys[1] == "spikedball":
                            temp = []
                            sub_temp = []
                            for i in value["values"]:
                                if len(i) > 0:
                                    sub_temp.append(int(i))
                            temp.append(sub_temp)
                            temp.append(pos)
                            temp.append(value["flip"])
                            temp.append(value["type"])
                            temp.append(value["z-index"])
                            spiked_ball.append(temp)

                    elif keys[0] == "items":
                            if keys[1] in ["apple", "bananas", "cherries", "kiwi", "melon", "orange", "pineapple", "strawberry"]:
                                entity_map = Fruits(value["name"], (pos[0], pos[1]), 
                                            self.image_fruits, None, value["flip"], 
                                            0, 0, 2, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_items("Fruits"))
                            if keys[1] == "box1":
                                entity_map = Box1(value["name"], (pos[0], pos[1]), 
                                            self.image_box1, None, value["flip"], 
                                            0, 0, 2, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_items("Box1"), self.image_fruits)
                            if keys[1] == "box2":
                                entity_map = Box2(value["name"], (pos[0], pos[1]), 
                                            self.image_box2, None, value["flip"], 
                                            0, 0, 2, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_items("Box2"), self.image_fruits)
                            if keys[1] == "box3":
                                entity_map = Box3(value["name"], (pos[0], pos[1]), 
                                            self.image_box3, None, value["flip"], 
                                            0, 0, 2, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_items("Box3"), self.image_fruits)
                                
                            if keys[1] == "checkpoint":
                                entity_map = CheckPoint(value["name"], (pos[0], pos[1]), 
                                            self.image_checkpoint, None, value["flip"], 
                                            0, 0, 2, int(value["type"]), int(value["z-index"]),
                                            self.data.load_data_items("Check Point"))
                            
                    else:
                        entity_map = Map(value["name"], (pos[0], pos[1]), 
                                            self.image_maps[value["name"]], None, value["flip"], 
                                            0, 0, 5, int(value["type"]), int(value["z-index"]))
                    if entity_map != None:
                        self.data_maps.append(entity_map)

                        if self.left_top == None:
                            self.left_top = (entity_map.pos[0], entity_map.pos[1])
                        if self.left_top[0] > entity_map.pos[0]:
                            self.left_top = (entity_map.pos[0], self.left_top[1])
                        if self.left_top[1] >  entity_map.pos[1]:
                            self.left_top = (self.left_top[0],  entity_map.pos[1])
                        if self.bottom_right == None:
                            self.bottom_right = (entity_map.pos[0],  entity_map.pos[1])
                        if self.bottom_right[0] < entity_map.rect().right:
                            self.bottom_right = (entity_map.rect().right, self.bottom_right[1])
                        if self.bottom_right[1] < entity_map.rect().bottom:
                            self.bottom_right = (self.bottom_right[0], entity_map.rect().bottom)

        # Tạo dữ liệu cho saw
        if len(saw) > 0:
            saw = sorted(saw, key =lambda x: (x[0][0], x[0][1]))
            saw.append([[saw[-1][0][0] + 1, 1]])
            temp = [saw[0]]
            for i in range(1, len(saw)):
                if saw[i][0][0] == temp[-1][0][0]:
                    temp.append(saw[i][:2])
                else:
                    entity = Saw("traps_saw", (0, 0), self.image_saw, None, 
                                saw[i-1][2], 0, 0, 5, saw[i-1][3], saw[i-1][4], temp)
                    entity.create()
                    self.data_maps.append(entity)
                    temp = [saw[i]]

        # Taooj dữ liệu cho Spiked Ball
        if len(spiked_ball) > 0:
            spiked_ball = sorted(spiked_ball, key =lambda x: (x[0][0], x[0][1]))
            spiked_ball.append([[spiked_ball[-1][0][0] + 1, 1]])
            temp = [spiked_ball[0]]
            for i in range(1, len(spiked_ball)):
                if spiked_ball[i][0][0] == temp[-1][0][0]:
                    temp.append(spiked_ball[i][:2])
                else:
                    entity = SpikedBall("traps_spikedball", (0, 0), self.image_spiked_ball, None, 
                                spiked_ball[i-1][2], 0, 0, 5, spiked_ball[i-1][3], spiked_ball[i-1][4], temp)
                    entity.create()
                    self.data_maps.append(entity)
                    temp = [spiked_ball[i]]


    def filter_type(self):
        self.traps = []
        self.maps = []
        for i in self.data_maps:
            if i.name.split("_")[0] in ["traps", "items"]:
                self.traps.append(i)
            else:
                self.maps.append(i)

    def update_fps(self, fps=60):
        self.fps = fps

    def get_traps(self, pos = None):
        if pos != None:
            res = []
            for i in self.traps:
                x = i.get_pos()[0] - pos[0]
                y = i.get_pos()[1] - pos[1]
                if math.hypot(x, y) < 240:
                    res.append(i)
            return res
        return self.traps
    
    def get_maps_traps(self, pos = None):
        if pos!= None:
            res = []
            for i in self.data_maps:
                x = i.get_pos()[0] - pos[0]
                y = i.get_pos()[1] - pos[1]
                if math.hypot(x, y) < 240:
                    res.append(i)
            return res
        return self.data_maps

    def get_maps(self, pos = None):
        if pos != None:
            res = []
            for i in self.maps:
                x = i.get_pos()[0] - pos[0]
                y = i.get_pos()[1] - pos[1]
                if math.hypot(x, y) < 240:
                    res.append(i)
            return res
        return self.maps

    def get_left_top(self):
        return self.left_top
    
    def get_bottom_right(self):
        return self.bottom_right

    def sort_by_type(self):
        self.data_maps.sort(key = lambda item : item.z_index)
        # return self.data_maps
    
    def update(self, pos_player = None, max_len = 500):
        for entity_map in self.data_maps:
            if entity_map.show(pos_player, max_len):
                if not entity_map.is_die():
                    if entity_map.name in ["traps_rockhead", "traps_spikehead"]:
                        entity_map.update(self.get_maps(entity_map.get_pos()))
                    else:
                        entity_map.update()

    def render(self, surface : pygame.Surface, offset = (0, 0), pos_player = None, max_len = 500, pause = False):
        for entity_map in self.data_maps:
            if entity_map.show(pos_player, max_len):
                if not entity_map.is_die():
                    if entity_map.name == "items_checkpoint":
                        self.next_level = entity_map.next_level
                    entity_map.render(surface, offset, pause)
    def start_pos_player(self):
        if "player" in self.data_json:
            key = list(self.data_json["player"].keys())
            pos = key[0]
            x, y = map(int, pos.split(":"))
            result = (x, y)
        else:
            result = (0, 0)  # Default position if player not found in the map
        return result
    
    def update_sumpoint(self):
        self.sum_point = 0
        for entity in self.data_maps:
            if entity.name in ["items_apple", "items_bananas", "items_kiwi", "items_cherries", 
                                          "items_pineapple", "items_melon", "items_strawberry", "items_orange"]:
                self.sum_point += 1

            if entity.name == "items_box1":
                self.sum_point += 4
            if entity.name == "items_box2":
                self.sum_point += 6
            if entity.name == "items_box3":
                self.sum_point += 8
  
    def run(self, level = 1):
        self.next_level = False
        self.load_map(level)
        self.create_data()
        self.convert()
        self.update_sumpoint()
        self.sort_by_type()
        self.filter_type()