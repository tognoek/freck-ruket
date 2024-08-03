import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character

class CheckPoint(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, 
                 size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_action = True
        self.next_level = False

    def collision_player(self, player : Character):
        if self.is_action and player.rate_play == 100:
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            other_rect = pygame.Rect((x, y),(w, h))       
            if self.type_entity == 1:
                for i in range(8):
                    if player.collision_tognoek(other_rect, player.data[player.action][i]):
                        self.set_action("On")
                        self.is_action = False
                        break


    def update(self, loop=True):
        if super().update(loop):
            if self.action == "On":
                self.set_action("On_Idle")
            if self.action == "On_Idle":
                if self.loop_frame == 3:
                    self.next_level = True

    
