import pygame
from models.game_entities.entity import Entity

class Broken(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, 
                 frame, size_frame = 5, type_entity = 1, z_index = 1, 
                 data = None, speed = (0, 0), action = "Broken"):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.live = 3
        self.is_die_broken = False
        self.action = action
        self.speed = speed

    def is_die(self):
        return self.is_die_broken
    
    def update(self, loop=True):
        self.speed[1] += 0.3
        if self.speed[1] > 4:
            self.speed[1] = 4
        self.pos = (self.pos[0] + self.speed[0], self.pos[1] + self.speed[1])
        if super().update(loop):
            self.live -= 1
            if self.live < 0:
                self.is_die_broken = True