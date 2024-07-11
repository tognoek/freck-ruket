import pygame
import json
import os
from ENV import PATH_CHARCTERS, PATH_MAPS, PATH_BACKGROUND, PATH_TRAPS


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
    
    def load_image_trap(self, name, rotate = 0):
        data = self.file_json["Images"]["Traps"][name]
        images = {}
        frames = {}
        for attribute, values in data.items():
            path = PATH_TRAPS + "/" + name + "/" + attribute + " (" + values["Size"] + ").png"
            x, y = map(int , values["Size"].split("x"))
            images[attribute] = self.cut_image(path, int(values["Frame"]), (x, y), rotate)
            frames[attribute] = int(values["Frame"])
        
        return images, frames
    
    def load_data_charactre(self, name):
        return self.data_error["Points Collision"]["Main Characters"][name] 
    def load_data_traps(self, name):
        return self.data_error["Points Collision"]["Traps"][name] 

    def load_data_maps(self):
        images = {}
        for filename in os.listdir(PATH_MAPS):
            file_path = os.path.join(PATH_MAPS, filename)
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
