import pygame
from entity import Entity

class Block(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
    