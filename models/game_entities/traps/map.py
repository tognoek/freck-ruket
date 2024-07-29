import pygame
from models.game_entities.entity import Entity

class Map(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
