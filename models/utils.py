import pygame # type: ignore
import json
import os
from ENV import PATH_CHARCTERS, PATH_MAPS, PATH_BACKGROUND, PATH_TRAPS, PATH_ITEMS, PATH_IMAGES_LEVELS, PATH_IMAGES_BUTTONS
MAXLEVEL = 50
class Save:
    def __init__(self):
        self.path_locks = "data/Json/Level/lock_levels.json"
        self.path_start = "data/Json/Level/start.json"
    def save_lock(self, key):
        if key > MAXLEVEL:
            key = MAXLEVEL
        key = str(f"{key:02}")
        with open(self.path_locks) as file:
            data = json.load(file)
        data[key] = False
        with open(self.path_locks, "w") as file:
            json.dump(data, file, indent=2)

    def get_start(self):
        with open(self.path_start) as file:
            data = json.load(file)
        return int(data["level"])
    def get_character(self):
        with open(self.path_start) as file:
            data = json.load(file)
        return data["character"]
    def get_life(self):
        with open(self.path_start) as file:
            data = json.load(file)
        return int(data["life"])
    
    def save_life(self, life):
        with open(self.path_start, "r") as file:
            data = json.load(file)
        data["life"] = life
        with open(self.path_start, "w") as file:
            json.dump(data, file, indent=2)

    def reset(self):
        data = {}
        data["01"] = False
        for i in range(2, 51):
            name = str(f"{i:02}")
            data[name] = True
        with open(self.path_locks, "w") as file:
            json.dump(data, file, indent=4)

        with open(self.path_start, "w") as file:
            data = {}
            data["level"] = 1
            data["character"] = "Pink Man"
            data["life"] = 5
            json.dump(data, file, indent=2)

    def update_character(self, key):
        with open(self.path_start, "r") as file:
            data = json.load(file)
        data["character"] = key
        with open(self.path_start, "w") as file:
            json.dump(data, file, indent=2)
    
    def update_start(self, key):
        with open(self.path_start, "r") as file:
            data = json.load(file)
        key_old = int(data["level"])
        if key > MAXLEVEL:
            key = MAXLEVEL
        if key_old < key:
            data["level"] = key
            with open(self.path_start, "w") as file:
                json.dump(data, file, indent=2)

class Data:

    def __init__(self):
        with open("data/Json/images.json") as file:
            self.file_json = json.load(file)
        with open("data/Json/data_entities.json", "r") as file:
            self.data_error = json.load(file)
        
    
    def load(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        image.set_colorkey((0, 0, 0)) 
        return image
    
    def cut_image(self, path, frame, size=(32, 32), rotate = 0):
        image = pygame.image.load(path)
        res = []
        for i in range(frame):
            temp = pygame.Surface(size)
            temp.blit(image, (0, 0), (i * size[0], 0, size[0], size[1]))
            temp.set_colorkey((0, 0, 0))
            if rotate != 0:
                temp = pygame.transform.rotate(temp, rotate)
            res.append(temp.convert_alpha())
        return res
    def load_images_main_character(self, name):
        data = self.file_json["Images"]["Main Characters"][name]
        images = {}
        frames = {}
        for attribute, values in data.items():
            path = PATH_CHARCTERS + "/" + name + "/" + attribute + " (" + values["Size"] + ").png"
            x, y = map(int , values["Size"].split("x"))
            images[attribute] = self.cut_image(path, int(values["Frame"]), (x, y))
            frames[attribute] = int(values["Frame"])
            # print(x, y)

        return images, frames
    
    def load_mouse(self):
        return pygame.image.load("data/Images/Menu/Mouse/mouse.png")

    def load_image_traps(self, name, rotate = 0):
        data = self.file_json["Images"]["Traps"][name]
        images = {}
        frames = {}
        for attribute, values in data.items():
            path = PATH_TRAPS + "/" + name + "/" + attribute + " (" + values["Size"] + ").png"
            x, y = map(int , values["Size"].split("x"))
            images[attribute] = self.cut_image(path, int(values["Frame"]), (x, y), rotate)
            frames[attribute] = int(values["Frame"])
        
        return images, frames
    
    def load_image_items(self, name, rotate = 0):
        data = self.file_json["Images"]["Items"][name]
        images = {}
        frames = {}
        for attribute, values in data.items():
            path = PATH_ITEMS + "/" + name + "/" + attribute + " (" + values["Size"] + ").png"
            x, y = map(int , values["Size"].split("x"))
            images[attribute] = self.cut_image(path, int(values["Frame"]), (x, y), rotate)
            frames[attribute] = int(values["Frame"])
        
        return images, frames
    
    def load_data_charactre(self, name):
        return self.data_error["Points Collision"]["Main Characters"][name] 
    def load_data_traps(self, name):
        return self.data_error["Points Collision"]["Traps"][name] 
    def load_data_items(self, name):
        return self.data_error["Points Collision"]["Items"][name] 

    def load_data_maps(self):
        images = {}
        for filename in os.listdir(PATH_MAPS):
            file_path = os.path.join(PATH_MAPS, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):

                image = pygame.image.load(file_path)
                key = os.path.splitext(filename)[0]
                images[key] = image
        
        return images
    def load_data_images_level(self):
        images = {}
        for filename in os.listdir(PATH_IMAGES_LEVELS):
            file_path = os.path.join(PATH_IMAGES_LEVELS, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):

                image = pygame.image.load(file_path)
                key = os.path.splitext(filename)[0]
                images[key] = image
        
        return images

    def convert_action_maps(self):
        data = self.load_data_maps()
        names = list(data.keys())
        result = {}
        for i in names:
            result[i] = {"Idle" : [data[i]]}
        return result

    def load_background(self):
        images = {}
        for filename in os.listdir(PATH_BACKGROUND):
            file_path = os.path.join(PATH_BACKGROUND, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):

                image = pygame.image.load(file_path)
                key = os.path.splitext(filename)[0]
                images[key] = image
        
        return images
    
    def load_data_lock_levels(self):
        with open("data/Json/Level/lock_levels.json") as f:
            data = json.load(f)
        return data
    
class Text:
    def __init__(self):
        self.name = ["a", "b", "c", "d", "e", "f", "g",
                      "h", "i", "j", "k", "l", "m", "n",
                        "o", "p", "q", "r", "s", "t", "u",
                          "v", "w", "x", "y", "z", " ",
                          "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                          ".", ",", ":", "?", "!", "(", ")", "+", "-"]
        self.image = pygame.image.load("data/Images/Menu/Text/Text (Black) (8x10).png")
        self.data = {}

    def create(self):
        temp = []
        for i in range(5):
            for t in range(10):
                sur = pygame.Surface((8, 10))
                sur.blit(self.image, (0, 0), (t * 8, i * 10, 8, 10))
                sur.set_colorkey((0, 0, 0))
                temp.append(sur)

        t = 0
        for i in range(0, 27):
            self.data[self.name[t]] = temp[i]
            t = t + 1
        for i in range(30, 49):
            self.data[self.name[t]] = temp[i]
            t = t + 1

    def get_text(self, s : str) -> list:
        temp = []
        for i in s.lower():
            if i not in self.name:
                temp.append(self.data["?"])
            else:
                temp.append(self.data[i])
        return temp
    
class Image:
    def __init__(self):
        pass

    def load_image(self, path : str):
        sur = pygame.image.load(path).convert_alpha()
        result = pygame.Surface((sur.get_width(),sur.get_height()))
        result.blit(sur, (0, 0))
        result.set_colorkey((0, 0, 0))
        return result
    
    def load_image_character(self, name):
        image = pygame.image.load(PATH_CHARCTERS + "/" + name + "/Idle (32x32).png")
        sur = pygame.Surface((32, 32))
        sur.blit(image, (0, 0), (0, 0, 32, 32))
        sur.set_colorkey((0, 0, 0))
        return sur
    
    def load_image_button(sef, name):
        return pygame.image.load(PATH_IMAGES_BUTTONS + "/" + name + ".png")
    