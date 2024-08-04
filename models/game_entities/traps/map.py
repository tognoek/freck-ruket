import pygame
from models.game_entities.entity import Entity

class Map(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)


    def render_mini_map(self, surface, offset, ratio = 0.25, offet_mini = (0, 0)):
        size = self.get_image().get_size()
        size = (int(size[0] * ratio), int(size[1] * ratio))
        sur = pygame.Surface(size)
        sur.fill((115, 27, 23))
        offsetmini = (int(offset[0] * ratio + offet_mini[0]), int(offset[1] * ratio + offet_mini[1]))
        pos = (int(self.get_pos()[0] * ratio + offsetmini[0]), 
               int(self.get_pos()[1] * ratio + offsetmini[1]))
        surface.blit(sur, pos)