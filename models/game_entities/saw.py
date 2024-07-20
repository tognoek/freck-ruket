import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character 
import math

class Saw(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.array = []
        self.array_dot = []
        self.action = "On"
        self.dot = 0
        self.sub_dot = 0

    def calculate_coordinates(self, x1, y1, x2, y2, step=1, offet = (0, 0)):
        coordinates = []
        
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        
        steps = int(distance // step)
        
        for i in range(steps + 1):
            t = i / steps
            x = x1 + t * dx - offet[0]
            y = y1 + t * dy - offet[1]
            coordinates.append((round(x), round(y)))
        
        return coordinates
    
    def collision_player(self, player : Character):
        if self.action == "On":
            for i in range(8):
                if player.collision_tognoek(self.rect(), player.data[player.action][i]):
                    player.type_entity = 3
                    return

    def create(self):
        temp = self.data.copy()
        temp.append(self.data[0])
        if len(self.data) > 1:
            for i in range(len(self.data)):
                start = (temp[i][1][0], temp[i][1][1])
                end = (temp[i+1][1][0], temp[i+1][1][1])
                self.array.append(self.calculate_coordinates(start[0], start[1], end[0], end[1], 1, (16, 16)))
                self.array_dot.append(self.calculate_coordinates(start[0], start[1], end[0], end[1], 8))
        else:
            start = (temp[0][1][0] - 16, temp[0][1][1] - 16)
            self.array = [[start]]
            start = (temp[0][1][0], temp[0][1][1])
            self.array_dot = [[start]]

    def render(self, surface : pygame.Surface, offset):
        self.pos = self.array[self.dot][self.sub_dot]

        for i in self.array_dot:
            for t in i:
                surface.blit(self.images["Chain"][0], (t[0] + offset[0], t[1] + offset[1]))
        super().render(surface, offset)

        self.sub_dot += 1
        if self.sub_dot == len(self.array[self.dot]):
            self.sub_dot = 0
            self.dot += 1
            if self.dot == len(self.array):
                self.dot = 0