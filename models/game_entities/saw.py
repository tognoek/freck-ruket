import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character 
import math

class Saw(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.array = []
        self.action = "On"
        self.dot = 0
        self.sub_dot = 0

    def calculate_coordinates(self, x1, y1, x2, y2, step=1):
        coordinates = []
        
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        
        steps = int(distance // step)
        
        for i in range(steps + 1):
            t = i / steps
            x = x1 + t * dx
            y = y1 + t * dy
            coordinates.append((round(x), round(y)))
        
        return coordinates

    def create(self):
        temp = self.data.copy()
        temp.append(self.data[0])
        for i in range(len(self.data)):
            start = (temp[i][2][0], temp[i][2][1])
            end = (temp[i+1][2][0], temp[i+1][2][1])
            print(start, end)
            self.array.append(self.calculate_coordinates(start[0], start[1], end[0], end[1]))

    def render(self, surface, offset):
        self.pos = self.array[self.dot][self.sub_dot]

        super().render(surface, offset)

        self.sub_dot += 1
        if self.sub_dot == len(self.array[self.dot]):
            self.sub_dot = 0
            self.dot += 1
            if self.dot == len(self.array):
                self.dot = 0