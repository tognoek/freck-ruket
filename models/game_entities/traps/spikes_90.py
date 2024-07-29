import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character

class Spikes_90(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True

    def collision_player(self, player : Character):
        if self.is_active:
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            if self.flip[0]:
                 x = self.get_pos()[0]
            else:
                x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            other_rect = pygame.Rect((x, y),(w, h))
            player_rect = player.rect()
            if self.type_entity == 1:
                if player.speed[0] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][2]):
                         player.type_entity = 3
                    if player.collision_tognoek(other_rect, player.data[player.action][3]):
                         player.type_entity = 3
                if player.speed[0] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][6]):
                         player.type_entity = 3
                    if player.collision_tognoek(other_rect, player.data[player.action][7]):
                         player.type_entity = 3
                
                player.pos = (player_rect.x, player.pos[1])
            player_rect = player.rect()
            if self.type_entity == 1:
                if player.speed[1] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][0]):
                         player.type_entity = 3
                    if player.collision_tognoek(other_rect, player.data[player.action][1]):
                         player.type_entity = 3
                if player.speed[1] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][4]):
                         player.type_entity = 3
                    if player.collision_tognoek(other_rect, player.data[player.action][5]):
                         player.type_entity = 3
                player.pos = (player.pos[0], player_rect.y)

